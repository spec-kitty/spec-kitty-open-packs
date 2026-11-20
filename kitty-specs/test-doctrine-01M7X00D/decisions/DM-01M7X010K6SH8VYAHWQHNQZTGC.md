# Decision Moment `01M7X010K6SH8VYAHWQHNQZTGC`

- **Mission:** `test-doctrine-01M7X00D`
- **Origin flow:** `specify`
- **Slot key:** `specify.scope.red-first-carve-out`
- **Input key:** `red_first_carve_out`
- **Status:** `resolved`
- **Created:** `2026-11-20T17:28:19.814452+00:00`
- **Resolved:** `2026-11-20T17:28:21.064504+00:00`
- **Opened by:** `cli`
- **Other answer:** `false`

## Question

When is a red-first test required, and what replaces it otherwise?

## Options

_(none)_

## Final answer

Operator ruling 2026-11-20: real-run or existing-gate evidence REPLACES the red-first test for config/glue work. Red-first is required only for lasting regression risk (product logic, gate/classifier scripts, invariants, security/permission policy). Add an [evidenced-by-run] delivery label beside [build]/[ratchet]/[folded], and the long-term-value question. Reviewers flag pure config-restatement tests as waste.

## Rationale

_(none)_

## Change log

- `2026-11-20T17:28:19.814452+00:00` - opened
- `2026-11-20T17:28:21.064504+00:00` - resolved (final_answer="Operator ruling 2026-11-20: real-run or existing-gate evidence REPLACES the red-first test for config/glue work. Red-first is required only for lasting regression risk (product logic, gate/classifier scripts, invariants, security/permission policy). Add an [evidenced-by-run] delivery label beside [build]/[ratchet]/[folded], and the long-term-value question. Reviewers flag pure config-restatement tests as waste.")
