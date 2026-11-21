# Test Plan

## Role in the QA lifecycle

This step turns the strategy into an executable test plan: items, environments, test data,
suites, tooling, schedule and owners. Its output is `plan.md`, scaffolded from
`test-plan-template.md`.

## Requested role

This step asks for the `qa-strategist` role. The pack's `qa` preset activates `qa-strategist-quinn` for it.

## Directive citations

- `QA_004` (exit-criteria-precede-execution): the plan must not move or loosen the exit
  criteria in `spec.md`.
- `QA_005` (risk-based-prioritization): suites and schedule follow the risk order.

## What to do

1. Load the step's governance: `spec-kitty charter context --action plan --mission-type qa --json`.
2. Read `spec.md`, especially the risk register, exit criteria and requirement register.
3. Fill each section of `plan.md`. Order suites by risk, using the
   `qa-risk-based-test-prioritization` tactic.
4. In **4. Suite Breakdown**, give each suite a bold `**Suite**:` line, its scope and the
   requirement ids it targets.
5. In **8. Traceability-Matrix Skeleton**, add one row per test item with its requirement ids.
   Every id in the requirement register appears at least once.
6. In **5. Tooling**, describe tooling generically. Do not name a specific test runner.
7. Review the draft with the `qa-test-plan-review-workshop` procedure before hand-off.
8. History is rewritten at close-out, so a commit SHA written now will not resolve later: cite changes and code as the writing pack's `research-citation-discipline` styleguide (when installed) says.

## Success criteria

- No template placeholder text is left.
- The traceability matrix covers every requirement id in `spec.md`.
- Every suite has an owner, an environment and a data source.
- The plan gate accepts `plan.md` as filled (`plan-field-declaration.yaml` names the sections
  it checks).

## Hand-off

`tasks` reads `plan.md` and designs the suites, cases and work packages.
