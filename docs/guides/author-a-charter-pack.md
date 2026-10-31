---
title: Author a Charter Pack
description: Lay out a Spec Kitty 4.x Charter Pack, write schema-valid artifacts, namespace IDs, add a DRG fragment, and optionally ship presets and an org-charter.yaml.
doc_status: wip
updated: '2026-10-31'
related:
- guides/validate-a-pack
- guides/publish-a-pack
- packs/catalog-proposal
---
# Author a Charter Pack

This guide walks a pack author from an empty directory to a validated pack. It adapts the
canonical upstream reference,
[How to create an org Charter Pack (core)](https://github.com/spec-kitty/spec-kitty/blob/main/docs/guides/how-to/governance/create-an-org-doctrine-pack.md),
for the open-packs marketplace. Where that guide and the artifact schemas disagree, the schemas
(`src/charter/offering/schemas/`) and `spec-kitty charter pack validate` win. You do **not** need a Spec Kitty project to author a pack.

## 1. Lay out the directory

One directory per artifact kind, directly under the pack root. The artifact directories are
optional, but every pack ships `drg/fragment.yaml` (see step 4); a valid pack is any non-empty
subset of the artifact kinds plus that fragment. Spec Kitty 4.x reads only this flat layout: the 3.x nested
`<pack>/doctrine/<kind>/<layer>/` layout is ignored.

```
my-pack/
├── directives/                 # *.directive.yaml — project rules
├── tactics/                    # *.tactic.yaml — domain tactics (subdirs allowed)
├── styleguides/                # *.styleguide.yaml — style standards
├── toolguides/                 # *.toolguide.yaml — tool usage rules
├── paradigms/                  # *.paradigm.yaml — paradigm definitions
├── procedures/                 # *.procedure.yaml — operational procedures
├── agent_profiles/             # *.agent.yaml — agent personas
├── mission_step_contracts/     # *.step-contract.yaml — mission step contracts
├── glossary_packs/             # *.glossary-pack.yaml — terminology
├── assets/                     # *.asset.yaml sidecars plus the files they describe
├── skills/                     # *.skill.yaml — agent skills, installed under skill_namespace
├── missions/                   # <type>/<type>.mission-type.yaml plus steps/ — custom mission types
├── presets/                    # <name>.yaml — activation presets
├── drg/fragment.yaml           # additive DRG fragment (the only DRG file an org pack may have)
└── org-charter.yaml            # optional: policy, required artifacts, interview defaults
```

> **Do not hand-write `pack-manifest.yaml`.** It is written by tooling (`charter fetch` for
> non-git sources, `charter pack assemble`); `charter pack validate` does not read it, so a
> hand-edited manifest goes unnoticed rather than flagged.

## 2. Write artifacts — one rule per file

Each file conforms to the same YAML schema Spec Kitty uses everywhere. Every artifact carries
`schema_version: "1.0"` and a unique `id`; fill the required fields for its kind and save it in
the matching directory. Example directive:

```yaml
# directives/acme-001-secret-handling.directive.yaml
schema_version: "1.0"
id: ACME_001_SECRET_HANDLING
title: Never commit credentials to the repository
intent: |
  Secrets must be supplied via environment or secret manager. Pre-commit hooks
  must scan staged content for known credential shapes.
enforcement: required        # required | lenient-adherence | advisory
```

Required fields per kind:

| Kind | `id` shape | Required fields |
| --- | --- | --- |
| directive | upper case, `^[A-Z][A-Z0-9_-]*$` | `schema_version`, `id`, `title`, `intent`, `enforcement` |
| tactic | lower-case kebab | `schema_version`, `id`, `name`, `steps` |
| procedure | lower-case kebab | `schema_version`, `id`, `title`, `description`, `entry_condition`, `exit_condition`, `steps` |
| styleguide | lower-case kebab | `schema_version`, `id`, `title`, `scope`, `principles` |
| toolguide | lower-case kebab | `schema_version`, `id`, `tool`, `title`, `guide_path` (`<id>.guide.md`), `summary` |
| paradigm | lower-case kebab | `schema_version`, `id`, `name`, `summary` |
| agent profile | `profile-id` (not `id`) | `profile-id`, `name`, `purpose`, `specialization` |

Resist dumping a whole policy page into one artifact — split so each rule can be cited
individually in lint advisories and review feedback.

## 3. Namespace your IDs

Org-pack IDs collide **globally** with built-in and project IDs. Prefix them to keep
collisions visible:

| Artifact type | File pattern | Recommended ID prefix |
| --- | --- | --- |
| Directives | `*.directive.yaml` | `<ORG>_<SEQ>_<SLUG>` |
| Tactics | `*.tactic.yaml` | `<org>-tac-<seq>` |
| Styleguides | `*.styleguide.yaml` | `<org>-sty-<seq>` |
| Toolguides | `*.toolguide.yaml` | `<org>-tg-<seq>` |
| Paradigms | `*.paradigm.yaml` | `<org>-par-<seq>` |
| Procedures | `*.procedure.yaml` | `<org>-proc-<seq>` |
| Agent profiles | `*.agent.yaml` | `<org>-<role>` |
| Mission step contracts | `*.step-contract.yaml` | `<org>-msc-<seq>` |

Colliding with a built-in id is *permitted* but raises a `same_id_collision` advisory, and the
artifact field-merges into the built-in. Say what you mean with a DRG edge from your artifact to
the built-in in `drg/fragment.yaml` (`relation: enhances` to keep the merge, `overrides` for a full
replacement; the schemas reject `enhances:`/`overrides:` as artifact fields, whatever the advisory
text suggests). `doctor charter-packs` then fails on the override until the pack sanctions it in a
`replaceable-builtins.yaml` at the pack root:

```yaml
# replaceable-builtins.yaml
replaceable_builtins:
  - urn: directive:DIRECTIVE_001
    reason: Why this pack replaces the built-in rule (mandatory for directives).
```

Keep such overrides intentional.

## 4. Add the DRG fragment

Ship a `drg/fragment.yaml` even when the pack adds no relations: `charter pack validate` accepts a
pack without one, but a consumer's `doctor charter-packs` fails with "org pack missing:
…/drg/fragment.yaml not found". An empty fragment is `nodes: []` and `edges: []`. Add the pack's
typed graph relations there:

```yaml
# drg/fragment.yaml
nodes: []   # nodes are inferred from artifact files
edges:
  - source: directive:ACME_001_SECRET_HANDLING
    target: tactic:acme-tac-001-scan-staged
    relation: requires
```

Endpoints are `<kind>:<id>`. The fragment is **additive only**, and it is the only DRG file an
org pack may have: `drg/*.graph.yaml` shards fail validation with `drg_root_graph_missing`.

## 5. Ship presets and policy (optional)

A **preset** is a named set of activations a consumer applies with
`spec-kitty charter activate --pack <pack> --preset <id>`. The file name is the preset id. This
repository validates presets in the charter's **sanitized shape** (charter ADR-0042): a
`schema_version` of `"1.0"`, an `id` equal to the file name, a `description`, and each activation
list holding `{id: ...}` items with the artifact's own `id` (not its file name):

```yaml
# presets/acme.yaml
schema_version: "1.0"
id: acme
description: Turn on the Acme rules.
activated_directives:
  - id: ACME_001_SECRET_HANDLING
# activated_<kind>: absent = unrestricted; a list is never empty.
# activated_mission_types: [{id: ...}] activates mission types.
```

A preset is self-contained, not incremental: it is the whole activation selection for the kinds
it names, not a delta on top of other presets. Which agent profiles it holds is an operator's
choice, so a preset need not fill every role its mission types name; list the profiles you want
in force and leave the rest out.

The old shape (`name:`, `activated_directives: [ACME_001_SECRET_HANDLING]`,
`mission_type_activations`) fails validation. Core up to 4.0.0rc8 reads only the old shape.

An `org-charter.yaml` at the pack root can pre-fill the consumer's charter interview, put
artifacts in force for every consumer, or surface advisory policy. Prefer presets for packs
that should stay opt-in:

```yaml
# org-charter.yaml
schema_version: 2
org_name: acme
interview_defaults:
  language: python
  test_framework: pytest
required_directives:
  - ACME_001_SECRET_HANDLING
governance_policies:
  - field: min_test_coverage
    value: "80"
    enforcement: advisory
```

Omit it entirely for packs that ship only artifacts. `spec-kitty charter org init` scaffolds
a schema-2 `org-charter.yaml` and a starter preset (rewrite the preset in the shape above).

### Mission step inputs

A mission type's step lists what it needs under `expected_input_artifacts`. Reuse the
`artifact_key` of the step that produces the artifact, and mark the input `blocking: true` only
when that producer's `expected_output_artifacts` entry is `blocking`. An input whose producer is
not blocking stays non-blocking, so a step is not held up by an artifact that may legitimately be
absent.

## 6. Reuse existing built-in artifacts

Many open packs are **carved from the built-in corpus** rather than written from scratch.
When a pack's purpose maps to existing built-in directives/tactics/etc., reference them in
the pack's tracking issue and, where the pack is a curated subset, keep IDs stable so
consumers recognize them. See the [pack catalog proposal](../packs/catalog-proposal.md) for
the source-artifact mapping per proposed pack.

## Next

- [Validate a pack](validate-a-pack.md)
- [Publish a pack](publish-a-pack.md)
