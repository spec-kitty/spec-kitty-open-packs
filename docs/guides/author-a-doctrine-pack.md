---
title: Author a doctrine pack
description: Lay out a Spec Kitty doctrine pack, write artifacts, namespace IDs, add DRG fragments, and optionally ship activation defaults via org-charter.yaml.
doc_status: wip
updated: '2026-07-12'
related:
- docs/guides/validate-a-pack.md
- docs/guides/publish-a-pack.md
- docs/packs/catalog-proposal.md
---
# Author a doctrine pack

This guide walks a pack author from an empty directory to a validated pack. It adapts the
canonical upstream reference,
[How to Create an Org Doctrine Pack](https://github.com/Priivacy-ai/spec-kitty/blob/main/docs/guides/create-an-org-doctrine-pack.md),
for the open-packs marketplace. You do **not** need a Spec Kitty project to author a pack.

## 1. Lay out the directory

One directory per artifact kind. All are optional; a valid pack is any non-empty subset.

```
my-pack/
├── directives/                 # *.directive.yaml — project rules
├── tactics/                    # *.tactic.yaml — domain tactics (subdirs allowed)
├── styleguides/                # *.styleguide.yaml — style standards
├── toolguides/                 # *.toolguide.yaml — tool usage rules
├── paradigms/                  # *.paradigm.yaml — paradigm definitions
├── procedures/                 # *.procedure.yaml — operational procedures
├── agent_profiles/             # *.agent.yaml — agent personas
├── mission_step_contracts/     # *.contract.yaml — mission step contracts
├── drg/                        # *.graph.yaml — additive DRG fragments
└── org-charter.yaml            # optional: activation defaults / policy
```

> **Do not hand-write `pack-manifest.yaml`.** It is written by tooling (`doctrine fetch` for
> non-git sources, `doctrine pack assemble`). Manual edits surface as an advisory in
> `pack validate`.

## 2. Write artifacts — one rule per file

Each file conforms to the same YAML schema Spec Kitty uses everywhere. Give it a unique `id`,
fill the required fields for its kind, and save it in the matching directory. Example
directive:

```yaml
# directives/acme-001-secret-handling.directive.yaml
id: acme-001-secret-handling
title: Never commit credentials to the repository
severity: high
description: |
  Secrets must be supplied via environment or secret manager. Pre-commit hooks
  must scan staged content for known credential shapes.
action_scope:
  - implement
  - review
```

Resist dumping a whole policy page into one artifact — split so each rule can be cited
individually in lint advisories and review feedback.

## 3. Namespace your IDs

Org-pack IDs collide **globally** with built-in and project IDs. Prefix them to keep
collisions visible:

| Artifact type | File pattern | Recommended ID prefix |
| --- | --- | --- |
| Directives | `*.directive.yaml` | `<org>-<seq>-<slug>` |
| Tactics | `*.tactic.yaml` | `<org>-tac-<seq>` |
| Styleguides | `*.styleguide.yaml` | `<org>-sty-<seq>` |
| Toolguides | `*.toolguide.yaml` | `<org>-tg-<seq>` |
| Paradigms | `*.paradigm.yaml` | `<org>-par-<seq>` |
| Procedures | `*.procedure.yaml` | `<org>-proc-<seq>` |
| Agent profiles | `*.agent.yaml` | `<org>-<role>` |
| Mission step contracts | `*.contract.yaml` | `<org>-msc-<seq>` |

Colliding with a built-in id is *permitted* but produces a full-replace advisory. Keep such
overrides intentional.

## 4. Add DRG fragments (optional)

If your pack contributes typed graph relations, add a fragment under `drg/`:

```yaml
# drg/010-security.graph.yaml
nodes: []   # nodes are inferred from artifact files
edges:
  - source: urn:directive:acme-001-secret-handling
    target: urn:action:implement
    relation: scope
```

DRG fragments are **additive only**. Fragment files merge in alphabetical filename order —
use numeric prefixes (`010-`, `020-`) when order matters.

## 5. Ship activation defaults (optional)

An `org-charter.yaml` at the pack root can pre-fill the consumer's charter interview, require
directives, or surface advisory policy:

```yaml
# org-charter.yaml
schema_version: "1"
org_name: ACME Corporation
interview_defaults:
  language: python
  test_framework: pytest
required_directives:
  - acme-001-secret-handling
governance_policies:
  - field: min_test_coverage
    value: "80"
    enforcement: advisory
```

Omit it entirely for packs that ship only doctrine artifacts.

## 6. Reuse existing built-in artifacts

Many open packs are **carved from the built-in corpus** rather than written from scratch.
When a pack's purpose maps to existing built-in directives/tactics/etc., reference them in
the pack's tracking issue and, where the pack is a curated subset, keep IDs stable so
consumers recognize them. See the [pack catalog proposal](../packs/catalog-proposal.md) for
the source-artifact mapping per proposed pack.

## Next

- [Validate a pack](validate-a-pack.md)
- [Publish a pack](publish-a-pack.md)
