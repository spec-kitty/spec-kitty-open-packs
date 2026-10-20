---
title: 'ADR: Semver releases with a reproducible archive per pack'
description: Decision to release spec-kitty-open-packs with repository-wide vX.Y.Z tags that publish a deterministic tar.gz and sha256 for every pack, and never to move or delete a release tag.
doc_status: active
updated: '2026-10-20'
related:
- architecture/adr/2026-07-18-3-build-time-checksum-tagging
- guides/contributing
- guides/publish-a-pack
---
# Semver releases with a reproducible archive per pack

**Filename:** `2026-10-20-1-semver-releases-with-per-pack-archives.md`

**Status:** Accepted

**Date:** 2026-10-20

**Deciders:** maintainers (operator-directed)

**Technical Story:** [open-packs #53](https://github.com/spec-kitty/spec-kitty-open-packs/issues/53);
consumer [core #6492](https://github.com/spec-kitty/spec-kitty/issues/6492)

---

## Context and Problem Statement

Core pins this repository by a raw 40-hex commit and fetches `packs/built-in` and `packs/internal`
with git sparse checkout. Pin bumps are unreadable, there are no release notes per version, and the
sparse-checkout path is fragile (scratch repository, `read-tree`, `core.autocrlf`, lazy fetch). Core
wants to pin `{tag, commit, archive_sha256, tree_digest}` and fetch a verified archive over HTTPS
with no git binary. We need a release unit, an archive format, and a tag policy.

## Decision Drivers

* A whole-archive digest must be checkable before anything is extracted, so archives must be
  byte-reproducible from the tag.
* An archive must equal the pack's subtree at the tagged commit: no extra, missing or linked files.
* Consumers verify against a recorded commit and digest, so a tag that moves breaks them.
* Releasing should not need per-pack bookkeeping while the packs are curated together.

## Considered Options

* **Per-pack tags** (`pack/<pack>/vX.Y.Z`), each releasing one pack.
* **Repository-wide `vX.Y.Z` tags**, each releasing an archive for every pack.
* **Keep commit pins**, with no release process.

## Decision Outcome

**Chosen option:** "Repository-wide `vX.Y.Z` tags", because one tag gives consumers one readable
version with one changelog section behind it, and every pack (`built-in`, `internal`, `qa`,
`event-driven`, `cave-kitty`) ships from the same validated commit.

* `.github/workflows/release.yml` runs on a `vX.Y.Z` tag on a `main` commit. It re-runs pack
  validation, then publishes a GitHub release with `<pack>-vX.Y.Z.tar.gz` and
  `<pack>-vX.Y.Z.tar.gz.sha256` for each directory under `packs/`.
* `scripts/release/release_assets.py` builds each archive from the tagged commit's git tree:
  entries sorted, rooted at `<pack>/`, uid/gid 0 with no owner names, mode 0644 or 0755, mtime
  the commit's committer time, no directory entries, gzip header with no name and mtime 0. A
  symlink or submodule in a pack fails the build.
* The release notes are the `## [X.Y.Z]` changelog section; the release fails without one.
* **A release tag is never moved or deleted, and a published release's assets are never
  replaced.** A bad release is superseded by a new version. Assets are uploaded to a draft that
  is published only once every archive is present.
* Prerelease tags (`vX.Y.Z-rc1`) are not released.

### Which digest proves what

A pack now has up to three integrity values, and each answers a different question:

* **`archive_sha256`** (the published `.sha256`) proves **transport**: the downloaded bytes are
  the published bytes. It covers every file and is checked before anything is extracted. The
  published value is authoritative; nobody needs to rebuild the archive to check it.
* **`tree_digest`** (`spec-kitty-snapshot-sha256`, recorded for `built-in` in
  `packs/built-in.source.yaml`) proves **content identity** after extraction. It hashes every
  file except `pack-manifest.yaml`, so it is not a substitute for the archive digest.
* The **build-time checksum** of [ADR 2026-07-18-3](2026-07-18-3-build-time-checksum-tagging.md)
  stays a docsite-side display of pack content. This ADR does not replace it.

### Consequences

#### Positive

* Core can drop sparse checkout and the git dependency at fetch time (core #6492).
* Pin bumps read as versions, with release notes behind them.
* The archive digest covers every file, including `pack-manifest.yaml`, which `tree_digest`
  skips.

#### Negative

* A change to one pack releases a new version of all of them, even when the others are unchanged.
* Byte-reproducibility relies on the runner's Python `zlib`; a rebuild elsewhere could compress
  differently. The release job's rebuild check only catches nondeterminism within one run. The
  published `.sha256` is authoritative, and `tree_digest` gives content equality across tools.

#### Neutral

* `internal` is released alongside the others; consumers that do not want it ignore its asset.
* This puts a release-time digest beside the build-time checksum of ADR 2026-07-18-3 without
  replacing it (see "Which digest proves what").

### Confirmation

The release job rebuilds every archive and fails if a digest differs, and `tests/release` guards
reproducibility, subtree equality, symlink refusal and the changelog requirement. Core #6492
verifying a fetched asset against its pin confirms the format in use.

## Pros and Cons of the Options

### Per-pack tags

**Pros:**

* A pack's version changes only when that pack changes.

**Cons:**

* Five tag streams and changelogs to maintain while the packs are curated together.
* Core would pin `built-in` and `internal` at unrelated versions.

### Repository-wide tags

**Pros:**

* One version, one changelog section, one validated commit for every pack.

**Cons:**

* Versions bump for packs that did not change.

### Keep commit pins

**Pros:**

* No new workflow.

**Cons:**

* Keeps every problem in the context: unreadable bumps, no notes, fragile sparse checkout.
