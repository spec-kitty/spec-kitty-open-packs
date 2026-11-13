---
title: rust pack reference
description: "Generated reference for the rust Charter Pack: artifact inventory, per-kind counts, and content checksum."
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

# rust pack reference

> **Generated page — do not edit by hand.** This file is produced by `scripts/docs/gen_pack_reference.py` from the pack source. Hand edits are overwritten on regeneration, and the CI drift gate fails on any difference.

## Provenance & integrity

- **Pack directory:** `packs/rust`
- **Pack level:** `org`
- **Declared version:** `1.0.1`
- **Content checksum (sha256):** `bf88dcfa298964ed184c71e14dee14ca7e3ea5728bb74f44f441cda225e95dfc`
- **Checksum recipe:** sha256 over the sorted `(relative-path + NUL + bytes + LF)` of every file in the pack directory. Re-hash a downloaded pack with the same recipe to verify integrity.

## Purpose

Idiomatic Rust for any Rust codebase: domain values as validated types, typed errors, money that is
never a float, exhaustive matches, isolated `unsafe`, and a cheapest-first Cargo review gate.

An opt-in org stack pack with general-purpose Rust doctrine for teams that build in Rust under Spec
Kitty.

| Artifact | Kind | What it gives an agent |
| --- | --- | --- |
| `rust-conventions` | styleguide | How to write the code: validated newtypes, parsing at the boundary, `thiserror` in libraries and `anyhow` at binary edges, money as a decimal or a currency-carrying minor-units type, exhaustive matches, documented `unsafe`, `///` docs. Each rule comes with bad and good examples. |
| `rust-review-checks` | toolguide | What to run before approving: `cargo fmt`, `clippy -D warnings`, tests and doc-tests, `cargo doc`, `cargo deny` / `cargo audit`, and where they apply `cargo hack`, `cargo semver-checks`, Miri and `cargo mutants`. Cheapest first. |
| `rust-ruben` | agent profile | A Rust implementer that requires `rust-conventions` and self-reviews with `rust-review-checks`. |
| `rust` | preset | Puts the three above in force. |

**Depends on:** [`foundation`](foundation.md) `>=1.0,<2`, [`testing`](testing.md) `>=2.0,<3`

## Artifact inventory

| Kind | Count |
| --- | --- |
| `styleguides` | 1 |
| `toolguides` | 2 |
| `agent_profiles` | 1 |
| `drg` | 1 |
| `presets` | 1 |
| **Total files** | **9** |

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
