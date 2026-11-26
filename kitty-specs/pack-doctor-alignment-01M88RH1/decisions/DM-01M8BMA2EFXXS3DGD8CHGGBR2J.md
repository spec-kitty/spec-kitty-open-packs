# Decision Moment `01M8BMA2EFXXS3DGD8CHGGBR2J`

- **Mission:** `pack-doctor-alignment-01M88RH1`
- **Origin flow:** `plan`
- **Slot key:** `plan.retire.profile_refs`
- **Input key:** `profile_refs_not_judged`
- **Status:** `resolved`
- **Created:** `2026-11-26T09:52:10.191789+00:00`
- **Resolved:** `2026-11-26T09:52:13.310782+00:00`
- **Resolved by:** `operator (in the implementer session)`
- **Opened by:** `claude::implementer-ivan`
- **Other answer:** `false`

## Question

The pinned jar (f6f21e4c) does not judge agent-profile references, though #348 maps three profile_reference_violations parts to pack_reference_* and the charter guide check-packs.md says they are checked. Retire them?

## Options

- Keep + charter issue
- Keep, no issue
- Retire anyway

## Final answer

Keep + charter issue: the three parts stay (C-003) with comments and a real-jar test that fails once pack-doctor judges them; the implementer drafts a spec-kitty-charter issue on the guide/jar disagreement for the operator to file. #348 stays open for these three rows. (operator answer in the implementer session, 2026-11-26)

## Rationale

_(none)_

## Change log

- `2026-11-26T09:52:10.191789+00:00` - opened
- `2026-11-26T09:52:13.310782+00:00` - resolved (final_answer="Keep + charter issue: the three parts stay (C-003) with comments and a real-jar test that fails once pack-doctor judges them; the implementer drafts a spec-kitty-charter issue on the guide/jar disagreement for the operator to file. #348 stays open for these three rows. (operator answer in the implementer session, 2026-11-26)")
