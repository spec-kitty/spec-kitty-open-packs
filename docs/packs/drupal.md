---
title: drupal pack reference
description: "Generated reference for the drupal Charter Pack: artifact inventory, per-kind counts, content checksum, and validation status."
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

# drupal pack reference

> **Generated page — do not edit by hand.** This file is produced by `scripts/docs/gen_pack_reference.py` from the pack source. Hand edits are overwritten on regeneration, and the CI drift gate fails on any difference.

## Provenance & integrity

- **Pack directory:** `packs/drupal`
- **Declared version:** `2.0.0`
- **Content checksum (sha256):** `3fb65d328f244c21dd9233956d80ba427d650ea0f2890683c64b965b0d7618ee`
- **Checksum recipe:** sha256 over the sorted `(relative-path + NUL + bytes + LF)` of every file in the pack directory. Re-hash a downloaded pack with the same recipe to verify integrity.

## Purpose

The Drupal stack: the Drupal Dries profile, Drupal conventions, security and performance guidance, and review checks.

- **Contents:** 2 styleguides, 1 agent profile, 1 toolguide.
- **Agent profiles:** `drupal-dries`.

**Depends on:** `01M75HSYR9S9KPA372PHGT0EX3 >=1.0,<2`, `01M75PCTC6HS38NX8HJGT26VTP >=2.0,<3`

## Artifact inventory

| Kind | Count |
| --- | --- |
| `styleguides` | 2 |
| `toolguides` | 2 |
| `agent_profiles` | 1 |
| `drg` | 1 |
| **Total files** | **8** |

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

## Validation

Reported by the charter pack schemas (`scripts/ci/validate_pack_schemas.py`): **passing**.

- Errors: 0
