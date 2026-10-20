---
title: internal pack reference
description: "Generated reference for the internal Charter Pack: artifact inventory, per-kind counts, content checksum, and validation status."
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

# internal pack reference

> **Generated page — do not edit by hand.** This file is produced by `scripts/docs/gen_pack_reference.py` from the pack source. Hand edits are overwritten on regeneration, and the CI drift gate fails on any difference.

## Provenance & integrity

- **Pack directory:** `packs/internal`
- **Declared version:** `1.0.0`
- **Content checksum (sha256):** `c051f32dd23c5db23bc2f559958dd1e6170993738e20a145d7999b8d492f6ebc`
- **Checksum recipe:** sha256 over the sorted `(relative-path + NUL + bytes)` of every file in the pack directory. Re-hash a downloaded pack with the same recipe to verify integrity.

## Purpose

_No `purpose` is declared in this pack's `pack.yaml`, so none is shown here (the generator never fabricates one). See the pack's `README.md` and the [Packs hub](index.md) for authored context._

## Artifact inventory

| Kind | Count |
| --- | --- |
| `directives` | 2 |
| `tactics` | 4 |
| `styleguides` | 6 |
| `toolguides` | 6 |
| `procedures` | 13 |
| `assets` | 20 |
| `glossary_packs` | 1 |
| `drg` | 1 |
| `skills` | 10 |
| **Total files** | **67** |

### Full listing

<details>
<summary><code>directives</code> (2)</summary>

- `no-full-heavy-suites-in-mission.directive.yaml`
- `operator-signal-contract.directive.yaml`

</details>

<details>
<summary><code>tactics</code> (4)</summary>

- `branded-deliverable.tactic.yaml`
- `spec-kitty-gate-non-vacuity-exemplar.tactic.yaml`
- `spec-kitty-ratchet-cost.tactic.yaml`
- `tracker-backlog-iterative-deepening.tactic.yaml`

</details>

<details>
<summary><code>styleguides</code> (6)</summary>

- `executive-debrief.styleguide.yaml`
- `feature-and-scenario-authoring.styleguide.yaml`
- `report-writing.styleguide.yaml`
- `spec-kitty-docs-lint-config.styleguide.yaml`
- `spec-kitty-package-tiers.styleguide.yaml`
- `spec-kitty-tracker-labels.styleguide.yaml`

</details>

<details>
<summary><code>toolguides</code> (6)</summary>

- `BRANDED_DOCUMENT_GENERATION.md`
- `TERMINOLOGY_GUARD.md`
- `TEST_QUALITY_TRIAGE.md`
- `branded-document-generation.toolguide.yaml`
- `terminology-guard.toolguide.yaml`
- `test-quality-triage.toolguide.yaml`

</details>

<details>
<summary><code>procedures</code> (13)</summary>

- `charter-offering-scenario-extraction.procedure.yaml`
- `cloud-session-dispatch.procedure.yaml`
- `executive-debrief-generation.procedure.yaml`
- `issue-to-mission-delivery.procedure.yaml`
- `issue-triage-pass.procedure.yaml`
- `landing-contributor-prs.procedure.yaml`
- `memory-curation-and-escalation.procedure.yaml`
- `project-evolution-postmortem.procedure.yaml`
- `semi-auto-delivery.procedure.yaml`
- `spec-kitty-arch-gate-adjudication.procedure.yaml`
- `spec-kitty-red-main-policy.procedure.yaml`
- `test-suite-quality-assessment.procedure.yaml`
- `tracker-organisation-workflow.procedure.yaml`

</details>

<details>
<summary><code>assets</code> (20)</summary>

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

- `spk-internal.glossary-pack.yaml`

</details>

<details>
<summary><code>drg</code> (1)</summary>

- `fragment.yaml`

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

Reported by `spec-kitty charter pack validate --json`: **passing (`ok: true`)**.

- Errors: 0

Advisories are non-blocking and vary by validator version; run `spec-kitty charter pack validate <dir> --json` for the current list.
