---
title: planning-analysis pack reference
description: "Generated reference for the planning-analysis Charter Pack: artifact inventory, per-kind counts, content checksum, and validation status."
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

# planning-analysis pack reference

> **Generated page — do not edit by hand.** This file is produced by `scripts/docs/gen_pack_reference.py` from the pack source. Hand edits are overwritten on regeneration, and the CI drift gate fails on any difference.

## Provenance & integrity

- **Pack directory:** `packs/planning-analysis`
- **Declared version:** `2.0.0`
- **Content checksum (sha256):** `8f410ac56a952d5819803ec0c79344423279df143135d633344b27e5de532bab`
- **Checksum recipe:** sha256 over the sorted `(relative-path + NUL + bytes + LF)` of every file in the pack directory. Re-hash a downloaded pack with the same recipe to verify integrity.

## Purpose

Planning, research and brownfield analysis: the planner and researcher profiles, the retrospective facilitator, situational assessment, legacy triage, spikes and the planning templates.

A built-in-level core bundle, carved out of `built-in` by #73 and aggregated by it since 3.0.0 (ADR 2026-11-11-1, amendment 2026-11-11). It builds on `architecture`, `foundation`.

**Depends on:** `01M75PCTDT75M19ZMXHRES4CSJ ==2.0.0`, `01M75HSYR9S9KPA372PHGT0EX3 ==1.0.0`

## Artifact inventory

| Kind | Count |
| --- | --- |
| `tactics` | 1 |
| `styleguides` | 1 |
| `paradigms` | 1 |
| `procedures` | 5 |
| `agent_profiles` | 3 |
| `drg` | 1 |
| **Total files** | **17** |

### Full listing

<details>
<summary><code>tactics</code> (1)</summary>

- `analysis/analysis-extract-before-interpret.tactic.yaml`

</details>

<details>
<summary><code>styleguides</code> (1)</summary>

- `planning-and-tracking.styleguide.yaml`

</details>

<details>
<summary><code>paradigms</code> (1)</summary>

- `brownfield-onboarding.paradigm.yaml`

</details>

<details>
<summary><code>procedures</code> (5)</summary>

- `domain-aware-decision-interview.procedure.yaml`
- `issue-triage-state-machine.procedure.yaml`
- `legacy-codebase-triage.procedure.yaml`
- `situational-assessment.procedure.yaml`
- `spike-timebox-policy.procedure.yaml`

</details>

<details>
<summary><code>agent_profiles</code> (3)</summary>

- `planner-priti.agent.yaml`
- `researcher-robbie.agent.yaml`
- `retrospective-facilitator.agent.yaml`

</details>

<details>
<summary><code>drg</code> (1)</summary>

- `fragment.yaml`

</details>

## Validation

Reported by the charter pack schemas (`scripts/ci/validate_pack_schemas.py`): **passing**.

- Errors: 0
