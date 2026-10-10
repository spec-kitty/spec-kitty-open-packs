---
title: Docsite information architecture
description: 'Audience analysis, proposed navigation, and the generated-vs-authored split for the docsite, reconciled with the existing tree and Common Docs.'
doc_status: active
updated: '2026-07-18'
type: Context
kind: Explanation
related:
- research
- architecture/docsite-design
- architecture/adr/2026-07-18-4-docsite-information-architecture
- architecture/adr/2026-10-10-5-dockitty-docsite
---
# Docsite information architecture

> Research capture, 2026-07-18. Grounded in this repo's `docs/` tree, root symlinks, the
> [pack catalog proposal](../packs/catalog-proposal.md), and core's adopted Common Docs standard +
> live `docs/toc.yml`. Feeds
> [ADR-4 (docsite IA)](../architecture/adr/2026-07-18-4-docsite-information-architecture.md).

## Constraints that shape the IA

- The existing tree is lean: `docs/index.md`, `docs/toc.yml`, `docs/guides/` (7 files),
  `docs/packs/catalog-proposal.md`, `docs/changelog/`. Root `CONTRIBUTING.md` and `CHANGELOG.md`
  are symlinks into `docs/`.
- Frontmatter already uses the standard's **namespaced `doc_status`** (not `status`), plus
  `title`/`description`/`updated`/`related`. **Keep this exactly** — do not regress to `status`.
- `packs/` holds only `README.md`; the catalog is proposed, not materialized.
- Core has a working precedent for **generated docs wired into DocFX**
  (`scripts/docs/generate_kitty_specs_docs.py` → a "Mission Runs" toc node) and separates
  hand-authored reference (`docs/api/`) from narrative. This is the template to reuse.
- The defining challenge: separate a small set of stable **hand-authored** pages from a
  **generated** pack/validator reference that must never be edited by hand.

## Audiences & jobs-to-be-done

| Audience | Top job | Entry path | Primary sections |
| --- | --- | --- | --- |
| **Pack consumers** | Pin a pack into `.kittify/config.yaml`, confirm it resolves, pick the right one | `index.md` → Guides (`use`, `compose`) → Pack Catalog | `guides/`, `packs/` |
| **Pack authors / contributors** | Author, validate, publish a pack; understand anatomy + DRG | `index.md` → Guides (`author`, `validate`, `publish`) → Architecture → Reference | `guides/`, `architecture/`, `api/` |
| **Maintainers / SK Inc.** | Keep boundaries coherent, record decisions, govern trust, stay consistent with core | `contributing.md` → ADRs + Research + Architecture + Security | `architecture/adr/`, `research/`, `architecture/`, `security/` |
| **Curious / evaluators** | What is this, why, is it real yet, can I trust a pack? | `README.md` / `index.md` → Pack Catalog → Security → Research | `index.md`, `packs/`, `security/`, `research/` |

**Design implication:** consumers and evaluators are the high-traffic front door → the toc must
front-load **Guides** and **Pack Catalog**, not lead with Context/Architecture the way an internal
engineering repo would.

## Proposed navigation & directory tree

**Stance:** adopt Common Docs **section names + per-dir `index.md` + required frontmatter** (parity
with core), but **only scaffold sections that carry weight**. A content/packaging repo has no real
`operations/`, `integrations/`, `configuration/`, or `migrations/` yet — creating empty ones would
trip the same anti-sprawl principle core enforces. Leave them **deferred** (add when content exists).

```
docs/
├── index.md                         # AUTHORED — start-here home (exists)
├── toc.yml                          # docfx nav (exists; extended)
├── guides/                          # AUTHORED how-tos (exists, unchanged)
│   └── use / compose / author / validate / publish / contributing
├── packs/                           # PACK CATALOG section
│   ├── index.md                     # AUTHORED — how to read a pack page (to add when generator lands)
│   ├── catalog-proposal.md          # AUTHORED — boundaries/roadmap narrative (exists)
│   └── reference/                   # ── GENERATED — DO NOT HAND-EDIT ── (empty until packs materialize)
│       ├── index.md                 #   generated catalog: pack · version · checksum · validation
│       └── <pack-name>.md           #   one page per MATERIALIZED pack
├── api/                             # REFERENCE (tooling contracts) — mirrors core docs/api/ (to add with generator)
│   ├── pack-validator.md            # AUTHORED shell + generated taxonomy/--help
│   └── pack-manifest-schema.md      # GENERATED from core's manifest schema
├── architecture/                    # AUTHORED — ecosystem structure + design (NEW, this task)
│   ├── index.md · vision.md · docsite-design.md
│   └── adr/                         # AUTHORED — decision records (this task; see note)
├── research/                        # AUTHORED — pre-decision investigations (NEW, this task)
├── security/                        # AUTHORED — trust & verifiability position (to add with checksum work)
└── changelog/                       # AUTHORED (exists, unchanged)

Deferred (create only when populated): context/, plans/, integrations/, operations/, configuration/, migrations/.
```

**On ADR placement.** Common Docs canonical and core's live `toc.yml` place `adr/` at the **top
level** (`docs/adr/`). This task's brief, however, explicitly specifies `docs/architecture/adr/`.
The research recommendation is top-level for tooling parity; the **decision taken** (HiC's explicit
instruction) is `docs/architecture/adr/`, surfaced as its own top-level toc node so decisions are
not buried inside Architecture. See
[ADR-4](../architecture/adr/2026-07-18-4-docsite-information-architecture.md).

**The two "catalogs" are different artifacts and must not duplicate:**

- `docs/packs/catalog-proposal.md` = **authored narrative** — *why* these boundaries, *what's*
  coming. Changes only when boundaries change.
- `docs/packs/reference/**` = **generated fact** — one page per *materialized* pack, listing actual
  artifacts + the integrity block. Regenerated from `packs/*/`; never hand-edited. Until packs
  materialize, `reference/` is empty and the proposal carries the section.

### Proposed `toc.yml` top level (audience-ordered)

```yaml
- name: Home            {href: index.md}
- name: Guides          {href: guides/index.md}
- name: Pack Catalog    {href: packs/index.md, items: [Proposed Packs → catalog-proposal.md, Pack Reference → packs/reference/index.md (generated)]}
- name: Reference       {href: api/index.md, items: [Pack Validator, Manifest Schema]}
- name: Architecture    {href: architecture/index.md, items: [Vision, Docsite Design, ADRs → architecture/adr/index.md]}
- name: Research        {href: research/index.md}
- name: Security        {href: security/index.md}
- name: Changelog       {href: changelog/index.md}
```

## Maintenance & contribution model

- **Generated vs authored separation** is the core low-maintenance lever. Everything under
  `docs/packs/reference/**` and the manifest-schema page is emitted by one generator
  (`scripts/docs/generate_pack_reference.py`) modelled on core's `generate_kitty_specs_docs.py`.
  Mark those paths `linguist-generated=true`, give them `doc_status: generated` + a "do not edit"
  banner, and add a **CI regenerate-and-diff gate** (core's "generate → compare → drift = fail"
  pattern).
- **Consistency with core:** same DocFX `toc.yml` mechanism, `index.md` per dir, required
  frontmatter, namespaced `doc_status`, and the anti-sprawl ratchet (single `docs/` root).
- **Community contribution — ideally the contributor writes *no* docs.** Adding a pack = a PR that
  creates `packs/<name>/` in canonical layout and passes `spec-kitty doctrine pack validate`. The
  per-pack reference page and catalog listing **regenerate automatically**; the contributor touches
  zero files under `docs/packs/reference/`. This is the single biggest maintenance win: the
  highest-volume contribution type requires no doc authoring and cannot drift from reality.
- **Checksum display is generated only, never hand-typed:** a "Provenance & integrity" block on each
  generated pack page (version, sha256, trust tier) and a compact column in the generated catalog
  table. The *conceptual* trust model is authored once in `docs/security/pack-trust-model.md`;
  the *values* live only in generated pages. Authored explanation, generated evidence — never duplicated.
