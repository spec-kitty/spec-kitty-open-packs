# Discovery

## Role in the QA lifecycle

This step investigates the feature under test before a test strategy is written. It runs as the
built-in `research` action. It has no bound template and no required output artifact.

## Requested role

This step asks for the `researcher` role. The pack's `qa` preset activates no profile for it. A
researcher profile such as `researcher-robbie` (from the `planning-analysis` pack) fills it when
the operator activates one.

## Directive citations

- `QA_005` (risk-based-prioritization): find the risks that will order the strategy.
- `QA_006` (exploratory-charters-timeboxed): any exploration you do here runs under a
  timeboxed charter.

## What to do

1. Load the step's governance: `spec-kitty charter context --action discovery --mission-type qa --json`.
2. Read what the feature promises: its description, user-facing docs, open issues and recent
   changes. Note who uses it and what breaks for them if it fails.
3. Draft a risk list: each risk with a rough likelihood and impact.
4. List the requirements you can already name, with the ids you expect to give them
   (`FR-NNN`, `NFR-NNN`, `C-NNN`).
5. If you need hands-on exploration, scope one timeboxed charter first. Use the
   `qa-exploratory-charter-writing` tactic and the shape of `exploratory-charter-template.md`.
6. Note what is out of scope, and any environment or test-data constraint you found.

## Success criteria

- A risk list ordered by likelihood and impact.
- A first list of requirements to test, with ids.
- Scope boundaries and known constraints, written down.
- Any exploration ran under a stated timebox, and overruns are recorded.

## Hand-off

Carry the findings into `specify`. They become sections 1, 2 and 5 of `spec.md`.
