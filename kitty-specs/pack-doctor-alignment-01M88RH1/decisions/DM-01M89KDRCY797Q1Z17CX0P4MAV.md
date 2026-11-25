# Decision Moment `01M89KDRCY797Q1Z17CX0P4MAV`

- **Mission:** `pack-doctor-alignment-01M88RH1`
- **Origin flow:** `plan`
- **Slot key:** `plan.curation.batch_size`
- **Input key:** `curation_batch_size`
- **Status:** `resolved`
- **Created:** `2026-11-25T14:58:13.534734+00:00`
- **Resolved:** `2026-11-25T14:58:16.547690+00:00`
- **Resolved by:** `operator (via dispatcher)`
- **Opened by:** `claude::implementer-ivan`
- **Other answer:** `true`

## Question

NFR-005 caps a curation WP at about 70 entries; the home-pack batches have 77 (WP04) and 72 (WP07) origin entries, and WP03 clusters all 273. Waive, split WP04, or other?

## Options

- waive for the home-pack batches
- split WP04
- Other

## Final answer

waive NFR-005's ~70 for the home-pack batches (WP04 77, WP07 72); the merge map counts as a clustering pass, not row calls (operator ruling 2026-11-25, relayed by the dispatcher session_019C2Tk6DpTSEBeTcn9F6smy)

## Rationale

_(none)_

## Change log

- `2026-11-25T14:58:13.534734+00:00` - opened
- `2026-11-25T14:58:16.547690+00:00` - resolved (final_answer="waive NFR-005's ~70 for the home-pack batches (WP04 77, WP07 72); the merge map counts as a clustering pass, not row calls (operator ruling 2026-11-25, relayed by the dispatcher session_019C2Tk6DpTSEBeTcn9F6smy)")
