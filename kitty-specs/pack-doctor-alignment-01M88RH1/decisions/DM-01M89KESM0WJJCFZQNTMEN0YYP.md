# Decision Moment `01M89KESM0WJJCFZQNTMEN0YYP`

- **Mission:** `pack-doctor-alignment-01M88RH1`
- **Origin flow:** `plan`
- **Slot key:** `plan.process.review_guard`
- **Input key:** `planning_artifact_review_guard`
- **Status:** `resolved`
- **Created:** `2026-11-25T14:58:47.552573+00:00`
- **Resolved:** `2026-11-25T14:58:50.622155+00:00`
- **Resolved by:** `operator (via dispatcher)`
- **Opened by:** `claude::implementer-ivan`
- **Other answer:** `true`

## Question

move-task --to for_review refuses planning-artifact WPs: their evidence window looks at feat/pack-doctor-alignment, but the work lives on the coordination branch. Force, land planning commits on feat, or review without the state move?

## Options

- move-task --force with a note naming the mismatch
- land planning commits on feat
- review without the state move

## Final answer

use move-task <WP> --to for_review --force with a note naming the topology mismatch, for WP02-WP07; the dispatcher files the core issue (operator ruling 2026-11-25, relayed by the dispatcher session_019C2Tk6DpTSEBeTcn9F6smy)

## Rationale

_(none)_

## Change log

- `2026-11-25T14:58:47.552573+00:00` - opened
- `2026-11-25T14:58:50.622155+00:00` - resolved (final_answer="use move-task <WP> --to for_review --force with a note naming the topology mismatch, for WP02-WP07; the dispatcher files the core issue (operator ruling 2026-11-25, relayed by the dispatcher session_019C2Tk6DpTSEBeTcn9F6smy)")
