---
title: 'ADR: Pack reference is generated from source, not hand-authored'
description: Decision to generate per-pack reference pages and the catalog table from the pack directories plus a new author-facing pack.yaml, so docs cannot drift from source.
doc_status: active
updated: '2026-07-18'
related:
- architecture/docsite-design
- research/docsite-feasibility-and-generator
- research/docsite-information-architecture
---
# Pack reference is generated from source, not hand-authored

**Filename:** `2026-07-18-2-pack-reference-generated-from-source.md`

**Status:** Proposed

**Date:** 2026-07-18

**Deciders:** architect squad (proposed) — pending HiC ratification

**Technical Story:** open-packs docsite epic; grounded in [feasibility research](../../research/docsite-feasibility-and-generator.md)

---

## Context and Problem Statement

The goal requires the docsite to "pull content from the actual code structure (packs, validator)".
A pack is a directory of schema-validated YAML artifacts; per-artifact `id`/`title`/`intent`/
`enforcement` already exist in source. But the catalog wants each pack page to also show a
**purpose** and a **`depends_on`** list — and neither has a source field: `pack-manifest.yaml` is
tooling-written (and hand-editing it is a validator advisory), and `depends_on` has no pack-level
schema in core. We must decide whether pack reference pages are hand-authored or generated, and how
to source the missing pack-level metadata.

## Decision Drivers

* **Docs must not drift from reality** — the highest-volume contribution (new packs) should not
  require, or risk, hand-written reference docs.
* **Low maintenance** for a small OSS team.
* **Decouple from core internals** — importing core's Pydantic models would tie doc builds to core's
  moving internal package layout.
* Content-from-code is the stated goal; hand-authoring pack pages contradicts it.

## Considered Options

* **Generate pack reference from source + a new `pack.yaml`.** Walk `packs/*/`, parse artifacts,
  read a small hand-authored `pack.yaml` for `name`/`purpose`/`depends_on`, run the validator, emit
  pages.
* **Hand-author each pack page.** Contributors write a reference page per pack.
* **Reuse `pack-manifest.yaml` as the metadata source.** Read purpose/deps from the tooling manifest.

## Decision Outcome

**Chosen option:** "Generate pack reference from source + a new `pack.yaml`", because it is the only
option that makes documentation *unable* to drift, eliminates per-pack doc authoring, and keeps the
docsite decoupled from core internals. The generator parses artifact YAML with a **light local
schema** and only shells out to `spec-kitty doctrine pack validate --json` for validation status, so
it does not depend on core's package layout. The single new source-of-truth file is
`packs/<name>/pack.yaml` (`name`, `purpose`, `depends_on: []`, optional `maturity`); everything else
(inventory, counts, checksum, validation) is derived. A **CI regenerate-and-diff gate** fails the
build on any drift between generated output and committed files.

### Consequences

#### Positive

* Adding a pack = a PR with `packs/<name>/` + `pack.yaml` that passes validation; the reference page
  and catalog listing regenerate automatically. Contributors write **zero** reference docs.
* Generated pages carry provenance (validation status, checksum) that hand-authoring could not keep
  honest.
* Doc builds survive core refactors because they parse YAML, not core internals.

#### Negative

* Introduces a new file convention (`pack.yaml`) distinct from the tooling `pack-manifest.yaml` —
  must be clearly documented to avoid confusion.
* The generator (`scripts/docs/generate_pack_reference.py`) is net-new code to build and maintain,
  plus the CI drift gate.
* A thin hand-authored layer remains over the generated validator taxonomy (normative prose lives in
  a core contract, not a machine registry).

#### Neutral

* `pack.yaml` is an interim carrier for `purpose`/`depends_on`; if core #2467 later standardizes
  these fields, the generator's read path changes but the generated-from-source principle does not.

### Confirmation

Validated when the first materialized pack produces a correct reference page and catalog row with no
hand-authoring, and the CI drift gate blocks a deliberately stale commit. Confidence: high for
per-artifact content; medium for pack-level metadata until `pack.yaml` is exercised on a real pack.

## Pros and Cons of the Options

### Generate from source + `pack.yaml`

**Pros:** cannot drift; zero per-pack authoring; decoupled from core; provenance-bearing.
**Cons:** new file convention; net-new generator + gate.

### Hand-author each pack page

**Pros:** no tooling to build.
**Cons:** guaranteed drift; per-pack authoring burden; contradicts the content-from-code goal.
**Rejected.**

### Reuse `pack-manifest.yaml`

**Pros:** no new file.
**Cons:** it is tooling-written (editing is an advisory), carries no `name`/`purpose`/`depends_on`,
and `depends_on` has no schema. Structurally cannot supply what the catalog needs. **Rejected.**
