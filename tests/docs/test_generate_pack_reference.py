"""Tests for scripts/docs/generate_pack_reference.py.

Stdlib ``unittest`` (also collected by pytest). Run from the repository root:

    python3 -m unittest discover -s tests/docs -v
"""

from __future__ import annotations

import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "docs" / "generate_pack_reference.py"
FIXTURES = REPO_ROOT / "tests" / "fixtures" / "valid"
GOLDEN = REPO_ROOT / "tests" / "golden" / "pack-reference"

_spec = importlib.util.spec_from_file_location("generate_pack_reference", SCRIPT)
gen = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
sys.modules[_spec.name] = gen  # dataclasses resolve annotations via sys.modules
_spec.loader.exec_module(gen)

EPOCH_A = "1791590400"  # 2026-10-10
EPOCH_B = "1793404800"  # 2026-10-31


def frontmatter(text: str) -> dict:
    assert text.startswith("---\n")
    return yaml.safe_load(text[4 : text.index("\n---\n", 4)])


class FixturePackRendering(unittest.TestCase):
    """The committed golden output is exactly what the fixture pack renders to."""

    def test_golden_is_up_to_date(self):
        rc = gen.main(["--packs-root", str(FIXTURES), "--out", str(GOLDEN), "--check"])
        self.assertEqual(rc, 0, "golden drifted: re-run the generator with --packs-root tests/fixtures/valid --out tests/golden/pack-reference")

    def test_renders_every_fixture_artifact(self):
        files = gen.build(FIXTURES, GOLDEN)
        self.assertEqual(sorted(files), ["checksums.json", "example-pack.md", "index.md"])
        page = files["example-pack.md"]
        for needle in (
            "# Pack: example-pack",
            "`ACME_001_SECRET_HANDLING` | Never commit credentials to the repository",
            "Secrets come from the environment or a secret manager",
            "| `required` |",
            "`acme-tac-001-scan-staged` | Scan staged content for credentials",
            "| 1 step |",
            "| `acme` | acme | Turn on the Acme rules. | 1 directive |",
            "| DRG fragment | 0 node(s), 1 edge(s)",
            "org `acme`; keys: `org_name`, `schema_version`",
            "Generated — do not edit.",
        ):
            self.assertIn(needle, page)
        self.assertIn("[example-pack](example-pack.md)", files["index.md"])

    def test_frontmatter_meets_the_dockitty_contract(self):
        files = gen.build(FIXTURES, GOLDEN)
        for name in ("example-pack.md", "index.md"):
            fm = frontmatter(files[name])
            for key in ("title", "description", "doc_status", "updated", "type", "kind"):
                self.assertTrue(fm.get(key), f"{name}: missing {key}")
            self.assertLessEqual(len(fm["description"]), 180)
            self.assertEqual(fm["doc_status"], "active")
            self.assertEqual(fm["type"], "API")
            self.assertEqual(fm["generated"]["by"], gen.GENERATOR)
            self.assertEqual(fm["generated"]["at"], fm["updated"])

    def test_checksum_matches_the_published_shell_recipe(self):
        if shutil.which("sha256sum") is None or shutil.which("bash") is None:
            self.skipTest("sha256sum/bash not available")
        pack = FIXTURES / "example-pack"
        shell = subprocess.run(
            ["bash", "-c", "find . -type f ! -path '*/.*' | LC_ALL=C sort | while IFS= read -r f; do sha256sum \"$f\"; done | sha256sum"],
            cwd=pack, capture_output=True, text=True, check=True,
        ).stdout.split()[0]
        self.assertEqual(gen.pack_checksum(pack)[0], shell)
        self.assertIn(f"sha256:{shell}", gen.build(FIXTURES, GOLDEN)["example-pack.md"])


class DeterminismAndDrift(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)
        self.packs = self.tmp / "packs"
        shutil.copytree(FIXTURES, self.packs)
        self.out = self.tmp / "out"

    def run_gen(self, *extra: str, epoch: str = EPOCH_A) -> int:
        with mock.patch.dict(os.environ, {"SOURCE_DATE_EPOCH": epoch}):
            return gen.main(["--packs-root", str(self.packs), "--out", str(self.out), *extra])

    def test_fresh_output_is_dated_from_source_date_epoch(self):
        self.assertEqual(self.run_gen(), 0)
        self.assertEqual(frontmatter((self.out / "example-pack.md").read_text())["updated"], "2026-10-10")

    def test_unchanged_content_keeps_its_date_and_check_is_stable(self):
        self.run_gen(epoch=EPOCH_A)
        before = {p.name: p.read_text() for p in self.out.iterdir()}
        self.assertEqual(self.run_gen("--check", epoch=EPOCH_B), 0)
        self.run_gen(epoch=EPOCH_B)
        self.assertEqual({p.name: p.read_text() for p in self.out.iterdir()}, before)

    def test_changed_pack_gets_a_new_date_and_check_fails_until_regenerated(self):
        self.run_gen(epoch=EPOCH_A)
        tactic = self.packs / "example-pack" / "tactics" / "acme-tac-001.tactic.yaml"
        tactic.write_text(tactic.read_text().replace("Scan staged content", "Scan every staged file"))
        self.assertEqual(self.run_gen("--check", epoch=EPOCH_B), 1)
        self.run_gen(epoch=EPOCH_B)
        page = (self.out / "example-pack.md").read_text()
        self.assertIn("Scan every staged file", page)
        self.assertEqual(frontmatter(page)["updated"], "2026-10-31")
        self.assertEqual(self.run_gen("--check", epoch=EPOCH_B), 0)

    def test_check_flags_hand_edits_and_stale_pages(self):
        self.run_gen()
        page = self.out / "example-pack.md"
        page.write_text(page.read_text() + "\nhand edit\n")
        self.assertEqual(self.run_gen("--check"), 1)
        self.run_gen()
        (self.out / "removed-pack.md").write_text("---\ntitle: x\n---\n")
        self.assertEqual(self.run_gen("--check"), 1)
        self.run_gen()
        self.assertFalse((self.out / "removed-pack.md").exists())

    def test_empty_packs_root_renders_only_the_index(self):
        empty = self.tmp / "empty"
        empty.mkdir()
        (empty / "README.md").write_text("not a pack\n")
        with mock.patch.dict(os.environ, {"SOURCE_DATE_EPOCH": EPOCH_A}):
            files = gen.build(empty, self.out)
        self.assertEqual(sorted(files), ["index.md"])
        self.assertIn("No packs are materialized", files["index.md"])

    def test_invalid_yaml_is_a_generator_error(self):
        bad = self.packs / "example-pack" / "directives" / "broken.directive.yaml"
        bad.write_text("id: [unterminated\n")
        self.assertEqual(self.run_gen(), 2)

    def test_optional_pack_yaml_supplies_purpose_and_dependencies(self):
        (self.packs / "example-pack" / "pack.yaml").write_text(
            "name: example-pack\npurpose: Keep secrets out of git.\ndepends_on: [base-pack]\nmaturity: experimental\n"
        )
        self.run_gen()
        page = (self.out / "example-pack.md").read_text()
        self.assertIn("| Purpose | Keep secrets out of git. |", page)
        self.assertIn("| Depends on | `base-pack` |", page)
        self.assertIn("| Maturity | experimental |", page)
        self.assertIn("| Keep secrets out of git. | `base-pack` |", (self.out / "index.md").read_text())


if __name__ == "__main__":
    unittest.main()
