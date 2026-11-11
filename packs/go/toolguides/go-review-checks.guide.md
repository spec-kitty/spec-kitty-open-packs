# Go Review Checks

## Overview

These are the automated checks a reviewer runs, or verifies the implementer ran, before approving a
Go change. Each one catches a different class of defect, and none replaces another. The guide covers
module-wide checks through the `go` command and the standard ecosystem analysers. It does not cover
framework-specific linting, benchmarks or release builds.

## When to use

- Before approving any pull request that touches `*.go`, `go.mod` or `go.sum`.
- Before handing work to review, as the implementer's self-check.
- When a dependency is added or upgraded: run the supply-chain section even if no code changed.

## Setup

```bash
go install golang.org/x/tools/cmd/goimports@latest
go install honnef.co/go/tools/cmd/staticcheck@latest
go install golang.org/x/vuln/cmd/govulncheck@latest
# or golangci-lint, which bundles staticcheck and many other analysers
# (the project recommends its binary install script over go install):
go install github.com/golangci/golangci-lint/v2/cmd/golangci-lint@latest
```

Replace `@latest` with a pinned version in CI, so that a new analyser release cannot turn unchanged
code red. On Go 1.24 or later, a `tool` directive in `go.mod` pins these tools with the module.

## Usage

Run the checks cheapest first, and stop at the first failure:

1. `test -z "$(gofmt -l $(git ls-files '*.go' ':!vendor'))"`. Is the formatting clean? `gofmt -l`
   lists unformatted files and exits 0 even when it finds some, so test for empty output. This
   form leaves `vendor/` out.
2. `go vet ./...`. Is the code free of suspicious constructs?
3. `staticcheck ./...`, or `golangci-lint run`. Does static analysis pass?
4. `go test -race -count=1 ./...`. Do the tests pass with no data race?
5. `govulncheck ./...`. Are no reachable known vulnerabilities present?
6. `go mod verify` and `go mod tidy -diff` (Go 1.23+). Are the modules intact and the manifest
   tidy?
7. `go test -fuzz='^FuzzXxx$' -fuzztime=30s ./pkg`. Run it on changed parsers and decoders.

Feed the first failure back to the implementer. Do not run expensive checks while cheap ones are red.

## Formatting

`gofmt -l` lists every file whose formatting differs from gofmt's (run it as in Usage step 1, which
leaves `vendor/` out). `goimports` also fixes and
groups imports. **Review signal:** any listed file means the implementer skipped the local gate.

## Vet

`go vet ./...` runs the standard analysers. They catch:

- `Printf` format and argument mismatches;
- copied locks (`copylocks`);
- unreachable code;
- struct tags that do not parse;
- a context's cancel function that is never called (`lostcancel`);
- misuse of `errors.As` with a non-pointer.

`go test` runs a subset of vet automatically. Run the full set explicitly.

## Static analysis

`staticcheck ./...` finds bugs (`SA`), simplifications (`S`), style problems (`ST`), quick fixes (`QF`)
and unused code (`U1000`). `golangci-lint run` runs staticcheck alongside other linters configured in
`.golangci.yml`, such as `errcheck`, `errorlint`, `bodyclose` and `contextcheck`.

**Review signal:** every new `//nolint` or `//lint:ignore` needs a named check and a reason. A
blanket `//nolint` is not acceptable.

## Tests

`go test -race -count=1 ./...` runs every package's tests with the race detector, bypassing the test
cache.

**What it catches:** regressions, and data races that only show under concurrency. A race report is
a defect even if the tests pass.

**Review signal:** new behaviour without a table case, a `t.Skip` without a reason, or a test that
sleeps instead of synchronising.

## Fuzzing

For parsers, decoders and validators, add a `FuzzXxx` target with a seed corpus. During review, run
`go test -fuzz='^FuzzXxx$' -fuzztime=30s` on the changed package. Failing inputs are saved under
`testdata/fuzz/` and become regression cases.

## Supply chain

`govulncheck ./...` reports known vulnerabilities from the Go vulnerability database, and only those
whose vulnerable functions the code actually calls. `go mod verify` checks that downloaded modules
match `go.sum`. `go mod tidy -diff` shows `go.mod` / `go.sum` drift without writing anything.

**Review signal:** a new dependency without a stated reason, a `replace` directive pointing at a
fork or a local path, or a `go.sum` change with no `go.mod` change.

## Cautions

- `-race` needs cgo (`CGO_ENABLED=1` and a C toolchain) on Linux and Windows. It typically raises
  memory use 5–10x and run time 2–20x. Keep it in CI even if local runs skip it.
- Loop variables are per-iteration only when `go.mod` declares `go 1.22` or later. An older `go` line
  built with a new toolchain still shares them across closures and goroutines.
- `-count=1` defeats the test cache on purpose. Without it, an unchanged package reports a cached
  pass.
- golangci-lint configurations drift between versions. Pin the version and keep `.golangci.yml` in
  the repository.
- `gofmt -l` exits 0 even when it lists files. A CI step must test for empty output.
- Build tags hide files from every check. Run the checks with each tag set that ships, such as
  `-tags integration`.

## Known limitations

- govulncheck knows only published advisories, and it cannot see reachability through reflection or
  plugins.
- The race detector finds only races that the tests actually execute.
- None of these checks judge whether the design is right. The `go-conventions` styleguide and the
  reviewer do.

## References

- [Effective Go](https://go.dev/doc/effective_go)
- [Go Code Review Comments](https://go.dev/wiki/CodeReviewComments)
- [go vet analysers](https://pkg.go.dev/cmd/vet)
- [Staticcheck](https://staticcheck.dev/)
- [golangci-lint](https://golangci-lint.run/)
- [Data race detector](https://go.dev/doc/articles/race_detector)
- [Go fuzzing](https://go.dev/doc/security/fuzz/)
- [govulncheck](https://go.dev/doc/security/vuln/)
