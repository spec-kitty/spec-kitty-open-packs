---
title: python pack reference
description: "Generated reference for the python Charter Pack: artifact inventory, per-kind counts, content checksum, and validation status."
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

# python pack reference

> **Generated page — do not edit by hand.** This file is produced by `scripts/docs/gen_pack_reference.py` from the pack source. Hand edits are overwritten on regeneration, and the CI drift gate fails on any difference.

## Provenance & integrity

- **Pack directory:** `packs/python`
- **Declared version:** `1.0.0`
- **Content checksum (sha256):** `34fa557331941cbb049b9f50f0d486dcc8cf67d092d6127a3117b4986a805782`
- **Checksum recipe:** sha256 over the sorted `(relative-path + NUL + bytes + LF)` of every file in the pack directory. Re-hash a downloaded pack with the same recipe to verify integrity.

## Purpose

The Python stack: the Python Pedro profile, Python conventions, review checks, supply-chain and mutation tooling.

An opt-in, org-level bundle carved out of `built-in` by #73 (charter ADR-0048 decision 14). It builds on `foundation`, `testing`.

**Depends on:** `01M75HSYR9S9KPA372PHGT0EX3 >=1.0,<2`, `01M75PCTC6HS38NX8HJGT26VTP >=2.0,<3`

## Artifact inventory

| Kind | Count |
| --- | --- |
| `styleguides` | 1 |
| `toolguides` | 6 |
| `agent_profiles` | 1 |
| `drg` | 1 |
| **Total files** | **14** |

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

## Validation

Reported by the charter pack schemas (`scripts/ci/validate_pack_schemas.py`): **passing**.

- Errors: 0
