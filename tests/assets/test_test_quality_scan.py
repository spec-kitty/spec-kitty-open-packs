"""Behavioural fixtures for the Python front end of test-quality-scan."""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCANNER_PATH = ROOT / "packs" / "internal" / "assets" / "test-quality-scan.py"
FIXTURES = ROOT / "tests" / "fixtures" / "test_quality_scan" / "python"
_spec = importlib.util.spec_from_file_location("test_quality_scan", SCANNER_PATH)
scanner = importlib.util.module_from_spec(_spec)
sys.modules["test_quality_scan"] = scanner
_spec.loader.exec_module(scanner)


class PythonFrontendTest(unittest.TestCase):
    def scan(self, name: str) -> tuple[object, dict[str, list[str]]]:
        relative = (FIXTURES / name).relative_to(ROOT).as_posix()
        row, rows = scanner.scan_file(ROOT, relative, None)
        return row, {test.test: test.flags for test in rows}

    def test_oracle_flags_are_exact(self) -> None:
        row, actual = self.scan("test_oracles.py")
        self.assertEqual(
            {
                "test_without_an_oracle": ["no-assertion"],
                "test_only_checks_non_none": ["weak-only-assert"],
                "test_only_checks_type": ["type-only-assert"],
                "test_catches_any_exception": ["broad-raises"],
            },
            actual,
        )
        self.assertEqual(6, row.tests)
        self.assertEqual(4, row.flagged_tests)

    def test_smell_flags_are_exact(self) -> None:
        row, actual = self.scan("test_smells.py")
        self.assertEqual(
            {
                "test_mock_call_interaction": ["interaction-assert"],
                "test_too_many_mocks": ["over-mocking"],
                "test_reads_private_attributes": ["private-attr"],
                "test_scans_source_literally": ["literal-source-scan"],
                "test_pins_a_source_line": ["line-number-pin"],
                "test_uses_a_fake_mission_id": ["fake-short-ulid"],
                "test_sleeps": ["sleep"],
                "test_reads_current_time": ["wallclock"],
                "test_is_skipped": ["skip-or-xfail"],
            },
            actual,
        )
        self.assertEqual(9, row.tests)
        self.assertEqual(9, row.flagged_tests)

    def test_shape_flags_are_exact(self) -> None:
        row, actual = self.scan("test_shapes.py")
        self.assertEqual(
            {
                "test_1": ["vague-name"],
                "test_many_assertions": ["many-asserts"],
                "test_issue_123_regression": ["provenance-tokens"],
                "test_a_long_behaviour": ["long-test"],
            },
            actual,
        )
        self.assertEqual(5, row.tests)
        self.assertEqual(4, row.flagged_tests)

    def test_unparseable_file_is_a_file_level_finding(self) -> None:
        row, actual = self.scan("test_unparseable.py")
        self.assertEqual({}, actual)
        self.assertEqual(0, row.tests)
        self.assertEqual({"unparseable": 1}, row.flags)

    def test_discovery_and_domains(self) -> None:
        relative = FIXTURES.relative_to(ROOT).as_posix()
        self.assertEqual(
            [
                f"{relative}/test_oracles.py",
                f"{relative}/test_shapes.py",
                f"{relative}/test_smells.py",
                f"{relative}/test_unparseable.py",
            ],
            scanner.collect_paths(ROOT, [relative]),
        )
        self.assertEqual("(root)", scanner.domain_of("tests/test_root.py"))
        self.assertEqual("status", scanner.domain_of("tests/status/test_status.py"))
        self.assertEqual(
            "specify_cli/commands",
            scanner.domain_of("tests/specify_cli/commands/test_command.py"),
        )


if __name__ == "__main__":
    unittest.main()
