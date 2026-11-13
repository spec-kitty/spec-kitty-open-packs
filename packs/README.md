# Packs

This directory holds the materialized Charter Packs:

- the built-in distribution: [`built-in/`](built-in/), which aggregates [`foundation/`](foundation/README.md),
  [`writing/`](writing/README.md) and the core bundles [`testing/`](testing/README.md),
  [`refactoring/`](refactoring/README.md), [`architecture/`](architecture/README.md) and
  [`planning-analysis/`](planning-analysis/README.md);
- the opt-in bundles carved from it by #73: [`pack-authoring/`](pack-authoring/README.md), [`python/`](python/README.md),
  [`javascript/`](javascript/README.md), [`drupal/`](drupal/README.md) and [`java/`](java/README.md);
- the opt-in stack packs [`rust/`](rust/README.md) and [`go/`](go/README.md);
- the topical packs [`cave-kitty/`](cave-kitty/README.md), [`event-driven/`](event-driven/README.md),
  [`qa/`](qa/README.md) and [`spdd/`](spdd/README.md), and the maintainer pack
  [`internal/`](internal/README.md).

The rest of the [catalog proposal](../docs/packs/catalog-proposal.md) is still open.

Each pack is a directory using the canonical layout:

```
packs/<pack-name>/
├── directives/          # *.directive.yaml
├── tactics/             # *.tactic.yaml
├── styleguides/         # *.styleguide.yaml
├── toolguides/          # *.toolguide.yaml
├── paradigms/           # *.paradigm.yaml
├── procedures/          # *.procedure.yaml
├── agent_profiles/      # *.agent.yaml
├── assets/              # asset files + *.asset.yaml sidecars
├── glossary_packs/      # *.glossary-pack.yaml
├── presets/             # <name>.yaml activation presets
├── drg/fragment.yaml    # additive DRG fragment
├── pack.yaml            # the descriptor: identity, level and lineage (required)
├── README.md            # the pack document: its description, served by the charter
└── policy.yaml          # optional mutability levels (open, extendable, locked)
```

See [Author a Charter Pack](../docs/guides/author-a-charter-pack.md) to add one, and
[Validate a pack](../docs/guides/validate-a-pack.md) before you open a PR. CI validates every
directory here on each pull request (`scripts/ci/validate-packs.sh`).

The exceptions are the built-in-level packs. [`built-in/`](built-in/) is the default
*distribution pack*: it holds no artifacts and aggregates [`foundation/`](foundation/),
[`writing/`](writing/), [`testing/`](testing/), [`refactoring/`](refactoring/),
[`architecture/`](architecture/) and [`planning-analysis/`](planning-analysis/) (#73, charter
ADR-0048 decision 12). `foundation`, `writing` and `built-in` carry root
`*.graph.yaml` shards instead of `drg/fragment.yaml`; the four core bundles keep their
`drg/fragment.yaml`. Every pack in this directory carries the `pack-manifest.yaml` the charter derives
(`validate_pack_schemas.py --derive-manifest`, #255). All six members are built-in level, so they depend only
on built-in-level packs (ADR-0048 decision 7), and are read-only to registration. Every pack's tree digest is recorded in `packs/<name>.source.yaml` and checked by
`scripts/ci/check-pack-digests.sh`; see
[`built-in.source.yaml`](built-in.source.yaml) for built-in's provenance. The stacks and `pack-authoring` carved from
built-in ship as opt-in org bundles: `pack-authoring`, `python`, `javascript`, `drupal` and `java`.
