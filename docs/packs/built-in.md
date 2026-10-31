---
title: built-in pack reference
description: "Generated reference for the built-in Charter Pack: artifact inventory, per-kind counts, content checksum, and validation status."
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

# built-in pack reference

> **Generated page — do not edit by hand.** This file is produced by `scripts/docs/gen_pack_reference.py` from the pack source. Hand edits are overwritten on regeneration, and the CI drift gate fails on any difference.

## Provenance & integrity

- **Pack directory:** `packs/built-in`
- **Declared version:** `1.0.0`
- **Content checksum (sha256):** `022ff47ea85b714aff266d43ef26bea5cad27778eaab913a053f1e0b76764eb5`
- **Checksum recipe:** sha256 over the sorted `(relative-path + NUL + bytes)` of every file in the pack directory. Re-hash a downloaded pack with the same recipe to verify integrity.

## Purpose

_No `purpose` is declared in this pack's `pack.yaml`, so none is shown here (the generator never fabricates one). See the pack's `README.md` and the [Packs hub](index.md) for authored context._

## Artifact inventory

| Kind | Count |
| --- | --- |
| `directives` | 39 |
| `tactics` | 121 |
| `styleguides` | 26 |
| `toolguides` | 37 |
| `paradigms` | 14 |
| `procedures` | 22 |
| `agent_profiles` | 27 |
| `assets` | 15 |
| `glossary_packs` | 1 |
| `missions` | 113 |
| `presets` | 2 |
| `skills` | 1 |
| `templates` | 2 |
| **Total files** | **437** |

### Full listing

<details>
<summary><code>directives</code> (39)</summary>

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
- `038-structured-prompt-boundary.directive.yaml`
- `039-lynn-cole-engineering-culture.directive.yaml`
- `040-recurring-bug-structural-intervention.directive.yaml`
- `041-tests-as-scaffold-not-friction.directive.yaml`
- `042-common-docs.directive.yaml`
- `043-close-defect-class-by-construction.directive.yaml`
- `044-canonical-sources-and-unification.directive.yaml`
- `045-prs-only-and-read-intent.directive.yaml`
- `046-readable-consistent-prs.directive.yaml`
- `047-audience-oriented-writing.directive.yaml`
- `048-version-governance.directive.yaml`
- `049-agent-declaration-and-self-introduction.directive.yaml`
- `050-credential-handling-discipline.directive.yaml`
- `051-supply-chain-install-safety.directive.yaml`
- `052-prefer-durable-fixes.directive.yaml`
- `053-choose-op-or-mission-before-starting.directive.yaml`
- `action-item-attribution.directive.yaml`
- `disciplined-refactoring.directive.yaml`
- `minutes-stand-alone.directive.yaml`
- `reconcile-change-scope-tensions.directive.yaml`
- `red-main-release-discipline.directive.yaml`
- `use-c4-model-techniques.directive.yaml`
- `use-mutation-testing-to-validate-test-quality.directive.yaml`

</details>

<details>
<summary><code>tactics</code> (121)</summary>

- `adversarial-qa-handoff.tactic.yaml`
- `analysis/ammerse-impact-analysis.tactic.yaml`
- `analysis/analysis-extract-before-interpret.tactic.yaml`
- `analysis/bounded-context-canvas-fill.tactic.yaml`
- `analysis/bounded-context-identification.tactic.yaml`
- `analysis/code-documentation-analysis.tactic.yaml`
- `analysis/connascence-analysis.tactic.yaml`
- `analysis/context-boundary-inference.tactic.yaml`
- `analysis/context-mapping-classification.tactic.yaml`
- `analysis/dialectic-research.tactic.yaml`
- `analysis/entity-value-object-classification.tactic.yaml`
- `analysis/forensic-repository-audit.tactic.yaml`
- `analysis/premortem-risk-identification.tactic.yaml`
- `analysis/requirements-validation-workflow.tactic.yaml`
- `analysis/reverse-speccing.tactic.yaml`
- `analysis/safe-to-fail-experiment.tactic.yaml`
- `analysis/split-brain-authority-detection.tactic.yaml`
- `analysis/strategic-domain-classification.tactic.yaml`
- `analysis/terminology-extraction-mapping.tactic.yaml`
- `architectural-gate-non-vacuity.tactic.yaml`
- `architecture/aggregate-boundary-design.tactic.yaml`
- `architecture/anti-corruption-layer.tactic.yaml`
- `architecture/architecture-diagram-review-checklist.tactic.yaml`
- `architecture/atomic-design-review-checklist.tactic.yaml`
- `architecture/atomic-state-ownership.tactic.yaml`
- `architecture/c4-zoom-in-architecture-documentation.tactic.yaml`
- `architecture/compositional-stream-boundaries.tactic.yaml`
- `architecture/cross-cutting-state-via-store.tactic.yaml`
- `architecture/deepening-opportunity-assessment.tactic.yaml`
- `architecture/dependency-hygiene.tactic.yaml`
- `architecture/development-bdd.tactic.yaml`
- `architecture/domain-event-capture.tactic.yaml`
- `architecture/interface-variation-design.tactic.yaml`
- `architecture/language-driven-design.tactic.yaml`
- `architecture/paula-patterns-architecture-scout-review.tactic.yaml`
- `architecture/problem-decomposition.tactic.yaml`
- `architecture/reference-architectural-patterns.tactic.yaml`
- `autonomous-operation-protocol.tactic.yaml`
- `avoid-gold-plating.tactic.yaml`
- `canonical-source-unification.tactic.yaml`
- `change-apply-smallest-viable-diff.tactic.yaml`
- `clean-linear-commit-history.tactic.yaml`
- `code-patterns/chain-of-responsibility-rule-pipeline.tactic.yaml`
- `code-review-incremental.tactic.yaml`
- `common-docs-find.tactic.yaml`
- `common-docs-scaffold.tactic.yaml`
- `common-docs-write.tactic.yaml`
- `communication/adr-drafting-workflow.tactic.yaml`
- `communication/decision-marker-capture.tactic.yaml`
- `communication/documentation-curation-audit.tactic.yaml`
- `communication/glossary-curation-interview.tactic.yaml`
- `communication/stakeholder-alignment.tactic.yaml`
- `communication/traceable-decisions.tactic.yaml`
- `communication/usage-examples-sync.tactic.yaml`
- `communication/writing-audience-catalog.tactic.yaml`
- `easy-to-change.tactic.yaml`
- `eisenhower-prioritisation.tactic.yaml`
- `five-paradigm-parallel-debugging.tactic.yaml`
- `focused-function-complexity-check.tactic.yaml`
- `frozen-baseline-shrink-only-ratchet.tactic.yaml`
- `generated-code-stewardship.tactic.yaml`
- `input-validation-fail-fast.tactic.yaml`
- `model-task-routing.tactic.yaml`
- `moscow-scoping-lens.tactic.yaml`
- `occurrence-classification-workflow.tactic.yaml`
- `op-or-mission-selection.tactic.yaml`
- `ownership-map-leeway.tactic.yaml`
- `pr-agent-worktree-isolation.tactic.yaml`
- `reasons-canvas-fill.tactic.yaml`
- `reasons-canvas-review.tactic.yaml`
- `refactoring/refactoring-change-function-declaration.tactic.yaml`
- `refactoring/refactoring-combine-functions-into-transform.tactic.yaml`
- `refactoring/refactoring-conditional-to-strategy.tactic.yaml`
- `refactoring/refactoring-consolidate-conditional-expression.tactic.yaml`
- `refactoring/refactoring-encapsulate-record.tactic.yaml`
- `refactoring/refactoring-encapsulate-variable.tactic.yaml`
- `refactoring/refactoring-extract-class-by-responsibility-split.tactic.yaml`
- `refactoring/refactoring-extract-first-order-concept.tactic.yaml`
- `refactoring/refactoring-guard-clauses-before-polymorphism.tactic.yaml`
- `refactoring/refactoring-inline-temp.tactic.yaml`
- `refactoring/refactoring-introduce-null-object.tactic.yaml`
- `refactoring/refactoring-move-field.tactic.yaml`
- `refactoring/refactoring-move-method.tactic.yaml`
- `refactoring/refactoring-replace-magic-number-with-symbolic-constant.tactic.yaml`
- `refactoring/refactoring-replace-temp-with-query.tactic.yaml`
- `refactoring/refactoring-retry-pattern.tactic.yaml`
- `refactoring/refactoring-state-pattern-for-behavior.tactic.yaml`
- `refactoring/refactoring-strangler-fig.tactic.yaml`
- `review-intent-and-risk-first.tactic.yaml`
- `reviewer-implementer-role-separation.tactic.yaml`
- `secure-design-checklist.tactic.yaml`
- `secure-regex-catastrophic-backtracking.tactic.yaml`
- `security/supply-chain-install-safety.tactic.yaml`
- `semantic-compression/semantic-compression-abstraction-extraction.tactic.yaml`
- `semantic-compression/semantic-compression-behavioral-boundary-mapping.tactic.yaml`
- `semantic-compression/semantic-compression-dead-weight-elimination.tactic.yaml`
- `semantic-compression/semantic-compression-equivalence-verification.tactic.yaml`
- `semantic-compression/semantic-compression-redundancy-discovery.tactic.yaml`
- `semantic-compression/semantic-compression-semantic-consolidation.tactic.yaml`
- `stopping-conditions.tactic.yaml`
- `testing/acceptance-criteria-non-vacuity.tactic.yaml`
- `testing/acceptance-test-first.tactic.yaml`
- `testing/atdd-adversarial-acceptance.tactic.yaml`
- `testing/bdd-scenario-formulation.tactic.yaml`
- `testing/black-box-integration-testing.tactic.yaml`
- `testing/delete-the-assertion-not-the-test.tactic.yaml`
- `testing/formalized-constraint-testing.tactic.yaml`
- `testing/function-over-form-testing.tactic.yaml`
- `testing/mutation-testing-workflow.tactic.yaml`
- `testing/no-parallel-duplicate-test-runs.tactic.yaml`
- `testing/quality-gate-verification.tactic.yaml`
- `testing/tdd-red-green-refactor.tactic.yaml`
- `testing/test-boundaries-by-responsibility.tactic.yaml`
- `testing/test-minimisation.tactic.yaml`
- `testing/test-pyramid-progression.tactic.yaml`
- `testing/test-readability-clarity-check.tactic.yaml`
- `testing/test-scaffolding-as-design-smell.tactic.yaml`
- `testing/test-to-system-reconstruction.tactic.yaml`
- `testing/testing-select-appropriate-level.tactic.yaml`
- `testing/zombies-tdd.tactic.yaml`
- `work-package-completion-validation.tactic.yaml`

</details>

<details>
<summary><code>styleguides</code> (26)</summary>

- `aggregate-design-rules.styleguide.yaml`
- `boring-code-review.styleguide.yaml`
- `common-docs.styleguide.yaml`
- `deployable-skill-authoring.styleguide.yaml`
- `divio-type-discipline.styleguide.yaml`
- `docs-accessibility.styleguide.yaml`
- `docs-freshness-sla.styleguide.yaml`
- `drupal-conventions.styleguide.yaml`
- `drupal-security-performance.styleguide.yaml`
- `given-when-then-authoring.styleguide.yaml`
- `java-conventions.styleguide.yaml`
- `meeting-minutes-format.styleguide.yaml`
- `mutation-aware-test-design.styleguide.yaml`
- `plain-language.styleguide.yaml`
- `planning-and-tracking.styleguide.yaml`
- `professional-communications.styleguide.yaml`
- `publication-authority.styleguide.yaml`
- `python-conventions.styleguide.yaml`
- `quadruple-a-test-format.styleguide.yaml`
- `reasons-canvas-writing.styleguide.yaml`
- `research-citation-discipline.styleguide.yaml`
- `test-desiderata-and-boundaries.styleguide.yaml`
- `testing-principles.styleguide.yaml`
- `tiered-standards.styleguide.yaml`
- `writing/README.md`
- `writing/kitty-glossary-writing.styleguide.yaml`

</details>

<details>
<summary><code>toolguides</code> (37)</summary>

- `contextive.guide.md`
- `contextive.toolguide.yaml`
- `drupal-review-checks.guide.md`
- `drupal-review-checks.toolguide.yaml`
- `efficient-local-tooling.guide.md`
- `efficient-local-tooling.toolguide.yaml`
- `gherkin.guide.md`
- `gherkin.toolguide.yaml`
- `git-agent-commit-signing.guide.md`
- `git-agent-commit-signing.toolguide.yaml`
- `git-worktree-pr-workflow.guide.md`
- `git-worktree-pr-workflow.toolguide.yaml`
- `github-tracker.guide.md`
- `github-tracker.toolguide.yaml`
- `java-supply-chain.guide.md`
- `java-supply-chain.toolguide.yaml`
- `javascript-supply-chain.guide.md`
- `javascript-supply-chain.toolguide.yaml`
- `maven-review-checks.guide.md`
- `maven-review-checks.toolguide.yaml`
- `mermaid-diagramming.guide.md`
- `mermaid-diagramming.toolguide.yaml`
- `plantuml-diagramming.guide.md`
- `plantuml-diagramming.toolguide.yaml`
- `powershell-syntax.guide.md`
- `powershell-syntax.toolguide.yaml`
- `python-mutation-tools.guide.md`
- `python-mutation-tools.toolguide.yaml`
- `python-review-checks.guide.md`
- `python-review-checks.toolguide.yaml`
- `python-supply-chain.guide.md`
- `python-supply-chain.toolguide.yaml`
- `sonar.guide.md`
- `sonar.toolguide.yaml`
- `system_tools/__init__.py`
- `typescript-mutation-tools.guide.md`
- `typescript-mutation-tools.toolguide.yaml`

</details>

<details>
<summary><code>paradigms</code> (14)</summary>

- `atomic-design.paradigm.yaml`
- `behaviour-driven-development.paradigm.yaml`
- `brownfield-onboarding.paradigm.yaml`
- `c4-incremental-detail-modeling.paradigm.yaml`
- `deep-module-design.paradigm.yaml`
- `domain-driven-design.paradigm.yaml`
- `execution-lanes.paradigm.yaml`
- `extract-then-publish-separation.paradigm.yaml`
- `git-flow.paradigm.yaml`
- `semantic-compression.paradigm.yaml`
- `shared-branch-ci.paradigm.yaml`
- `specification-by-example.paradigm.yaml`
- `structured-prompt-driven-development.paradigm.yaml`
- `trunk-based.paradigm.yaml`

</details>

<details>
<summary><code>procedures</code> (22)</summary>

- `adversarial-squad-deployment.procedure.yaml`
- `bdd-scenario-lifecycle.procedure.yaml`
- `development-assist-test-cleanup.procedure.yaml`
- `disciplined-defect-diagnosis.procedure.yaml`
- `documentation-gap-prioritization.procedure.yaml`
- `domain-aware-decision-interview.procedure.yaml`
- `drill-down-documentation.procedure.yaml`
- `event-storming-discovery.procedure.yaml`
- `example-mapping-workshop.procedure.yaml`
- `glossary-maintenance-workflow.procedure.yaml`
- `issue-triage-state-machine.procedure.yaml`
- `legacy-codebase-triage.procedure.yaml`
- `meeting-minutes-pipeline.procedure.yaml`
- `migrate-project-guidance-to-spec-kitty-charter.procedure.yaml`
- `mission-tracer-files.procedure.yaml`
- `mission-wrap-up-sequence.procedure.yaml`
- `onboard-external-agent-to-pack.procedure.yaml`
- `post-merge-arch-gate-adjudication.procedure.yaml`
- `refactoring.procedure.yaml`
- `situational-assessment.procedure.yaml`
- `spike-timebox-policy.procedure.yaml`
- `test-first-bug-fixing.procedure.yaml`

</details>

<details>
<summary><code>agent_profiles</code> (27)</summary>

- `README.md`
- `analyst-annie.agent.yaml`
- `architect-alphonso.agent.yaml`
- `comms-cleo.agent.yaml`
- `curator-carla.agent.yaml`
- `debugger-debbie.agent.yaml`
- `designer-dagmar.agent.yaml`
- `diagram-daisy.agent.yaml`
- `doctrine-daphne.agent.yaml`
- `drupal-dries.agent.yaml`
- `frontend-freddy.agent.yaml`
- `generic-agent.agent.yaml`
- `human-in-charge.agent.yaml`
- `implementer-ivan.agent.yaml`
- `java-jenny.agent.yaml`
- `lexical-larry.agent.yaml`
- `minutes-mahad.agent.yaml`
- `node-norris.agent.yaml`
- `paula-patterns.agent.yaml`
- `planner-priti.agent.yaml`
- `python-pedro.agent.yaml`
- `randy-reducer.agent.yaml`
- `researcher-robbie.agent.yaml`
- `retrospective-facilitator.agent.yaml`
- `reviewer-renata.agent.yaml`
- `scribe-sally.agent.yaml`
- `synthesizer-sam.agent.yaml`

</details>

<details>
<summary><code>assets</code> (15)</summary>

- `README.md`
- `audiences/README.md`
- `audiences/agentic-framework-core-team.md`
- `audiences/agentic-framework-core-team.md.asset.yaml`
- `audiences/automation_agent.md`
- `audiences/automation_agent.md.asset.yaml`
- `audiences/line_manager.md`
- `audiences/line_manager.md.asset.yaml`
- `audiences/nontech_educator.md`
- `audiences/nontech_educator.md.asset.yaml`
- `audiences/software_engineer.md`
- `audiences/software_engineer.md.asset.yaml`
- `docs_structural_lint.config.yaml`
- `docs_structural_lint.py`
- `docs_structural_lint.py.asset.yaml`

</details>

<details>
<summary><code>glossary_packs</code> (1)</summary>

- `spec-kitty-core.glossary-pack.yaml`

</details>

<details>
<summary><code>missions</code> (113)</summary>

- `README.md`
- `built_in_step_contracts/__init__.py`
- `built_in_step_contracts/documentation-accept.step-contract.yaml`
- `built_in_step_contracts/documentation-audit.step-contract.yaml`
- `built_in_step_contracts/documentation-design.step-contract.yaml`
- `built_in_step_contracts/documentation-discover.step-contract.yaml`
- `built_in_step_contracts/documentation-generate.step-contract.yaml`
- `built_in_step_contracts/documentation-publish.step-contract.yaml`
- `built_in_step_contracts/documentation-validate.step-contract.yaml`
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
- `documentation/README.md`
- `documentation/documentation.mission-type.yaml`
- `documentation/steps/accept.guidelines.md`
- `documentation/steps/accept.prompt.md`
- `documentation/steps/audit.guidelines.md`
- `documentation/steps/audit.prompt.md`
- `documentation/steps/design.guidelines.md`
- `documentation/steps/design.prompt.md`
- `documentation/steps/discover.guidelines.md`
- `documentation/steps/discover.prompt.md`
- `documentation/steps/generate.guidelines.md`
- `documentation/steps/generate.prompt.md`
- `documentation/steps/publish.guidelines.md`
- `documentation/steps/publish.prompt.md`
- `documentation/steps/retrospect.prompt.md`
- `documentation/steps/validate.guidelines.md`
- `documentation/steps/validate.prompt.md`
- `documentation/templates/README.md`
- `documentation/templates/divio/README.md`
- `documentation/templates/divio/explanation-template.md`
- `documentation/templates/divio/howto-template.md`
- `documentation/templates/divio/reference-template.md`
- `documentation/templates/divio/tutorial-template.md`
- `documentation/templates/documentation-plan-template.md`
- `documentation/templates/documentation-spec-template.md`
- `documentation/templates/generators/README.md`
- `documentation/templates/generators/jsdoc.json.template`
- `documentation/templates/generators/sphinx-conf.py.template`
- `documentation/templates/release-template.md`
- `documentation/templates/task-prompt-template.md`
- `documentation/templates/tasks-template.md`
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

<details>
<summary><code>presets</code> (2)</summary>

- `default.yaml`
- `minimal.yaml`

</details>

<details>
<summary><code>skills</code> (1)</summary>

- `.gitkeep`

</details>

<details>
<summary><code>templates</code> (2)</summary>

- `writing/meeting-discussion-notes.md`
- `writing/meeting-minutes.md`

</details>

## Validation

Reported by the charter pack schemas (`scripts/ci/validate_pack_schemas.py`): **passing**.

- Errors: 0
