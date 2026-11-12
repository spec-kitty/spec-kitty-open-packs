# Foundation pack (`foundation`)

The basis of every Spec Kitty project, and a member of the `built-in` distribution.

- **Agent profiles:** `generic-agent` (Generic Giannis, the fallback), `implementer-ivan`,
  `reviewer-renata`, `analyst-annie`, `human-in-charge`.
- **Mission types:** `software-dev`, `plan`, `research`.
- **Doctrine:** every cross-cutting directive with its how-to procedures, tactics and toolguides.

Build on it from another pack with `depends_on` (`range: ">=1.0,<2"`) and reference its artifacts
as `foundation::<kind>:<id>`. Mission roles no installed profile fills (for example `researcher`
without the `planning-analysis` bundle) go to a profile that lists the role as an alt-role (for
example `comms-cleo` or `synthesizer-sam` in `writing`, for `researcher`), else to Generic Giannis.

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
