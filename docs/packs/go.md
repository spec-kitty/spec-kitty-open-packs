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
- **Content checksum (sha256):** `fa8269b6195a8049be50f4eb99b7219bc6fce948cbee17fb1eba1f4f4c1fdd8d`
- **Checksum recipe:** sha256 over the sorted `(relative-path + NUL + bytes + LF)` of every file in the pack directory. Re-hash a downloaded pack with the same recipe to verify integrity.

## Purpose

Idiomatic Go for any Go codebase: validated typed constants, wrapped errors matched with
`errors.Is`/`errors.As`, context first, explicit dependencies instead of package globals, money that
is never `float64`, owned goroutines, and a cheapest-first review gate.

An opt-in org stack pack with general-purpose Go doctrine for teams that build in Go under Spec Kitty.

| Artifact | Kind | What it gives an agent |
| --- | --- | --- |
| `go-conventions` | styleguide | How to write the code: typed constants with a validated parse, errors wrapped with `%w` and matched with `errors.Is`/`errors.As`, `context.Context` first, an explicit dependency struct instead of package globals, money as a decimal or minor units with its currency, `defer` for cleanup, owned goroutines, table-driven tests. Each rule comes with bad and good examples. |
| `go-review-checks` | toolguide | What to run before approving: `gofmt`, `go vet`, `staticcheck` or `golangci-lint`, `go test -race`, fuzzing, `govulncheck`, `go mod verify`. Cheapest first. |
| `go-gwen` | agent profile | A Go implementer that requires `go-conventions` and self-reviews with `go-review-checks`. |
| `go` | preset | Puts the three above in force. |

**Depends on:** `01M75HSYR9S9KPA372PHGT0EX3 >=1.0,<2`, `01M75PCTC6HS38NX8HJGT26VTP >=2.0,<3`

## Artifact inventory

| Kind | Count |
| --- | --- |
| `styleguides` | 1 |
| `toolguides` | 2 |
| `agent_profiles` | 1 |
| `drg` | 1 |
| `presets` | 1 |
| **Total files** | **8** |

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
