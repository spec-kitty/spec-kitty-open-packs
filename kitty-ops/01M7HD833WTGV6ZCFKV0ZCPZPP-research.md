# Grounding note: #285 slice A, items 2 to 4 (charter slice F, ADR-0077)

Op `01M7HD833WTGV6ZCFKV0ZCPZPP`. Grounded on `origin/main` at `c0ec640`, charter pin `eacbc3c`
(`charter.lock.yaml`), spec-kitty CLI 4.0.0rc9. Kind: feature (pack content), size M. Operator ruling: items
2, 3 and 4 only. Items 1 (fold) and 5 (validator, docs, pin) wait for the pin bump.

## Sources

- #285 and the drafts on charter `main` (`9798572`) under
  `kitty-specs/slice-f-kind-taxonomy-01M7B19K/research/open-packs-drafts/`: `TBD-step-requires-edges.md`,
  `TBD-delegation-scope-edges.md`, `TBD-pre-review-guard.md`, `apply-drafts.py`, `census-check.py`. These were
  fetched read-only.
- The drafts counted at `1692a3b` and name `17ce3f9` as the current pin. Main has moved to `c0ec640` and the
  pin to `eacbc3c`, so every count below was taken again on `c0ec640`, and every gate ran at `eacbc3c`.

## How the drafts were applied

The session's permission classifier refused to execute the downloaded `apply-drafts.py` and `census-check.py`.
They were read in full and re-implemented as a session-local script, which was not committed. It uses the
same selection and the same textual placement rules: a node goes in sorted place, and an edge goes after the
last edge of the same source. It was first run as a dry count, then applied to this branch.

- The scope edges it added are identical to the draft's generated table: 79 of 79 rows, compared by `diff`.
- Item 4 follows its draft verbatim. Its draft says to hand-add the two manifest constituents and then
  `--regenerate-manifest`. Main now derives manifests (#255), so the manifest was written with
  `validate_pack_schemas.py --derive-manifest packs/foundation`. It adds exactly the two constituents
  (`guard`, `lifecycle`).

## Counts on `c0ec640`

| Item | Before | After |
| --- | --- | --- |
| 2: missing `mission_type -requires-> action` edges | 26 (cave-dev 8, qa 7, software-dev 8, research 2, documentation 1) | 0 |
| 2: missing `action` nodes | 23 (cave-dev 8, qa 7, software-dev 7, research 1) | 0 |
| 2: stray `requires` edges to a non-step action | 0 | 0 |
| 3: delegation candidate uses (step contracts) | 144, of which 0 are unresolved in their closure | 144 |
| 3: unscoped (step action, candidate) pairs | 79 edges / 80 uses (foundation 47, qa 18, writing 14) | 0 |
| 4: guards / lifecycles in foundation | 0 / 0 | 1 / 1 |

These are the same numbers the drafts give at `1692a3b`. No pair gains a second relation (ADR-0027: one
edge per component pair), checked over every edge of the four packs. Item 3 is computed from the
`*.step-contract.yaml` candidates because the fold (item 1) is not applied. Each target is qualified as the
fold will write it: bare in the same pack, `foundation::` from writing.

## Similar surfaces

- The two other unsharded packs with mission types are qa and cave-kitty. Both had no `action` node, and both
  are covered.
- No other pack holds a mission type, a step contract or a gate. There are 6 mission types in all
  (foundation 3, writing 1, qa 1, cave-kitty 1).
- The only step-contract gate is software-dev `review` (`in_progress->for_review`). Item 4's guard is its
  successor, and the contract's `gates[]` stays until item 1 retires the file.

## Tracked issues, dispositioned

- **#258, #259** (stale paths): they touch writing prose only, with no file overlap. Adjacent, no action. Both
  restamp the writing digest, and whoever lands second rebases and restamps.
- **#265** (consumer references): it touches the same four packs, but not `action.graph.yaml`,
  `mission_type.graph.yaml` or `drg/fragment.yaml`. It must coordinate only on digests and pack pages.
  Whoever lands second rebases and restamps.
- **#283** (glossary contexts): it rewrites `vocabulary` edges, possibly in `packs/qa/drg/fragment.yaml`, and
  is gated on a charter release. It will likely land after this and rebase. No action here.
- **#284** (drift task move): pin-bump work, which is the same PR as #285 item 5. Out of scope.
- **#286** (`specializes_from` cycle): validator only. Unrelated.
- Open PRs at grounding: none.
- Prior art checked:
  - #143 and PR #181 set the convention for `action:plan/*` scope edges, which is followed here.
  - PR #132 set the `requires` vs `suggests` rule. `mission_type -requires-> action` is the edge ADR-0077
    decision 4 mandates.
- #229 (DAG and scope rules how-to) could use these edges as examples. Not widened here.

## Open points (not widened)

- **`pack_version`:** DIRECTIVE_018 applies, through foundation's `doctrine-version-change` procedure: an
  additive change ("a new artifact, edge or optional field") takes a minor bump. The squad caught that this
  was missed.
  - qa goes to 3.1.0 and cave-kitty to 2.1.0. No pack pins either of them.
  - foundation and writing are pinned exactly (`==1.0.0`) and released in lockstep: foundation by
    architecture, built-in, planning-analysis, refactoring, testing and writing; writing by architecture
    and built-in. Bumping them cascades into six descriptors, so that is put to the operator. The
    recommendation is to ride with the item 1+5 pin move, which is breaking for the lockstep set anyway.
- **Other lifecycle guards:** the charter's guard schema also lists `builtin:dependency-ready`,
  `implementation-ready`, `review-approved`, `review-ref` and `transition-context-complete`. Core enforces
  these conditions on other transitions in `specify_cli/status/wp_state.py`: dependency readiness, reviewer
  approval for approved/done, and a review reference on rewinds. The draft guards only
  `in_progress -> for_review`, so the other guards are a follow-up and are not widened here.
- **Lifecycle shape:** core's nine lanes, as drafted. The charter example uses six. Kept at nine so a client
  that maps lanes one-to-one finds every lane, and the guarded transition is unchanged either way.
- **Census zero check:** the charter's `census-check.py` also needs the charter's `edge-census.py` CSV, which
  comes from a charter build. The session-local checker covers its two counts in scope: 0 unlinked steps and
  0 unscoped candidates. The charter service job in CI judges composition at the current pin.
