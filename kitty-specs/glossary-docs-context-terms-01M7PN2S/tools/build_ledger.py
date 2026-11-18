#!/usr/bin/env python3
"""Build the classification ledger of core's docs/context terms (mission tool, not shipped).

Usage: build_ledger.py > research/ledger.yaml

Paths are fixed, never taken from the command line: REPO is this repository's root (four levels up), and
CORE_CONTEXT is core's docs/context in a core checkout beside it, at commit 01e577d:
`git clone https://github.com/spec-kitty/spec-kitty ../spec-kitty && git -C ../spec-kitty checkout 01e577d`.

Every `###`/`####` heading followed by a `| Definition | ... |` row is one source term. The verdict
comes from the page's default (PAGE_DEFAULT) unless OVERRIDES names the heading. Pages without term
tables contribute the hand-listed rows in EXTRA. A term whose id, name or alias is already in the
target context gets the verdict `exists`.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[3]
CORE_CONTEXT = REPO.parent / "spec-kitty" / "docs" / "context"
STATUS = {"canonical": "active", "candidate": "draft", "deprecated": "deprecated"}

PAGE_DEFAULT = {
    "charter.md": "foundation",
    "configuration-project-structure.md": "foundation",
    "dossier.md": "foundation",
    "execution.md": "foundation",
    "governance.md": "foundation",
    "identity.md": "foundation",
    "identity-fields.md": "foundation",
    "lexical.md": "foundation",
    "orchestration.md": "foundation",
    "planning-and-tracking.md": "internal",
    "practices-principles.md": "foundation",
    "product-lines.md": "internal",
    "spec-driven.md": "foundation",
    "system-events.md": "foundation",
    "technology-foundations.md": "foundation",
    "testing-taxonomy.md": "internal",
    "topology.md": "foundation",
}
FOUNDATION_REASON = {
    "charter.md": "charter, activation and DRG vocabulary a project's charter and its packs use",
    "configuration-project-structure.md": "a directory or file every Spec Kitty project has",
    "dossier.md": "what `spec-kitty reconcile` and the Mission dossier report to a project",
    "execution.md": "a runtime or tool concept a project meets when running Missions",
    "governance.md": "a charter-governance concept a project configures or reads",
    "identity.md": "a collaborator identity a project's Missions and profiles name",
    "identity-fields.md": "an identity field in a project's config or Mission metadata",
    "lexical.md": "how the glossary runtime treats a project's terms",
    "orchestration.md": "Mission lifecycle, branch or gate vocabulary of a project's Missions and CLI output",
    "planning-and-tracking.md": "a unit of governed work a project chooses",
    "practices-principles.md": "a glossary-strictness rule a project's generation is held to",
    "spec-driven.md": "spec vocabulary of a project's Mission specs",
    "system-events.md": "an event or log a project's Missions write or a consumer reads",
    "technology-foundations.md": "a foundational term other definitions rely on; the writing pack's glossary styleguide and the curation-interview tactic require it to be defined (reverses decision 01M7PN8GR51G0YAS30CRRJ0NWP)",
    "topology.md": "Mission topology vocabulary of a project's `meta.json`, lanes and CLI errors",
}
INTERNAL_REASON = {
    "testing-taxonomy.md": "a pytest marker of core's own test suite",
    "planning-and-tracking.md": "a label or issue convention of core's GitHub tracker",
    "product-lines.md": "a Spec Kitty Inc. product line, not a concept a project meets",
}
PAGE_REASON = {
    "foundation": "consumer concept: met in a project's own Missions, charter, packs, CLI output or event logs",
    "internal": "house concept: core's code, repository, tests, tracker or product lines",
    "excluded": "generic technology term, not a Spec Kitty concept (decision 01M7PN8GR51G0YAS30CRRJ0NWP)",
}

CODE = "core code symbol or module, not something a consumer meets"
# heading -> (verdict, reason[, id])
OVERRIDES: dict[str, tuple] = {
    # charter.md
    "Contract Scenario": ("internal", "the charter's own contract-test vocabulary"),
    "Trigger Registry": ("internal", CODE),
    "Charter Facade": ("internal", CODE),
    "CharterScope": ("internal", CODE),
    "Workflow Sequence": ("internal", "core runtime's internal schema registry"),
    "Workflow ID": ("internal", "core runtime's internal schema registry key"),
    "Ratchet Baseline": ("internal", "core's architectural test gates"),
    "Cat-7 Grandfathered Orphan": ("internal", "core's architectural test gates"),
    "Symbol-level Dead Code": ("internal", "core's architectural test gates"),
    "`__all__` Declaration Convention": ("internal", "core's Python module convention"),
    "Mission-Type Profile": ("internal", "core's per-type governance profile file; no pack carries one"),
    "Guideline": ("excluded", "core's doctrine precedence layer; the charter has no guideline artifact kind"),
    "Import Candidate": ("internal", "core's doctrine-curation record; no charter counterpart"),
    # configuration-project-structure.md
    "`glossary/`": ("excluded", "names a directory the page says does not exist"),
    "Bootstrap (Candidate)": ("excluded", "a proposed flow, not shipped; the page says it is not a command"),
    "Charter Library": ("excluded", "the page says the compiler writes no separate library"),
    # dossier.md
    "ArtifactRef": ("internal", CODE),
    "Baseline Key": ("internal", "lists core's internal baseline fields"),
    # execution.md
    "Tool Surface": ("internal", "derived term of the tool-vs-agent naming record; installer internals"),
    "Middleware Pipeline": ("internal", "core's glossary runtime design"),
    "Checkpoint/Resume": ("internal", "core's glossary runtime design"),
    "Seed File": ("excluded", "the .kittify/glossaries seed is retiring in core (#5269); the pack yaml is the source"),
    "GovernanceContext": ("internal", "design concept with no code type (core)"),
    "MissionExecutionContext": ("internal", CODE),
    "InfraContext": ("internal", "design concept with no code type (core)"),
    "Effector": ("internal", "core's domain-model naming, docs only"),
    "Shadow Clone (Isolated Dev Environment)": ("internal", "practice for developing Spec Kitty itself"),
    # governance.md
    "Activation Chokepoint": ("internal", CODE),
    # identity.md
    "engagement": ("internal", "core's project-egress consent rationale"),
    "Human-in-Charge (HiC)": ("foundation", "the accountable human a project's Missions and procedures name; worded 'operator' (#139)", "operator"),
    "Audience Persona": ("internal", "personas model Spec Kitty's own docs audience"),
    "Internal Audience Persona": ("internal", "personas model Spec Kitty's own docs audience"),
    "External Audience Persona": ("internal", "personas model Spec Kitty's own docs audience"),
    # orchestration.md
    "Feature": ("foundation", "consumer meets the retired word; carried as deprecated", "feature"),
    "WorkPackage (Alias)": ("alias", "alias row of work package", "work-package"),
    "Tracker Connector Boundary (Alias)": ("alias", "alias row of Tracker Connector", "tracker-connector"),
    "Runtime Bridge": ("internal", CODE),
    "step contract": ("excluded", "retired by the charter: step contracts are folded into their steps' substeps (#285), and the term was dropped (#283)"),
    "Mission-Runtime YAML": ("internal", "core's runtime file; a charter mission type is <id>.mission-type.yaml"),
    "Step Dependency": ("internal", "core's runtime step DAG; a charter mission type orders its steps by list"),
    "Mission State Derivation": ("internal", "core runtime internals"),
    "Window-open SHA": ("internal", "consolidation-gate internals"),
    "Window opener": ("internal", "consolidation-gate internals"),
    "Exemption anchor": ("internal", "consolidation-gate internals"),
    "Claim inputs": ("internal", CODE),
    "Named window variant": ("internal", "consolidation-gate design record"),
    "Publish to origin/main": ("internal", "core repository's own publishing rule"),
    "Target-owned bookkeeping": ("internal", "core state-contract internals"),
    "Routing": ("internal", "umbrella word over core code senses"),
    "The drain": ("internal", "retired core vocabulary"),
    "Residue": ("internal", "core code senses of a kitty-specs child"),
    # planning-and-tracking.md
    "op": ("foundation", "consumer concept: the Op of DIRECTIVE_053 (#234); authored by hand", "op"),
    # practices-principles.md
    "Mostly Invisible Process": ("internal", "design principle of core's glossary runtime"),
    "Highly Visible Outcomes": ("internal", "design principle of core's glossary runtime"),
    "Append-Only Semantic History": ("internal", "design principle of core's glossary runtime"),
    "Deterministic Gate, Human Clarification": ("internal", "design principle of core's glossary runtime"),
    "Human-in-Charge (Cross-Reference)": ("excluded", "a cross-reference to Human-in-Charge (HiC), not a term"),
    # system-events.md
    "Telemetry (Out of Scope for This Slice)": ("excluded", "out of scope per its own page"),
    # topology.md
    "LANE_MEMBERSHIP_FROZEN": ("foundation", "consumer meets the error from finalize-tasks", "lane-membership-frozen"),
}

# Pages without term tables: (page, heading, source status, verdict, id, reason)
EXTRA = [
    ("mission-types.md", "software-dev", "canonical", "foundation", "software-dev-mission", "shipped mission type; authored by hand"),
    ("mission-types.md", "research", "canonical", "foundation", "research-mission", "shipped mission type; authored by hand"),
    ("mission-types.md", "documentation", "canonical", "foundation", "documentation-mission", "shipped mission type; authored by hand"),
    ("mission-types.md", "plan", "canonical", "foundation", "plan-mission", "shipped mission type; authored by hand"),
    ("ops-vs-missions.md", "Op", "canonical", "folded", "op", "same concept as planning-and-tracking.md `op`; one term"),
    ("naming-decision-tool-vs-agent.md", "Naming Decision: Tool vs Agent", "canonical", "internal", "tool-vs-agent-naming", "the team's internal decision record (#221)"),
    ("team-kitty.md", "Team Kitty", "canonical", "folded", "team-kitty", "same as product-lines.md Team Kitty"),
    ("team-kitty.md", "Zeitgeist", "canonical", "internal", "zeitgeist", "retired hosted vocabulary"),
    ("team-kitty.md", "Moment", "canonical", "internal", "moment", "retired hosted vocabulary"),
    ("team-kitty.md", "Drain", "canonical", "folded", "the-drain", "same as orchestration.md The drain"),
]


def slug(text: str) -> str:
    text = re.sub(r"\(.*?\)", "", text.replace("`", ""))
    text = text.split(" — ")[0].split(" / ")[0]
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def table_row(line: str) -> tuple[str, str] | None:
    """A two-cell Markdown table row `| key | value |` as (key, value), or None; the value runs to the last pipe."""
    text = line.strip()
    if len(text) < 2 or not (text.startswith("|") and text.endswith("|")):
        return None
    key, sep, value = text[1:-1].partition("|")
    key = key.strip()
    if key.startswith("**") and key.endswith("**") and len(key) > 4:
        key = key[2:-2]
    key = key.strip()
    if not sep or not key or "*" in key:
        return None
    return key, value.strip()


def parse(root: Path):
    for page in sorted(root.rglob("*.md")):
        current = None
        for line in page.read_text(encoding="utf-8").splitlines():
            head = re.match(r"^(#{2,4}) (.+)$", line)
            if head:
                if current and "Definition" in current["rows"]:
                    yield current
                current = {"page": str(page.relative_to(root)), "heading": head.group(2).strip(), "rows": {}} if len(head.group(1)) >= 3 else None
                continue
            if current:
                row = table_row(line)
                if row:
                    current["rows"][row[0]] = row[1]
        if current and "Definition" in current["rows"]:
            yield current


def known(context: Path) -> dict[str, str]:
    data = yaml.safe_load(context.read_text(encoding="utf-8"))
    out = {}
    for term in data["terms"]:
        for form in [term["id"], term["name"], *(term.get("aliases") or [])]:
            out[slug(form)] = term["id"]
    return out


def main() -> None:
    src, repo = CORE_CONTEXT, REPO
    targets = {
        "foundation": known(repo / "packs/foundation/glossaries/spec-kitty-core.glossary.yaml"),
        "internal": known(repo / "packs/internal/glossaries/spk-internal-glossary.glossary.yaml"),
    }
    rows, seen = [], {"foundation": set(), "internal": set()}
    for term in parse(src):
        heading = term["heading"]
        status = term["rows"].get("Status", "").split()[0].strip("`*") if term["rows"].get("Status") else ""
        default = PAGE_DEFAULT[term["page"]]
        page_reason = (FOUNDATION_REASON if default == "foundation" else INTERNAL_REASON).get(term["page"], PAGE_REASON[default])
        verdict, reason, *rest = OVERRIDES.get(heading) or (default, page_reason)
        tid = rest[0] if rest else slug(heading)
        row = {"page": term["page"], "heading": heading, "source_status": status, "verdict": verdict, "id": tid, "reason": reason}
        if term["page"] == "testing-taxonomy.md":  # core's pytest markers: bare words like "unit" would claim generic ids
            row.update(id=f"{tid}-test-marker", name=f"{heading.replace('`', '')} (core test marker)")
            tid = row["id"]
        elif heading == "usability (label)":
            row.update(id="usability-label")
            tid = row["id"]
        if verdict in targets:
            for context in ("foundation", "internal"):
                if slug(heading) in targets[context] or tid in targets[context]:
                    row.update(verdict="exists", context=context, id=targets[context].get(tid) or targets[context][slug(heading)],
                               reason=f"already a term of the {context} context")
                    break
            else:
                if tid in seen[verdict]:
                    tid = f"{tid}-{slug(term['page'][:-3])}"
                    row["id"] = tid
                seen[verdict].add(tid)
        rows.append(row)
    for page, heading, status, verdict, tid, reason in EXTRA:
        rows.append({"page": page, "heading": heading, "source_status": status, "verdict": verdict, "id": tid, "reason": reason})
    yaml.safe_dump({"source": "spec-kitty/spec-kitty docs/context @ 01e577d", "rows": rows}, sys.stdout, sort_keys=False, width=120, allow_unicode=True)


if __name__ == "__main__":
    main()
