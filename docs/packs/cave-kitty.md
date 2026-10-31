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
- **Content checksum (sha256):** `6fa65f45ff63bd72e038451ac1f1f07a6cf82eb832cce4aeb4bb4f492721c3ec`
- **Checksum recipe:** sha256 over the sorted `(relative-path + NUL + bytes)` of every file in the pack directory. Re-hash a downloaded pack with the same recipe to verify integrity.

## Purpose

_No `purpose` is declared in this pack's `pack.yaml`, so none is shown here (the generator never fabricates one). See the pack's `README.md` and the [Packs hub](index.md) for authored context._

## Artifact inventory

| Kind | Count |
| --- | --- |
| `directives` | 1 |
| `styleguides` | 1 |
| `drg` | 1 |
| `missions` | 9 |
| **Total files** | **15** |

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

Reported by `spec-kitty charter pack validate --json`: **passing (`ok: true`)**.

- Errors: 0

Advisories are non-blocking and vary by validator version; run `spec-kitty charter pack validate <dir> --json` for the current list.
