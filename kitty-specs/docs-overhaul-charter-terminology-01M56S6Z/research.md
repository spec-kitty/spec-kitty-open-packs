# Research & grounding note — docs overhaul (Charter terminology, Brain Kitty)

Read-only grounding pass, committed before any spec. Date: 2026-10-18. CLI: `spec-kitty-cli 4.0.0rc7`.

## Scope as agreed with the operator

- Target repository: `spec-kitty-open-packs` (operator confirmed; the brief's "spec-kitty-events" was a slip).
- Draft PR spec-kitty/spec-kitty-open-packs#29 (`docs/dockitty-docsite`) is **superseded** by this work (operator decision); the docsite it proposed is already on `main` via mission `docsite-bootstrap-01M55JVF`.
- doc-kitty is bumped to the latest release, **v0.3.0** (tag 2026-10-14). The GitHub Packages registry needs a `read:packages` token this session lacks; local verification uses a tarball packed from the `v0.3.0` tag, CI is the authoritative build proof.

## Sizes and responsibility map

| Surface | Size | Responsibility |
| --- | --- | --- |
| `README.md` | 147 lines | Repository front door; WIP banner, "doctrine packs" framing. |
| `docs/` | ~3.4k lines, 33 files | Authored guides/architecture/research + 5 generated pack pages. |
| `docs/_meta/sections.yaml` | 5 sections | **The nav source of truth** (doc-kitty ADR-0004). |
| `docs/toc.yml` | — | Stale DocFX leftover; superseded by `sections.yaml` per ADR `2026-10-17-1`. Lists Changelog, which `sections.yaml` omits. |
| `site/` | Astro + `@spec-kitty/doc-toolkit@0.2.0` | Renders `../docs`; base `/spec-kitty-open-packs`; no `/docs` URL segment. |
| `scripts/docs/gen_pack_reference.py` | 640 lines | Generates `docs/packs/{built-in,cave-kitty,event-driven,internal,qa}.md`; `--check` is the drift gate. |

## Invariants that must survive

- Generated pages are never hand-edited; change the generator, regenerate, `--check` green (charter: generated-evidence/authored split, `DIRECTIVE_044`).
- ADRs are superseded, never silently edited (`DIRECTIVE_003`).
- Canonical terminology (core `docs/context/charter.md:29`): "Never use bare 'doctrine' … the governing term is `charter`". "Doctrine" **survives** as domain vocabulary: *doctrine artifact*, the *Doctrine Relationship Graph (DRG)*, the `doctrine` package history. Each occurrence is classified, not blindly replaced (precedent: core #3732).
- Product lines (core `docs/context/product-lines.md`): **Build Kitty** (CLI + Mission Status Read API), **Brain Kitty** (charter governance line — this repo and `spec-kitty-charter`), **Team Kitty** (consumer "Multiplayer Mode"; hosted surfaces removed in core #6164 — never point users at them). Brand names are never code identifiers.
- Pack tiers: `pack_level` ∈ `built-in | org | project` (`kernel.pack_tiers`). `packs/internal` never ships in the wheel.
- Charter Offering = what a project can draw from (built-in + org packs + project layer); Active Charter = what it activated (`ActiveCharterService`).
- Historical snapshots (changelog entries, ADRs, research notes, archived missions) keep their wording.

## Gates touched and how to keep them green

| Gate | Where | Plan |
| --- | --- | --- |
| Front-matter + source links | `npm run validate` (CI build job) | Every new page gets valid front-matter; renamed guides update all inbound links. |
| Site build | `npm run build` | Migrate to doc-toolkit 0.3.0 (drop loader `indexBasename`; no README+index collisions). |
| Drift gate | `gen_pack_reference.py --check` | Wording change in generator → regenerate → check. Currently green on rc7. |
| Generator tests | `tests/docs/test_gen_pack_reference.py` | Re-run; assertions on the description string must be checked. |
| Pack validation | `validate-packs.yml` | Untouched (no pack content changes). |

## Discovery squad 1 — similar surfaces

| Surface | Disposition |
| --- | --- |
| "doctrine" in README (16 lines) and 27 docs files (147 lines) | In scope: classify and rewrite in live docs; keep in historical changelog/ADRs/research. |
| Generator description string ("doctrine pack") | In scope (generator + regenerate). |
| `site/astro.config.mjs` description, `site/src/pages/llms.txt.ts` | In scope. |
| Guide filenames `use-a-doctrine-pack.md`, `author-a-doctrine-pack.md` | In scope: rename to `*-charter-pack.md`, update inbound links. |
| `docs/toc.yml` | In scope: remove (superseded nav). |
| `CONTRIBUTING.md`, `SECURITY.md`, issue templates | In scope for terminology only where live. |
| Privacii-AI / Priivacy-ai references | Explicit: **none found** (`grep -ri privacii` → 0). |
| Pack content (`built-in/`, `packs/*`) wording | Out of scope (vendored/parity-gated content); not touched. |

## Discovery squad 2 — tracked issues

- Supersedes: open-packs #29 (draft PR).
- Refs: open-packs #19, #21, #23, #24 (content-from-code docsite epic and its slices; the new Contracts section documents the manifest/schema surfaces by hand where not yet generated), #31 (built-in migration), #18 (glossary idea — wording only).
- Refs (core): #6100, #648 (doc-kitty migration), #3022, #3504 (vendoring), #3023/#3505 (internal pack), #2053, #1799 (charter explanation gaps), #3154 (Team Kitty vocabulary).
- Precedent only: core #3732, #4836, #4098 (doctrine→charter), #4562, #4020 (org rename).
- Gaps: no issue tracks Brain/Build Kitty positioning or the doctrine→charter rename inside open-packs; covered by this PR's description.

## Open P0 / sibling-run interactions

None in this repo. Sibling: core #6100 migrates the core docsite to doc-kitty; keep conventions aligned (sections.yaml nav, index basename).

## 90-day churn

Highest: `docs/changelog/CHANGELOG.md` (9), `docs/packs/catalog-proposal.md` (6), `docs/packs/built-in.md` (5, generated). All docs created within the window; low conflict risk once #29 is superseded.
