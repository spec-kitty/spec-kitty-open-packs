---
title: spdd pack reference
description: "Generated reference for the spdd Charter Pack: artifact inventory, per-kind counts, and content checksum."
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

# spdd pack reference

> **Generated page — do not edit by hand.** This file is produced by `scripts/docs/gen_pack_reference.py` from the pack source. Hand edits are overwritten on regeneration, and the CI drift gate fails on any difference.

## Provenance & integrity

- **Pack directory:** `packs/spdd`
- **Pack level:** `org`
- **Declared version:** `3.0.1`
- **Content checksum (sha256):** `89fe105c6a09bce0fe626f6370f1c8aa9e7eb0a03cf214b863da72f32919c100`
- **Checksum recipe:** sha256 over the sorted `(relative-path + NUL + bytes + LF)` of every file in the pack directory. Re-hash a downloaded pack with the same recipe to verify integrity.

## Purpose

Structured-Prompt-Driven Development (SPDD) treats structured prompts and
REASONS canvases as governed change-intent and decision-boundary artifacts.
This opt-in org pack holds the SPDD paradigm, its directive, the REASONS canvas
fill/review tactics and writing styleguide, and prompt enhancements for the
`software-dev` specify, plan, tasks, implement and review steps. Activating its `spdd`
preset selects the doctrine and all five step enhancements together.

**Depends on:** [`architecture`](architecture.md) `>=2.0,<3`, [`foundation`](foundation.md) `>=1.0,<2`

## Artifact inventory

| Kind | Count |
| --- | --- |
| `directives` | 1 |
| `tactics` | 2 |
| `styleguides` | 1 |
| `paradigms` | 1 |
| `drg` | 1 |
| `missions` | 10 |
| `presets` | 1 |
| **Total files** | **20** |

### Full listing

<details>
<summary><code>directives</code> (1)</summary>

- `038-structured-prompt-boundary.directive.yaml`

</details>

<details>
<summary><code>tactics</code> (2)</summary>

- `reasons-canvas-fill.tactic.yaml`
- `reasons-canvas-review.tactic.yaml`

</details>

<details>
<summary><code>styleguides</code> (1)</summary>

- `reasons-canvas-writing.styleguide.yaml`

</details>

<details>
<summary><code>paradigms</code> (1)</summary>

- `structured-prompt-driven-development.paradigm.yaml`

</details>

<details>
<summary><code>drg</code> (1)</summary>

- `fragment.yaml`

</details>

<details>
<summary><code>missions</code> (10)</summary>

- `software-dev/enhancements/spdd-implement.prompt-fragment.md`
- `software-dev/enhancements/spdd-implement.step-enhancement.yaml`
- `software-dev/enhancements/spdd-plan.prompt-fragment.md`
- `software-dev/enhancements/spdd-plan.step-enhancement.yaml`
- `software-dev/enhancements/spdd-review.prompt-fragment.md`
- `software-dev/enhancements/spdd-review.step-enhancement.yaml`
- `software-dev/enhancements/spdd-specify.prompt-fragment.md`
- `software-dev/enhancements/spdd-specify.step-enhancement.yaml`
- `software-dev/enhancements/spdd-tasks.prompt-fragment.md`
- `software-dev/enhancements/spdd-tasks.step-enhancement.yaml`

</details>

<details>
<summary><code>presets</code> (1)</summary>

- `spdd.yaml`

</details>
