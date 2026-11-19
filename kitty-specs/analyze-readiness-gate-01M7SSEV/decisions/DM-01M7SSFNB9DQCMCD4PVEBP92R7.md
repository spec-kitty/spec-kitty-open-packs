# Decision Moment `01M7SSFNB9DQCMCD4PVEBP92R7`

- **Mission:** `analyze-readiness-gate-01M7SSEV`
- **Origin flow:** `specify`
- **Slot key:** `specify.readiness.cannot-run-severity`
- **Input key:** `cannot_run_severity`
- **Status:** `resolved`
- **Created:** `2026-11-19T11:36:16.489312+00:00`
- **Resolved:** `2026-11-19T11:37:11.447874+00:00`
- **Opened by:** `cli`
- **Other answer:** `true`

## Question

When finalize-tasks --validate-only cannot run, should analyze record a MEDIUM finding plus residual-risk warning, or a HIGH finding that blocks the verdict?

## Options

- MEDIUM plus residual-risk warning
- HIGH (fail closed)
- Other

## Final answer

HIGH (fail closed): verdict blocked; the finding names the CLI version that provides the check

## Rationale

_(none)_

## Change log

- `2026-11-19T11:36:16.489312+00:00` - opened
- `2026-11-19T11:37:11.447874+00:00` - resolved (final_answer="HIGH (fail closed): verdict blocked; the finding names the CLI version that provides the check")
