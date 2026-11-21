---
affected_files: []
cycle_number: 1
mission_slug: citation-and-docs-writing-01M7YGMQ
reproduction_command:
reviewed_at: '2026-11-21T07:54:46Z'
reviewer_agent: claude::reviewer-renata
wp_id: WP03
---

**Issue 1 (blocking): new comms-cleo edge steals the existing edge's `reason`** - `packs/writing/agent_profile.graph.yaml`.

The new edge was inserted between the `relation: requires` line of the existing edge `agent_profile:comms-cleo -> tactic:writing-audience-catalog` and that edge's `reason:` block. As a result:
- the `requires` edge to `tactic:writing-audience-catalog` lost its rationale, and
- the new `suggests` edge to `styleguide:ai-writing-tells` now carries the wrong reason: "Provides the ready-to-use catalog of writing-audience personas needed to satisfy the Audience-Oriented Writing directive. ... this is about who is reading the prose, not who has a stake in a design decision."

Fix: move the `reason:` block (all four lines) back under `target: tactic:writing-audience-catalog` / `relation: requires`, and put the new edge after it. Optionally give the new edge its own short reason, e.g. `reason: The shared AI-writing tells list is the check comms-cleo runs before publishing a page (FR-010).` Re-run `python3 -m pytest -q tests/ci/test_graph_edge_identity.py` afterwards. The test passes now because it checks only edge identity, not attached fields.

**Note (not blocking; a rationale was requested for edits outside the owned files):** the edits to `packs/internal/README.md` (tree comment) and `packs/internal/styleguides/executive-debrief.styleguide.yaml` (anti-pattern "Restating report-writing here", which now says em-dash and buzzword rules belong to ai-writing-tells) are needed follow-ups to FR-009. Without them both files would name report-writing as the owner of the tells. Keep them. A one-line mention in the resubmission note is enough.

Everything else checks out. The seven tells are in `ai-writing-tells` only (none left in report-writing; grep finds no other copy). Principles are 194/194/196 chars, and the report-writing pointer is 239 chars. Examples are neutral. All FR-004 and FR-010 edges are present: specify and plan scope research-citation-discipline; documentation mission type, generate and validate scope ai-writing-tells; comms-cleo suggests it; the tells styleguide suggests plain-language. The internal edge `report-writing refines writing::styleguide:ai-writing-tells` and the node title are updated. Graph-edge, ASCII and vocabulary gates pass.
