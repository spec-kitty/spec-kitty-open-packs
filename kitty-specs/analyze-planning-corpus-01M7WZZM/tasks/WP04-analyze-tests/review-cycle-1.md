---
affected_files: []
cycle_number: 1
mission_slug: analyze-planning-corpus-01M7WZZM
reproduction_command:
reviewed_at: '2026-11-20T18:04:37Z'
reviewer_agent: claude:opus:reviewer-renata
wp_id: WP04
---

# WP04 review feedback (reviewer-renata)

Red proof re-run independently on 3bedeef: exactly 17 tests fail (12 + the 5 whose subtests fail: both_tactics_cited, tactic_files_parse, graph_wires, recommendation_literal, cave_prompt_parity); all 7 ratchets pass. Full suite in lane: 357 passed. FR-016 coverage is complete. Two fixes needed, both small:

1. **[MEDIUM] Cap positive control does not exercise the HIGH/CRITICAL branch** — tests/ci/test_analyze_readiness_prompts.py:338-346 (helper at :208-216).
   The `bad` line `- **HIGH**: a product-coherence finding that changes what gets built` lacks both "never higher" and "MEDIUM", so `coherence_capped` returns False through the final `any/all` line regardless of the HIGH regex at :214. Deleting the HIGH/CRITICAL check leaves the control green, so the control is vacuous for the exact regression T014 asks it to prove.
   Fix: make the bad block otherwise valid, so only the tier check can reject it, e.g.
   `good + f"- **{tier}**: product-coherence findings are MEDIUM, never higher\n"` -> assertFalse.

2. **[LOW] Five positive controls are tagged "red-first" but pass on 3bedeef by design** — :277, :295, :307, :339, :355.
   The module docstring (:10-12) defines red-first as "fails on the pre-change prompts"; these run on synthetic text only and passed in the red proof. Tag them "control" (and add that third tag to the module docstring) so the red-first/ratchet ledger is honest.

Nits (optional, no re-review needed for these):
- :391, :418, :424 are red-first tests living in `ExistingContentRatchetTest`; consider a note in the class docstring or moving FR-018 pins to their own class.
- :276-280 graph control only asserts NotIn of edges that never existed; it shows membership can be False but not that `graph_edges` would miss a removed edge. Acceptable as-is.
