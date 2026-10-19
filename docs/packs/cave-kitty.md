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
- **Content checksum (sha256):** `b7c2c6f3b5fdda53313b75ce06e0cfe2e7c7310d54a76208e672d21f53107beb`
- **Checksum recipe:** sha256 over the sorted `(relative-path + NUL + bytes)` of every file in the pack directory. Re-hash a downloaded pack with the same recipe to verify integrity.

## Purpose

_No `purpose` is declared in this pack's `pack.yaml`, so none is shown here (the generator never fabricates one). See the pack's `README.md` and the [Packs hub](index.md) for authored context._

## Artifact inventory

| Kind | Count |
| --- | --- |
| `directives` | 1 |
| `styleguides` | 1 |
| `drg` | 1 |
| `mission_types` | 2 |
| `missions` | 11 |
| **Total files** | **19** |

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
<summary><code>mission_types</code> (2)</summary>

- `cave-dev.yaml`
- `cave-dev/governance-profile.yaml`

</details>

<details>
<summary><code>missions</code> (11)</summary>

- `cave-dev/command-templates/accept.md`
- `cave-dev/command-templates/analyze.md`
- `cave-dev/command-templates/discovery.md`
- `cave-dev/command-templates/implement.md`
- `cave-dev/command-templates/plan.md`
- `cave-dev/command-templates/review.md`
- `cave-dev/command-templates/specify.md`
- `cave-dev/command-templates/tasks.md`
- `cave-dev/expected-artifacts.yaml`
- `cave-dev/mission-runtime.yaml`
- `cave-dev/mission.yaml`

</details>

## Validation

Reported by `spec-kitty charter pack validate --json`: **passing (`ok: true`)**.

- Errors: 0

Advisories are non-blocking and vary by validator version; run `spec-kitty charter pack validate <dir> --json` for the current list.
