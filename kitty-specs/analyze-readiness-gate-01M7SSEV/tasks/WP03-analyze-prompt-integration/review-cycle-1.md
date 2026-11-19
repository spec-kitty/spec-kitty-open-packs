---
affected_files: []
cycle_number: 1
mission_slug: analyze-readiness-gate-01M7SSEV
reproduction_command:
reviewed_at: '2026-11-19T13:56:33Z'
reviewer_agent: claude::generic-reviewer
wp_id: WP03
---

# WP03 review feedback - changes requested

Reviewed: lane-c @ 25f70dc, the whole `analyze.prompt.md`, including the unreviewed #246 draft from 59e1574. Independent reviewer: claude::generic-reviewer (session_019C2Tk5NruMoumnqkuwALns).

## F1 (must fix) - the version gate comes after the command it gates (FR-004, FR-005, US2.1)

Step 2a puts `spec-kitty --version` and `finalize-tasks --validate-only ...` in one code block. The rule "Below 3.1.0a5, do **not** run it" only appears after the block. An agent that runs the block runs both lines. Below 3.1.0a5 that is exactly the case where `--validate-only` writes, so the read-only guarantee fails on the hosts the gate exists for.

Fix: split the step.
1. Run `spec-kitty --version`.
2. If it is below 3.1.0a5 (or missing), stop and record the could-not-run finding.
3. Only then show the `--validate-only` command, in its own block.

## F2 (must fix) - resolution errors are classified as refusals before the could-not-run carve-out (FR-004, US2.2)

Two rules catch resolution errors as refusals:
- line 96: "Exit code non-zero with an `error` payload: a validation refusal ... CRITICAL";
- line 113: the table row "any other `error` or `error_code` | Report it verbatim".

Both match `MISSION_CONTEXT_UNRESOLVED` and `MISSION_AMBIGUOUS_SELECTOR`, which exit 1 (research R1). The rule that makes them HIGH could-not-run only comes later, at line 124. Read top-down, US2.2 yields a CRITICAL refusal.

Fix: classify could-not-run first. Alternatively, have lines 96 and 113 explicitly exclude the resolution `error_code`s and point to the could-not-run paragraph.

## F3 (must fix) - one defect is reported twice, beyond the R6 pair

The 2b dedupe line covers pairing and cycles only. Other defects still produce a second finding:
- 2b blocker "a WP mapped to no requirement" repeats 2a `missing_requirement_refs_wps` (a W finding as well as the V finding).
- Pass E "Requirements with zero associated tasks" repeats 2a `unmapped_functional_requirements`. That gives a CRITICAL V finding plus a C finding, and changes counts between hosts where the check ran and hosts where it could not.
- Pass F "Task ordering contradictions" and pass E "Tasks with no mapped requirement" overlap the same way with `cycles` and `missing_requirement_refs_wps`.

Fix: replace the narrow sentence with one general rule. Whenever a `V` finding already covers a defect, every later step (2b, passes A-G) cites that `V` id instead of raising its own finding. Mention the coverage table: it can still show the row, citing the V id.

## F4 (must fix) - the B/G split does not reliably produce US4's expected output

US4: "the system should be fast". Pass G says: "Pass B keeps vague adjectives and placeholders; pass G judges the rest." That leaves two readings, and both are wrong:
- an agent emits only B1, so there is no requirement-quality (Q) finding, and US4's Independent Test fails;
- or it emits B1 plus a Q finding for the same words, which is double reporting.

Fix: state the rule for a requirement that fails on a vague adjective, so that US4 yields exactly what its test expects. Two possible rules:
- (a) B reports the wording. G raises a Q finding only for the other properties it fails (here: testable), citing the B id. The clarification question attaches to the HIGH one.
- (b) A vague adjective inside an FR/NFR row is a Q finding, and B keeps vague wording elsewhere (plan, tasks, stories).

Either works; pick one and say it in one line.

## F5 (should fix) - "numbered in order of appearance" is undefined (NFR-002)

Order of appearance in the report depends on how the agent orders the table, so ids can renumber on a rerun.

Fix: define the order. Number by step (2a, 2b, then passes A-G); within a step, by artifact (spec.md, plan.md, tasks.md, WP files in id order), then by line.

## F6 (question for the operator, non-blocking for me) - `validation_stage: tasks-outline` -> CRITICAL is not in the ruling or in data-model.md's severity map

The severity may well be right. But it is a new source the map does not list, and it would also double-report with 2b's missing-prompt blockers (see F3).

Fix: add it to data-model.md with operator sign-off, or fold it into the 2b missing-files blockers.

## F7 (nit) - remediation verbs inside 2a

In 2a, "(run `/spec-kitty.tasks-packages`)", "(re-run `/spec-kitty.tasks-finalize`)" and "(run `/spec-kitty.tasks-finalize`)" read as instructions to the analyzing agent. Phrase them as the finding's recommendation, for example "Recommendation: run ...". That keeps the non-remediating rule unambiguous.

## Challenges

1. Read-only: the prohibitions are complete. Every `finalize-tasks` mention is `--validate-only`, a prohibition, or prose (line 16). The hole is F1.
2. Version gate: could-not-run is HIGH everywhere, and there is no MEDIUM residue. Gate ordering is F1; classification order is F2.
3. Determinism: the prefixes match the ruling exactly (D/B/U/K/C/I and V/W/Q/S), the sections are always present with "None.", and the order is fixed. Numbering is F5.
4. B/G split: F4. 2a vs 2b: R6 is applied for pairing and cycles, but F3 covers the rest.
5. C-002: clean. The template is only "as resolved"; the payload keys belong to the CLI, not the template. Tactic citations are one-line summaries, and restating the FR-008 thresholds is justified by FR-008.
6. User stories:
   - US1.1-1.4: reachable;
   - US2.1: F1;
   - US2.2: F2;
   - US3.1-3.3: reachable via 2b and the tactic;
   - US4.1-4.3: reachable except the Q finding in the Independent Test (F4).

## Passed

- The severity map matches the rulings:
  - refusal CRITICAL;
  - stale / `would_modify` HIGH;
  - warnings MEDIUM;
  - collapsed lane LOW;
  - could-not-run HIGH with `>= 3.1.0a5` named;
  - the carrier is unchanged, with closed severities.
- Fail-fast residual risk is stated (lines 94, 248 and 271).
- Gates:
  - passed: 373 lines (cap 500), ASCII, vocabulary 0;
  - `tests/ci` passes except 11 errors in `test_prompt_fragments` and `test_validate_pack_schemas`, which all come from the charter contract fetch returning 404 in the reviewer's environment, not from this WP;
  - validate-packs was not reproduced (same cause); CI must confirm.
