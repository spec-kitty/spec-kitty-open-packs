# Drupal pack (`drupal`)

The Drupal stack: the Drupal Dries profile, Drupal conventions, security and performance guidance, and review checks.

- **Level:** org (opt-in). Not aggregated by `built-in`.
- **pack_id:** `01M75PCTJCYC7R2WD6M8KBJ4ZK`
- **Depends on:** `foundation`, `testing`
- **Contents:** 2 styleguides, 1 agent profile, 1 toolguide.
- **Agent profiles:** `drupal-dries`.

## Adopt

Register the pack and its dependencies (see `depends_on` in `pack.yaml`), then activate what you
need per project with `spec-kitty charter activate ...`. Reference its artifacts from another pack as
`drupal::<kind>:<id>`.

## Provenance

Carved from `packs/built-in/` by #73; see [PROVENANCE.md](PROVENANCE.md).
