---
affected_files: []
cycle_number: 2
mission_slug: pack-doctor-alignment-01M88RH1
reproduction_command:
reviewed_at: '2026-11-26T16:25:08Z'
reviewer_agent: claude::reviewer-renata
wp_id: WP10
---

# WP10 review cycle 2: changes requested

Reviewer: claude::reviewer-renata, an in-session reviewer subagent. Reviewed the fold 67e72665.

## Required

R1. `unlisted_nodes` still repeats part of `manifest_membership`. This breaks C-003 and goes beyond decision 01M8BMA8KVQH0CXKAT05RW7Z9X.
- The rule fires on every unlisted node of a non-exempt kind, including nodes backed by a file the jar already refuses as `manifest_membership`.
- Probe: a tactic file left out of the manifest. The jar refuses it with `manifest_membership`, and Python also names `tactic:...`.
- The new comments, the `validate-packs.sh:58` header and the `MANIFEST_EXEMPT_NODE_KINDS` note describe it as "a graph node no file declares", which is wrong.
- Fix:
  - restrict `unlisted_nodes` to nodes whose `kind:id` no file the pack holds declares;
  - keep the ghost-node test;
  - add a test that a file-backed unlisted node is no longer named.

## Nits

N1. The `classify` comment (#348 comment 3) should name the kept rules that depend on it:
- the profile-reference house rules, through `held_artifacts` and `profile_references`;
- `unlisted_nodes`, through `declared_nodes`;
- `charter_service_check.py`'s `file_not_held` policy.

## Verified
- R1, N2 and N5 from cycle 1 are fixed (proven by revert, with prompt_path edge cases probed).
- `unlisted_constituents` is retired and nothing is left uncovered: the charter derives membership for every kind, and a later fault in the same pack does not hide it.
- The suites, real-jar tests, validate-packs.sh, the gate and the grep all pass.
- The lazy import works, and the CI job installs the dependencies.
