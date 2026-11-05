---
title: cave-kitty pack reference
description: "Generated reference for the cave-kitty Charter Pack: artifact inventory, per-kind counts, content checksum, and validation status."
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

# cave-kitty pack reference

> **Generated page — do not edit by hand.** This file is produced by `scripts/docs/gen_pack_reference.py` from the pack source. Hand edits are overwritten on regeneration, and the CI drift gate fails on any difference.

## Provenance & integrity

- **Pack directory:** `packs/cave-kitty`
- **Declared version:** `1.0.0`
- **Content checksum (sha256):** `a572af92aa4969ae656f0359618dfae0809239d62113b12ed61fa0f93dd24c6f`
- **Checksum recipe:** sha256 over the sorted `(relative-path + NUL + bytes)` of every file in the pack directory. Re-hash a downloaded pack with the same recipe to verify integrity.

## Purpose

_No `purpose` is declared for a pack: the `pack.yaml` schema has no such field. See the pack's `README.md` and the [Packs hub](index.md) for authored context._

**Depends on:** `01ARWG13C000000000000000FG >=1.0,<2`

## Artifact inventory

| Kind | Count |
| --- | --- |
| `directives` | 1 |
| `styleguides` | 1 |
| `drg` | 1 |
| `missions` | 9 |
| **Total files** | **16** |

### Full listing

<details>
<summary><code>directives</code> (1)</summary>

- `cave-001-terse-output.directive.yaml`

</details>

<details>
<summary><code>styleguides</code> (1)</summary>

- `cave-sty-001-communication.styleguide.yaml`

</details>

<details>
<summary><code>drg</code> (1)</summary>

- `fragment.yaml`

</details>

<details>
<summary><code>missions</code> (9)</summary>

- `cave-dev/cave-dev.mission-type.yaml`
- `cave-dev/steps/accept.prompt.md`
- `cave-dev/steps/analyze.prompt.md`
- `cave-dev/steps/discovery.prompt.md`
- `cave-dev/steps/implement.prompt.md`
- `cave-dev/steps/plan.prompt.md`
- `cave-dev/steps/review.prompt.md`
- `cave-dev/steps/specify.prompt.md`
- `cave-dev/steps/tasks.prompt.md`

</details>

## Validation

Validation status unavailable — the charter pack schemas could not be used (cannot fetch https://raw.githubusercontent.com/spec-kitty/spec-kitty-charter/85c20fa148bd9cb1517e9e95d3d13c3718201dd4/contracts/packs/file-kinds.yaml: <HTTPError 404: 'Not Found'>). Run `python3 scripts/ci/validate_pack_schemas.py <dir>` locally.
