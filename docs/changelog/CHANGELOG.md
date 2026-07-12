---
title: Changelog
description: Canonical changelog for the Spec Kitty Open Packs repository, following Keep a Changelog and Semantic Versioning.
doc_status: wip
updated: '2026-07-12'
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

- **Repository bootstrap.** Initialized `spec-kitty-open-packs` with `spec-kitty init`
  (Claude Code, Codex, Gemini, Copilot surfaces), MIT license, Code of Conduct, security
  position, and the documentation convention mirrored from Spec Kitty core (docfx `toc.yml`,
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
