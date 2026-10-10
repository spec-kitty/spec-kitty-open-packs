---
title: 'ADR: Docsite information architecture & ADR placement'
description: 'Decision to adopt Common Docs section names, front-load consumers, keep generated reference separate, and nest ADRs under docs/architecture/adr.'
doc_status: active
updated: '2026-07-18'
type: ADR
kind: ADR
related:
- architecture/docsite-design
- research/docsite-information-architecture
- architecture/adr/2026-10-10-5-dockitty-docsite
---
# Docsite information architecture & ADR placement

**Filename:** `2026-07-18-4-docsite-information-architecture.md`

**Status:** Proposed

**Date:** 2026-07-18

**Deciders:** architect squad (proposed) — pending HiC ratification

**Technical Story:** open-packs docsite epic; grounded in [IA research](../../research/docsite-information-architecture.md)

---

## Context and Problem Statement

The docsite serves four audiences (pack consumers, authors/contributors, maintainers/SK Inc.,
evaluators) with different entry points, and must reconcile the existing lean `docs/` tree with
core's adopted Common Docs standard. It must also cleanly separate a **generated** pack/validator
reference from **authored** narrative. Finally, the project brief specifies `docs/architecture/adr/`,
whereas Common Docs and core place ADRs at top-level `docs/adr/` — this placement must be decided
explicitly.

## Decision Drivers

* **Audience-optimized front door** — consumers/evaluators are highest-traffic.
* **Parity with core** conventions (section names, per-dir `index.md`, frontmatter, namespaced
  `doc_status`, anti-sprawl ratchet).
* **Generated ≠ authored** must be structurally visible, not a convention.
* **Respect the explicit project brief** while recording the trade-off against the standard.

## Considered Options

* **Adopt Common Docs section names, scaffold only weight-bearing sections, generated reference under
  `packs/reference/` + `api/`, ADRs at top-level `docs/adr/`.**
* **Same, but ADRs nested under `docs/architecture/adr/`.**
* **Scaffold the full Common Docs section set now** (including empty `operations/`, `integrations/`,
  etc.).

## Decision Outcome

**Chosen option:** "Common Docs section names, weight-bearing sections only, generated reference
under `packs/reference/` + `api/`, **ADRs nested under `docs/architecture/adr/`**", because it honors
the project brief's explicit structure (`docs/architecture` with an `adr` subdirectory) while
front-loading the consumer path and keeping generated evidence physically separate from authored
narrative. Weightless sections (`context/`, `plans/`, `integrations/`, `operations/`,
`configuration/`, `migrations/`) are **deferred** until they carry content, to respect the
anti-sprawl ratchet. ADRs, though nested, surface as their own **top-level `toc.yml` node** so
decisions are not buried inside Architecture.

The research recommendation was top-level `docs/adr/` for maximal tooling parity with core; the brief
overrides this, and the deviation is accepted and recorded here. If shared ADR tooling from core is
later adopted and expects a flat top-level path, this ADR is the migration anchor.

### Consequences

#### Positive

* Matches the project brief exactly (`docs/architecture/`, `docs/architecture/adr/`,
  `docs/research/`).
* Consumer/evaluator path is front-loaded (Guides → Pack Catalog).
* Generated reference (`packs/reference/`, `api/`) is impossible to confuse with authored narrative.
* No empty sections — the tree stays honest and small.

#### Negative

* Diverges from Common Docs/core's top-level `docs/adr/`; any core ADR tooling assuming a flat path
  needs a shim or a later move.
* Two "catalog" surfaces (`catalog-proposal.md` authored vs `packs/reference/` generated) must be
  clearly signposted to avoid perceived duplication.

#### Neutral

* `toc.yml` order is presentational only (no tooling cost), so audience-ordering is free to change.
* Deferred sections can be added incrementally as content appears.

### Confirmation

Validated when the published nav front-loads Guides/Pack Catalog, ADRs appear as a top-level node,
generated pages are visibly marked, and no empty Common Docs section exists. Confidence: high.

## Pros and Cons of the Options

### Weight-bearing sections + nested ADRs (chosen)

**Pros:** matches brief; honest tree; clear generated/authored split.
**Cons:** ADR path diverges from core/standard.

### Weight-bearing sections + top-level `docs/adr/`

**Pros:** maximal parity with core/standard tooling.
**Cons:** contradicts the explicit project brief. **Rejected on brief.**

### Full Common Docs section set now

**Pros:** complete up front.
**Cons:** empty sections trip the anti-sprawl principle core itself enforces. **Rejected.**
