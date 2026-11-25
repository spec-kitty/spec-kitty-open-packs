---
schema_version: 1
artifact_type: spec-kitty.analysis-report
command: /spec-kitty.analyze
mission_slug: pack-doctor-alignment-01M88RH1
mission_id: 01M88RH1WRS5YA0FC3G7M3JJ49
generated_at: '2026-11-25T12:50:09.109965+00:00'
analyzer_agent: unknown
input_artifacts:
  spec.md:
    path: .worktrees/pack-doctor-alignment-01M88RH1-coord/kitty-specs/pack-doctor-alignment-01M88RH1/spec.md
    sha256: 441076f14dbe6e61a9e0b48127e4e1fd2b0b2168166b5daa3f560d786a57255c
  plan.md:
    path: .worktrees/pack-doctor-alignment-01M88RH1-coord/kitty-specs/pack-doctor-alignment-01M88RH1/plan.md
    sha256: 85bcf734964edebb9120d2c49fc2bfdbd153279e5a57cb61995227d2a9770d34
  tasks.md:
    path: .worktrees/pack-doctor-alignment-01M88RH1-coord/kitty-specs/pack-doctor-alignment-01M88RH1/tasks.md
    sha256: 519b7f963e58a0c721ad841f921b1fcf1715ab4d19cd6b29bb3ef8dc73649a84
  charter:
    path: .kittify/charter/charter.yaml
    sha256: efcfe1f5ac18032e213f3962fe660e8ea93b377b55562edf5265c2f6d8ac3ce7
verdict: ready
issue_counts:
  critical: 0
  medium: 4
  high: 0
  low: 3
  info: 0
findings:
- id: F3
  severity: medium
  category: coverage
  summary: 'NFR-005 (about 70 entries per curation WP) is strained: WP04 has 77 origin entries and WP07 72 before merged-in rows, and WP03 T014 judges all 273 entries in one merge map.'
- id: U3
  severity: medium
  category: underspecification
  summary: When a cluster merges members with different wording, no artifact says which member's verbatim title/description the home file carries; data-model.md says 'after the merge rule', but no rule defines it.
- id: C1
  severity: medium
  category: coverage
  summary: SC-001 (the nightly charter-main track green on the mission head) has no task that dispatches the charter-track ref run in CI; WP09 T049 measures locally only.
- id: U2
  severity: medium
  category: underspecification
  summary: 'The #348 line references have drifted; WP10 locates the rules by name, but the reviewer has no line map to check against.'
- id: C2
  severity: low
  category: coverage
  summary: The process constraints C-005, C-006 and C-007 map to no WP; they are owned by the orchestration and close-out.
- id: I1
  severity: low
  category: inconsistency
  summary: plan.md treats WP11 as docs-only, but finalize-tasks normalised it to code_change (docs/ paths). No behavioural effect.
- id: I2
  severity: low
  category: inconsistency
  summary: WP08 T042 uses the WP01 jar script but WP08 does not depend on WP01; the prompt gives the quickstart fallback.
---

## Specification Analysis Report

Re-run after the planning amendment `530cf28` (spec, plan and data model aligned to decisions Q1 and Q3). Resolved since the previous run: F1 (spec FR-007, US2 scenario 1, duplicates edge case), F2 (data-model ledger row, plan structure), I3 (plan re-plan marked done) and I4 (spec Key Entities gains the merge map). F3 and U3 are with the operator (dispatcher, 2026-11-25); the recommendations are to waive NFR-005's ~70 for the home-pack batches, and to take a merged file's text from the home-pack member, else the earliest source.

| ID | Category | Severity | Location(s) | Summary | Recommendation |
|----|----------|----------|-------------|---------|----------------|
| F3 | Coverage | MEDIUM | spec.md NFR-005; tasks WP03, WP04, WP07 | Batch sizes above about 70; the merge map spans all 273. | Either split WP04 (testing / writing) and accept WP07 at 72, or record an operator waiver of NFR-005 for the home-pack batching. The merge map is a clustering pass, not 273 row calls; say so in NFR-005 or WP03. |
| U3 | Underspecification | MEDIUM | data-model.md anti-pattern `description`; WP02 T011 text rules | Which member's verbatim text a merged file carries is undefined. | Add a rule (e.g. the member from the home pack, else the earliest source in the merge map) or raise it as an operator question with the merge map. |
| C1 | Coverage | MEDIUM | spec.md SC-001; WP09 T049 | No task runs the charter-track `ref` dispatch on the branch. | At close-out, dispatch Charter track (`track: ref`) on the PR branch and record the result in the PR body. |
| U2 | Underspecification | MEDIUM | WP10, issue #348 | The rule locations drifted. | Reviewers check by the rule names in #348's table; WP10 history lists the removed symbols. |
| C2 | Coverage | LOW | spec.md C-005..C-007 | Process constraints are not mapped. | Covered by orchestration and close-out. No WP change. |
| I1 | Inconsistency | LOW | plan.md; WP11 frontmatter | The WP kind was normalised. | None needed. |
| I2 | Inconsistency | LOW | WP08 T042 | Uses a WP01 surface without depending on WP01. | The fallback is in the prompt, or add a WP01 dependency. |

**Coverage Summary Table:**

| Requirement Key | Has Task? | Task IDs | Notes |
|-----------------|-----------|----------|-------|
| FR-001..FR-006 | Yes | WP01 T001-T008 | |
| FR-007, FR-008, FR-010 | Yes | WP02 T009-T011; WP03-WP07 T014-T038; WP08 T040-T041 | |
| FR-009 | Yes | WP02 T012-T013; WP08 T039 | |
| FR-011, FR-013, FR-018 | Yes | WP09 T044-T049 | |
| FR-012, FR-016 | Yes | WP01 T003, T006 | |
| FR-013 (Python), FR-014, FR-015, FR-017 | Yes | WP10 T050-T056 | |
| FR-019 | Yes | WP01 T007; WP11 T057-T059 | |
| FR-020 | Yes | WP11 T060 | |
| NFR-001, NFR-003, NFR-004 | Yes | WP09 T045, T046, T049 | |
| NFR-002 | Yes | WP02 T010; WP03-WP07 | |
| NFR-005 | Partly | WP03-WP07 | F3 |
| C-001, C-002 | Yes | WP01 | |
| C-003 | Yes | WP10 | |
| C-004 | Yes | WP02-WP07 | |
| C-005..C-007 | No | — | C2, process |

**Charter Alignment Issues:** none. The main pin is the charter's "on demand" path by operator ruling; the gate stays fail-closed; generated pages are regenerated, not hand-edited.

**Unmapped Tasks:** none.

**Metrics:**

- Total Requirements: 32 (20 FR, 5 NFR, 7 C)
- Total Tasks: 61 subtasks in 11 WPs
- Coverage: 29/32 = 91% (the 3 unmapped are process constraints)
- Ambiguity Count: 2 (U2, U3)
- Duplication Count: 0
- Critical Issues Count: 0 (High: 0)

## Next Actions

- No critical or high findings: implementation may proceed. WP02 (tool, ledger 00) does not depend on F3 or U3.
- F3 and U3 must be answered by the operator before WP03 fixes its batch sizes and the merge map's text rule; fold the answers into NFR-005 / WP02 T011, then re-run `/spec-kitty.analyze`.
- C1: dispatch the charter-track `ref` run on the PR branch at close-out.
