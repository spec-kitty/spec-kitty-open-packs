---
title: java pack reference
description: "Generated reference for the java Charter Pack: artifact inventory, per-kind counts, content checksum, and validation status."
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

# java pack reference

> **Generated page — do not edit by hand.** This file is produced by `scripts/docs/gen_pack_reference.py` from the pack source. Hand edits are overwritten on regeneration, and the CI drift gate fails on any difference.

## Provenance & integrity

- **Pack directory:** `packs/java`
- **Declared version:** `1.0.0`
- **Content checksum (sha256):** `4b185f4f6a0a3a1d3da4248f17731f694540634d1822169b9cecf0c37c245c43`
- **Checksum recipe:** sha256 over the sorted `(relative-path + NUL + bytes + LF)` of every file in the pack directory. Re-hash a downloaded pack with the same recipe to verify integrity.

## Purpose

The Java stack: the Java Jenny profile, Java conventions, Maven review checks and Java supply-chain guidance.

An opt-in, org-level bundle carved out of `built-in` by #73 (charter ADR-0048 decision 14). It builds on `foundation`, `testing`.

**Depends on:** `01M75HSYR9S9KPA372PHGT0EX3 >=1.0,<2`, `01M75PCTC6HS38NX8HJGT26VTP >=1.0,<2`

## Artifact inventory

| Kind | Count |
| --- | --- |
| `styleguides` | 1 |
| `toolguides` | 4 |
| `agent_profiles` | 1 |
| `drg` | 1 |
| **Total files** | **12** |

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

## Validation

Reported by the charter pack schemas (`scripts/ci/validate_pack_schemas.py`): **passing**.

- Errors: 0
