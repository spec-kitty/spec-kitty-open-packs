---
title: Architecture Decision Records
description: Index of architecture decision records for spec-kitty-open-packs, covering the content-from-code docsite direction and its integrity model.
doc_status: active
updated: '2026-10-10'
type: ADR
kind: Hub
sidebar:
  order: 4
related:
- architecture
- architecture/docsite-design
---
# Architecture Decision Records

Durable records of the material decisions behind this repository's architecture. Each ADR captures
context, the options considered, the chosen option, and its consequences.

## Conventions

- **Filename:** `YYYY-MM-DD-N-descriptive-title-with-dashes.md` (`N` = 1, 2, 3… per day).
- **Status:** `Proposed` → `Accepted` → (`Superseded` | `Deprecated`). Superseded files are kept
  for history; do not implement from them.
- Use the [template](../../../.github/ADR_TEMPLATE.md) (kept outside `docs/` so it is not published as a page; copy its frontmatter too).

> **Placement note.** The Common Docs standard and core's live docsite place ADRs at top-level
> `docs/adr/`. This repository nests them under `docs/architecture/adr/` per the project brief,
> while still surfacing them as their own top-level navigation node. The trade-off is recorded in
> [ADR 2026-07-18-4](2026-07-18-4-docsite-information-architecture.md).

## Index

| Date | # | Title | Status |
| --- | --- | --- | --- |
| 2026-07-18 | 1 | [MkDocs Material as the docsite generator](2026-07-18-1-mkdocs-material-as-docsite-generator.md) | Superseded by 5 |
| 2026-07-18 | 2 | [Pack reference is generated from source, not hand-authored](2026-07-18-2-pack-reference-generated-from-source.md) | Proposed |
| 2026-07-18 | 3 | [Build-time checksum tagging as an interim integrity mechanism](2026-07-18-3-build-time-checksum-tagging.md) | Proposed |
| 2026-07-18 | 4 | [Docsite information architecture & ADR placement](2026-07-18-4-docsite-information-architecture.md) | Proposed |
| 2026-10-10 | 5 | [DocKitty (Astro + Starlight) as the docsite toolchain](2026-10-10-5-dockitty-docsite.md) | Accepted |

ADRs 2–4 are **Proposed**: they come from the 2026-07-18 docsite research and are waiting for HiC
ratification. ADR-1 (MkDocs Material) was never implemented and is **superseded** by ADR-5, which
the maintainer decided: the docsite uses DocKitty, the toolchain shared across Spec Kitty repos.
ADR-2's generator stays in force; it now emits DocKitty pages under `docs/packs/reference/`.
