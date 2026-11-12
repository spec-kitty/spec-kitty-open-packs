# Testing pack (`testing`)

Test design and test-first practice beyond the foundation basics: BDD and specification by example, test minimisation and reconstruction, mutation testing, Gherkin, and the debugging profile.

## Contents

- **Contents:** 9 tactics, 5 procedures, 5 styleguides, 2 paradigms, 1 agent profile, 1 directive, 1 toolguide.
- **Agent profiles:** `debugger-debbie`.

## Who uses it

Teams that want a deeper testing discipline, and every stack pack (java, python, javascript, drupal), whose profiles build on these practices.

## Adopt

Place the pack beside `built-in` and its dependencies (see `depends_on` in `pack.yaml`; it is not registered at org level), then activate what you
need per project with `spec-kitty charter activate ...`. Reference its artifacts from another pack as
`testing::<kind>:<id>`.

## Provenance

Every artifact in this pack was carved out of `packs/built-in/` by #73 (mission
`kitty-specs/foundation-writing-split-01M75HV3/`), with `git mv`, so `git log --follow <file>` shows
its full history. The ids and content are unchanged; only cross-pack references were qualified and
graph edges re-homed (see that mission's `research.md`, D4 and D11).

`packs/built-in/` was itself seeded from spec-kitty core (`packs/built-in` at commit
`f166339300dfe207ea7635a285e498beb877f1a0`, 2026-10-19) and has been authored in this repository since;
see `packs/built-in.source.yaml`.
