"""Behavioural fixtures for the Python front end of test-quality-scan."""

from __future__ import annotations

import builtins
import importlib.util
import sys
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
SCANNER_PATH = ROOT / "packs" / "internal" / "assets" / "test-quality-scan.py"
FIXTURES = ROOT / "tests" / "fixtures" / "test_quality_scan" / "python"
JAVA_FIXTURES = ROOT / "tests" / "fixtures" / "test_quality_scan" / "java"
_spec = importlib.util.spec_from_file_location("test_quality_scan", SCANNER_PATH)
scanner = importlib.util.module_from_spec(_spec)
sys.dont_write_bytecode = True
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


class JavaFrontendTest(unittest.TestCase):
    def scan(self, name: str) -> tuple[object, dict[str, list[str]]]:
        relative = f"{JAVA_FIXTURES.relative_to(ROOT).as_posix()}/src/test/java/com/acme/quality/{name}"
        row, rows = scanner.scan_file(ROOT, relative, None)
        return row, {test.test: test.flags for test in rows}

    def assert_flags(self, name: str, expected: dict[str, list[str]]) -> None:
        _, actual = self.scan(name)
        self.assertEqual(expected, actual)

    def test_oracle_flags_are_exact(self) -> None:
        self.assert_flags(
            "NoAssertionTest.java",
            {"NoAssertionTest.performsAnAction": ["no-assertion"]},
        )
        self.assert_flags(
            "WeakOnlyAssertTest.java",
            {
                "WeakOnlyAssertTest.onlyChecksTrue": ["weak-only-assert"],
                "WeakOnlyAssertTest.onlyChecksNonNull": ["weak-only-assert"],
                "WeakOnlyAssertTest.onlyChecksAssertJNonNull": ["weak-only-assert"],
            },
        )

    def test_type_and_broad_exception_flags_are_exact(self) -> None:
        self.assert_flags(
            "TypeOnlyAssertTest.java",
            {
                "TypeOnlyAssertTest.onlyChecksJunitType": ["type-only-assert"],
                "TypeOnlyAssertTest.onlyChecksAssertJType": ["type-only-assert"],
                "TypeOnlyAssertTest.onlyChecksExceptionType": ["type-only-assert"],
                "TypeOnlyAssertTest.onlyChecksJUnit4ExceptionType": ["type-only-assert"],
                "TypeOnlyAssertTest.onlyChecksCaughtExceptionType": ["type-only-assert"],
            },
        )
        self.assert_flags(
            "BroadRaisesTest.java",
            {
                "BroadRaisesTest.catchesException": ["type-only-assert", "broad-raises"],
                "BroadRaisesTest.catchesJUnit4RuntimeException": ["type-only-assert", "broad-raises"],
                "BroadRaisesTest.catchesThrowableInTryFail": ["type-only-assert", "broad-raises"],
            },
        )

    def test_mocking_flags_are_exact(self) -> None:
        self.assert_flags(
            "InteractionAssertTest.java",
            {
                "InteractionAssertTest.verifiesACollaboratorCall": ["interaction-assert"],
                "InteractionAssertTest.verifiesNoCollaboratorCalls": ["interaction-assert"],
                "InteractionAssertTest.verifiesCollaboratorOrder": ["interaction-assert"],
            },
        )
        self.assert_flags(
            "OverMockingTest.java",
            {"OverMockingTest.constructsFourMocks": ["over-mocking"]},
        )
        self.assert_flags(
            "OverMockingFieldsTest.java",
            {"OverMockingFieldsTest.usesAMockCollaborator": ["over-mocking"]},
        )

    def test_skip_and_non_determinism_flags_are_exact(self) -> None:
        self.assert_flags(
            "SkipsTest.java",
            {
                "SkipsTest.disabledJUnit5Test": ["skip-or-xfail"],
                "SkipsTest.ignoredJUnit4Test": ["skip-or-xfail"],
                "SkipsTest.assumedTest": ["skip-or-xfail"],
            },
        )
        self.assert_flags(
            "NonDeterminismTest.java",
            {
                "NonDeterminismTest.sleeps": ["sleep"],
                "NonDeterminismTest.readsCurrentTime": ["wallclock"],
            },
        )

    def test_shape_flags_are_exact(self) -> None:
        self.assert_flags("LongTest.java", {"LongTest.checksAVeryLongBehaviour": ["long-test"]})
        self.assert_flags("ManyAssertsTest.java", {"ManyAssertsTest.checksFifteenValues": ["many-asserts"]})
        self.assert_flags("VagueNameTest.java", {"VagueNameTest.test1": ["vague-name"]})
        self.assert_flags(
            "ProvenanceTokensTest.java",
            {"ProvenanceTokensTest.test_issue_123_regression": ["provenance-tokens"]},
        )

    def test_junit_variants_and_asserting_helpers_are_clean(self) -> None:
        row, actual = self.scan("CleanTest.java")
        self.assertEqual({}, actual)
        self.assertEqual(6, row.tests)
        self.assertEqual(0, row.flagged_tests)
        row, actual = self.scan("PropertyTest.java")
        self.assertEqual({}, actual)
        self.assertEqual(0, row.tests)

    def test_unparseable_file_is_a_file_level_finding(self) -> None:
        row, actual = self.scan("BrokenTest.java")
        self.assertEqual({}, actual)
        self.assertEqual(0, row.tests)
        self.assertEqual({"unparseable": 1}, row.flags)

    def test_discovery_and_domains(self) -> None:
        relative = JAVA_FIXTURES.relative_to(ROOT).as_posix()
        discovered = scanner.collect_paths(ROOT, [relative])
        self.assertIn(f"{relative}/src/test/java/com/acme/quality/CleanTest.java", discovered)
        self.assertIn(f"{relative}/src/test/java/com/acme/quality/PropertyTest.java", discovered)
        self.assertNotIn(f"{relative}/src/test/java/com/acme/quality/Ignored.java", discovered)
        self.assertNotIn(f"{relative}/src/main/java/com/acme/quality/ProductionTest.java", discovered)
        self.assertEqual(
            "quality",
            scanner.JAVA_FRONTEND.domain_of("service/src/test/java/com/acme/quality/CleanTest.java"),
        )
        self.assertEqual("(root)", scanner.JAVA_FRONTEND.domain_of("src/test/java/RootTest.java"))
        for filename in ("ExampleTest.java", "ExamplesTests.java", "ExampleIT.java"):
            self.assertTrue(scanner.JAVA_FRONTEND.matches(f"src/test/java/com/acme/{filename}"))

    def test_changed_names_compares_java_method_bodies(self) -> None:
        before = """
            class ExampleTest {
                @org.junit.jupiter.api.Test void changed() { assertEquals(1, 1); }
                @org.junit.jupiter.api.Test void unchanged() { assertEquals(2, 2); }
            }
        """
        after = before.replace("assertEquals(1, 1)", "assertEquals(1, result)")
        self.assertEqual(
            {"ExampleTest.changed"},
            scanner.JAVA_FRONTEND.changed_names(before, after),
        )

    def test_missing_parser_dependency_has_an_installation_remedy(self) -> None:
        real_import = builtins.__import__

        def missing_parser(name, *args, **kwargs):
            if name in {"tree_sitter", "tree_sitter_java"}:
                raise ImportError("not installed")
            return real_import(name, *args, **kwargs)

        with mock.patch("builtins.__import__", side_effect=missing_parser):
            with self.assertRaisesRegex(scanner.JavaDependencyError, "uv run.*tree-sitter==0.25.2"):
                scanner._java_parser()


if __name__ == "__main__":
    unittest.main()
