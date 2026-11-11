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
- **Declared version:** `2.0.0`
- **Content checksum (sha256):** `9105e5862884c23ab1bdd368507f02034daf684de284c3ad2ce539285e943bb5`
- **Checksum recipe:** sha256 over the sorted `(relative-path + NUL + bytes + LF)` of every file in the pack directory. Re-hash a downloaded pack with the same recipe to verify integrity.

## Purpose

The **built-in** pack is Spec Kitty's default distribution. Since #73 it is a *distribution pack*
(charter ADR-0048 decision 12): it holds no artifacts of its own and aggregates its two members,
`foundation` and `writing`, through `depends_on`, pinned exactly and released in lockstep
(decision 17). It keeps the `default` and `minimal` presets and declares the fallback profile.

Specialist doctrine (testing, refactoring, architecture, planning and analysis, adversarial review,
pack authoring, and the python, javascript, drupal and java stacks) ships as opt-in org bundles
that build on `foundation`; built-in does not aggregate them (decision 14).

It has no `parent_pack` (it is the root of every lineage chain).

**Depends on:** `01M75HSYR9S9KPA372PHGT0EX3 ==1.0.0`, `01M75HSYS69RYRFPB4WCC5AC9D ==1.0.0`

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
