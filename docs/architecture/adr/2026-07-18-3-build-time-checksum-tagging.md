---
title: 'ADR: Build-time checksum tagging as an interim integrity mechanism'
description: 'Decision to publish a deterministic per-pack sha256 content hash at docsite build time, as a bridge until core''s verified distribution lands.'
doc_status: active
updated: '2026-07-18'
type: ADR
kind: ADR
related:
- architecture/docsite-design
- research/blockers-and-core-dependencies
external_references:
- url: https://github.com/spec-kitty/spec-kitty-open-packs/blob/main/SECURITY.md
  title: SECURITY.md
---
# Build-time checksum tagging as an interim integrity mechanism

**Filename:** `2026-07-18-3-build-time-checksum-tagging.md`

**Status:** Proposed

**Date:** 2026-07-18

**Deciders:** architect squad (proposed) — pending HiC ratification

**Technical Story:** open-packs docsite epic + checksum-tagging ticket; cross-refs core #2539, #2543, #2540

---

## Context and Problem Statement

The direction requires each pack to be **checksum-tagged** so a downloaded copy can be compared to
the published hash. But **no pack-level checksum mechanism exists in core today**: the only sha256
usage hashes individual artifacts for doctrine versioning. Core's verified-distribution work (#2539
epic, #2543 content-hash integrity) is unstarted, P3, and scoped around the *executable-gate-asset*
trust envelope (#2540) — whereas most proposed open-packs packs are **content-only**. We must decide
how to deliver checksum tagging now without blocking on that upstream schedule.

## Decision Drivers

* The checksum requirement is a first-class goal, not deferrable to "someday core."
* Core's canonical scheme is not available and is scoped for a different (executable-asset) case.
* The docsite is already generated at build time — the natural place to compute a deterministic hash.
* Whatever we ship must **migrate cleanly** to core's canonical scheme when it lands, without a
  second competing standard.

## Considered Options

* **Generate an interim content hash at docsite build time**, publish it, migrate later.
* **Wait for core #2539/#2543** and ship no checksums until then.
* **Invent a bespoke standalone signing/trust system** in open-packs now.

## Decision Outcome

**Chosen option:** "Generate an interim content hash at docsite build time", because it delivers the
requirement immediately, reuses the generation pipeline, and is explicitly a bridge rather than a
competing standard. Mechanics:

* **Computed** deterministically by the generator: `sha256` over the sorted `(relative-path + bytes)`
  of every artifact file in the pack.
* **Displayed** on each generated pack page (a "Provenance & integrity" block) and written to
  `docs/packs/reference/checksums.json`.
* **Verifiable**: the exact hashing recipe is published so a consumer can re-hash a fetched pack and
  compare.
* **Migratable**: when core's verified-distribution scheme lands, the interim tag **defers** to the
  canonical one. The conceptual trust model is authored once in `docs/security/pack-trust-model.md`;
  only the *values* live in generated pages.

This choice also motivates a candidate **core** ticket — *"pack manifest records `pack_id` +
`version` + aggregate content checksum for content-only packs, independent of the executable-asset
trust envelope"* — which is **flagged for HiC approval and NOT filed** (see
[blockers & core dependencies](../../research/blockers-and-core-dependencies.md)).

### Consequences

#### Positive

* Checksum tagging ships now, with no dependency on unstarted core work.
* Tamper-evidence for content-only packs is available to evaluators immediately.
* A clean migration path to core's canonical scheme is defined up front.

#### Negative

* Two integrity notions co-exist until core's scheme lands (interim vs canonical) — must be labelled
  to avoid confusion.
* A build-time content hash without a signed manifest is **tamper-evidence, not tamper-proofing** —
  it detects post-publication modification but is not a full provenance/trust chain.
* The hash is only as stable as the artifact set + the recipe; the recipe must be versioned.

#### Neutral

* Binding the hash to a stable `pack_id`/`version` is stronger once core #2467 lands; until then the
  hash binds to the pack directory contents as committed.

### Confirmation

Validated when a materialized pack's published checksum can be independently reproduced from a fetched
copy using the documented recipe, and a single-byte change flips the hash. Confidence: high for the
mechanism; the *trust* strength is intentionally bounded (evidence, not proof) until #2539/#2543.

## Pros and Cons of the Options

### Interim build-time content hash

**Pros:** ships now; reuses the pipeline; migratable; user-verifiable.
**Cons:** evidence not proof; transitional dual-notion; recipe must be versioned.

### Wait for core #2539/#2543

**Pros:** single canonical scheme.
**Cons:** unstarted, P3, exec-asset-scoped — leaves the requirement unmet indefinitely. **Rejected.**

### Bespoke standalone trust system

**Pros:** maximal control.
**Cons:** duplicates/forks core's future scheme; heavy to build and maintain; likely thrown away.
**Rejected.**
