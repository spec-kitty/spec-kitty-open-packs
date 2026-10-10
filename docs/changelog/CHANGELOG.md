---
title: Changelog
description: Canonical changelog for the Spec Kitty Open Packs repository, following Keep a Changelog and Semantic Versioning.
doc_status: active
updated: '2026-10-10'
type: Changelog
kind: Changelog
sidebar:
  order: 2
  label: Release history
---
# Changelog

<!-- markdownlint-disable MD024 -->

All notable changes to the Spec Kitty Open Packs repository are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

> **🚧 Pre-release.** This repository has no released version yet. It is bootstrapping the
> doctrine-pack marketplace direction in the open. Entries below record the scaffolding as it
> lands; pack boundaries and the manifest schema are still subject to change.

## [Unreleased]

### ✨ Added

- **DocKitty docsite** (ADR-5; refs #19, #20, #25). The repository root is now an Astro project
  built on `@spec-kitty/doc-toolkit@^0.1.1` (Astro + Starlight, Spec Kitty theme). It renders
  `docs/` and publishes to GitHub Pages at `/spec-kitty-open-packs` through
  `.github/workflows/docsite.yml`, which builds on pull requests and deploys from `main`. Section
  order and labels move from the DocFX-era `docs/toc.yml` (removed) to
  `docs/_meta/charter.yaml`. Every page now carries DocKitty `type`/`kind` frontmatter.
- **Generated pack reference** (ADR-2; refs #22, #23). `scripts/docs/generate_pack_reference.py`
  renders one page per pack under `packs/` into `docs/packs/reference/`, plus a catalog index and
  `checksums.json` with a published, re-runnable `sha256` recipe. `--check` fails CI when the
  committed pages drift from the packs. The fixture pack's rendering is pinned by
  `tests/golden/pack-reference/` and `tests/docs/`.
- **`qa` Charter Pack** (`packs/qa/`). A `qa` mission type that redefines the seven canonical
  steps in QA terms, eight QA directives (`QA_001`–`QA_008`), test-design tactics, procedures, five
  QA agent profiles, an ISTQB-grounded glossary, and three evidence tools (`qa-result-ingest`,
  `qa-traceability-lint`, `qa-promise-trace-lint`), plus a promise-page → scenario → acceptance CI
  loop. Ported from `spec-kitty/spec-kitty-qa-pack` at `e9ed31c` via `spec-kitty/private-packs`
  PR #1; the ingester now reads the template-mandated body-fenced test cases
  (spec-kitty-qa-pack#5). See `packs/qa/PROVENANCE.md`.
- **Pack validation CI** (#27). `.github/workflows/validate-packs.yml` runs
  `scripts/ci/validate-packs.sh` on every pull request against a pinned spec-kitty commit: it
  validates each pack under `packs/`, loads all packs together in a scratch project with
  `doctor charter-packs`, and requires the fixtures under `tests/fixtures/invalid/` to fail, so the
  gate cannot pass vacuously.
- **Repository bootstrap.** Initialized `spec-kitty-open-packs` with `spec-kitty init`
  (Claude Code, Codex, Gemini, Copilot surfaces), MIT license, Code of Conduct, security
  position, and the documentation convention mirrored from Spec Kitty core (`toc.yml` nav skeleton,
  frontmatter, root `CHANGELOG.md` / `CONTRIBUTING.md` symlinks, `.github` artifacts).
- **Documentation scaffold.** Added `docs/guides/` with usage guides (use a pack, compose
  packs) and authoring guides (author, validate, publish a pack).
- **Pack catalog proposal.** Added `docs/packs/catalog-proposal.md` — 16 base packs (incl. a
  `spec-kitty-internal` dogfooding pack) + 4 compound stacks, carved from the current built-in
  doctrine corpus and cross-referenced to the core pack-ecosystem epics
  ([#2466](https://github.com/Priivacy-ai/spec-kitty/issues/2466),
  [#2467](https://github.com/Priivacy-ai/spec-kitty/issues/2467)).
- **Tracker seed.** Filed one tracking issue per base pack (open-packs #1–#16) plus a single
  compound-pack epic (#17), with `pack` / `doctrine` / `epic` / `compound-pack` labels.
- **Docsite research & architecture.** Investigated a content-from-code, checksum-tagged docsite
  via a three-lens research squad (feasibility & generator, blockers & core dependencies,
  information architecture) and recorded the outcome under Common Docs structure:
  `docs/research/` (three findings docs), `docs/architecture/` (vision, docsite design), and
  `docs/architecture/adr/` (ADR-1 docsite generator, ADR-2 generated-from-source pack reference,
  ADR-3 build-time checksum tagging, ADR-4 information architecture). Extended `docs/toc.yml`
  with Architecture + Research sections. Decision: **MkDocs Material** — single Python toolchain,
  purpose-built content-from-code plugins, largest OSS ecosystem — with DocFX (consistency-with-core)
  recorded as considered-but-deferred and Hugo rejected; one hand-authored `pack.yaml` is the
  content-from-code prerequisite; generate an interim sha256 content hash pending core verified
  distribution. (ADR-1 revised from an initial DocFX draft following maintainer review.)
- **Docsite tracker tickets.** Opened epic #19 (content-from-code docsite) with scoping children
  #20–#25, cross-referencing core epics
  ([#2314](https://github.com/Priivacy-ai/spec-kitty/issues/2314) pipeline,
  [#2467](https://github.com/Priivacy-ai/spec-kitty/issues/2467) manifest,
  [#2471](https://github.com/Priivacy-ai/spec-kitty/issues/2471) validator,
  [#2539](https://github.com/Priivacy-ai/spec-kitty/issues/2539) trust). Candidate new **core**
  tickets are drafted for HiC approval only and were **not** filed.

### 🔄 Changed

- **ADR-1 (MkDocs Material) is superseded by ADR-5 (DocKitty).** The maintainer chose DocKitty so
  that all Spec Kitty repos share one docs toolchain. ADRs 2–4 stand; ADR-2's generator now emits
  DocKitty pages.
- **Docs frontmatter follows the DocKitty contract.** `doc_status: wip` became `active` for the
  current guides, home, and changelog, and `draft` for the catalog proposal. Over-length
  descriptions were shortened to 180 characters. `related` refs became docs-root-relative slugs,
  and links to repo files moved to `external_references`.
- **Guides follow the Spec Kitty 4.x Charter Pack cutover.** `spec-kitty doctrine …` became
  `spec-kitty charter …`, `doctrine.org.packs` became `charter_packs.org.packs` (with `subdir`
  for packs in this repository), `doctor doctrine` became `doctor charter-packs`, the DRG lives
  in `drg/fragment.yaml`, the directive example matches the schema, and presets replace
  activation defaults. Core links point at `spec-kitty/spec-kitty`.

