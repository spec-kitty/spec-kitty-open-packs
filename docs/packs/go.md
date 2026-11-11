---
title: go pack reference
description: "Generated reference for the go Charter Pack: artifact inventory, per-kind counts, content checksum, and validation status."
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

# go pack reference

> **Generated page — do not edit by hand.** This file is produced by `scripts/docs/gen_pack_reference.py` from the pack source. Hand edits are overwritten on regeneration, and the CI drift gate fails on any difference.

## Provenance & integrity

- **Pack directory:** `packs/go`
- **Declared version:** `1.0.0`
- **Content checksum (sha256):** `97c89c91e858b946204bd6b7edcccf3b4aff761a99fe67f484cde181acd2b089`
- **Checksum recipe:** sha256 over the sorted `(relative-path + NUL + bytes + LF)` of every file in the pack directory. Re-hash a downloaded pack with the same recipe to verify integrity.

## Purpose

Idiomatic Go for any Go codebase: validated typed constants, wrapped errors matched with
`errors.Is`/`errors.As`, context first, explicit dependencies instead of package globals, money that
is never `float64`, owned goroutines, and a cheapest-first review gate.

This opt-in org stack pack holds the `go-conventions` styleguide, the `go-review-checks` toolguide
and the `go-gwen` implementer profile, which requires the conventions. Activating its `go` preset
puts all three in force; the pack's org charter activates nothing on its own.

**Depends on:** `01M75HSYR9S9KPA372PHGT0EX3 >=1.0,<2`, `01M75PCTC6HS38NX8HJGT26VTP >=2.0,<3`

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

- `go-conventions.styleguide.yaml`

</details>

<details>
<summary><code>toolguides</code> (2)</summary>

- `go-review-checks.guide.md`
- `go-review-checks.toolguide.yaml`

</details>

<details>
<summary><code>agent_profiles</code> (1)</summary>

- `go-gwen.agent.yaml`

</details>

<details>
<summary><code>drg</code> (1)</summary>

- `fragment.yaml`

</details>

<details>
<summary><code>presets</code> (1)</summary>

- `go.yaml`

</details>

## Validation

Reported by the charter pack schemas (`scripts/ci/validate_pack_schemas.py`): **passing**.

- Errors: 0
