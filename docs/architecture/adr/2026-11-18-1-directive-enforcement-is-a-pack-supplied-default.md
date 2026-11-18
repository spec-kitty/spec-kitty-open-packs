---
title: 'ADR: A directive''s enforcement level is a pack-supplied default'
description: Directives keep the enforcement field the pinned charter schema requires, read as a default the adopting charter overrides; directive prose never restates a level.
doc_status: draft
updated: '2026-11-18'
related:
- guides/author-a-charter-pack
- artefacts/index
---
# A directive's enforcement level is a pack-supplied default

**Status:** Proposed (the operator accepts it by merging #233's pull request)

**Date:** 2026-11-18

**Deciders:** Stijn Dejongh (operator)

**Technical Story:** [#233](https://github.com/spec-kitty/spec-kitty-open-packs/issues/233), the
open-packs half of core
[spec-kitty#5207](https://github.com/spec-kitty/spec-kitty/issues/5207); epic
[#245](https://github.com/spec-kitty/spec-kitty-open-packs/issues/245).

---

## Context and Problem Statement

Every directive carries an `enforcement:` level (`required`, `lenient-adherence` or `advisory`).
Many directives also said in their prose how binding they were, and the two disagreed:
DIRECTIVE_051 was `required` but called itself "advisory in v1", DIRECTIVE_052 was `advisory` but
called its output "mandatory", and DIRECTIVE_028 was `required` while every rule said "prefer".
The three levels were not defined anywhere in the packs. Core #5207 set the direction: how
strictly a directive binds is a property of the adopting project's charter, not of the directive.

Should the packs retire the field, and where does the level vocabulary live?

## Decision Drivers

- The packs validate against the charter contract at the pin (`charter.lock.yaml`), not against
  core.
- One fact, one home: a level stated in both the field and the prose drifts.
- New directives (#216, #217, #219) need a settled vocabulary to start from.

## Considered Options

1. Retire the `enforcement:` field.
2. Keep the field as the pack-supplied default, define the levels once, and take level prose
   out of the content.
3. Keep both the field and the prose, and reconcile them by hand.

## Decision Outcome

Chosen option: **2, keep the field as the pack-supplied default**, because the pin leaves no
other valid shape. At charter `050d780`, `contracts/packs/schemas/directive.schema.json` lists
`enforcement` under `required`, with the enum `required | lenient-adherence | advisory` and
`additionalProperties: false`. Removing the field, or moving it to a new name, fails validation.

- The value a directive ships is the **default level**. The adopting charter's activation
  config decides the level that applies (core #5207).
- The levels are defined once, as `term:spec-kitty-core/enforcement-level` in the foundation
  glossary context. The authoring guide and the `doctrine-instruction-voice` styleguide point
  there.
- A directive's body, and any content that cites a directive (steps, prompts, tactics, graph
  edge reasons, READMEs), states what the rule requires and never how strictly it binds. The
  vocabulary guard (`scripts/ci/check_vocabulary.py`) refuses the self-binding phrasings.
- No default value changed in the migration.
- This vocabulary is separate from activation presets' `must_have` items and `policy.yaml`
  levels, which decide *which* artefacts are in force (#242, #201).

### Consequences

#### Positive

- A directive's text no longer contradicts its level, and a charter can change the level
  without the text going stale.
- Pack authors look levels up in one term.

#### Negative

- Some context moves out of directive text: DIRECTIVE_051 no longer says it adds no
  fail-closed transition gate. A reader who needs the effective level reads the charter.

#### Neutral

- If the charter schema later drops or renames the field, this ADR is superseded by the pin
  move that migrates it.

### Confirmation

`validate-packs.sh` passes at the pin with the field present on all 59 directives, and
`check_vocabulary.py` finds no self-binding phrasing under `packs/`.

## Pros and Cons of the Options

### Retire the field

- Good, because the charter would be the only home of the level.
- Bad, because the pinned schema refuses it, and adopters would lose a default.

### Keep the field as the pack-supplied default

- Good, because it is valid at the pin and preserves behaviour.
- Good, because a default still lets a pack say how strongly it recommends the rule.
- Neutral, because the reading depends on core #5207 for overrides.

### Keep both and reconcile by hand

- Bad, because it is the arrangement that drifted.
