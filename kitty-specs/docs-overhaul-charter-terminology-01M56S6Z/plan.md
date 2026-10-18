# Plan — Docsite & README overhaul

Spec: [spec.md](spec.md) · Grounding: [research.md](research.md)

## Information architecture (nav order, `docs/_meta/sections.yaml`)

| Order | Section (`docs/<id>/`) | Divio type | Content |
| --- | --- | --- | --- |
| — | `index.md` (site root) | Explanation | Overview: Brain Kitty, packs → Charter Offering → Active Charter → CLI. |
| 10 | `packs/` | Reference | Catalog hub + generated per-pack pages (unchanged mechanism). |
| 20 | `guides/` | How-to / Tutorial | Existing guides, renamed `use-a-charter-pack`, `author-a-charter-pack`. |
| 30 | `artefacts/` | Reference | One page: structure per artefact kind. |
| 40 | `organisations/` | Explanation + how-to | Multi-tier packs, org charter, standard provisionings. |
| 50 | `contracts/` | Reference | Pack/org/preset/manifest/config schemas, validator CLI, charter seams. (`contracts/`, not `api/`, avoids confusion with the toolkit's `/api/*.json` agent routes.) |
| 60 | `architecture/` | Explanation | New `overview.md`; existing vision, docsite design, ADRs. |
| 70 | `research/` | Research | Unchanged (historical). |
| 80 | `glossary/` | Reference | Canonical terms. |
| 90 | `changelog/` | Changelog | Last. |

## Toolkit bump (0.2.0 → 0.3.0)

- Remove `indexBasename` from `docKittyDocsLoader` (`site/src/content.config.ts`).
- CLI scripts read index names from `astro.config.*`; pass `--astro-config astro.config.mjs` in `validate`.
- Confirm no `README.md` + `index.md` pair in one folder.

## Terminology

Classify each "doctrine" occurrence: governing sense → Charter / Charter Pack / Charter Offering / Active Charter; domain sense (doctrine artifact, DRG) → keep; historical (CHANGELOG entries, ADRs, research, archived missions) → keep.

## Verification

`npm run validate`, `npm run build` (local tarball of v0.3.0), `gen_pack_reference.py --check`, `pytest tests/docs`.
