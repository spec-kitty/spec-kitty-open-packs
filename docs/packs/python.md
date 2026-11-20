---
title: python pack reference
description: "Generated reference for the python Charter Pack: artifact inventory, per-kind counts, and content checksum."
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

# python pack reference

> **Generated page — do not edit by hand.** This file is produced by `scripts/docs/gen_pack_reference.py` from the pack source. Hand edits are overwritten on regeneration, and the CI drift gate fails on any difference.

## Provenance & integrity

- **Pack directory:** `packs/python`
- **Pack level:** `org`
- **Declared version:** `2.2.0`
- **Content checksum (sha256):** `55e23d247da10e0a2fef2a3b0a46e0f71fbbfefc94583042fb22f3a6cda638b4`
- **Checksum recipe:** sha256 over the sorted `(relative-path + NUL + bytes + LF)` of every file in the pack directory. Re-hash a downloaded pack with the same recipe to verify integrity.

## Purpose

The Python stack: the Python Pedro profile, Python conventions, review checks, supply-chain and mutation tooling.

**Depends on:** [`foundation`](foundation.md) `>=3.2,<4`, [`testing`](testing.md) `>=2.0,<4`

## Artifact inventory

| Kind | Count |
| --- | --- |
| `styleguides` | 1 |
| `toolguides` | 6 |
| `agent_profiles` | 1 |
| `drg` | 1 |
| **Total files** | **12** |

### Full listing

<details>
<summary><code>styleguides</code> (1)</summary>

- `python-conventions.styleguide.yaml`

</details>

<details>
<summary><code>toolguides</code> (6)</summary>

- `python-mutation-tools.guide.md`
- `python-mutation-tools.toolguide.yaml`
- `python-review-checks.guide.md`
- `python-review-checks.toolguide.yaml`
- `python-supply-chain.guide.md`
- `python-supply-chain.toolguide.yaml`

</details>

<details>
<summary><code>agent_profiles</code> (1)</summary>

- `python-pedro.agent.yaml`

</details>

<details>
<summary><code>drg</code> (1)</summary>

- `fragment.yaml`

</details>
