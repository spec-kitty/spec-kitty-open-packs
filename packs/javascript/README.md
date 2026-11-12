# JavaScript pack (`javascript`)

The JavaScript and web stack: Node, frontend and design profiles, TypeScript, HTML and CSS conventions, atomic design, supply-chain and mutation tooling.

- **Contents:** 4 tactics, 3 agent profiles, 3 styleguides, 2 toolguides, 1 paradigm.
- **Agent profiles:** `designer-dagmar`, `frontend-freddy`, `node-norris`.

## Who opts in

JavaScript, TypeScript and frontend teams.

## Adopt

Register the pack and its dependencies (see `depends_on` in `pack.yaml`), then activate what you
need per project with `spec-kitty charter activate ...`. Reference its artifacts from another pack as
`javascript::<kind>:<id>`.

## Provenance

Every artifact in this pack was carved out of `packs/built-in/` by #73 (mission
`kitty-specs/foundation-writing-split-01M75HV3/`), with `git mv`, so `git log --follow <file>` shows
its full history. The ids and content are unchanged; only cross-pack references were qualified and
graph edges re-homed (see that mission's `research.md`, D4 and D11).

`packs/built-in/` was itself seeded from spec-kitty core (`packs/built-in` at commit
`f166339300dfe207ea7635a285e498beb877f1a0`, 2026-10-19) and has been authored in this repository since;
see `packs/built-in.source.yaml`.
