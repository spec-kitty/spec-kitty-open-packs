---
title: built-in pack reference
description: "Generated reference for the built-in Charter Pack: artifact inventory, per-kind counts, and content checksum."
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

# built-in pack reference

> **Generated page — do not edit by hand.** This file is produced by `scripts/docs/gen_pack_reference.py` from the pack source. Hand edits are overwritten on regeneration, and the CI drift gate fails on any difference.

## Provenance & integrity

- **Pack directory:** `packs/built-in`
- **Pack level:** `built-in`
- **Declared version:** `3.0.0`
- **Content checksum (sha256):** `060c1207d1d8dc2f3b86ec160c3500963801ae1b3f5dc1f18a624c9d4f359016`
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

**Depends on:** [`foundation`](foundation.md) `==1.0.0`, [`writing`](writing.md) `==1.0.0`, [`testing`](testing.md) `==2.0.0`, [`refactoring`](refactoring.md) `==2.0.0`, [`architecture`](architecture.md) `==2.0.0`, [`planning-analysis`](planning-analysis.md) `==2.0.0`

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
