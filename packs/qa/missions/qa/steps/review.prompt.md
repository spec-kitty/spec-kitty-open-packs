# Test Report Review

## Role in the QA lifecycle

This step checks that the execution results are genuine, computes coverage from the evidence,
triages defects and writes the test report. Its outputs are `test-report.md`, scaffolded from
`test-report-template.md`, and the traceability carrier `qa-traceability.yaml`. The release
decision itself is made at `accept`.

## Requested role

This step asks for the `qa-reporter` role. The pack's `qa` preset activates `qa-reporter-rhea` for it.

## Directive citation

- `QA_003` (no-fake-green): the report shows genuine outcomes, with numbers taken only from the
  computed evidence.

## What to do

1. Load the step's governance: `spec-kitty charter context --action review --mission-type qa --json`.
2. Find the execution start time (`--since`, below).
3. Build the carrier with `qa-result-ingest` (below).
4. Score it with `qa-traceability-lint` (below). This writes `qa-coverage.json`.
5. Triage the defects in `defect-log.md` with the `qa-defect-triage-ritual` procedure.
6. Fill `test-report.md`. Take every number in the coverage and pass/fail tables from
   `qa-coverage.json`. Fill the residual-risk statement and the go/no-go recommendation.
7. Commit `qa-traceability.yaml`, `qa-coverage.json` and `test-report.md`.

### Find the execution start time

`--since` is the moment test execution started. Results older than it are stale. Take it from
the mission's status event log, never from a guess:

1. List the work packages and their lanes:
   `spec-kitty agent tasks status --mission <handle> --json`. Note the test-execution work
   packages in `work_packages[]`.
2. The status JSON carries lanes, not timestamps. Read the timestamps from the event log,
   `kitty-specs/<mission>/status.events.jsonl`. Each lane change is one JSON line with `wp_id`,
   `from_lane`, `to_lane` and `at`.
3. Take the earliest `at` among those work packages' events with `to_lane` `in_progress`. For
   example: `jq -r 'select(.to_lane == "in_progress") | .at' status.events.jsonl | sort | head -1`.
   Narrow it to the execution work packages if other packages ran earlier.

### Build the carrier

1. Resolve the script: `spec-kitty charter pack asset path qa-result-ingest`.
2. Pass each result file with its own `--results` flag. Never hand a shell glob to a single
   `--results`: it breaks as soon as there are two files. In bash:

   ```
   shopt -s nullglob          # without this, an empty results/ passes the literal '*.xml'
   results_args=()
   for f in evidence/results/*.xml; do results_args+=(--results "$f"); done
   python <resolved-path> "${results_args[@]}" --strategy spec.md --tasks-dir tasks/ \
       --since <timestamp> --mission-dir . --json
   ```

   `--results` is needed only when at least one case declares an `automation_ref`. A mission
   with only manual and exploratory cases leaves it out.
3. Read the exit code. `0` (`ingested`): the carrier was written from current-run evidence.
   `1` (`blocked`): a named guard fired, for example zero test cases or stale results, and the
   carrier was not written. `2` (`error`): the input is unusable, for example a missing `spec.md`
   or an unsupported JUnit dialect. Fix the cause and run it again; do not hand-edit the carrier.

The ingester reads JUnit-XML only, in the dialect that marks outcomes with `<failure>`, `<error>`
and `<skipped/>` child elements. It refuses the `status="..."` attribute dialect, and it does not
read TAP, TRX, Cucumber JSON, Robot Framework XML or CTRF. See the `qa-result-ingest` toolguide.

### Score the carrier

1. Resolve the script: `spec-kitty charter pack asset path qa-traceability-lint`.
2. Run `python <resolved-path> --carrier qa-traceability.yaml --mission-dir . --json`.
3. Read the exit code. `0`: measured, verdict `ready`. `1`: measured, verdict `blocked`. `2`:
   no carrier (`not_measured`) or a malformed one (`error`).
4. The lint writes `qa-coverage.json` on every run. Take the requirement table from
   `requirements_covered`, `requirements_uncovered` and `requirements_blocked`, and the case
   counts from `passed`, `failed`, `skipped` and `overrun`. Never count by hand from the carrier
   or the raw evidence.

## Success criteria

- `qa-traceability.yaml` was built by the ingester from this run's evidence.
- `qa-coverage.json` exists, and every number in `test-report.md` matches it.
- Every defect has an agreed severity and priority.
- The go/no-go recommendation names the exit criteria it rests on.

## Hand-off

`accept` re-checks the coverage against the frozen exit criteria and records the go/no-go
decision. Run the ingester and the lint yourself: what the runtime enforces for this step is
stated in the pack README, under "Known limitations".
