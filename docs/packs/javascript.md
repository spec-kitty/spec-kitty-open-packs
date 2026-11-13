---
title: javascript pack reference
description: "Generated reference for the javascript Charter Pack: artifact inventory, per-kind counts, and content checksum."
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

# javascript pack reference

> **Generated page — do not edit by hand.** This file is produced by `scripts/docs/gen_pack_reference.py` from the pack source. Hand edits are overwritten on regeneration, and the CI drift gate fails on any difference.

## Provenance & integrity

- **Pack directory:** `packs/javascript`
- **Pack level:** `org`
- **Declared version:** `2.0.1`
- **Content checksum (sha256):** `9f638ccfdb5d05f65092c60555e84dd41283b654a207ac5c82866d0a9f98ea74`
- **Checksum recipe:** sha256 over the sorted `(relative-path + NUL + bytes + LF)` of every file in the pack directory. Re-hash a downloaded pack with the same recipe to verify integrity.

## Purpose

The JavaScript and web stack: Node, frontend and design profiles, TypeScript, HTML and CSS conventions, atomic design, supply-chain and mutation tooling.

**Depends on:** [`foundation`](foundation.md) `>=1.0,<2`, [`testing`](testing.md) `>=2.0,<3`

## Artifact inventory

| Kind | Count |
| --- | --- |
| `tactics` | 4 |
| `styleguides` | 3 |
| `toolguides` | 4 |
| `paradigms` | 1 |
| `agent_profiles` | 3 |
| `drg` | 1 |
| **Total files** | **19** |

### Full listing

<details>
<summary><code>tactics</code> (4)</summary>

- `architecture/atomic-design-review-checklist.tactic.yaml`
- `architecture/atomic-state-ownership.tactic.yaml`
- `architecture/compositional-stream-boundaries.tactic.yaml`
- `architecture/cross-cutting-state-via-store.tactic.yaml`

</details>

<details>
<summary><code>styleguides</code> (3)</summary>

- `css-conventions.styleguide.yaml`
- `html-conventions.styleguide.yaml`
- `typescript-conventions.styleguide.yaml`

</details>

<details>
<summary><code>toolguides</code> (4)</summary>

- `javascript-supply-chain.guide.md`
- `javascript-supply-chain.toolguide.yaml`
- `typescript-mutation-tools.guide.md`
- `typescript-mutation-tools.toolguide.yaml`

</details>

<details>
<summary><code>paradigms</code> (1)</summary>

- `atomic-design.paradigm.yaml`

</details>

<details>
<summary><code>agent_profiles</code> (3)</summary>

- `designer-dagmar.agent.yaml`
- `frontend-freddy.agent.yaml`
- `node-norris.agent.yaml`

</details>

<details>
<summary><code>drg</code> (1)</summary>

- `fragment.yaml`

</details>
