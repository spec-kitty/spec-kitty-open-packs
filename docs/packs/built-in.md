---
title: built-in pack reference
description: "Generated reference for the built-in doctrine pack: artifact inventory, per-kind counts, content checksum, and validation status."
doc_status: active
updated: '2026-10-14'
kind: Reference
related:
- packs
- architecture/docsite-design
- packs/catalog-proposal
generated:
  by: scripts/docs/gen_pack_reference.py
  at: '2026-10-14'
---

# built-in pack reference

> **Generated page — do not edit by hand.** This file is produced by `scripts/docs/gen_pack_reference.py` from the pack source. Hand edits are overwritten on regeneration, and the CI drift gate fails on any difference.

## Provenance & integrity

- **Pack directory:** `built-in`
- **Declared version:** `1.0.0`
- **Content checksum (sha256):** `9d87a5f61846f58f7c606147a1aefef40ce13667ea6f9c3900addc7aea1deec9`
- **Checksum recipe:** sha256 over the sorted `(relative-path + NUL + bytes)` of every file in the pack directory. Re-hash a downloaded pack with the same recipe to verify integrity.

## Purpose

_No `purpose` is declared in this pack's `pack.yaml`, so none is shown here (the generator never fabricates one). See the pack's `README.md` and the [Packs hub](index.md) for authored context._

## Artifact inventory

| Kind | Count |
| --- | --- |
| `directives` | 38 |
| `tactics` | 121 |
| `styleguides` | 26 |
| `toolguides` | 37 |
| `paradigms` | 14 |
| `procedures` | 23 |
| `agent_profiles` | 27 |
| `assets` | 15 |
| `glossary_packs` | 1 |
| `missions` | 177 |
| `presets` | 2 |
| `skills` | 1 |
| `templates` | 2 |
| **Total files** | **501** |

### Full listing

<details>
<summary><code>directives</code> (38)</summary>

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

- `CONTEXTIVE.md`
- `DRUPAL_REVIEW_CHECKS.md`
- `EFFICIENT_LOCAL_TOOLING.md`
- `GHERKIN.md`
- `GITHUB_TRACKER.md`
- `GIT_AGENT_COMMIT_SIGNING.md`
- `GIT_WORKTREE_PR_WORKFLOW.md`
- `JAVASCRIPT_SUPPLY_CHAIN.md`
- `JAVA_SUPPLY_CHAIN.md`
- `MAVEN_REVIEW_CHECKS.md`
- `MERMAID_DIAGRAMMING.md`
- `PLANTUML_DIAGRAMMING.md`
- `POWERSHELL_SYNTAX.md`
- `PYTHON_MUTATION_TOOLS.md`
- `PYTHON_REVIEW_CHECKS.md`
- `PYTHON_SUPPLY_CHAIN.md`
- `SONAR.md`
- `TYPESCRIPT_MUTATION_TOOLS.md`
- `contextive.toolguide.yaml`
- `drupal-review-checks.toolguide.yaml`
- `efficient-local-tooling.toolguide.yaml`
- `gherkin.toolguide.yaml`
- `git-agent-commit-signing.toolguide.yaml`
- `git-worktree-pr-workflow.toolguide.yaml`
- `github-tracker.toolguide.yaml`
- `java-supply-chain.toolguide.yaml`
- `javascript-supply-chain.toolguide.yaml`
- `maven-review-checks.toolguide.yaml`
- `mermaid-diagramming.toolguide.yaml`
- `plantuml-diagramming.toolguide.yaml`
- `powershell-syntax.toolguide.yaml`
- `python-mutation-tools.toolguide.yaml`
- `python-review-checks.toolguide.yaml`
- `python-supply-chain.toolguide.yaml`
- `sonar.toolguide.yaml`
- `system_tools/__init__.py`
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
<summary><code>procedures</code> (23)</summary>

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
- `red-main-release-discipline.procedure.yaml`
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
<summary><code>missions</code> (177)</summary>

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
- `documentation/actions/accept/index.yaml`
- `documentation/actions/audit/index.yaml`
- `documentation/actions/design/index.yaml`
- `documentation/actions/discover/index.yaml`
- `documentation/actions/generate/index.yaml`
- `documentation/actions/publish/index.yaml`
- `documentation/actions/retrospect/index.yaml`
- `documentation/actions/validate/index.yaml`
- `documentation/expected-artifacts.yaml`
- `documentation/governance-profile.yaml`
- `documentation/mission-runtime.yaml`
- `documentation/mission.yaml`
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
- `mission-steps/documentation/accept/guidelines.md`
- `mission-steps/documentation/accept/prompt.md`
- `mission-steps/documentation/accept/step.yaml`
- `mission-steps/documentation/audit/guidelines.md`
- `mission-steps/documentation/audit/prompt.md`
- `mission-steps/documentation/audit/step.yaml`
- `mission-steps/documentation/design/guidelines.md`
- `mission-steps/documentation/design/prompt.md`
- `mission-steps/documentation/design/step.yaml`
- `mission-steps/documentation/discover/guidelines.md`
- `mission-steps/documentation/discover/prompt.md`
- `mission-steps/documentation/discover/step.yaml`
- `mission-steps/documentation/generate/guidelines.md`
- `mission-steps/documentation/generate/prompt.md`
- `mission-steps/documentation/generate/step.yaml`
- `mission-steps/documentation/publish/guidelines.md`
- `mission-steps/documentation/publish/prompt.md`
- `mission-steps/documentation/publish/step.yaml`
- `mission-steps/documentation/retrospect/prompt.md`
- `mission-steps/documentation/retrospect/step.yaml`
- `mission-steps/documentation/validate/guidelines.md`
- `mission-steps/documentation/validate/prompt.md`
- `mission-steps/documentation/validate/step.yaml`
- `mission-steps/plan/plan/prompt.md`
- `mission-steps/plan/plan/step.yaml`
- `mission-steps/plan/research/prompt.md`
- `mission-steps/plan/research/step.yaml`
- `mission-steps/plan/review/prompt.md`
- `mission-steps/plan/review/step.yaml`
- `mission-steps/plan/specify/prompt.md`
- `mission-steps/plan/specify/step.yaml`
- `mission-steps/research/gathering/guidelines.md`
- `mission-steps/research/gathering/prompt.md`
- `mission-steps/research/gathering/step.yaml`
- `mission-steps/research/methodology/guidelines.md`
- `mission-steps/research/methodology/prompt.md`
- `mission-steps/research/methodology/step.yaml`
- `mission-steps/research/output/guidelines.md`
- `mission-steps/research/output/prompt.md`
- `mission-steps/research/output/step.yaml`
- `mission-steps/research/retrospect/prompt.md`
- `mission-steps/research/retrospect/step.yaml`
- `mission-steps/research/scoping/guidelines.md`
- `mission-steps/research/scoping/prompt.md`
- `mission-steps/research/scoping/step.yaml`
- `mission-steps/research/synthesis/guidelines.md`
- `mission-steps/research/synthesis/prompt.md`
- `mission-steps/research/synthesis/step.yaml`
- `mission-steps/software-dev/accept/prompt.md`
- `mission-steps/software-dev/accept/step.yaml`
- `mission-steps/software-dev/analyze/prompt.md`
- `mission-steps/software-dev/analyze/step.yaml`
- `mission-steps/software-dev/charter/prompt.md`
- `mission-steps/software-dev/charter/step.yaml`
- `mission-steps/software-dev/implement/guidelines.md`
- `mission-steps/software-dev/implement/prompt.md`
- `mission-steps/software-dev/implement/step.yaml`
- `mission-steps/software-dev/plan/guidelines.md`
- `mission-steps/software-dev/plan/prompt.md`
- `mission-steps/software-dev/plan/step.yaml`
- `mission-steps/software-dev/research/prompt.md`
- `mission-steps/software-dev/research/step.yaml`
- `mission-steps/software-dev/review/guidelines.md`
- `mission-steps/software-dev/review/prompt.md`
- `mission-steps/software-dev/review/step.yaml`
- `mission-steps/software-dev/specify/guidelines.md`
- `mission-steps/software-dev/specify/prompt.md`
- `mission-steps/software-dev/specify/step.yaml`
- `mission-steps/software-dev/tasks-finalize/prompt.md`
- `mission-steps/software-dev/tasks-finalize/step.yaml`
- `mission-steps/software-dev/tasks-outline/prompt.md`
- `mission-steps/software-dev/tasks-outline/step.yaml`
- `mission-steps/software-dev/tasks-packages/prompt.md`
- `mission-steps/software-dev/tasks-packages/step.yaml`
- `mission-steps/software-dev/tasks/guidelines.md`
- `mission-steps/software-dev/tasks/prompt.md`
- `mission-steps/software-dev/tasks/step.yaml`
- `mission_types/documentation.yaml`
- `mission_types/plan.yaml`
- `mission_types/research.yaml`
- `mission_types/software-dev.yaml`
- `plan/README.md`
- `plan/actions/plan/index.yaml`
- `plan/actions/research/index.yaml`
- `plan/actions/review/index.yaml`
- `plan/actions/specify/index.yaml`
- `plan/expected-artifacts.yaml`
- `plan/governance-profile.yaml`
- `plan/mission-runtime.yaml`
- `plan/mission.yaml`
- `plan/templates/.gitkeep`
- `plan/templates/README.md`
- `plan/templates/plan-plan-skeleton.md`
- `plan/templates/plan-spec-skeleton.md`
- `research/README.md`
- `research/actions/gathering/index.yaml`
- `research/actions/methodology/index.yaml`
- `research/actions/output/index.yaml`
- `research/actions/retrospect/index.yaml`
- `research/actions/scoping/index.yaml`
- `research/actions/synthesis/index.yaml`
- `research/expected-artifacts.yaml`
- `research/governance-profile.yaml`
- `research/mission-runtime.yaml`
- `research/mission.yaml`
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
- `software-dev/actions/implement/index.yaml`
- `software-dev/actions/plan/index.yaml`
- `software-dev/actions/retrospect/index.yaml`
- `software-dev/actions/review/index.yaml`
- `software-dev/actions/specify/index.yaml`
- `software-dev/actions/tasks/index.yaml`
- `software-dev/expected-artifacts.yaml`
- `software-dev/governance-profile.yaml`
- `software-dev/mission-runtime.yaml`
- `software-dev/mission.yaml`
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

Reported by `spec-kitty charter pack validate --json`: **passing (`ok: true`)**.

- Errors: 0
- Advisories: 157

### Advisories

- {'artifact_id': 'ACTION_ITEM_ATTRIBUTION', 'artifact_type': 'directives', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/directives/action-item-attribution.directive.yaml', 'message': "artifact id 'ACTION_ITEM_ATTRIBUTION' will field-merge into the built-in directive — declare 'enhances: ACTION_ITEM_ATTRIBUTION' to suppress this advisory, or 'overrides: ACTION_ITEM_ATTRIBUTION' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'DIRECTIVE_001', 'artifact_type': 'directives', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/directives/001-architectural-integrity-standard.directive.yaml', 'message': "artifact id 'DIRECTIVE_001' will field-merge into the built-in directive — declare 'enhances: DIRECTIVE_001' to suppress this advisory, or 'overrides: DIRECTIVE_001' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'DIRECTIVE_003', 'artifact_type': 'directives', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/directives/003-decision-documentation-requirement.directive.yaml', 'message': "artifact id 'DIRECTIVE_003' will field-merge into the built-in directive — declare 'enhances: DIRECTIVE_003' to suppress this advisory, or 'overrides: DIRECTIVE_003' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'DIRECTIVE_010', 'artifact_type': 'directives', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/directives/010-specification-fidelity-requirement.directive.yaml', 'message': "artifact id 'DIRECTIVE_010' will field-merge into the built-in directive — declare 'enhances: DIRECTIVE_010' to suppress this advisory, or 'overrides: DIRECTIVE_010' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'DIRECTIVE_018', 'artifact_type': 'directives', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/directives/018-doctrine-versioning-requirement.directive.yaml', 'message': "artifact id 'DIRECTIVE_018' will field-merge into the built-in directive — declare 'enhances: DIRECTIVE_018' to suppress this advisory, or 'overrides: DIRECTIVE_018' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'DIRECTIVE_024', 'artifact_type': 'directives', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/directives/024-locality-of-change.directive.yaml', 'message': "artifact id 'DIRECTIVE_024' will field-merge into the built-in directive — declare 'enhances: DIRECTIVE_024' to suppress this advisory, or 'overrides: DIRECTIVE_024' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'DIRECTIVE_025', 'artifact_type': 'directives', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/directives/025-boy-scout-rule.directive.yaml', 'message': "artifact id 'DIRECTIVE_025' will field-merge into the built-in directive — declare 'enhances: DIRECTIVE_025' to suppress this advisory, or 'overrides: DIRECTIVE_025' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'DIRECTIVE_028', 'artifact_type': 'directives', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/directives/028-search-tool-discipline.directive.yaml', 'message': "artifact id 'DIRECTIVE_028' will field-merge into the built-in directive — declare 'enhances: DIRECTIVE_028' to suppress this advisory, or 'overrides: DIRECTIVE_028' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'DIRECTIVE_029', 'artifact_type': 'directives', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/directives/029-agent-commit-signing-policy.directive.yaml', 'message': "artifact id 'DIRECTIVE_029' will field-merge into the built-in directive — declare 'enhances: DIRECTIVE_029' to suppress this advisory, or 'overrides: DIRECTIVE_029' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'DIRECTIVE_030', 'artifact_type': 'directives', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/directives/030-test-and-typecheck-quality-gate.directive.yaml', 'message': "artifact id 'DIRECTIVE_030' will field-merge into the built-in directive — declare 'enhances: DIRECTIVE_030' to suppress this advisory, or 'overrides: DIRECTIVE_030' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'DIRECTIVE_031', 'artifact_type': 'directives', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/directives/031-context-aware-design.directive.yaml', 'message': "artifact id 'DIRECTIVE_031' will field-merge into the built-in directive — declare 'enhances: DIRECTIVE_031' to suppress this advisory, or 'overrides: DIRECTIVE_031' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'DIRECTIVE_032', 'artifact_type': 'directives', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/directives/032-conceptual-alignment.directive.yaml', 'message': "artifact id 'DIRECTIVE_032' will field-merge into the built-in directive — declare 'enhances: DIRECTIVE_032' to suppress this advisory, or 'overrides: DIRECTIVE_032' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'DIRECTIVE_033', 'artifact_type': 'directives', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/directives/033-targeted-staging-policy.directive.yaml', 'message': "artifact id 'DIRECTIVE_033' will field-merge into the built-in directive — declare 'enhances: DIRECTIVE_033' to suppress this advisory, or 'overrides: DIRECTIVE_033' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'DIRECTIVE_034', 'artifact_type': 'directives', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/directives/034-test-first-development.directive.yaml', 'message': "artifact id 'DIRECTIVE_034' will field-merge into the built-in directive — declare 'enhances: DIRECTIVE_034' to suppress this advisory, or 'overrides: DIRECTIVE_034' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'DIRECTIVE_035', 'artifact_type': 'directives', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/directives/035-bulk-edit-occurrence-classification.directive.yaml', 'message': "artifact id 'DIRECTIVE_035' will field-merge into the built-in directive — declare 'enhances: DIRECTIVE_035' to suppress this advisory, or 'overrides: DIRECTIVE_035' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'DIRECTIVE_036', 'artifact_type': 'directives', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/directives/036-black-box-integration-testing.directive.yaml', 'message': "artifact id 'DIRECTIVE_036' will field-merge into the built-in directive — declare 'enhances: DIRECTIVE_036' to suppress this advisory, or 'overrides: DIRECTIVE_036' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'DIRECTIVE_037', 'artifact_type': 'directives', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/directives/037-living-documentation-sync.directive.yaml', 'message': "artifact id 'DIRECTIVE_037' will field-merge into the built-in directive — declare 'enhances: DIRECTIVE_037' to suppress this advisory, or 'overrides: DIRECTIVE_037' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'DIRECTIVE_038', 'artifact_type': 'directives', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/directives/038-structured-prompt-boundary.directive.yaml', 'message': "artifact id 'DIRECTIVE_038' will field-merge into the built-in directive — declare 'enhances: DIRECTIVE_038' to suppress this advisory, or 'overrides: DIRECTIVE_038' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'DIRECTIVE_039', 'artifact_type': 'directives', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/directives/039-lynn-cole-engineering-culture.directive.yaml', 'message': "artifact id 'DIRECTIVE_039' will field-merge into the built-in directive — declare 'enhances: DIRECTIVE_039' to suppress this advisory, or 'overrides: DIRECTIVE_039' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'DIRECTIVE_040', 'artifact_type': 'directives', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/directives/040-recurring-bug-structural-intervention.directive.yaml', 'message': "artifact id 'DIRECTIVE_040' will field-merge into the built-in directive — declare 'enhances: DIRECTIVE_040' to suppress this advisory, or 'overrides: DIRECTIVE_040' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'DIRECTIVE_041', 'artifact_type': 'directives', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/directives/041-tests-as-scaffold-not-friction.directive.yaml', 'message': "artifact id 'DIRECTIVE_041' will field-merge into the built-in directive — declare 'enhances: DIRECTIVE_041' to suppress this advisory, or 'overrides: DIRECTIVE_041' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'DIRECTIVE_042', 'artifact_type': 'directives', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/directives/042-common-docs.directive.yaml', 'message': "artifact id 'DIRECTIVE_042' will field-merge into the built-in directive — declare 'enhances: DIRECTIVE_042' to suppress this advisory, or 'overrides: DIRECTIVE_042' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'DIRECTIVE_043', 'artifact_type': 'directives', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/directives/043-close-defect-class-by-construction.directive.yaml', 'message': "artifact id 'DIRECTIVE_043' will field-merge into the built-in directive — declare 'enhances: DIRECTIVE_043' to suppress this advisory, or 'overrides: DIRECTIVE_043' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'DIRECTIVE_044', 'artifact_type': 'directives', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/directives/044-canonical-sources-and-unification.directive.yaml', 'message': "artifact id 'DIRECTIVE_044' will field-merge into the built-in directive — declare 'enhances: DIRECTIVE_044' to suppress this advisory, or 'overrides: DIRECTIVE_044' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'DIRECTIVE_045', 'artifact_type': 'directives', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/directives/045-prs-only-and-read-intent.directive.yaml', 'message': "artifact id 'DIRECTIVE_045' will field-merge into the built-in directive — declare 'enhances: DIRECTIVE_045' to suppress this advisory, or 'overrides: DIRECTIVE_045' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'DIRECTIVE_046', 'artifact_type': 'directives', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/directives/046-readable-consistent-prs.directive.yaml', 'message': "artifact id 'DIRECTIVE_046' will field-merge into the built-in directive — declare 'enhances: DIRECTIVE_046' to suppress this advisory, or 'overrides: DIRECTIVE_046' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'DIRECTIVE_047', 'artifact_type': 'directives', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/directives/047-audience-oriented-writing.directive.yaml', 'message': "artifact id 'DIRECTIVE_047' will field-merge into the built-in directive — declare 'enhances: DIRECTIVE_047' to suppress this advisory, or 'overrides: DIRECTIVE_047' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'DIRECTIVE_048', 'artifact_type': 'directives', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/directives/048-version-governance.directive.yaml', 'message': "artifact id 'DIRECTIVE_048' will field-merge into the built-in directive — declare 'enhances: DIRECTIVE_048' to suppress this advisory, or 'overrides: DIRECTIVE_048' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'DIRECTIVE_049', 'artifact_type': 'directives', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/directives/049-agent-declaration-and-self-introduction.directive.yaml', 'message': "artifact id 'DIRECTIVE_049' will field-merge into the built-in directive — declare 'enhances: DIRECTIVE_049' to suppress this advisory, or 'overrides: DIRECTIVE_049' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'DIRECTIVE_050', 'artifact_type': 'directives', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/directives/050-credential-handling-discipline.directive.yaml', 'message': "artifact id 'DIRECTIVE_050' will field-merge into the built-in directive — declare 'enhances: DIRECTIVE_050' to suppress this advisory, or 'overrides: DIRECTIVE_050' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'DIRECTIVE_051', 'artifact_type': 'directives', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/directives/051-supply-chain-install-safety.directive.yaml', 'message': "artifact id 'DIRECTIVE_051' will field-merge into the built-in directive — declare 'enhances: DIRECTIVE_051' to suppress this advisory, or 'overrides: DIRECTIVE_051' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'DIRECTIVE_052', 'artifact_type': 'directives', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/directives/052-prefer-durable-fixes.directive.yaml', 'message': "artifact id 'DIRECTIVE_052' will field-merge into the built-in directive — declare 'enhances: DIRECTIVE_052' to suppress this advisory, or 'overrides: DIRECTIVE_052' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'DIRECTIVE_053', 'artifact_type': 'directives', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/directives/053-choose-op-or-mission-before-starting.directive.yaml', 'message': "artifact id 'DIRECTIVE_053' will field-merge into the built-in directive — declare 'enhances: DIRECTIVE_053' to suppress this advisory, or 'overrides: DIRECTIVE_053' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'DISCIPLINED_REFACTORING', 'artifact_type': 'directives', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/directives/disciplined-refactoring.directive.yaml', 'message': "artifact id 'DISCIPLINED_REFACTORING' will field-merge into the built-in directive — declare 'enhances: DISCIPLINED_REFACTORING' to suppress this advisory, or 'overrides: DISCIPLINED_REFACTORING' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'MINUTES_STAND_ALONE', 'artifact_type': 'directives', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/directives/minutes-stand-alone.directive.yaml', 'message': "artifact id 'MINUTES_STAND_ALONE' will field-merge into the built-in directive — declare 'enhances: MINUTES_STAND_ALONE' to suppress this advisory, or 'overrides: MINUTES_STAND_ALONE' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'RECONCILE_CHANGE_SCOPE_TENSIONS', 'artifact_type': 'directives', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/directives/reconcile-change-scope-tensions.directive.yaml', 'message': "artifact id 'RECONCILE_CHANGE_SCOPE_TENSIONS' will field-merge into the built-in directive — declare 'enhances: RECONCILE_CHANGE_SCOPE_TENSIONS' to suppress this advisory, or 'overrides: RECONCILE_CHANGE_SCOPE_TENSIONS' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'USE_C4_MODEL_TECHNIQUES', 'artifact_type': 'directives', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/directives/use-c4-model-techniques.directive.yaml', 'message': "artifact id 'USE_C4_MODEL_TECHNIQUES' will field-merge into the built-in directive — declare 'enhances: USE_C4_MODEL_TECHNIQUES' to suppress this advisory, or 'overrides: USE_C4_MODEL_TECHNIQUES' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'USE_MUTATION_TESTING_TO_VALIDATE_TEST_QUALITY', 'artifact_type': 'directives', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/directives/use-mutation-testing-to-validate-test-quality.directive.yaml', 'message': "artifact id 'USE_MUTATION_TESTING_TO_VALIDATE_TEST_QUALITY' will field-merge into the built-in directive — declare 'enhances: USE_MUTATION_TESTING_TO_VALIDATE_TEST_QUALITY' to suppress this advisory, or 'overrides: USE_MUTATION_TESTING_TO_VALIDATE_TEST_QUALITY' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'adversarial-qa-handoff', 'artifact_type': 'tactics', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/tactics/adversarial-qa-handoff.tactic.yaml', 'message': "artifact id 'adversarial-qa-handoff' will field-merge into the built-in tactic — declare 'enhances: adversarial-qa-handoff' to suppress this advisory, or 'overrides: adversarial-qa-handoff' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'adversarial-squad-deployment', 'artifact_type': 'procedures', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/procedures/adversarial-squad-deployment.procedure.yaml', 'message': "artifact id 'adversarial-squad-deployment' will field-merge into the built-in procedure — declare 'enhances: adversarial-squad-deployment' to suppress this advisory, or 'overrides: adversarial-squad-deployment' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'aggregate-design-rules', 'artifact_type': 'styleguides', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/styleguides/aggregate-design-rules.styleguide.yaml', 'message': "artifact id 'aggregate-design-rules' will field-merge into the built-in styleguide — declare 'enhances: aggregate-design-rules' to suppress this advisory, or 'overrides: aggregate-design-rules' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'architectural-gate-non-vacuity', 'artifact_type': 'tactics', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/tactics/architectural-gate-non-vacuity.tactic.yaml', 'message': "artifact id 'architectural-gate-non-vacuity' will field-merge into the built-in tactic — declare 'enhances: architectural-gate-non-vacuity' to suppress this advisory, or 'overrides: architectural-gate-non-vacuity' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'atomic-design', 'artifact_type': 'paradigms', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/paradigms/atomic-design.paradigm.yaml', 'message': "artifact id 'atomic-design' will field-merge into the built-in paradigm — declare 'enhances: atomic-design' to suppress this advisory, or 'overrides: atomic-design' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'autonomous-operation-protocol', 'artifact_type': 'tactics', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/tactics/autonomous-operation-protocol.tactic.yaml', 'message': "artifact id 'autonomous-operation-protocol' will field-merge into the built-in tactic — declare 'enhances: autonomous-operation-protocol' to suppress this advisory, or 'overrides: autonomous-operation-protocol' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'avoid-gold-plating', 'artifact_type': 'tactics', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/tactics/avoid-gold-plating.tactic.yaml', 'message': "artifact id 'avoid-gold-plating' will field-merge into the built-in tactic — declare 'enhances: avoid-gold-plating' to suppress this advisory, or 'overrides: avoid-gold-plating' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'bdd-scenario-lifecycle', 'artifact_type': 'procedures', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/procedures/bdd-scenario-lifecycle.procedure.yaml', 'message': "artifact id 'bdd-scenario-lifecycle' will field-merge into the built-in procedure — declare 'enhances: bdd-scenario-lifecycle' to suppress this advisory, or 'overrides: bdd-scenario-lifecycle' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'behaviour-driven-development', 'artifact_type': 'paradigms', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/paradigms/behaviour-driven-development.paradigm.yaml', 'message': "artifact id 'behaviour-driven-development' will field-merge into the built-in paradigm — declare 'enhances: behaviour-driven-development' to suppress this advisory, or 'overrides: behaviour-driven-development' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'boring-code-review', 'artifact_type': 'styleguides', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/styleguides/boring-code-review.styleguide.yaml', 'message': "artifact id 'boring-code-review' will field-merge into the built-in styleguide — declare 'enhances: boring-code-review' to suppress this advisory, or 'overrides: boring-code-review' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'brownfield-onboarding', 'artifact_type': 'paradigms', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/paradigms/brownfield-onboarding.paradigm.yaml', 'message': "artifact id 'brownfield-onboarding' will field-merge into the built-in paradigm — declare 'enhances: brownfield-onboarding' to suppress this advisory, or 'overrides: brownfield-onboarding' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'c4-incremental-detail-modeling', 'artifact_type': 'paradigms', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/paradigms/c4-incremental-detail-modeling.paradigm.yaml', 'message': "artifact id 'c4-incremental-detail-modeling' will field-merge into the built-in paradigm — declare 'enhances: c4-incremental-detail-modeling' to suppress this advisory, or 'overrides: c4-incremental-detail-modeling' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'canonical-source-unification', 'artifact_type': 'tactics', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/tactics/canonical-source-unification.tactic.yaml', 'message': "artifact id 'canonical-source-unification' will field-merge into the built-in tactic — declare 'enhances: canonical-source-unification' to suppress this advisory, or 'overrides: canonical-source-unification' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'change-apply-smallest-viable-diff', 'artifact_type': 'tactics', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/tactics/change-apply-smallest-viable-diff.tactic.yaml', 'message': "artifact id 'change-apply-smallest-viable-diff' will field-merge into the built-in tactic — declare 'enhances: change-apply-smallest-viable-diff' to suppress this advisory, or 'overrides: change-apply-smallest-viable-diff' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'clean-linear-commit-history', 'artifact_type': 'tactics', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/tactics/clean-linear-commit-history.tactic.yaml', 'message': "artifact id 'clean-linear-commit-history' will field-merge into the built-in tactic — declare 'enhances: clean-linear-commit-history' to suppress this advisory, or 'overrides: clean-linear-commit-history' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'code-review-incremental', 'artifact_type': 'tactics', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/tactics/code-review-incremental.tactic.yaml', 'message': "artifact id 'code-review-incremental' will field-merge into the built-in tactic — declare 'enhances: code-review-incremental' to suppress this advisory, or 'overrides: code-review-incremental' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'common-docs', 'artifact_type': 'styleguides', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/styleguides/common-docs.styleguide.yaml', 'message': "artifact id 'common-docs' will field-merge into the built-in styleguide — declare 'enhances: common-docs' to suppress this advisory, or 'overrides: common-docs' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'common-docs-find', 'artifact_type': 'tactics', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/tactics/common-docs-find.tactic.yaml', 'message': "artifact id 'common-docs-find' will field-merge into the built-in tactic — declare 'enhances: common-docs-find' to suppress this advisory, or 'overrides: common-docs-find' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'common-docs-scaffold', 'artifact_type': 'tactics', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/tactics/common-docs-scaffold.tactic.yaml', 'message': "artifact id 'common-docs-scaffold' will field-merge into the built-in tactic — declare 'enhances: common-docs-scaffold' to suppress this advisory, or 'overrides: common-docs-scaffold' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'common-docs-structural-lint', 'artifact_type': 'assets', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/assets/docs_structural_lint.py.asset.yaml', 'message': "artifact id 'common-docs-structural-lint' will field-merge into the built-in asset — declare 'enhances: common-docs-structural-lint' to suppress this advisory, or 'overrides: common-docs-structural-lint' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'common-docs-write', 'artifact_type': 'tactics', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/tactics/common-docs-write.tactic.yaml', 'message': "artifact id 'common-docs-write' will field-merge into the built-in tactic — declare 'enhances: common-docs-write' to suppress this advisory, or 'overrides: common-docs-write' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'contextive', 'artifact_type': 'toolguides', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/toolguides/contextive.toolguide.yaml', 'message': "artifact id 'contextive' will field-merge into the built-in toolguide — declare 'enhances: contextive' to suppress this advisory, or 'overrides: contextive' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'deep-module-design', 'artifact_type': 'paradigms', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/paradigms/deep-module-design.paradigm.yaml', 'message': "artifact id 'deep-module-design' will field-merge into the built-in paradigm — declare 'enhances: deep-module-design' to suppress this advisory, or 'overrides: deep-module-design' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'deployable-skill-authoring', 'artifact_type': 'styleguides', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/styleguides/deployable-skill-authoring.styleguide.yaml', 'message': "artifact id 'deployable-skill-authoring' will field-merge into the built-in styleguide — declare 'enhances: deployable-skill-authoring' to suppress this advisory, or 'overrides: deployable-skill-authoring' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'development-assist-test-cleanup', 'artifact_type': 'procedures', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/procedures/development-assist-test-cleanup.procedure.yaml', 'message': "artifact id 'development-assist-test-cleanup' will field-merge into the built-in procedure — declare 'enhances: development-assist-test-cleanup' to suppress this advisory, or 'overrides: development-assist-test-cleanup' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'disciplined-defect-diagnosis', 'artifact_type': 'procedures', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/procedures/disciplined-defect-diagnosis.procedure.yaml', 'message': "artifact id 'disciplined-defect-diagnosis' will field-merge into the built-in procedure — declare 'enhances: disciplined-defect-diagnosis' to suppress this advisory, or 'overrides: disciplined-defect-diagnosis' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'divio-type-discipline', 'artifact_type': 'styleguides', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/styleguides/divio-type-discipline.styleguide.yaml', 'message': "artifact id 'divio-type-discipline' will field-merge into the built-in styleguide — declare 'enhances: divio-type-discipline' to suppress this advisory, or 'overrides: divio-type-discipline' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'docs-accessibility', 'artifact_type': 'styleguides', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/styleguides/docs-accessibility.styleguide.yaml', 'message': "artifact id 'docs-accessibility' will field-merge into the built-in styleguide — declare 'enhances: docs-accessibility' to suppress this advisory, or 'overrides: docs-accessibility' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'docs-freshness-sla', 'artifact_type': 'styleguides', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/styleguides/docs-freshness-sla.styleguide.yaml', 'message': "artifact id 'docs-freshness-sla' will field-merge into the built-in styleguide — declare 'enhances: docs-freshness-sla' to suppress this advisory, or 'overrides: docs-freshness-sla' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'documentation-gap-prioritization', 'artifact_type': 'procedures', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/procedures/documentation-gap-prioritization.procedure.yaml', 'message': "artifact id 'documentation-gap-prioritization' will field-merge into the built-in procedure — declare 'enhances: documentation-gap-prioritization' to suppress this advisory, or 'overrides: documentation-gap-prioritization' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'domain-aware-decision-interview', 'artifact_type': 'procedures', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/procedures/domain-aware-decision-interview.procedure.yaml', 'message': "artifact id 'domain-aware-decision-interview' will field-merge into the built-in procedure — declare 'enhances: domain-aware-decision-interview' to suppress this advisory, or 'overrides: domain-aware-decision-interview' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'domain-driven-design', 'artifact_type': 'paradigms', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/paradigms/domain-driven-design.paradigm.yaml', 'message': "artifact id 'domain-driven-design' will field-merge into the built-in paradigm — declare 'enhances: domain-driven-design' to suppress this advisory, or 'overrides: domain-driven-design' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'drill-down-documentation', 'artifact_type': 'procedures', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/procedures/drill-down-documentation.procedure.yaml', 'message': "artifact id 'drill-down-documentation' will field-merge into the built-in procedure — declare 'enhances: drill-down-documentation' to suppress this advisory, or 'overrides: drill-down-documentation' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'drupal-conventions', 'artifact_type': 'styleguides', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/styleguides/drupal-conventions.styleguide.yaml', 'message': "artifact id 'drupal-conventions' will field-merge into the built-in styleguide — declare 'enhances: drupal-conventions' to suppress this advisory, or 'overrides: drupal-conventions' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'drupal-review-checks', 'artifact_type': 'toolguides', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/toolguides/drupal-review-checks.toolguide.yaml', 'message': "artifact id 'drupal-review-checks' will field-merge into the built-in toolguide — declare 'enhances: drupal-review-checks' to suppress this advisory, or 'overrides: drupal-review-checks' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'drupal-security-performance', 'artifact_type': 'styleguides', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/styleguides/drupal-security-performance.styleguide.yaml', 'message': "artifact id 'drupal-security-performance' will field-merge into the built-in styleguide — declare 'enhances: drupal-security-performance' to suppress this advisory, or 'overrides: drupal-security-performance' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'easy-to-change', 'artifact_type': 'tactics', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/tactics/easy-to-change.tactic.yaml', 'message': "artifact id 'easy-to-change' will field-merge into the built-in tactic — declare 'enhances: easy-to-change' to suppress this advisory, or 'overrides: easy-to-change' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'efficient-local-tooling', 'artifact_type': 'toolguides', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/toolguides/efficient-local-tooling.toolguide.yaml', 'message': "artifact id 'efficient-local-tooling' will field-merge into the built-in toolguide — declare 'enhances: efficient-local-tooling' to suppress this advisory, or 'overrides: efficient-local-tooling' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'eisenhower-prioritisation', 'artifact_type': 'tactics', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/tactics/eisenhower-prioritisation.tactic.yaml', 'message': "artifact id 'eisenhower-prioritisation' will field-merge into the built-in tactic — declare 'enhances: eisenhower-prioritisation' to suppress this advisory, or 'overrides: eisenhower-prioritisation' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'event-storming-discovery', 'artifact_type': 'procedures', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/procedures/event-storming-discovery.procedure.yaml', 'message': "artifact id 'event-storming-discovery' will field-merge into the built-in procedure — declare 'enhances: event-storming-discovery' to suppress this advisory, or 'overrides: event-storming-discovery' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'example-mapping-workshop', 'artifact_type': 'procedures', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/procedures/example-mapping-workshop.procedure.yaml', 'message': "artifact id 'example-mapping-workshop' will field-merge into the built-in procedure — declare 'enhances: example-mapping-workshop' to suppress this advisory, or 'overrides: example-mapping-workshop' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'execution-lanes', 'artifact_type': 'paradigms', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/paradigms/execution-lanes.paradigm.yaml', 'message': "artifact id 'execution-lanes' will field-merge into the built-in paradigm — declare 'enhances: execution-lanes' to suppress this advisory, or 'overrides: execution-lanes' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'extract-then-publish-separation', 'artifact_type': 'paradigms', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/paradigms/extract-then-publish-separation.paradigm.yaml', 'message': "artifact id 'extract-then-publish-separation' will field-merge into the built-in paradigm — declare 'enhances: extract-then-publish-separation' to suppress this advisory, or 'overrides: extract-then-publish-separation' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'five-paradigm-parallel-debugging', 'artifact_type': 'tactics', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/tactics/five-paradigm-parallel-debugging.tactic.yaml', 'message': "artifact id 'five-paradigm-parallel-debugging' will field-merge into the built-in tactic — declare 'enhances: five-paradigm-parallel-debugging' to suppress this advisory, or 'overrides: five-paradigm-parallel-debugging' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'focused-function-complexity-check', 'artifact_type': 'tactics', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/tactics/focused-function-complexity-check.tactic.yaml', 'message': "artifact id 'focused-function-complexity-check' will field-merge into the built-in tactic — declare 'enhances: focused-function-complexity-check' to suppress this advisory, or 'overrides: focused-function-complexity-check' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'frozen-baseline-shrink-only-ratchet', 'artifact_type': 'tactics', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/tactics/frozen-baseline-shrink-only-ratchet.tactic.yaml', 'message': "artifact id 'frozen-baseline-shrink-only-ratchet' will field-merge into the built-in tactic — declare 'enhances: frozen-baseline-shrink-only-ratchet' to suppress this advisory, or 'overrides: frozen-baseline-shrink-only-ratchet' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'generated-code-stewardship', 'artifact_type': 'tactics', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/tactics/generated-code-stewardship.tactic.yaml', 'message': "artifact id 'generated-code-stewardship' will field-merge into the built-in tactic — declare 'enhances: generated-code-stewardship' to suppress this advisory, or 'overrides: generated-code-stewardship' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'gherkin', 'artifact_type': 'toolguides', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/toolguides/gherkin.toolguide.yaml', 'message': "artifact id 'gherkin' will field-merge into the built-in toolguide — declare 'enhances: gherkin' to suppress this advisory, or 'overrides: gherkin' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'git-agent-commit-signing', 'artifact_type': 'toolguides', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/toolguides/git-agent-commit-signing.toolguide.yaml', 'message': "artifact id 'git-agent-commit-signing' will field-merge into the built-in toolguide — declare 'enhances: git-agent-commit-signing' to suppress this advisory, or 'overrides: git-agent-commit-signing' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'git-flow', 'artifact_type': 'paradigms', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/paradigms/git-flow.paradigm.yaml', 'message': "artifact id 'git-flow' will field-merge into the built-in paradigm — declare 'enhances: git-flow' to suppress this advisory, or 'overrides: git-flow' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'git-worktree-pr-workflow', 'artifact_type': 'toolguides', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/toolguides/git-worktree-pr-workflow.toolguide.yaml', 'message': "artifact id 'git-worktree-pr-workflow' will field-merge into the built-in toolguide — declare 'enhances: git-worktree-pr-workflow' to suppress this advisory, or 'overrides: git-worktree-pr-workflow' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'github-tracker', 'artifact_type': 'toolguides', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/toolguides/github-tracker.toolguide.yaml', 'message': "artifact id 'github-tracker' will field-merge into the built-in toolguide — declare 'enhances: github-tracker' to suppress this advisory, or 'overrides: github-tracker' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'given-when-then-authoring', 'artifact_type': 'styleguides', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/styleguides/given-when-then-authoring.styleguide.yaml', 'message': "artifact id 'given-when-then-authoring' will field-merge into the built-in styleguide — declare 'enhances: given-when-then-authoring' to suppress this advisory, or 'overrides: given-when-then-authoring' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'glossary-maintenance-workflow', 'artifact_type': 'procedures', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/procedures/glossary-maintenance-workflow.procedure.yaml', 'message': "artifact id 'glossary-maintenance-workflow' will field-merge into the built-in procedure — declare 'enhances: glossary-maintenance-workflow' to suppress this advisory, or 'overrides: glossary-maintenance-workflow' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'input-validation-fail-fast', 'artifact_type': 'tactics', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/tactics/input-validation-fail-fast.tactic.yaml', 'message': "artifact id 'input-validation-fail-fast' will field-merge into the built-in tactic — declare 'enhances: input-validation-fail-fast' to suppress this advisory, or 'overrides: input-validation-fail-fast' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'issue-triage-state-machine', 'artifact_type': 'procedures', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/procedures/issue-triage-state-machine.procedure.yaml', 'message': "artifact id 'issue-triage-state-machine' will field-merge into the built-in procedure — declare 'enhances: issue-triage-state-machine' to suppress this advisory, or 'overrides: issue-triage-state-machine' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'java-conventions', 'artifact_type': 'styleguides', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/styleguides/java-conventions.styleguide.yaml', 'message': "artifact id 'java-conventions' will field-merge into the built-in styleguide — declare 'enhances: java-conventions' to suppress this advisory, or 'overrides: java-conventions' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'java-supply-chain', 'artifact_type': 'toolguides', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/toolguides/java-supply-chain.toolguide.yaml', 'message': "artifact id 'java-supply-chain' will field-merge into the built-in toolguide — declare 'enhances: java-supply-chain' to suppress this advisory, or 'overrides: java-supply-chain' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'javascript-supply-chain', 'artifact_type': 'toolguides', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/toolguides/javascript-supply-chain.toolguide.yaml', 'message': "artifact id 'javascript-supply-chain' will field-merge into the built-in toolguide — declare 'enhances: javascript-supply-chain' to suppress this advisory, or 'overrides: javascript-supply-chain' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'kitty-glossary-writing', 'artifact_type': 'styleguides', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/styleguides/writing/kitty-glossary-writing.styleguide.yaml', 'message': "artifact id 'kitty-glossary-writing' will field-merge into the built-in styleguide — declare 'enhances: kitty-glossary-writing' to suppress this advisory, or 'overrides: kitty-glossary-writing' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'legacy-codebase-triage', 'artifact_type': 'procedures', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/procedures/legacy-codebase-triage.procedure.yaml', 'message': "artifact id 'legacy-codebase-triage' will field-merge into the built-in procedure — declare 'enhances: legacy-codebase-triage' to suppress this advisory, or 'overrides: legacy-codebase-triage' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'maven-review-checks', 'artifact_type': 'toolguides', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/toolguides/maven-review-checks.toolguide.yaml', 'message': "artifact id 'maven-review-checks' will field-merge into the built-in toolguide — declare 'enhances: maven-review-checks' to suppress this advisory, or 'overrides: maven-review-checks' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'meeting-minutes-format', 'artifact_type': 'styleguides', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/styleguides/meeting-minutes-format.styleguide.yaml', 'message': "artifact id 'meeting-minutes-format' will field-merge into the built-in styleguide — declare 'enhances: meeting-minutes-format' to suppress this advisory, or 'overrides: meeting-minutes-format' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'meeting-minutes-pipeline', 'artifact_type': 'procedures', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/procedures/meeting-minutes-pipeline.procedure.yaml', 'message': "artifact id 'meeting-minutes-pipeline' will field-merge into the built-in procedure — declare 'enhances: meeting-minutes-pipeline' to suppress this advisory, or 'overrides: meeting-minutes-pipeline' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'mermaid-diagramming', 'artifact_type': 'toolguides', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/toolguides/mermaid-diagramming.toolguide.yaml', 'message': "artifact id 'mermaid-diagramming' will field-merge into the built-in toolguide — declare 'enhances: mermaid-diagramming' to suppress this advisory, or 'overrides: mermaid-diagramming' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'migrate-project-guidance-to-spec-kitty-charter', 'artifact_type': 'procedures', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/procedures/migrate-project-guidance-to-spec-kitty-charter.procedure.yaml', 'message': "artifact id 'migrate-project-guidance-to-spec-kitty-charter' will field-merge into the built-in procedure — declare 'enhances: migrate-project-guidance-to-spec-kitty-charter' to suppress this advisory, or 'overrides: migrate-project-guidance-to-spec-kitty-charter' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'mission-tracer-files', 'artifact_type': 'procedures', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/procedures/mission-tracer-files.procedure.yaml', 'message': "artifact id 'mission-tracer-files' will field-merge into the built-in procedure — declare 'enhances: mission-tracer-files' to suppress this advisory, or 'overrides: mission-tracer-files' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'mission-wrap-up-sequence', 'artifact_type': 'procedures', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/procedures/mission-wrap-up-sequence.procedure.yaml', 'message': "artifact id 'mission-wrap-up-sequence' will field-merge into the built-in procedure — declare 'enhances: mission-wrap-up-sequence' to suppress this advisory, or 'overrides: mission-wrap-up-sequence' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'model-task-routing', 'artifact_type': 'tactics', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/tactics/model-task-routing.tactic.yaml', 'message': "artifact id 'model-task-routing' will field-merge into the built-in tactic — declare 'enhances: model-task-routing' to suppress this advisory, or 'overrides: model-task-routing' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'moscow-scoping-lens', 'artifact_type': 'tactics', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/tactics/moscow-scoping-lens.tactic.yaml', 'message': "artifact id 'moscow-scoping-lens' will field-merge into the built-in tactic — declare 'enhances: moscow-scoping-lens' to suppress this advisory, or 'overrides: moscow-scoping-lens' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'mutation-aware-test-design', 'artifact_type': 'styleguides', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/styleguides/mutation-aware-test-design.styleguide.yaml', 'message': "artifact id 'mutation-aware-test-design' will field-merge into the built-in styleguide — declare 'enhances: mutation-aware-test-design' to suppress this advisory, or 'overrides: mutation-aware-test-design' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'occurrence-classification-workflow', 'artifact_type': 'tactics', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/tactics/occurrence-classification-workflow.tactic.yaml', 'message': "artifact id 'occurrence-classification-workflow' will field-merge into the built-in tactic — declare 'enhances: occurrence-classification-workflow' to suppress this advisory, or 'overrides: occurrence-classification-workflow' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'onboard-external-agent-to-pack', 'artifact_type': 'procedures', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/procedures/onboard-external-agent-to-pack.procedure.yaml', 'message': "artifact id 'onboard-external-agent-to-pack' will field-merge into the built-in procedure — declare 'enhances: onboard-external-agent-to-pack' to suppress this advisory, or 'overrides: onboard-external-agent-to-pack' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'op-or-mission-selection', 'artifact_type': 'tactics', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/tactics/op-or-mission-selection.tactic.yaml', 'message': "artifact id 'op-or-mission-selection' will field-merge into the built-in tactic — declare 'enhances: op-or-mission-selection' to suppress this advisory, or 'overrides: op-or-mission-selection' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'ownership-map-leeway', 'artifact_type': 'tactics', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/tactics/ownership-map-leeway.tactic.yaml', 'message': "artifact id 'ownership-map-leeway' will field-merge into the built-in tactic — declare 'enhances: ownership-map-leeway' to suppress this advisory, or 'overrides: ownership-map-leeway' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'plain-language', 'artifact_type': 'styleguides', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/styleguides/plain-language.styleguide.yaml', 'message': "artifact id 'plain-language' will field-merge into the built-in styleguide — declare 'enhances: plain-language' to suppress this advisory, or 'overrides: plain-language' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'planning-and-tracking', 'artifact_type': 'styleguides', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/styleguides/planning-and-tracking.styleguide.yaml', 'message': "artifact id 'planning-and-tracking' will field-merge into the built-in styleguide — declare 'enhances: planning-and-tracking' to suppress this advisory, or 'overrides: planning-and-tracking' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'plantuml-diagramming', 'artifact_type': 'toolguides', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/toolguides/plantuml-diagramming.toolguide.yaml', 'message': "artifact id 'plantuml-diagramming' will field-merge into the built-in toolguide — declare 'enhances: plantuml-diagramming' to suppress this advisory, or 'overrides: plantuml-diagramming' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'post-merge-arch-gate-adjudication', 'artifact_type': 'procedures', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/procedures/post-merge-arch-gate-adjudication.procedure.yaml', 'message': "artifact id 'post-merge-arch-gate-adjudication' will field-merge into the built-in procedure — declare 'enhances: post-merge-arch-gate-adjudication' to suppress this advisory, or 'overrides: post-merge-arch-gate-adjudication' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'powershell-syntax', 'artifact_type': 'toolguides', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/toolguides/powershell-syntax.toolguide.yaml', 'message': "artifact id 'powershell-syntax' will field-merge into the built-in toolguide — declare 'enhances: powershell-syntax' to suppress this advisory, or 'overrides: powershell-syntax' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'pr-agent-worktree-isolation', 'artifact_type': 'tactics', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/tactics/pr-agent-worktree-isolation.tactic.yaml', 'message': "artifact id 'pr-agent-worktree-isolation' will field-merge into the built-in tactic — declare 'enhances: pr-agent-worktree-isolation' to suppress this advisory, or 'overrides: pr-agent-worktree-isolation' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'professional-communications', 'artifact_type': 'styleguides', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/styleguides/professional-communications.styleguide.yaml', 'message': "artifact id 'professional-communications' will field-merge into the built-in styleguide — declare 'enhances: professional-communications' to suppress this advisory, or 'overrides: professional-communications' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'publication-authority', 'artifact_type': 'styleguides', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/styleguides/publication-authority.styleguide.yaml', 'message': "artifact id 'publication-authority' will field-merge into the built-in styleguide — declare 'enhances: publication-authority' to suppress this advisory, or 'overrides: publication-authority' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'python-conventions', 'artifact_type': 'styleguides', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/styleguides/python-conventions.styleguide.yaml', 'message': "artifact id 'python-conventions' will field-merge into the built-in styleguide — declare 'enhances: python-conventions' to suppress this advisory, or 'overrides: python-conventions' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'python-mutation-tools', 'artifact_type': 'toolguides', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/toolguides/python-mutation-tools.toolguide.yaml', 'message': "artifact id 'python-mutation-tools' will field-merge into the built-in toolguide — declare 'enhances: python-mutation-tools' to suppress this advisory, or 'overrides: python-mutation-tools' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'python-review-checks', 'artifact_type': 'toolguides', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/toolguides/python-review-checks.toolguide.yaml', 'message': "artifact id 'python-review-checks' will field-merge into the built-in toolguide — declare 'enhances: python-review-checks' to suppress this advisory, or 'overrides: python-review-checks' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'python-supply-chain', 'artifact_type': 'toolguides', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/toolguides/python-supply-chain.toolguide.yaml', 'message': "artifact id 'python-supply-chain' will field-merge into the built-in toolguide — declare 'enhances: python-supply-chain' to suppress this advisory, or 'overrides: python-supply-chain' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'quadruple-a-test-format', 'artifact_type': 'styleguides', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/styleguides/quadruple-a-test-format.styleguide.yaml', 'message': "artifact id 'quadruple-a-test-format' will field-merge into the built-in styleguide — declare 'enhances: quadruple-a-test-format' to suppress this advisory, or 'overrides: quadruple-a-test-format' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'reasons-canvas-fill', 'artifact_type': 'tactics', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/tactics/reasons-canvas-fill.tactic.yaml', 'message': "artifact id 'reasons-canvas-fill' will field-merge into the built-in tactic — declare 'enhances: reasons-canvas-fill' to suppress this advisory, or 'overrides: reasons-canvas-fill' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'reasons-canvas-review', 'artifact_type': 'tactics', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/tactics/reasons-canvas-review.tactic.yaml', 'message': "artifact id 'reasons-canvas-review' will field-merge into the built-in tactic — declare 'enhances: reasons-canvas-review' to suppress this advisory, or 'overrides: reasons-canvas-review' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'reasons-canvas-writing', 'artifact_type': 'styleguides', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/styleguides/reasons-canvas-writing.styleguide.yaml', 'message': "artifact id 'reasons-canvas-writing' will field-merge into the built-in styleguide — declare 'enhances: reasons-canvas-writing' to suppress this advisory, or 'overrides: reasons-canvas-writing' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'red-main-release-discipline', 'artifact_type': 'procedures', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/procedures/red-main-release-discipline.procedure.yaml', 'message': "artifact id 'red-main-release-discipline' will field-merge into the built-in procedure — declare 'enhances: red-main-release-discipline' to suppress this advisory, or 'overrides: red-main-release-discipline' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'refactoring', 'artifact_type': 'procedures', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/procedures/refactoring.procedure.yaml', 'message': "artifact id 'refactoring' will field-merge into the built-in procedure — declare 'enhances: refactoring' to suppress this advisory, or 'overrides: refactoring' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'research-citation-discipline', 'artifact_type': 'styleguides', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/styleguides/research-citation-discipline.styleguide.yaml', 'message': "artifact id 'research-citation-discipline' will field-merge into the built-in styleguide — declare 'enhances: research-citation-discipline' to suppress this advisory, or 'overrides: research-citation-discipline' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'review-intent-and-risk-first', 'artifact_type': 'tactics', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/tactics/review-intent-and-risk-first.tactic.yaml', 'message': "artifact id 'review-intent-and-risk-first' will field-merge into the built-in tactic — declare 'enhances: review-intent-and-risk-first' to suppress this advisory, or 'overrides: review-intent-and-risk-first' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'reviewer-implementer-role-separation', 'artifact_type': 'tactics', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/tactics/reviewer-implementer-role-separation.tactic.yaml', 'message': "artifact id 'reviewer-implementer-role-separation' will field-merge into the built-in tactic — declare 'enhances: reviewer-implementer-role-separation' to suppress this advisory, or 'overrides: reviewer-implementer-role-separation' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'secure-design-checklist', 'artifact_type': 'tactics', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/tactics/secure-design-checklist.tactic.yaml', 'message': "artifact id 'secure-design-checklist' will field-merge into the built-in tactic — declare 'enhances: secure-design-checklist' to suppress this advisory, or 'overrides: secure-design-checklist' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'secure-regex-catastrophic-backtracking', 'artifact_type': 'tactics', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/tactics/secure-regex-catastrophic-backtracking.tactic.yaml', 'message': "artifact id 'secure-regex-catastrophic-backtracking' will field-merge into the built-in tactic — declare 'enhances: secure-regex-catastrophic-backtracking' to suppress this advisory, or 'overrides: secure-regex-catastrophic-backtracking' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'semantic-compression', 'artifact_type': 'paradigms', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/paradigms/semantic-compression.paradigm.yaml', 'message': "artifact id 'semantic-compression' will field-merge into the built-in paradigm — declare 'enhances: semantic-compression' to suppress this advisory, or 'overrides: semantic-compression' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'shared-branch-ci', 'artifact_type': 'paradigms', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/paradigms/shared-branch-ci.paradigm.yaml', 'message': "artifact id 'shared-branch-ci' will field-merge into the built-in paradigm — declare 'enhances: shared-branch-ci' to suppress this advisory, or 'overrides: shared-branch-ci' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'situational-assessment', 'artifact_type': 'procedures', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/procedures/situational-assessment.procedure.yaml', 'message': "artifact id 'situational-assessment' will field-merge into the built-in procedure — declare 'enhances: situational-assessment' to suppress this advisory, or 'overrides: situational-assessment' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'sonar', 'artifact_type': 'toolguides', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/toolguides/sonar.toolguide.yaml', 'message': "artifact id 'sonar' will field-merge into the built-in toolguide — declare 'enhances: sonar' to suppress this advisory, or 'overrides: sonar' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'specification-by-example', 'artifact_type': 'paradigms', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/paradigms/specification-by-example.paradigm.yaml', 'message': "artifact id 'specification-by-example' will field-merge into the built-in paradigm — declare 'enhances: specification-by-example' to suppress this advisory, or 'overrides: specification-by-example' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'spike-timebox-policy', 'artifact_type': 'procedures', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/procedures/spike-timebox-policy.procedure.yaml', 'message': "artifact id 'spike-timebox-policy' will field-merge into the built-in procedure — declare 'enhances: spike-timebox-policy' to suppress this advisory, or 'overrides: spike-timebox-policy' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'stopping-conditions', 'artifact_type': 'tactics', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/tactics/stopping-conditions.tactic.yaml', 'message': "artifact id 'stopping-conditions' will field-merge into the built-in tactic — declare 'enhances: stopping-conditions' to suppress this advisory, or 'overrides: stopping-conditions' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'structured-prompt-driven-development', 'artifact_type': 'paradigms', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/paradigms/structured-prompt-driven-development.paradigm.yaml', 'message': "artifact id 'structured-prompt-driven-development' will field-merge into the built-in paradigm — declare 'enhances: structured-prompt-driven-development' to suppress this advisory, or 'overrides: structured-prompt-driven-development' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'test-desiderata-and-boundaries', 'artifact_type': 'styleguides', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/styleguides/test-desiderata-and-boundaries.styleguide.yaml', 'message': "artifact id 'test-desiderata-and-boundaries' will field-merge into the built-in styleguide — declare 'enhances: test-desiderata-and-boundaries' to suppress this advisory, or 'overrides: test-desiderata-and-boundaries' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'test-first-bug-fixing', 'artifact_type': 'procedures', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/procedures/test-first-bug-fixing.procedure.yaml', 'message': "artifact id 'test-first-bug-fixing' will field-merge into the built-in procedure — declare 'enhances: test-first-bug-fixing' to suppress this advisory, or 'overrides: test-first-bug-fixing' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'testing-principles', 'artifact_type': 'styleguides', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/styleguides/testing-principles.styleguide.yaml', 'message': "artifact id 'testing-principles' will field-merge into the built-in styleguide — declare 'enhances: testing-principles' to suppress this advisory, or 'overrides: testing-principles' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'tiered-standards', 'artifact_type': 'styleguides', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/styleguides/tiered-standards.styleguide.yaml', 'message': "artifact id 'tiered-standards' will field-merge into the built-in styleguide — declare 'enhances: tiered-standards' to suppress this advisory, or 'overrides: tiered-standards' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'trunk-based', 'artifact_type': 'paradigms', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/paradigms/trunk-based.paradigm.yaml', 'message': "artifact id 'trunk-based' will field-merge into the built-in paradigm — declare 'enhances: trunk-based' to suppress this advisory, or 'overrides: trunk-based' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'typescript-mutation-tools', 'artifact_type': 'toolguides', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/toolguides/typescript-mutation-tools.toolguide.yaml', 'message': "artifact id 'typescript-mutation-tools' will field-merge into the built-in toolguide — declare 'enhances: typescript-mutation-tools' to suppress this advisory, or 'overrides: typescript-mutation-tools' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'work-package-completion-validation', 'artifact_type': 'tactics', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/tactics/work-package-completion-validation.tactic.yaml', 'message': "artifact id 'work-package-completion-validation' will field-merge into the built-in tactic — declare 'enhances: work-package-completion-validation' to suppress this advisory, or 'overrides: work-package-completion-validation' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'writing-audience-agentic-framework-core-team', 'artifact_type': 'assets', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/assets/audiences/agentic-framework-core-team.md.asset.yaml', 'message': "artifact id 'writing-audience-agentic-framework-core-team' will field-merge into the built-in asset — declare 'enhances: writing-audience-agentic-framework-core-team' to suppress this advisory, or 'overrides: writing-audience-agentic-framework-core-team' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'writing-audience-automation-agent', 'artifact_type': 'assets', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/assets/audiences/automation_agent.md.asset.yaml', 'message': "artifact id 'writing-audience-automation-agent' will field-merge into the built-in asset — declare 'enhances: writing-audience-automation-agent' to suppress this advisory, or 'overrides: writing-audience-automation-agent' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'writing-audience-line-manager', 'artifact_type': 'assets', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/assets/audiences/line_manager.md.asset.yaml', 'message': "artifact id 'writing-audience-line-manager' will field-merge into the built-in asset — declare 'enhances: writing-audience-line-manager' to suppress this advisory, or 'overrides: writing-audience-line-manager' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'writing-audience-nontech-educator', 'artifact_type': 'assets', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/assets/audiences/nontech_educator.md.asset.yaml', 'message': "artifact id 'writing-audience-nontech-educator' will field-merge into the built-in asset — declare 'enhances: writing-audience-nontech-educator' to suppress this advisory, or 'overrides: writing-audience-nontech-educator' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': 'writing-audience-software-engineer', 'artifact_type': 'assets', 'category': 'same_id_collision', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/assets/audiences/software_engineer.md.asset.yaml', 'message': "artifact id 'writing-audience-software-engineer' will field-merge into the built-in asset — declare 'enhances: writing-audience-software-engineer' to suppress this advisory, or 'overrides: writing-audience-software-engineer' to declare a full replacement", 'severity': 'advisory'}
- {'artifact_id': None, 'artifact_type': 'pack', 'category': 'PACK_LEVEL_MISSING', 'file': '/home/stijn/Documents/_code/SDD/fork/spec-kitty-open-packs/built-in/pack.yaml', 'message': "PACK_LEVEL_MISSING: pack.yaml has no 'pack_level'; add 'pack_level: built-in|org|project' (required once the deprecation window closes)", 'severity': 'advisory'}
