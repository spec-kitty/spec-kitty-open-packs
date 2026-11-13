---
title: drupal pack reference
description: "Generated reference for the drupal Charter Pack: artifact inventory, per-kind counts, and content checksum."
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

# drupal pack reference

> **Generated page — do not edit by hand.** This file is produced by `scripts/docs/gen_pack_reference.py` from the pack source. Hand edits are overwritten on regeneration, and the CI drift gate fails on any difference.

## Provenance & integrity

- **Pack directory:** `packs/drupal`
- **Pack level:** `org`
- **Declared version:** `2.0.1`
- **Content checksum (sha256):** `bd77522152660814c57bb667d98c1a578f32c5dbc11874355db2834cbd0f0dea`
- **Checksum recipe:** sha256 over the sorted `(relative-path + NUL + bytes + LF)` of every file in the pack directory. Re-hash a downloaded pack with the same recipe to verify integrity.

## Purpose

The Drupal stack: the Drupal Dries profile, Drupal conventions, security and performance guidance, and review checks.

**Depends on:** [`foundation`](foundation.md) `>=1.0,<2`, [`testing`](testing.md) `>=2.0,<3`

## Artifact inventory

| Kind | Count |
| --- | --- |
| `styleguides` | 2 |
| `toolguides` | 2 |
| `agent_profiles` | 1 |
| `drg` | 1 |
| **Total files** | **9** |

### Full listing

<details>
<summary><code>styleguides</code> (2)</summary>

- `drupal-conventions.styleguide.yaml`
- `drupal-security-performance.styleguide.yaml`

</details>

<details>
<summary><code>toolguides</code> (2)</summary>

- `drupal-review-checks.guide.md`
- `drupal-review-checks.toolguide.yaml`

</details>

<details>
<summary><code>agent_profiles</code> (1)</summary>

- `drupal-dries.agent.yaml`

</details>

<details>
<summary><code>drg</code> (1)</summary>

- `fragment.yaml`

</details>
