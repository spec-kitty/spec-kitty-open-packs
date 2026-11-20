# Decision Moment `01M7X00Y4M4P44AJJCJG5PHZZ5`

- **Mission:** `test-doctrine-01M7X00D`
- **Origin flow:** `specify`
- **Slot key:** `specify.scope.mock-allow-list`
- **Input key:** `mock_allow_list`
- **Status:** `resolved`
- **Created:** `2026-11-20T17:28:17.300520+00:00`
- **Resolved:** `2026-11-20T17:28:18.553600+00:00`
- **Opened by:** `cli`
- **Other answer:** `false`

## Question

Which collaborators may a test mock or stub?

## Options

_(none)_

## Final answer

Operator ruling 2026-11-20: widened allow-list — another domain/bounded context, filesystem, database, network/external APIs, clock, randomness, git/process, and narrow system cases (DTO validation, hook/notification sends). Everything else inside the responsibility border runs for real.

## Rationale

_(none)_

## Change log

- `2026-11-20T17:28:17.300520+00:00` - opened
- `2026-11-20T17:28:18.553600+00:00` - resolved (final_answer="Operator ruling 2026-11-20: widened allow-list — another domain/bounded context, filesystem, database, network/external APIs, clock, randomness, git/process, and narrow system cases (DTO validation, hook/notification sends). Everything else inside the responsibility border runs for real.")
