# Pack authoring pack (`pack-authoring`)

Doctrine and pack authoring: the Doctrine Daphne profile, onboarding external agents into a pack, deployable skill authoring and the migration-to-charter procedure.

- **Level:** org (opt-in). Not aggregated by `built-in`.
- **pack_id:** `01M75PCTG46SQ9VA5NQF8ZZ2AG`
- **Depends on:** `foundation`, `writing`
- **Contents:** 3 templates, 2 procedures, 1 agent profile, 1 styleguide.
- **Agent profiles:** `doctrine-daphne`.

## Adopt

Register the pack and its dependencies (see `depends_on` in `pack.yaml`), then activate what you
need per project with `spec-kitty charter activate ...`. Reference its artifacts from another pack as
`pack-authoring::<kind>:<id>`.

## Provenance

Carved from `packs/built-in/` by #73; see [PROVENANCE.md](PROVENANCE.md).
