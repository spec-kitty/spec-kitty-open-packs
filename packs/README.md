# Packs

This directory holds the materialized Charter Packs:

- the built-in distribution: [`built-in/`](built-in/), which aggregates [`foundation/`](foundation/README.md)
  and [`writing/`](writing/README.md);
- the opt-in bundles carved from it by #73: [`testing/`](testing/README.md),
  [`refactoring/`](refactoring/README.md), [`architecture/`](architecture/README.md),
  [`planning-analysis/`](planning-analysis/README.md),
  [`pack-authoring/`](pack-authoring/README.md), [`python/`](python/README.md),
  [`javascript/`](javascript/README.md), [`drupal/`](drupal/README.md) and [`java/`](java/README.md);
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
└── org-charter.yaml     # optional policy / required artifacts
```

See [Author a Charter Pack](../docs/guides/author-a-charter-pack.md) to add one, and
[Validate a pack](../docs/guides/validate-a-pack.md) before you open a PR. CI validates every
directory here on each pull request (`scripts/ci/validate-packs.sh`).

The exceptions are the three built-in-level packs. [`built-in/`](built-in/) is the default
*distribution pack*: it holds no artifacts and aggregates [`foundation/`](foundation/) and
[`writing/`](writing/) (#73, charter ADR-0048 decision 12). The three carry a generated
`pack-manifest.yaml` and root `*.graph.yaml` shards instead of `drg/fragment.yaml`. They are
read-only to registration. `scripts/ci/check-built-in.sh` checks the built-in digest; see
[`built-in.source.yaml`](built-in.source.yaml) for its provenance. Specialist doctrine carved from
built-in ships as opt-in org bundles: `testing`, `refactoring`, `architecture`, `planning-analysis`,
`pack-authoring`, `python`, `javascript`, `drupal` and `java`.
