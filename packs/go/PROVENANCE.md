# Provenance

This pack is **not** a port. It was authored fresh in this repository for
[#192](https://github.com/spec-kitty/spec-kitty-open-packs/issues/192) and is distributed under the
repository's MIT licence.

## Seed

The starting point was the draft Go idiom table in
[`spec-kitty/charter-cobol-migrations`](https://github.com/spec-kitty/charter-cobol-migrations) at
commit `2c4ce2a` (2026-11-02), in `charter-packs/go/README.md`. That draft is about migrating legacy
systems to Go. What this pack takes from it is only the **target-language idioms**: money never as
`float64`, typed constants with validated sets in place of enums, an explicit context struct instead
of global linkage, small functions with explicit state instead of fall-through flows, and `goto`
kept to cleanup.

Not taken: its migration mapping, its graduation checklist and its non-goals, which are specific to
porting one system. **No text was copied.** The styleguide, toolguide, guide, profile and preset are
written from scratch in Spec Kitty's doctrine schema.

## Seed contradictions and how they were resolved

| Seed | Problem | This pack |
| --- | --- | --- |
| Money as "`shopspring/decimal.Decimal` or i64-cents newtype". | Two representations with no rule for choosing. A bare `int64` cents value loses the currency and overflows silently. | A decimal type when the scale varies or the arithmetic divides or applies rates. Otherwise integer minor units in a type that **carries its currency**, with an overflow check. Never `float64`, never a bare integer. |
| "Typed constants + `map[byte]bool` validated sets". | It ties the set to `byte` and makes membership a separate lookup that callers can forget. A direct conversion such as `Status(n)` still accepts anything. | A named type with typed constants, an explicit zero-value `Unknown`, and a `Parse` function that is the only way in from outside and rejects unknown values. |
| "`goto` reserved for error-cleanup of legacy shape". | It framed `goto` as a porting device. | A general rule: `defer` for cleanup. A forward `goto` to a single cleanup label is acceptable only where `defer` cannot express the release order. Never backwards, never into a block. |
| A context struct "mirroring" another pack's environment type. | It named one port. | A general rule: no package-level mutable state; dependencies go in an explicit struct built in `main` or a constructor. `context.Context` stays a first parameter and is never stored in that struct. |

## Other sources consulted

Consulted as references, not copied: [Effective Go](https://go.dev/doc/effective_go),
[Go Code Review Comments](https://go.dev/wiki/CodeReviewComments), and the documentation of `go vet`,
Staticcheck, golangci-lint, the race detector, Go fuzzing, govulncheck and
`golang.org/x/sync/errgroup`.

## Verification at authoring time

The stdlib code examples (typed constants and parse, error wrapping and matching, the money type,
context-first request, defer cleanup with `errors.Join`, the mutex receiver and the table-driven
test) compile and pass `gofmt`, `go vet` and `go test -race` on go1.24.7. Examples that use external
modules (`errgroup`, `shopspring/decimal`) were checked against those modules' documented APIs.
