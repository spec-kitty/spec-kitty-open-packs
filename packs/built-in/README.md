# Built-in Charter Pack

The **built-in** pack is Spec Kitty's default distribution. Since #73 it is a *distribution pack*
(charter ADR-0048 decision 12): it holds no artifacts of its own and aggregates its six members, `foundation`, `writing`, `testing`, `refactoring`, `architecture` and
`planning-analysis`, through `depends_on`, pinned exactly and released in lockstep (decision 17). It
keeps the `default` and `minimal` presets and declares the fallback profile.

Built-in is the aggregate of the general-purpose open-packs: the foundation basics, writing
doctrine, and the testing, refactoring, architecture and planning-analysis bundles. Each member is a
built-in-level pack, so it depends only on built-in-level packs (decision 7). The stacks (`python`,
`javascript`, `drupal`, `java`), `pack-authoring` and the topical and process packs (`qa`,
`event-driven`, `spdd`, `cave-kitty`, `internal`) stay opt-in at org level (decision 14).

It has no `parent_pack` (it is the root of every lineage chain).

## Authored and generated files

This README and its sibling `pack.yaml` are **authored**: hand-edited data that is never
regenerated. The generated `pack-manifest.yaml` next to it is machine-written only and must
never be hand-edited.
