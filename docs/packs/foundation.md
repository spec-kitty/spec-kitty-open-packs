---
title: foundation pack reference
description: "Generated reference for the foundation Charter Pack: artifact inventory, per-kind counts, content checksum, and validation status."
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

# foundation pack reference

> **Generated page — do not edit by hand.** This file is produced by `scripts/docs/gen_pack_reference.py` from the pack source. Hand edits are overwritten on regeneration, and the CI drift gate fails on any difference.

## Provenance & integrity

- **Pack directory:** `packs/foundation`
- **Declared version:** `1.0.0`
- **Content checksum (sha256):** `69fcfb882c776c0ded9b90e29f0119660f4319bd128c811a2a0f2bf00ca02a9d`
- **Checksum recipe:** sha256 over the sorted `(relative-path + NUL + bytes + LF)` of every file in the pack directory. Re-hash a downloaded pack with the same recipe to verify integrity.

## Purpose

The basis of every Spec Kitty project, and a member of the `built-in` distribution.

- **Agent profiles:** `generic-agent` (Generic Giannis, the fallback), `implementer-ivan`,
  `reviewer-renata`, `analyst-annie`, `human-in-charge`.
- **Mission types:** `software-dev`, `plan`, `research`.
- **Doctrine:** every cross-cutting directive with its how-to procedures, tactics and toolguides.

Build on it from another pack with `depends_on` (`range: ">=1.0,<2"`) and reference its artifacts
as `foundation::<kind>:<id>`. Mission roles no installed profile fills (for example `researcher`
without the `planning-analysis` bundle) go to a profile that lists the role as an alt-role (for
example `comms-cleo` or `synthesizer-sam` in `writing`, for `researcher`), else to Generic Giannis.

## Artifact inventory

| Kind | Count |
| --- | --- |
| `directives` | 32 |
| `tactics` | 58 |
| `styleguides` | 1 |
| `toolguides` | 12 |
| `paradigms` | 1 |
| `procedures` | 40 |
| `agent_profiles` | 6 |
| `glossary_packs` | 1 |
| `missions` | 74 |
| **Total files** | **241** |

### Full listing

<details>
<summary><code>directives</code> (32)</summary>

- `001-architectural-integrity-standard.directive.yaml`
- `003-decision-documentation-requirement.directive.yaml`
- `010-specification-fidelity-requirement.directive.yaml`
- `018-doctrine-versioning-requirement.directive.yaml`
- `024-locality-of-change.directive.yaml`
- `025-boy-scout-rule.directive.yaml`
- `028-search-tool-discipline.directive.yaml`
- `029-agent-commit-signing-policy.directive.yaml`
- `030-test-and-typecheck-quality-gate.directive.yaml`
- `031-context-aware-design.directive.yaml`
- `032-conceptual-alignment.directive.yaml`
- `033-targeted-staging-policy.directive.yaml`
- `034-test-first-development.directive.yaml`
- `035-bulk-edit-occurrence-classification.directive.yaml`
- `036-black-box-integration-testing.directive.yaml`
- `037-living-documentation-sync.directive.yaml`
- `039-lynn-cole-engineering-culture.directive.yaml`
- `040-recurring-bug-structural-intervention.directive.yaml`
- `041-tests-as-scaffold-not-friction.directive.yaml`
- `043-close-defect-class-by-construction.directive.yaml`
- `044-canonical-sources-and-unification.directive.yaml`
- `045-prs-only-and-read-intent.directive.yaml`
- `046-readable-consistent-prs.directive.yaml`
- `048-version-governance.directive.yaml`
- `049-agent-declaration-and-self-introduction.directive.yaml`
- `050-credential-handling-discipline.directive.yaml`
- `051-supply-chain-install-safety.directive.yaml`
- `052-prefer-durable-fixes.directive.yaml`
- `053-choose-op-or-mission-before-starting.directive.yaml`
- `disciplined-refactoring.directive.yaml`
- `reconcile-change-scope-tensions.directive.yaml`
- `red-main-release-discipline.directive.yaml`

</details>

<details>
<summary><code>tactics</code> (58)</summary>

- `adversarial-qa-handoff.tactic.yaml`
- `analysis/bounded-context-identification.tactic.yaml`
- `analysis/dialectic-research.tactic.yaml`
- `analysis/forensic-repository-audit.tactic.yaml`
- `analysis/premortem-risk-identification.tactic.yaml`
- `analysis/requirements-validation-workflow.tactic.yaml`
- `analysis/reverse-speccing.tactic.yaml`
- `analysis/safe-to-fail-experiment.tactic.yaml`
- `analysis/split-brain-authority-detection.tactic.yaml`
- `architectural-gate-non-vacuity.tactic.yaml`
- `architecture/deepening-opportunity-assessment.tactic.yaml`
- `architecture/dependency-hygiene.tactic.yaml`
- `architecture/interface-variation-design.tactic.yaml`
- `architecture/language-driven-design.tactic.yaml`
- `architecture/problem-decomposition.tactic.yaml`
- `autonomous-operation-protocol.tactic.yaml`
- `avoid-gold-plating.tactic.yaml`
- `canonical-source-unification.tactic.yaml`
- `change-apply-smallest-viable-diff.tactic.yaml`
- `clean-linear-commit-history.tactic.yaml`
- `code-review-incremental.tactic.yaml`
- `communication/adr-drafting-workflow.tactic.yaml`
- `communication/decision-marker-capture.tactic.yaml`
- `communication/glossary-curation-interview.tactic.yaml`
- `communication/traceable-decisions.tactic.yaml`
- `communication/usage-examples-sync.tactic.yaml`
- `easy-to-change.tactic.yaml`
- `eisenhower-prioritisation.tactic.yaml`
- `five-paradigm-parallel-debugging.tactic.yaml`
- `focused-function-complexity-check.tactic.yaml`
- `frozen-baseline-shrink-only-ratchet.tactic.yaml`
- `generated-code-stewardship.tactic.yaml`
- `input-validation-fail-fast.tactic.yaml`
- `lane-recovery.tactic.yaml`
- `model-task-routing.tactic.yaml`
- `moscow-scoping-lens.tactic.yaml`
- `occurrence-classification-workflow.tactic.yaml`
- `op-or-mission-selection.tactic.yaml`
- `ownership-map-leeway.tactic.yaml`
- `pr-agent-worktree-isolation.tactic.yaml`
- `review-intent-and-risk-first.tactic.yaml`
- `reviewer-implementer-role-separation.tactic.yaml`
- `secure-design-checklist.tactic.yaml`
- `secure-regex-catastrophic-backtracking.tactic.yaml`
- `security/supply-chain-install-safety.tactic.yaml`
- `stopping-conditions.tactic.yaml`
- `testing/acceptance-criteria-non-vacuity.tactic.yaml`
- `testing/acceptance-test-first.tactic.yaml`
- `testing/black-box-integration-testing.tactic.yaml`
- `testing/delete-the-assertion-not-the-test.tactic.yaml`
- `testing/function-over-form-testing.tactic.yaml`
- `testing/quality-gate-verification.tactic.yaml`
- `testing/tdd-red-green-refactor.tactic.yaml`
- `testing/test-boundaries-by-responsibility.tactic.yaml`
- `testing/test-readability-clarity-check.tactic.yaml`
- `testing/test-scaffolding-as-design-smell.tactic.yaml`
- `testing/testing-select-appropriate-level.tactic.yaml`
- `work-package-completion-validation.tactic.yaml`

</details>

<details>
<summary><code>styleguides</code> (1)</summary>

- `boring-code-review.styleguide.yaml`

</details>

<details>
<summary><code>toolguides</code> (12)</summary>

- `efficient-local-tooling.guide.md`
- `efficient-local-tooling.toolguide.yaml`
- `execution-lanes.guide.md`
- `execution-lanes.toolguide.yaml`
- `git-agent-commit-signing.guide.md`
- `git-agent-commit-signing.toolguide.yaml`
- `git-worktree-pr-workflow.guide.md`
- `git-worktree-pr-workflow.toolguide.yaml`
- `github-tracker.guide.md`
- `github-tracker.toolguide.yaml`
- `powershell-syntax.guide.md`
- `powershell-syntax.toolguide.yaml`

</details>

<details>
<summary><code>paradigms</code> (1)</summary>

- `trunk-based.paradigm.yaml`

</details>

<details>
<summary><code>procedures</code> (40)</summary>

- `adversarial-squad-deployment.procedure.yaml`
- `agent-commit-signing.procedure.yaml`
- `agent-self-declaration.procedure.yaml`
- `black-box-integration-test-design.procedure.yaml`
- `bounded-context-alignment.procedure.yaml`
- `bulk-edit-occurrence-mapping.procedure.yaml`
- `canonical-source-discipline.procedure.yaml`
- `change-scope-tension-resolution.procedure.yaml`
- `component-boundary-definition.procedure.yaml`
- `credential-exposure-prevention.procedure.yaml`
- `decision-record-keeping.procedure.yaml`
- `defect-class-construction-gate.procedure.yaml`
- `disciplined-refactoring-cycle.procedure.yaml`
- `doctrine-version-change.procedure.yaml`
- `durable-fix-investigation.procedure.yaml`
- `example-mapping-workshop.procedure.yaml`
- `failing-test-triage.procedure.yaml`
- `five-paradigm-structural-intervention.procedure.yaml`
- `git-flow.procedure.yaml`
- `keep-change-local.procedure.yaml`
- `land-changes-via-pull-request.procedure.yaml`
- `living-documentation-sync.procedure.yaml`
- `local-tooling-selection.procedure.yaml`
- `observable-contract-test-authoring.procedure.yaml`
- `op-or-mission-lifecycle.procedure.yaml`
- `post-merge-arch-gate-adjudication.procedure.yaml`
- `read-intent-before-high-risk-operation.procedure.yaml`
- `readable-pr-preparation.procedure.yaml`
- `red-first-bug-reproduction.procedure.yaml`
- `red-main-handling.procedure.yaml`
- `small-explicit-code-shaping.procedure.yaml`
- `specification-traceability-check.procedure.yaml`
- `targeted-staging.procedure.yaml`
- `tech-debt-point-cut-triage.procedure.yaml`
- `term-interpretation-alignment.procedure.yaml`
- `test-and-typecheck-gate-run.procedure.yaml`
- `test-first-cycle.procedure.yaml`
- `tidy-first-campsite-clean.procedure.yaml`
- `touched-area-cleanup.procedure.yaml`
- `version-freshness-check.procedure.yaml`

</details>

<details>
<summary><code>agent_profiles</code> (6)</summary>

- `README.md`
- `analyst-annie.agent.yaml`
- `generic-agent.agent.yaml`
- `human-in-charge.agent.yaml`
- `implementer-ivan.agent.yaml`
- `reviewer-renata.agent.yaml`

</details>

<details>
<summary><code>glossary_packs</code> (1)</summary>

- `spec-kitty-core.glossary-pack.yaml`

</details>

<details>
<summary><code>missions</code> (74)</summary>

- `README.md`
- `built_in_step_contracts/implement.step-contract.yaml`
- `built_in_step_contracts/plan-plan.step-contract.yaml`
- `built_in_step_contracts/plan-research.step-contract.yaml`
- `built_in_step_contracts/plan-review.step-contract.yaml`
- `built_in_step_contracts/plan-specify.step-contract.yaml`
- `built_in_step_contracts/plan.step-contract.yaml`
- `built_in_step_contracts/research-gathering.step-contract.yaml`
- `built_in_step_contracts/research-methodology.step-contract.yaml`
- `built_in_step_contracts/research-output.step-contract.yaml`
- `built_in_step_contracts/research-scoping.step-contract.yaml`
- `built_in_step_contracts/research-synthesis.step-contract.yaml`
- `built_in_step_contracts/review.step-contract.yaml`
- `built_in_step_contracts/specify.step-contract.yaml`
- `built_in_step_contracts/tasks.step-contract.yaml`
- `plan/README.md`
- `plan/plan.mission-type.yaml`
- `plan/steps/plan.prompt.md`
- `plan/steps/research.prompt.md`
- `plan/steps/review.prompt.md`
- `plan/steps/specify.prompt.md`
- `plan/templates/.gitkeep`
- `plan/templates/README.md`
- `plan/templates/plan-plan-skeleton.md`
- `plan/templates/plan-spec-skeleton.md`
- `research/README.md`
- `research/research.mission-type.yaml`
- `research/steps/accept.prompt.md`
- `research/steps/gathering.guidelines.md`
- `research/steps/gathering.prompt.md`
- `research/steps/methodology.guidelines.md`
- `research/steps/methodology.prompt.md`
- `research/steps/output.guidelines.md`
- `research/steps/output.prompt.md`
- `research/steps/retrospect.prompt.md`
- `research/steps/scoping.guidelines.md`
- `research/steps/scoping.prompt.md`
- `research/steps/synthesis.guidelines.md`
- `research/steps/synthesis.prompt.md`
- `research/templates/README.md`
- `research/templates/data-model-template.md`
- `research/templates/research-plan-template.md`
- `research/templates/research-spec-template.md`
- `research/templates/research-template.md`
- `research/templates/research/README.md`
- `research/templates/research/evidence-log.csv`
- `research/templates/research/source-register.csv`
- `research/templates/task-prompt-template.md`
- `research/templates/tasks-template.md`
- `software-dev/README.md`
- `software-dev/software-dev.mission-type.yaml`
- `software-dev/steps/accept.prompt.md`
- `software-dev/steps/analyze.prompt.md`
- `software-dev/steps/charter.prompt.md`
- `software-dev/steps/discovery.prompt.md`
- `software-dev/steps/implement.guidelines.md`
- `software-dev/steps/implement.prompt.md`
- `software-dev/steps/plan.guidelines.md`
- `software-dev/steps/plan.prompt.md`
- `software-dev/steps/retrospect.prompt.md`
- `software-dev/steps/review.guidelines.md`
- `software-dev/steps/review.prompt.md`
- `software-dev/steps/specify.guidelines.md`
- `software-dev/steps/specify.prompt.md`
- `software-dev/steps/tasks-finalize.prompt.md`
- `software-dev/steps/tasks-outline.prompt.md`
- `software-dev/steps/tasks-packages.prompt.md`
- `software-dev/steps/tasks.guidelines.md`
- `software-dev/steps/tasks.prompt.md`
- `software-dev/templates/README.md`
- `software-dev/templates/plan-template.md`
- `software-dev/templates/spec-template.md`
- `software-dev/templates/task-prompt-template.md`
- `software-dev/templates/tasks-template.md`

</details>

## Validation

Reported by the charter pack schemas (`scripts/ci/validate_pack_schemas.py`): **passing**.

- Errors: 0
