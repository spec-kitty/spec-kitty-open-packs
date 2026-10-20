---
title: Contributing to Spec Kitty Open Packs
description: How to propose, author, and submit Charter Packs and documentation to the Spec Kitty Open Packs repository, including the WIP status and where charter logic lives.
doc_status: wip
updated: '2026-10-20'
related:
- guides/author-a-charter-pack
- guides/validate-a-pack
---
# Contributing to Spec Kitty Open Packs

Thanks for your interest. This repository distributes **open, free Charter Packs** for
[Spec Kitty](https://github.com/spec-kitty/spec-kitty). It is deliberately **early and
in-the-open** — a product-direction shift toward Charter-Packs-as-a-marketplace. Conventions
here will change; contributions that help shape them are welcome.

## What belongs here vs. in core

| You want to… | Contribute to |
| --- | --- |
| Propose or author a Charter Pack | **this repository** |
| Improve a usage or authoring guide | **this repository** |
| Change how charter artefacts are resolved, validated, or composed | [`spec-kitty/spec-kitty`](https://github.com/spec-kitty/spec-kitty) |
| Change the pack manifest schema or the validator | [`spec-kitty/spec-kitty`](https://github.com/spec-kitty/spec-kitty) |

If you are unsure, open an issue here first and we will help route it. Cross-referencing
between the two repositories is expected.

## Proposing a pack

1. Check the [pack catalog proposal](../packs/catalog-proposal.md) and the
   [issue tracker](https://github.com/spec-kitty/spec-kitty-open-packs/issues) — the pack you
   have in mind may already be proposed or in progress.
2. Open an issue using the **Pack proposal** template. Describe the pack's purpose, the
   artifacts it would contain (ideally referencing existing built-in artifacts), any
   `depends_on` packs, and the intended consumer.
3. Once the scope is agreed, author the pack following
   [Author a Charter Pack](author-a-charter-pack.md).

## Authoring standards

- **Namespace your IDs.** Use an organisation/pack prefix so IDs don't collide silently with
  built-in or project charter artefacts. See the authoring guide for the recommended patterns.
- **One rule per file.** Resist dumping a whole policy page into a single artifact — split so
  each rule can be cited individually.
- **Validate before you push.** Run the canonical validator (see
  [Validate a pack](validate-a-pack.md)). Packs must pass with exit code `0`.
- **Keep it inert where possible.** Prefer data-only artifacts. If a pack must ship an
  executable gate asset, read the [security position](../../SECURITY.md) first and declare
  the executable surface explicitly.

## Documentation conventions

Docs follow the Spec Kitty core convention: Markdown with YAML frontmatter
(`title`, `description`, `doc_status`, `updated`, optional `related`), an ordered nav in `docs/_meta/sections.yaml`
(the nav source of truth, built by doc-kitty/Astro — see [ADR 2026-10-17-1](../architecture/adr/2026-10-17-1-doc-kitty-astro-as-docsite-generator.md)), and
a canonical changelog under `docs/changelog/` symlinked from the repository root.

## Releases

A release is a `vX.Y.Z` [semver](https://semver.org/) tag on a commit on `main`, and it covers
the whole repository. Pushing the tag runs `.github/workflows/release.yml`, which re-runs pack
validation and then publishes one GitHub release with, for **every** pack under `packs/`, a
`<pack>-vX.Y.Z.tar.gz` and its `<pack>-vX.Y.Z.tar.gz.sha256`.

To cut a release:

1. Rename `## [Unreleased]` in the changelog to `## [X.Y.Z] - YYYY-MM-DD`, add a fresh empty
   `## [Unreleased]` above it, and merge that to `main`. The release fails if the changelog has
   no section for the version; that section becomes the release notes.
2. Tag the merged commit and push the tag: `git tag vX.Y.Z <sha> && git push origin vX.Y.Z`.

The archives are reproducible: each one is built from the tagged commit's git tree (sorted
entries, fixed mtimes, no owner, fixed gzip header), so rebuilding a tag gives the same
sha256. Build them locally with `scripts/release/release_assets.py build vX.Y.Z --rev HEAD`.
A pack may hold only regular files; a symlink fails the release.

**Tag policy: a release tag is never moved or deleted**, and a published release's assets are
never replaced. Consumers, Spec Kitty core among them, pin a tag together with its commit and
archive digest, so a moved tag breaks their verification. A bad release is superseded by a new
version.

## Code of Conduct

All participation is governed by the [Code of Conduct](../../CODE_OF_CONDUCT.md).

## AI-assisted contributions

Contributions authored with AI coding agents are welcome — this is a Spec Kitty repository.
Please review generated content for correctness and disclose substantial AI assistance in
your PR description.
