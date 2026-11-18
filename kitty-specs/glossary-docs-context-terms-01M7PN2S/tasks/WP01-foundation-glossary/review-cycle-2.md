---
affected_files: []
cycle_number: 2
mission_slug: glossary-docs-context-terms-01M7PN2S
reproduction_command:
reviewed_at: '2026-11-18T06:54:06Z'
reviewer_agent: claude-reviewer-019C2Tk4
wp_id: WP01
---

# WP01 review, cycle 2 (claude-reviewer-019C2Tk4, independent session): changes requested

Reviewed `spec-kitty-core.glossary.yaml` at 823b86b. That commit holds the WP01 state; the recorded range ends at 1ff718a, so the range is stale.

## Passes
- FR-001 / SC-001: `op` is active, aliased "profile invocation" and sees `mission`. Its open, close, no-artifacts, one-sitting and swept-to-abandoned wording matches DIRECTIVE_053.
- FR-002 / NFR-002 / SC-002 (foundation half): the ledger has 297 rows, every row has a reason, and no source term appears twice. All 156 `foundation` rows and all `exists`/`alias` rows resolve to a term.
- FR-003: every `see_also` resolves within `spec-kitty-core`. The status deviations are recorded (decision 5).
- FR-006: the four mission-type terms are present. FR-007: the header and description name the file as the authoring source, and "migrated from" is gone.
- NFR-003: 294 terms, with 0 duplicate ids, 0 duplicate names and 0 alias collisions. C-001: no new context.
- C-002: no id is removed or renamed. A whitespace-normalised diff of the 23 changed pre-existing definitions shows only citation removal, retired-wording fixes and the `WorkPackage` alias.
- `check_vocabulary.py`: 0 findings. CI "Charter Pack validation" is green on the PR head.

## Issue 1 (FR-005, blocking): five pre-existing definitions still cite core internals
823b86b cleaned `target-branch` of "Since WP07 (FR-012)" and `resolve_planning_branch_from_meta()`. Its sibling terms keep the same kind of citation:

- `structural-debt`: "Canonical example: `doctor.py::mission_state` at CC 57 …" and "WP06 of mission `quality-devex-hardening-3-2-01KRJGKH` extracted it …". These are a core source path, symbol and mission. Drop the example sentences, as was done for `deliberate-linearity`'s `_auth_doctor.py::render_report`.
- `current-branch`: "Since WP07 (FR-012), spec-kitty refuses …". Drop "Since WP07 (FR-012)," (the reader will also confuse it with this mission's own FR-012).
- `merge-target-branch`: "read as a fallback by resolve_planning_branch_from_meta() when target_branch is absent (pre-WP03 missions)" and "(pre-WP07 pattern …)". Say "read as a fallback when target_branch is absent (older missions)", and drop the WP numbers.
- `planning-base-branch`: "(pre-WP07)". Drop it.
- `charter-content-migration`: "The WP08 scan … with the WP06 chokepoint contract". Reword without core WP numbers (for example "The scan + normalize-or-fail-loud flow that brings existing missions' charter content into compliance with the charter chokepoint contract"). If it cannot be made consumer-meaningful, deprecate it as `review-py-package` was.

All five edits are citation removal, which C-002 allows. Put them in `tools/clean_existing.py` / `rewrites.yaml` so the pipeline stays reproducible, and update the count in research.md ("23 pre-existing definitions").

Check: this scan returns nothing over the definitions:
`\bWP\d+\b|\bFR-\d+|\w+\(\)|::\w+|\.py\b`

## Non-blocking
- Decide whether `deliberate-linearity` ("regardless of Sonar S3776 score") and `sonar-quality-gate` are consumer terms. They are pre-existing, so this is not required here.

## Anti-pattern checklist
1 dead code N/A (content). 2 synthetic fixture N/A (the test is WP03). 3 silent empty return N/A. 4 FR coverage: the FR-011 test is WP03's, and it is checked there. 5 frozen surface PASS. 6 locked decision PASS. 7 shared-file ownership PASS (only WP02 commits touch the internal glossary; research/ and tools/ are noted in the move reason). 8 production fragility N/A.
