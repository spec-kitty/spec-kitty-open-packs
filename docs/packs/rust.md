---
title: rust pack reference
description: "Generated reference for the rust Charter Pack: artifact inventory, per-kind counts, content checksum, and validation status."
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

# rust pack reference

> **Generated page — do not edit by hand.** This file is produced by `scripts/docs/gen_pack_reference.py` from the pack source. Hand edits are overwritten on regeneration, and the CI drift gate fails on any difference.

## Provenance & integrity

- **Pack directory:** `packs/rust`
- **Declared version:** `1.0.0`
- **Content checksum (sha256):** `5d9eab00f31a992ca557d26c57138dd9156d21f8bd1258c83e1fabe9c0c587c2`
- **Checksum recipe:** sha256 over the sorted `(relative-path + NUL + bytes + LF)` of every file in the pack directory. Re-hash a downloaded pack with the same recipe to verify integrity.

## Purpose

Idiomatic Rust for any Rust codebase: domain values as validated types, typed errors, money that is
never a float, exhaustive matches, isolated `unsafe`, and a cheapest-first Cargo review gate.

This opt-in org stack pack holds the `rust-conventions` styleguide, the `rust-review-checks`
toolguide and the `rust-ruben` implementer profile, which requires the conventions. Activating its
`rust` preset puts all three in force; the pack's org charter activates nothing on its own.

**Depends on:** `01M75HSYR9S9KPA372PHGT0EX3 >=1.0,<2`, `01M75PCTC6HS38NX8HJGT26VTP >=1.0,<2`

## Artifact inventory

| Kind | Count |
| --- | --- |
| `styleguides` | 1 |
| `toolguides` | 2 |
| `agent_profiles` | 1 |
| `drg` | 1 |
| `presets` | 1 |
| **Total files** | **11** |

### Full listing

<details>
<summary><code>styleguides</code> (1)</summary>

- `rust-conventions.styleguide.yaml`

</details>

<details>
<summary><code>toolguides</code> (2)</summary>

- `rust-review-checks.guide.md`
- `rust-review-checks.toolguide.yaml`

</details>

<details>
<summary><code>agent_profiles</code> (1)</summary>

- `rust-ruben.agent.yaml`

</details>

<details>
<summary><code>drg</code> (1)</summary>

- `fragment.yaml`

</details>

<details>
<summary><code>presets</code> (1)</summary>

- `rust.yaml`

</details>

## Validation

Reported by the charter pack schemas (`scripts/ci/validate_pack_schemas.py`): **passing**.

- Errors: 0
