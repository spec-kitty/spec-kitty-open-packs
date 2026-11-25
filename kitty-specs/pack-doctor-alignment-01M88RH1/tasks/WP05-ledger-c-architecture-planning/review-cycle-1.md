---
affected_files: []
cycle_number: 1
mission_slug: pack-doctor-alignment-01M88RH1
reproduction_command:
reviewed_at: '2026-11-25T17:58:17Z'
reviewer_agent: claude::reviewer-renata
wp_id: WP05
---

# WP05 review cycle 1: changes requested

Reviewer: claude::reviewer-renata. Reviewed at 18515cd (coordination branch).

## Required

**R1. `skipping-the-existing-artifact-overlap-audit`: the authored bad example misstates a real directive.**
`pack-authoring` `procedures/onboard-external-agent-to-pack.procedure.yaml#/anti_patterns/6`. The example says
"`READABLE_CONSISTENT_PRS` already enforces the same size limit." No directive has that id: the real one is
`DIRECTIVE_046` ("Readable and Consistent Pull Requests",
`packs/foundation/directives/046-readable-consistent-prs.directive.yaml`), and it enforces no PR size limit (it
requires linear history, complete scope and independent review). This is new doctrine (Q3), so it must not make a
false claim about shipped doctrine. Either use clearly invented artifacts with ids in the real form (for example two
project-tier directives `DIRECTIVE_101` and `DIRECTIVE_117` that both cap PR size), or cite a real overlap
accurately.

**R2. `multiple-active-state-labels`: the example's states are not the procedure's.**
`procedures/issue-triage-state-machine.procedure.yaml#/anti_patterns/0`. The host procedure is tracker-neutral and
names its states `needs-triage, needs-info, ready-for-agent, ready-for-human, wontfix`; `status:blocked` is not one of
them. Use two of the procedure's own states (for example `ready-for-agent` and `needs-info`).

**R3. `ignoring-external-references`: the offending artifact is the remedy.**
`procedures/onboard-external-agent-to-pack.procedure.yaml#/anti_patterns/8`. The example makes a *toolguide* the
artifact that assumes Jira, while the content (and the procedure's step) says the fix is to author a toolguide or
document the dependency. Make the offending artifact a tactic, directive or procedure that calls the external API,
with no covering toolguide and no owner acknowledgement.

## Nits (fix if cheap; not blocking)

- N1. `blocking-on-the-optional-steps` grounding says "a merge or report held needlessly"; nothing here is a merge.
  "a report held needlessly" is enough.
- N2. `child-ticket-checklist-in-the-epic-body` grounding glosses the quote as "the record becomes wrong -> severe";
  the rubric's own example maps "a wrong result" to `breaking`. The call (severe) is supported by the quote; reword the
  gloss (e.g. "the tracking drifts from the source of truth") so a reader does not see a rubric contradiction.
- N3 (tool, residual for WP06/WP07). `build_corpus` adds every row's `bad_example` to the corpus, including authored
  ones, so a curator-written example containing "default" can make a matching grounding quote pass the guard. No
  current ledger does this (no grounding or merge reason in ledgers 00-C mentions "default"). Consider excluding
  `bad_example` rows whose `bad_example_source` starts with `authored`. Also `except yaml.YAMLError: continue` there is
  fail-safe (a skipped document only makes the guard stricter) but deserves a one-line comment.
- Observation, not a ruling: `over-reading-squash-merged-history` (severe, "will undercount activity") and
  `decomposing-before-understanding-the-agent` (breaking, "misrepresent its behaviour") are both read as wrong
  results with different calls. The severe call is defensible (the text asks to corroborate "before drawing strong
  conclusions"); flagging only for cross-batch consistency.

## Verified (no change needed)

- Coverage: 46 rows = the 46 members of the 42 merge-map clusters homed in architecture, event-driven, pack-authoring,
  planning-analysis (none in refactoring/spdd); ids, homes, `merged_into` and `merge_reason` agree with the map.
- Verbatim: every `source_title`, `owner`, `title`, `description`, `good_example` and source `bad_example` matches its
  source; every quoted span in every `severity_grounding`, every authored `bad_example_source` clause, and every
  `merge_reason` quote appears verbatim in the entry (merge quotes in the named member).
- Merges (M1): the three multi-member clusters make the same claim; meta-tracker's internal#78 member follows decision
  01M89PV9YNGP5YCABX4HJ8Y1MW. No theme merges. U3: each home row carries the planning-analysis member's text.
- Authored bad examples: all 29 read; all are on singleton title/content entries with no verbatim example among
  cluster members (R1 per 01M89Q9JT79VYFMBRNPS9BHHP1). Apart from R1-R3 they are concrete, minimal and faithful.
- Charter precedent: `direct-object-references` and `transaction-spanning` match the charter's
  `service/packs/src/testFixtures/resources/example-packs/built-in/anti_patterns/` files (charter 4b95b9151) in text,
  examples and severity `severe`.
- Severity questions C1-C4 (scope-creep, solution-mode, host-specific-assumptions, treating-triage-as-a-verdict) are
  with the operator; not decided here.
- Default guard: refuses made-up quotes ('"by default"', '"default state of the world"', a bare '"default"') and
  allows real ones, including a whitespace-reflowed real quote. 39 tests pass.
- Parse cache: per-Tree, keyed by path and validated against the exact text, so no cross-file or post-edit staleness
  (probed: a pending write, a disk edit and a revert each re-parse); no caller mutates a loaded document. Ledgers
  00-C with the cache disabled give byte-identical apply logs, an identical tree and identical `--check` output
  (25 s vs 2.5 s).
- Dry run reproduced on a scratch copy (questions cleared on the copy only): C deletes 11 inline blocks
  (architecture 2, event-driven 1, pack-authoring 3, planning-analysis 5), keeps 10 for later batches; a second apply
  writes nothing; `--check` reports only later batches (25 blocks still carrying `anti_patterns`, 115 map members
  without rows), none in C's homes. The pack-doctor code counts were not reproduced this cycle (charter jar build);
  to be checked on resubmission.

## Checklist

1 dead code PASS (`build_corpus` called from `plan_apply` and `check`); 2 synthetic fixture PASS (tests drive
`says_default` and the ledger refusal path); 3 silent empty return PASS (see N3); 4 FR coverage N/A (ledger work);
5 frozen surface PASS (no `packs/` edits); 6 locked decision PASS; 7 shared-file ownership PASS with note:
`apply_curation.py` and its tests are WP02's files, changed here as named WP02-tool changes in the shared planning
lane; 8 production fragility N/A.
