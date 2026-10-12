#!/usr/bin/env python3
"""REC-01 regression and executable checks; synthetic fixtures, never commits."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import runpy
import shlex
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from contextlib import redirect_stderr
from io import StringIO

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "canonical/skills/git-commit/scripts/check_secrets.py"
WRAPPER = ROOT / "tools/check_secrets.py"
TEMP_DIR = os.environ.get("AI_AGENTS_TEST_TMP")


def synthetic_token(prefix: str = "ghp") -> bytes:
    return (prefix + "_" + "Z9" * 18).encode()


def synthetic_key(kind: str = "RSA ") -> bytes:
    return ("-----" + "BEGIN " + kind + "PRIVATE KEY" + "-----\nfictional\n").encode()


class ContractTests(unittest.TestCase):
    def test_no_unconditional_sensitive_override(self):
        text = (ROOT / "canonical/skills/git-commit/SKILL.md").read_text()
        for phrase in ("Nunca bloquees el flujo: el usuario decide.",
                       "**No bloquees ni canceles el commit.**",
                       "Incluirlo de todas formas — necesito tu autorización explícita."):
            self.assertTrue(phrase not in text, "Permanece una autorización genérica de sensibles")

    def test_consumers_preserve_non_overridable_exclusion(self):
        for relative in ("canonical/skills/git-commit/SKILL.md",
                         "canonical/skills/release-management/SKILL.md",
                         "canonical/skills/security/SKILL.md",
                         "canonical/agents/git-release-manager.md",
                         "docs/agentes/git-release-manager.md"):
            text = (ROOT / relative).read_text().casefold()
            self.assertIn("secretos confirmados", text, relative)
            self.assertIn("autorización", text, relative)


class ScannerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="rec01-", dir=TEMP_DIR)
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.repo = self.base / "repo"
        self.repo.mkdir()
        self.env = dict(os.environ, GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)
        self.git("init", "--quiet")

    def git(self, *args):
        result = subprocess.run(["git", "-C", str(self.repo), *args],
                                env=self.env, capture_output=True)
        self.assertEqual(result.returncode, 0, "Preparación Git del fixture fallida")
        return result.stdout

    def write(self, name: str, content: bytes):
        path = self.repo / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        return path

    def scan(self, *args, entry=SCRIPT, code=0, forbidden=b""):
        result = subprocess.run([sys.executable, str(entry), "--repo", str(self.repo), *args],
                                env=self.env, capture_output=True)
        output = result.stdout + result.stderr
        if forbidden:
            self.assertTrue(forbidden not in output, "Diagnóstico expone valor sintético")
        self.assertTrue(b"Traceback" not in output, "Diagnóstico incluye traceback")
        self.assertEqual(result.returncode, code, "Código de salida inesperado")
        return result

    def snapshot(self):
        return {str(p.relative_to(self.repo)): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in self.repo.rglob("*") if p.is_file() and not p.is_symlink()}

    def test_scan_detects_signature(self):
        detect = runpy.run_path(str(SCRIPT))["scan_content"]
        self.assertTrue(detect(synthetic_token()), "La regla no detecta la firma sintética")

    def test_detectable_content_in_normal_and_suspicious_names(self):
        value = synthetic_token()
        for name in ("Config.kt", ".env"):
            with self.subTest(name=name):
                self.write(name, b"token=" + value)
                self.scan(name, code=1, forbidden=value)

    def test_public_and_placeholders_not_blocked_by_name(self):
        for name, content in ((".env", b"API_URL=https://example.invalid\nTOKEN=${TOKEN}\n"),
                              ("google-services.json", b'{"project_id":"public-demo"}'),
                              ("credentials.example", b"token=YOUR_TOKEN\npassword=<placeholder>")):
            with self.subTest(name=name):
                self.write(name, content)
                self.scan(name)

    def test_supported_token_families(self):
        for prefix in ("ghp", "gho", "ghu", "ghs", "ghr"):
            with self.subTest(prefix=prefix):
                value = synthetic_token(prefix)
                self.write("config", value)
                self.scan("config", code=1, forbidden=value)
        value = ("github" + "_pat_" + "A" * 22 + "_" + "B" * 59).encode()
        self.write("config", value)
        self.scan("config", code=1, forbidden=value)

    def test_supported_private_headers(self):
        for kind in ("", "RSA ", "EC ", "DSA ", "OPENSSH ", "ENCRYPTED "):
            with self.subTest(kind=kind):
                value = synthetic_key(kind)
                self.write("config", value)
                self.scan("config", code=1, forbidden=value.splitlines()[0])

    def test_index_is_not_worktree(self):
        value = synthetic_token()
        self.write("config", value)
        self.git("add", "config")
        self.write("config", b"TOKEN=YOUR_TOKEN")
        self.scan("--staged", code=1, forbidden=value)
        self.scan("--tracked")
        self.git("add", "config")
        self.write("config", value)
        self.scan("--staged")
        self.scan("--tracked", code=1, forbidden=value)

    def test_control_is_read_only(self):
        self.write("config", synthetic_token())
        self.git("add", "config")
        before = self.snapshot()
        self.scan("--staged", code=1, forbidden=synthetic_token())
        self.assertTrue(before == self.snapshot(), "El control modificó el fixture/índice/refs")

    def test_public_staged_and_empty_index(self):
        self.scan("--staged")
        self.write(".env", b"API_URL=https://example.invalid\nTOKEN=<placeholder>")
        self.git("add", ".env")
        self.scan("--staged")

    def test_missing_path_and_invalid_repository(self):
        self.scan("missing", code=2)
        result = subprocess.run([sys.executable, str(SCRIPT), "--repo", str(self.base), "--staged"],
                                capture_output=True)
        self.assertEqual(result.returncode, 2)
        self.assertNotIn(b"Traceback", result.stderr)

    def test_external_paths_rejected(self):
        self.scan("../outside", code=2)
        self.scan(str(self.base / "outside"), code=2)

    def test_symlink_is_not_followed(self):
        outside = self.base / "outside"
        value = synthetic_token()
        outside.write_bytes(value)
        (self.repo / "link").symlink_to(outside)
        self.scan("link", code=2, forbidden=value)
        self.git("add", "link")
        self.scan("--staged", code=2, forbidden=value)
        self.scan("--tracked", code=2, forbidden=value)

    def test_control_characters_and_sensitive_path_sanitized(self):
        value = synthetic_token()
        name = value.decode() + "\nconfig"
        self.write(name, value)
        result = self.scan(name, code=1, forbidden=value)
        self.assertIn(b"[REDACTED]", result.stdout)

    def test_no_authorization_override(self):
        self.write("config", synthetic_token())
        self.scan("config", "--allow-secret", code=2, forbidden=synthetic_token())

    @unittest.skipUnless(os.name == "posix", "Cadena shell POSIX")
    def test_rejected_control_prevents_following_operation(self):
        value = synthetic_token()
        self.write("config", value)
        self.git("add", "config")
        sentinel = self.base / "publication-was-called"
        # This is a fake following operation, never git commit.
        following = "from pathlib import Path; Path(" + repr(str(sentinel)) + ").touch()"
        first = shlex.join([sys.executable, str(SCRIPT), "--repo", str(self.repo), "--staged"])
        second = shlex.join([sys.executable, "-c", following])
        result = subprocess.run(["/bin/sh", "-c", first + " && " + second],
                                env=self.env, capture_output=True)
        self.assertEqual(result.returncode, 1)
        self.assertFalse(sentinel.exists(), "Se ejecutó una operación después del rechazo")
        self.assertTrue(value not in result.stdout + result.stderr, "Cadena expone fixture")

    def test_argument_error_does_not_echo_value(self):
        value = synthetic_token()
        self.scan("--" + value.decode(), code=2, forbidden=value)

    def test_conflicted_index_is_incomplete(self):
        self.write("config", b"public")
        self.git("add", "config")
        oid = self.git("rev-parse", ":config").strip()
        data = b"0 " + b"0" * len(oid) + b"\tconfig\n"
        data += b"100644 " + oid + b" 1\tconfig\n"
        result = subprocess.run(["git", "-C", str(self.repo), "update-index", "--index-info"],
                                input=data, env=self.env, capture_output=True)
        self.assertEqual(result.returncode, 0, "Preparación de conflicto fallida")
        self.scan("--staged", code=2)

    def test_submodule_index_is_incomplete(self):
        self.write("config", b"public")
        self.git("add", "config")
        oid = self.git("rev-parse", ":config").strip().decode()
        self.git("update-index", "--add", "--cacheinfo", "160000," + oid + ",module")
        self.scan("--staged", code=2)

    def test_directory_symlink_and_nonfile_rejected(self):
        (self.repo / "dir").symlink_to(self.base, target_is_directory=True)
        self.scan("dir/file", code=2)
        self.scan(".git", code=2)

    def test_incompatible_modes_and_missing_input(self):
        self.scan("--staged", "--tracked", code=2)
        self.scan("--staged", "config", code=2)
        self.scan(code=2)

    def test_line_numbers_without_content(self):
        value = synthetic_token()
        self.write("config", b"public\n\n" + value + b"\n")
        result = self.scan("config", code=1, forbidden=value)
        self.assertIn(b":3:", result.stdout)

    def test_read_error_is_sanitized(self):
        value = synthetic_token()
        self.write("config", value)
        main = runpy.run_path(str(SCRIPT))["main"]
        output = StringIO()
        with patch.object(Path, "read_bytes", side_effect=OSError(value.decode())):
            with redirect_stderr(output):
                code = main(["--repo", str(self.repo), "config"])
        self.assertEqual(code, 2)
        self.assertTrue(value.decode() not in output.getvalue(), "Error expone valor sintético")

    def test_staged_deleted_worktree_can_still_be_evaluated(self):
        value = synthetic_token()
        path = self.write("config", value)
        self.git("add", "config")
        path.unlink()
        self.scan("--staged", code=1, forbidden=value)
        self.scan("--tracked", code=2, forbidden=value)

    def test_git_control_does_not_use_inherited_index(self):
        self.write("config", synthetic_token())
        self.git("add", "config")
        self.env["GIT_INDEX_FILE"] = str(self.base / "unrelated-index")
        self.scan("--staged", code=1, forbidden=synthetic_token())

    def test_wrapper_ci_and_distributions(self):
        value = synthetic_token()
        self.write("config", value)
        self.git("add", "config")
        self.scan("--tracked", entry=WRAPPER, code=1, forbidden=value)
        platforms = json.loads((ROOT / "canonical/manifest.json").read_text())["platforms"]
        for platform in platforms:
            with self.subTest(platform=platform):
                entry = ROOT / "generated" / platform / "skills/git-commit/scripts/check_secrets.py"
                self.assertTrue(entry.read_bytes() == SCRIPT.read_bytes(), "Distribución difiere de fuente")
                self.scan("--staged", entry=entry, code=1, forbidden=value)


if __name__ == "__main__":
    unittest.main()
