---
title: cave-kitty pack reference
description: "Generated reference for the cave-kitty Charter Pack: artifact inventory, per-kind counts, and content checksum."
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

# cave-kitty pack reference

> **Generated page — do not edit by hand.** This file is produced by `scripts/docs/gen_pack_reference.py` from the pack source. Hand edits are overwritten on regeneration, and the CI drift gate fails on any difference.

## Provenance & integrity

- **Pack directory:** `packs/cave-kitty`
- **Pack level:** `org`
- **Declared version:** `2.0.1`
- **Content checksum (sha256):** `df879021d8783166e6eed80dc7261945e96b9a4cee7907b8c3bf873a25f45676`
- **Checksum recipe:** sha256 over the sorted `(relative-path + NUL + bytes + LF)` of every file in the pack directory. Re-hash a downloaded pack with the same recipe to verify integrity.

## Purpose

An open Spec Kitty Charter Pack that makes an agent answer in a **compressed, token-saving
"caveman" voice** — outcome-first, filler cut — while keeping every payload and every negation
exact and restoring full sentences at a cliff edge.

**Depends on:** [`foundation`](foundation.md) `>=1.0,<2`

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
