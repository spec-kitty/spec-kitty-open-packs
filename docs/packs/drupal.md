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
- **Declared version:** `2.2.0`
- **Content checksum (sha256):** `ec967f48bbf1f231c28de16f070cbf79ccd8cff126bedc28799d3edbf19eeed7`
- **Checksum recipe:** sha256 over the sorted `(relative-path + NUL + bytes + LF)` of every file in the pack directory. Re-hash a downloaded pack with the same recipe to verify integrity.

## Purpose

The Drupal stack: the Drupal Dries profile, Drupal conventions, security and performance guidance, and review checks.

**Depends on:** [`foundation`](foundation.md) `>=3.2,<4`, [`testing`](testing.md) `>=2.0,<4`

## Artifact inventory

| Kind | Count |
| --- | --- |
| `styleguides` | 2 |
| `toolguides` | 2 |
| `anti_patterns` | 14 |
| `agent_profiles` | 1 |
| `drg` | 1 |
| **Total files** | **23** |

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
<summary><code>anti_patterns</code> (14)</summary>

- `business-logic-in-the-module-file.anti-pattern.yaml`
- `calling-removed-entity-loaders.anti-pattern.yaml`
- `configuration-stored-in-state.anti-pattern.yaml`
- `credentials-in-version-control.anti-pattern.yaml`
- `entity-query-without-an-explicit-access-check.anti-pattern.yaml`
- `fetching-services-via-drupal-inside-a-class.anti-pattern.yaml`
- `hardcoded-ids-and-paths.anti-pattern.yaml`
- `markup-for-untrusted-text.anti-pattern.yaml`
- `raw-sql-instead-of-entity-query.anti-pattern.yaml`
- `reading-superglobals-instead-of-the-injected-request.anti-pattern.yaml`
- `render-array-without-cache-metadata.anti-pattern.yaml`
- `sprawling-form-alter.anti-pattern.yaml`
- `twig-raw-filter-on-user-input.anti-pattern.yaml`
- `views-data-without-table-aliases.anti-pattern.yaml`

</details>

<details>
<summary><code>agent_profiles</code> (1)</summary>

- `drupal-dries.agent.yaml`

</details>

<details>
<summary><code>drg</code> (1)</summary>

- `fragment.yaml`

</details>
