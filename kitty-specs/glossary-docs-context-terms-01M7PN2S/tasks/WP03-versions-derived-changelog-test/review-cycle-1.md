---
affected_files: []
cycle_number: 1
mission_slug: glossary-docs-context-terms-01M7PN2S
reproduction_command:
reviewed_at: '2026-11-18T07:05:15Z'
reviewer_agent: claude-reviewer-019C2Tk4
wp_id: WP03
---

# WP03 review, cycle 1 (claude-reviewer-019C2Tk4, independent session): changes requested

## Passes
- FR-008 (DIRECTIVE_018): foundation 2.0.0→2.1.0 and internal 4.0.0→4.1.0. Every exact pin in the 19 packs equals its target's current version: writing 2.1.0; testing, refactoring, architecture and planning-analysis 2.2.0; built-in 4.1.0. Range pins (`>=2.0,<3`) still hold.
- FR-009 / C-005: `check-pack-digests.sh` ok; `gen_pack_reference.py --check` reports no drift on 19 pages; the manifest and sidecar diffs are version and hash only.
- FR-011: `test_glossary_content.py` reads the shipped files, so it would fail without them. It pins the Op term (id, name, active, alias, see_also, the DIRECTIVE_053 phrases), the four mission types, the citation scan with a positive control, the authoring-source description and header, and uniqueness and see_also in both contexts. It also keeps house terms out of foundation. All of it passes.
- Vocabulary: 0 findings. tests/assets, docs, release and vocabulary pass. In tests/ci, only the 3 setUpClass errors that need the private charter contract fail here; CI covers those.
- Shared files: `tests/ci/test_pack_digest.py` (the BUILT_IN_DIGEST restamp) is outside owned_files. It is a derived constant that has to follow the digest, so this is accepted as coordination.

## Issue 1 (SC-004 / NFR-001, blocking): the SonarCloud quality gate fails on the PR head
The "SonarCloud Code Analysis" check on PR #300 fails: "E Security Rating on New Code" and "C Reliability Rating on New Code", where A is required. It passed on #293, so this PR introduces the failure. The new Python on this PR is the three mission tools (`kitty-specs/.../tools/build_ledger.py`, `render_terms.py`, `clean_existing.py`) and `tests/ci/test_glossary_content.py`.

This container cannot reach sonarcloud.io, so I could not read the issue list. Please pull it from the dashboard (PR 300) and fix or justify each issue.

Likely suspects:
- `render_terms.py:40`: a nested-quantifier regex with alternation (ReDoS, python:S5852 / S5998).
- Write paths built from `sys.argv` (`render_terms.py`, `clean_existing.py`, `build_ledger.py`): pythonsecurity:S2083 path injection.

A Sonar exclusion for `kitty-specs/**/tools/**` is a repository policy call, not a WP decision. Raise it with the orchestrator if you prefer it to code fixes.

Also confirm "Charter service validation" goes green on the final head. It was still running at review time.

## Issue 2 (FR-010, blocking, small): the changelog count is stale
The CHANGELOG entry says "23 pre-existing definitions drop core source paths …". After the WP01 cycle-2 fix, research.md says 28. Make the changelog match.

## Non-blocking
- The version policy is pending with the operator, per the orchestrator. If the operator changes it, the bumps stay isolated to `packs/*/pack.yaml` and the derived files follow.

## Anti-pattern checklist
1 dead code PASS (the test is collected by `unittest discover`). 2 synthetic fixture PASS (the test reads the shipped files; the positive control only checks the regex). 3 silent empty return N/A. 4 FR coverage PASS for FR-011; FR-008/009/010 are gate- and doc-checked. 5 frozen surface PASS. 6 locked decision PASS. 7 shared-file ownership: `test_pack_digest.py` is noted above. 8 production fragility N/A.
