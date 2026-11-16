---
title: Plans
description: "Where the open-packs backlog is going: the living roadmap of themes and horizons, and how it relates to the vision, the tracker and the changelog."
doc_status: active
updated: '2026-11-16'
related:
- plans/roadmap
- architecture/vision
- changelog
---
# Plans

This section says where the work is going and in what order it lands. Each layer owns one question,
and no page repeats what another page owns:

| Question | Owner | Kept current by |
| --- | --- | --- |
| Why does this repository exist, and what does success look like? | [Vision](../architecture/vision.md) | Rarely changes; edited by ADR-level decisions. |
| Which themes are we pursuing, and in which horizon? | [Roadmap](roadmap.md) | A pull request at each horizon review. |
| What is in scope for an epic, and how far along is it? | The [issue tracker](https://github.com/spec-kitty/spec-kitty-open-packs/issues?q=is%3Aissue%20label%3Aepic) | The tracker itself (sub-issues). |
| What has landed? | [Changelog](../changelog/CHANGELOG.md) | Every user-facing pull request. |
| Why was a structural choice made? | [ADRs](../architecture/adr/index.md) | One ADR per decision; superseded, never edited. |

The split is recorded in
[ADR 2026-11-16-1](../architecture/adr/2026-11-16-1-roadmap-and-plans-in-the-docs.md).

## Roadmap

- [Roadmap](roadmap.md): the themes, their horizon (Now, Next, Later), goals and exit criteria, and
  the epics that deliver each theme.

## Progress

Epic progress is a tracker fact, so it is never written into these pages. Rendering it on the
docsite from the tracker at build time is planned in
[doc-kitty#350](https://github.com/spec-kitty/doc-kitty/issues/350). Until then, read it on each
epic in the tracker.

Dated plans that order the next pull requests may be added to this section later. A dated plan is
point-in-time: a newer plan replaces it, and the roadmap stays the living page.
