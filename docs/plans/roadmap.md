---
title: Roadmap
description: "The themes open-packs is pursuing, the horizon each sits in, what done looks like, and the tracker epics that deliver each theme."
doc_status: active
updated: '2026-11-16'
related:
- plans
- architecture/vision
- changelog
---
# Roadmap

<!--
AUTHORING RULES (keep this comment; it is the maintenance contract)
- Authored only: goals, horizon and its reason, exit criteria, what a theme waits on.
- Epics are named by number only (as issue links; the docsite does not autolink #n), on the
  one "Epics:" line per theme. Every open epic is on exactly one Epics line. Never list an
  epic's children, counts, open/closed state or percentages here: the tracker owns those
  (doc-kitty#350 will render them).
- A theme heading is a published anchor that epic bodies link to. Do not reword a heading;
  if a theme must be renamed, update the "Roadmap:" line of every epic on its Epics line
  in the same session.
- Horizons are an attribute of a theme, never a heading, so moving a theme between
  horizons never breaks a link.
- Bump `updated:` only when the roadmap was re-checked against the tracker (horizon review),
  not for a typo fix.
-->

The roadmap turns the [vision](../architecture/vision.md) into themes. Each theme has one horizon:

- **Now**: being worked on.
- **Next**: starts when a Now theme finishes or its blocker clears.
- **Later**: agreed direction, not yet scheduled.
- **Done**: every epic is closed and the exit criteria hold. The section stays in place (its
  heading is a published anchor), cut down to the goal and a pointer to the
  [changelog](../changelog/CHANGELOG.md).

Scope and progress live in the tracker: each epic's sub-issues are its scope, and GitHub shows their
progress on the epic. Open the [epics in the tracker](https://github.com/spec-kitty/spec-kitty-open-packs/issues?q=is%3Aissue%20label%3Aepic)
to see all of them at once. Rendering that progress here is planned in
[doc-kitty#350](https://github.com/spec-kitty/doc-kitty/issues/350).

## At a glance

| Horizon | Themes |
| --- | --- |
| Now | [Charter lockstep](#charter-lockstep), [Pack content quality](#pack-content-quality), [Doctrine from core](#doctrine-from-core) |
| Next | [Catalog shape and publication](#catalog-shape-and-publication) |
| Later | [Docsite and trust](#docsite-and-trust) |
| Done | none yet |

## Charter lockstep

**Horizon:** Now. The charter owns the pack schemas and their validation, so every other theme
builds on the charter commit this repository pins; moving that pin first keeps later changes small.

**Goal:** "This repository aligns to the charter (spec-kitty-charter), not to spec-kitty core"
(AGENTS.md), and packs follow the charter through one pin, a charter release by default
([vision](../architecture/vision.md#division-of-responsibility)).

**Epics:** [#287](https://github.com/spec-kitty/spec-kitty-open-packs/issues/287)

**Exit criteria:**

- `charter.lock.yaml` pins a charter release or pre-release tag (`service-v*`), its commit and its
  jar digest, and every pack validates against it; charter `main` HEAD is pinned only on demand.
- A scheduled job proposes the next lock bump when the charter moves and the gates are green, so
  pin moves stay small.
- The local schema-validation bridge is retired once the charter ships a validator this repository
  can call.
- The decisions behind the lockstep and the ownership split are recorded as ADRs.

## Pack content quality

**Horizon:** Now. Consumers adopt what ships today; stale or contradictory content erodes trust in
the catalog faster than missing content does.

**Goal:** "Canonical & curated. SK Inc. maintains and curates the catalog"
([vision](../architecture/vision.md#the-vision-statement)), with docs kept "in sync with shipped
behaviour" (charter, `DIRECTIVE_037`).

**Epics:** [#263](https://github.com/spec-kitty/spec-kitty-open-packs/issues/263),
[#207](https://github.com/spec-kitty/spec-kitty-open-packs/issues/207),
[#244](https://github.com/spec-kitty/spec-kitty-open-packs/issues/244)

**Exit criteria:**

- A re-run of the pack content audit finds no core source paths, core issue numbers, retired CLI
  flags or internal-only ids in consumer packs.
- The mission-type prompts and templates do not contradict the work-package template or the
  styleguides.
- The analyze prompt reads the whole mission corpus and every work-package prompt, and checks
  product coherence, read-only.

## Doctrine from core

**Horizon:** Now for the artefacts other work waits on; the additive rest follows as Next.

**Goal:** "Content ownership is in the packs repositories" (charter, operator ruling 2026-11-16):
new doctrine is authored here, not extracted from core.

**Epics:** [#288](https://github.com/spec-kitty/spec-kitty-open-packs/issues/288)

**Exit criteria:**

- Every tactic, directive, profile and glossary entry still owed by core is authored in a pack here
  and validates.
- No pack points back at core as the source of its content.

## Catalog shape and publication

**Horizon:** Next. The redistribution and the releases start once the charter pin settles; the
stack presets and the graph hygiene are Later inside this theme, because they wait on the
redistribution and on the charter's graph shape.

**Goal:** "Coherent, composable, opt-in packs", with compound stacks shipped as curated presets on
`built-in` ([vision](../architecture/vision.md#the-problem-this-repository-answers)), published as
versioned, checksummed releases.

**Epics:** [#190](https://github.com/spec-kitty/spec-kitty-open-packs/issues/190),
[#17](https://github.com/spec-kitty/spec-kitty-open-packs/issues/17),
[#245](https://github.com/spec-kitty/spec-kitty-open-packs/issues/245),
[#294](https://github.com/spec-kitty/spec-kitty-open-packs/issues/294)

**Exit criteria:**

- Every pack has one clear home, and each remaining catalog idea is built or explicitly parked.
- Each compound stack registers as a preset on `built-in`, and the vision and
  [catalog proposal](../packs/catalog-proposal.md) describe the preset model.
- Every `suggests` edge carries its condition, the graph has no orphan or file-less nodes, and one
  enforcement vocabulary is defined once.
- A tagged semver release publishes every pack as an archive with its checksum, and the release
  cadence and versioning policy are written down.

**Waits on:** the charter graph view, for the graph census.

## Docsite and trust

**Horizon:** Later. The generated reference already ships; the remaining work waits on doc-kitty.

**Goal:** "Documented from source, not by hand" and "Verifiable by checksum"
([vision](../architecture/vision.md#the-vision-statement)).

**Epics:** [#19](https://github.com/spec-kitty/spec-kitty-open-packs/issues/19)

**Exit criteria:**

- The docsite publishes per-pack checksums, the versioned install recipe and the trust model.
- The schema reference pages are generated from the pinned charter schemas.
- The pack pages are rendered by doc-kitty, retiring this repository's own page generator.
- A gate flags authored pages whose `updated:` date has gone stale.

**Waits on:** pack-page support in doc-kitty.
