---
title: Docsite feasibility & generator selection
description: Whether pack and validator reference pages can be generated from the actual code structure, the minimum machine-readable input needed, and a DocFX/Hugo/MkDocs Material comparison.
doc_status: active
updated: '2026-07-18'
related:
- research
- research/blockers-and-core-dependencies
- architecture/docsite-design
- architecture/adr/2026-07-18-1-mkdocs-material-as-docsite-generator
- architecture/adr/2026-07-18-2-pack-reference-generated-from-source
---
# Docsite feasibility & generator selection

> Research capture, 2026-07-18. Grounded in `spec-kitty-open-packs` (`README.md`, `docs/`,
> `packs/`) and the sibling core repo (`src/doctrine/**`, `src/specify_cli/doctrine/**`,
> `docs/docfx.json`, `.github/workflows/docs-pages.yml`). Feeds
> [ADR-1 (docsite generator)](../architecture/adr/2026-07-18-1-mkdocs-material-as-docsite-generator.md) and
> [ADR-2 (generated pack reference)](../architecture/adr/2026-07-18-2-pack-reference-generated-from-source.md).
>
> **Superseded (2026-07-25):** the recommendation below leaned DocFX on *consistency with core*.
> Following maintainer review, [ADR-1](../architecture/adr/2026-07-18-1-mkdocs-material-as-docsite-generator.md)
> revised the decision to **MkDocs Material** (single Python toolchain; consistency-with-core is a
> resource-bounded constraint, not a durable merit). This section is kept as the original analysis of
> record; the ADR is the authoritative decision.

## What a pack is on disk (the raw material)

A pack is a directory with one subdirectory per artifact kind (`directives/`, `tactics/`,
`styleguides/`, `toolguides/`, `paradigms/`, `procedures/`, `agent_profiles/`, `drg/`) plus an
optional `org-charter.yaml`. Each artifact is a **schema-validated, Pydantic-modelled YAML file**
in core:

- **Directive** (`src/doctrine/directives/models.py`): `id`, `schema_version`, `title`, `intent`,
  `enforcement`, optional `scope`.
- **Tactic** (`src/doctrine/tactics/models.py`): `id`, `schema_version`, `name`, `purpose`,
  `steps`, `failure_modes`, `applies_to_languages`, `references`, `opposed_by`.
- Same pattern for the remaining artifact kinds (registry in
  `src/specify_cli/doctrine/pack_validator.py`).

So per-artifact **`id` + `title`/`name` + `intent`/`purpose` + `enforcement`** already exist in
source YAML. That is enough to generate a per-artifact reference table with **no new upstream work**.

## Feasibility verdict

**Highly feasible for per-artifact content; partially blocked for pack-level metadata**
(`purpose`, `depends_on`, checksum), which has no source field today.

### The one true prerequisite: an author-facing `pack.yaml`

The catalog design ([`catalog-proposal.md`](../packs/catalog-proposal.md)) wants each pack page to
show a **purpose** and a **`depends_on`** list. Neither exists as a source field:

- `pack-manifest.yaml` is **written by tooling** (`doctrine fetch`/`assemble`,
  `src/specify_cli/doctrine/snapshot.py`) and hand-editing it is an explicit validator **advisory**.
  It carries `pack_version`, `fetched_at`, `source_type`, `source_url`, `artifact_counts` — no
  `name`, `purpose`, or `depends_on`.
- `depends_on` has **no pack-level schema in core at all** (it exists only on *mission steps*).
- `org-charter.yaml` carries activation defaults, not a description or dependency DAG.

**Fix:** introduce one small, hand-authored, author-facing manifest per pack — `pack.yaml`
(distinct from the tooling-written `pack-manifest.yaml`) — with just `name`, `purpose`,
`depends_on: []`, and optional `maturity`/`status`. Everything else (artifact inventory, counts,
checksum, validation state) is **derived**. Without this single file, `purpose`/`depends_on` on
generated pages would have to be hand-maintained in the docs — exactly what the goal forbids.

### Validator-as-docs is feasible via two surfaces

1. **Per-pack validation result** — `validate_pack(pack_dir).to_dict()` returns
   `{ok, errors[], advisories[]}`, driven by `spec-kitty doctrine pack validate ./pack --json`.
   Run it in the build and embed a pass/fail + advisories block on each pack page.
2. **Validator rule reference** — the issue taxonomy is an enumerable Python-level set
   (`ValidationIssue.category` in `pack_validator.py`), and the error/advisory split is already
   tabulated in [`validate-a-pack.md`](../guides/validate-a-pack.md). This makes the rule reference
   **semi-generated**: taxonomy from code, normative prose from the guide/core contract.

## Generator landscape & recommendation

**Framing that decides everything:** the content-from-code work is a script that emits
**Markdown**, and all three candidate generators consume Markdown. Generation ergonomics are
therefore near-identical; the real engineering is the generator, not the static-site generator
(SSG). The SSG choice is decided by **consistency, maintenance, and contributor familiarity**.

| Criterion | DocFX | Hugo | MkDocs Material |
| --- | --- | --- | --- |
| Content-from-code (emit `.md`) | Equal | Equal | Equal, plus purpose-built `mkdocs-gen-files` / `mkdocstrings` |
| Maintenance for a small OSS team | Low **if** already run; needs .NET SDK | Medium — Go toolchain + Go templates, new to this stack | Low — `pip install`, matches the Python stack the validator/generator use |
| Consistency with core | **Best** — same engine, template, `docs.spec-kitty.ai` | None | None |
| GitHub Pages publish | Proven in core (`docs-pages.yml`) | Well-trodden | Well-trodden (`mkdocs gh-deploy`) |
| Contribution friendliness | Smaller community; must learn `toc.yml` | Large community, Go-template barrier | **Best** — ubiquitous in OSS |
| Already wired here | **Yes** — `docs/toc.yml` + `doc_status` frontmatter | No | No |

Core already operates the exact pattern this task wants:
`.github/workflows/docs-pages.yml` runs **a Python generator (`generate_kitty_specs_docs.py`) that
emits Markdown → `docfx docfx.json` → publish to Pages**. This repo is already half-configured for
DocFX (`docs/toc.yml` is DocFX-shaped; every doc carries `doc_status`/`title`/`description`).

### Recommendation: **DocFX**, with one explicit fallback

Adopt **DocFX** because it is the **lowest *new* maintenance** (the generate → build → Pages
pattern is already operated by the core team and reusable), it is **already wired** here, and
**consistency with core is a stated goal** (one look, one `docs.spec-kitty.ai` presence; open-packs
can be a subsite/subdomain). The content-from-code investment is SSG-agnostic, so DocFX costs
nothing extra on the dimension the task cares most about.

**Fallback — MkDocs Material** — if the repo deliberately prioritizes contributor familiarity and
toolchain independence over brand/pipeline consistency: it aligns with the Python stack the
generator and validator already live in and has the widest contributor base.

**Reject Hugo:** it adds a Go toolchain and Go-template learning curve with no ecosystem-alignment
or consistency payoff for this repo.

## Auto-generation pipeline sketch

```
SOURCE OF TRUTH (in-repo, versioned)
  packs/<name>/{directives,tactics,...}/*.<kind>.yaml   # per-artifact fields (id/title/intent/enforcement)
  packs/<name>/pack.yaml            # NEW hand-authored: name, purpose, depends_on[], maturity
  packs/<name>/org-charter.yaml     # optional activation defaults (defined upstream)
        │
        ▼
GENERATION STEP  (scripts/docs/generate_pack_reference.py — net-new, Python)
  for each pack:
    1. read pack.yaml (name/purpose/depends_on)
    2. glob + parse artifacts → inventory (id, title, intent/purpose, enforcement, counts)
    3. run `spec-kitty doctrine pack validate <pack> --json` → embed ok/errors/advisories
    4. CHECKSUM = sha256 over sorted (relpath + bytes) of all artifact files
    5. emit docs/packs/reference/<name>.md (+ frontmatter: doc_status: generated, checksum)
    6. append to generated docs/packs/reference/index.md (table: pack · purpose · depends_on · counts · checksum · validation)
  also emit docs/api/pack-validator.md content from the category taxonomy + `validate --help`
  also write docs/packs/reference/checksums.json (machine-readable, for user verification)
        │
        ▼
STATIC BUILD   docfx docfx.json        (MkDocs `mkdocs build` under the fallback)
        │
        ▼
PUBLISH        GitHub Actions → Pages  (copy core's docs-pages.yml; add generate step before build)
```

**Where checksum tagging fits:** there is **no pack-level checksum in core today** (see
[blockers](blockers-and-core-dependencies.md)); open-packs generates its own at build,
deterministically (sha256 over sorted artifact contents), shows it on each pack page + in
`checksums.json`, and publishes the exact hashing recipe so consumers can re-run and compare. This
is a local tamper-evidence stopgap that later defers to core's canonical scheme when it lands.

**Hand-authored vs generated:**

- **Hand-authored:** `index.md` (vision), all of `docs/guides/`, the `catalog-proposal.md`
  narrative, `changelog/`, `SECURITY.md`, the architecture/research/adr docs.
- **Generated (never hand-edited):** per-pack reference pages, the catalog *table*, the validator
  rule reference, captured CLI `--help`, and `checksums.json`. Generated `toc` entries for packs
  should be a generated partial merged into `docs/toc.yml`.

## What's missing today (gaps carried into blocker analysis)

1. **No author-facing pack manifest** (`purpose`/`depends_on` have no source field). *The one true
   prerequisite* — fix with a minimal `pack.yaml` in open-packs.
2. **No packs materialized** — `packs/` holds only `README.md`; the generator has nothing to run
   against until the first pack lands.
3. **No pack-level checksum in core** — open-packs must define and generate its own content hash.
4. **No doctrine-artifact → docs generator exists anywhere** — net-new script (core's
   `generate_kitty_specs_docs.py` generates from `kitty-specs/`, not doctrine YAML).
5. **Validator rule reference is only semi-generatable** — expect a thin hand-authored layer over
   the generated taxonomy.
6. **open-packs has no `docfx.json` and no docs CI workflow** — only `toc.yml` + frontmatter; the
   core template must be vendored/shared and a Pages workflow added.
7. **Cross-repo version coupling risk** — prefer parsing pack YAML with a light local schema in the
   generator and only shelling out to the CLI for `validate --json`, to decouple the docsite from
   core's internal package layout.

These gaps are triaged and mapped to owners in
[Blockers & core dependencies](blockers-and-core-dependencies.md).
