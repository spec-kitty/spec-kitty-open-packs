---
title: event-driven pack reference
description: "Generated reference for the event-driven doctrine pack: artifact inventory, per-kind counts, content checksum, and validation status."
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
- **Content checksum (sha256):** `489379ea88330e5a7bfa298fc57b5b83025f4ea2bc12672f42b970720dd0205b`
- **Checksum recipe:** sha256 over the sorted `(relative-path + NUL + bytes)` of every file in the pack directory. Re-hash a downloaded pack with the same recipe to verify integrity.

## Purpose

_No `purpose` is declared in this pack's `pack.yaml`, so none is shown here (the generator never fabricates one). See the pack's `README.md` and the [Packs hub](index.md) for authored context._

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
| **Total files** | **19** |

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

Reported by `spec-kitty charter pack validate --json`: **passing (`ok: true`)**.

- Errors: 0

Advisories are non-blocking and vary by validator version; run `spec-kitty charter pack validate <dir> --json` for the current list.
