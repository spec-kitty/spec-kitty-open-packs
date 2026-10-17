---
title: Docsite design — content-from-code publishing with checksum tagging
description: "The architecture of the open-packs docsite: the source-of-truth model, the generation pipeline, the generated-versus-authored boundary, checksum tagging, and the CI drift gate."
doc_status: active
updated: '2026-07-18'
related:
- architecture/vision
- architecture/adr
- research/docsite-feasibility-and-generator
- research/docsite-information-architecture
- research/blockers-and-core-dependencies
---
# Docsite design

The design realizes the [vision](vision.md): a **simple-to-maintain, content-from-code, checksum-
verifiable** docsite. It is grounded in the [feasibility research](../research/docsite-feasibility-and-generator.md)
and structured per the [IA research](../research/docsite-information-architecture.md). Each material
choice is recorded as an [ADR](adr/index.md).

## Design principles

1. **Generated evidence, authored explanation — never both.** Facts derivable from the code (pack
   inventories, checksums, validation status) are **generated**; *why* and *how-to* are
   **authored**. The two must never restate the same datum.
2. **Decouple from core internals.** The generator parses pack YAML with a light local schema and
   only shells out to the CLI for `validate --json`, so the docsite does not depend on core's
   internal package layout ([ADR-2](adr/2026-07-18-2-pack-reference-generated-from-source.md)).
3. **Adopt core's canonical mechanisms as they land.** Interim solutions (own checksum, shelled-out
   validator) are explicitly labelled as bridges to core #2467/#2471/#2539.
4. **One shared docs toolchain across the product line** — Common Docs conventions, doc-kitty (Astro)
   with shared Brain Kitty branding, GitHub Pages
   ([ADR 2026-10-17-1](adr/2026-10-17-1-doc-kitty-astro-as-docsite-generator.md), which supersedes the
   earlier MkDocs Material choice in [ADR-1](adr/2026-07-18-1-mkdocs-material-as-docsite-generator.md)).
   The static-site generator is **decoupled** from the content-from-code generator — the generator
   emits Markdown that any SSG consumes — so adopting the same doc-kitty toolchain as
   `spec-kitty-charter`'s site leaves the generated-versus-authored boundary and checksum design below
   unchanged.

## Source-of-truth model

| Datum | Source of truth | Kind |
| --- | --- | --- |
| Per-artifact `id`/`title`/`intent`/`enforcement` | `packs/<name>/<kind>/*.yaml` | in-repo, upstream-schema'd |
| Pack `name` / `purpose` / `depends_on` | `packs/<name>/pack.yaml` **(new, hand-authored)** | in-repo |
| Activation defaults | `packs/<name>/org-charter.yaml` (optional) | in-repo, upstream-schema'd |
| Artifact inventory & counts | derived by the generator | generated |
| Validation status | `spec-kitty doctrine pack validate --json` | generated |
| Checksum / integrity | sha256 over sorted artifact contents | generated |

The **only new source-of-truth file** is a small `pack.yaml` (`name`, `purpose`, `depends_on: []`,
optional `maturity`). Everything else is derived. This closes the one true feasibility gap:
`purpose`/`depends_on` have no field in the tooling-written `pack-manifest.yaml`
([ADR-2](adr/2026-07-18-2-pack-reference-generated-from-source.md)).

## Generation pipeline

```
SOURCE (versioned)      packs/<name>/{<kind>/*.yaml, pack.yaml, org-charter.yaml?}
        │
GENERATE                scripts/docs/generate_pack_reference.py   (net-new, Python; models core's generate_kitty_specs_docs.py)
  per pack →  read pack.yaml · parse artifacts · validate --json · sha256 · emit docs/packs/reference/<name>.md
  catalog  →  docs/packs/reference/index.md (table: pack · purpose · depends_on · counts · checksum · validation)
  machine  →  docs/packs/reference/checksums.json
  contracts→  docs/api/pack-validator.md (taxonomy + captured --help), docs/api/pack-manifest-schema.md
        │
BUILD                   doc-kitty (Astro) build                   (generated Markdown consumed as-is)
        │
PUBLISH                 GitHub Actions → Pages                    (Pages workflow; generate step precedes build)
```

## Generated vs authored boundary

- **Generated (never hand-edited):** `docs/packs/reference/**`, `docs/packs/reference/checksums.json`,
  the generated portions of `docs/api/pack-validator.md`, `docs/api/pack-manifest-schema.md`, and the
  generated `toc` partial for packs. Marked `linguist-generated=true`, `doc_status: generated`, with
  a "do not edit" banner.
- **Authored (small, stable):** `index.md`, all of `docs/guides/`, `docs/packs/catalog-proposal.md`
  + `docs/packs/index.md`, `docs/architecture/**`, `docs/research/**`, `docs/security/**`,
  `docs/changelog/`.

A **CI regenerate-and-diff gate** runs the generator and fails on any drift between generated output
and committed files (core's "generate → compare → drift = fail" pattern), guaranteeing the docsite
cannot lie about the packs.

## Checksum tagging

There is **no pack-level checksum mechanism in core today** (core's only sha256 use hashes
individual artifacts for versioning). Open-packs therefore generates its **own interim content hash**
now ([ADR-3](adr/2026-07-18-3-build-time-checksum-tagging.md)):

- **Computed** deterministically at build: sha256 over the sorted `(relative-path + bytes)` of every
  artifact file in the pack.
- **Displayed** on each generated pack page (a "Provenance & integrity" block) and in
  `checksums.json`.
- **Verifiable** by consumers: the exact hashing recipe is published so a downloaded pack can be
  re-hashed and compared.
- **Migratable:** when core's verified-distribution scheme lands (#2539/#2543), the interim tag
  defers to the canonical one. The conceptual trust model is authored once in
  `docs/security/pack-trust-model.md`; only the *values* live in generated pages.

## Information architecture

The docsite adopts Common Docs section names with per-directory `index.md` and required frontmatter,
front-loading Guides and Pack Catalog for the high-traffic consumer/evaluator path. Weightless
sections (`operations/`, `integrations/`, `configuration/`, `migrations/`, `context/`, `plans/`) are
**deferred** until they carry content, to respect the anti-sprawl ratchet. Full tree, audience map,
and the original IA proposal are in the [IA research](../research/docsite-information-architecture.md)
and codified in [ADR-4](adr/2026-07-18-4-docsite-information-architecture.md).

Navigation is driven by doc-kitty's `docs/_meta/sections.yaml` section registry (label, order, and
type per top-level section). The earlier DocFX-shaped `docs/toc.yml` is **superseded** and no longer
the navigation source of truth; it is retained only as historical input to the IA.

## Dependencies on core (and how the design avoids blocking on them)

| Need | Core status | Design response |
| --- | --- | --- |
| Stable pack manifest schema (`pack_id`/`version`/`depends_on`) | #2467 planned, not landed | Interim `pack.yaml` in open-packs; adopt core fields when they land |
| Reusable validator surface | #2471 planned; logic exists inside `specify_cli` | Shell out to `spec-kitty doctrine pack validate --json` now; swap to `doctrine-validate` later |
| Checksum / verified distribution | #2539/#2543 planned, P3, exec-asset-scoped | Generate own interim content hash; defer to canonical scheme later |
| Docsite pipeline | core #2314 runs it (DocFX) for core's own site | Reuse the generate → build → Pages *pattern* on the shared doc-kitty (Astro) toolchain ([ADR 2026-10-17-1](adr/2026-10-17-1-doc-kitty-astro-as-docsite-generator.md), superseding [ADR-1](adr/2026-07-18-1-mkdocs-material-as-docsite-generator.md)) |

See [blockers & core dependencies](../research/blockers-and-core-dependencies.md) for the ranked
blocker list and the candidate core tickets flagged for HiC approval.
