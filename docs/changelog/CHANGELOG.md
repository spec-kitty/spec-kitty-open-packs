---
title: Changelog
description: Canonical changelog for the Spec Kitty Open Packs repository, following Keep a Changelog and Semantic Versioning.
doc_status: wip
updated: '2026-10-14'
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

- **`cave-kitty` Charter Pack** (`packs/cave-kitty/`, #35). A "caveman" communication voice as
  opt-in doctrine: an agent answers outcome-first with filler cut, while every payload (code,
  paths, numbers), every negation, and the user's own words stay exact, and it restores full
  sentences at a cliff edge (destructive or irreversible actions, a confused reader). Ships a
  styleguide (`cave-sty-001-communication`), a directive (`CAVE_001`) that governs the agent's
  output prose only, and a `cave-dev` mission type that re-voices the eight-step `software-dev`
  lifecycle without touching its engineering rigour. Activate the voice on `--type software-dev`
  for a clean token-impact comparison, or run `--type cave-dev` for the re-voiced lifecycle —
  note `--type cave-dev` does not inherit software-dev's `next`-loop WP iteration or guards (a
  CLI-level coupling), so the voice-activation path is the instrument for a token A/B.
- **Stable `Validate packs gate` CI check** (#34). The pack-validation workflow now ends in a
  fixed-name gate job, so branch protection on `main` can require one status check that does not
  rename itself when the pinned `spec-kitty` commit is bumped (the old matrix-leg name carried the
  pin). Require `Validate packs gate` as the protected check.
- **`event-driven` Charter Pack** (`packs/event-driven/`). Event-sourced design as opt-in
  doctrine: an `evd-event-sourced-design` paradigm, six directives (`EVD_001`–`EVD_006`: schema
  version on every event, one canonical writer per stream, immutable past-tense facts,
  producers emit the latest version while consumers declare what they accept, side effects in
  consumers, shared contracts only), four tactics (versioning and upcasting, ports-and-adapters
  event bridge, projection replay, idempotent consumers), an event naming and payload
  styleguide, a glossary, an `event-driven` activation preset, and a worked example after
  Martin Fowler's *Event Sourcing* article set on a Spec Kitty lane board. Links to built-in
  `domain-event-capture`, `event-storming-discovery` and related doctrine rather than restating it.
- **Seeded `built-in/`** (#31). The Spec Kitty consumer built-in pack, byte-identical to core
  `packs/built-in/` at `82fee752`, so core can vendor it from a pinned commit here
  (spec-kitty/spec-kitty#3504). It sits outside `packs/` because CI registers every `packs/*`
  directory as an org pack. `built-in.source.yaml` records the source commit, the tree digest
  and the supported core range, and `scripts/ci/check-built-in.sh` validates the pack and checks
  the digest. Core is still where built-in content is edited until the authoring flip.
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
  gate cannot pass vacuously. It also fails when two packs declare the same id (which
  `doctor charter-packs` only reports), runs every spec-kitty call under a throwaway `HOME`, and
  pins its actions by commit SHA.
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

- **Guides follow the Spec Kitty 4.x Charter Pack cutover.** `spec-kitty doctrine …` became
  `spec-kitty charter …`, `doctrine.org.packs` became `charter_packs.org.packs` (with `subdir`
  for packs in this repository), `doctor doctrine` became `doctor charter-packs`, the DRG lives
  in `drg/fragment.yaml`, the directive example matches the schema, and presets replace
  activation defaults. Core links point at `spec-kitty/spec-kitty`. Built-in overrides are declared
  as DRG edges and sanctioned in `replaceable-builtins.yaml` (the schemas reject `enhances:` /
  `overrides:` fields), `drg/fragment.yaml` is documented as required, examples use the real `qa`
  pack, and the multi-pack `--include` gap (spec-kitty#5779) is called out.

