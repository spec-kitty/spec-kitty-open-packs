# Acceptance

## Role in the QA lifecycle

This step confirms that the exit criteria were met and records the go/no-go decision. Its
output is `qa-coverage.json`, recomputed from the committed carrier. It has no template.

## Requested role

This step asks for the `qa-reporter` role. The pack's `qa` preset activates `qa-reporter-rhea` for it.

## Directive citations

- `QA_003` (no-fake-green): the decision must not paper over missing or failing evidence.
- `QA_004` (exit-criteria-precede-execution): the decision is judged against the exit criteria
  as they stood when execution started.

## What to do

1. Load the step's governance: `spec-kitty charter context --action accept --mission-type qa --json`.
2. Check that every evidence file under `evidence/` and `qa-traceability.yaml` is committed. Any
   uncommitted evidence file blocks acceptance.
3. Re-run the carrier lint so `qa-coverage.json` reflects the committed carrier:
   `python "$(spec-kitty charter pack asset path qa-traceability-lint)" --carrier qa-traceability.yaml --mission-dir . --json`.
   Commit the refreshed `qa-coverage.json`.
4. Confirm the numbers in `test-report.md` still match `qa-coverage.json`. If they differ, go
   back to `review`.
5. Find the frozen exit criteria: section 4 of `spec.md`, as it stood at the execution start
   time `review` used. Check the history of `spec.md` after that time. Any change needs a
   recorded decision naming who, what, why and when (`QA_004`). An unrecorded change voids the
   criteria record.
6. Compare each exit criterion with `qa-coverage.json` and the open defects. Mark each one met
   or not met, with the number or defect that shows it.
7. Run the `qa-go-no-go-readiness-review` procedure.
8. Record the decision in `test-report.md` under the go/no-go section: `go` or `no-go`, the
   rationale, who decided and when. Commit it.

## Success criteria

- `qa-coverage.json` was recomputed in this step from the committed carrier.
- Each exit criterion is marked met or not met, with evidence.
- Any change to the exit criteria after execution start has a recorded decision.
- The go/no-go decision and its rationale are recorded and committed.

## Hand-off

A `go` lets the mission close. A `no-go` names the unmet criteria and the defects that block
release, so the next run can target them.
