# Provenance: spec-kitty-internal Charter Pack (canonical home)

This is the **canonical home** of the in-house (org-tier) **internal** Charter
Pack. It is registered for `spec-kitty-open-packs`' own governance via
`.kittify/config.yaml` → `charter_packs.org.packs`, and other repositories take
it from here at a pinned commit.

## Identity is minted and owned here

`pack.yaml` pins the canonical `pack_id`. `spec-kitty-open-packs` is the single
minting authority for the `spec-kitty-internal` identity. Downstream repositories
that need this pack take it as it is at a pinned commit of this repository: they
never edit it, re-mint its `pack_id` or diverge from it.

## How downstream repositories take the pack

- `spec-kitty-charter` holds no tracked copy (spec-kitty-charter#364). Its
  `packs/internal` and `packs/qa` are gitignored copies that `./gradlew syncPacks`
  syncs from this repository at the commit named by `openPacksRef` in
  `gradle.properties`; `packs/open-packs.lock.yaml` records their tree digests.
- `spec-kitty` core pins a commit of this repository the same way and takes the
  pack with `spec-kitty charter pack vendor --pack internal --ref <sha>`.

A change lands here first and reaches a downstream repository when that
repository bumps its pin. Nothing is copied back.

## Received from built-in (#73)

Four artifacts moved here from `packs/built-in/` with `git mv` when #73 split built-in, so their
history follows the files: the `mission-tracer-files` and `mission-wrap-up-sequence` procedures,
the `tiered-standards` styleguide and the `agentic-framework-core-team` writing-audience asset.
