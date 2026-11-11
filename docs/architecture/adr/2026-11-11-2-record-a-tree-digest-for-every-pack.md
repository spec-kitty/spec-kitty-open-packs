---
title: 'ADR: Record a tree digest for every pack'
description: Every pack records a snapshot_sha256 tree digest in its own sidecar, checked fail-closed in the required gate and shipped with each release.
doc_status: active
updated: '2026-11-11'
related:
- packs
- packs/built-in
- architecture/adr/2026-10-20-1-semver-releases-with-per-pack-archives
---
# Record a tree digest for every pack

**Status:** Accepted

**Date:** 2026-11-11

**Deciders:** Stijn Dejongh (operator)

**Technical Story:** [#194](https://github.com/spec-kitty/spec-kitty-open-packs/issues/194) (epic
[#190](https://github.com/spec-kitty/spec-kitty-open-packs/issues/190)), mission
`per-pack-digest-gate-01M75YJ0`

---

## Context and Problem Statement

[ADR 2026-10-20-1](2026-10-20-1-semver-releases-with-per-pack-archives.md) has a consumer pin
`{tag, commit, archive_sha256, tree_digest}`, but only `built-in` recorded a `tree_digest`. Since
the [built-in split](2026-11-11-1-split-built-in-into-foundation-writing-and-opt-in-bundles.md)
`built-in` is a distribution pack that holds no doctrine, so the one recorded digest proves nothing
about the doctrine itself, and an edit to any member or org pack passes the gate unnoticed.

## Decision Drivers

* Every pack's content must be pinned, not only the distribution shell.
* Core reads `packs/built-in.source.yaml` and its recipe; neither may change.
* Parallel pack pull requests must not collide on one shared file.
* Nobody should copy a digest by hand.

## Considered Options

* One map of every pack's digest in `built-in.source.yaml`
* A digest stamp inside each `pack-manifest.yaml`
* A sidecar `packs/<name>.source.yaml` per pack

## Decision Outcome

**Chosen option:** "A sidecar per pack", because it sits outside the hashed tree, so the recipe and
its exclusions stay as they are, it reuses the shape core already reads, and pull requests that touch
different packs touch different files.

Every directory `packs/<name>/` with a `pack.yaml` has `packs/<name>.source.yaml` holding
`tree_digest` with `algorithm: spec-kitty-snapshot-sha256` and the `value`. The recipe is core's
`snapshot_sha256`, unchanged. A missing, stale or orphan sidecar fails the required
`Validate packs gate`. `python3 scripts/ci/pack_digest.py --update` restamps the sidecars, so none is
copied by hand. Each release also carries `<pack>-vX.Y.Z.source.yaml`, the exact sidecar at the tagged
commit. This extends ADR 2026-10-20-1, which is not edited; it does not supersede it.

### Consequences

#### Positive

* Every pack edit is pinned, and an unrecorded change fails the gate.
* A consumer of a release can check each pack's tree against its sidecar.
* `packs/built-in.source.yaml` keeps its path and keys, so core is unaffected.

#### Negative

* Every pack edit restamps one sidecar line, and a rebase over another pack change may need it again.

#### Neutral

* The clean-tree-sha256 recipe and the generated-docs checksum (#23) stay separate decisions.

### Confirmation

A pack edit with no restamp turns the required gate red, and the workflow test fails if the digest
step leaves the required check.

## Pros and Cons of the Options

### One map in `built-in.source.yaml`

* Good, because there is a single file to read.
* Bad, because every pack pull request edits it, and it names the wrong pack for most digests.

### A stamp in `pack-manifest.yaml`

* Bad, because many packs ship no manifest, and the charter schema owns that file.

### A sidecar per pack

* Good, because it is outside the hashed tree and collision-free across pull requests.
* Bad, because it adds one file per pack.
