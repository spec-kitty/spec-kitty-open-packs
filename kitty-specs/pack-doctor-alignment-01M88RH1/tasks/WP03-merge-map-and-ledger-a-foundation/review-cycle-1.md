---
affected_files: []
cycle_number: 1
mission_slug: pack-doctor-alignment-01M88RH1
reproduction_command:
reviewed_at: '2026-11-25T16:15:41Z'
reviewer_agent: claude::reviewer-renata
wp_id: WP03
---

**Issue 1: theme merge in the merge map (M1: strict same-claim; Q1: "A merge whose meanings genuinely differ becomes an operator question").**
Cluster `returning-final-minutes-while-attribution-gaps-remain` (writing) joins two different claims:
- `writing procedures/meeting-minutes-pipeline.procedure.yaml#/anti_patterns/1` "Returning final minutes while attribution gaps remain": a pipeline-gate failure ("do not return the final Markdown, and do not hand off for publishing until the gate passes"; "Do not invent owners").
- `writing styleguides/meeting-minutes-format.styleguide.yaml#/anti_patterns/1` "Unattributed action items": a content defect ("Recording an action without a named owner. 'The team', 'TBD', 'everyone'…"). It names the pipeline's refusal as a consequence, not as its claim.

The merge_reason's shared quote, "Unowned action items cannot be followed up", is the procedure's rationale, not its claim. Under U3 the home file would carry the procedure's title and text, which the styleguide's rule ("Owner: TBD") does not state. Split it into two singletons, or raise it as an operator_question in the map. Either way it is a merge-map change, so ledger B (WP04) inherits it.

**Issue 2: required WP-history records are missing.** `status.events.jsonl` has only the subtasks annotation and the for_review note for WP03. The prompt requires these `add-history` records:
- T014: the cluster count and the per-home counts ("WP04-WP07 read their row counts from it"). Per-home now: internal 57, writing 38, testing 32, foundation 28, planning-analysis 19, pack-authoring 14, drupal 14, javascript 13, go 8, architecture 6, rust 6, java 5, python 4, event-driven 3, qa 2. Recount after Issue 1.
- T017: that the operator questions were sent. The dispatcher transcript shows they were.
- T018: the before/after counts per code.

The commit messages carry part of this, but the WP history is the contract surface.

**Verified, no action needed:**
- All 273 entries appear exactly once across 249 clusters, with unique ids per home. Every home is in each member's depends_on closure, and no depends_on is added. Every merge_reason quote is found verbatim in its members, and each member is quoted.
- The 25 multi-member clusters are same-claim apart from Issue 1. A fuzzy scan of non-merged pairs found no missed merges.
- Rulings applied as ruled: M2 (4 authored titles and descriptions, members' examples verbatim and labelled), M3, M4 (subagent assessment recorded; Q1a-Q8a with Q3b and Q7a), M6 n/a here, W3-1 (smell). No open operator_question remains.
- Ledger A: 32 rows match the map, and titles, descriptions, good and bad examples are verbatim where not authored. The 15 rows citing the charter example-pack precedent match charter 4b95b91 in severity, bad example and text (see N2). I read every authored example (12 from the precedent, 8 of yours, the new cart/ReflectionTestUtils one, and the 4 cross-language texts). All are accurate and grounded.
- T018 reproduced at 7e1754b with a pack-doctor built from charter 4b95b91 (only _JAVA_OPTIONS cleared):
  - artifact_schema_error 61→57, substep_delegation_unresolved 3→2, drg_schema_error 15→0;
  - after remediating foundation, 87 violations (excluding validation_failed summaries), with no new code;
  - a second apply is byte-identical;
  - --check reports only later-batch blocks and map members;
  - 36 tests pass.
- WP02 tool delta (also_rejects, also_rejected_by, reason_update, replace_list_items) reviewed. It is sound, idempotent, refused outside the closure, and its re-parse proof holds. The three edge reasons are rewritten and the TDD edge is untouched.

**Process note:** `spec-kitty agent action review WP03` is refused by the bulk-edit diff-compliance gate. The occurrence map's `kitty-specs/**` do_not_change exception catches the curation README edit. The dispatcher accepted that edit, but the gate will refuse again on re-review unless the occurrence map gets an exception for `kitty-specs/pack-doctor-alignment-01M88RH1/curation/**` (or the dispatcher rules on it).

**Nits (optional):**
- N1: two quoted grounding clauses are cut mid-phrase. `trusting-a-biased-delegate` ends at "(e", split on "e.g.", and `unbounded-squad` ends at "a small".
- N2: the `hard-wiring-the-squad-as-a-gate` grounding says "the source adds its own Bad/Good sentences". The charter text has them too; the only difference is the e.g. (charter "raising a StatusGateError", source "a squad report is attached"). The authored bad example uses the charter's StatusGateError.
- N3: the verbatim java good_example in `storage-or-wire-format-on-domain-types` says "PaymentStatus follows the fromByte pattern above". In a foundation file that reference dangles. It is verbatim, so it is for the operator to rule on if wanted.
- N4: `retire-coverage-disguised-as-a-duplicate` is same-claim (delete only after proving a covering guard). The internal member's trigger ("because its Mission closed") is not a disguised duplicate, so the home title is narrower than that member. I accept it as is.
- N5: --check's reason_update scan does not filter on relation == rejects, while apply does. This is harmless.
