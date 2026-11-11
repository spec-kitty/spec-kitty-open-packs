---
title: built-in pack reference
description: "Generated reference for the built-in Charter Pack: artifact inventory, per-kind counts, content checksum, and validation status."
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

# built-in pack reference

> **Generated page — do not edit by hand.** This file is produced by `scripts/docs/gen_pack_reference.py` from the pack source. Hand edits are overwritten on regeneration, and the CI drift gate fails on any difference.

## Provenance & integrity

- **Pack directory:** `packs/built-in`
- **Declared version:** `3.0.0`
- **Content checksum (sha256):** `03834ca7051f278e879015bf0f1dc8ec517e4e34f619cfb0e483fb24858fe569`
- **Checksum recipe:** sha256 over the sorted `(relative-path + NUL + bytes + LF)` of every file in the pack directory. Re-hash a downloaded pack with the same recipe to verify integrity.

## Purpose

The **built-in** pack is Spec Kitty's default distribution. Since #73 it is a *distribution pack*
(charter ADR-0048 decision 12): it holds no artifacts of its own and aggregates its six members, `foundation`, `writing`, `testing`, `refactoring`, `architecture` and
`planning-analysis`, through `depends_on`, pinned exactly and released in lockstep (decision 17). It
keeps the `default` and `minimal` presets and declares the fallback profile.

Built-in is the aggregate of the general-purpose open-packs: the foundation basics, writing
doctrine, and the testing, refactoring, architecture and planning-analysis bundles. Each member is a
built-in-level pack, so it depends only on built-in-level packs (decision 7). The stacks (`python`,
`javascript`, `drupal`, `java`), `pack-authoring` and the topical and process packs (`qa`,
`event-driven`, `spdd`, `cave-kitty`, `internal`) stay opt-in at org level (decision 14).

It has no `parent_pack` (it is the root of every lineage chain).

**Depends on:** `01M75HSYR9S9KPA372PHGT0EX3 ==1.0.0`, `01M75HSYS69RYRFPB4WCC5AC9D ==1.0.0`, `01M75PCTC6HS38NX8HJGT26VTP ==2.0.0`, `01M75PCTD0V3AFZA9EAXDJ894D ==2.0.0`, `01M75PCTDT75M19ZMXHRES4CSJ ==2.0.0`, `01M75PCTEKGDXQW59TGSFQQ9QT ==2.0.0`

## Artifact inventory

| Kind | Count |
| --- | --- |
| `presets` | 2 |
| **Total files** | **5** |

### Full listing

<details>
<summary><code>presets</code> (2)</summary>

- `default.yaml`
- `minimal.yaml`

</details>

## Validation

Reported by the charter pack schemas (`scripts/ci/validate_pack_schemas.py`): **passing**.

- Errors: 0
