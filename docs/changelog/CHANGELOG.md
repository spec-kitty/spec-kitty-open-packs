---
title: Changelog
description: Canonical changelog for the Spec Kitty Open Packs repository, following Keep a Changelog and Semantic Versioning.
doc_status: wip
updated: '2026-10-26'
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

- **A vocabulary guard keeps retired names out of every pack** (spec-kitty/spec-kitty#6553).
  Core checks pack content for retired doctrine ids, the renamed `merge` command and the retired
  governing glossary surface, but only over the synced built-in and internal trees and only
  after a pin bump, and this repository had no such check. `scripts/ci/check_vocabulary.py`
  now runs the same rules over every pack in `validate-packs.yml`, with `::error` annotations
  per file and line, and fails when a provenance exemption no longer matches its file. Prose
  where the old command name runs on ("merges", "merged") is not flagged, the same as in core
  (#62). All packs are clean today.

- **Semver releases with a reproducible archive per pack** (#53). Until now this repository
  could only be pinned by a raw commit, with no release notes and a fragile sparse checkout to
  fetch one pack. Pushing a `vX.Y.Z` tag now re-validates the packs and publishes a GitHub
  release with a reproducible `<pack>-vX.Y.Z.tar.gz` and `.sha256` for every pack: `built-in`,
  `internal`, `qa`, `event-driven` and `cave-kitty`. The notes come from the matching changelog
  section, and a release without one fails. The release stays a draft until every archive has
  uploaded. Release tags are never moved or deleted; prereleases are not released.

- **Docsite and README overhaul for the Brain Kitty line.** The README and the docsite now
  describe open packs as the content half of **Brain Kitty**, and show how a pack reaches the
  Spec Kitty CLI: vendored or registered, merged into the **Charter Offering**, activated into
  the **Active Charter**, and served through the charter's entry seams. The landing page is that
  overview. New sections: **Charter artefacts** (the structure of every artefact kind),
  **Organisations** (built-in → org → project tiers, `required_<kind>`, skill namespaces and the
  standard provisionings that ship), **Contracts** (pack, org-charter, preset, manifest and DRG
  files, consumer registration, commands, charter seams), an **architectural overview** and a
  **Glossary**. The nav is reordered with the changelog last, and the site wears an olive Brain
  Kitty colourway over the Spec Kitty theme. Live docs use canonical Charter terminology
  ("doctrine pack" is now "Charter Pack"; the guides moved to `use-a-charter-pack` and
  `author-a-charter-pack`), and links to the retired `Priivacy-ai` organisation now point at
  `spec-kitty`. The site builds on doc-kitty **0.3.0**; the stale `docs/toc.yml` is removed.
- **Published documentation site for the open packs** (#40). `spec-kitty-open-packs` now has a
  browsable, Brain Kitty-branded docs site built with **doc-kitty/Astro** (the same stack as the
  charter site), so anyone adopting a pack has a real home for the material instead of reading
  raw files. It surfaces the existing guides, adds a **packs hub**, and ships
  **generated-from-source per-pack reference** pages — inventory, per-kind counts, validation
  status, and a content checksum derived straight from each pack, kept honest by a CI
  drift gate so the pages can never silently diverge from the packs. A getting-started tutorial
  walks a newcomer through adopting a pack with the `spec-kitty` CLI and a charter. This
  supersedes the earlier MkDocs direction (new ADR
  `2026-10-17-1-doc-kitty-astro-as-docsite-generator`, superseding ADR-1). The site publishes to
  GitHub Pages from `main` once a repo admin turns Pages on (Settings → Pages → Source: GitHub
  Actions).
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
  ([#2466](https://github.com/spec-kitty/spec-kitty/issues/2466),
  [#2467](https://github.com/spec-kitty/spec-kitty/issues/2467)).
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
  ([#2314](https://github.com/spec-kitty/spec-kitty/issues/2314) pipeline,
  [#2467](https://github.com/spec-kitty/spec-kitty/issues/2467) manifest,
  [#2471](https://github.com/spec-kitty/spec-kitty/issues/2471) validator,
  [#2539](https://github.com/spec-kitty/spec-kitty/issues/2539) trust). Candidate new **core**
  tickets are drafted for HiC approval only and were **not** filed.
### 🔄 Changed

- **Red-main discipline is a directive, not a procedure**
  ([spec-kitty-charter#199](https://github.com/spec-kitty/spec-kitty-charter/pull/199)). A
  procedure is a playbook for one situation; the red-main content is a standing rule (no
  green-washing, no release on red, no expensive QA on a red base). The built-in
  `red-main-release-discipline` procedure is now the `RED_MAIN_RELEASE_DISCIPLINE` directive
  (`enforcement: required`), and the internal pack's `spec-kitty-red-main-policy` procedure is
  now the `SPEC_KITTY_RED_MAIN_POLICY` directive that refines it. The substance is unchanged: the
  steps became the directive's procedures, the "do not" statements its integrity rules and the
  exit condition its validation criteria; only a short scope line is new. Every
  DRG edge and reference moved with them (`test-first-bug-fixing`, `DIRECTIVE_030`,
  `NO_FULL_HEAVY_SUITES_IN_MISSION`, `landing-contributor-prs`, the QA go/no-go review, the
  internal glossary), and the built-in manifest and tree digest are regenerated. A consumer
  that activated the procedure by id activates the directive instead. Core still names the old
  procedure id in a curated DRG edge and in tests, so the next core pin bump has to update them.

- **The internal pack's README names the spec-conformant command-skill folders**
  ([spec-kitty#6475](https://github.com/spec-kitty/spec-kitty/issues/6475),
  [spec-kitty#6470](https://github.com/spec-kitty/spec-kitty/issues/6470)). Spec Kitty now
  generates its command skills as `.agents/skills/spec-kitty-<command>` instead of the dotted
  `spec-kitty.<command>`, which several harnesses silently dropped. The recovery note for the
  untracked command-skill ledger now names both forms and warns not to remove the shipped
  `spec-kitty-*` charter skills. Mission-step prompts keep their `/spec-kitty.<command>`
  invocations: they are correct for the slash-command agents, and core rewrites them to the
  skill name when it renders a command skill.

- **The internal pack's tracker-label doctrine matches the 2026-10-19 label clean-up on
  `spec-kitty/spec-kitty`** ([spec-kitty#6503](https://github.com/spec-kitty/spec-kitty/pull/6503)).
  The `spec-kitty-tracker-labels` styleguide no longer offers `bug` or `enhancement` as kind
  labels (kind is the native issue type; `bug`, `enhancement` and `type:*` were deleted), names
  `deferred` instead of the non-existent `future`, adds `triage:needs-decision` (formerly
  `type:decision`), and gains a "Renamed and retired labels" pattern (`domain:merge` →
  `domain:consolidation`, `domain:dashboard` → `domain:status-api`, `domain:hosted` →
  `legacy:hosted`, `documentation` merged into `domain:docs`, and the deleted `squad:*`,
  `needs:*`, `ci:green`/`ci:red`, fleet `from:*` labels outside the provenance set, `launch-window`, `question`, `help wanted`,
  `invalid` and `wontfix`). The `issue-triage-pass` procedure and the `kitty-issue-triage` skill
  no longer call `status:*` fleet-owned: the SkyKitty fleet is switched off, `status:*`,
  `taken-by-human` and `ready-for-squad` are human workflow state, and a triage pass removes
  `status:triage` once an issue is decided. `issue-to-mission-delivery` and
  `landing-contributor-prs` drop their fleet-dispatcher and `squad:*` wording to match.
- **Built-in doctrine no longer sends agents to the closed `docs/adr/3.x/` folder**
  ([spec-kitty#5428](https://github.com/spec-kitty/spec-kitty/issues/5428)). The software-dev
  review prompt pointed reviewers at `docs/adr/3.x/` for architectural intent, and the
  `common-docs-scaffold` tactic used `adr/3.x/` as the home of a new ADR, though that era takes
  no new records. The prompt now names `docs/adr/`, filed by era, and the tactic's examples use
  `adr/4.x/`. `packs/built-in.source.yaml` records the new tree digest.
- **The shared JVM toolguides now apply to Kotlin projects** (spec-kitty/spec-kitty#6444).
  **Before:** `java-supply-chain` and `maven-review-checks` were tagged `java`, so a Kotlin
  project, or one that declares only Gradle or Maven, never received them. **After:** both are
  tagged `jvm`. Core expands `java` and `kotlin` to the `jvm` family when it matches doctrine,
  so Java and Kotlin projects both get them; `java-jenny` and `java-conventions` stay
  Java-only. Needs a core that knows the `jvm` family (spec-kitty/spec-kitty#6444).

- **Org DRG fragments now match the charter's pack schema**
  ([spec-kitty-charter#114](https://github.com/spec-kitty/spec-kitty-charter/issues/114)), so the
  charter service can load every pack here. Before, `packs/internal/drg/fragment.yaml` had 84
  bare-id edge endpoints and the org fragments carried provenance header fields, which that
  schema refuses. Endpoints are now the URNs core already resolved them to
  (`landing-contributor-prs` → `procedure:landing-contributor-prs`), and the fragments drop the
  header fields they carried; core overwrites those from the consumer's registration. Core's
  merged graph is unchanged (461 nodes, 1235 edges). `validate-packs.sh` now fails on a bare-id
  endpoint or a header field, because core still accepts both.
- **The charter step says up front that activation is additive (core `#6408`).** The
  `software-dev` charter prompt never said that interview selections only add to what is
  already active, or that the first activation list is frozen, so later built-ins seemed to go
  missing. It now says so, and names the narrow paths: `charter interview --narrow-activation`,
  `charter activate <kind> <id> --only` and `charter activate --preset minimal`.
- **The `internal` pack declares `pack_level: org`, `active_charter` and `pack_drg` again.**
  Core's loader needs these fields to fetch the pack from this repository
  (spec-kitty/spec-kitty#6451). CI now validates against core `f166339`, which accepts them.
- **The built-in pack now lives at `packs/built-in/`, next to the other packs.** It used to sit at
  the repository root as `built-in/`, with its pin at `built-in.source.yaml`. Both are now under
  `packs/`: `packs/built-in/` and `packs/built-in.source.yaml`. The content and digest are
  unchanged. `validate-packs.sh` skips it, because it is the built-in tier and not an org pack.
  Core's vendoring has to read the new path; spec-kitty/spec-kitty#6451 tracks sourcing it from
  here directly.
- **Guides follow the Spec Kitty 4.x Charter Pack cutover.** `spec-kitty doctrine …` became
  `spec-kitty charter …`, `doctrine.org.packs` became `charter_packs.org.packs` (with `subdir`
  for packs in this repository), `doctor doctrine` became `doctor charter-packs`, the DRG lives
  in `drg/fragment.yaml`, the directive example matches the schema, and presets replace
  activation defaults. Core links point at `spec-kitty/spec-kitty`. Built-in overrides are declared
  as DRG edges and sanctioned in `replaceable-builtins.yaml` (the schemas reject `enhances:` /
  `overrides:` fields), `drg/fragment.yaml` is documented as required, examples use the real `qa`
  pack, and the multi-pack `--include` gap (spec-kitty#5779) is called out.

### 🐛 Fixed

- **The licence names the right copyright holder (#64).** `LICENSE` named `Spec Kitty LLC and
  the Spec Kitty contributors`, but no `Spec Kitty LLC` exists. It now names the legal entity,
  `Spec Kitty, Inc.`. The MIT grant is unchanged, and contributors keep their copyright as before.
- **A PR body without a `closes #<n>` line is a warning, not a failure** (`internal`, #59). The
  `validate-pr-body` asset refused any body without an issue link, which blocked
  decision-recording PRs that legitimately close no issue. A missing link now prints
  `warning: ...` and exits 0, and the match covers GitHub's full keyword set (`close`, `fix`,
  `resolve` and their forms). A real structural violation still fails. The fragment title and the
  `semi-auto-delivery` procedure say the link is advisory. Upstreams the copy vendored in
  spec-kitty-charter (commit `19cc37f`).
- **`plan` missions advance past `specify`.** The `plan` mission's artifact manifest named the
  old phases (`goals`/`structure`/`draft`) and asked for `goals.md`, so `spec-kitty next` blocked
  a committed `spec.md` with `Required artifact missing: spec.md`. The manifest now keys on the
  runtime steps (`specify` → `spec.md`, `research` → `research.md`, `plan` → `plan.md`), and the
  plan `mission.yaml` and README match. Re-seeded from core (spec-kitty/spec-kitty#6395), which
  also absorbs the interim plan step-contract patch below: `built-in/` is byte-identical to core
  again.
- **`plan` missions now compose and run (`#42`).** The built-in pack shipped the `plan` mission
  type but none of its four step contracts, so every `plan` action failed at runtime with
  `No step contract found for mission/action plan/<action>` and plan missions were unusable for
  consumers. The pack now carries `plan-specify`, `plan-research`, `plan-plan`, and `plan-review`
  contracts keyed `mission: plan`, mirroring the `research-*` shape; `plan-review` deliberately
  omits the work-package `move-task` transition and pre-review gate, which a plan mission (no work
  packages) has no use for. Shipped as a deliberate interim override of the byte-identical core
  seed — the gap originates upstream, and the durable fix re-vendors from core via
  spec-kitty/spec-kitty#3504.

