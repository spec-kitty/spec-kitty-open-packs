# Provenance

This pack is **not** a port. It was authored fresh in this repository for
[#191](https://github.com/spec-kitty/spec-kitty-open-packs/issues/191) and is distributed under the
repository's MIT licence.

## Seed

The starting point was the Rust idioms listed in
[`spec-kitty/charter-cobol-migrations`](https://github.com/spec-kitty/charter-cobol-migrations) at
commit `2c4ce2a` (2026-11-02), in `charter-packs/rust/README.md`. That pack is about migrating
legacy systems to Rust. What this pack takes from it is only the **target-language idioms**: closed
sets as enums or validated newtypes rather than raw integers, an explicit decimal strategy for money,
and domain types kept apart from storage layout.

Not taken: its migration doctrine (characterization before translation, golden masters, parity
harnesses, slice porting, copybook disposition), its worked examples and its evidence catalog. These
belong to legacy-migration work, not to a general Rust pack. **No text was copied.** The styleguide,
toolguide, guide, profile and preset are written from scratch in Spec Kitty's doctrine schema.

## Seed contradictions and how they were resolved

| Seed | Problem | This pack |
| --- | --- | --- |
| Money via "`rust_decimal` vs bignum", and elsewhere in the seed family "i64-cents newtype". | Three representations with no rule for choosing. A bare `i64` loses the currency and the scale, and it wraps silently on overflow in release builds. | A decimal type when the scale varies or the arithmetic divides or applies rates. Otherwise a newtype over integer minor units that **carries its currency**, with `checked_*` arithmetic. Never a float, never a bare integer. |
| Condition names become "explicit Rust enums or validated newtypes, never raw ints". | It was framed for one legacy construct. | A general rule: closed sets are enums (matched exhaustively), and open validated values are newtypes with a fallible constructor. |
| An application-specific environment struct threaded through calls. | It named one port. | A general rule: parse at the boundary and pass typed values and explicit dependencies inward. |

## Other sources consulted

Consulted as references, not copied: the [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/),
the [Clippy documentation](https://doc.rust-lang.org/clippy/), the
[rustdoc book](https://doc.rust-lang.org/rustdoc/), and the documentation of `thiserror`, `anyhow`,
`rust_decimal`, `cargo-deny`, `cargo-audit`, `cargo-hack`, `cargo-semver-checks`, Miri and
`cargo-mutants`.

## Verification at authoring time

The std-only code examples (newtype, money, enum parsing, exhaustive match, the `unsafe` example)
compile and pass `cargo clippy --all-targets -- -D warnings` on rustc 1.97.0. Examples that use
external crates were checked against those crates' documented APIs.
