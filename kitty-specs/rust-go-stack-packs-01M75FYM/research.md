# Research: Rust and Go stack packs

Seed read: spec-kitty/charter-cobol-migrations at `2c4ce2a` (2026-11-02):
`charter-packs/rust/README.md` and `charter-packs/go/README.md`. The repository is a read-only clone.
Its packs are COBOL-to-Rust and COBOL-to-Go *migration* packs, so most of their content
(characterization, parity harnesses, copybook disposition) is out of scope here (spec NFR-002). Only
the target-language idioms carry over, and they are re-authored in general terms.

## R-01 — `built-in` does not aggregate `rust` or `go`

- **Decision**: The packs are opt-in org packs. `built-in` is not changed.
- **Rationale**: #73 and charter ADR-0048 d14 / ADR-0053 q1 make stack packs opt-in at org level.
  `java`'s planned aggregation into `built-in` exists to keep existing consumers. `rust` and `go` are
  new, so no consumer loses anything. If `built-in` aggregated them while they depended on
  `foundation`, `built-in`'s scope would grow for every consumer.
- **Alternatives**: Aggregate into `built-in`. The operator rejected it on 2026-11-11.

## R-02 — Seed contradictions and how they are resolved

| Seed statement | Problem | Resolution in this pack |
| --- | --- | --- |
| Go: money as "`shopspring/decimal.Decimal` or i64-cents newtype". Rust: money via "`rust_decimal` vs bignum". | Three representations, with no rule for choosing. A bare `i64` cents value loses the currency and the scale, and it overflows silently in release builds. | One rule for both languages: use a decimal type when the scale varies or a calculation divides or applies rates. Use a newtype over integer minor units that **carries its currency** when the scale is fixed and the arithmetic is additive. Never a float, never a bare integer. Overflow is checked. Rounding is explicit, with a named mode. |
| Go: "typed constants + `map[byte]bool` validated sets". | Ties the set to `byte` and makes membership a separate, forgettable lookup. | A named type plus constants, and a `Valid()` / `Parse` function that is the only way in from outside. Unknown values are rejected at the boundary. A `switch` with a `default` that errors. |
| Go: "`goto` reserved for error-cleanup of legacy shape". | It framed `goto` as a porting device. | General rule: prefer `defer` for cleanup. `goto` is allowed only for a forward jump to a cleanup label in one function, never backwards, and never into a block. |
| Rust: "88-level ... explicit Rust enums or validated newtypes, never raw ints". | It was COBOL-specific. | General rule: closed sets are enums, and open, validated values are newtypes with a fallible constructor. |
| Rust/Go: `&Env{...}` / `AcasEnv` context struct. | It named a specific port. | General rule: thread an explicit environment or context struct, with no package-level mutable globals. |

## R-03 — Error crates (Rust)

- **Decision**: Libraries define their error enums with `thiserror`. Binaries and application edges
  use `anyhow` (or `eyre`) with `.context()`. A library's public API never returns `anyhow::Error`.
- **Rationale**: Callers of a library need to match on the cause. An application needs context and
  a report.
- **Alternatives**: Hand-written `impl Error`, which is fine but more ceremony. It is mentioned as
  equivalent.

## R-04 — Go error-check tooling

- **Decision**: `gofmt -l`, `go vet ./...`, `staticcheck ./...` *or* `golangci-lint run` (which
  bundles staticcheck), `go test -race ./...`, and `govulncheck ./...`. Optionally `go mod verify` and
  `go mod tidy -diff` (Go 1.23+).
- **Rationale**: These are the community standard, cheapest first. `-race` catches the data races
  that review misses.

## R-05 — Rust review tooling

- **Decision**: `cargo fmt --check`; `cargo clippy --all-targets --all-features -- -D warnings`;
  `cargo test --all-features`; `cargo doc --no-deps` with `RUSTDOCFLAGS=-D warnings`; `cargo deny
  check` (licenses, bans, advisories, sources) or `cargo audit`. Optionally `cargo +nightly miri
  test` for `unsafe` code, `cargo semver-checks` for published libraries and `cargo mutants`.
- **Rationale**: These are the standard ecosystem tools, cheapest first.

## R-06 — Specialist profile identity

- **Decision**: `rust-ruben` ("Rust Ruben") and `go-gwen` ("Go Gwen"). Each has `role: implementer`
  and `applies_to_languages` set to its language. It `requires` its conventions styleguide (#131) and
  `suggests` its review-checks toolguide. Once `foundation` exists, it `specializes_from`
  `foundation::agent_profile:implementer-ivan` and takes directive and tactic references like the
  built-in language specialists (`java-jenny`, `python-pedro`).
- **Rationale**: This follows the built-in alliterative naming and the #131 rule. The operator
  confirmed it on 2026-11-11.

## R-07 — Manifest

- **Decision**: No `pack-manifest.yaml` for org packs.
- **Rationale**: Only `built-in` carries one. `validate_pack_schemas.py` checks a manifest only
  "when it has one". #182's completeness guard is not implemented yet, and it targets built-in's
  manifest drift. If #73's `foundation` work introduces an org-pack manifest convention before this
  merges, the packs adopt it on rebase (spec C-004).

## R-08 — Charter service check locally

- **Finding**: The pinned charter repository is public and readable, so the schema pre-check runs
  locally with `CHARTER_CONTRACT_DIR`. Building the service jar (`./gradlew :deployable:bootJar`)
  was refused by the session's permission classifier as execution of external code. Per the
  operator brief, this is not worked around: the service gate is proven in CI.
- **Mitigation**: The guide layout rules were read from the charter source (`GuideBlock`,
  `GuideMarkdown`), so the guides are authored to the service's rules up front.
