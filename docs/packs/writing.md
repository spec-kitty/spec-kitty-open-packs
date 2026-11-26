---
title: writing pack reference
description: "Generated reference for the writing Charter Pack: artifact inventory, per-kind counts, and content checksum."
doc_status: active
updated: '2026-11-12'
kind: Reference
related:
- packs
- architecture/docsite-design
- packs/catalog-proposal
generated:
  by: scripts/docs/gen_pack_reference.py
  at: '2026-11-12'
---

# writing pack reference

> **Generated page — do not edit by hand.** This file is produced by `scripts/docs/gen_pack_reference.py` from the pack source. Hand edits are overwritten on regeneration, and the CI drift gate fails on any difference.

## Provenance & integrity

- **Pack directory:** `packs/writing`
- **Pack level:** `built-in`
- **Declared version:** `3.7.0`
- **Content checksum (sha256):** `369fb00adb6b9902e7f7c3252f1f1820af48fcca3e4ffc10dc79a11311063804`
- **Checksum recipe:** sha256 over the sorted `(relative-path + NUL + bytes + LF)` of every file in the pack directory. Re-hash a downloaded pack with the same recipe to verify integrity.

## Purpose

Documentation, communication and terminology doctrine, and a member of the `built-in`
distribution: the documentation mission type; the comms, scribe, minutes, synthesis, diagram,
lexical and curator profiles; Common Docs and audience-oriented writing directives, the
documentation styleguides, the diagram and docs structural-lint toolguides, the
glossary-stewardship tactics and templates, the docs structural lint and the writing-audience
assets.

**Depends on:** [`foundation`](foundation.md) `==3.7.0`

## Artifact inventory

| Kind | Count |
| --- | --- |
| `directives` | 4 |
| `tactics` | 9 |
| `styleguides` | 12 |
| `toolguides` | 8 |
| `procedures` | 8 |
| `anti_patterns` | 39 |
| `agent_profiles` | 7 |
| `assets` | 14 |
| `missions` | 29 |
| `templates` | 2 |
| **Total files** | **146** |

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
<summary><code>styleguides</code> (12)</summary>

- `ai-writing-tells.styleguide.yaml`
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
<summary><code>toolguides</code> (8)</summary>

- `common-docs-structural-lint.guide.md`
- `common-docs-structural-lint.toolguide.yaml`
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
<summary><code>anti_patterns</code> (39)</summary>

- `aspirational-documentation-ahead-of-the-code.anti-pattern.yaml`
- `assuming-reader-knowledge.anti-pattern.yaml`
- `bare-sha-citation.anti-pattern.yaml`
- `buried-contradiction.anti-pattern.yaml`
- `buzzword-soup.anti-pattern.yaml`
- `calling-the-llm-from-inside-the-optional-publish-step.anti-pattern.yaml`
- `circular-definition.anti-pattern.yaml`
- `citation-laundering.anti-pattern.yaml`
- `confidence-inflation.anti-pattern.yaml`
- `drifting-line-citation.anti-pattern.yaml`
- `duplicated-fact-with-no-canonical-home.anti-pattern.yaml`
- `em-dash-sprawl-and-buzzword-fog.anti-pattern.yaml`
- `empty-or-ownerless-action-items-in-discussion-notes.anti-pattern.yaml`
- `forcing-a-discussion-meeting-into-the-decision-table.anti-pattern.yaml`
- `freshness-date-bumped-without-re-verifying-content.anti-pattern.yaml`
- `hand-patching-a-generated-page-to-look-current.anti-pattern.yaml`
- `implementation-leaking-into-definition.anti-pattern.yaml`
- `jargon-aimed-at-the-wrong-audience.anti-pattern.yaml`
- `meaning-carried-only-by-colour-or-only-by-a-diagram.anti-pattern.yaml`
- `missing-or-wrong-section-order.anti-pattern.yaml`
- `narrating-existing-state-as-a-decision.anti-pattern.yaml`
- `one-size-fits-none-document.anti-pattern.yaml`
- `passive-hedged-filler-laden-instruction.anti-pattern.yaml`
- `publishing-without-the-validated-markdown-in-this-chat.anti-pattern.yaml`
- `reference-page-carrying-narrative-rationale.anti-pattern.yaml`
- `rendering-without-selecting-a-format.anti-pattern.yaml`
- `requiring-an-api-key-for-an-already-running-chat-agent.anti-pattern.yaml`
- `returning-final-minutes-while-attribution-gaps-remain.anti-pattern.yaml`
- `second-documentation-root.anti-pattern.yaml`
- `sidecar-metadata-ssot.anti-pattern.yaml`
- `silent-fact-drift.anti-pattern.yaml`
- `skipped-or-size-driven-heading-levels.anti-pattern.yaml`
- `transcript-level-detail-in-notes.anti-pattern.yaml`
- `treating-json-or-wiki-publish-as-mandatory-delivery.anti-pattern.yaml`
- `treating-truncation-silently.anti-pattern.yaml`
- `tutorial-that-branches-on-reader-choices.anti-pattern.yaml`
- `unattributed-action-items.anti-pattern.yaml`
- `undefined-audience.anti-pattern.yaml`
- `unsourced-assertion.anti-pattern.yaml`

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
<summary><code>assets</code> (14)</summary>

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
- `docs_structural_lint.config.yaml.asset.yaml`
- `docs_structural_lint.py`
- `docs_structural_lint.py.asset.yaml`

</details>

<details>
<summary><code>missions</code> (29)</summary>

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

</details>

<details>
<summary><code>templates</code> (2)</summary>

- `writing/meeting-discussion-notes.md`
- `writing/meeting-minutes.md`

</details>
