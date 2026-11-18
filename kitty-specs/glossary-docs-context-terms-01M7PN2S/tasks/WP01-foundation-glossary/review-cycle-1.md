---
affected_files: []
cycle_number: 1
mission_slug: glossary-docs-context-terms-01M7PN2S
reproduction_command:
reviewed_at: '2026-11-18T06:40:14Z'
reviewer_agent: user
wp_id: WP01
---

# WP01 review (reviewer-renata): changes requested

1. `guideline`: core-only doctrine concept (no charter artifact kind or precedence layer) — exclude.
2. `import-candidate`: core's curation record, no charter counterpart — internal.
3. `artifactref` (code type) and `baseline-key` (code fields) — internal, consistent with CharterScope etc.
4. `clarification-burst-policy`: not implemented per its own text — draft, say "not shipped".
5. `mostly-invisible-process`, `highly-visible-outcomes`, `append-only-semantic-history`, `deterministic-gate-human-clarification`: core glossary-runtime design principles — internal.
6. Status deviations from the FR-003 map (glossary-vocabulary, delegation, refinement → draft; agent-profile → active) need a recorded rationale.
7. Ledger verdict `folded` is not one of FR-002's verdicts — amend FR-002 or change the rows.
8. `schema`: "used in CI/tests" describes core's CI — say pack validation rejects invalid artifacts.
9. `execution-mode-stamp`: "older code" refers to core code — reword.
10. `op`: add that a sweep to abandoned is a lapse, not a completion (DIRECTIVE_053).
11. Ownership: note the non-owned mission files (research/, tools/) touched in the shared lane.
12. Every foundation ledger row carries the same boilerplate reason; give a per-row/per-page justification.

Folded in on rework (orchestrator): #139 — the glossary contexts say "the operator", not HiC / Human-in-Charge / human-in-command; and FR-005 extends to the 17 pre-existing foundation definitions that cite core paths, ADRs or docs/context.
