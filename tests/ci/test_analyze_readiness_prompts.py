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

# A finalize command: the full CLI form, or `run` followed by a bare `finalize-tasks`.
_COMMAND = re.compile(r"spec-kitty\s+agent\s+mission\s+finalize-tasks\b|\brun\s+`?finalize-tasks\b", re.IGNORECASE)
# A prohibition directly attached to the command: "never run `...", "do not run ...".
_GOVERNED_COMMAND = re.compile(r"\b(?:never|not)\s+(?:(?:run|pass|use|invoke)\s+)?`?$", re.IGNORECASE)
_WRITING_FLAGS = ("--refresh-planning-commit", "--allow-orphaned")
# A prohibition directly governing a flag, allowing a list: "never pass `--a` or `--b`".
_GOVERNED_FLAG = re.compile(
    r"\b(?:never|not)\s+(?:(?:pass|run|use|invoke|with)\s+)?(?:`--[\w-]+`\s*(?:,|or|and)\s+(?:never\s+)?)*`?$",
    re.IGNORECASE,
)


def _command_span(line: str, end: int) -> str:
    """The rest of the command after the match: up to the closing backtick, or the line end."""
    close = line.find("`", end)
    return line[end:] if close == -1 else line[end:close]


def writing_finalize_lines(text: str) -> list[str]:
    """Lines that instruct a writing `finalize-tasks` run.

    A command counts unless its own span carries `--validate-only` or a
    prohibition is directly attached to it. A writing-only flag counts unless
    a prohibition directly governs it. A prohibition word elsewhere on the
    line ("if the check could not run, run ...") exempts nothing.
    """
    hits = []
    for line in text.splitlines():
        flagged = False
        for match in _COMMAND.finditer(line):
            if "--validate-only" in _command_span(line, match.end()):
                continue
            if _GOVERNED_COMMAND.search(line[: match.start()]):
                continue
            flagged = True
        for flag in _WRITING_FLAGS:
            for match in re.finditer(re.escape(flag), line):
                if not _GOVERNED_FLAG.search(line[: match.start()]):
                    flagged = True
        if flagged:
            hits.append(line)
    return hits


class AnalyzeReadOnlyTest(unittest.TestCase):
    def test_no_writing_finalize_command_in_analyze_prompts(self) -> None:
        for path in (ANALYZE, CAVE_ANALYZE):
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertEqual(writing_finalize_lines(path.read_text(encoding="utf-8")), [])

    def test_positive_control_sees_a_writing_command(self) -> None:
        # Same classifier, same kind of text: every writing form must be caught,
        # including ones a stray prohibition word elsewhere on the line used to hide.
        must_catch = [
            "spec-kitty agent mission finalize-tasks --mission x --json",
            "If the check could not run, run `spec-kitty agent mission finalize-tasks --mission <slug>` to finalize.",
            "Do not forget: spec-kitty agent mission finalize-tasks --mission x --json",
            "Next, run `finalize-tasks` without flags to finalize.",
            "Then run with --refresh-planning-commit to update the pin.",
        ]
        self.assertEqual(writing_finalize_lines("\n".join(must_catch)), must_catch)

    def test_real_prohibitions_and_validate_only_forms_pass(self) -> None:
        must_pass = [
            "spec-kitty agent mission finalize-tasks --validate-only --mission <mission-slug> --json",
            "Otherwise run `spec-kitty agent mission finalize-tasks --validate-only --mission <slug> --json`",
            "Never run `finalize-tasks` without `--validate-only`, and never pass `--refresh-planning-commit` or `--allow-orphaned`: those are the write paths.",
            "and nothing else: never the plain form, never `--refresh-planning-commit`, never `--allow-orphaned`.",
            "**If the version is below 3.1.0a5, or `spec-kitty` is not installed, stop here: do not run the check.**",
            "- **NEVER run a writing `finalize-tasks`**: `--validate-only` is the only permitted form",
        ]
        self.assertEqual(writing_finalize_lines("\n".join(must_pass)), [])


class AnalyzeReadinessContentTest(unittest.TestCase):
    def test_version_gate_named_in_both_analyze_prompts(self) -> None:
        for path in (ANALYZE, CAVE_ANALYZE):
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertIn(VERSION_GATE, path.read_text(encoding="utf-8"))

    def test_version_check_precedes_the_validation_command(self) -> None:
        for path in (ANALYZE, CAVE_ANALYZE):
            with self.subTest(path=path.relative_to(ROOT)):
                text = path.read_text(encoding="utf-8")
                self.assertLess(text.index("spec-kitty --version"), text.index("finalize-tasks --validate-only --mission"))

    def test_resolution_and_placement_codes_classify_as_could_not_run(self) -> None:
        # Case 1 (could not run, HIGH) must catch these before case 2 (refusal,
        # CRITICAL) does; the classification is first-match-wins.
        text = ANALYZE.read_text(encoding="utf-8")
        case1 = text.index("**1. The check could not run.**")
        case2 = text.index("**2. Exit code non-zero")
        for code in ("MISSION_CONTEXT_UNRESOLVED", "MISSION_AMBIGUOUS_SELECTOR", "PLANNING_BRANCH_NOT_PERSISTED"):
            with self.subTest(code=code):
                self.assertTrue(case1 < text.index(code, case1) < case2)

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
