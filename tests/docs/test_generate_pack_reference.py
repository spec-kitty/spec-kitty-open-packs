"""Tests for scripts/docs/generate_pack_reference.py.

Stdlib ``unittest`` (also collected by pytest). Run from the repository root:

    python3 -m unittest discover -s tests/docs -v
"""

from __future__ import annotations

import importlib.util
import os
import re
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
            "# Pack: example\\-pack",
            "`ACME_001_SECRET_HANDLING` | Never commit credentials to the repository",
            "Secrets come from the environment or a secret manager\\, never from the repository\\.",
            "| `required` |",
            "`acme-tac-001-scan-staged` | Scan staged content for credentials",
            "| 1 step |",
            "| `acme` | acme | Turn on the Acme rules\\. | 1 directive |",
            "| DRG fragment | 0 node(s), 1 edge(s)",
            "org `acme`; keys: `org_name`, `schema_version`",
            "Generated — do not edit.",
        ):
            self.assertIn(needle, page)
        self.assertIn("[example\\-pack](example-pack.md)", files["index.md"])

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
            ["bash", "-c", "git ls-files -z --cached --others --exclude-standard -- . | tr '\\0' '\\n' | LC_ALL=C sort | while IFS= read -r f; do sha256sum \"./$f\"; done | sha256sum"],
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
        self.assertIn("| Purpose | Keep secrets out of git\\. |", page)
        self.assertIn("| Depends on | `base-pack` |", page)
        self.assertIn("| Maturity | experimental |", page)
        self.assertIn("| Keep secrets out of git\\. | `base-pack` |", (self.out / "index.md").read_text())


XSS_PAYLOAD = "[click](javascript:alert(1)) ![i](https://evil.example/x.png) <img src=x onerror=alert(1)> **bold** https://evil.example/auto www.evil.example"


class UntrustedPackContent(unittest.TestCase):
    """Pack text is third-party input: it must render literally, never as markup."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)
        self.packs = self.tmp / "packs"
        shutil.copytree(FIXTURES, self.packs)
        self.pack = self.packs / "example-pack"
        self.out = self.tmp / "out"

    def render(self) -> str:
        with mock.patch.dict(os.environ, {"SOURCE_DATE_EPOCH": EPOCH_A}):
            return gen.build(self.packs, self.out)["example-pack.md"]

    def write(self, rel: str, text: str) -> None:
        path = self.pack / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def test_markdown_and_html_in_pack_text_is_escaped(self):
        self.write(
            "directives/acme-001-secret-handling.directive.yaml",
            yaml.safe_dump({"schema_version": "1.0", "id": "ACME_001", "title": XSS_PAYLOAD, "intent": XSS_PAYLOAD, "enforcement": "required"}),
        )
        page = self.render()
        body = page.split("\n---\n", 1)[1]
        for raw in ("[click](", "![i](", "<img", "**bold**", "https://evil", "www.evil"):
            # Present only in backslash-escaped form, never as live syntax.
            self.assertIsNone(re.search(r"(?<!\\)" + re.escape(raw), body), f"unescaped {raw!r} in rendered page")
        self.assertIn(r"\[click\]\(javascript\:alert\(1\)\)", body)
        self.assertIn(r"\!\[i\]\(https\:\/\/evil\.example\/x\.png\)", body)
        self.assertIn(r"\<img src\=x onerror\=alert\(1\)\>", body)

    def test_code_spans_keep_angle_brackets_and_survive_backticks_and_pipes(self):
        self.assertEqual(gen._code("@promise:<id>"), "`@promise:<id>`")
        self.assertEqual(gen._code("a`b"), "``a`b``")
        self.assertEqual(gen._code("`x`"), "`` `x` ``")
        self.assertEqual(gen._code("a|b"), "`a\\|b`")
        self.write("directives/acme-001-secret-handling.directive.yaml",
                   yaml.safe_dump({"id": "ID`<x>|y", "title": "t", "enforcement": "required"}))
        self.assertIn("| ``ID`<x>\\|y`` |", self.render())

    def test_non_scalar_values_never_leak_as_python_repr(self):
        self.write("directives/acme-001-secret-handling.directive.yaml",
                   yaml.safe_dump({"id": "ACME_001", "title": {"nested": "x"}, "intent": ["a", "b"], "enforcement": {"k": 1}}))
        page = self.render()
        self.assertNotIn("{'", page)
        self.assertNotIn("['", page)
        self.assertIn("| `ACME_001` | ACME\\_001 | — | [", page)


class PackLayoutCoverage(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)
        self.packs = self.tmp / "packs"
        self.pack = self.packs / "p"
        files = {
            "assets/lint.py": "print('hi')\n",
            "assets/lint.py.asset.yaml": "id: p-lint\ntitle: Lint\nmime: text/x-python\npath: lint.py\n",
            "assets/logo.svg": "<svg/>\n",
            "assets/logo.svg.asset.yaml": "id: p-logo\ntitle: Logo\nmime: image/svg+xml\npath: logo.svg\n",
            "agent_profiles/p-rhea.agent.yaml": "profile-id: p-rhea\nname: Rhea\nroles: [p-reporter]\npurpose: Reports.\n",
            "mission_types/m.yaml": "id: m\ndisplay_name: M\n",
            "missions/m/mission-runtime.yaml": "mission: {key: m, name: Mission M}\nsteps:\n  - {id: specify}\n  - {id: plan}\n",
            "missions/m/command-templates/specify.md": "x\n",
            "mission-steps/m/plan/step.yaml": "id: plan\ndisplay_name: Plan it\nagent_profile: p-rhea\ndepends_on: [specify]\n",
            "mission_step_contracts/m-plan.step-contract.yaml": "id: m-plan\naction: plan\nmission: m\nsteps: [{id: a}, {id: b}]\n",
        }
        for rel, text in files.items():
            path = self.pack / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text)
        self.out = self.tmp / "out"

    def render(self) -> dict:
        with mock.patch.dict(os.environ, {"SOURCE_DATE_EPOCH": EPOCH_A}):
            return gen.build(self.packs, self.out)

    def test_assets_are_listed_and_executables_flagged(self):
        files = self.render()
        page = files["p.md"]
        self.assertIn("This pack ships executable code.", page)
        self.assertIn("| `p-lint` | Lint | `text/x-python` | [`assets/lint.py`](", page)
        self.assertIn("| **yes** |", page)
        self.assertIn("| `p-logo` | Logo | `image/svg+xml` | [`assets/logo.svg`](", page)
        self.assertIn("| no |", page)
        self.assertIn("| **1** |", files["index.md"])

    def test_agent_profiles_read_kebab_case_ids(self):
        self.assertIn("| `p-rhea` | Rhea | Reports\\. | `p-reporter` |", self.render()["p.md"])

    def test_mission_types_take_actions_from_the_mission_runtime(self):
        page = self.render()["p.md"]
        self.assertIn("| `m` | M | — | `specify` → `plan` (from [`missions/m/mission-runtime.yaml`]", page)
        self.assertIn("| `m` | Mission M | `specify` → `plan` | 1 | 0 |", page)
        self.assertIn("| `m` | `plan` | Plan it | `p-rhea` | `specify` |", page)
        self.assertIn("| `m-plan` | m\\-plan | — | mission `m`, action `plan`, 2 steps |", page)


class MalformedInput(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)
        self.packs = self.tmp / "packs"
        shutil.copytree(FIXTURES, self.packs)
        self.pack = self.packs / "example-pack"
        self.out = self.tmp / "out"

    def rc(self, env: dict | None = None) -> int:
        with mock.patch.dict(os.environ, env or {"SOURCE_DATE_EPOCH": EPOCH_A}):
            return gen.main(["--packs-root", str(self.packs), "--out", str(self.out)])

    def test_non_mapping_yaml_is_exit_2(self):
        for rel in ("drg/fragment.yaml", "org-charter.yaml", "directives/acme-001-secret-handling.directive.yaml", "pack.yaml"):
            with self.subTest(rel=rel):
                path = self.pack / rel
                backup = path.read_text() if path.exists() else None
                path.write_text("- a\n- b\n")
                self.assertEqual(self.rc(), 2)
                if backup is None:
                    path.unlink()
                else:
                    path.write_text(backup)

    def test_wrongly_typed_pack_yaml_fields_are_exit_2(self):
        for body in ("depends_on: base\n", "depends_on: [{a: 1}]\n", "maturity: {level: x}\n", "purpose: [x]\n"):
            with self.subTest(body=body):
                (self.pack / "pack.yaml").write_text(body)
                self.assertEqual(self.rc(), 2)

    def test_bad_source_date_epoch_is_exit_2(self):
        self.assertEqual(self.rc({"SOURCE_DATE_EPOCH": "yesterday"}), 2)

    def test_symlinks_are_rejected(self):
        (self.pack / "link.yaml").symlink_to(self.pack / "org-charter.yaml")
        self.assertEqual(self.rc(), 2)


@unittest.skipIf(shutil.which("git") is None, "git not available")
class ChecksumFileSet(unittest.TestCase):
    """Only what git would ship counts; ignored build droppings never flip --check."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)
        self.repo = self.tmp / "repo"
        self.packs = self.repo / "packs"
        shutil.copytree(FIXTURES, self.packs)
        (self.repo / ".gitignore").write_text("__pycache__/\n*.pyc\n")
        git = ["git", "-C", str(self.repo), "-c", "user.name=t", "-c", "user.email=t@example.invalid"]
        subprocess.run(["git", "init", "-q", str(self.repo)], check=True)
        subprocess.run(git + ["add", "-A"], check=True)
        subprocess.run(git + ["commit", "-q", "-m", "init"], check=True)
        self.out = self.tmp / "out"

    def run_gen(self, *extra: str) -> int:
        with mock.patch.dict(os.environ, {"SOURCE_DATE_EPOCH": EPOCH_A}):
            return gen.main(["--packs-root", str(self.packs), "--out", str(self.out), *extra])

    def test_ignored_files_do_not_change_the_checksum(self):
        before = gen.pack_checksum(self.packs / "example-pack")
        self.assertEqual(before[2], "git")
        self.assertEqual(before[:2], gen.pack_checksum(FIXTURES / "example-pack")[:2])
        self.assertEqual(self.run_gen(), 0)
        cache = self.packs / "example-pack" / "assets" / "__pycache__"
        cache.mkdir(parents=True)
        (cache / "x.cpython-312.pyc").write_bytes(b"\x00junk")
        self.assertEqual(gen.pack_checksum(self.packs / "example-pack"), before)
        self.assertEqual(self.run_gen("--check"), 0)

    def test_untracked_unignored_files_count(self):
        before = gen.pack_checksum(self.packs / "example-pack")
        (self.packs / "example-pack" / "NOTES.md").write_text("new\n")
        self.assertNotEqual(gen.pack_checksum(self.packs / "example-pack")[0], before[0])


if __name__ == "__main__":
    unittest.main()
