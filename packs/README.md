# Packs

This directory holds the materialized Charter Packs. It ships three packs so far,
[`cave-kitty/`](cave-kitty/README.md), [`event-driven/`](event-driven/README.md) and
[`qa/`](qa/README.md); the rest of the catalog is still a
[proposal](../docs/packs/catalog-proposal.md), carved from the Spec Kitty built-in corpus
incrementally, one tracking issue at a time.

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

The exception is [`built-in/`](built-in/), the Spec Kitty consumer built-in pack. It is not an org pack:
`validate-packs.sh` skips it and `scripts/ci/check-built-in.sh` checks it instead. See
[`built-in.source.yaml`](built-in.source.yaml) for its provenance.
