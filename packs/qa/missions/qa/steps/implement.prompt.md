# Test Execution

## Role in the QA lifecycle

This step runs the designed tests and records what happened. Its output is `defect-log.md`,
scaffolded from `defect-log-template.md`, plus the raw evidence under `evidence/`.

## Requested role

This step asks for the `test-executor` role. The pack's `qa` preset activates `qa-test-executor-elena` for it.

## Directive citations

- `QA_002` (defect-report-quality): every defect is reproducible from its report.
- `QA_006` (exploratory-charters-timeboxed): exploratory sessions keep to their timebox, and
  overruns are recorded.

## What to do

1. Load the step's governance: `spec-kitty charter context --action implement --mission-type qa --json`.
2. Move each work package to in progress before you run its tests
   (`spec-kitty agent tasks move-task <WP> --to doing --mission <handle>`). `review` reads the
   start of execution from that status change.
3. Run the automated suites. Write JUnit-XML results to `evidence/results/*.xml`. Use the
   `qa-regression-suite-selection`, `qa-test-data-minimization` and `qa-flaky-test-quarantine`
   tactics as they apply.
4. Run each exploratory charter. Write one `evidence/sessions/<name>.session.yaml` per session
   with `charter`, `timebox_minutes`, `overrun` (a boolean), `areas`, `bugs_found`, `bug_ids`,
   `status` (`completed` or `aborted`) and `debrief`.
5. Log each defect in `defect-log.md`: reproduction steps, expected and actual result,
   environment, severity, priority and attached evidence.
6. Commit every evidence file before the step completes (see below).

## Evidence commit discipline

Commit every `evidence/results/*.xml` and `evidence/sessions/*.session.yaml` file this step
produces. Any uncommitted evidence file blocks `accept`. That holds for new, untracked files as
much as for modified tracked ones. Uncommitted evidence does not just risk loss at merge: it makes
`accept` fail until the file is committed.

## Success criteria

- Every planned case ran, or its skip is recorded with a reason.
- Every failure is either logged as a defect or explained as a test problem.
- Every evidence file is committed.

## Hand-off

`review` ingests the evidence, computes coverage and writes the test report.
