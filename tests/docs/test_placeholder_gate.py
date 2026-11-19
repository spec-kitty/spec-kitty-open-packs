"""The documentation mission's placeholder gate fails closed.

The gate is a Python snippet inside the writing pack's ``validate`` step prompt. These
tests extract it from the prompt as an agent would copy it, and run it on small pages, so
the prompt and the tests cannot drift apart. Stdlib ``unittest`` only::

    python3 -m unittest discover -s tests/docs
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROMPT = ROOT / "packs/writing/missions/documentation/steps/validate.prompt.md"
FENCE3 = "`" * 3
FENCE4 = "`" * 4


def gate_source() -> str:
    """The snippet between the ``python3 - ... <<'EOF'`` line and its ``EOF``."""
    lines = PROMPT.read_text(encoding="utf-8").splitlines()
    start = next(i for i, line in enumerate(lines) if line.strip().startswith("python3 - ") and "<<'EOF'" in line)
    end = next(i for i in range(start + 1, len(lines)) if lines[i].strip() == "EOF")
    return textwrap.dedent("\n".join(lines[start + 1 : end])) + "\n"


class PlaceholderGate(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)
        self.source = gate_source()

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def run_gate(self, *pages: str) -> subprocess.CompletedProcess[str]:
        paths = []
        for i, text in enumerate(pages):
            path = self.dir / f"page{i}.md"
            path.write_text(text, encoding="utf-8")
            paths.append(str(path))
        return self.run_on(*paths)

    def run_on(self, *paths: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-", *paths], input=self.source, capture_output=True, text=True, check=False
        )

    def test_no_page_fails_instead_of_passing(self) -> None:
        result = self.run_on()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("no page given", result.stderr)

    def test_missing_page_fails(self) -> None:
        self.assertNotEqual(self.run_on(str(self.dir / "absent.md")).returncode, 0)

    def test_filled_page_passes(self) -> None:
        result = self.run_gate("---\ntitle: Install\nupdated: '2026-11-19'\n---\n# Install\n\nRun the installer.\n")
        self.assertEqual((result.returncode, result.stdout), (0, ""))

    def test_slot_in_prose_or_frontmatter_fails(self) -> None:
        result = self.run_gate("---\nupdated: \"{YYYY-MM-DD}\"\n---\nSee {Related concept}.\n")
        self.assertEqual(result.returncode, 1)
        self.assertIn("FAIL", result.stdout)
        self.assertIn("{YYYY-MM-DD}", result.stdout)
        self.assertIn("{Related concept}", result.stdout)

    def test_todo_marker_fails(self) -> None:
        result = self.run_gate("Intro.\n\n[TODO: describe the flags]\n")
        self.assertEqual(result.returncode, 1)
        self.assertIn("[TODO: marker", result.stdout)

    def test_slot_in_code_is_listed_for_review_only(self) -> None:
        page = f"Use `{{value}}` here.\n\n{FENCE3}bash\nrun {{command}}\n{FENCE3}\n\n~~~\n{{x}}\n~~~\n"
        result = self.run_gate(page)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(result.stdout.count("REVIEW"), 3)
        self.assertNotIn("FAIL", result.stdout)

    def test_nested_fence_does_not_end_the_outer_block(self) -> None:
        # A three-backtick fence inside a four-backtick block: the inner closer must not end the outer block.
        page = f"{FENCE4}markdown\n{FENCE3}bash\nrun\n{FENCE3}\nstill code {{slot}}\n{FENCE4}\n"
        result = self.run_gate(page)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("REVIEW", result.stdout)
        # An odd count: a lone shorter fence line inside the outer block is content, not a closer.
        result = self.run_gate(f"{FENCE4}\n{FENCE3}\n{{slot}}\n{FENCE4}\n")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("REVIEW", result.stdout)

    def test_prose_after_the_outer_block_is_checked_again(self) -> None:
        page = f"{FENCE4}\n{FENCE3}\ninner\n{FENCE3}\n{FENCE4}\n\nAfter {{Leftover slot}}.\n"
        result = self.run_gate(page)
        self.assertEqual(result.returncode, 1)
        self.assertIn("FAIL", result.stdout)
        self.assertIn("{Leftover slot}", result.stdout)

    def test_a_tilde_line_does_not_close_a_backtick_fence(self) -> None:
        page = f"{FENCE3}\n~~~\n{{inside}}\n{FENCE3}\n"
        result = self.run_gate(page)
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_unclosed_fence_fails(self) -> None:
        result = self.run_gate(f"Intro.\n\n{FENCE3}bash\nrun\n\nLater {{Leftover slot}}.\n")
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("never closed", result.stdout)

    def test_raw_divio_templates_fail(self) -> None:
        templates = sorted((ROOT / "packs/writing/missions/documentation/templates/divio").glob("*-template.md"))
        self.assertEqual(len(templates), 4)
        for template in templates:
            with self.subTest(template=template.name):
                self.assertEqual(self.run_on(str(template)).returncode, 1)


if __name__ == "__main__":
    unittest.main()
