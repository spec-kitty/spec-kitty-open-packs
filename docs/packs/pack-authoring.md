---
title: pack-authoring pack reference
description: "Generated reference for the pack-authoring Charter Pack: artifact inventory, per-kind counts, and content checksum."
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

# pack-authoring pack reference

> **Generated page — do not edit by hand.** This file is produced by `scripts/docs/gen_pack_reference.py` from the pack source. Hand edits are overwritten on regeneration, and the CI drift gate fails on any difference.

## Provenance & integrity

- **Pack directory:** `packs/pack-authoring`
- **Pack level:** `org`
- **Declared version:** `1.0.1`
- **Content checksum (sha256):** `a7b107ff94128653647896375a216aa35dffbf1f904690e985f6a66a3bad9bd4`
- **Checksum recipe:** sha256 over the sorted `(relative-path + NUL + bytes + LF)` of every file in the pack directory. Re-hash a downloaded pack with the same recipe to verify integrity.

## Purpose

Doctrine and pack authoring: the Doctrine Daphne profile, onboarding external agents into a pack, deployable skill authoring, the voice doctrine instructions are written in, and the migration-to-charter procedure.

**Depends on:** [`foundation`](foundation.md) `>=1.0,<2`, [`writing`](writing.md) `>=1.0,<2`

## Artifact inventory

| Kind | Count |
| --- | --- |
| `styleguides` | 2 |
| `procedures` | 2 |
| `agent_profiles` | 1 |
| `drg` | 1 |
| **Total files** | **9** |

### Full listing

<details>
<summary><code>styleguides</code> (2)</summary>

- `deployable-skill-authoring.styleguide.yaml`
- `doctrine-instruction-voice.styleguide.yaml`

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
