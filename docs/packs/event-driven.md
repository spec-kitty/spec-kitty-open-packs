---
title: event-driven pack reference
description: "Generated reference for the event-driven Charter Pack: artifact inventory, per-kind counts, content checksum, and validation status."
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

# event-driven pack reference

> **Generated page — do not edit by hand.** This file is produced by `scripts/docs/gen_pack_reference.py` from the pack source. Hand edits are overwritten on regeneration, and the CI drift gate fails on any difference.

## Provenance & integrity

- **Pack directory:** `packs/event-driven`
- **Declared version:** `1.0.0`
- **Content checksum (sha256):** `4a34f1c856134933223d1b2ab2e90df43770146532e970ec5d797214ad840a88`
- **Checksum recipe:** sha256 over the sorted `(relative-path + NUL + bytes)` of every file in the pack directory. Re-hash a downloaded pack with the same recipe to verify integrity.

## Purpose

_No `purpose` is declared for a pack: the `pack.yaml` schema has no such field. See the pack's `README.md` and the [Packs hub](index.md) for authored context._

**Depends on:** `01ARWG13C000000000000000FG >=1.0,<2`

## Artifact inventory

| Kind | Count |
| --- | --- |
| `directives` | 6 |
| `tactics` | 4 |
| `styleguides` | 1 |
| `paradigms` | 1 |
| `assets` | 2 |
| `glossary_packs` | 1 |
| `drg` | 1 |
| `presets` | 1 |
| **Total files** | **20** |

### Full listing

<details>
<summary><code>directives</code> (6)</summary>

- `evd-001-events-carry-schema-version.directive.yaml`
- `evd-002-one-canonical-writer-per-stream.directive.yaml`
- `evd-003-events-are-immutable-past-tense-facts.directive.yaml`
- `evd-004-producers-emit-latest-consumers-declare-versions.directive.yaml`
- `evd-005-side-effects-live-in-consumers.directive.yaml`
- `evd-006-share-only-published-event-contracts.directive.yaml`

</details>

<details>
<summary><code>tactics</code> (4)</summary>

- `evd-event-bridge-port.tactic.yaml`
- `evd-event-versioning-and-upcasting.tactic.yaml`
- `evd-idempotent-consumer.tactic.yaml`
- `evd-projection-replay.tactic.yaml`

</details>

<details>
<summary><code>styleguides</code> (1)</summary>

- `evd-event-naming-and-payload.styleguide.yaml`

</details>

<details>
<summary><code>paradigms</code> (1)</summary>

- `evd-event-sourced-design.paradigm.yaml`

</details>

<details>
<summary><code>assets</code> (2)</summary>

- `event_sourced_lane_board.md`
- `event_sourced_lane_board.md.asset.yaml`

</details>

<details>
<summary><code>glossary_packs</code> (1)</summary>

- `evd-glossary.glossary-pack.yaml`

</details>

<details>
<summary><code>drg</code> (1)</summary>

- `fragment.yaml`

</details>

<details>
<summary><code>presets</code> (1)</summary>

- `event-driven.yaml`

</details>

## Validation

Validation status unavailable — the charter pack schemas could not be used (cannot fetch https://raw.githubusercontent.com/spec-kitty/spec-kitty-charter/85c20fa148bd9cb1517e9e95d3d13c3718201dd4/contracts/packs/file-kinds.yaml: <HTTPError 404: 'Not Found'>). Run `python3 scripts/ci/validate_pack_schemas.py <dir>` locally.
