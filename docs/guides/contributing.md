---
title: Contributing to Spec Kitty Open Packs
description: How to propose, author and submit Charter Packs and docs here, where charter logic lives, and the required check on main.
doc_status: wip
updated: '2026-11-02'
related:
- architecture/adr/2026-11-01-1-merge-queue-readiness-and-pr-pause-ci
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
| Change the pack schemas (`contracts/packs/`) | [`spec-kitty/spec-kitty-charter`](https://github.com/spec-kitty/spec-kitty-charter) |

If you are unsure, open an issue here first and we will help route it. Cross-referencing
between the two repositories is expected.

### Contracts, not core releases

Packs align with the contracts in [`spec-kitty/spec-kitty-charter`](https://github.com/spec-kitty/spec-kitty-charter)
(operator ruling, 2026-11-06). A pack change is gated on those contracts, which
`scripts/ci/validate-packs.sh` and the charter service job check, and not on a Spec Kitty core release. Core becomes
compatible by wiring in the charter service's generated client. Following the contracts, and
using them properly, is the consumer's decision. Neither this repository nor charter is
responsible for it. A pin bump in a consumer, core included, is that consumer's choice.

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
- **Validate before you push.** Run `scripts/ci/validate-packs.sh` (see
  [Validate a pack](validate-a-pack.md)); it checks every pack against the charter pack schemas and must exit `0`.
- **Keep retired names out.** `python3 scripts/ci/check_vocabulary.py` fails on a retired
  doctrine id, the renamed `spec-kitty merge` command (use `spec-kitty consolidate`) or the
  retired governing glossary surface in any pack. The rules are core's; this repository runs
  them on every pack before a change can reach a pin, while core checks only the synced
  built-in and internal trees after a pin bump.
- **Keep it inert where possible.** Prefer data-only artifacts. If a pack must ship an
  executable gate asset, read the [security position](../../SECURITY.md) first and declare
  the executable surface explicitly.

## Documentation conventions

Docs follow the Spec Kitty core convention: Markdown with YAML frontmatter
(`title`, `description`, `doc_status`, `updated`, optional `related`), an ordered nav in `docs/_meta/sections.yaml`
(the nav source of truth, built by doc-kitty/Astro — see [ADR 2026-10-17-1](../architecture/adr/2026-10-17-1-doc-kitty-astro-as-docsite-generator.md)), and
a canonical changelog under `docs/changelog/` symlinked from the repository root.

## Required checks

`main` requires one check before a pull request merges
([ADR 2026-11-01-1](../architecture/adr/2026-11-01-1-merge-queue-readiness-and-pr-pause-ci.md)).
There is no merge queue: in core it duplicated CI runs rather than avoiding reruns.

### What runs where

- **`Validate packs gate`** is the one required check. It comes from
  `.github/workflows/validate-packs.yml`, which runs on every pull request, on `main`, and before a
  release. It covers:
  - pack validation (the per-pack schema pre-check);
  - the charter service validation (every pack composed and registered through the charter service
    at the commit pinned in `charter.lock.yaml`, and every invalid fixture refused);
  - the built-in digest;
  - the vocabulary guard;
  - the generated-pack-page drift check;
  - the tooling tests.
- **`Docs site`** builds the docsite. It runs only when docs, site or pack files change, so it
  cannot be required.

Two pack changes that each re-seed `docs/packs/` can drift once combined. Each passes on its own, so
a clash shows on the push to `main`, where the drift check fails. Fix it with a follow-up pull
request.

### Pausing CI on a parked pull request

During a pile-up, a maintainer can label a parked pull request `pr:pause-ci`:

- Adding the label cancels its running check.
- While the label is on, validation is skipped and `Validate packs gate` fails, so a paused pull
  request never reads as green and cannot merge.
- Removing the label runs CI again.
- A change to any other label re-runs validation, without cancelling the pull request's own run.

### Operator setup (one time)

1. Create a label named exactly `pr:pause-ci`.
2. In **Settings → General → Pull Requests**, keep **Allow rebase merging** on. `main` is linear.
3. Create a ruleset (or branch protection rule) that covers `main`, if none exists, and under
   **Require status checks to pass** require exactly one check: `Validate packs gate`, with
   **GitHub Actions** as its source, so no other integration can post it.
4. Turn off **Require branches to be up to date before merging**. A pull request need not be
   rebased onto every new `main` before it merges; see the note above on a clash.

## Releases

A release is a `vX.Y.Z` [semver](https://semver.org/) tag on a commit on `main`, and it covers
the whole repository. Pushing the tag runs `.github/workflows/release.yml`, which re-runs pack
validation and then publishes one GitHub release with, for **every** pack under `packs/`, a
`<pack>-vX.Y.Z.tar.gz` and its `<pack>-vX.Y.Z.tar.gz.sha256`.

To cut a release:

1. Rename `## [Unreleased]` in the changelog to `## [X.Y.Z] - YYYY-MM-DD`, add a fresh empty
   `## [Unreleased]` above it, and merge that to `main`. The release fails if the changelog has
   no section for the version; that section becomes the release notes. On the first release,
   also remove the changelog's "no released version yet" banner in the same change.
2. Tag the merged commit and push the tag: `git tag vX.Y.Z <sha> && git push origin vX.Y.Z`.

The archives are reproducible: each one is built from the tagged commit's git tree (sorted
entries, fixed mtimes, no owner, fixed gzip header), so rebuilding a tag gives the same
sha256. Build them locally with `scripts/release/release_assets.py build vX.Y.Z --rev HEAD`.
A pack may hold only regular files; a symlink or submodule fails the release. Prerelease tags
(`vX.Y.Z-rc1`) are not released. Assets are uploaded to a draft that is published only once
every archive is present, so a failed run never leaves a half-published release.

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
