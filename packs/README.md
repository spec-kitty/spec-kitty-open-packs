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
├── presets/             # <name>.yaml activation presets
├── drg/fragment.yaml    # additive DRG fragment
└── org-charter.yaml     # optional policy / required artifacts
```

See [Author a Charter Pack](../docs/guides/author-a-doctrine-pack.md) to add one, and
[Validate a pack](../docs/guides/validate-a-pack.md) before you open a PR. CI validates every
directory here on each pull request (`scripts/ci/validate-packs.sh`).
