---
title: 'ADR: Strict pack composition and the end of as-is CLI compatibility'
description: Decision that every pack follows the charter service's strict composition rules, and that the packs stop being compatible with the as-is Spec Kitty CLI after the tag pre-charter-cutover.
doc_status: active
updated: '2026-11-05'
related:
- guides/compose-packs
- guides/validate-a-pack
- contracts
- architecture/adr/2026-11-01-1-merge-queue-readiness-and-pr-pause-ci
---
# Strict pack composition and the end of as-is CLI compatibility

**Status:** Accepted

**Date:** 2026-11-04

**Deciders:** Stijn Dejongh (operator)

**Technical Story:** [#118](https://github.com/spec-kitty/spec-kitty-open-packs/issues/118), mission
`strict-pack-composition-01M6M0W4`

---

## Context and Problem Statement

The charter service composes packs strictly. It refuses a pack with no descriptor, and it refuses a
bare reference to an artifact only another pack holds. The packs here predate those rules, so the
service refused every compose of them: a real pack could not be served at all.

The rules cannot be met without breaking the other consumer of these files. The as-is CLI (checked
at `4.0.0rc8`) reads `pack.yaml` with a closed model that has no `depends_on` field, so a descriptor
that satisfies the service is one the CLI rejects. A pack can satisfy one of them, not both.

## Decision Drivers

* The charter service is the product's direction, and until it composes these packs none can be
  served.
* An author should hear about a bad reference in this repository's gate, not at the next charter
  pin bump.
* Keeping both consumers working would need two descriptors or two reference spellings for every
  pack.

## Considered Options

* Follow the service's rules and end compatibility with the as-is CLI.
* Hold the packs back until the CLI reads `depends_on` (spec-kitty/spec-kitty#7153 tracks the core
  side).
* Carry the composition data somewhere the CLI ignores.

## Decision Outcome

**Chosen option:** "Follow the service's rules and end compatibility with the as-is CLI", because
the service is where these packs are going, and any bridge would be a third format to retire.

The tag `pre-charter-cutover` (`f85cf23`) marks the last commit that was semi-compatible with the
as-is CLI. A consumer still on that CLI pins that tag.

### What the packs now follow

**Every pack has a descriptor.** A pack with no `pack.yaml` fails this repository's gate and is
refused by the service.

**Every pack's name is its qualifier.**

| Directory | `name` |
| --- | --- |
| `packs/built-in` | `built-in` |
| `packs/internal` | `spec-kitty-internal` |
| `packs/qa` | `quality-assurance` |
| `packs/event-driven` | `event-driven` |
| `packs/cave-kitty` | `cave-kitty` |

`quality-assurance` differs from its directory on purpose. The operator ruled on the name, over the
proposed `qa` and `spec-kitty-qa`. A qualifier resolves against the descriptor's `name`, never the
directory, so nothing requires the two to match, and `packs/qa` stays where
`.kittify/config.yaml` already registers it.

**Cross-pack references take one of two forms.** Which one depends on where the reference is
written, and the schema refuses the other:

| Where | Form | Example |
| --- | --- | --- |
| An end of a graph edge | `<pack>::<kind>:<id>` | `built-in::tactic:bdd-scenario-formulation` |
| The `id` of a typed reference, which already has a `type` | `<pack>::<id>` | `built-in::domain-event-capture` |

A reference to the pack's own artifact stays bare. A bare reference that no pack holds is not refused
and stays as it is.

**Dependencies are declared by id, with a range.** `internal`, `quality-assurance`, `event-driven`
and `cave-kitty` each declare `depends_on` on `built-in`'s `pack_id` at `>=1.0,<2`: any `built-in`
release of major version 1, and not the next major. `cave-kitty`
writes no checked reference to `built-in`, but declares the dependency because its prompts bind
built-in profiles in prose. `built-in` depends on nothing.

**This repository's gate is an early signal, not a second authority.** `validate_pack_schemas.py`
catches a missing descriptor, a duplicate `pack_id` or `name`, a bare reference held only by another
pack, a qualifier outside the pack's `depends_on` closure, a qualified target that pack does not
hold, and a sidecar naming a payload the pack does not hold. Ordering, levels, version ranges and
sibling rules stay with the service.

### The CLI's charter preflight is off in this repository

`.kittify/config.yaml` sets `preflight: enabled: false` (commit `c8d798d`, an operator decision). The
preflight refused every `implement` with `synthesized_drg missing`. This repository has never had a
synthesized DRG, and synthesizing one needs generated charter artifacts built on the doctrine this
work changes. The cost is that charter freshness is not checked here. This predates the migration
and is not caused by it.

### Consequences

#### Positive

* The service composes the real packs, each with `built-in` and all five together, in the charter's
  own test against these files.
* A bad reference fails this repository's gate on the pull request that writes it.

#### Negative

* **This repository's own governance loses `internal` and `qa` under the as-is CLI, and it does so
  quietly.** The operator accepted this.
  * `.kittify/config.yaml` registers both packs by local path. Because the CLI rejects `depends_on`,
    the whole org DRG layer fails to load, for `internal` and `qa` together. One rejected descriptor
    is enough to lose both.
  * `charter status` still exits 0. The failure shows only in its output, as `org_layer.packs: []`
    with the error in `org_layer.errors`.
  * `charter context` output does not change, so it gives no sign of the loss.
  * `charter org validate <pack>` and `doctor charter-packs` do report it, and name `depends_on` as
    the fault. Both exit non-zero.
  * `charter list` still lists artifacts.
  * This starts when consolidation lands the migrated packs on the repository root checkout. It does
    not happen earlier, while the work sits in lanes.
* Any other project that registers these packs by path, or pins a commit after `pre-charter-cutover`,
  sees the same thing.
* Core's asset resolver (`_anchor_for`) breaks at its next pin bump, because the six `built-in`
  sidecars now name their payload relative to `assets/`. Core's strict composition work is tracked in
  [spec-kitty/spec-kitty#7153](https://github.com/spec-kitty/spec-kitty/issues/7153).

#### Neutral

* 24 references to `built-in` in `quality-assurance`'s agent profiles stay bare. The service does not
  read those fields today, and qualifying them breaks a working stanza in core. Qualifying them needs
  a coordinated charter and core change.
* The charter's pin moves only after this work reaches `main`, because a rebase merge changes the
  commit it would point at.

### Confirmation

The charter's compose test reads these files at the pinned commit, composes each pack with `built-in`
and all five together, asserts the served pack list, and proves that restoring a bare reference or
removing a `depends_on` is refused. High confidence: the proof is the service's own code. The one
exception is `cave-kitty`, which has no checked reference: removing its `depends_on` is not refused,
and is caught only by the test's assertion on the edge the offering serves.

## Pros and Cons of the Options

### Follow the service and end CLI compatibility

**Pros:**

* One format, and the packs can be served.
* The gate and the service agree on what a correct reference is.

**Cons:**

* This repository's own CLI governance loses `internal` and `qa`, quietly, as described above.

### Hold the packs until the CLI reads `depends_on`

**Pros:**

* Nothing breaks here.

**Cons:**

* The service stays unable to serve a real pack for as long as core takes, which this repository
  does not control.

### Carry the composition data where the CLI ignores it

**Pros:**

* Both consumers keep working for a while.

**Cons:**

* The service reads `depends_on` from `pack.yaml` and references where they are written, so this
  needs a translation step and a second source of truth, which would then need retiring too.
