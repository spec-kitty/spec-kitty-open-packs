---
title: internal pack reference
description: "Generated reference for the internal Charter Pack: artifact inventory, per-kind counts, content checksum, and validation status."
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

# internal pack reference

> **Generated page — do not edit by hand.** This file is produced by `scripts/docs/gen_pack_reference.py` from the pack source. Hand edits are overwritten on regeneration, and the CI drift gate fails on any difference.

## Provenance & integrity

- **Pack directory:** `packs/internal`
- **Declared version:** `2.0.0`
- **Content checksum (sha256):** `00aaed13e722e978b9896622c702bd78d7a9da32f3cfdff6e74a24a257207de8`
- **Checksum recipe:** sha256 over the sorted `(relative-path + NUL + bytes + LF)` of every file in the pack directory. Re-hash a downloaded pack with the same recipe to verify integrity.

## Purpose

Spec Kitty's own internal Charter Pack: the doctrine that governs the Spec Kitty project's
contributors, maintainers and core team. It is loaded as an org-tier pack (registered in
`.kittify/config.yaml` under `charter_packs.org.packs`), overlaying the public `built-in`
product doctrine.

It is never shipped to consumers: maintainer-only doctrine — how PRs are landed, the tracker
processed, main kept honest — must not be force-shipped on the wheel, so the packaging narrows
its `packs` include to `packs/built-in/` specifically to keep this tree in-repo.

**Depends on:** `01M75HSYR9S9KPA372PHGT0EX3 >=1.0,<2`, `01M75PCTEKGDXQW59TGSFQQ9QT >=2.0,<3`, `01M75PCTD0V3AFZA9EAXDJ894D >=2.0,<3`, `01M75PCTC6HS38NX8HJGT26VTP >=2.0,<3`, `01M75HSYS69RYRFPB4WCC5AC9D >=1.0,<2`

## Artifact inventory

| Kind | Count |
| --- | --- |
| `directives` | 5 |
| `tactics` | 4 |
| `styleguides` | 7 |
| `toolguides` | 6 |
| `procedures` | 19 |
| `assets` | 22 |
| `glossary_packs` | 1 |
| `drg` | 1 |
| `presets` | 1 |
| `skills` | 10 |
| **Total files** | **81** |

### Full listing

<details>
<summary><code>directives</code> (5)</summary>

- `cloud-session-orchestration.directive.yaml`
- `no-full-heavy-suites-in-mission.directive.yaml`
- `operator-signal-contract.directive.yaml`
- `spec-kitty-docs-conventions.directive.yaml`
- `spec-kitty-red-main-policy.directive.yaml`

</details>

<details>
<summary><code>tactics</code> (4)</summary>

- `branded-deliverable.tactic.yaml`
- `spec-kitty-gate-non-vacuity-exemplar.tactic.yaml`
- `spec-kitty-ratchet-cost.tactic.yaml`
- `tracker-backlog-iterative-deepening.tactic.yaml`

</details>

<details>
<summary><code>styleguides</code> (7)</summary>

- `executive-debrief.styleguide.yaml`
- `feature-and-scenario-authoring.styleguide.yaml`
- `report-writing.styleguide.yaml`
- `spec-kitty-docs-lint-config.styleguide.yaml`
- `spec-kitty-package-tiers.styleguide.yaml`
- `spec-kitty-tracker-labels.styleguide.yaml`
- `tiered-standards.styleguide.yaml`

</details>

<details>
<summary><code>toolguides</code> (6)</summary>

- `branded-document-generation.guide.md`
- `branded-document-generation.toolguide.yaml`
- `terminology-guard.guide.md`
- `terminology-guard.toolguide.yaml`
- `test-quality-triage.guide.md`
- `test-quality-triage.toolguide.yaml`

</details>

<details>
<summary><code>procedures</code> (19)</summary>

- `charter-offering-scenario-extraction.procedure.yaml`
- `cloud-session-dispatch.procedure.yaml`
- `executive-debrief-generation.procedure.yaml`
- `issue-to-mission-delivery.procedure.yaml`
- `issue-triage-pass.procedure.yaml`
- `landing-contributor-prs.procedure.yaml`
- `memory-curation-and-escalation.procedure.yaml`
- `mission-tracer-files.procedure.yaml`
- `mission-wrap-up-sequence.procedure.yaml`
- `operator-signal-emission.procedure.yaml`
- `project-evolution-postmortem.procedure.yaml`
- `semi-auto-delivery.procedure.yaml`
- `spec-kitty-arch-gate-adjudication.procedure.yaml`
- `spec-kitty-common-docs-layout.procedure.yaml`
- `spec-kitty-page-audience.procedure.yaml`
- `spec-kitty-red-main-triage.procedure.yaml`
- `targeted-mission-test-run.procedure.yaml`
- `test-suite-quality-assessment.procedure.yaml`
- `tracker-organisation-workflow.procedure.yaml`

</details>

<details>
<summary><code>assets</code> (22)</summary>

- `audiences/agentic-framework-core-team.md`
- `audiences/agentic-framework-core-team.md.asset.yaml`
- `debrief/collect-debrief.py`
- `debrief/collect-debrief.py.asset.yaml`
- `debrief/debrief-template.html`
- `debrief/debrief-template.html.asset.yaml`
- `debrief/fonts/FallingSky-Bold.otf`
- `debrief/fonts/FallingSky-Bold.otf.asset.yaml`
- `debrief/fonts/FallingSky-Extrabold.otf`
- `debrief/fonts/FallingSky-Extrabold.otf.asset.yaml`
- `debrief/fonts/FallingSky-Regular.otf`
- `debrief/fonts/FallingSky-Regular.otf.asset.yaml`
- `debrief/logo.png`
- `debrief/logo.png.asset.yaml`
- `debrief/render-debrief.py`
- `debrief/render-debrief.py.asset.yaml`
- `spec-kitty-branded-pdf.py`
- `spec-kitty-branded-pdf.py.asset.yaml`
- `test-quality-scan.py`
- `test-quality-scan.py.asset.yaml`
- `validate-pr-body.py`
- `validate-pr-body.py.asset.yaml`

</details>

<details>
<summary><code>glossary_packs</code> (1)</summary>

- `spk-internal-glossary.glossary-pack.yaml`

</details>

<details>
<summary><code>drg</code> (1)</summary>

- `fragment.yaml`

</details>

<details>
<summary><code>presets</code> (1)</summary>

- `base.yaml`

</details>

<details>
<summary><code>skills</code> (10)</summary>

- `issue-triage.skill.md`
- `issue-triage.skill.yaml`
- `land-pr.skill.md`
- `land-pr.skill.yaml`
- `mission-from-issue.skill.md`
- `mission-from-issue.skill.yaml`
- `report-debrief.skill.md`
- `report-debrief.skill.yaml`
- `semi-auto.skill.md`
- `semi-auto.skill.yaml`

</details>

## Validation

Reported by the charter pack schemas (`scripts/ci/validate_pack_schemas.py`): **passing**.

- Errors: 0
