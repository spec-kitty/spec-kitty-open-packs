---
title: pack-authoring pack reference
description: "Generated reference for the pack-authoring Charter Pack: artifact inventory, per-kind counts, content checksum, and validation status."
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

# pack-authoring pack reference

> **Generated page — do not edit by hand.** This file is produced by `scripts/docs/gen_pack_reference.py` from the pack source. Hand edits are overwritten on regeneration, and the CI drift gate fails on any difference.

## Provenance & integrity

- **Pack directory:** `packs/pack-authoring`
- **Declared version:** `1.0.0`
- **Content checksum (sha256):** `d70d267c8387c89ce63226172f22499ddc5d14d196a64dc3e33d42dcf8f17f9f`
- **Checksum recipe:** sha256 over the sorted `(relative-path + NUL + bytes + LF)` of every file in the pack directory. Re-hash a downloaded pack with the same recipe to verify integrity.

## Purpose

Doctrine and pack authoring: the Doctrine Daphne profile, onboarding external agents into a pack, deployable skill authoring and the migration-to-charter procedure.

An opt-in, org-level bundle carved out of `built-in` by #73 (charter ADR-0048 decision 14). It builds on `foundation`, `writing`.

**Depends on:** `01M75HSYR9S9KPA372PHGT0EX3 >=1.0,<2`, `01M75HSYS69RYRFPB4WCC5AC9D >=1.0,<2`

## Artifact inventory

| Kind | Count |
| --- | --- |
| `styleguides` | 1 |
| `procedures` | 2 |
| `agent_profiles` | 1 |
| `drg` | 1 |
| **Total files** | **10** |

### Full listing

<details>
<summary><code>styleguides</code> (1)</summary>

- `deployable-skill-authoring.styleguide.yaml`

</details>

<details>
<summary><code>procedures</code> (2)</summary>

- `migrate-project-guidance-to-spec-kitty-charter.procedure.yaml`
- `onboard-external-agent-to-pack.procedure.yaml`

</details>

<details>
<summary><code>agent_profiles</code> (1)</summary>

- `doctrine-daphne.agent.yaml`

</details>

<details>
<summary><code>drg</code> (1)</summary>

- `fragment.yaml`

</details>

## Validation

Reported by the charter pack schemas (`scripts/ci/validate_pack_schemas.py`): **passing**.

- Errors: 0
