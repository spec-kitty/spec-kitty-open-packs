---
title: qa pack reference
description: "Generated reference for the qa doctrine pack: artifact inventory, per-kind counts, content checksum, and validation status."
doc_status: active
updated: '2026-10-10'
kind: Reference
related:
- packs
- architecture/docsite-design
- packs/catalog-proposal
generated:
  by: scripts/docs/gen_pack_reference.py
  at: '2026-10-10'
---

# qa pack reference

> **Generated page — do not edit by hand.** This file is produced by `scripts/docs/gen_pack_reference.py` from the pack source. Hand edits are overwritten on regeneration, and the CI drift gate fails on any difference.

## Provenance & integrity

- **Pack directory:** `packs/qa`
- **Content checksum (sha256):** `1835df5cb8517f2949c094f2ec9b35d533e9b6be6adf60f7bf38481d54c63b89`
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
| `mission-steps` | 7 |
| `mission_step_contracts` | 7 |
| `mission_types` | 2 |
| `missions` | 22 |
| **Total files** | **82** |

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

- `QA-CARRIER-LINT.md`
- `QA-PROMISE-TRACE-LINT.md`
- `QA-RESULT-INGEST.md`
- `qa-carrier-lint.toolguide.yaml`
- `qa-promise-trace-lint.toolguide.yaml`
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
<summary><code>mission-steps</code> (7)</summary>

- `qa/accept/step.yaml`
- `qa/discovery/step.yaml`
- `qa/implement/step.yaml`
- `qa/plan/step.yaml`
- `qa/review/step.yaml`
- `qa/specify/step.yaml`
- `qa/tasks/step.yaml`

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
<summary><code>mission_types</code> (2)</summary>

- `qa.yaml`
- `qa/governance-profile.yaml`

</details>

<details>
<summary><code>missions</code> (22)</summary>

- `qa/command-templates/accept.md`
- `qa/command-templates/discovery.md`
- `qa/command-templates/implement.md`
- `qa/command-templates/plan.md`
- `qa/command-templates/review.md`
- `qa/command-templates/specify.md`
- `qa/command-templates/tasks.md`
- `qa/expected-artifacts.yaml`
- `qa/mission-runtime.yaml`
- `qa/mission.yaml`
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

Reported by `spec-kitty charter pack validate --json`: **passing (`ok: true`)**.

- Errors: 0

Advisories are non-blocking and vary by validator version; run `spec-kitty charter pack validate <dir> --json` for the current list.
