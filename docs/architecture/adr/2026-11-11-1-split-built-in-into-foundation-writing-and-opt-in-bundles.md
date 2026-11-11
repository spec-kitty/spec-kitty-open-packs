---
title: 'ADR: Split built-in into foundation, writing and opt-in bundles'
description: built-in becomes a distribution pack aggregating foundation and writing (and, by the 2026-11-11 amendment, the testing, refactoring, architecture and planning-analysis core bundles); the remaining doctrine ships as opt-in org bundles.
doc_status: active
updated: '2026-11-11'
related:
- packs
- packs/built-in
- packs/foundation
- packs/writing
- architecture/adr/2026-11-04-1-strict-pack-composition-and-the-end-of-cli-compatibility
---
# Split built-in into foundation, writing and opt-in bundles

**Status:** Accepted

**Date:** 2026-11-11

**Deciders:** Stijn Dejongh (operator)

**Technical Story:** [#73](https://github.com/spec-kitty/spec-kitty-open-packs/issues/73) (epic
[#190](https://github.com/spec-kitty/spec-kitty-open-packs/issues/190)), mission
`foundation-writing-split-01M75HV3`

---

## Context and Problem Statement

`built-in` shipped everything: 398 doctrine graph nodes, from the fallback profile to Drupal
conventions. Every consumer inherited all of it. Charter ADR-0048 makes `built-in` a *distribution
pack* that holds no artifacts and aggregates members through `depends_on` (decision 12), and makes
stack and topical packs opt-in at `pack_level: org` (decision 14). ADR-0053 (decisions 3 and 9)
names the members `foundation` and `writing`. Which artifact goes where was left to per-artifact
operator rulings.

## Decision Drivers

* The default distribution should carry the basis every project needs, not every specialism.
* The base mission types must keep working on their own: their step contracts, the roles they
  request and the directives' how-to procedures.
* Stack packs (`java`, and downstream `rust`/`go`) need a stable pack to build on.
* The charter service at the `charter.lock.yaml` pin is the gate. Core spec-kitty compatibility is
  not a constraint here (AGENTS.md).

## Considered Options

* Strict foundation and a temporary staging pack
* Foundation with its how-to layer, writing, and nine opt-in bundles carved now
* Foundation without its how-to layer, plus an opt-in `core-engineering` bundle

## Decision Outcome

**Chosen option:** "Foundation with its how-to layer, writing, and nine opt-in bundles carved now",
because it is the smallest valid foundation that keeps the base missions and the cross-cutting
directives actionable on their own, and carving the bundles now gives every consumer stable pack
names from day one. A four-lens research squad (graph clustering, curation, adversarial review,
consumer journeys; `kitty-specs/foundation-writing-split-01M75HV3/research/bundle-squad/`) showed
that option 1 was invalid as approved:

* analyst-annie → DIRECTIVE_047 made a cycle.
* writing → staging references were level violations.
* The base missions' requested roles went unfilled.
* Two implement steps lost their only candidate.
* 33 directive how-tos had no consumer outside foundation.
* A single staging pack would have cost about nine breaking repoints.

The resulting packs:

| Pack | Level | depends_on | Holds |
| --- | --- | --- | --- |
| `built-in` 2.0.0 | built-in | foundation `==1.0.0`, writing `==1.0.0` | No artifacts; the `default` and `minimal` presets; `fallback_profile` |
| `foundation` | built-in | — | Generic Giannis (`generic-agent`), implementer-ivan, reviewer-renata, analyst-annie, human-in-charge; the software-dev, plan and research missions; every cross-cutting directive with its procedures, tactics and toolguides (git workflow, execution lanes and adversarial-review squads included); the glossary; the fallback lock |
| `writing` | built-in | foundation | The documentation mission; the comms, docs, diagram and glossary profiles and guidance |
| `testing` | org | foundation | Test-design and BDD practice, mutation testing, debugger-debbie |
| `refactoring` | org | foundation, testing | The refactoring catalogue, semantic compression, randy-reducer |
| `architecture` | org | foundation, refactoring, writing | DDD and C4; architect-alphonso, paula-patterns |
| `planning-analysis` | org | foundation, architecture | planner-priti, researcher-robbie, retrospective-facilitator, brownfield analysis |
| `pack-authoring` | org | foundation, writing | doctrine-daphne, pack onboarding |
| `python`, `javascript`, `drupal`, `java` | org | foundation, testing | The language stacks |

### Rules applied

* **Levels.** foundation and writing are `pack_level: built-in`, since built-in may only depend on
  its own level or nearer (ADR-0048 decision 7). The ranks are foundation < writing < built-in < org
  bundles in DAG order, so there is no cycle.
* **Edges.**
  * An edge is homed in its source's pack when the target is in that pack's `depends_on` closure.
    Otherwise it is declared in the target's pack, with a qualified source (`foundation::<urn>`).
    110 edges moved this way.
  * Endpoints outside the home pack are written `<pack>::<urn>`.
* **Body references.**
  * Body references (profile `*-references`, operating procedures) cannot be relocated. Those
    outside the closure are dropped from the body, and their graph edge is kept in the target pack:
    annie → DIRECTIVE_047, daisy → USE_C4_MODEL_TECHNIQUES, ivan → test-first-bug-fixing.
    (renata → adversarial-squad-deployment was dropped too, then restored when the pre-PR review
    moved the adversarial-review practice into foundation: the default missions mark that
    procedure mandatory.)
  * In-closure profile references to another pack are qualified (`foundation::010`). Step-contract
    `delegates_to` candidates stay bare, which the charter allows within the closure.
* **Service-only refusals**, found by the service check:
  * A bundle may not add a relationship to the locked fallback profile.
  * A graph-only node (no file) is not held for a cross-pack reference.
  * Five edges were dropped and one graph-only template moved to its only referrer
    (`membership.json` `service_check_folds`).
* **Manifests (#182).** built-in, foundation and writing carry a `pack-manifest.yaml`, and the pack
  gate now fails when a file-backed doctrine artifact is missing from it. The covered kinds are
  profiles, directives, tactics, procedures, paradigms, styleguides, toolguides, assets, glossary
  packs, skills, guards and lifecycles. Templates, mission types and step contracts are exempt:
  this repository's manifests have never listed them. The org bundles carry no manifest, as before.
* **Layout.** `missions/` keeps its name. The pinned charter's file-kinds rules still anchor
  mission files under `missions/` (its retired `mission_types/` rule matches only flat files), so
  the ADR-0048 decision 16 rename is deferred to a later charter pin.
* **Where the fallback lives.** `foundation` holds `generic-agent` and locks it in its own
  `policy.yaml` (ADR-0063 keys name the pack's own artifacts). Both `foundation` and `built-in`
  declare `fallback_profile: generic-agent`, so a pack that depends on foundation alone also sees
  the fallback (ADR-0068).
* **The java question.** Whether `built-in` should aggregate `java` is left open. It needs a
  charter ADR amending ADR-0048 decision 14 and ADR-0053 decisions 1 and 3. The split forecloses
  neither answer: aggregating later is one more `depends_on` entry plus re-levelling `java`, and
  `testing` with it, since java depends on testing and built-in may only depend on its own level.

### Consequences

#### Positive

* The default distribution carries the basis and documentation doctrine and nothing else, and
  teams opt into specialisms.
* Stack packs have a stable base (`foundation` + `testing`) to build on.
* The pack gate now catches manifest drift (#182), and the service check proves every pack
  composes and registers.

#### Negative

* The change is breaking for anyone who:
  * places `built-in` alone (its members must be placed beside it);
  * writes `built-in::` references;
  * pins a `<2` range on built-in;
  * registers one of this repository's org packs without its new `depends_on` closure.

  See the CHANGELOG entry for the migration.
* spec-kitty core, which fetches `packs/built-in/` alone at a pinned commit, gets no doctrine from
  it. Core must fetch the members at the same pin before it moves its pin. This is out of scope
  here (AGENTS.md).
* Five graph edges the service refuses across packs were dropped (`service_check_folds`). Two of
  them are `rejects` edges whose reasoning text is lost.

#### Neutral

* Without `planning-analysis` or `architecture`, the `facilitator` and `architect` roles fall back
  to Generic Giannis. The `researcher` role goes first to a `writing` profile that lists it as an
  alt-role (`comms-cleo`, `synthesizer-sam`; ADR-0069).
* Three profile bodies lost a reference that left their closure. Each graph edge ships with the
  pack that holds its target.
* The pre-PR review moved the proposed `adversarial-review` bundle into foundation (operator
  ruling). The default missions require its squad procedure.

### Confirmation

On the final head, `scripts/ci/charter_service_check.py` composes all 18 packs and the example
fixture, registers every org pack dependencies first, and still refuses both invalid fixtures. The bundle membership is
script-verified against `membership.json`.

The decision is confirmed if the downstream stack packs (`rust`, `go`, `java` and the private
COBOL packs) build on `foundation` + `testing` without needing anything from the other bundles,
and if each later bundle change ships without touching `foundation`. High confidence on validity,
medium on the bundle boundaries: the curation lens lists overlap clusters to revisit.

## Pros and Cons of the Options

### Strict foundation and a temporary staging pack

**Pros:**

* The smallest, least opinionated foundation (115 nodes).
* Every how-to becomes an explicit opt-in.

**Cons:**

* Invalid as approved: annie → DIRECTIVE_047 is a cycle, and writing → staging references break
  the level rule.
* Two implement steps lose their only candidate, and the base missions request roles foundation
  cannot fill.
* Directives such as 010 and 053 go hollow without their procedures.
* Every carve-out of the staging pack is a breaking repoint, about nine times over.

### Foundation with its how-to layer, writing, and nine opt-in bundles carved now

**Pros:**

* Valid, and the base missions and directives work on their own.
* Stable pack names; stacks are leaves on `foundation` + `testing`.

**Cons:**

* A larger foundation (183 nodes, with the adversarial-review practice) carrying opinionated how-tos (Git Flow, PR landing). An org can
  still override a procedure by id in a higher layer.
* A large one-off pull request (11 new packs).

### Foundation without its how-to layer, plus an opt-in `core-engineering` bundle

**Pros:**

* A small foundation (about 120 nodes) that stays valid.

**Cons:**

* Nearly every software consumer must register `core-engineering`, and the directives in
  foundation are hollow without it.

## Amendment 2026-11-11: built-in aggregates the core bundles

The decision above made `built-in` aggregate only `foundation` and `writing` and shipped
`testing`, `refactoring`, `architecture` and `planning-analysis` as opt-in org bundles. That part of
the decision is amended. The original text above is kept as written; this section supersedes it for
those four bundles.

**Decision.** `built-in` is the aggregate of the general-purpose open-packs. The four bundles move
from `pack_level: org` to `pack_level: built-in`, and `built-in` lists them in `depends_on` with
exact `==` pins, beside `foundation` and `writing`. Built-in now has six members.

**Why.** Pack membership is decided in this repository. Operator decision: a default distribution
that leaves out test design, refactoring, architecture and planning guidance is too thin for general
software work, and every stack pack already builds on `testing`. These four are general-purpose and
carry no stack or organisation choice, so they belong in the default. The stacks (`python`,
`javascript`, `drupal`, `java`), `pack-authoring` and the topical and process packs (`internal`,
`qa`, `event-driven`, `spdd`, `cave-kitty`) stay opt-in at org level.

**Constraint held.** A built-in-level pack may depend only on built-in-level packs (charter
ADR-0048 decision 7). The closures of the four stay inside built-in level: `testing` depends on
`foundation`; `refactoring` on `foundation` and `testing`; `architecture` on `foundation`,
`refactoring` and `writing`; `planning-analysis` on `architecture` and `foundation`. Built-in-level
packs are read-only to registration, so they are placed beside `built-in` and not registered at org
level.

**Versions.** A level change is breaking. `testing`, `refactoring`, `architecture` and
`planning-analysis` go 1.0.0 → 2.0.0, and `built-in` 2.0.0 → 3.0.0 with `==` pins on all six
members (`foundation` and `writing` stay at 1.0.0). Org packs that depend on the four move their
range from `>=1.0,<2` to `>=2.0,<3`. Because their `depends_on` changed, each of those eight takes
its next major version, as the split did for `qa` in 91b603f: `python`, `javascript`, `drupal` and
`java` 1.0.0 → 2.0.0; `qa`, `internal`, `event-driven` and `spdd` 2.0.0 → 3.0.0. No pack pins them.

**Descriptors and manifests.** The four bundles keep their unsharded layout (one `drg/fragment.yaml`)
but now match the other built-in-level packs: `pack.yaml` declares `schema_version: "1.0"`, and each
bundle carries a generated `pack-manifest.yaml` listing its file-backed constituents (the #182
guard). Their `org-charter.yaml` and the `active_charter` pointer are removed, as `foundation` and
`writing` have none. Only `foundation` holds the fallback lock, so the four need no
`mutability_policy`.

**Consequences.** Consumers who registered any of the four at org level must drop that opt-in and
place the packs as built-in members. The default distribution now carries the architect, planner,
researcher, retrospective-facilitator, randy-reducer and debugger-debbie profiles, so the silent
fallbacks described in the changelog for 3.0 no longer occur on the `default` preset.
