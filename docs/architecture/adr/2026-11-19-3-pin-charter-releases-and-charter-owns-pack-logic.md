---
title: 'ADR: The packs pin a charter release, and the charter owns the pack logic'
description: charter.lock.yaml pins a charter service release by default and charter main only on demand, superseding the 2026-11-16 lockstep with main; the charter owns pack logic, core assembles, pack repositories own content.
doc_status: active
updated: '2026-11-19'
related:
- guides/validate-a-pack
- plans/roadmap
- architecture/vision
- architecture/adr/2026-11-04-1-strict-pack-composition-and-the-end-of-cli-compatibility
---
# The packs pin a charter release, and the charter owns the pack logic

**Status:** Accepted

**Date:** 2026-11-18 (pin policy); 2026-11-16 (ownership); recorded 2026-11-19

**Deciders:** Stijn Dejongh (operator)

**Technical Story:** epic [#287](https://github.com/spec-kitty/spec-kitty-open-packs/issues/287)
(the [2026-11-18 pin policy comment](https://github.com/spec-kitty/spec-kitty-open-packs/issues/287#issuecomment-6970620025));
[#253](https://github.com/spec-kitty/spec-kitty-open-packs/issues/253) and
[#311](https://github.com/spec-kitty/spec-kitty-open-packs/issues/311); PRs
[#298](https://github.com/spec-kitty/spec-kitty-open-packs/pull/298) (ownership),
[#306](https://github.com/spec-kitty/spec-kitty-open-packs/pull/306) (first release pin),
[#308](https://github.com/spec-kitty/spec-kitty-open-packs/pull/308) (release tracking) and
[#314](https://github.com/spec-kitty/spec-kitty-open-packs/pull/314) (nightly `main` check)

**Supersedes:** the operator's 2026-11-16 ruling that the packs move in lockstep with charter
`main`. That ruling was never recorded as an ADR; it is recorded here, as superseded. No ADR is
superseded.

---

## Context and Problem Statement

`charter.lock.yaml` names the one charter commit every pack check uses: the schema pass, the
charter service check and the charter's round trip (charter ADR-0070). Two questions shape how it
moves.

**Who owns what.** On 2026-11-16 the operator ruled that packs and their schema, structure and
validation are no longer a concern of the core repository. That ruling still stands.

**Which charter the pin follows.** The same day, the operator ruled that the packs track charter
`main` in lockstep. The pin moved to charter `main` `050d780` under that ruling (PR #293). On
2026-11-18 the charter published its first service pre-release, `service-v0.1.0-rc.1`, and the
operator replaced lockstep with a release pin.

## Decision Drivers

The rulings state the policy, not a rationale. The drivers below are the trade-offs between the
options, as the CHANGELOG and the `Charter track` workflow describe them.

* A pin must name the same code tomorrow, and a pull request gate should not go red because of an
  unreleased charter change.
* Pack authors should still hear early about what charter `main` is about to change.
* One repository owns each concern: logic, assembly and content are not split across owners.

## Considered Options

* Lockstep with charter `main` (the 2026-11-16 ruling).
* Pin a charter release by default, and check charter `main` on demand and nightly, without
  bumping the lock.
* Pin a commit and bump by hand, with no tracking.

## Decision Outcome

**Chosen option:** "Pin a charter release by default" (the operator's ruling). A release is a
versioned, digest-checked artifact. The pull request gate then moves only when a release does, while the
on-demand and nightly runs against `main` keep the early warning.

### Ownership (operator ruling, 2026-11-16)

| Repository | Owns |
| --- | --- |
| [`spec-kitty-charter`](https://github.com/spec-kitty/spec-kitty-charter) | The pack logic: schemas, structure, validation, resolution, the DRG, activation. |
| [`spec-kitty`](https://github.com/spec-kitty/spec-kitty) (core) | The deployable assembler. A core release is never a gate for pack work. |
| Pack repositories, this one included | The content. |

### Pin policy (operator ruling, 2026-11-18)

* **The pull request gate pins a charter service release or pre-release.** The lock carries
  `release_tag`, `jar_sha256` and `commit`, the commit that tag points at. The `Charter service
  validation` job downloads the release jar and refuses any other digest. The round trip runs from
  the charter source at the tagged commit.
* **Charter `main` HEAD is pinned only on demand**, as a commit with `release_tag` and
  `jar_sha256` empty.
* **The `Charter track` workflow follows the charter** (#253, PR #308; #311, PR #314):
  * daily, it checks the newest service release. From `main` of this repository, it opens one
    bump pull request when the packs pass, or one `charter:release-red` issue when they fail;
  * on demand (a `track: ref` dispatch, or the `charter:head` label on a pull request), it checks
    the packs against unreleased charter, `main` by default, and only reports;
  * nightly, it checks charter `main`, and keeps one `charter:main-red` issue open while that
    fails.
  * The `main` runs never bump the lock, and none of these runs is a required check.

The first release pin, `service-v0.1.0-rc.1` at commit
`ebce9083cc132c4cc7f7602f8b8681b933dac98a`, landed in PR #306.

### Consequences

#### Positive

* The required check moves only when a release does, and the lock names a digest-checked jar.
* Breaking charter changes still show up before they are released: on the nightly
  `charter:main-red` issue, or on a pull request labelled `charter:head`.

#### Negative

* The packs can trail charter `main`. A charter change the packs need waits for a charter release,
  or for an on-demand `main` pin.
* Two red signals (`charter:release-red` and `charter:main-red`) need watching.

#### Neutral

* Each charter contract change still gets one migration issue under epic #287, landed with the pin
  move that needs it.

### Confirmation

The lock carries a release pin (`service-v0.1.0-rc.1`). The decision is working when bump pull
requests arrive from the release track and land green, and when `charter:main-red` issues show
charter changes before they are released. Medium confidence until the first scheduled bump
lands.

## Pros and Cons of the Options

### Lockstep with charter `main`

**Pros:**

* The packs never trail the charter.

**Cons:**

* Every charter merge can turn the required check red, and the pin names no released artifact.

### Release pin, with `main` checked on demand and nightly

**Pros:**

* A stable, digest-checked gate, and still an early signal from `main`.

**Cons:**

* The packs can trail `main`, and there is more workflow to maintain.

### Commit pin, bumped by hand

**Pros:**

* No automation.

**Cons:**

* Nobody hears about a charter change until someone bumps the pin by hand.
