#!/usr/bin/env python3
"""Opt-in OpenCode engine probe, real tools + local simulated Anthropic provider.

No LLM behavioral claim, human-consent claim, credentials, or global installation.
Exit 0: listed engine scenarios passed; 1: assertion failure; 2: unavailable host.
"""
from __future__ import annotations

import json
import argparse
import os
import re
import shutil
import shlex
import socket
import subprocess
import tempfile
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent.parent


class Provider(BaseHTTPRequestHandler):
    def log_message(self, *_):
        pass

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"public local permission fixture\n")

    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        self.server.requests += 1
        self.server.available_tools = {tool["name"] for tool in body.get("tools", [])}
        messages = body.get("messages", [])
        scenario = None
        for message in messages:
            if message.get("role") != "user":
                continue
            content = message.get("content", [])
            if isinstance(content, str):
                content = [{"type": "text", "text": content}]
            for part in content:
                if part.get("type") == "text" and "REC02_CASE " in part.get("text", ""):
                    raw = part["text"].split("REC02_CASE ", 1)[1]
                    scenario = json.JSONDecoder().raw_decode(raw)[0]
        last = messages[-1].get("content", []) if messages else []
        finished = isinstance(last, list) and any(p.get("type") == "tool_result" for p in last)
        tool = scenario["tool"] if scenario and not finished else None
        if tool and tool not in {t["name"] for t in body.get("tools", [])}:
            self.server.missing_tools.add(tool)
            tool = None
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.end_headers()

        def event(kind, data):
            self.wfile.write(("event: " + kind + "\ndata: " + json.dumps({"type": kind, **data}) + "\n\n").encode())

        event("message_start", {"message": {"id": "msg_fixture", "type": "message", "role": "assistant",
              "model": body.get("model"), "content": [], "stop_reason": None,
              "usage": {"input_tokens": 1, "output_tokens": 0}}})
        if tool:
            event("content_block_start", {"index": 0, "content_block": {"type": "tool_use",
                  "id": "tool_fixture", "name": tool, "input": {}}})
            event("content_block_delta", {"index": 0, "delta": {"type": "input_json_delta",
                  "partial_json": json.dumps(scenario["args"])}})
        else:
            event("content_block_start", {"index": 0, "content_block": {"type": "text", "text": ""}})
            event("content_block_delta", {"index": 0, "delta": {"type": "text_delta", "text": "fixture complete"}})
        event("content_block_stop", {"index": 0})
        event("message_delta", {"delta": {"stop_reason": "tool_use" if tool else "end_turn",
              "stop_sequence": None}, "usage": {"output_tokens": 1}})
        event("message_stop", {})
        self.wfile.flush()


def free_port():
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def main():
    executable = shutil.which("opencode")
    if not executable:
        print("BLOCKED: OpenCode CLI no disponible; ningún escenario ejecutado.")
        return 2
    with tempfile.TemporaryDirectory(prefix="rec02-host-", dir=os.environ.get("AI_AGENTS_TEST_TMP")) as temp:
        base = Path(temp).resolve()
        repo = base / "repo"
        home = base / "home"
        repo.mkdir()
        home.mkdir()
        for domain in (".architecture", ".navigator", ".data", ".design", ".quality", ".security", "src"):
            (repo / domain).mkdir()
        agents = repo / ".opencode/agents"
        agents.mkdir(parents=True)
        for agent in ("documentation-orchestrator", "code-review", "sdd"):
            shutil.copyfile(ROOT / "generated/opencode/agents" / f"{agent}.md", agents / f"{agent}.md")
        provider = ThreadingHTTPServer(("127.0.0.1", 0), Provider)
        provider.missing_tools = set()
        provider.requests = 0
        provider.available_tools = set()
        thread = threading.Thread(target=provider.serve_forever, daemon=True)
        thread.start()
        config = {"$schema": "https://opencode.ai/config.json", "autoupdate": False,
                  "share": "disabled", "snapshot": False, "plugin": [], "formatter": False, "lsp": False,
                  "model": "anthropic/rec02-fixture", "enabled_providers": ["anthropic"],
                  "provider": {"anthropic": {"models": {"rec02-fixture": {
                      "name": "REC02 local fixture", "tool_call": True,
                      "limit": {"context": 128000, "output": 4096}}}, "options": {
                      "baseURL": f"http://127.0.0.1:{provider.server_port}/v1", "apiKey": "public-fixture"}}},
                  # Deliberately permissive globals exercise agent precedence.
                  "permission": {"edit": "allow", "external_directory": "allow", "task": "allow",
                                 "bash": {"*": "allow", "git status*": "allow", "python3 *": "allow", "rm *": "allow"}},
                  "agent": {"title": {"disable": True}, "summary": {"disable": True}}}
        env = {key: os.environ[key] for key in ("PATH", "LANG", "TMPDIR", "SYSTEMROOT") if key in os.environ}
        env.update(HOME=str(home), USERPROFILE=str(home), XDG_CONFIG_HOME=str(base / "config"),
                   XDG_DATA_HOME=str(base / "data"), XDG_CACHE_HOME=str(base / "cache"),
                   XDG_STATE_HOME=str(base / "state"), GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull,
                   OPENCODE_DISABLE_EXTERNAL_SKILLS="1", OPENCODE_DISABLE_CLAUDE_CODE_SKILLS="1",
                   OPENCODE_DISABLE_MODELS_FETCH="1",
                   OPENCODE_DISABLE_DEFAULT_PLUGINS="1", OPENCODE_CONFIG_CONTENT=json.dumps(config))
        subprocess.run(["git", "init", "--quiet", str(repo)], env=env, check=True, capture_output=True)
        port = free_port()
        log_path = base / "host.log"
        log_stream = log_path.open("wb")
        process = subprocess.Popen([executable, "serve", "--pure", "--print-logs", "--log-level", "DEBUG",
                                    "--hostname", "127.0.0.1", "--port", str(port)],
                                   cwd=repo, env=env, stdout=log_stream, stderr=log_stream)
        url = f"http://127.0.0.1:{port}"

        def request(path, body=None):
            data = None if body is None else json.dumps(body).encode()
            req = Request(url + path, data=data, headers={"Content-Type": "application/json"})
            try:
                with urlopen(req, timeout=20) as response:
                    value = response.read()
                    return json.loads(value) if value else None
            except HTTPError as error:
                # Isolated fixture API only; no user credentials or project content.
                detail = error.read().decode(errors="replace").replace(str(base), "<fixture>")
                raise AssertionError(f"fixture API {path}: HTTP {error.code}: {detail[:800]}") from error

        try:
            deadline = time.monotonic() + 60
            while True:
                try:
                    health = request("/global/health")
                    break
                except (URLError, TimeoutError):
                    if process.poll() is not None or time.monotonic() > deadline:
                        print("BLOCKED: servidor aislado no inició; no es PASS.")
                        return 2
                    time.sleep(0.2)
            print("HOST: OpenCode " + health["version"] + "; perfil temporal; proveedor local simulado.")
            scenario_count = 0

            def scenario(label, tool, args, decision, expected, target=None, agent="documentation-orchestrator"):
                nonlocal scenario_count
                scenario_count += 1
                session = request("/session", {"title": "REC02 " + label})["id"]
                request(f"/session/{session}/prompt_async", {"agent": agent,
                        "parts": [{"type": "text", "text": "REC02_CASE " + json.dumps({"tool": tool, "args": args})}]})
                approvals = []
                deadline = time.monotonic() + 35
                parts = []
                while time.monotonic() < deadline:
                    for permission in request("/permission"):
                        if permission["sessionID"] == session:
                            approvals.append(permission["permission"])
                            request(f"/permission/{permission['id']}/reply", {"reply": decision})
                    messages = request(f"/session/{session}/message")
                    parts = [p for m in messages for p in m["parts"] if p["type"] == "tool" and p["tool"] == tool]
                    if any(m["info"].get("finish") == "stop" for m in messages):
                        break
                    status = request("/session/status").get(session, {"type": "idle"})
                    if parts and all(p["state"]["status"] in ("completed", "error") for p in parts) and status["type"] == "idle":
                        break
                    if any(m["info"].get("error") for m in messages):
                        raise AssertionError(label + ": host devolvió error; detalles omitidos")
                    time.sleep(0.1)
                else:
                    request(f"/session/{session}/abort", {})
                    summary = [{"role": m["info"]["role"], "finish": m["info"].get("finish"),
                                "parts": [p["type"] for p in m["parts"]]} for m in messages]
                    log = log_path.read_text(errors="replace")
                    services = list(dict.fromkeys(re.findall(r"service=([\w.-]+)", log)))
                    stages = [word for word in ("install", "bun", "loading", "provider", "error", "npm") if word in log.lower()]
                    errors = []
                    for line in log.splitlines():
                        if "error" not in line.lower():
                            continue
                        for key, value in re.findall(r'"(message|error|name)"\s*:\s*"([^"\n]{1,200})"', line):
                            errors.append(key + "=" + value.replace(str(base), "<fixture>"))
                        if not errors:
                            errors.append(re.sub(r'\x1b\[[0-9;]*m', '', line).replace(str(base), "<fixture>")[:200])
                    raise AssertionError(label + ": timeout; no es PASS; provider_requests=" +
                                         str(provider.requests) + "; estados=" + json.dumps(summary) +
                                         "; servicios=" + ",".join(services) + "; señales=" + ",".join(stages) +
                                         "; errores=" + str(errors[-4:]))
                assert tool not in provider.missing_tools, label + ": tool no expuesta"
                assert len(parts) == 1, label + ": no hubo un intento de tool único"
                state = parts[0]["state"]["status"]
                detail = str(parts[0]["state"].get("error", "")).replace(str(base), "<fixture>")[:600]
                assert state == expected, label + ": estado " + state + ", esperado " + expected + "; " + detail
                if expected == "error":
                    assert any(word in detail.lower() for word in ("permission", "denied", "rejected", "rule")), label + ": error no atribuible a permisos"
                    if decision == "reject":
                        assert approvals, label + ": no hubo solicitud de consentimiento"
                if decision == "once" and expected == "completed":
                    assert approvals, label + ": ejecutó sin aprobación pese a ask de agente"
                    if tool == "bash":
                        metadata = parts[0]["state"].get("metadata", {})
                        assert metadata.get("exit", 0) == 0, label + ": comando no terminó correctamente"
                if target:
                    assert target.exists() == (expected == "completed"), label + ": efecto de archivo incorrecto"
                    if target.exists():
                        assert target.read_text() == "rec02-fixture\n", label + ": contenido incorrecto"
                prefix = "LIMITATION observada: " if label.startswith("limitacion-") else "PASS engine: "
                print(prefix + label + "; tool=" + tool + "; state=" + state +
                      "; permisos=" + ",".join(approvals) + "; decision=" + decision)

            def write(label, relative, decision, expected, agent="documentation-orchestrator"):
                target = repo / relative
                scenario(label, "write", {"filePath": str(target), "content": "rec02-fixture\n"},
                         decision, expected, target, agent)

            write("documentacion-aprobada", ".architecture/approved.txt", "once", "completed")
            write("documentacion-rechazada", ".data/rejected.txt", "reject", "error")
            write("agents-guia-rechazada", "AGENTS.md", "reject", "error")
            write("agents-guia-aprobada", "AGENTS.md", "once", "completed")
            write("docs-guia-rechazada", "docs/extra-tools/rejected.md", "reject", "error")
            write("docs-guia-aprobada", "docs/extra-tools/README.md", "once", "completed")
            write("docs-codigo-denegado", "docs/script.py", "once", "error")
            write("docs-configuracion-denegada", "docs/config.json", "once", "error")
            scenario("docs-edicion-aprobada", "edit", {
                "filePath": str(repo / "docs/extra-tools/README.md"),
                "oldString": "rec02-fixture", "newString": "rec02-fixture-edited"}, "once", "completed")
            assert (repo / "docs/extra-tools/README.md").read_text() == "rec02-fixture-edited\n"
            scenario("agents-edicion-aprobada", "edit", {
                "filePath": str(repo / "AGENTS.md"),
                "oldString": "rec02-fixture", "newString": "rec02-fixture-edited"}, "once", "completed")
            assert (repo / "AGENTS.md").read_text() == "rec02-fixture-edited\n"
            if "apply_patch" in provider.available_tools:
                patch = ("*** Begin Patch\n*** Update File: " + str(repo / "AGENTS.md") +
                         "\n@@\n-rec02-fixture-edited\n+rec02-combined\n*** Update File: " +
                         str(repo / "docs/extra-tools/README.md") +
                         "\n@@\n-rec02-fixture-edited\n+rec02-combined\n*** End Patch")
                scenario("docs-agents-parche-combinado", "apply_patch", {"patchText": patch}, "once", "completed")
                for relative in ("AGENTS.md", "docs/extra-tools/README.md"):
                    assert (repo / relative).read_text() == "rec02-combined\n", relative
            else:
                print("NOT VERIFIED: apply_patch no expuesta por este perfil/modelo; parche combinado cubierto solo estáticamente.")
            write("otras-instrucciones-denegadas", "CLAUDE.md", "once", "error")
            write("producto-fuera-de-alcance", "src/denied.txt", "once", "error")
            write("spec-fuera-de-alcance", ".sdd/denied.txt", "once", "error")
            write("externo-fuera-de-alcance", "../outside.txt", "once", "error")
            write("remediacion-especialista-aprobada", "src/remediation.txt", "once", "completed", "code-review")
            scenario("consulta-git-aprobada", "bash", {"command": "git status --short", "description": "fixture query"},
                     "once", "completed")
            scenario("catchall-especialista-sobre-allow-global-especifico", "bash", {
                      "command": "git status --short", "description": "fixture agent precedence"},
                      "once", "completed", agent="code-review")
            for specialist in ("code-review", "sdd"):
                write(specialist + "-escritura-rechazada", "src/" + specialist + "-rejected.txt",
                      "reject", "error", specialist)
                scenario(specialist + "-shell-rechazado", "bash", {
                         "command": "git status --short", "description": "fixture approval rejection"},
                         "reject", "error", agent=specialist)
                for decision, expected in (("reject", "error"), ("once", "completed")):
                    scenario(specialist + "-webfetch-" + decision, "webfetch", {
                             "url": f"http://127.0.0.1:{provider.server_port}/fixture", "format": "text", "timeout": 10},
                             decision, expected, agent=specialist)
            scenario("git-escritura-denegada", "bash", {"command": "git add --dry-run src", "description": "fixture dry-run"},
                     "once", "error")
            scenario("rm-denegado", "bash", {"command": "rm nonexistent-rec02-fixture", "description": "fixture missing path"},
                     "once", "error")
            command = "python3 -c \"from pathlib import Path; Path('.architecture/shell.txt').write_text('rec02-fixture\\n')\""
            scenario("shell-documental-aprobado", "bash", {"command": command, "description": "fixture write"},
                     "once", "completed", repo / ".architecture/shell.txt")
            command = "python3 -c \"from pathlib import Path; Path('src/rejected-shell.txt').write_text('rec02-fixture\\n')\""
            scenario("shell-fuera-de-alcance-rechazado", "bash", {"command": command, "description": "fixture rejection"},
                     "reject", "error", repo / "src/rejected-shell.txt")
            scenario("comando-compuesto-rechazado", "bash", {"command": "git status --short && " + command,
                     "description": "fixture compound rejection"}, "reject", "error", repo / "src/rejected-shell.txt")
            (base / "outside/.data").mkdir(parents=True)
            write("dominio-externo-rechazado", "../outside/.data/rejected.txt", "reject", "error")
            command = "python3 -c \"from pathlib import Path; Path('src/approved-shell.txt').write_text('rec02-fixture\\n')\""
            scenario("limitacion-shell-aprobado-fuera-de-raices", "bash", {"command": command,
                     "description": "fixture documenting residual boundary"}, "once", "completed", repo / "src/approved-shell.txt")
            (repo / ".architecture/link").symlink_to(repo / "src", target_is_directory=True)
            write("limitacion-enlace-dentro-de-workspace", ".architecture/link/symlink.txt", "once", "completed")
            print(f"PASS: {scenario_count} escenarios (incluidas 2 limitaciones observadas); no acredita conducta LLM ni consentimiento humano.")
            return 0
        except (AssertionError, OSError, ValueError, KeyError) as error:
            print("FAIL/BLOCKED: " + str(error))
            return 1
        finally:
            process.terminate()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
            provider.shutdown()
            provider.server_close()
            thread.join(timeout=5)
            log_stream.close()


def available_host_probe(host):
    """Probe other available surfaces without inheriting user configuration."""
    executable = shutil.which("pi" if host == "pi" else "kiro-cli")
    if not executable:
        print("BLOCKED: " + host + " no disponible.")
        return 2
    with tempfile.TemporaryDirectory(prefix="rec02-" + host + "-", dir=os.environ.get("AI_AGENTS_TEST_TMP")) as temp:
        base = Path(temp).resolve()
        home, repo = base / "home", base / "repo"
        home.mkdir()
        repo.mkdir()
        env = {key: os.environ[key] for key in ("PATH", "LANG", "TMPDIR", "SYSTEMROOT") if key in os.environ}
        env.update(HOME=str(home), USERPROFILE=str(home), XDG_CONFIG_HOME=str(base / "config"),
                   XDG_DATA_HOME=str(base / "data"), XDG_CACHE_HOME=str(base / "cache"),
                   XDG_STATE_HOME=str(base / "state"), GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1")
        if host == "kiro-formats":
            path = ROOT / "generated/kiro/agents/documentation-orchestrator.md"
            try:
                result = subprocess.run([executable, "agent", "validate", "--path", str(path)],
                                        cwd=repo, env=env, capture_output=True, timeout=30)
            except subprocess.TimeoutExpired:
                print("BLOCKED: Kiro validate agotó 30 s; no es prueba de permisos runtime.")
                return 2
            print("FORMAT CHECK: Kiro 2.x validate sobre Markdown V3; exit=" + str(result.returncode) +
                  "; no acredita ejecución de permissions.rules; salida bruta omitida.")
            return 0 if not result.returncode else 2
        provider = ThreadingHTTPServer(("127.0.0.1", 0), Provider)
        provider.requests = 0
        provider.missing_tools = set()
        thread = threading.Thread(target=provider.serve_forever, daemon=True)
        thread.start()
        config = base / "pi"
        config.mkdir()
        models = {"providers": {"rec02": {"baseUrl": f"http://127.0.0.1:{provider.server_port}/v1",
                  "api": "anthropic-messages", "apiKey": "public-fixture", "models": [
                  {"id": "rec02-fixture", "name": "REC02 local fixture", "reasoning": False,
                   "input": ["text"], "contextWindow": 128000, "maxTokens": 4096,
                   "cost": {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0}}]}}}
        (config / "models.json").write_text(json.dumps(models))
        env.update(PI_CODING_AGENT_DIR=str(config), PI_OFFLINE="1", PI_TELEMETRY="0")
        template = ROOT / "generated/pi/agents/documentation-orchestrator.md"
        common = [executable, "--offline", "--no-extensions", "--no-skills", "--no-context-files",
                  "--no-themes", "--no-session", "--provider", "rec02", "--model", "rec02-fixture",
                  "--thinking", "off", "--prompt-template", str(template), "--mode", "json", "--print"]
        try:
            for label, relative, tools in (("documentacion", ".architecture/fixture.txt", None),
                                           ("guia-docs", "docs/extra-tools/README.md", None),
                                           ("guia-agents", "AGENTS.md", None),
                                           ("producto", "src/fixture.txt", None),
                                           ("exterior", "../outside.txt", None),
                                           ("consulta-sin-write", "src/blocked.txt", "read")):
                target = repo / relative
                case = {"tool": "write", "args": {"path": str(target), "content": "rec02-fixture\n"}}
                command = "/documentation-orchestrator " + shlex.quote("REC02_CASE " + json.dumps(case))
                argv = common + (["--tools", tools] if tools else []) + [command]
                result = subprocess.run(argv, cwd=repo, env=env, capture_output=True, timeout=35)
                output = result.stdout.decode(errors="replace")
                assert result.returncode == 0, label + ": Pi error, salida bruta omitida"
                assert "# Documentation Orchestrator" in output, label + ": carga de plantilla no acreditada"
                if tools:
                    assert "write" in provider.missing_tools and not target.exists(), label + ": tool no excluida"
                    print("PASS engine Pi: consulta con --tools read excluye write; no cambia plantilla distribuida.")
                else:
                    assert target.exists() and target.read_text() == "rec02-fixture\n", label + ": escritura no acreditada"
                    assert "tool_execution_end" in output, label + ": evento de ejecución ausente"
                    print("LIMITATION observada Pi: " + label + "; plantilla cargada; write ejecutada sin gate por rol.")
            print("PASS probe Pi: guías docs/ y AGENTS.md escribibles; 5 escrituras sin gate por rol + exclusión explícita de write; no conducta de LLM real.")
            return 0
        except (AssertionError, OSError, ValueError, subprocess.TimeoutExpired) as error:
            print("FAIL/BLOCKED Pi: " + str(error))
            return 1
        finally:
            provider.shutdown()
            provider.server_close()
            thread.join(timeout=5)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", choices=("opencode", "pi", "kiro-formats"), default="opencode")
    args = parser.parse_args()
    raise SystemExit(main() if args.host == "opencode" else available_host_probe(args.host))
