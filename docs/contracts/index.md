---
title: Contracts
description: "The machine contracts a Charter Pack meets: pack, org-charter, preset, manifest and DRG files, registration, commands and charter seams."
doc_status: draft
updated: '2026-10-31'
related:
- artefacts
- organisations
- architecture/overview
- guides/validate-a-pack
---
# Contracts

The files and interfaces a pack is held to. The **schemas are owned by the charter**
([`spec-kitty-charter`](https://github.com/spec-kitty/spec-kitty-charter), `contracts/packs/`), and CI validates against them; this page describes them as consumed here. Generated, schema-derived
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

## `presets/<id>.yaml` — activation presets

This repository validates presets in the charter's sanitized shape (charter ADR-0042, schema
`preset.schema.json`). The old shape (`name`, bare id strings, `mission_type_activations`) fails
validation here.

| Field | Meaning |
| --- | --- |
| `schema_version` | The string `"1.0"`. Required. |
| `id` | Preset id, equal to the file stem; used by `spec-kitty charter activate --preset <id>`. Lowercase words joined by `-`. Required. |
| `description` | What applying the preset puts in force. Required. |
| `activated_kinds` | Optional kind gate: the kinds the preset activates, each once. A kind left out is switched off; without the key no kind is gated. |
| `activated_mission_types` | Mission types to activate, each item `{id: <mission type id>}`. |
| `activated_<plural kind>` | Artefacts to activate for that kind, each item `{id: <artefact id>}` and optionally `must_have: true`. Use the artefact's `id`, not its file name. A kind with no key stays unrestricted; a key is never an empty list. |

```yaml
schema_version: "1.0"
id: qa
description: Run QA missions.
activated_mission_types:
  - id: qa
activated_agent_profiles:
  - id: qa-strategist-quinn
```

Core up to 4.0.0rc8 does not read this shape; see the [changelog](../changelog/CHANGELOG.md).

## Mission step inputs and outputs

A mission step lists the artifacts it needs under `expected_input_artifacts` and the ones it
writes under `expected_output_artifacts`. An input reuses the `artifact_key` of the step that
produces it (the same key may stand at two steps). An input is `blocking` only when its
producer's output is `blocking`.

## `drg/fragment.yaml` — DRG fragment

This covers org Charter Pack fragments; the built-in pack's `<kind>.graph.yaml` shards are a
separate, generated format. The authoritative schema is spec-kitty-charter's pack schema
([charter#114](https://github.com/spec-kitty/spec-kitty-charter/issues/114), charter ADR-0017);
this table summarises it.

| Field | Meaning |
| --- | --- |
| `nodes` | `{id, kind, title, body_path}` per artefact. |
| `edges` | `{source, target, relation}`. Endpoints are DRG URNs (`<kind>:<id>`, singular kind), a node of this fragment included: write `procedure:my-procedure`, not `my-procedure`. |

A fragment carries no provenance header. The pack's name, source and layer come from the
consumer's registration (`.kittify/config.yaml`), so `pack_name`, `source_kind`, `source_ref`,
`layer_index` and `provenance_marker` are not written here. The charter's pack schema refuses
them and bare-id endpoints. This repository validates against the charter's schemas, so
`scripts/ci/validate-packs.sh` enforces the rule for its packs.

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
| `spec-kitty charter pack list` | Packs in the offering and the presets each ships. |
| `spec-kitty charter pack regenerate-graph` | Regenerates the pack manifest and graph deterministically. |
| `spec-kitty charter fetch [--pack <name>] [--dry-run]` | Fetches configured org packs. |
| `spec-kitty charter activate <kind> <id>` / `--preset <name>` | Changes the Active Charter. |
| `spec-kitty charter context --action <action>` | Renders action-scoped guidance. |
| `spec-kitty doctor charter-packs [--json]` | Health of each loaded pack, including skipped profiles. |
| `python3 scripts/ci/validate_pack_schemas.py <dir>` | This repository's validator: every pack file against the charter pack schemas. Zero violations is the publishing gate. |

## Charter entry seams

| Seam | Purpose |
| --- | --- |
| `charter.offering.api` | The only entry point for CLI reads of the offering. |
| `charter.activation.api` | Reads and changes the Active Charter. |

Both are Python packages in the core CLI today. The
[`spec-kitty-charter`](https://github.com/spec-kitty/spec-kitty-charter) repository will hold
the OpenAPI 3.1 contract (`contracts/charter/`, planned) that a charter service and the CLI both
generate their data types from. Pack files are unaffected by that move.
