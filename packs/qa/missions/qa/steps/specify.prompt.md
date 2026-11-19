# Test Strategy

## Role in the QA lifecycle

This step writes the test strategy: scope, risks, quality bar, exit criteria and the requirement
register. Its output is `spec.md`, scaffolded from `test-strategy-template.md`.

## Requested role

This step asks for the `qa-strategist` role. The pack's `qa` preset activates `qa-strategist-quinn` for it.

## Directive citations

- `QA_001` (traceability-mandatory): every declared requirement must be traceable from the start.
- `QA_004` (exit-criteria-precede-execution): exit criteria are written here, before execution.
- `QA_005` (risk-based-prioritization): the strategy is ordered by risk.

## What to do

1. Load the step's governance: `spec-kitty charter context --action specify --mission-type qa --json`.
2. Fill each section of `spec.md`:
   - **1. SUT / Test-Item Scope**: what is tested and what is explicitly out of scope.
   - **2. Risk Register**: each risk with likelihood and impact.
   - **3. Quality Criteria**: the measurable bar the system must clear.
   - **4. Entry/Exit Criteria**: what must be true to start testing and to call it done. Make
     each exit criterion checkable against a number in `qa-coverage.json` or a named defect state.
   - **5. Requirement Register**: one row per requirement, id first, in the table or bullet
     shape the template shows.
3. Use ids of the form `FR-NNN`, `NFR-NNN` or `C-NNN`: uppercase, exactly three digits. The
   result-ingest tool reads only that shape, so other ids drop out of coverage.
4. Give each requirement a risk level from the risk register.

## Success criteria

- No template placeholder text is left.
- Every requirement has a well-formed, unique id.
- Every exit criterion can be checked later without judgement calls.
- Out-of-scope items are named, not implied.

## Hand-off

`plan` reads `spec.md` and turns it into an executable test plan. Exit criteria are frozen once
execution starts (`QA_004`); a later change needs a recorded decision.
