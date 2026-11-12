---
title: javascript pack reference
description: "Generated reference for the javascript Charter Pack: artifact inventory, per-kind counts, content checksum, and validation status."
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

# javascript pack reference

> **Generated page — do not edit by hand.** This file is produced by `scripts/docs/gen_pack_reference.py` from the pack source. Hand edits are overwritten on regeneration, and the CI drift gate fails on any difference.

## Provenance & integrity

- **Pack directory:** `packs/javascript`
- **Declared version:** `2.0.0`
- **Content checksum (sha256):** `d9ac0faeea72ce74519dc9c12d473fd2e177000bc01d316aa7e3e75f1540af4b`
- **Checksum recipe:** sha256 over the sorted `(relative-path + NUL + bytes + LF)` of every file in the pack directory. Re-hash a downloaded pack with the same recipe to verify integrity.

## Purpose

The JavaScript and web stack: Node, frontend and design profiles, TypeScript, HTML and CSS conventions, atomic design, supply-chain and mutation tooling.

**Depends on:** `01M75HSYR9S9KPA372PHGT0EX3 >=1.0,<2`, `01M75PCTC6HS38NX8HJGT26VTP >=2.0,<3`

## Artifact inventory

| Kind | Count |
| --- | --- |
| `tactics` | 4 |
| `styleguides` | 3 |
| `toolguides` | 4 |
| `paradigms` | 1 |
| `agent_profiles` | 3 |
| `drg` | 1 |
| **Total files** | **18** |

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

## Validation

Reported by the charter pack schemas (`scripts/ci/validate_pack_schemas.py`): **passing**.

- Errors: 0
