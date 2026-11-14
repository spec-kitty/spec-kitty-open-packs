# Research note: one owner per delivery rule in the internal pack (#271, #260)

Op `01M7DHH6Q03FJTC81BRV714S2H`. Grounded on `origin/main` at `fd7d644`, spec-kitty CLI 4.0.0rc9
(core `d7cedd7`, `make sync-packs` clean). Kind: tidy-first doctrine edit. Each rule keeps its meaning
and moves to one owner; the other copies become pointers. The two exceptions are the ready-flip rule,
which changes to match operator ruling R2, and the three reconciled rules listed under "Decisions".

## Issues read

- **#271** (P2, child of epic #263). The internal delivery procedures and skills restate the same
  rules 5 to 8 times, and the copies disagree. Operator ruling R2 (issue comment, 2026-11-14): the
  closeout step of `mission-wrap-up-sequence` owns the ready-flip rule. Order: consolidation closeout
  (clean history, rebase on main, changelog, pre-PR review, folds), draft PR, CI to green, then the
  implementer flips the PR to ready for review. Merging stays with the operator.
- **#260** (P3, sub-issue of #271). Delegate profile loading is restated as "self-load only" in the
  internal procedures and skills, against `adversarial-squad-deployment`'s three routes (injected,
  self-loaded, on-disk fallback) and its diff pre-load rule.
- **#263** (epic). Gates for every child: `validate-packs.sh`, the charter service check,
  `check_vocabulary.py`, `gen_pack_reference.py --check`, digests restamped.
- **#270** (separate slice, P2). Makes the `base` must-have flows repo-neutral (R1). This slice does
  not generalise core literals (`spec-kitty/spec-kitty`, `docs/changelog/unreleased/`, the five-section
  template, `scripts/docs/*`). It moves them, unchanged, into the owner, so #270 has one place to edit
  per rule. New text adds no core literal.
- **#275** (parallel, pack-authoring and foundation). No file overlap: this slice edits only
  `packs/internal` plus the generated surfaces and the changelog.

## Owners

| Rule | Copies on `main` | Owner after this slice |
| --- | --- | --- |
| Ready-for-review flip (R2) | wrap-up:36-39,50-52 (forbids); issue-to-mission:5,9,39,50; semi-auto-delivery:9,44,66; mission-from-issue.skill:1,17,30; semi-auto.skill:18,45 | `mission-wrap-up-sequence`, step "Close out: draft PR, green CI, then ready for review" |
| Changelog fragment | landing:29,52; issue-to-mission:36; cloud-dispatch:21; semi-auto-delivery:44; land-pr.skill:25; mission-from-issue.skill:16; semi-auto.skill:18,31 | wrap-up, step "Update the changelog and docs" (`<id>` per core's fragment README, plus the spelling check, L9) |
| Do not regenerate the docs index | landing:29,52; issue-to-mission:36; cloud-dispatch:21; memory-curation:32; semi-auto.skill:31 | wrap-up, step "Update the changelog and docs" |
| PR-body contract and validator | landing:52; issue-to-mission:39; semi-auto-delivery:44; semi-auto.skill:18; wrap-up:36 (weaker) | wrap-up, step "Write the PR body"; the validator is resolved with `spec-kitty charter pack asset path validate-pr-body` (L5; verified to resolve) |
| Deferral bar | landing:43; issue-to-mission:33; semi-auto-delivery:44; land-pr.skill:22; mission-from-issue.skill:15 vs wrap-up:47-49 | wrap-up, step "Review the rebased branch and fold every finding" (Decision D1) |
| Tree check before a force-push | wrap-up:28 vs landing:46, issue-to-mission:30, land-pr.skill:23 | wrap-up, step "Compact the branch" (Decision D2) |
| Base ref | cloud-dispatch:21 and semi-auto.skill:31 ("latest origin/main") vs semi-auto-delivery:41 ("canonical remote's main") | wrap-up, step "Rebase onto the canonical remote's main" |
| CLOUD_SESSION_ORCHESTRATION | directive:16-24; cloud-dispatch:21,44,50; semi-auto.skill:32-33 | the directive (unchanged) |
| Grounding and discovery squads | semi-auto-delivery:16; cloud-dispatch:44 §(1) | `semi-auto-delivery` step 2 |
| Delegate profile loading (#260) | landing:37,43,49; issue-to-mission:16,27,33; issue-triage-pass:19; cloud-dispatch:44 item 9; mission-from-issue.skill:19; semi-auto.skill:33 | `adversarial-squad-deployment` (foundation), step "Dispatch in parallel, profile-LOADED" |
| Commit attribution | semi-auto-delivery:44; cloud-dispatch:21,44 §(6); semi-auto.skill:49 | wrap-up closeout step (Decision D3) |

Line numbers are the file's own (`cat -n`), as cited in #271.

## Structure changes

- `semi-auto.skill.md` holds only the order and the mode fork (M6). The cloud-mode fleet controls
  point at `cloud-session-dispatch`.
- Steps over about 1,500 characters in `landing-contributor-prs` and `issue-triage-pass` are split (M8).
- DRG: `landing-contributor-prs` and `cloud-session-dispatch` now `require`
  `mission-wrap-up-sequence` (they take their closeout rules from it); `memory-curation-and-escalation`
  `suggests` it; `issue-triage-pass` and `landing-contributor-prs` `suggest`
  `adversarial-squad-deployment` for delegate loading where no edge existed.

## Decisions (sent to the operator as one batch; work proceeds on the recommendation, reversibly)

- **D1, deferral bar.** DIRECTIVE_046 (foundation, required) defers only "high-effort or
  mission-sized" work. The internal copies name three exceptions. Recommendation: the owner states
  the three exceptions as the internal refinement of DIRECTIVE_046: significant effort is 046's
  high-effort or mission-sized work, a significant operator decision is an escalation, and a highly
  impactful finding is a change that needs its own reviewable PR. Each is filed and named in the PR.
- **D2, tree check.** Recommendation: the rebuilt tree equals the pre-cleanup head's tree, except for
  files deliberately removed (committed ignored artefacts, personal data, machine-local paths); then
  `git diff <old> <new>` shows only those removals, and the hand-off lists them. This reconciles the
  wrap-up carve-out with the byte-identical rule and with "remove personal data from the commit that
  introduced it".
- **D3, attribution.** Not in #271's list, but the same defect class in the same files.
  Recommendation: fold it in, owned by the wrap-up closeout step.

## Similar-surfaces sweep

Commands: `grep -rnE` over `packs/` for each rule's marker (`changelog/unreleased`,
`regen-docs-index|retrieval index`, `validate-pr-body|five-section`, `agent profile show`,
`highly impactful|high-effort|mission-sized`, `HEAD^{tree}|byte-identical`,
`origin/main|canonical remote's`, `ready.for.review|flip`).

| Surface | Disposition |
| --- | --- |
| Every internal copy in the table above | in scope now |
| `foundation/directives/046-readable-consistent-prs` and `foundation/procedures/readable-pr-preparation` (deferral bar; "except intentionally dropped ignored artifacts") | out of scope (foundation). Consistent with D1 and D2 as refinements; no change needed. Reported, not filed. |
| `foundation/tactics/clean-linear-commit-history` (tree identity) | owner of the technique; the internal owner cites it |
| `foundation/missions/*/steps/*.prompt.md`, `*/templates/task-prompt-template.md` (`agent profile show`) | out of scope: a session loading its own profile, not a delegate dispatch |
| `internal/styleguides/spec-kitty-docs-lint-config` (`changelog/unreleased`) | out of scope: a lint path list, not the delivery rule |
| `internal/README.md:86` (validator description) | accurate; no change |
| Core literals in the moved text | #270 |

## Tracked-issues sweep

Searched open and closed issues (`gh api search/issues`, terms: ready-for-review, changelog fragment,
wrap-up, delivery rule) and read the epic's children.

- Closes: #271 and #260 (both fully delivered).
- Refs: #263 (epic); #270 (repo-neutral wording, separate slice); #275 (parallel, no file overlap);
  #272 (P3, stale core references in internal; touches `cloud-session-dispatch:27` and
  `memory-curation-and-escalation:5`, lines this slice does not edit).
- Closed predecessors, not reopened: #105 (fragments, not CHANGELOG.md edits) and #106 (dispatch
  conventions). This slice keeps their rules and gives each one owner.
- No duplicate or superseding issue found.
- Open PRs: #256 and #257 are merged. #279 (#264) touches only the generated internal surfaces
  (`pack-manifest.yaml`, `internal.source.yaml`, `docs/packs/internal.md`) and the changelog. Whoever
  lands second rebases and regenerates those with the tools, never by a hand merge.
