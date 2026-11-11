---
work_package_id: WP02
title: Go doctrine content
dependencies: []
requirement_refs:
- FR-006
- FR-007
- FR-008
- NFR-001
- NFR-002
- C-001
planning_base_branch: feat/rust-go-packs
merge_target_branch: feat/rust-go-packs
branch_strategy: Planning artifacts for this mission were generated on feat/rust-go-packs. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/rust-go-packs unless the human explicitly redirects the landing branch.
subtasks:
- T006
- T007
- T008
- T009
- T010
history:
- at: '2026-11-11T15:00:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: implementer-ivan
authoritative_surface: packs/go/
create_intent:
- packs/go/styleguides/go-conventions.styleguide.yaml
- packs/go/toolguides/go-review-checks.toolguide.yaml
- packs/go/toolguides/go-review-checks.guide.md
- packs/go/agent_profiles/go-gwen.agent.yaml
- packs/go/presets/go.yaml
execution_mode: code_change
owned_files:
- packs/go/styleguides/**
- packs/go/toolguides/**
- packs/go/agent_profiles/**
- packs/go/presets/**
role: implementer
tags: []
tracker_refs: []
---

# Work Package Prompt: WP02 – Go doctrine content

## ⚡ Do This First: Load Agent Profile

Before reading anything else, load the assigned profile with the `/spk-charter-profile-load` skill:
`implementer-ivan`. If the skill is not available, run `spec-kitty agent profile show implementer-ivan`.

## Objective

Author the Go pack's doctrine: real, general-purpose, idiomatic Go. Spec FR-006 to FR-008.

## Branch Strategy

- Planning/base branch `feat/rust-go-packs`; final merge target `feat/rust-go-packs`, which reaches
  `main` by pull request.
- Implement with `spec-kitty agent action implement WP02 --agent claude --mission rust-go-stack-packs-01M75FYM`.

## Context

The same reading, hard rules and exemplars as WP01 (see `tasks/WP01-rust-doctrine.md` § Context),
applied to Go. Research R-02 (typed constants, `goto`, environment struct, money) and R-04 (tooling)
are binding.

## Subtasks

### T006 — `styleguides/go-conventions.styleguide.yaml`

`id: go-conventions`, `title: Go Conventions Styleguide`, `scope: code`, `applies_to_languages: [go]`.

Principles. Cover at least:

1. **Money is never `float64`.** Use a decimal type (for example `github.com/shopspring/decimal`, or
   `cockroachdb/apd` for strict contexts) when the scale varies or the arithmetic divides or applies
   rates. Otherwise use a named integer minor-units type carried with its currency, with an overflow
   check.
2. **Closed sets are typed constants plus validation.** `type Status uint8` with `const (...)`
   using `iota`, a `Valid()` method, and a `ParseStatus` that rejects unknown values. The zero value
   is either meaningful or an explicit `StatusUnknown`.
3. **Errors are values.** Wrap with `fmt.Errorf("...: %w", err)`. Match with `errors.Is` /
   `errors.As`, never by string comparison. Use sentinel errors or typed errors for causes a caller
   acts on. Handle each error once: either log it or return it.
4. **`context.Context` comes first.** It is the first parameter of every function that blocks, does
   I/O or crosses an API boundary. It is never stored in a struct, and never `nil`.
5. **No package-level mutable state.** Thread dependencies through an explicit struct (`type Env
   struct{...}` / constructor injection). Keep `init()` for registration only.
6. **Small functions, with explicit state.** Long fall-through flows become small functions over an
   explicit state type and a `switch`. Return early.
7. **`defer` for cleanup.** `goto` is acceptable only as a forward jump to a cleanup label in one
   function, never backwards, never into a block. Prefer `defer` and `errors.Join`.
8. **Accept interfaces, return structs.** Interfaces are small and defined at the consumer. Do not
   create an interface before there is a second implementation or a test seam.
9. **Every goroutine has an owner and an exit.** Whoever starts a goroutine guarantees it stops: use
   context cancellation, `errgroup`, or a closed channel. Use no unbounded fan-out.
10. **The zero value is useful, and copies are safe.** Keep the mutex next to what it guards. Do not
    copy a struct that holds a `sync.Mutex`.
11. **Doc comments and formatting.** Every exported identifier has a comment that starts with its
    name. Code is `gofmt`-clean. Package names are short and lower case, with no `util` / `common`.
12. **Table-driven tests.** Use `t.Run` subtests, `t.Parallel()` where safe, `testing/quick` or fuzz
    tests (`go test -fuzz`) for parsers, and `-race` in CI.

Patterns: Typed Constants with a Validated Parse; Wrapping and Matching Errors; Explicit Environment
Struct; Context-First Signature; Minor Units with Currency (and the decimal alternative); Defer-based
Cleanup (with the bounded `goto` case shown as acceptable); errgroup-Owned Goroutines; Table-Driven
Test.

Anti-patterns: float64 Money; Untyped iota Values Accepted Unchecked; Error String Matching;
Package-level Mutable Globals; Context Stored in a Struct; Fire-and-Forget Goroutine; Producer-side
Interface; Backward `goto` / Fall-through Flow.

`tooling`: gofmt / goimports, go vet, staticcheck or golangci-lint, go test -race, govulncheck.

### T007 — `toolguides/go-review-checks.toolguide.yaml`

`id: go-review-checks`, `tool: go`, `title: Go Review Checks`, `guide_path: go-review-checks.guide.md`,
a summary, `commands` (gofmt, goimports, go-vet, staticcheck, golangci-lint, go-test, govulncheck,
go-mod-verify), `applies_to_languages: [go]`.

### T008 — `toolguides/go-review-checks.guide.md`

The same layout rules as WP01 T003, with `# Go Review Checks` as the H1. Content:

- **Setup**: `go install` lines for staticcheck, govulncheck and golangci-lint, pinned to `@latest`
  only with a caution to pin a version.
- **Usage**: the cheapest-first checklist:
  1. `gofmt -l .` (empty output);
  2. `go vet ./...`;
  3. `staticcheck ./...` or `golangci-lint run`;
  4. `go test -race -count=1 ./...`;
  5. `govulncheck ./...`;
  6. `go mod verify` and `go mod tidy -diff`.
- **Freeform sections** per category.
- **Cautions**: `-race` needs cgo and slows tests; golangci-lint configs drift; `-count=1` defeats
  the test cache.
- **Known limitations**.
- **References**.

### T009 — `agent_profiles/go-gwen.agent.yaml`

The same shape as WP01 T004: `profile-id: go-gwen`, `name: Go Gwen`, `role: implementer`,
`applies_to_languages: [go]`, frameworks (net/http, database/sql, errgroup, testing, testify
optional), file patterns `**/*.go`, `**/go.mod`, and a self-review protocol (gofmt, vet, staticcheck,
`test -race`, govulncheck). References: `go-conventions` and `go-review-checks` only.

### T010 — `presets/go.yaml`

`id: go`; activates `go-conventions`, `go-review-checks` and `go-gwen`.

## Definition of Done

- [ ] Five files exist and are schema-valid (scratch check as in WP01).
- [ ] ≥ 10 principles, ≥ 8 patterns, ≥ 8 anti-patterns, each with examples.
- [ ] `grep -riE 'cobol|acas|legacy port' packs/go` finds nothing.

## Reviewer guidance

Read it as a senior Go reviewer would: Effective Go and Go Code Review Comments compliance, correct
`errors.Is` / `As` usage, and no `context` misuse.
