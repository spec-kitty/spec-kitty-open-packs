---
title: Charter artefacts
description: "The structure of every charter artefact kind a Charter Pack can carry: directory, file naming and key fields."
doc_status: draft
updated: '2026-10-31'
related:
- contracts
- guides/author-a-charter-pack
- glossary
---
# Charter artefacts

A Charter Pack is a set of **charter artefacts**, one YAML file each, grouped in one directory
per kind. The kind vocabulary is owned by the charter (`ArtifactKind`); every pack, whatever its
tier, uses the same layout. Field lists below are taken from real files under `packs/`; scaffold a new one with `spec-kitty charter new` and validate with
`spec-kitty charter pack validate`.

## Kinds at a glance

| Kind | Directory | File name | What it governs |
| --- | --- | --- | --- |
| Directive | `directives/` | `<id>.directive.yaml` | A binding rule, with an enforcement level. |
| Tactic | `tactics/` | `<id>.tactic.yaml` | A reusable how-to: steps and failure modes. |
| Styleguide | `styleguides/` | `<id>.styleguide.yaml` | Conventions for writing code, docs or prose. |
| Toolguide | `toolguides/` | `<id>.toolguide.yaml` | How to use one tool, with commands. |
| Paradigm | `paradigms/` | `<id>.paradigm.yaml` | A way of working that ties directives together. |
| Procedure | `procedures/` | `<id>.procedure.yaml` | A multi-step process with entry and exit conditions. |
| Agent profile | `agent_profiles/` | `<id>.agent.yaml` | A role an agent can adopt. |
| Mission step contract | `mission_step_contracts/` | `<id>.step-contract.yaml` | What one Mission action must do and produce. |
| Template | `templates/` | any (Markdown etc.) | Document skeletons used by Missions. |
| Asset | `assets/` | `<file>.asset.yaml` + the file | A file shipped with the pack (scripts, gate code). |
| Glossary pack | `glossary_packs/` | `<id>.glossary-pack.yaml` | A set of canonical terms. |
| Skill | `skills/` | `<id>.skill.yaml` + body | A parameterised entry point rendered for agent tools. |
| Anti-pattern | inside other artefacts / the DRG | — | A named failure mode; not a standalone file. |

Packs may also carry `missions/` and `presets/` (see [Contracts](../contracts/index.md)). A
mission type lives in `missions/<type>/<type>.mission-type.yaml`, which holds its steps in run
order. Each step's prompt and guidelines sit next to that file, in `steps/<step>.prompt.md` and
`steps/<step>.guidelines.md`. Content templates sit in `templates/`.

## Directive

```yaml
schema_version: "1.0"
id: DIRECTIVE_043
title: Close Defect Classes by Construction
intent: >
  A repeating defect class signals a missing structural constraint. …
enforcement: required
scope: >
  Applies when a defect class has been identified as recurring …
procedures:
  - Identify the structural gap …
```

Key fields: `id`, `title`, `intent`, `enforcement`, `scope`, `procedures`, `integrity_rules`,
`validation_criteria`, `references`.

## Tactic

Key fields: `id`, `name`, `purpose`, `steps`, `failure_modes`, `references`.

## Styleguide

Key fields: `id`, `title`, `scope`, `applies_to_languages`, `principles`, `patterns`,
`anti_patterns`, `tooling`, `quality_test`.

## Toolguide

Key fields: `id`, `tool`, `title`, `guide_path` (the sibling `<id>.guide.md`), `summary`, `commands`, `last_updated`.

## Paradigm

Key fields: `id`, `name`, `summary`, `directive_refs`.

## Procedure

Key fields: `id`, `title`, `description`, `entry_condition`, `exit_condition`, `steps` (each with a
title, description and optional `role`), `anti_patterns`. Older packs used `name`, `purpose` and
`actor` for `title`, `description` and `role`.

## Agent profile

```yaml
profile-id: curator-carla
name: Curator Carla
description: Knowledge base and doctrine maintenance specialist
roles: [curator]
capabilities: [knowledge-organization, glossary-management, documentation-audit]
purpose: >
  Maintain the health, consistency, and completeness of the project's knowledge base …
```

Key fields: `profile-id`, `name`, `description`, `roles`, `capabilities`, `purpose`,
`specialization`, `collaboration`. Lineage between profiles is a DRG edge
(`specializes_from`), not a profile field.

## Mission step contract

Key fields: `id`, `action`, `mission`, `steps`.

## Asset

Key fields: `id`, `mime`, `path`, `title`. Assets that carry executable code are part of the
pack's trust surface — read the [security position](https://github.com/spec-kitty/spec-kitty-open-packs/blob/main/SECURITY.md).

## Glossary pack

Key fields: `id`, `description`, `provenance`, `terms`.

## Skill

Key fields: `id`, `title`, `description`, `triggers`, `form`, `body_path`, `parameters`,
`invocation`, `version`, `maintainers`. A pack that ships skills needs a `skill_namespace`
([Organisations](../organisations/index.md)); the skill renders as
`<skill_namespace>-<id>/SKILL.md`.

## How artefacts connect

Each pack's DRG fragment declares its artefacts as nodes and their relations as edges
(`requires`, `suggests`, `specializes_from`, …). Activating an artefact can cascade along those
edges (`spec-kitty charter activate <kind> <id> --cascade all`).
