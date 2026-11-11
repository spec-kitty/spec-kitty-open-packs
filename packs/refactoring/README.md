# Refactoring pack (`refactoring`)

The refactoring catalogue (Fowler-style moves, strangler fig, state and strategy patterns), semantic compression, the code-smell anti-patterns and the Randy Reducer profile.

- **Level:** org (opt-in). Not aggregated by `built-in`.
- **pack_id:** `01M75PCTD0V3AFZA9EAXDJ894D`
- **Depends on:** `foundation`, `testing`
- **Contents:** 25 tactics, 7 anti patterns, 1 agent profile, 1 paradigm, 1 procedure.
- **Agent profiles:** `randy-reducer`.

## Adopt

Register the pack and its dependencies (see `depends_on` in `pack.yaml`), then activate what you
need per project with `spec-kitty charter activate ...`. Reference its artifacts from another pack as
`refactoring::<kind>:<id>`.

## Provenance

Carved from `packs/built-in/` by #73; see [PROVENANCE.md](PROVENANCE.md).
