# Packs

This directory holds the materialized doctrine packs. It is **intentionally near-empty** for
now — the catalog is still a [proposal](../docs/packs/catalog-proposal.md), and packs are
carved from the Spec Kitty built-in corpus incrementally, one tracking issue at a time.

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
├── drg/                 # *.graph.yaml (additive fragments)
└── org-charter.yaml     # optional activation defaults
```

See [Author a doctrine pack](../docs/guides/author-a-doctrine-pack.md) to add one, and
[Validate a pack](../docs/guides/validate-a-pack.md) before you open a PR.
