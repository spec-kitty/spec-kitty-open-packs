# Decision Moment `01M8A4N1KBDNZKWS0SNGTPR8RC`

- **Mission:** `pack-doctor-alignment-01M88RH1`
- **Origin flow:** `plan`
- **Slot key:** `plan.sequencing.feat_update`
- **Input key:** `feat_update_after_consolidate`
- **Status:** `resolved`
- **Created:** `2026-11-25T19:59:18.123840+00:00`
- **Resolved:** `2026-11-25T19:59:20.673667+00:00`
- **Resolved by:** `operator (via dispatcher)`
- **Opened by:** `claude::implementer-ivan`
- **Other answer:** `true`

## Question

Refines 01M8A46SAWTKB2ZH3XEW5B2J89: once consolidate lands the Mission on feat, feat and main diverge, so a plain fast-forward of feat to origin/main is impossible. How is feat brought up to main?

## Options

- (i) fast-forward feat before consolidate
- (ii) merge main into feat after consolidate
- Other

## Final answer

"Consolidate mission first, then clean branch history, then rebase on main." 1. consolidate onto feat; 2. clean feat's history (squash or fix up the CLI and bookkeeping commits); 3. rebase feat onto origin/main, resolving conflicts there; 4. re-sign every rewritten commit. Main is never merged into feat. No force-push without the operator's approval: otherwise push a -v2 branch (operator ruling 2026-11-25, given directly to the dispatcher session_019C2Tk6DpTSEBeTcn9F6smy)

## Rationale

_(none)_

## Change log

- `2026-11-25T19:59:18.123840+00:00` - opened
- `2026-11-25T19:59:20.673667+00:00` - resolved (final_answer=""Consolidate mission first, then clean branch history, then rebase on main." 1. consolidate onto feat; 2. clean feat's history (squash or fix up the CLI and bookkeeping commits); 3. rebase feat onto origin/main, resolving conflicts there; 4. re-sign every rewritten commit. Main is never merged into feat. No force-push without the operator's approval: otherwise push a -v2 branch (operator ruling 2026-11-25, given directly to the dispatcher session_019C2Tk6DpTSEBeTcn9F6smy)")
