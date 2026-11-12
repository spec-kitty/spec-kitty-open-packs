# Python pack (`python`)

The Python stack: the Python Pedro profile, Python conventions, review checks, supply-chain and mutation tooling.

## Contents

- **Contents:** 3 toolguides, 1 agent profile, 1 styleguide.
- **Agent profiles:** `python-pedro`.

## Who opts in

Python teams.

## Adopt

Register the pack and its dependencies (see `depends_on` in `pack.yaml`), then activate what you
need per project with `spec-kitty charter activate ...`. Reference its artifacts from another pack as
`python::<kind>:<id>`.

## Provenance

Every artifact in this pack was carved out of `packs/built-in/` by #73 (mission
`kitty-specs/foundation-writing-split-01M75HV3/`), with `git mv`, so `git log --follow <file>` shows
its full history. The ids and content are unchanged; only cross-pack references were qualified and
graph edges re-homed (see that mission's `research.md`, D4 and D11).

`packs/built-in/` was itself seeded from spec-kitty core (`packs/built-in` at commit
`f166339300dfe207ea7635a285e498beb877f1a0`, 2026-10-19) and has been authored in this repository since;
see `packs/built-in.source.yaml`.
