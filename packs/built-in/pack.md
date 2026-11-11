# Built-in Charter Pack

The **built-in** pack is Spec Kitty's default distribution. Since #73 it is a *distribution pack*
(charter ADR-0048 decision 12): it holds no artifacts of its own and aggregates its two members,
`foundation` and `writing`, through `depends_on`, pinned exactly and released in lockstep
(decision 17). It keeps the `default` and `minimal` presets and declares the fallback profile.

Specialist doctrine (testing, refactoring, architecture, planning and analysis, adversarial review,
pack authoring, and the python, javascript, drupal and java stacks) ships as opt-in org bundles
that build on `foundation`; built-in does not aggregate them (decision 14).

It has no `parent_pack` (it is the root of every lineage chain).

## Authored and generated files

This file and its sibling `pack.yaml` are **authored**: hand-edited data that is never
regenerated. The generated `pack-manifest.yaml` next to this file is machine-written only and must
never be hand-edited.
