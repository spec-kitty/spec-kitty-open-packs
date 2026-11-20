"""Pin the analyze step's readiness invariants (#246, #237, #247, #213, #214).

The analyze step must stay read-only: the only `finalize-tasks` form it may
instruct is `--validate-only`, behind a CLI version gate. A prompt edit could
silently reintroduce a writing finalize command, so this test guards it, with
a positive control proving the check can see one.

The planning-corpus (#213) and product-coherence (#214) passes are pinned too:
inputs, tactics, graph wiring, finding-id prefixes, section order, the MEDIUM
cap and the recommendation line. New tests are tagged in their docstrings:
"red-first" (new contract, fails on the pre-change prompts), "ratchet"
(pins content that already existed, so it passes by design and stops a silent
deletion) or "control" (a positive control on synthetic text: it proves a
check can see what it guards, so it passes on any prompt version). A helper that carries logic (the read-only classifier, the cap check, the prefix parser, the NON-REMEDIATING gap check) has a positive control on synthetic text.
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
MAX_CAVE_ANALYZE_LINES = 90
CORPUS_TACTIC = "planning-corpus-consistency"
COHERENCE_TACTIC = "product-coherence-review"
RECOMMENDATION = "Recommendation: revise spec | revise plan | revise tasks | proceed"
ACTION_GRAPH = ROOT / "packs" / "foundation" / "action.graph.yaml"
CAVE_FRAGMENT = ROOT / "packs" / "cave-kitty" / "drg" / "fragment.yaml"
OLD_PREFIXES = {
    "D": "duplication", "B": "ambiguity", "U": "underspecification", "K": "charter", "C": "coverage",
    "I": "inconsistency", "V": "finalize-validation", "W": "wp-readiness", "Q": "requirement-quality", "S": "scenario",
}
SECTION_LEADS = (
    "**Finalize Validation:**", "**Per-WP Readiness:**", "**Requirement Quality:**", "**Scenario Audit:**",
    "**Intent & Planning-Artifact Consistency:**", "**Product Coherence:**", "**Clarification Questions:**",
    "**Coverage Summary Table:**", "**Residual Risk:**",
)
_PREFIX_ROW = re.compile(r"^\|\s*([A-Z])\s*\|\s*([\w-]+)\s*\|\s*([A-Z])\s*\|\s*([\w-]+)\s*\|\s*$")

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

    def test_analyze_prompt_within_line_budget(self) -> None:
        lines = len(ANALYZE.read_text(encoding="utf-8").splitlines())
        self.assertLessEqual(lines, MAX_ANALYZE_LINES)



def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def section(text: str, start: str, end: str) -> str:
    """Text from the `start` marker up to (excluding) the next `end` marker."""
    begin = text.index(start)
    return text[begin : text.index(end, begin + len(start))]


def prefix_pairs(text: str) -> list[tuple[str, str]]:
    """Every (prefix, category) pair from the two-column-pair finding-id table."""
    pairs = []
    for line in text.splitlines():
        match = _PREFIX_ROW.match(line)
        if match:
            pairs += [(match[1], match[2]), (match[3], match[4])]
    return pairs


def coherence_capped(severity_text: str) -> bool:
    """True when every product-coherence line is MEDIUM/LOW and none sits under HIGH or CRITICAL."""
    lines = [ln for ln in severity_text.splitlines() if "product-coherence" in ln.lower()]
    if not lines:
        return False
    for line in lines:
        if re.match(r"\s*-\s*\*\*(?:HIGH|CRITICAL)\*\*", line):
            return False
    return any("never higher" in ln for ln in lines) and all("MEDIUM" in ln for ln in lines)


def graph_edges(path: Path) -> set[tuple[str, str, str]]:
    return {(e["source"], e["target"], e["relation"]) for e in yaml.safe_load(read(path))["edges"]}


def load_tactic(tactic_id: str) -> dict:
    return yaml.safe_load(read(TACTICS / f"{tactic_id}.tactic.yaml"))


class PlanningCorpusContractTest(unittest.TestCase):
    def test_corpus_inputs_are_named(self) -> None:
        """red-first: the analyze prompt names the corpus inputs, headings first."""
        text = read(ANALYZE)
        for name in ("artifact_files", "artifact_dirs", "feature_dir", "meta.json", "purpose_tldr",
                     "purpose_context", "source_description", "occurrence_map.yaml"):
            with self.subTest(name=name):
                self.assertIn(name, text)
        self.assertIn("headings first", text.lower())
        self.assertIn("is absent from the inventory, say so in", text)  # fail-open guard: absent keys are never "no artifacts"

    def test_tactics_are_cited_in_the_prompts(self) -> None:
        """red-first: both analyze prompts cite all four tactics in the fetch form; specify cites the quality tactic."""
        for path in (ANALYZE, CAVE_ANALYZE):
            for tactic_id in (QUALITY_TACTIC, WP_TACTIC, CORPUS_TACTIC, COHERENCE_TACTIC):
                with self.subTest(path=path.relative_to(ROOT), tactic=tactic_id):
                    self.assertIn(f"--include tactic:{tactic_id}", read(path))
        self.assertIn(f"tactic:{QUALITY_TACTIC}", read(SPECIFY))

    def test_tactic_files_parse_with_id_and_steps(self) -> None:
        """red-first: all four analyze tactic files exist, parse, carry id == stem and steps."""
        for tactic_id in (QUALITY_TACTIC, WP_TACTIC, CORPUS_TACTIC, COHERENCE_TACTIC):
            with self.subTest(tactic=tactic_id):
                data = load_tactic(tactic_id)
                self.assertEqual(data["id"], tactic_id)
                self.assertTrue(data["steps"])

    def test_tactic_content_names_its_concepts(self) -> None:
        """red-first: the tactics carry the concepts the prompts delegate to them."""
        expected = {
            CORPUS_TACTIC: ("feature_dir", "meta.json", "occurrence_map.yaml", "research", "decision",
                            "data model", "contracts", "quickstart", "ungrounded"),
            COHERENCE_TACTIC: ("MVP", "vertical slice", "scaffolding", "overbuild", "sequencing", "Inferred:",
                               "revise spec", "revise plan", "revise tasks", "proceed"),
        }
        for tactic_id, words in expected.items():
            text = read(TACTICS / f"{tactic_id}.tactic.yaml").lower()
            for word in words:
                with self.subTest(tactic=tactic_id, word=word):
                    self.assertIn(word.lower(), text)

    def test_graph_wires_both_tactics_to_analyze(self) -> None:
        """red-first: scope edges from each analyze action to both tactics, parsed from YAML."""
        cases = ((ACTION_GRAPH, "action:software-dev/analyze", "tactic:"),
                 (CAVE_FRAGMENT, "action:cave-dev/analyze", "foundation::tactic:"))
        for path, source, target_prefix in cases:
            edges = graph_edges(path)
            for tactic_id in (CORPUS_TACTIC, COHERENCE_TACTIC):
                with self.subTest(path=path.name, tactic=tactic_id):
                    self.assertIn((source, f"{target_prefix}{tactic_id}", "scope"), edges)

    def test_prefix_table_has_twelve_distinct_prefixes(self) -> None:
        """red-first: X and M join the ten existing prefixes; table parsed, not substring-matched."""
        pairs = prefix_pairs(read(ANALYZE))
        table = dict(pairs)
        self.assertEqual(len(pairs), 12)
        self.assertEqual(len(table), 12)
        self.assertEqual(table["X"], "planning-artifact")
        self.assertEqual(table["M"], "product-coherence")
        for prefix, category in OLD_PREFIXES.items():
            with self.subTest(prefix=prefix):
                self.assertEqual(table[prefix], category)

    def test_prefix_parser_positive_control(self) -> None:
        """control: the parser extracts both columns, and skips the header and separator rows."""
        synthetic = "| Prefix | Category | Prefix | Category |\n|---|---|---|---|\n| A | alpha | B | beta |\n"
        self.assertEqual(prefix_pairs(synthetic), [("A", "alpha"), ("B", "beta")])

    def test_pass_labels_skip_i(self) -> None:
        """red-first: passes H and J exist as headings, and there is no pass I heading."""
        text = read(ANALYZE)
        self.assertRegex(text, r"(?m)^#### H\. Intent & Planning-Artifact Consistency$")
        self.assertRegex(text, r"(?m)^#### J\. Product Coherence$")
        self.assertIsNone(re.search(r"(?m)^#### I\.", text))

    def test_report_sections_in_order(self) -> None:
        """red-first: the report section leads appear in the fixed order, strictly increasing."""
        text = read(ANALYZE)
        indices = [text.index(lead) for lead in SECTION_LEADS]
        self.assertEqual(indices, sorted(set(indices)))

    def test_id_ordering_and_one_defect_rule(self) -> None:
        """red-first: ids are ordered through H, J and the earliest step owns a defect."""
        text = read(ANALYZE)
        self.assertIn("passes A-G, H, J", text)
        self.assertIn("The earliest step that detects a defect owns it", text)
        self.assertIn("**One defect, one finding.**", text)


class SeverityAndRecommendationTest(unittest.TestCase):
    def severity_block(self) -> str:
        return section(read(ANALYZE), "### 5. Severity Assignment", "### 6.")

    def test_recommendation_literal_in_both_prompts(self) -> None:
        """red-first: the whole recommendation line, never the bare word, is in both prompts, once."""
        for path in (ANALYZE, CAVE_ANALYZE):
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertIn(RECOMMENDATION, read(path))
                # exactly one `Recommendation: <choice>` line: step findings say "Recommended action:"
                self.assertEqual(len(re.findall(r"Recommendation: (?!`)", read(path))), 1)

    def test_cap_helper_positive_control(self) -> None:
        """control: a block that is otherwise valid but lists product-coherence under HIGH or CRITICAL is rejected."""
        for tier in ("HIGH", "CRITICAL"):
            with self.subTest(tier=tier):
                # Carries MEDIUM and "never higher" on the product-coherence line, so only the tier check can fail it.
                bad = f"- **{tier}**: product-coherence finding, MEDIUM or LOW elsewhere, never higher\n"
                self.assertFalse(coherence_capped(bad))
        good = "- **Product-coherence findings** are MEDIUM or LOW, never higher\n"
        self.assertTrue(coherence_capped(good))
        self.assertFalse(coherence_capped("- **MEDIUM**: terminology drift\n"))

    def test_planning_artifact_keeps_normal_severity(self) -> None:
        """red-first: a planning-artifact contradiction is HIGH, so X findings are not capped like M."""
        high = [ln for ln in self.severity_block().splitlines() if re.match(r"\s*-\s*\*\*HIGH\*\*", ln)]
        self.assertTrue(any("planning-artifact" in ln for ln in high))
        self.assertFalse(any("product-coherence" in ln.lower() for ln in high))

    def test_verdict_rule_unchanged(self) -> None:
        """ratchet: any high or critical finding still means blocked."""
        self.assertRegex(read(ANALYZE), r"any `high` or `critical` finding\s*->\s*`blocked`")

    def test_inferred_carrier_and_v_exemption(self) -> None:
        """red-first: Inferred: sits in the carrier summary and the table Summary cell; V never carries it."""
        line = next(ln for ln in read(ANALYZE).splitlines() if "starts with `Inferred:`" in ln)
        self.assertIn("carrier `summary`", line)
        self.assertIn("table Summary cell", line)
        self.assertRegex(line, r"`V` finding .*never carries the label")


class ReportFormatAndParityTest(unittest.TestCase):
    """New report-format contract (red-first): table layout, FR-018 nits and cave-dev parity."""

    def test_scenario_audit_table_and_ascii_marker(self) -> None:
        """red-first: Finding column, ASCII `-` marker, and only the gap rows become S findings."""
        self.assertRegex(read(ANALYZE), r"Only missing-edge, surprising-accepted and surprising-rejected\b.*`S` findings")
        rule = section(read(ANALYZE), "**Scenario Audit:**", "**Clarification Questions:**")
        self.assertIn("| Kind | Scenario | Location | Finding |", rule)
        self.assertIn("Finding is the `S` id, or `-` for accepted and rejected rows", rule)

    def test_example_row_uses_lowercase_category(self) -> None:
        """red-first: the example table row uses the lowercase category `duplication` (FR-018)."""
        rows = [ln for ln in read(ANALYZE).splitlines() if ln.startswith("| D1 |")]
        self.assertEqual(len(rows), 1)
        self.assertIn("| duplication |", rows[0])

    def test_cave_prompt_parity(self) -> None:
        """red-first: the cave-dev prompt names X, M, the Inferred: label, both tactics, the recommendation and feature_dir."""
        text = read(CAVE_ANALYZE)
        for needle in ("`X`", "`M`", "`Inferred:`", CORPUS_TACTIC, COHERENCE_TACTIC, RECOMMENDATION, "feature_dir"):
            with self.subTest(needle=needle):
                self.assertIn(needle, text)


class ExistingContentRatchetTest(unittest.TestCase):
    """The #247 content the Step-0 squad found deletable without a failing test."""

    def test_scenario_audit_kinds_in_order(self) -> None:
        """ratchet: the five scenario kinds stay, in order."""
        text = read(ANALYZE)
        bullet = next(ln for ln in text.splitlines() if "scenario audit in five kinds" in ln)
        kinds = ["accepted", "rejected", "missing edge", "surprising accepted", "surprising rejected"]
        positions = [bullet.index(k) for k in kinds]
        self.assertEqual(positions, sorted(positions))

    def test_clarification_choices_rule(self) -> None:
        """ratchet: two to four choices, or a concrete remediation, for HIGH/CRITICAL findings."""
        text = read(ANALYZE)
        self.assertIn("two to four concrete choices", text)
        self.assertIn("or a concrete remediation", text)
        self.assertRegex(text, r"every HIGH or CRITICAL ambiguity or requirement-quality finding")

    def test_five_quality_properties_in_tactic(self) -> None:
        """ratchet: the five requirement-quality properties stay in the tactic, as list items."""
        text = read(TACTICS / f"{QUALITY_TACTIC}.tactic.yaml")
        for prop in ("Testable", "Solution-free", "Unambiguous", "Consistent", "Complete"):
            with self.subTest(prop=prop):
                self.assertRegex(text, rf"(?m)^\s*-\s*{prop}:")

    def test_cave_prompt_within_line_budget(self) -> None:
        """ratchet: the cave-dev analyze prompt stays at or under its size guard."""
        self.assertLessEqual(len(read(CAVE_ANALYZE).splitlines()), MAX_CAVE_ANALYZE_LINES)


OWNER_MAPPING = "Owners by category first: `C`, `V` and `W` -> tasks; `M` -> the owner of its first cited location"


def squash(text: str) -> str:
    """Whitespace-collapsed text, so a folded YAML scalar compares with a prompt line."""
    return " ".join(text.split())


def never_proceeds_when_blocked(text: str) -> bool:
    return bool(re.search(r"(?i)never\s+(?:choose\s+)?`?\"?proceed\"?`?\s+(?:while|when|over)\b[^.]*blocked", squash(text)))


class RecommendationRuleTest(unittest.TestCase):
    def tactic_recommend_text(self) -> str:
        steps = load_tactic(COHERENCE_TACTIC)["steps"]
        return next(s["description"] for s in steps if s["title"] == "Recommend one outcome")

    def test_prompt_states_the_deterministic_owner_rule(self) -> None:
        """red-first: the prompt maps owners and orders the choice by the first finding in table order."""
        text = squash(read(ANALYZE))
        self.assertIn(OWNER_MAPPING, text)
        self.assertIn("revise the owner of the first HIGH or CRITICAL finding in table order", text)
        self.assertIn("checklists, decisions, occurrence_map.yaml) -> plan", text)
        self.assertIn("proceed, unless an `M` finding of MEDIUM severity exists", text)
        self.assertIn("then revise the owner of the first such finding in table order", text)
        self.assertNotIn("owns the most severe finding", text)

    def test_never_proceed_while_blocked(self) -> None:
        """red-first: the prompt and the tactic both forbid proceed over a blocked verdict."""
        self.assertTrue(never_proceeds_when_blocked(read(ANALYZE)))
        self.assertTrue(never_proceeds_when_blocked(self.tactic_recommend_text()))

    def test_tactic_leaves_the_owner_rule_to_the_prompt(self) -> None:
        """red-first: the recommendation rule has one owner; the tactic restates neither owners nor table order."""
        tactic = squash(self.tactic_recommend_text())
        self.assertNotIn("table order", tactic)
        self.assertNotIn("Owners:", tactic)

    def test_never_proceed_check_positive_control(self) -> None:
        """control: the checker sees the rule when present and its absence."""
        self.assertTrue(never_proceeds_when_blocked("never `proceed` while the verdict is `blocked`."))
        self.assertFalse(never_proceeds_when_blocked("proceed while the verdict is blocked."))
        self.assertFalse(never_proceeds_when_blocked("a revise choice is allowed."))


QUOTED_SUMMARY_RULE = ("double-quoted YAML string", "an unquoted `Inferred:` prefix breaks the carrier")


class CarrierSummaryQuotingTest(unittest.TestCase):
    def test_summary_must_be_double_quoted(self) -> None:
        """red-first: the carrier rules require a double-quoted summary and warn about an unquoted Inferred: prefix."""
        for token in QUOTED_SUMMARY_RULE:
            self.assertIn(token, read(ANALYZE))



ID_ORDER_RULE = ("then occurrence_map.yaml, then decision files by name", "sorts by its first cited location")
RESIDUAL_RISK_RULE = "neither inventoried nor read"


class DeterminismTest(unittest.TestCase):
    def test_id_ordering_covers_map_decisions_and_multi_artifact_findings(self) -> None:
        """red-first: the id ordering names occurrence_map.yaml, decision files by name and the first-cited-location rule."""
        for token in ID_ORDER_RULE:
            self.assertIn(token, read(ANALYZE))
        self.assertIn("then by id number; when rows overflow the 50-row cap, every HIGH and CRITICAL row stays", read(ANALYZE))

    def test_decisions_are_listed_not_globbed(self) -> None:
        """red-first: the prompt and the corpus tactic list the decisions directory and skip index.json; no DM-*.md glob."""
        corpus = squash(read(TACTICS / f"{CORPUS_TACTIC}.tactic.yaml"))
        for text in (read(ANALYZE), corpus):
            with self.subTest(text=text[:20]):
                self.assertRegex(squash(text), r"list `\S*decisions/` and read the decision records it holds \(not `index.json`\)")
                self.assertNotIn("DM-*", text)

    def test_residual_risk_names_unread_directory_entries(self) -> None:
        """red-first: Residual Risk reports mission-directory entries that were neither inventoried nor read."""
        risk = section(read(ANALYZE), "**Residual Risk:**", "**Charter Alignment")
        self.assertIn(RESIDUAL_RISK_RULE, risk)



MVP_SOURCE = ("an MVP Scope note or any heading containing MVP", '"MVP unclear"')
SEVERITY_SPLIT = ("MEDIUM for intent drift", "LOW otherwise")
SETUP_NOT_SCAFFOLDING = "setup or foundation WPs the MVP slice directly needs are not scaffolding"
TASKS_MVP_NOTE = "recorded in tasks.md's MVP Scope note"
FINALIZE_MVP_NOTE = "writes no MVP Scope note"


class MvpAndScaffoldingTest(unittest.TestCase):
    def test_mvp_source_is_the_tasks_md_slice(self) -> None:
        """red-first: pass J reads the MVP slice from any MVP-bearing heading in tasks.md and never defines it."""
        text = read(ANALYZE)
        for token in MVP_SOURCE:
            self.assertIn(token, text)
        self.assertIn("never define MVP here", text)

    def test_m_severity_split(self) -> None:
        """red-first: M findings are MEDIUM for drift, a lost scenario or a valueless named MVP and LOW otherwise, still capped."""
        block = self_severity()
        for token in SEVERITY_SPLIT:
            self.assertIn(token, block)
        self.assertTrue(coherence_capped(block))

    def test_setup_work_is_not_scaffolding(self) -> None:
        """red-first: prompt and tactic exempt the setup the MVP needs from the scaffolding finding."""
        self.assertIn(SETUP_NOT_SCAFFOLDING, read(ANALYZE))
        steps = load_tactic(COHERENCE_TACTIC)["steps"]
        slice_step = next(s["description"] for s in steps if s["title"] == "Compare vertical slices with scaffolding")
        self.assertIn("Setup or foundation work packages the MVP slice directly needs are not scaffolding", squash(slice_step))
        mvp_step = next(s["description"] for s in steps if s["title"] == "Read the smallest valuable slice")
        self.assertIn("any heading containing MVP", squash(mvp_step))

    def test_mvp_note_follows_who_writes_tasks_md(self) -> None:
        """red-first: the single-command tasks step writes the MVP Scope note; the split flow's finalize generates
        tasks.md, writes no note and says so, so a missing note stays a LOW finding that cannot force a revise."""
        self.assertIn(TASKS_MVP_NOTE, read(SOFTWARE_DEV / "tasks.prompt.md"))
        self.assertNotIn("usually Work Package 1", read(SOFTWARE_DEV / "tasks.prompt.md"))
        self.assertIn(FINALIZE_MVP_NOTE, read(SOFTWARE_DEV / "tasks-finalize.prompt.md"))
        self.assertIn("including a missing MVP note", self_severity())



def self_severity() -> str:
    return section(read(ANALYZE), "### 5. Severity Assignment", "### 6.")


STALENESS_SENTENCE = ("Editing any other planning artifact the report judged (research, data-model, contracts, quickstart, "
                      "decisions, occurrence_map.yaml, meta.json or a WP prompt) also invalidates its findings")


class UntrackedStalenessTest(unittest.TestCase):
    def test_analyze_names_untracked_planning_edits(self) -> None:
        """red-first: 7a says editing an untracked judged artifact invalidates the findings and asks for a re-run."""
        block = squash(section(read(ANALYZE), "### 7a.", "### 8."))
        self.assertIn(STALENESS_SENTENCE, block)
        self.assertIn("does not track it: re-run /spec-kitty.analyze", block)

    def test_tasks_prompts_mirror_the_sentence(self) -> None:
        """red-first: tasks and tasks-finalize state the same rule where they state the staleness rule."""
        for name in ("tasks.prompt.md", "tasks-finalize.prompt.md"):
            with self.subTest(name=name):
                self.assertIn(STALENESS_SENTENCE, squash(read(SOFTWARE_DEV / name)))



NON_REMEDIATING_TARGETS = ("spec.md", "plan.md", "tasks.md", "WP files", "any other planning artifact", "meta.json",
                           "occurrence_map.yaml", "decisions/")


def non_remediating_gaps(text: str) -> list[str]:
    """Targets missing from the NON-REMEDIATING line (all of them when the line is absent)."""
    line = next((ln for ln in text.splitlines() if ln.startswith("**NON-REMEDIATING**")), "")
    return [target for target in NON_REMEDIATING_TARGETS if f"`{target}`" not in line and target not in line]


class NonRemediatingListTest(unittest.TestCase):
    def test_list_covers_every_planning_input(self) -> None:
        """ratchet: the NON-REMEDIATING line names meta.json, occurrence_map.yaml and decisions/ beside the core artifacts."""
        self.assertEqual(non_remediating_gaps(read(ANALYZE)), [])

    def test_gap_check_positive_control(self) -> None:
        """control: the check reports a dropped target and a missing line on synthetic text."""
        full = "**NON-REMEDIATING**: Do not modify " + ", ".join(f"`{x}`" for x in NON_REMEDIATING_TARGETS)
        self.assertEqual(non_remediating_gaps(full), [])
        self.assertEqual(non_remediating_gaps(full.replace("`decisions/`", "")), ["decisions/"])
        self.assertEqual(non_remediating_gaps(full.replace("`meta.json`", "")), ["meta.json"])
        self.assertEqual(non_remediating_gaps("no such line"), list(NON_REMEDIATING_TARGETS))


if __name__ == "__main__":
    unittest.main()
