#!/usr/bin/env python3
"""Rewrite pre-existing spec-kitty-core definitions that cite core internals or say HiC (mission tool).

Usage: clean_existing.py  (the path is fixed: build_ledger.REPO)

FR-005 covers the whole consumer context: a definition must not cite core's source tree, tests, ADRs,
issue numbers or its docs/context pages. Term ids, names, statuses and every other field are kept, and
only the `definition` scalar of the terms in REWRITE is replaced, so the rest of the file keeps its bytes.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

REWRITE = {
    "catastrophic-backtracking": "A regular-expression engine failure mode in which a vulnerable pattern combined with adversarial input drives matching time into exponential or polynomial complexity. Backtracking engines (Python `re`, JavaScript, Java, .NET) attempt every possible partition of the input when a match fails; patterns with nested or consecutive non-possessive repetitions can produce O(2^N) or O(N^c) retry storms. The `secure-regex-catastrophic-backtracking` tactic codifies the four dangerous-shape patterns, the rewrite ladder (bound quantifier → refactor nested → possessive/atomic group → negated char class), and the escape hatches (drop the regex, re2, multi-pass, bounded-input cap). Every fix requires a wall-clock regression test asserting linear runtime on an adversarial input (default budget: ≤100 ms for 100 000 chars). Synonym \"ReDoS\" (Regular-expression Denial of Service) is acceptable only as a parenthetical.",
    "deliberate-linearity": "A function whose body is intentionally kept long-and-linear (rather than extracted into named helpers) for traceability against a documented contract, code-review map, or output-section sequence. Deliberate linearity functions are NOT refactor candidates regardless of Sonar S3776 score. Identified by an explicit code comment justifying the structure and/or a published output-section contract that reviewers verify line-by-line. Refactoring a deliberately linear function without updating its contract is a regression in traceability. Distinct from structural debt.",
    "dependency-readiness": "The condition the dependency gate evaluates before a work package may be claimed or implemented: every WP listed in its `dependencies` frontmatter must be in the `approved` or `done` WP state. `approved` is included deliberately — `done` is emitted only by whole-mission consolidation, so requiring a dependency to be strictly `done` would deadlock every same-mission dependency chain (the dependent WP could never start, so the mission could never consolidate, so the dependency could never reach `done`). The consolidation dependency gate treats `{approved, done}` as satisfied in the same way. `for_review`, `in_review`, `blocked`, `canceled`, and missing status are not ready.",
    "rule-pipeline": "A pipeline of small pure functions, each checking applicability, optionally executing its narrow piece of work, and returning a result threaded to the next function. Three flavors are recognized: Validator (accumulating findings), Transformer (chained state, actions and an optional error), Scorer (a weighted number). See the `chain-of-responsibility-rule-pipeline` tactic.",
    "skill": "A markdown file encoding a domain-specific agent workflow, discoverable as a named command. Skills are the primary unit of reusable agent capability in spec-kitty. The word names three distinct artifacts, so name the sense. A pack skill is a charter-activatable skill that a team shares through an org pack or the project tier. A doctrine skill ships with the Spec Kitty CLI. A command skill is a generated spec-kitty.<command> skill.",
    "review-py-package": "Deprecated: an internal layout detail of the Spec Kitty CLI (its review command is a package of sibling files, no longer a single module), not a concept a project meets.",
    "target-branch": "The git branch on which a mission's code, planning artifacts, and status events must ultimately land. Persisted in meta.json under the key target_branch at mission-create time and never overwritten; merge_target_branch is its legacy alias in older meta.json files. All downstream commands (finalize-tasks, implement, review, consolidate) derive the branch contract from this stored value, not from the operator's current branch at invocation time. In branch-context JSON output, target_branch and base_branch carry the same value when queried at the mission level.",
    "tool-surface-drift": "The state of a generated tool surface file that Spec Kitty still tracks as managed but whose content no longer matches anything Spec Kitty wrote, so Spec Kitty will not overwrite it without consent. In practice someone edited a generated slash-command file, command skill, managed skill, agent profile or plugin-bundle component. `spec-kitty upgrade` keeps such a file, names it (`Not updated, your local edit was kept: <path>`) and exits non-zero (whether it should is still open) with the outcome `drift_unresolved` and the failure reason `surface_drift`; `spec-kitty doctor tool-surfaces` reports the same file as drifted. Not tool-surface drift: a missing file (upgrade recreates it); a file that matches an older generated version (stale; upgrade rewrites it); a file Spec Kitty never generated (user-owned, left untouched); a difference between two branches' copies of `.kittify/metadata.yaml`. A known defect can misclassify an unedited generated file as drifted; that is the defect, not this term. Never write bare 'drift' in operator-facing text; say which file was kept and why.",
    "integrating-worktree": "A linked git worktree whose checked-out branch is a mission, lane or coordination branch (a `kitty/mission-` branch, as recognized by the branch-naming authority), or whose branch cannot be read (a detached HEAD counts, to fail safe). Its branch will later be integrated into another branch of the same Mission. `spec-kitty upgrade`, run from the repository root checkout, skips integrating worktrees: it writes, stamps and commits nothing in them, which is why a lane can still show a pre-upgrade `.kittify/metadata.yaml`. Not an integrating worktree: a worktree on an ordinary branch, such as a topic or landing branch, where upgrade still upgrades and commits; the repository root checkout, which never is one. For a per-work-package execution checkout in general, say lane worktree (see the `lane worktree` entry).",
    "target-owned-bookkeeping": "A tracked file at the project root that Spec Kitty fully generates, marks 'do not edit', and that no work package authors, declared target-owned in the state contract; today only `.kittify/metadata.yaml`. Its authoritative copy is the one on the merge target branch. When two branches of one Mission carry different copies, each integration site (consolidate, review start, implement resume, lane sync) resolves the conflict to a fixed side without asking: the copy closer to the merge target branch wins, and between two lanes the receiving lane keeps its own until consolidation. Not target-owned: an operator-editable file (`.gitattributes`, `.gitignore`, `.kittify/config.yaml`), whose conflicts still refuse. For where a Mission artifact is stored, say PRIMARY partition; `.kittify/metadata.yaml` is not a Mission artifact and has no partition. No site computes 'the repository root checkout's copy'. Do not call it 'primary-owned': that earlier name suggested the PRIMARY partition or the primary branch, and the merge target branch need not be the primary branch.",
    "current-branch": "The git branch checked out in the repository root checkout at the moment a spec-kitty workflow command (specify, plan, tasks, implement) is invoked. Read ephemerally from the working tree; never persisted in any mission artifact. Exposed as current_branch / CURRENT_BRANCH in branch-context JSON output. Spec Kitty never derives the mission target from current_branch: it reads target_branch from meta.json, so the branch contract is stable regardless of which branch the operator is on when driving the mission.",
    "merge-target-branch": "The branch where completed work-package code must ultimately land. Stored in every WP prompt's frontmatter (alongside planning_base_branch) to give implementing agents an explicit merge destination. In meta.json it is the legacy alias of target_branch, read as a fallback when target_branch is absent (older missions). All three (target_branch, planning_base_branch and merge_target_branch) carry the same value; the separation makes intent explicit in agent-facing prompts and prevents a temporary branch from leaking into work-package frontmatter in place of the persisted target.",
    "planning-base-branch": "The branch that was active in the repository root checkout when WP prompts were generated (at finalize-tasks time). Stored in every WP prompt's frontmatter and in lanes.json to root lane-worktree allocation correctly regardless of which branch the operator is on when running finalize-tasks. It equals target_branch. It exists so that running finalize-tasks from a temporary branch cannot leak that branch into WP frontmatter and break lane allocation once the temporary branch is deleted.",
    "structural-debt": "A function whose cognitive complexity has accumulated beyond reviewable bounds AND whose responsibilities are independently dispatching concerns with no shared state between branches. A structural debt function is a refactor candidate per the `refactoring-extract-first-order-concept` and `refactoring-extract-class-by-responsibility-split` tactics. Distinguished from deliberate linearity by the *absence* of a documented design intent and by the presence of independent dispatch arms or triplicated patterns, for example a command handler whose three modes share no state after option parsing and repeat the same output logic three times.",
    "charter-content-migration": "The scan and normalize-or-fail-loud flow that brings existing Missions' charter content into compliance with the charter-content chokepoint contract.",
    "enforcement-level": "How strictly an in-force directive binds, ranked `required` > `lenient-adherence` > `advisory` (the charter's directive schema). `required` means a deviation outside the directive's own `explicit_allowances` is a defect; `lenient-adherence` means the same, and the schema requires such a directive to list at least one allowance (the deviations it permits); `advisory` means the directive is guidance an agent weighs. A directive's `enforcement` field is the pack-supplied default level; which level applies in a project is the adopting charter's decision. Directive prose, and content that cites a directive, never restates the level. Distinct from activation presets' `must_have` items and `policy.yaml` levels, which decide which artefacts are in force.",
    "charter-offering": "Everything offered to a project: the Charter Packs it can draw from (the built-in pack and each configured org pack) plus the project layer. The offer side of the charter; the activation side is the active charter. Not the project's activated set: say active charter.",
    "active-charter": "What a project has activated: its activated_<kind> keys, activated_kinds and mission_type_activations, plus the deactivated_<kind> exclusions, held in the activation ledger .kittify/charter/activation.yaml (a project not yet upgraded to 4.0.0rc8 still keeps the allow keys in .kittify/config.yaml or the charter.yaml it points to); listed by `spec-kitty charter list --json`. 'Active' and 'inactive' alone still describe one artifact ('an active directive'); 'active charter' names the project's activated set as a whole; the .kittify/charter/ tree is never called 'active'.",
    "activation-ledger": "The git-tracked file .kittify/charter/activation.yaml, the single authority for what a project has activated: activated_kinds, mission_type_activations, the three-state activated_<kind> allow state and the deactivated_<kind> exclusions. The effective set of a kind is its allow state minus its exclusions, and an exclusion never removes an org-required id. `spec-kitty init` writes it; `spec-kitty upgrade` or `spec-kitty migrate activation-ledger` moves an older project's keys into it. Not the Migration Ledger (.kittify/migration-ledger.jsonl, which records the upgrade migrations that ran).",
    "doctrine-pack": "DEPRECATED. Replaced by `Charter Pack`. Retired by the charter-pack cutover; see the Charter Pack entry.",
    "doctrine-pack-id": "DEPRECATED. Replaced by `charter_pack_id`, the identity of a Charter Pack. See the Charter Pack entry.",
    "doctrine-catalog": "DEPRECATED. Replaced by `charter offering`: everything offered to a project. See the Charter offering entry.",
    "charter-selection": "DEPRECATED. Replaced by `active charter`: what a project has activated. See the Active charter entry.",
    "pack-default-charter": "DEPRECATED. Replaced by `activation preset`: the built-in pack's default preset. See the Activation preset entry.",
}
def drop_docs_context_pointers(text: str) -> str:
    """Remove each sentence 'See the <X> entry in docs/context/<page>.md.', a pointer at core's docs a consumer lacks."""
    while True:
        start = text.find("See the ")
        marker = text.find(" entry in docs/context/", start) if start >= 0 else -1
        end = text.find(".md.", marker) if marker >= 0 else -1
        if start < 0 or marker < 0 or end < 0 or "." in text[start:marker]:
            return text
        text = text[:start].rstrip() + text[end + len(".md."):]
#: Pre-existing terms whose status changes (ids kept, so the change is not breaking).
STATUS = {"review-py-package": "deprecated"}
FIELD = re.compile(r"^    [a-z_]+:")


sys.path.insert(0, str(Path(__file__).parent))
from build_ledger import REPO  # noqa: E402
from render_terms import OPERATOR, operatorize  # noqa: E402


def main() -> None:
    path = REPO / "packs/foundation/glossaries/spec-kitty-core.glossary.yaml"
    for term in yaml.safe_load(path.read_text(encoding="utf-8"))["terms"]:  # #139: operator wording everywhere
        text = REWRITE.get(term["id"], term["definition"])
        cleaned = drop_docs_context_pointers(operatorize(text))
        if cleaned != term["definition"]:
            REWRITE[term["id"]] = cleaned
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    out, current, skipping, done = [], None, False, set()
    for line in lines:
        if line.startswith("  - id: "):
            current, skipping = line[len("  - id: "):].strip(), False
        elif skipping and not FIELD.match(line):
            continue  # a continuation line of the replaced definition
        else:
            skipping = False
        if current in STATUS and line.startswith("    status:"):
            out.append(f"    status: {STATUS[current]}\n")
            continue
        if current in REWRITE and line.startswith("    definition:"):
            block = yaml.safe_dump({"definition": REWRITE[current]}, width=116, allow_unicode=True, sort_keys=False)
            out.append("".join(f"    {part}\n" for part in block.rstrip("\n").split("\n")))
            skipping, done = True, done | {current}
            continue
        out.append(line)
    missing = set(REWRITE) - done
    if missing:
        sys.exit(f"terms not found: {sorted(missing)}")
    path.write_text("".join(out), encoding="utf-8")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    got = {t["id"]: t["definition"] for t in data["terms"] if t["id"] in REWRITE}
    assert got == REWRITE, [k for k in REWRITE if got.get(k) != REWRITE[k]]
    print(f"rewrote {len(done)} definitions", file=sys.stderr)


if __name__ == "__main__":
    main()
