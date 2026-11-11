---
work_package_id: WP01
title: Rust doctrine content
dependencies: []
requirement_refs:
- FR-002
- FR-003
- FR-004
- NFR-001
- NFR-002
- C-001
planning_base_branch: feat/rust-go-packs
merge_target_branch: feat/rust-go-packs
branch_strategy: Planning artifacts for this mission were generated on feat/rust-go-packs. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/rust-go-packs unless the human explicitly redirects the landing branch.
subtasks:
- T001
- T002
- T003
- T004
- T005
history:
- at: '2026-11-11T15:00:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: implementer-ivan
authoritative_surface: packs/rust/
create_intent:
- packs/rust/styleguides/rust-conventions.styleguide.yaml
- packs/rust/toolguides/rust-review-checks.toolguide.yaml
- packs/rust/toolguides/rust-review-checks.guide.md
- packs/rust/agent_profiles/rust-ruben.agent.yaml
- packs/rust/presets/rust.yaml
execution_mode: code_change
owned_files:
- packs/rust/styleguides/**
- packs/rust/toolguides/**
- packs/rust/agent_profiles/**
- packs/rust/presets/**
role: implementer
tags: []
tracker_refs: []
---

# Work Package Prompt: WP01 – Rust doctrine content

## ⚡ Do This First: Load Agent Profile

Before reading anything else, load the assigned profile with the `/spk-charter-profile-load` skill:
`implementer-ivan`. If the skill is not available, run `spec-kitty agent profile show implementer-ivan`.

## Objective

Author the Rust pack's doctrine. It must be real, general-purpose and idiomatic: useful to any Rust
team, not a migration aid, and not a stub. Spec FR-002 to FR-004.

## Branch Strategy

- Planning/base branch `feat/rust-go-packs`; final merge target `feat/rust-go-packs`, which reaches
  `main` by pull request.
- Implement with `spec-kitty agent action implement WP01 --agent claude --mission rust-go-stack-packs-01M75FYM`
  and trust the workspace path it prints. Lanes come from `lanes.json`.

## Context

Read first: `spec.md`, `research.md` (R-02 seed contradictions, R-03 error crates, R-05 tooling,
R-06 profile), `data-model.md`. Exemplars of shape (not content):
`packs/built-in/styleguides/python-conventions.styleguide.yaml`,
`packs/built-in/toolguides/python-review-checks.*`, `packs/built-in/agent_profiles/java-jenny.agent.yaml`.
Schemas: charter `contracts/packs/schemas/{styleguide,toolguide,toolguide-guide,agent-profile,preset}.schema.json`.

Hard rules:
- No text copied from charter-cobol-migrations (C-001). No COBOL, ACAS or port vocabulary (NFR-002).
- Every principle has `{name, description}` with `description` ≤ 255 characters. Put longer
  reasoning in a same-named `patterns` entry (the charter #474 convention).
- Every pattern and anti-pattern carries a `bad_example` and a `good_example` that would compile in
  spirit: use real crate APIs, and no pseudo-code that a Rust reviewer would reject (NFR-001).
- No reference to any artifact outside `packs/rust` in these files. Relations to `foundation` live
  in the DRG (WP05).

## Subtasks

### T001 — `styleguides/rust-conventions.styleguide.yaml`

`id: rust-conventions`, `schema_version: "1.0"`, `title: Rust Conventions Styleguide`, `scope: code`,
`applies_to_languages: [rust]`.

Principles. Cover at least:

1. **Make invalid states unrepresentable.** Newtypes with private fields and a fallible constructor
   (`TryFrom` / `parse`) for bounded or validated values. Enums for closed sets.
2. **Raw bytes stay at the edge.** `[u8; N]` / `&[u8]` only for unvalidated bytes at I/O
   boundaries. Parse into domain types once, at the boundary ("parse, don't validate").
3. **Typed errors.** Libraries use `thiserror` enums with a variant per cause the caller can act on.
   Binaries use `anyhow` with `.context()`. Never `anyhow::Error` in a library's public API.
4. **No panics on recoverable paths.** `?` over `unwrap` / `expect`. `expect` only for an
   invariant, with its reason in the message. No `panic!` for input errors.
5. **Money is never a float.** Use a decimal type (`rust_decimal`) when the scale varies or the
   arithmetic divides or applies rates. Otherwise use a currency-carrying newtype over integer minor
   units, with `checked_*` arithmetic and explicit rounding. Never a bare `i64`.
6. **Enums over magic numbers and booleans.** An exhaustive `match`, with no `_ =>` wildcard on
   domain enums, so that adding a variant is a compile error.
7. **Domain types do not depend on storage or wire formats.** No `serde` / `sqlx` derives leaking
   format rules into the core; map at the adapter.
8. **Borrow by default.** Take `&str` / `&[T]` / `impl AsRef` in parameters. Return owned data. Clone
   deliberately, not to silence the borrow checker.
9. **`unsafe` is isolated and justified.** Every `unsafe` block carries a `// SAFETY:` comment and
   sits behind a safe API. `#![forbid(unsafe_code)]` where none is needed.
10. **Public items are documented.** `///` on every public item, with an `# Errors` section on
    fallible functions and `# Panics` where one can panic. `#![warn(missing_docs)]` for libraries.
11. **Clippy-clean and formatted.** `cargo fmt`, `clippy -D warnings`. An `#[allow]` carries a reason
    (`#[expect(..., reason = "...")]` on Rust 1.81+).
12. **Tests sit beside the code.** Unit tests in `#[cfg(test)] mod tests`, integration tests in
    `tests/`, doc-tests on public examples. Property tests (`proptest`) for parsers and arithmetic.

Patterns (each with good and bad examples): Validated Newtype; Parse at the Boundary; Library Error
Enum with thiserror; Application Errors with anyhow context; Money as Minor Units with Currency (and
the decimal alternative); Exhaustive Match on Domain Enums; Borrowed Parameters; Documented Unsafe
Block.

Anti-patterns: Float Money; Bare Integer Codes (magic numbers); Stringly-Typed Domain;
`unwrap()` on Input; Wildcard Match on a Domain Enum; Boolean Parameters (use an enum); Clone to
Silence the Borrow Checker; `anyhow` in a Library API.

`tooling`: formatter `cargo fmt (rustfmt)`, linter `cargo clippy --all-targets --all-features -- -D warnings`,
test runner `cargo test (cargo nextest optional)`, docs `cargo doc --no-deps`,
supply chain `cargo deny check / cargo audit`. Check the schema for the allowed `tooling` shape; it
may be a free map of strings.

`quality_test`: one question a reviewer can answer from the code alone. For example: can a caller
construct an invalid value of any domain type without going through a fallible constructor?

### T002 — `toolguides/rust-review-checks.toolguide.yaml`

`id: rust-review-checks`, `schema_version: '1.0'`, `tool: cargo`, `title: Rust Review Checks`,
`guide_path: rust-review-checks.guide.md`, a `summary`, `commands` (cargo-fmt, cargo-clippy,
cargo-test, cargo-doc, cargo-deny, cargo-audit, cargo-semver-checks, cargo-miri, cargo-mutants),
`applies_to_languages: [rust]`.

### T003 — `toolguides/rust-review-checks.guide.md`

The layout is enforced by the charter service (`GuideMarkdown`):

- `# Rust Review Checks` as the H1 (it must equal the title exactly);
- **no text before the first `##`**;
- the fixed blocks in this order, any of them optional except Overview: `## Overview`,
  `## When to use`, `## Setup`, `## Usage`;
- then freeform `##` sections;
- then `## Cautions`, `## Known limitations`, `## References`.

No freeform heading may be a case-variant of a fixed heading.

Content:

- **Overview**: what the checks cover.
- **Setup**: the components (`rustup component add rustfmt clippy`) and the `cargo install`
  commands for `cargo-deny`, `cargo-audit` and `cargo-semver-checks`.
- **Usage**: the ordered, cheapest-first checklist.
- **Freeform sections**, one per category (Formatting, Linting, Tests, Documentation, Supply
  chain, Unsafe code, API stability, Mutation testing), each giving the command, what it catches
  and the review signal.
- **Cautions**: `--all-features`, feature combinations (`cargo hack`), and clippy lint-level drift
  between toolchains.
- **Known limitations**: miri needs nightly and does not support FFI; deny/audit cover only known
  advisories.
- **References**: a list of links to the official docs.

Feature-gated code paths deserve their own note.

### T004 — `agent_profiles/rust-ruben.agent.yaml`

Mirror `java-jenny`'s shape: `profile-id: rust-ruben`, `name: Rust Ruben`, a `description`,
`schema-version: "1.0"`, `role: implementer`, `applies_to_languages: [rust]`, `capabilities`,
`routing-priority: 80`, `purpose`, `specialization` (primary focus, secondary awareness, avoidance
boundary, success definition), `collaboration`, `mode-defaults`, `initialization-declaration`,
`specialization-context` (languages, frameworks such as tokio, serde, thiserror, anyhow, proptest,
file-patterns `**/*.rs`, `**/Cargo.toml`, domain keywords) and `self-review-protocol` (fmt, clippy,
test, doc, deny, acceptance and locality steps).

References: `styleguide-references: [{id: rust-conventions, rationale}]` and
`toolguide-references: [{id: rust-review-checks, rationale}]` only. **No** `directive-references` or
`tactic-references` yet (WP05 adds the relations as DRG edges).

### T005 — `presets/rust.yaml`

`schema_version: "1.0"`, `id: rust`, a `description`, and these activations:

- `activated_styleguides: [{id: rust-conventions}]`;
- `activated_toolguides: [{id: rust-review-checks}]`;
- `activated_agent_profiles: [{id: rust-ruben}]`.

Check the item shape against `preset.schema.json`.

## Validation

`packs/rust` validates only once WP03 adds `pack.yaml`. Until then, schema-check the files directly:
create a scratch copy with a temporary `pack.yaml` in the scratchpad and run
`CHARTER_CONTRACT_DIR=... python3 scripts/ci/validate_pack_schemas.py <scratch>/rust`. Commit
nothing from the scratch copy.

## Definition of Done

- [ ] Five files exist and are schema-valid.
- [ ] ≥ 10 principles, ≥ 8 patterns, ≥ 8 anti-patterns, each with examples.
- [ ] `grep -riE 'cobol|acas|legacy port' packs/rust` finds nothing.
- [ ] Money guidance matches research R-02 exactly.

## Reviewer guidance

Read it as a senior Rust reviewer would. Would each example compile, apart from elided imports? Is
each rule current, idiomatic Rust (2021 / 2024 edition), and is nothing cargo-culted?
