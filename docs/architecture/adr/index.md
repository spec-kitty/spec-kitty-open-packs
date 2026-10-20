---
title: Architecture Decision Records
description: Index of architecture decision records for spec-kitty-open-packs, covering the content-from-code docsite direction and its integrity model.
doc_status: active
updated: '2026-10-20'
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
- Use the [template](adr-template.md).

> **Placement note.** The Common Docs standard and core's live docsite place ADRs at top-level
> `docs/adr/`. This repository nests them under `docs/architecture/adr/` per the project brief,
> while still surfacing them as their own top-level navigation node. The trade-off is recorded in
> [ADR 2026-07-18-4](2026-07-18-4-docsite-information-architecture.md).

## Index

| Date | # | Title | Status |
| --- | --- | --- | --- |
| 2026-07-18 | 1 | [MkDocs Material as the docsite generator](2026-07-18-1-mkdocs-material-as-docsite-generator.md) | Superseded |
| 2026-07-18 | 2 | [Pack reference is generated from source, not hand-authored](2026-07-18-2-pack-reference-generated-from-source.md) | Proposed |
| 2026-07-18 | 3 | [Build-time checksum tagging as an interim integrity mechanism](2026-07-18-3-build-time-checksum-tagging.md) | Proposed |
| 2026-07-18 | 4 | [Docsite information architecture & ADR placement](2026-07-18-4-docsite-information-architecture.md) | Proposed |
| 2026-10-17 | 1 | [doc-kitty (Astro) as the docsite generator](2026-10-17-1-doc-kitty-astro-as-docsite-generator.md) | Accepted |
| 2026-10-20 | 1 | [Semver releases with a reproducible archive per pack](2026-10-20-1-semver-releases-with-per-pack-archives.md) | Accepted |

The 2026-07-18 ADRs emerge from the docsite research and await HiC ratification; they document a
recommended direction, not yet-implemented policy. **ADR 2026-07-18-1 (MkDocs Material) is
Superseded** by [ADR 2026-10-17-1](2026-10-17-1-doc-kitty-astro-as-docsite-generator.md), which
adopts doc-kitty (Astro) as the shared product-line docs toolchain.
