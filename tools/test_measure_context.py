#!/usr/bin/env python3
"""Tests for explicit source-volume measurement; no token claims."""

from __future__ import annotations

from pathlib import Path
import unittest

import measure_context


class ContextMeasurementTests(unittest.TestCase):
    def test_measures_only_explicit_unique_files(self):
        path = "README.md"
        result = measure_context.measure([path, path])
        source = (measure_context.ROOT / path).read_text(encoding="utf-8")
        self.assertEqual(result["file_count"], 1)
        self.assertEqual(result["totals"]["characters"], len(source))
        self.assertEqual(result["totals"]["words"], len(source.split()))
        self.assertIn("not actual prompt/token usage", result["measurement"])

    def test_rejects_paths_outside_repository(self):
        for path in ("../outside.md", str(measure_context.ROOT / "README.md")):
            with self.subTest(path=path), self.assertRaises(ValueError):
                measure_context.measure([path])

    def test_rejects_missing_source(self):
        with self.assertRaises(ValueError):
            measure_context.measure(["docs/__missing_measure_fixture__.md"])

    def test_can_compare_source_volume_to_git_baseline(self):
        result = measure_context.measure(["README.md"], "HEAD")
        item = result["files"][0]
        self.assertIsNotNone(item["baseline"])
        self.assertEqual(item["delta"]["bytes"], item["bytes"] - item["baseline"]["bytes"])

    def test_rejects_symlink_sources(self):
        link = measure_context.ROOT / ".measure-context-test-link"
        try:
            link.symlink_to(measure_context.ROOT / "README.md")
            with self.assertRaises(ValueError):
                measure_context.measure([link.name])
        finally:
            if link.is_symlink():
                link.unlink()


if __name__ == "__main__":
    unittest.main()
