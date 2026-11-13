---
title: java pack reference
description: "Generated reference for the java Charter Pack: artifact inventory, per-kind counts, and content checksum."
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

# java pack reference

> **Generated page — do not edit by hand.** This file is produced by `scripts/docs/gen_pack_reference.py` from the pack source. Hand edits are overwritten on regeneration, and the CI drift gate fails on any difference.

## Provenance & integrity

- **Pack directory:** `packs/java`
- **Pack level:** `org`
- **Declared version:** `2.1.1`
- **Content checksum (sha256):** `54f52b19ce84f112f7991b51e6710a7424b0d32e0f2844e90cc1ef5fdf9ab2c0`
- **Checksum recipe:** sha256 over the sorted `(relative-path + NUL + bytes + LF)` of every file in the pack directory. Re-hash a downloaded pack with the same recipe to verify integrity.

## Purpose

The Java stack: the Java Jenny profile, Java conventions, Maven review checks and Java supply-chain guidance. The supply-chain guidance also applies to Kotlin on Maven or Gradle.

**Depends on:** [`foundation`](foundation.md) `>=1.0,<2`, [`testing`](testing.md) `>=2.0,<3`

## Artifact inventory

| Kind | Count |
| --- | --- |
| `styleguides` | 1 |
| `toolguides` | 4 |
| `agent_profiles` | 1 |
| `drg` | 1 |
| **Total files** | **10** |

### Full listing

<details>
<summary><code>styleguides</code> (1)</summary>

- `java-conventions.styleguide.yaml`

</details>

<details>
<summary><code>toolguides</code> (4)</summary>

- `java-supply-chain.guide.md`
- `java-supply-chain.toolguide.yaml`
- `maven-review-checks.guide.md`
- `maven-review-checks.toolguide.yaml`

</details>

<details>
<summary><code>agent_profiles</code> (1)</summary>

- `java-jenny.agent.yaml`

</details>

<details>
<summary><code>drg</code> (1)</summary>

- `fragment.yaml`

</details>
