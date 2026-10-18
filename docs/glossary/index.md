---
title: Glossary
description: "Canonical Charter vocabulary used in these docs, aligned with the Spec Kitty core glossary."
doc_status: draft
updated: '2026-10-18'
related:
- architecture/overview
- artefacts
- organisations
---
# Glossary

These terms follow the canonical glossary in Spec Kitty core
([`docs/context/`](https://github.com/spec-kitty/spec-kitty/tree/main/docs/context)). If the
two ever disagree, core wins.

## Charter terms

- **Charter** — The governance of a project: its purpose, constraints and norms, and the body of charter artefacts that govern its Missions. It is the governing term — do not say "doctrine" for it.
- **Charter artefact** — One governed unit — a directive, tactic, styleguide, toolguide, paradigm, procedure, agent profile, mission step contract, template, asset, glossary pack, anti-pattern or skill. Also called a *doctrine artifact* in the domain model. See [Charter artefacts](../artefacts/index.md).
- **Charter Pack** — A distributable bundle of charter artefacts and their DRG edges, with optional activation presets. Identified by its `pack_id`; declares its tier in `pack.yaml`.
- **Pack tier** (`pack_level`) — `built-in`, `org` or `project`. Built-in ships with the CLI; org packs are registered by a project; the project layer is the project's own.
- **Compound pack** — A pack that depends on other packs (`depends_on`, planned). Not yet materialised.
- **Org charter** (`org-charter.yaml`) — An org pack's policy file: `required_<kind>` lists and an optional `skill_namespace`.
- **Activation preset** — A named activation bundle a pack ships under `presets/<name>.yaml`. The built-in pack ships `default` and `minimal`.
- **Charter Offering** — Everything offered to a project: the built-in pack, each configured org pack, and the project layer.
- **Active Charter** — What a project has activated from its offering: its `activated_<kind>` keys and mission-type activations. Served by `ActiveCharterService`.
- **Charter context** — The action-scoped guidance the charter renders for a Mission step (`spec-kitty charter context --action <action>`).
- **Doctrine Relationship Graph (DRG)** — The graph of artefacts and their relations (`requires`, `suggests`, `specializes_from`, `enhances`, `overrides`, …). Each layer contributes a fragment; the charter merges them.
- **Pack manifest** (`pack-manifest.yaml`) — The generated inventory of a pack's constituents and content hashes. Never hand-edited.
- **Pack skill** — An artefact of kind `skill`: a thin, parameterised entry point (for example a team command) rendered as `<skill_namespace>-<id>/SKILL.md` into each configured agent tool.

## Product lines

- **Build Kitty** — The open-core delivery line: the free Spec Kitty CLI and its Mission Status Read API.
- **Brain Kitty** — The open-core governance line: the charter and the Charter Packs it serves — this repository and `spec-kitty-charter`.
- **Team Kitty** — The consumer line, "Multiplayer Mode": UI and multiplayer surfaces that consume the open-core APIs.

Brand names are never used as code identifiers.

## Retired terms

| Do not write | Write |
| --- | --- |
| doctrine (as the governing term), doctrine pack | charter, Charter Pack |
| `builtin` | `built-in` |
| feature (for a Mission) | Mission |
