---
work_package_id: WP04
title: Self-binding vocabulary precision (#304)
dependencies: []
requirement_refs:
- FR-009
- SC-001
planning_base_branch: ci/release-pin-follow-through
merge_target_branch: ci/release-pin-follow-through
branch_strategy: Planning artifacts for this mission were generated on ci/release-pin-follow-through. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into ci/release-pin-follow-through unless the human explicitly redirects the landing branch.
subtasks:
- T015
- T016
- T017
- T018
history:
- at: '2026-11-24T16:00:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: python-pedro
authoritative_surface: scripts/ci/check_vocabulary.py
create_intent: []
execution_mode: code_change
model: ''
owned_files:
- scripts/ci/check_vocabulary.py
- tests/vocabulary/test_check_vocabulary.py
role: implementer
tags: []
tracker_refs:
- '#304'
---
# Work Package Prompt: WP04 – Self-binding vocabulary precision (#304)

## ⚡ Do This First: Load Agent Profile

Load the assigned profile with `/spk-charter-profile-load python-pedro` before reading anything else.

## Objective

The `SELF_BINDING` patterns in `scripts/ci/check_vocabulary.py` (l.118–140) catch prose that states a directive's enforcement level. They over-match ordinary sentences and miss simple variants (#304). Fix both, with one test case each (FR-009, SC-001).

## Branch Strategy

The planning branch and merge target is `ci/release-pin-follow-through`. Worktrees are allocated per lane from `lanes.json`. Implement with `spec-kitty agent action implement WP04 --agent <name> --mission release-pin-follow-through-01M872WA`.

## Subtasks

### T015 — Red tests

File: `tests/vocabulary/test_check_vocabulary.py`, the class holding `test_refuses_every_self_binding_phrase` and `test_spares_other_senses_and_the_field`. Add the cases to the existing `subTest` lists, or as new tests.

**Must pass, with 0 findings each** (false positives):
- "The rule is mandatory reading for reviewers."
- "the directive is required by the charter"
- "Open the advisory context menu."
- "Spring makes rules binding at startup, then the service reads every directive and its rules binding the request."

The fourth case aims at the 160-character `makes? … rules? binding` reach. Keep the sentence realistic, and make sure the old pattern flags it, so the test is red today.

**Must flag, with 1 finding each** (false negatives):
- "This directive is strictly advisory."
- "Advisory in version 1."
- "These rules are mandatory."
- "An advisory-only directive."
- "This directive is non-blocking."

Run the tests and confirm that all nine fail before any pattern change. Record that in the commit body.

### T016 — Anchor the false-positive patterns

Anchor the adjective to the end of a clause, as #304 suggests. After the level word, require a clause boundary, `(?=\s*(?:[.;:,)!?]|$|\s+(?:and|but|in|at|for|until)\b))`, or another equivalent that keeps every existing positive case in `test_refuses_every_self_binding_phrase` flagged.
- `the rule is mandatory reading` → spared.
- `the directive is required by the charter` → spared. "required by" is activation, not strength. Exclude `required` followed by `by`, or anchor as above.
- `advisory context` → drop it, or restrict it to the self-binding sense ("is advisory context", "as advisory context"). Check which existing pack prose motivated it: `git log -S'advisory\s+context' -- scripts/ci/check_vocabulary.py`.
- `makes? … rules? binding`: shrink the reach to one clause, `[^.;:]{0,60}?`, and require `binding` at a clause end.

### T017 — Cover the false negatives

Add or extend patterns, each as narrow as the cases allow:
- `\b(?:strictly|purely|only|merely)\s+advisory\b`, plus the existing `this directive is …` with an optional adverb;
- `\badvisory\s+in\s+(?:version|v)\s*\d`;
- `\b(?:these|the|its)\s+(?:rules|directives)\s+are\s+(?:mandatory|advisory|binding|non-negotiable)\b`, anchored as in T016;
- `\badvisory-only\b`;
- `\b(?:this|the)\s+directive\s+is\s+non-blocking\b`, by adding `non-blocking` to the directive pattern.

### T018 — Error message and repo run

- The `::error` line for a self-binding finding must be at most 200 characters: the annotation text after `::`, excluding the `file=`/`line=` header. Shorten the message (see `findings_in`) and keep the glossary term it names (`test_findings_name_the_glossary_term`). Add an assertion on the length.
- Run `python3 scripts/ci/check_vocabulary.py` over the repo. It must report 0 findings. If a new pattern flags shipped pack prose, decide case by case: when the prose really states its own level, fix the prose, which needs an out-of-map edit recorded with a one-line rationale and a pack digest restamp (`python3 scripts/ci/pack_digest.py --update`). Otherwise narrow the pattern.

## Definition of Done

- `python3 -m unittest discover -s tests/vocabulary` passes; `python3 scripts/ci/check_vocabulary.py` exits 0.
- Every case listed in #304 has its own test case.

## Reviewer guidance

Read each new pattern against the full positive list. A pattern that matches a bare common word, such as `advisory` alone, is a regression.
