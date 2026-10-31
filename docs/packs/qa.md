---
title: qa pack reference
description: "Generated reference for the qa Charter Pack: artifact inventory, per-kind counts, content checksum, and validation status."
doc_status: active
updated: '2026-10-17'
kind: Reference
related:
- packs
- architecture/docsite-design
- packs/catalog-proposal
generated:
  by: scripts/docs/gen_pack_reference.py
  at: '2026-10-17'
---

# qa pack reference

> **Generated page — do not edit by hand.** This file is produced by `scripts/docs/gen_pack_reference.py` from the pack source. Hand edits are overwritten on regeneration, and the CI drift gate fails on any difference.

## Provenance & integrity

- **Pack directory:** `packs/qa`
- **Content checksum (sha256):** `3cd7364fe80d167e45b10ba008f9c636f2144ab69ae4309144b9d10cc4afb94e`
- **Checksum recipe:** sha256 over the sorted `(relative-path + NUL + bytes)` of every file in the pack directory. Re-hash a downloaded pack with the same recipe to verify integrity.

## Purpose

_No `purpose` is declared in this pack's `pack.yaml`, so none is shown here (the generator never fabricates one). See the pack's `README.md` and the [Packs hub](index.md) for authored context._

## Artifact inventory

| Kind | Count |
| --- | --- |
| `directives` | 8 |
| `tactics` | 8 |
| `styleguides` | 1 |
| `toolguides` | 6 |
| `procedures` | 5 |
| `agent_profiles` | 5 |
| `assets` | 6 |
| `glossary_packs` | 1 |
| `drg` | 1 |
| `mission_step_contracts` | 7 |
| `missions` | 20 |
| **Total files** | **71** |

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
<summary><code>toolguides</code> (6)</summary>

- `qa-carrier-lint.guide.md`
- `qa-carrier-lint.toolguide.yaml`
- `qa-promise-trace-lint-guide.guide.md`
- `qa-promise-trace-lint.toolguide.yaml`
- `qa-result-ingest-guide.guide.md`
- `qa-result-ingest.toolguide.yaml`

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

## Validation

Reported by `spec-kitty charter pack validate --json`: **failing (`ok: false`)**.

- Errors: 5

### Errors

- {'artifact_id': 'qa-coverage-gap-analysis', 'artifact_type': 'procedures', 'category': 'schema_invalid', 'file': 'packs/qa/procedures/qa-coverage-gap-analysis.procedure.yaml', 'message': 'schema validation failed: Field required', 'severity': 'error'}
- {'artifact_id': 'qa-defect-triage-ritual', 'artifact_type': 'procedures', 'category': 'schema_invalid', 'file': 'packs/qa/procedures/qa-defect-triage-ritual.procedure.yaml', 'message': 'schema validation failed: Field required', 'severity': 'error'}
- {'artifact_id': 'qa-description-to-acceptance-ci', 'artifact_type': 'procedures', 'category': 'schema_invalid', 'file': 'packs/qa/procedures/qa-description-to-acceptance-ci.procedure.yaml', 'message': 'schema validation failed: Field required', 'severity': 'error'}
- {'artifact_id': 'qa-go-no-go-readiness-review', 'artifact_type': 'procedures', 'category': 'schema_invalid', 'file': 'packs/qa/procedures/qa-go-no-go-readiness-review.procedure.yaml', 'message': 'schema validation failed: Field required', 'severity': 'error'}
- {'artifact_id': 'qa-test-plan-review-workshop', 'artifact_type': 'procedures', 'category': 'schema_invalid', 'file': 'packs/qa/procedures/qa-test-plan-review-workshop.procedure.yaml', 'message': 'schema validation failed: Field required', 'severity': 'error'}

Advisories are non-blocking and vary by validator version; run `spec-kitty charter pack validate <dir> --json` for the current list.
