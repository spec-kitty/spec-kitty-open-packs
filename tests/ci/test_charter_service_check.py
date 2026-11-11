"""The pin file and the charter service driver, off the service: everything that needs no running jar."""

from __future__ import annotations

import io
import subprocess
import sys
import tarfile
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "ci"))

import charter_lock as lock  # noqa: E402
import charter_service_check as check  # noqa: E402
import validate_pack_schemas as validator  # noqa: E402

COMMIT = "f4acac975522e4bf8d423d552672f9d1d78e8186"
DIGEST = "a" * 64


class CharterLock(unittest.TestCase):
    def read(self, text: str) -> dict[str, str]:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "charter.lock.yaml"
            path.write_text(text, encoding="utf-8")
            return lock.read(path)

    def test_the_repository_pin_is_a_full_commit_and_feeds_the_schema_validator(self) -> None:
        pin = lock.read()
        self.assertRegex(pin["commit"], r"^[0-9a-f]{40}$")
        self.assertEqual(validator.charter_commit(), pin["commit"])

    def test_a_commit_pin_reads_with_its_comments_and_empty_release_keys(self) -> None:
        pin = self.read(f"# why\ncommit: {COMMIT}  # the pin\nrelease_tag:\njar_sha256: ''\n")
        self.assertEqual(pin, {"commit": COMMIT, "release_tag": "", "jar_sha256": ""})

    def test_a_release_pin_needs_its_tag_and_digest_together(self) -> None:
        pin = self.read(f"commit: {COMMIT}\nrelease_tag: service-v1.2.3\njar_sha256: {DIGEST}\n")
        self.assertEqual(pin["release_tag"], "service-v1.2.3")
        self.read(f"commit: {COMMIT}\nrelease_tag: service-v1.2.3-rc.1\njar_sha256: {DIGEST}\n")
        for text in (f"commit: {COMMIT}\nrelease_tag: service-v1.2.3\n", f"commit: {COMMIT}\njar_sha256: {DIGEST}\n"):
            with self.subTest(text=text), self.assertRaises(lock.LockError):
                self.read(text)

    def test_anything_but_a_lowercase_full_commit_is_refused(self) -> None:
        for commit in ("main", "v1.0.0", COMMIT[:12], COMMIT.upper(), COMMIT + "0", "", "refs/heads/main"):
            with self.subTest(commit=commit), self.assertRaises(lock.LockError):
                self.read(f"commit: {commit}\n")
        with self.assertRaises(lock.LockError):  # no commit key at all
            self.read("release_tag:\n")

    def test_a_malformed_tag_digest_unknown_key_or_duplicate_is_refused(self) -> None:
        for text in (
            f"commit: {COMMIT}\nrelease_tag: v1.2.3\njar_sha256: {DIGEST}\n",
            f"commit: {COMMIT}\nrelease_tag: service-v1.2\njar_sha256: {DIGEST}\n",
            f"commit: {COMMIT}\nrelease_tag: service-v1.2.3\njar_sha256: {'A' * 64}\n",
            f"commit: {COMMIT}\nbranch: main\n",
            f"commit: {COMMIT}\ncommit: {COMMIT}\n",
            f"commit {COMMIT}\n",
        ):
            with self.subTest(text=text), self.assertRaises(lock.LockError):
                self.read(text)

    def test_a_missing_file_is_refused_and_the_validator_fails_closed_on_it(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, self.assertRaises(lock.LockError):
            lock.read(Path(tmp) / "absent.yaml")
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "charter.lock.yaml"
            bad.write_text("commit: main\n", encoding="utf-8")
            original, lock.LOCK_FILE = lock.LOCK_FILE, bad
            try:
                with self.assertRaises(validator.GateError):
                    validator.charter_commit()
            finally:
                lock.LOCK_FILE = original

    def test_the_cli_prints_a_key_and_exits_2_on_a_bad_name(self) -> None:
        done = subprocess.run([sys.executable, str(ROOT / "scripts" / "ci" / "charter_lock.py"), "commit"],
                              capture_output=True, text=True, check=False)
        self.assertEqual((done.returncode, done.stdout.strip()), (0, lock.read()["commit"]))
        done = subprocess.run([sys.executable, str(ROOT / "scripts" / "ci" / "charter_lock.py"), "branch"],
                              capture_output=True, text=True, check=False)
        self.assertEqual(done.returncode, 2)


class ExpectedCode(unittest.TestCase):
    def fixture(self, text: str | None) -> Path:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        fixture = Path(tmp.name) / "bad"
        fixture.mkdir()
        if text is not None:
            (fixture / "expected-code").write_text(text, encoding="utf-8")
        return fixture

    def test_both_paths_are_named_and_precheck_is_optional(self) -> None:
        parsed = check.parse_expected_code(self.fixture("# why\ncomposition: pack_unreadable  # c\nregistration: validation_failed\n"))
        self.assertEqual(parsed, {"composition": "pack_unreadable", "registration": "validation_failed"})
        parsed = check.parse_expected_code(self.fixture("composition: a_b\nregistration: c\nprecheck: accepted\n"))
        self.assertEqual(parsed["precheck"], "accepted")

    def test_a_missing_file_a_missing_path_or_a_malformed_line_fails_closed(self) -> None:
        for text in (None, "composition: pack_unreadable\n", "registration: x\n", "composition: Pack-Unreadable\nregistration: x\n",
                     "composition: a\nregistration: b\nprecheck: maybe\n", "composition: a\nregistration: b\nextra: c\n",
                     "composition a\nregistration: b\n", "composition:\nregistration: b\n"):
            with self.subTest(text=text), self.assertRaises(check.CannotRun):
                check.parse_expected_code(self.fixture(text))

    def test_every_invalid_fixture_of_the_repository_declares_its_codes(self) -> None:
        fixtures = check.pack_dirs(ROOT / "tests" / "fixtures" / "invalid")
        self.assertTrue(fixtures)
        for fixture in fixtures:
            with self.subTest(fixture=fixture.name):
                self.assertTrue(check.parse_expected_code(fixture))
        names = {fixture.name for fixture in fixtures}
        self.assertIn("legacy-shapes", names)
        self.assertEqual(check.parse_expected_code(ROOT / "tests" / "fixtures" / "invalid" / "legacy-shapes")["composition"], "pack_unreadable")


class Packs(unittest.TestCase):
    def make(self, root: Path, name: str, pack_id: str, level: str = "org", depends_on: tuple[str, ...] = ()) -> Path:
        pack = root / name
        (pack / "directives").mkdir(parents=True)
        entries = "".join(f"  - pack_id: {dep}\n    range: '>=1.0'\n" for dep in depends_on)
        (pack / "pack.yaml").write_text(
            f"# a comment\npack_id: {pack_id}\npack_version: 1.0.0\nparent_pack: null\nname: {name}\npack_level: {level}\n"
            + (f"depends_on:\n{entries}" if entries else ""), encoding="utf-8")
        (pack / "directives" / "d.directive.yaml").write_text("id: D\n", encoding="utf-8")
        return pack

    def setUp(self) -> None:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)

    def test_the_descriptor_reader_takes_scalars_and_dependency_ids(self) -> None:
        pack = self.make(self.root, "dependent", "01AAA", depends_on=("01BBB", "01CCC"))
        descriptor = check.read_descriptor(pack)
        self.assertEqual((descriptor["pack_id"], descriptor["pack_level"], descriptor["name"]), ("01AAA", "org", "dependent"))
        self.assertEqual(descriptor["depends_on"], ["01BBB", "01CCC"])
        self.assertNotIn("parent_pack", descriptor)  # null is no value
        self.assertEqual(check.read_descriptor(self.root / "absent"), {"depends_on": []})

    def test_dependencies_are_registered_first_whatever_the_order_found(self) -> None:
        base = self.make(self.root, "a-base", "01BASE")
        middle = self.make(self.root, "b-middle", "01MID", depends_on=("01BASE",))
        top = self.make(self.root, "c-top", "01TOP", depends_on=("01MID", "01BASE"))
        for given in ([top, middle, base], [middle, top, base], [base, middle, top]):
            order = check.registration_order(given)
            self.assertEqual([p.name for p in order], ["a-base", "b-middle", "c-top"])
        cyclic_a = self.make(self.root, "x", "01X", depends_on=("01Y",))
        cyclic_b = self.make(self.root, "y", "01Y", depends_on=("01X",))
        self.assertEqual(len(check.registration_order([cyclic_a, cyclic_b])), 2)  # a cycle is the service's to refuse

    def test_the_archive_leaves_out_fixture_files_and_unmodelled_documentation_only(self) -> None:
        pack = self.make(self.root, "p", "01P")
        for name in ("expected-code", "README.md", "PROVENANCE.md", "org-charter.yaml", "stray.md",
                     "missions/m/templates/README.md", "missions/m/templates/plan-field-declaration.yaml",
                     "missions/m/templates/kept.md", "directives/README.md"):
            (pack / name).parent.mkdir(parents=True, exist_ok=True)
            (pack / name).write_text("x\n", encoding="utf-8")
        left_out: list[str] = []
        body = check.archive(pack, left_out)
        with tarfile.open(fileobj=io.BytesIO(body), mode="r:gz") as tar:
            names = set(tar.getnames())
        self.assertEqual(names, {"pack.yaml", "directives", "directives/d.directive.yaml", "directives/README.md", "stray.md",
                                 "missions", "missions/m", "missions/m/templates", "missions/m/templates/kept.md"})
        self.assertEqual(sorted(left_out), ["PROVENANCE.md", "README.md", "missions/m/templates/README.md",
                                            "missions/m/templates/plan-field-declaration.yaml", "org-charter.yaml"])

    def test_two_directories_with_one_name_cannot_share_a_configuration_root(self) -> None:
        self.make(self.root / "one", "same", "01A")
        self.make(self.root / "two", "same", "01B")
        with self.assertRaises(check.CannotRun):
            check.pack_dirs(self.root / "one", self.root / "two")

    def test_staging_lays_packs_out_as_the_configuration_root_expects(self) -> None:
        pack = self.make(self.root / "src", "p", "01P")
        (pack / "expected-code").write_text("composition: a\nregistration: b\n", encoding="utf-8")
        check.stage(self.root / "cfg", [pack])
        self.assertTrue((self.root / "cfg" / "packs" / "p" / "pack.yaml").is_file())
        self.assertFalse((self.root / "cfg" / "packs" / "p" / "expected-code").exists())


if __name__ == "__main__":
    unittest.main()
