# Refactoring pack (`refactoring`)

The refactoring catalogue (Fowler-style moves, strangler fig, state and strategy patterns), semantic compression, the code-smell anti-patterns and the Randy Reducer profile.

## Contents

- **Contents:** 25 tactics, 7 anti patterns, 1 agent profile, 1 paradigm, 1 procedure.
- **Agent profiles:** `randy-reducer`.

## Who uses it

Teams doing sustained refactoring or legacy clean-up.

## Adopt

Place the pack beside `built-in` and its dependencies (see `depends_on` in `pack.yaml`; it is not registered at org level), then activate what you
need per project with `spec-kitty charter activate ...`. Reference its artifacts from another pack as
`refactoring::<kind>:<id>`.

## Provenance

Every artifact in this pack was carved out of `packs/built-in/` by #73 (mission
`kitty-specs/foundation-writing-split-01M75HV3/`), with `git mv`, so `git log --follow <file>` shows
its full history. The ids and content are unchanged; only cross-pack references were qualified and
graph edges re-homed (see that mission's `research.md`, D4 and D11).

`packs/built-in/` was itself seeded from spec-kitty core (`packs/built-in` at commit
`f166339300dfe207ea7635a285e498beb877f1a0`, 2026-10-19) and has been authored in this repository since;
see `packs/built-in.source.yaml`.
