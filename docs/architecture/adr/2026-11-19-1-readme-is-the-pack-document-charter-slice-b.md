---
title: 'ADR: README.md is the pack document, and org-charter.yaml is retired (charter slice B)'
description: Each pack's root README.md is its only document; pack.md, PROVENANCE.md, org-charter.yaml and active_charter are retired, and org enforcement is a governing preset, following charter slice B.
doc_status: active
updated: '2026-11-19'
related:
- contracts
- guides/author-a-charter-pack
- organisations
- architecture/adr/2026-11-04-1-strict-pack-composition-and-the-end-of-cli-compatibility
---
# README.md is the pack document, and org-charter.yaml is retired (charter slice B)

**Status:** Accepted

**Date:** 2026-11-12 (landed in [PR #248](https://github.com/spec-kitty/spec-kitty-open-packs/pull/248));
recorded 2026-11-19

**Deciders:** Stijn Dejongh (operator)

**Technical Story:** [#241](https://github.com/spec-kitty/spec-kitty-open-packs/issues/241),
[#242](https://github.com/spec-kitty/spec-kitty-open-packs/issues/242); charter
[#451](https://github.com/spec-kitty/spec-kitty-charter/issues/451),
[#431](https://github.com/spec-kitty/spec-kitty-charter/issues/431) and
[PR #501](https://github.com/spec-kitty/spec-kitty-charter/pull/501); mission
`charter-slice-b-migration-01M78K20`; epic
[#287](https://github.com/spec-kitty/spec-kitty-open-packs/issues/287)

**Supersedes:** no ADR. [ADR 2026-11-04-1](2026-11-04-1-strict-pack-composition-and-the-end-of-cli-compatibility.md)
still holds: this decision changes which documents a pack holds, not its descriptor or its
reference forms.

---

## Context and Problem Statement

Before this change a pack described itself in up to three documents: a root `README.md`, a
`pack.md`, and a `PROVENANCE.md`. Twelve packs also carried an `org-charter.yaml` (required lists
and a `skill_namespace`), pointed at by `active_charter` in `pack.yaml`.

Charter slice B (charter PR #501) changed the pack file model. At charter `17ce3f9` the service
refuses `pack.md`, `PROVENANCE.md` and `org-charter.yaml` by name (`retired`), and cannot read a
`pack.yaml` that declares `active_charter`. Moving the pin past slice B therefore required the
packs to move with it, in the same pull request.

## Decision Drivers

* The packs validate against the charter at the pin in `charter.lock.yaml`, and the new pin
  refuses the old files.
* One fact, one home: `pack.md` and the README restated the same description, and the Level,
  `pack_id` and Depends-on bullets restated `pack.yaml`.
* Org enforcement needs a shape the charter reads. Slice B reads a governing preset's
  `must_have: true` items and `policy.yaml`, not `org-charter.yaml`.

## Considered Options

* Follow slice B: the README is the only document, and org enforcement moves to a governing
  preset.
* Keep the old files and hold the pin before slice B.

## Decision Outcome

**Chosen option:** "Follow slice B", because the repository aligns to the charter, and the
service at the new pin refuses the old files. The operator chose the pin `17ce3f9` (a commit pin;
the charter had no release then).

What changed, in all 19 packs:

* **Each pack's root `README.md` is its only document.** `pack.md` is merged into it, and
  `PROVENANCE.md` is folded in as a `## Provenance` section. Both files are gone. The README
  preamble holds only the description, because the generated pack page takes its Purpose from it;
  contents and adoption prose sit under H2 sections.
* **`org-charter.yaml` and `active_charter` are gone** from the 12 packs that had them and from
  the valid fixture.
* **Org enforcement is a governing preset plus `policy.yaml`.** `internal`'s 18 required ids are
  `must_have: true` items of its governing `presets/base.yaml`. It has no `policy.yaml`, because
  no list meant "must not change". `skill_namespace` is dropped.
* **The gates follow.** `validate_pack_schemas.py` keys its pre-check on `README.md` and no longer
  allows `PROVENANCE.md`. A new invalid fixture, `tests/fixtures/invalid/retired-pack-document`,
  proves the service refuses a pack that still ships `pack.md` or `PROVENANCE.md`.

### Consequences

#### Positive

* The charter service composes and registers every pack at the new pin, and refuses every invalid
  fixture.
* A pack's description lives in one file, the README, and the generated page reads it from
  there.

#### Negative

* **Spec Kitty core still reads `org-charter.yaml`.** Until core aligns with the charter, a project
  that runs `internal` through core no longer sees its required lists or skill namespace, and core
  applies no `must_have`. Core then reports the committed `kitty-*` skill directories as orphaned,
  and `spec-kitty upgrade` would retire them. This is disclosed in `packs/internal/README.md`
  ("Pack skills"), `.kittify/config.yaml`, the project charter and the CHANGELOG. Following the
  repository's alignment rule, core's gap did not hold the migration back.

#### Neutral

* Validator gaps found by the review squad (`file_not_held` diagnostics, the `ignored` and
  case-variant rules) were deferred to
  [#249](https://github.com/spec-kitty/spec-kitty-open-packs/issues/249).

### Confirmation

At the PR head, `charter_service_check.py` against a `17ce3f9` jar accepted every pack (20
composed, 13 registered and read back) and refused each of the 3 invalid fixtures with its
expected codes, and a census found no `pack.md`, `PROVENANCE.md`, `org-charter.yaml` or
`active_charter` outside the deliberately invalid fixture. High confidence: the proof is the
service's own verdict, and it runs on every pull request since.

## Pros and Cons of the Options

### Follow slice B

**Pros:**

* The packs can move to the new pin, and the service serves them.
* One document per pack.

**Cons:**

* Core's reading of `org-charter.yaml` breaks until core aligns.

### Hold the pin before slice B

**Pros:**

* Core keeps reading `org-charter.yaml`.

**Cons:**

* The packs fall behind the charter, which owns the pack logic, and every later charter change
  stacks on top of this one.
