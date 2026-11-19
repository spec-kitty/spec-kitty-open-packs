---
title: 'ADR: Step contracts fold into steps, steps are linked, delegations are scoped (charter slice F)'
description: Following charter slice F (ADR-0077), step contracts become the substeps of their steps, every step is linked from its mission type, and every delegation candidate has a scope edge.
doc_status: active
updated: '2026-11-19'
related:
- artefacts
- guides/author-a-charter-pack
- architecture/adr/2026-11-11-1-split-built-in-into-foundation-writing-and-opt-in-bundles
---
# Step contracts fold into steps, steps are linked, delegations are scoped (charter slice F)

**Status:** Accepted

**Date:** 2026-11-17 (the pin move landed in
[PR #293](https://github.com/spec-kitty/spec-kitty-open-packs/pull/293); the additive items in
[PR #289](https://github.com/spec-kitty/spec-kitty-open-packs/pull/289) on 2026-11-16); recorded
2026-11-19

**Deciders:** Stijn Dejongh (operator)

**Technical Story:** [#285](https://github.com/spec-kitty/spec-kitty-open-packs/issues/285); charter
[#537](https://github.com/spec-kitty/spec-kitty-charter/issues/537), PR
[#567](https://github.com/spec-kitty/spec-kitty-charter/pull/567) and its ADR-0077; epic
[#287](https://github.com/spec-kitty/spec-kitty-open-packs/issues/287)

**Supersedes:** no ADR. It amends one rule of
[ADR 2026-11-11-1](2026-11-11-1-split-built-in-into-foundation-writing-and-opt-in-bundles.md)
(bare step-contract delegation candidates), which already carries an inline amendment for it.

---

## Context and Problem Statement

Charter slice F (charter PR #567, merged 2026-11-15, ADR-0077) changed the model the packs follow:

* the `mission_step_contract` kind is retired: a step contract's content becomes the `substeps`
  of its step;
* every step must be linked from its mission type, or the service refuses it
  (`mission_step_unlinked`);
* every substep delegation candidate needs a `scope` edge, or the service refuses it
  (`substep_delegation_unscoped`);
* an edge endpoint table governs every relation.

The packs carried 28 step contracts and two `mission_step_contract.graph.yaml` fragments. The pin
could not move past slice F until they followed.

## Decision Drivers

* The packs validate against the charter at the pin, and the new pin refuses every step-contract
  file and every unlinked step or unscoped candidate.
* The old pin refused `substeps`, so the fold and the pin move had to land together.
* The changes that were valid at both pins could land first and shrink the pin-move PR.

## Considered Options

* Follow slice F in two steps: the additive items first, then the fold with the pin move.
* Follow slice F in one pull request.
* Hold the pin before slice F.

## Decision Outcome

**Chosen option:** "Follow slice F in two steps", because the additive items are valid at the old
pin, and landing them first made the pin move smaller to review.

1. **Additive, before the pin move** (#285 items 2 to 4, PR #289):
   * 26 `mission_type:<t> -requires-> action:<t>/<s>` edges, so each mission type links every step
     and on-demand step;
   * 79 `scope` edges from a step's action to each delegation candidate that had none;
   * `foundation`'s `work-package` lifecycle and the `spec-kitty-pre-review` guard on
     `in_progress -> for_review` (charter ADR-0054 decision 12).
2. **With the pin move** (#285 items 1 and 5, PR #293, pin to charter `main` `050d780`):
   * the 28 step contracts fold into 149 substeps on 28 steps, and the contract files and the two
     graph fragments are removed;
   * 115 substep ids move to the kernel grammar (`-` instead of `_`);
   * writing's 34 cross-pack delegation candidates are written `foundation::<id>`;
   * the validator follows the pin's file rules: a `retired` rule beats a `files` rule that also
     matches, and the step-contract kind is no longer known.

Removing an artifact raises the major version (DIRECTIVE_018), so `foundation` and `writing`
moved to 2.0.0, with `built-in`, `qa`, `event-driven` and `internal` at 4.0.0. The exact
lockstep pins on the built-in members moved with them (charter ADR-0048 decision 17).

### Consequences

#### Positive

* The packs follow the charter's kind taxonomy, and the service refuses an unlinked step or an
  unscoped candidate on the pull request that writes it.
* A step's work lives in one place, the step.

#### Negative

* A pack that overrode or enhanced a step contract must rewrite its change against the step's
  substeps (the CHANGELOG's upgrade note).
* The renamed substep ids break any external reference to the old `_` spellings.

#### Neutral

* The retired relations (`impacts`, `replaces`, `delegates_to`) needed no migration: no pack here
  authored one.

### Confirmation

At pin `050d780`, `validate-packs.sh` (with `--cross-pack`) and the charter's
`:pack-validation:driftTest` passed on the migrated tree. The same drift test refuses 5 packs on the
pre-migration tree, so the check is not vacuous. The `Charter service validation` job has run it on
every pull request since. High confidence.

## Pros and Cons of the Options

### Two steps: additive first, then the fold with the pin

**Pros:**

* Each pull request is smaller, and the first is reviewable against the unchanged pin.

**Cons:**

* Two landings to coordinate; the second must be based on the first.

### One pull request

**Pros:**

* One landing.

**Cons:**

* A larger diff, with additive and breaking changes mixed.

### Hold the pin

**Pros:**

* No content change.

**Cons:**

* The packs fall behind the charter, and slice G and the glossary contexts, which the same pin
  carries, wait too.
