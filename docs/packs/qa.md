---
title: qa pack reference
description: "Generated reference for the qa Charter Pack: artifact inventory, per-kind counts, content checksum, and validation status."
doc_status: active
updated: '2026-11-09'
kind: Reference
related:
- packs
- architecture/docsite-design
- packs/catalog-proposal
generated:
  by: scripts/docs/gen_pack_reference.py
  at: '2026-11-09'
---

# qa pack reference

> **Generated page — do not edit by hand.** This file is produced by `scripts/docs/gen_pack_reference.py` from the pack source. Hand edits are overwritten on regeneration, and the CI drift gate fails on any difference.

## Provenance & integrity

- **Pack directory:** `packs/qa`
- **Declared version:** `2.0.0`
- **Content checksum (sha256):** `8ce50afd67a14f33ebd9659216ee5caf5d2bfd5e4d784fab8acd72dd85afbda1`
- **Checksum recipe:** sha256 over the sorted `(relative-path + NUL + bytes + LF)` of every file in the pack directory. Re-hash a downloaded pack with the same recipe to verify integrity.

## Purpose

An open Spec Kitty Charter Pack for running quality assurance as governed work, and for keeping
a product's acceptance tests tied to what the product promises.

It does two jobs: a `qa` mission type — the seven canonical steps redefined in QA terms, with
QA agent profiles, step contracts, templates and evidence tools — and the
description-to-acceptance-CI loop from a ratified promise page through a Given/When/Then
scenario to a bound acceptance test and a release gate. The pack names no test runner: a
project runs its own tests, and the pack governs what they must cover and how honestly they
report.

**Depends on:** `01M75HSYR9S9KPA372PHGT0EX3 >=1.0,<2`, `01M75PCTEKGDXQW59TGSFQQ9QT >=2.0,<3`, `01M75PCTC6HS38NX8HJGT26VTP >=2.0,<3`

## Artifact inventory

| Kind | Count |
| --- | --- |
| `directives` | 8 |
| `tactics` | 8 |
| `styleguides` | 1 |
| `toolguides` | 8 |
| `procedures` | 5 |
| `agent_profiles` | 5 |
| `assets` | 6 |
| `glossary_packs` | 1 |
| `drg` | 1 |
| `mission_step_contracts` | 7 |
| `missions` | 20 |
| `presets` | 1 |
| **Total files** | **76** |

### Full listing

<details>
<summary><code>directives</code> (8)</summary>

- `qa-001-traceability-mandatory.directive.yaml`
- `qa-002-defect-report-quality.directive.yaml`
- `qa-003-no-fake-green.directive.yaml`
- `qa-004-exit-criteria-precede-execution.directive.yaml`
- `qa-005-risk-based-prioritization.directive.yaml`
- `qa-006-exploratory-charters-timeboxed.directive.yaml`
- `qa-007-promise-traceability.directive.yaml`
- `qa-008-reproductions-gate-releases.directive.yaml`

</details>

<details>
<summary><code>tactics</code> (8)</summary>

- `qa-boundary-equivalence-partitioning.tactic.yaml`
- `qa-exploratory-charter-writing.tactic.yaml`
- `qa-flaky-test-quarantine.tactic.yaml`
- `qa-pairwise-test-reduction.tactic.yaml`
- `qa-promise-elicitation.tactic.yaml`
- `qa-regression-suite-selection.tactic.yaml`
- `qa-risk-based-test-prioritization.tactic.yaml`
- `qa-test-data-minimization.tactic.yaml`

</details>

<details>
<summary><code>styleguides</code> (1)</summary>

- `qa-promise-page.styleguide.yaml`

</details>

<details>
<summary><code>toolguides</code> (8)</summary>

- `qa-carrier-lint.guide.md`
- `qa-carrier-lint.toolguide.yaml`
- `qa-promise-trace-lint.guide.md`
- `qa-promise-trace-lint.toolguide.yaml`
- `qa-result-ingest.guide.md`
- `qa-result-ingest.toolguide.yaml`
- `sonar.guide.md`
- `sonar.toolguide.yaml`

</details>

<details>
<summary><code>procedures</code> (5)</summary>

- `qa-coverage-gap-analysis.procedure.yaml`
- `qa-defect-triage-ritual.procedure.yaml`
- `qa-description-to-acceptance-ci.procedure.yaml`
- `qa-go-no-go-readiness-review.procedure.yaml`
- `qa-test-plan-review-workshop.procedure.yaml`

</details>

<details>
<summary><code>agent_profiles</code> (5)</summary>

- `qa-defect-triager-dmitri.agent.yaml`
- `qa-reporter-rhea.agent.yaml`
- `qa-strategist-quinn.agent.yaml`
- `qa-test-designer-tessa.agent.yaml`
- `qa-test-executor-elena.agent.yaml`

</details>

<details>
<summary><code>assets</code> (6)</summary>

- `qa_carrier_lint.py`
- `qa_carrier_lint.py.asset.yaml`
- `qa_promise_trace_lint.py`
- `qa_promise_trace_lint.py.asset.yaml`
- `qa_result_ingest.py`
- `qa_result_ingest.py.asset.yaml`

</details>

<details>
<summary><code>glossary_packs</code> (1)</summary>

- `qa-glossary.glossary-pack.yaml`

</details>

<details>
<summary><code>drg</code> (1)</summary>

- `fragment.yaml`

</details>

<details>
<summary><code>mission_step_contracts</code> (7)</summary>

- `qa-accept.step-contract.yaml`
- `qa-discovery.step-contract.yaml`
- `qa-implement.step-contract.yaml`
- `qa-plan.step-contract.yaml`
- `qa-review.step-contract.yaml`
- `qa-specify.step-contract.yaml`
- `qa-tasks.step-contract.yaml`

</details>

<details>
<summary><code>missions</code> (20)</summary>

- `qa/qa.mission-type.yaml`
- `qa/steps/accept.prompt.md`
- `qa/steps/discovery.prompt.md`
- `qa/steps/implement.prompt.md`
- `qa/steps/plan.prompt.md`
- `qa/steps/review.prompt.md`
- `qa/steps/specify.prompt.md`
- `qa/steps/tasks.prompt.md`
- `qa/templates/EVIDENCE.md`
- `qa/templates/README.md`
- `qa/templates/defect-log-template.md`
- `qa/templates/exploratory-charter-template.md`
- `qa/templates/plan-field-declaration.yaml`
- `qa/templates/promise-page-template.md`
- `qa/templates/scenario-template.feature`
- `qa/templates/test-case-template.md`
- `qa/templates/test-plan-template.md`
- `qa/templates/test-report-template.md`
- `qa/templates/test-strategy-template.md`
- `qa/templates/test-suite-template.md`

</details>

<details>
<summary><code>presets</code> (1)</summary>

- `qa.yaml`

</details>

## Validation

Reported by the charter pack schemas (`scripts/ci/validate_pack_schemas.py`): **passing**.

- Errors: 0
