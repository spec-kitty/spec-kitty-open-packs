"""Pin the analyze step's readiness invariants (#246, #237, #247).

The analyze step must stay read-only: the only `finalize-tasks` form it may
instruct is `--validate-only`, behind a CLI version gate. A prompt edit could
silently reintroduce a writing finalize command, so this test guards it, with
a positive control proving the check can see one.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
SOFTWARE_DEV = ROOT / "packs" / "foundation" / "missions" / "software-dev" / "steps"
ANALYZE = SOFTWARE_DEV / "analyze.prompt.md"
SPECIFY = SOFTWARE_DEV / "specify.prompt.md"
CAVE_ANALYZE = ROOT / "packs" / "cave-kitty" / "missions" / "cave-dev" / "steps" / "analyze.prompt.md"
TACTICS = ROOT / "packs" / "foundation" / "tactics" / "analysis"

VERSION_GATE = "3.1.0a5"
QUALITY_TACTIC = "requirement-quality-ears"
WP_TACTIC = "wp-prompt-readiness-review"
MAX_ANALYZE_LINES = 500

_COMMAND = re.compile(r"spec-kitty\s+agent\s+mission\s+finalize-tasks\b")
_PROHIBITION = re.compile(r"\bnever\b|\bdo not\b|\bnot run\b", re.IGNORECASE)


def writing_finalize_lines(text: str) -> list[str]:
    """Lines that instruct a `finalize-tasks` command without `--validate-only`.

    A line counts when it spells the command, lacks `--validate-only`, and is
    not a prohibition. Lines naming the writing-only flags count unless they
    are a prohibition.
    """
    hits = []
    for line in text.splitlines():
        prohibited = bool(_PROHIBITION.search(line))
        if _COMMAND.search(line) and "--validate-only" not in line and not prohibited:
            hits.append(line)
        elif ("--refresh-planning-commit" in line or "--allow-orphaned" in line) and not prohibited:
            hits.append(line)
    return hits


class AnalyzeReadOnlyTest(unittest.TestCase):
    def test_no_writing_finalize_command_in_analyze_prompts(self) -> None:
        for path in (ANALYZE, CAVE_ANALYZE):
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertEqual(writing_finalize_lines(path.read_text(encoding="utf-8")), [])

    def test_positive_control_sees_a_writing_command(self) -> None:
        # Same classifier, same kind of text: a writing form must be caught,
        # and the validate-only and prohibited forms must not.
        fixture = "\n".join(
            [
                "spec-kitty agent mission finalize-tasks --mission x --json",
                "spec-kitty agent mission finalize-tasks --validate-only --mission x --json",
                "Never pass `--refresh-planning-commit`.",
                "Then run with --refresh-planning-commit to update the pin.",
            ]
        )
        self.assertEqual(
            writing_finalize_lines(fixture),
            [
                "spec-kitty agent mission finalize-tasks --mission x --json",
                "Then run with --refresh-planning-commit to update the pin.",
            ],
        )


class AnalyzeReadinessContentTest(unittest.TestCase):
    def test_version_gate_named_in_both_analyze_prompts(self) -> None:
        for path in (ANALYZE, CAVE_ANALYZE):
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertIn(VERSION_GATE, path.read_text(encoding="utf-8"))

    def test_version_check_precedes_the_validation_command(self) -> None:
        text = ANALYZE.read_text(encoding="utf-8")
        self.assertLess(text.index("spec-kitty --version"), text.index("finalize-tasks --validate-only --mission"))

    def test_tactics_are_cited(self) -> None:
        cited = {
            ANALYZE: (QUALITY_TACTIC, WP_TACTIC),
            CAVE_ANALYZE: (QUALITY_TACTIC, WP_TACTIC),
            SPECIFY: (QUALITY_TACTIC,),
        }
        for path, ids in cited.items():
            text = path.read_text(encoding="utf-8")
            for tactic_id in ids:
                with self.subTest(path=path.relative_to(ROOT), tactic=tactic_id):
                    self.assertIn(f"tactic:{tactic_id}", text)

    def test_analyze_prompt_within_line_budget(self) -> None:
        lines = len(ANALYZE.read_text(encoding="utf-8").splitlines())
        self.assertLessEqual(lines, MAX_ANALYZE_LINES)

    def test_fixed_finding_id_prefixes(self) -> None:
        text = ANALYZE.read_text(encoding="utf-8")
        for prefix, category in (
            ("D", "duplication"),
            ("B", "ambiguity"),
            ("U", "underspecification"),
            ("K", "charter"),
            ("C", "coverage"),
            ("I", "inconsistency"),
            ("V", "finalize-validation"),
            ("W", "wp-readiness"),
            ("Q", "requirement-quality"),
            ("S", "scenario"),
        ):
            with self.subTest(prefix=prefix):
                self.assertRegex(text, rf"\|\s*{prefix}\s*\|\s*{re.escape(category)}\s*\|")

    def test_tactic_files_exist_with_their_ids(self) -> None:
        for tactic_id in (QUALITY_TACTIC, WP_TACTIC):
            with self.subTest(tactic=tactic_id):
                data = yaml.safe_load((TACTICS / f"{tactic_id}.tactic.yaml").read_text(encoding="utf-8"))
                self.assertEqual(data["id"], tactic_id)


if __name__ == "__main__":
    unittest.main()
