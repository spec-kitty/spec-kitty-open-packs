---
title: 'ADR: The roadmap and plans live in the docs, epics stay in the tracker'
description: An authored roadmap of themes in docs/plans names tracker epics by number only; epic scope and progress stay in the tracker.
doc_status: active
updated: '2026-11-16'
related:
- plans
- plans/roadmap
- architecture/vision
- architecture/adr/2026-07-18-4-docsite-information-architecture
- architecture/adr/2026-07-18-2-pack-reference-generated-from-source
---
# The roadmap and plans live in the docs, epics stay in the tracker

**Status:** Accepted

**Date:** 2026-11-16

**Deciders:** Stijn Dejongh (operator)

**Technical Story:** the open epics
[#287](https://github.com/spec-kitty/spec-kitty-open-packs/issues/287),
[#263](https://github.com/spec-kitty/spec-kitty-open-packs/issues/263),
[#207](https://github.com/spec-kitty/spec-kitty-open-packs/issues/207),
[#244](https://github.com/spec-kitty/spec-kitty-open-packs/issues/244),
[#288](https://github.com/spec-kitty/spec-kitty-open-packs/issues/288),
[#190](https://github.com/spec-kitty/spec-kitty-open-packs/issues/190),
[#17](https://github.com/spec-kitty/spec-kitty-open-packs/issues/17),
[#245](https://github.com/spec-kitty/spec-kitty-open-packs/issues/245),
[#294](https://github.com/spec-kitty/spec-kitty-open-packs/issues/294),
[#19](https://github.com/spec-kitty/spec-kitty-open-packs/issues/19); generated progress is
deferred to [doc-kitty#350](https://github.com/spec-kitty/doc-kitty/issues/350).

---

## Context and Problem Statement

The tracker groups the backlog into epics with native sub-issues, but nothing states the direction
those epics serve or which come first, so progress cannot be read against a goal. A dated slice
plan was drafted for this, but it restated issue order and state that the tracker already holds,
and it went stale with the next triage.

[ADR 2026-07-18-4](2026-07-18-4-docsite-information-architecture.md) deferred a `plans/` section
"until it carries content". Direction is authored; epic membership, state and counts are tracker
facts (`DIRECTIVE_044`). Where should each live so that neither is restated?

## Decision Drivers

* `DIRECTIVE_044`: generated evidence and authored explanation never restate the same datum.
* Generated pages are deterministic, committed and drift-gated
  ([ADR 2026-07-18-2](2026-07-18-2-pack-reference-generated-from-source.md)).
* Least maintenance: closing a sub-issue must not require a docs edit.
* Two-way navigation between the published roadmap and each epic.

## Considered Options

* An authored roadmap in `docs/plans/` that names epics by number only; progress is read in the
  tracker, and later rendered by doc-kitty from the tracker at build time.
* The same, plus a generated epic-status page in this repository, rendered from a committed
  tracker snapshot.
* Theme issues in the tracker (epics as their sub-issues), with no roadmap page.
* Dated slice plans only, with no living roadmap.

## Decision Outcome

**Chosen option:** "An authored roadmap that names epics by number only", because it holds only
authored facts (goal, horizon, exit criteria) and leaves every tracker fact in the tracker.
Rendering epic progress on the docsite is doc-kitty's job
([doc-kitty#350](https://github.com/spec-kitty/doc-kitty/issues/350)), so this repository ships no
generator, snapshot or status page.

The layering is:

| Layer | Owns |
| --- | --- |
| [Vision](../vision.md) | Why the repository exists. |
| [Roadmap](../../plans/roadmap.md) | Which themes, their horizon, goal, exit criteria and epic numbers. |
| The tracker | Each epic's scope and progress. |
| [Changelog](../../changelog/CHANGELOG.md) | What landed. |
| ADRs | Why a structural choice was made. |

Conventions:

* `docs/plans/roadmap.md` has a fixed, undated name, because epic bodies link to it.
* Each theme is an H2 heading. Its slug is a published anchor: a theme heading is not reworded
  without updating the epics that link to it.
* A theme's horizon (Now, Next, Later, Done) is an attribute line, never a heading, so moving a
  theme between horizons breaks no link. A Done theme stays in place.
* Each theme has one `Epics:` line naming epics by number, as full issue links (the docsite does
  not autolink `#n`). Every open epic is on exactly one `Epics:` line. No child lists, counts or
  states.
* **Epic back-link.** The first line of each epic's body is
  `**Roadmap:** [<Theme>](https://spec-kitty.github.io/spec-kitty-open-packs/plans/roadmap/#<theme-slug>)`.
  Triage keeps the roadmap and the back-links in step.
* Dated plans may be added under `docs/plans/` later; a newer one replaces an older one, and none
  restates tracker state.

### Consequences

#### Positive

* A `plans` docs section exists, as ADR 2026-07-18-4 allowed once it carried content.
* Epic bodies link to a stable published anchor.
* Closing an issue never needs a docs edit.

#### Negative

* Theme headings become a published contract.
* Until doc-kitty#350 ships, nothing mechanical catches a new epic missing from the roadmap;
  triage carries it.

#### Neutral

* The tracker becomes a source for the docs, through doc-kitty rather than through this repository.

### Confirmation

Every open `epic` issue is named on exactly one `Epics:` line, every epic body carries its
`Roadmap:` back-link, and a horizon review touches only the roadmap page.

## Pros and Cons of the Options

### Authored roadmap, epics by number

**Pros:** no restated tracker data; low maintenance; stable anchors.

**Cons:** progress is not visible on the docsite until doc-kitty#350.

### Generated epic-status page from a committed snapshot

**Pros:** progress on the docsite now.

**Cons:** a second generator and a snapshot to refresh in this repository; duplicates the
build-time tracker support planned in doc-kitty.

### Theme issues in the tracker

**Pros:** everything in one tool.

**Cons:** each theme's goal is written both in an issue and in the vision.

### Dated slice plans only

**Pros:** precise ordering for the next pull requests.

**Cons:** restates issue order and state; stale after each triage; no stable link target for epics.
