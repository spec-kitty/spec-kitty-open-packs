# Rust Review Checks

## Overview

These are the automated checks a reviewer runs, or verifies the implementer ran, before approving a
Rust change. Each one catches a different class of defect, and none replaces another. This guide
covers workspace-wide checks through Cargo and its common extensions. It does not cover
framework-specific linting, benchmarking or release publishing.

## When to use

- Before approving any pull request that touches `*.rs`, `Cargo.toml` or `Cargo.lock`.
- Before handing work to review, as the implementer's self-check.
- When a dependency is added or upgraded: run the supply-chain section even if no code changed.

## Setup

```bash
rustup component add rustfmt clippy
cargo install --locked cargo-deny cargo-audit cargo-hack cargo-semver-checks cargo-mutants
rustup toolchain install nightly --component miri   # only for crates with unsafe code
```

Pin tool versions in CI, for example `cargo install --locked cargo-deny@<version>`. A newer Clippy
or rustfmt can change verdicts on unchanged code.

## Usage

Run the checks cheapest first, and stop at the first failure:

1. `cargo fmt --all --check`. Is the formatting clean?
2. `cargo clippy --workspace --all-targets --all-features -- -D warnings`. Is it lint-clean?
3. `cargo test --workspace --all-features`. Do the unit, integration and doc tests pass?
4. `RUSTDOCFLAGS="-D warnings" cargo doc --workspace --all-features --no-deps`. Do the docs build without broken
   links?
5. `cargo deny check`. Is the change free of known advisories, banned licences and unexpected
   sources? `cargo audit` covers advisories only. Use it as a fallback where there is no `deny.toml`.
6. `cargo hack check --feature-powerset --no-dev-deps`. Does every feature combination compile?
   Needed only when the crate has features. Add `cargo hack check --rust-version` to check the
   declared MSRV.
7. `cargo semver-checks`. Only for published library crates.
8. `cargo +nightly miri test`. Only for crates with `unsafe` code.
9. `cargo mutants`. Optional and costly; run it on critical modules.

Feed the first failure back to the implementer. Do not run expensive checks while cheap ones are red.

## Formatting

`cargo fmt --all --check` enforces rustfmt's layout, including a `rustfmt.toml` if the repository has
one, so that diffs show logic rather than whitespace. **Review signal:** unformatted code means the
implementer skipped the local gate.

## Linting

`cargo clippy --workspace --all-targets --all-features -- -D warnings` runs Clippy over library, binary, test,
bench and example targets, with warnings as errors.

**What the default lints catch:** `len() == 0` instead of `is_empty()`, `&Vec<T>` parameters,
redundant closures, large enum variants, suspicious arithmetic and many correctness bugs.

Default Clippy does **not** police the `rust-conventions` rules on panics, docs and unsafe. Opt in
through `[workspace.lints.clippy]`, with `[lints] workspace = true` in each member crate (without
it the workspace table is ignored):

- `unwrap_used` and `expect_used`, with `allow-unwrap-in-tests = true` and `allow-expect-in-tests = true` in
  `clippy.toml`; an invariant `expect` outside tests carries `#[expect(clippy::expect_used, reason = "...")]`;
- `missing_errors_doc` and `missing_panics_doc`;
- `needless_pass_by_value`;
- `undocumented_unsafe_blocks`;
- `allow_attributes_without_reason` and `allow_attributes`, so suppressions use `#[expect]` with a reason.

**Review signal:** every new `#[allow(clippy::...)]` or `#[expect(...)]` needs a stated reason. A
crate-wide `#![allow]` added in the diff needs a strong justification. Projects can enable
`clippy::pedantic` selectively in the same `[workspace.lints.clippy]` table.

## Tests

`cargo test --workspace --all-features` runs unit tests (`#[cfg(test)]`), integration tests
(`tests/`) and doc-tests. `cargo nextest run` is a faster runner but **does not run doc-tests**. Pair
it with `cargo test --doc`.

**Review signal:** new behaviour with no test, a test that asserts nothing observable, or a
`#[ignore]` added without a linked reason.

## Documentation

`RUSTDOCFLAGS="-D warnings" cargo doc --workspace --all-features --no-deps` fails on broken intra-doc links and on missing docs
where `#![warn(missing_docs)]` is set.

**Review signal:** a public fallible function without an `# Errors` section, or a panicking one
without `# Panics`.

## Supply chain

`cargo deny check` reads `deny.toml` and checks:

- advisories (RustSec);
- licences against an allow-list;
- banned or duplicate crates;
- crate sources (registries and git).

`cargo audit` checks `Cargo.lock` against the RustSec advisory database only.

**Review signal:** a new dependency without a stated reason, a git or path dependency in a published
crate, or a new licence family.

## Unsafe code

For crates with `unsafe`, `cargo +nightly miri test` runs the tests under Miri. Miri detects
undefined behaviour such as out-of-bounds access, use-after-free, invalid alignment and data races.

Miri runs isolated by default: filesystem access and wall-clock time (`SystemTime`) fail, host
environment variables are absent, and `Instant` runs on a virtual clock.
Use `MIRIFLAGS=-Zmiri-disable-isolation`, or mark those tests `#[cfg_attr(miri, ignore)]`.

**Review signal:** an `unsafe` block without a `// SAFETY:` comment, or `unsafe` that a safe API
could replace.

## API stability

`cargo semver-checks` compares the public API with the last published version and reports breaking
changes that the version bump does not reflect. Run it for library crates published to a registry.

## Mutation testing

`cargo mutants` mutates the code and checks whether the tests notice. Surviving mutants point at
assertions that are too weak to pin the behaviour. Scope it with `--file` or `-p` on critical
modules; a full-workspace run is slow.

## Cautions

- Run Clippy and tests with `--all-features`, otherwise feature-gated code is never checked. Run
  `cargo hack` for combinations that `--all-features` cannot reach, such as mutually exclusive
  features.
- Clippy and rustfmt verdicts change between toolchains. Pin the toolchain with
  `rust-toolchain.toml` so that CI and local runs agree.
- `-D warnings` on a moving toolchain can turn a green main red with no code change. Bump the
  toolchain deliberately, in its own commit.
- Doc-tests compile as external users of the crate; in edition 2024 they are merged into one binary
  unless marked `standalone_crate`. A doc-test that only compiles (`no_run`) checks less than one
  that runs.

## Known limitations

- `cargo deny` and `cargo audit` know only published advisories. They say nothing about unreported
  vulnerabilities or malicious code.
- Miri needs nightly, is slow, and cannot execute most FFI or inline assembly.
- `cargo semver-checks` sees API-level breakage, not behavioural changes behind an unchanged
  signature.
- None of these checks judge whether the design is right. The `rust-conventions` styleguide and the
  reviewer do.

## References

- [The rustfmt book](https://rust-lang.github.io/rustfmt/)
- [Clippy documentation](https://doc.rust-lang.org/clippy/)
- [The rustdoc book](https://doc.rust-lang.org/rustdoc/)
- [cargo-deny](https://embarkstudios.github.io/cargo-deny/)
- [RustSec advisory database and cargo-audit](https://rustsec.org/)
- [cargo-hack](https://github.com/taiki-e/cargo-hack)
- [cargo-semver-checks](https://github.com/obi1kenobi/cargo-semver-checks)
- [Miri](https://github.com/rust-lang/miri)
- [cargo-mutants](https://mutants.rs/)
- [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/)
