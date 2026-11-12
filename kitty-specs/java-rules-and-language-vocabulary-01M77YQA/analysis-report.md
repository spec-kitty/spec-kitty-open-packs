---
schema_version: 1
artifact_type: spec-kitty.analysis-report
command: /spec-kitty.analyze
mission_slug: java-rules-and-language-vocabulary-01M77YQA
mission_id: 01M77YQA3MKM8TS8RVXQ2B3VG6
generated_at: '2026-11-12T13:25:42.602369+00:00'
analyzer_agent: unknown
input_artifacts:
  spec.md:
    path: kitty-specs/java-rules-and-language-vocabulary-01M77YQA/spec.md
    sha256: c117be47e574be46a2f7bee93ce2f6c50e0cdb6ac9dee3bf94dd8a2b2bef36f4
  plan.md:
    path: kitty-specs/java-rules-and-language-vocabulary-01M77YQA/plan.md
    sha256: 7b2593f866a0620c506f40ea8e05cbc4590ae67720c9d11524771d5af9911a07
  tasks.md:
    path: kitty-specs/java-rules-and-language-vocabulary-01M77YQA/tasks.md
    sha256: 0c059d4e3d5cb97a65a48c6be97cbc80aabb4c585213f91f24694c8f16a0206c
  charter:
    path: .kittify/charter/charter.yaml
    sha256: 1366c23558591793907206832d72cc55cd6e96064d78e3fc1a04c801403216e9
verdict: ready
issue_counts:
  high: 0
  medium: 1
  low: 2
  critical: 0
  info: 0
findings:
- id: C1
  severity: medium
  category: charter
  summary: 'WP02 is assigned doctrine-daphne, not java-jenny: the project charter narrows out java-* profiles for this docs/pack repo.'
- id: U1
  severity: low
  category: underspecification
  summary: 'Issue matrix rows for context-only citations (#17, #194, #198, #211) carry verdict unknown; record not-applicable before approval.'
- id: U2
  severity: low
  category: underspecification
  summary: The guard's runtime-family list is a design choice in plan.md only; the spec states the rule, not the list.
---

## Specification Analysis Report

| ID | Category | Severity | Location(s) | Summary | Recommendation |
|----|----------|----------|-------------|---------|----------------|
| C1 | Charter | MEDIUM | tasks/WP02 | java-jenny is not in the effective profile set (charter narrows java-* out) | Keep doctrine-daphne (doctrine curation) for styleguide authoring; do not widen the charter |
| U1 | Underspecification | LOW | issue-matrix.md | Context-only issue rows have verdict unknown | Record not-applicable for #17, #194, #198, #211; in-mission for #202, #204 |
| U2 | Underspecification | LOW | plan.md design 2 | Family list lives only in plan | Acceptable: the guard is the generated evidence, the guide states the rule (DIRECTIVE_044) |

**Coverage Summary Table:**

| Requirement Key | Has Task? | Task IDs | Notes |
|-----------------|-----------|----------|-------|
| FR-001 retag toolguides | Yes | T001 | |
| FR-002 guard jvm | Yes | T002 | with unit tests |
| FR-003 vocabulary doc | Yes | T003 | |
| FR-004 three rules | Yes | T004 | |
| FR-005 minor bump + changelog | Yes | T005, T006 | |
| FR-006 regenerate page/digest | Yes | T005 | |
| NFR-001 gates | Yes | WP02 done-when | |

**Charter Alignment Issues:** none blocking (C1 handled within charter).

**Unmapped Tasks:** none.

**Metrics:** 7 requirements, 6 tasks, 100% coverage, 0 ambiguities, 0 duplications, 0 critical.

**Next Actions:** proceed to implement WP01, then WP02; fix the issue-matrix verdicts (U1) before approval.
