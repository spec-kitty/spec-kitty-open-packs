---
affected_files: []
cycle_number: 1
mission_slug: analyze-readiness-gate-01M7SSEV
reproduction_command:
reviewed_at: '2026-11-19T13:48:18Z'
reviewer_agent: claude::generic-reviewer
wp_id: WP02
---

# WP02 review feedback - changes requested

Reviewed: lane-b @ d627cab. Independent reviewer: claude::generic-reviewer (session_019C2Tk5NruMoumnqkuwALns).

## F1 (must fix) - boundary blocker misfires on declared dependencies

The step "Check the boundaries" says a work package "that cannot be completed without another work package's unfinished files is a blocker".

At analyze time every work package is unfinished. Read literally, this flags every declared, ordered dependency as a blocker, including this Mission's own WP01 -> WP05 chain. That contradicts the "Check dependencies and order" step, which treats ordering as delivery sense.

Fix: make the blocker an UNDECLARED dependency, one where the work package needs another work package's files or outputs but does not list that work package as a dependency. Leave declared dependencies to the dependencies step. A one-line example would help agents copy it correctly, for instance: "WP04 edits a file WP02 creates but does not list WP02 as a dependency - blocker."

## Passed (no change needed)

- Pairing both ways; cites the finalize pairing refusal instead of double-reporting (R6).
- Template deferral explicit ("as the Mission's template resolver returns it"; "keeps no list of its own"). The T006 literal-key grep is clean.
  - Challenge 1: the parenthetical names concepts, not keys. It defines which gaps block, not the template's layout, so it is acceptable under C-002.
- No severities, HIGH/LOW words, finding ids or report layout beyond the "one row per WP" the WP prompt asks for.
- Profile-first and size are improvements; the thresholds match exactly (200-500 target, >700 lines or >10 subtasks).
  - Challenge 2: the blocker/improvement split is right apart from F1.
- Read-only is stated twice and appears in failure_modes.
- #237 acceptance:
  - per-WP rows;
  - missing, orphaned, oversized, underspecified (via placeholders) and badly scoped are all reported;
  - blockers are kept apart from improvements;
  - read-only.
  - Challenge 3: covered.
- Gates:
  - passed: ASCII grep, ASCII test, vocabulary (0 findings);
  - not run by the reviewer: validate-packs (the charter contract returns 404 here; CI must confirm);
  - pack digest: stale until WP05, as expected.
