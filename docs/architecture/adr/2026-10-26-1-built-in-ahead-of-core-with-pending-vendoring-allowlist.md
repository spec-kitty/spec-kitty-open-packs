---
title: 'ADR: Author built-in ahead of core, with a pending-vendoring allowlist'
description: Decision that org packs validate against this repository's built-in, with a report-only pass against the pinned core for an explicit allowlist of ids core has not vendored yet.
doc_status: active
updated: '2026-10-26'
related:
- architecture/adr/2026-10-20-1-semver-releases-with-per-pack-archives
- guides/validate-a-pack
---
# Author built-in ahead of core, with a pending-vendoring allowlist

**Filename:** `2026-10-26-1-built-in-ahead-of-core-with-pending-vendoring-allowlist.md`

**Status:** Accepted

**Date:** 2026-10-26

**Deciders:** maintainers

**Technical Story:** [open-packs #74](https://github.com/spec-kitty/spec-kitty-open-packs/pull/74)

---

## Context and Problem Statement

This repository authors `packs/built-in`, and core later vendors it. Between the two, an org pack
can reference a built-in node that this repository has but the pinned core's bundled built-in
lacks. PR #74 moved a built-in procedure to a directive, and three edges in the internal pack now
target it. Validated against the pinned core, those edges dangle (CI run 40387728946); validated
against this repository's built-in, they resolve, and consumers on a released core still see them
dangle. We need a validation policy that neither blocks authoring nor hides that gap.

## Decision Drivers

* Built-in changes must be able to land here before core vendors them.
* A consumer on a released core must not silently receive dangling edges.
* The gap should be visible, bounded and removable, not a standing exception.

## Considered Options

* **Keep org packs on core's copy** of built-in (the previous behaviour).
* **Hold the edges** in org packs until core vendors the target.
* **Validate against this repository's built-in, plus a report-only pass against the pinned core.**

## Decision Outcome

**Chosen option:** "Validate against this repository's built-in, plus a report-only pass against
the pinned core", because it lets authoring proceed and keeps the consumer-facing gap on record.

* `scripts/ci/validate-packs.sh` sets `SPEC_KITTY_PACKS_ROOT` to `packs/`, so org packs validate
  against the built-in this repository authors. `scripts/ci/check-built-in.sh` still validates
  `packs/built-in` against the pinned core.
* A second `doctor charter-packs` pass runs without the override. Dangling targets listed in
  `scripts/ci/pending-core-vendoring.txt` are `::warning`s; any other dangling edge, error or
  unreadable report fails. A listed id that no longer dangles warns that the entry is stale.
* **Release rule:** no release while the allowlist is non-empty unless the changelog states the
  core version requirement.

### Consequences

#### Positive

* Built-in and the org packs that depend on it can change in one PR.
* The consumer-facing gap is listed in one file and surfaced on every CI run.

#### Negative

* The first pass cannot catch an edge to an id that exists only here; the allowlist does.
* The allowlist is maintained by hand and must be pruned when core vendors an id.

#### Neutral

* Dropping the override and the second pass is the end state, once the allowlist is empty.

### Confirmation

The second pass fails on any dangling target outside the allowlist and on an unparseable report.

## Pros and Cons of the Options

### Keep org packs on core's copy

**Pros:** validates exactly what a consumer on that core sees; no extra machinery.

**Cons:** every built-in change that an org pack references is blocked until a core release.

### Hold the edges until vendored

**Pros:** no dangling edges are ever published.

**Cons:** the org packs lose their relations for the whole lag and need a second PR to restore them.

### Validate here, plus a report-only pass against the pinned core

**Pros:** authoring is unblocked, the gap is explicit and bounded.

**Cons:** a second doctor run and a hand-kept list.
