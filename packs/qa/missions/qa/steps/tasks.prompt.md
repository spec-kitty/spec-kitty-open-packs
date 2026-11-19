# Test Design

## Role in the QA lifecycle

This step designs the concrete test suites, test cases and exploratory charters, and splits them
into work packages. Its output is `tasks.md`, scaffolded from `test-suite-template.md`, plus one
`tasks/WP*.md` file per work package.

## Requested role

This step asks for the `test-designer` role. The pack's `qa` preset activates `qa-test-designer-tessa` for it.

## Directive citations

- `QA_001` (traceability-mandatory): every case names the requirements it covers.
- `QA_006` (exploratory-charters-timeboxed): every exploratory charter has a timebox.

## What to do

1. Load the step's governance: `spec-kitty charter context --action tasks --mission-type qa --json`.
2. Read `plan.md`. Fill the suite manifest in `tasks.md`: one row per suite, with its target
   ids, priority and risk.
3. Reduce the case set with the `qa-pairwise-test-reduction` and
   `qa-boundary-equivalence-partitioning` tactics.
4. Write each work package. Put test cases in the WP body as fenced ```yaml blocks, in the
   shape of `test-case-template.md`. Never put case keys in the WP frontmatter.
5. Give an automated case an `automation_ref` naming its JUnit `classname::name`. Leave it out
   for manual and exploratory cases.
6. Write each exploratory session as a charter in the shape of
   `exploratory-charter-template.md`, with its timebox.
7. Map requirements to work packages with `spec-kitty agent tasks map-requirements`.
8. Check coverage with the `qa-coverage-gap-analysis` procedure. Close each gap or record why it
   stays open.

The two unbound templates are in the pack root that `spec-kitty charter pack path qa` prints,
under `missions/qa/templates/`.

## Success criteria

- Every requirement id in `spec.md` is covered by at least one case, or has a written reason.
- Every case has a unique id, `requirement_refs`, priority, type and preconditions.
- Every exploratory charter has a timebox and target areas.
- `map-requirements` reports no orphan or unknown id.

## Hand-off

`implement` runs the work packages and records results and defects.
