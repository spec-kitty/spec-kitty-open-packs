---
title: Contracts
description: "The machine contracts a Charter Pack meets: pack, org-charter, preset, manifest and DRG files, registration, commands and charter seams."
doc_status: draft
updated: '2026-10-18'
related:
- artefacts
- organisations
- architecture/overview
- guides/validate-a-pack
---
# Contracts

The files and interfaces a pack is held to. The **schemas are owned by the charter** (today in
the Spec Kitty core CLI); this page describes them as consumed here. Generated, schema-derived
reference pages are tracked in
[#24](https://github.com/spec-kitty/spec-kitty-open-packs/issues/24).

## Pack layout

```text
my-pack/
├── pack.yaml              # authored descriptor (required for new packs)
├── pack-manifest.yaml     # generated inventory — never hand-edit
├── org-charter.yaml       # org packs only: requirements and skill namespace
├── drg/fragment.yaml      # the pack's DRG fragment (empty is valid)
├── presets/<name>.yaml    # optional activation presets
└── <kind directories>/    # one per artefact kind — see Charter artefacts
```

The built-in pack is the exception: it ships per-kind graph files (`<kind>.graph.yaml`) at its
root instead of `drg/fragment.yaml`.

## `pack.yaml` — pack descriptor

Authored and hand-edited.

| Field | Meaning |
| --- | --- |
| `pack_id` | ULID, minted once and never changed or fabricated downstream. |
| `pack_version` | SemVer of the pack content. |
| `parent_pack` | Parent pack id, or `null`. |
| `name` | Pack name. |
| `pack_level` | Tier: `built-in`, `org` or `project`. A mismatch with where the pack is loaded fails with `PACK_LEVEL_MISMATCH`; omission with `PACK_LEVEL_MISSING`. |

```yaml
pack_id: 01ARWG13C000000000000000FG
pack_version: 1.0.0
parent_pack: null
name: built-in
pack_level: built-in
```

## `pack-manifest.yaml` — generated inventory

Machine-written by the charter tooling: a `constituents` list of `{id, kind, path,
content_hash, provenance_path}`. Regenerate with `spec-kitty charter pack regenerate-graph`
after changing a pack; never edit it by hand.

## `org-charter.yaml` — org policy

| Field | Meaning |
| --- | --- |
| `schema_version` | Optional schema version. |
| `org_name` | The organisation the pack represents. |
| `skill_namespace` | Prefix for rendered pack skills: lowercase ASCII, starts with a letter, `[a-z0-9]` segments joined by `-`, at most 32 characters; `spk-`, `spec-kitty-` and `spec-kitty.` are reserved. Required when the pack ships skills. |
| `required_<plural kind>` | Artefact ids that are always in force for any project registering the pack, e.g. `required_directives`, `required_procedures`, `required_toolguides`, `required_glossary_packs`, `required_skills`. |

See [Organisations](../organisations/index.md) for how these are used.

## `presets/<name>.yaml` — activation presets

| Field | Meaning |
| --- | --- |
| `name` | Preset name, used by `spec-kitty charter activate --preset <name>`. |
| `description` | One line. |
| `mission_type_activations` | Mission types to activate. |
| `activated_<plural kind>` | Artefact ids to activate for that kind. A kind with no key stays unrestricted. |

## `drg/fragment.yaml` — DRG fragment

| Field | Meaning |
| --- | --- |
| `pack_name`, `source_kind`, `source_ref`, `layer_index` | Placeholders; overwritten at load time. |
| `nodes` | `{id, kind, title, body_path}` per artefact. |
| `edges` | `{source, target, relation}`. Endpoints are DRG URNs (`<kind>:<id>`) or ids declared in `nodes`; anything else is refused as `unresolved_edge_endpoint`. |

Relations include `requires`, `suggests`, `applies`, `scope`, `vocabulary`, `delegates_to`,
`specializes_from`, `enhances`, `overrides`, `refines`, `replaces`, `rejects`, `instantiates`,
`in_tension_with` and `reconciles_tension`.

## Consumer registration — `.kittify/config.yaml`

```yaml
charter_packs:
  org:
    packs:
      - name: qa
        local_path: "${SPEC_KITTY_PACK_HOME}/qa"
        source_type: git            # git | https | artifactory | api
        url: "https://github.com/spec-kitty/spec-kitty-open-packs.git"
        ref: "<commit SHA or tag>"  # never a branch
        subdir: packs/qa
```

| Field | Required | Meaning |
| --- | --- | --- |
| `name` | yes | Pack name, used by `--pack`. |
| `local_path` | yes | Where the snapshot lives; `~` and `${VAR}` expand. |
| `source_type` | no | `git`, `https`, `artifactory` or `api`; omit for a pack already on disk. |
| `url` | with `source_type` | Remote location. |
| `ref` | no | Version pin. |
| `subdir` | no | The pack's directory inside a multi-pack source. |

## Commands

| Command | Contract |
| --- | --- |
| `spec-kitty charter pack validate <dir> [--json]` | Schema and DRG validation. Zero errors is the publishing gate. |
| `spec-kitty charter pack list` | Packs in the offering and the presets each ships. |
| `spec-kitty charter pack regenerate-graph` | Regenerates the pack manifest and graph deterministically. |
| `spec-kitty charter fetch [--pack <name>] [--dry-run]` | Fetches configured org packs. |
| `spec-kitty charter activate <kind> <id>` / `--preset <name>` | Changes the Active Charter. |
| `spec-kitty charter context --action <action>` | Renders action-scoped guidance. |
| `spec-kitty doctor charter-packs [--json]` | Health of each loaded pack, including skipped profiles. |

## Charter entry seams

| Seam | Purpose |
| --- | --- |
| `charter.offering.api` | The only entry point for CLI reads of the offering. |
| `charter.activation.api` | Reads and changes the Active Charter. |

Both are Python packages in the core CLI today. The
[`spec-kitty-charter`](https://github.com/spec-kitty/spec-kitty-charter) repository will hold
the OpenAPI 3.1 contract (`contracts/charter/`, planned) that a charter service and the CLI both
generate their data types from. Pack files are unaffected by that move.
