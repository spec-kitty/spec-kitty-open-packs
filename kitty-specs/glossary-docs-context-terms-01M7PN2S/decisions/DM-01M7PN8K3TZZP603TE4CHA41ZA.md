# Decision Moment `01M7PN8K3TZZP603TE4CHA41ZA`

- **Mission:** `glossary-docs-context-terms-01M7PN2S`
- **Origin flow:** `specify`
- **Slot key:** `specify.release.version-bump`
- **Input key:** `version_bump`
- **Status:** `resolved`
- **Created:** `2026-11-18T06:24:47.226972+00:00`
- **Resolved:** `2026-11-18T06:24:57.142916+00:00`
- **Opened by:** `cli`
- **Other answer:** `false`

## Question

How are the changed packs versioned under DIRECTIVE_018?

## Options

- minor bumps plus exact-pin followers
- no bump
- Other

## Final answer

minor bumps plus exact-pin followers: additive terms are non-breaking (DIRECTIVE_018); foundation 2.0.0->2.1.0 and internal 4.0.0->4.1.0, and every pack pinning foundation ==2.0.0 moves its pin and takes a minor bump, as #287 did.

## Rationale

_(none)_

## Change log

- `2026-11-18T06:24:47.226972+00:00` - opened
- `2026-11-18T06:24:57.142916+00:00` - resolved (final_answer="minor bumps plus exact-pin followers: additive terms are non-breaking (DIRECTIVE_018); foundation 2.0.0->2.1.0 and internal 4.0.0->4.1.0, and every pack pinning foundation ==2.0.0 moves its pin and takes a minor bump, as #287 did.")
