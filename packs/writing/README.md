# Writing pack (`writing`)

Documentation, communication and terminology doctrine, and a member of the `built-in`
distribution.

- **Agent profiles:** `comms-cleo`, `curator-carla`, `diagram-daisy`, `lexical-larry`,
  `minutes-mahad`, `scribe-sally`, `synthesizer-sam`.
- **Mission type:** `documentation`.

Reference its artifacts from another pack as `writing::<kind>:<id>`.

## Authored and generated files

This README and its sibling `pack.yaml` are authored; `pack-manifest.yaml` is generated and never
hand-edited.

## Provenance

Every artifact in this pack was carved out of `packs/built-in/` by #73 (mission
`kitty-specs/foundation-writing-split-01M75HV3/`), with `git mv`, so `git log --follow <file>` shows
its full history. The ids and content are unchanged; only cross-pack references were qualified and
graph edges re-homed (see that mission's `research.md`, D4 and D11).

`packs/built-in/` was itself seeded from spec-kitty core (`packs/built-in` at commit
`f166339300dfe207ea7635a285e498beb877f1a0`, 2026-10-19) and has been authored in this repository since;
see `packs/built-in.source.yaml`.
