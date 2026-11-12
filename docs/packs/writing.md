---
title: writing pack reference
description: "Generated reference for the writing Charter Pack: artifact inventory, per-kind counts, content checksum, and validation status."
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

# writing pack reference

> **Generated page — do not edit by hand.** This file is produced by `scripts/docs/gen_pack_reference.py` from the pack source. Hand edits are overwritten on regeneration, and the CI drift gate fails on any difference.

## Provenance & integrity

- **Pack directory:** `packs/writing`
- **Declared version:** `1.0.0`
- **Content checksum (sha256):** `8163257eacb43a050986a33f4f21731af8f4123a2176dd45dd9c73a1d5818736`
- **Checksum recipe:** sha256 over the sorted `(relative-path + NUL + bytes + LF)` of every file in the pack directory. Re-hash a downloaded pack with the same recipe to verify integrity.

## Purpose

Documentation, communication and terminology doctrine, and a member of the `built-in`
distribution: the documentation mission type; the comms, scribe, minutes, synthesis, diagram,
lexical and curator profiles; Common Docs and audience-oriented writing directives, the
documentation styleguides, diagram toolguides, the glossary-stewardship tactics and templates, and
the writing-audience assets.

**Depends on:** `01M75HSYR9S9KPA372PHGT0EX3 ==1.0.0`

## Artifact inventory

| Kind | Count |
| --- | --- |
| `directives` | 4 |
| `tactics` | 9 |
| `styleguides` | 11 |
| `toolguides` | 6 |
| `procedures` | 8 |
| `agent_profiles` | 7 |
| `assets` | 13 |
| `missions` | 38 |
| `templates` | 2 |
| **Total files** | **112** |

### Full listing

<details>
<summary><code>directives</code> (4)</summary>

- `042-common-docs.directive.yaml`
- `047-audience-oriented-writing.directive.yaml`
- `action-item-attribution.directive.yaml`
- `minutes-stand-alone.directive.yaml`

</details>

<details>
<summary><code>tactics</code> (9)</summary>

- `analysis/code-documentation-analysis.tactic.yaml`
- `analysis/context-boundary-inference.tactic.yaml`
- `analysis/terminology-extraction-mapping.tactic.yaml`
- `common-docs-find.tactic.yaml`
- `common-docs-scaffold.tactic.yaml`
- `common-docs-write.tactic.yaml`
- `communication/documentation-curation-audit.tactic.yaml`
- `communication/stakeholder-alignment.tactic.yaml`
- `communication/writing-audience-catalog.tactic.yaml`

</details>

<details>
<summary><code>styleguides</code> (11)</summary>

- `common-docs.styleguide.yaml`
- `divio-type-discipline.styleguide.yaml`
- `docs-accessibility.styleguide.yaml`
- `docs-freshness-sla.styleguide.yaml`
- `meeting-minutes-format.styleguide.yaml`
- `plain-language.styleguide.yaml`
- `professional-communications.styleguide.yaml`
- `publication-authority.styleguide.yaml`
- `research-citation-discipline.styleguide.yaml`
- `writing/README.md`
- `writing/kitty-glossary-writing.styleguide.yaml`

</details>

<details>
<summary><code>toolguides</code> (6)</summary>

- `contextive.guide.md`
- `contextive.toolguide.yaml`
- `mermaid-diagramming.guide.md`
- `mermaid-diagramming.toolguide.yaml`
- `plantuml-diagramming.guide.md`
- `plantuml-diagramming.toolguide.yaml`

</details>

<details>
<summary><code>procedures</code> (8)</summary>

- `action-item-attribution-gate.procedure.yaml`
- `audience-oriented-drafting.procedure.yaml`
- `common-docs-page-authoring.procedure.yaml`
- `declare-page-audience.procedure.yaml`
- `documentation-gap-prioritization.procedure.yaml`
- `glossary-maintenance-workflow.procedure.yaml`
- `meeting-minutes-pipeline.procedure.yaml`
- `minutes-self-sufficiency-check.procedure.yaml`

</details>

<details>
<summary><code>agent_profiles</code> (7)</summary>

- `comms-cleo.agent.yaml`
- `curator-carla.agent.yaml`
- `diagram-daisy.agent.yaml`
- `lexical-larry.agent.yaml`
- `minutes-mahad.agent.yaml`
- `scribe-sally.agent.yaml`
- `synthesizer-sam.agent.yaml`

</details>

<details>
<summary><code>assets</code> (13)</summary>

- `README.md`
- `audiences/README.md`
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
<summary><code>missions</code> (38)</summary>

- `built_in_step_contracts/documentation-accept.step-contract.yaml`
- `built_in_step_contracts/documentation-audit.step-contract.yaml`
- `built_in_step_contracts/documentation-design.step-contract.yaml`
- `built_in_step_contracts/documentation-discover.step-contract.yaml`
- `built_in_step_contracts/documentation-generate.step-contract.yaml`
- `built_in_step_contracts/documentation-publish.step-contract.yaml`
- `built_in_step_contracts/documentation-validate.step-contract.yaml`
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

</details>

<details>
<summary><code>templates</code> (2)</summary>

- `writing/meeting-discussion-notes.md`
- `writing/meeting-minutes.md`

</details>

## Validation

Reported by the charter pack schemas (`scripts/ci/validate_pack_schemas.py`): **passing**.

- Errors: 0
