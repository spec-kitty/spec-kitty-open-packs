---
title: Next slices, November 2026
description: "The order in which the open-packs backlog lands after the 2026-11-12 triage: eight slices, what holds each, and the issues that wait on the charter or core."
doc_status: active
updated: '2026-11-12'
related:
- plans
- packs/catalog-proposal
---
# Next slices, November 2026

This plan comes from a three-lens planning squad run on 2026-11-12 against `main` 34a4de9: readiness and value, file overlap, and charter sequencing. Operator rulings from the same day are applied. A slice is one pull request. The issue tracker owns each issue's scope; this page owns the grouping and the order.

## Order

| # | Slice | Issues | Size | Lands |
|---|---|---|---|---|
| 1 | Charter slice B migration | #241, #242, and the charter pin bump | L | First |
| 2 | Mocking-boundary and test-value doctrine | #216 (GA), then #209 and #151 | L | In parallel with 1, rebased onto it |
| 3 | Analyze prompt (epic #244) | #246 first, then #237 and #213; #214 and #247 later | M | Now |
| 4 | Stale paths left by the split | #195, #227, #159 | M | Right after 1 |
| 5 | Implement, review and plan prompts | #164, #226, #222 (review half), #158, #176, #210 | M | After 4 |
| 6 | Specify front half | #149, #223, #220, #247 (specify half) | M | Any time |
| 7 | Tasks family | #230, #236 | S | After 3 |
| 8 | Graph and directive sweeps (epic #245, then #233) | #196 (with the orphan census from #225), #224, #197, #233 | L | Last |

Every slice edits `CHANGELOG.md` and restamps pack digests. Land slices one at a time and restamp on rebase; never hand-merge a digest.

## Slice notes

**1. Charter slice B migration.** Charter PR #501 merged on 2026-11-12 (`ddfd9549e3c2`). The charter has no release yet, so the bump is a commit pin: move `charter.lock.yaml` from `fb24052` to `ddfd954` or later, and leave `release_tag` and `jar_sha256` empty. #241 and #242 go in the same pull request, because only both together register all 19 packs against slice B. The pull request touches:
- `scripts/ci/charter_service_check.py`, `scripts/ci/validate_pack_schemas.py`, `scripts/docs/gen_pack_reference.py`, `scripts/ci/check_vocabulary.py` and their tests;
- the README merges (#241) and the `org-charter.yaml` conversions (#242).

The pin jumps 218 charter commits, so run the service check on the bumped pin before the content edits. Landing it clears charter #509.

**2. Test doctrine.** #216 is the only open 4.0.0 GA item; #218 is folded into it.
- Pick a free directive id: 047, 052 and 053 are taken.
- Splitting the mindset half out of DIRECTIVE_041 is its own reviewed change.
- #209 is split by tier: the general rule goes in `foundation` and `testing`, and Spec Kitty's CI-workflow specifics go in `internal`.
- #209 and #151 edit the same tactics as #216, so they follow it.

**3. Analyze prompt.** Every issue here edits `packs/foundation/missions/software-dev/steps/analyze.prompt.md`.
- #246 (P1) adds the `finalize-tasks --validate-only` readiness check. That command returns only a topology preview, so analyze must not treat it as a write.
- The `cave-kitty` analyze prompt needs the same change.

**4. Stale paths.** The split (#198) left shipped prompts and procedures pointing at `packs/built-in/...` files that no longer exist. Regenerate the `.agents/skills/` copies; do not hand-edit them.

**5–7. Step prompts.** These keep `tests/ci/test_software_dev_ascii.py` green. #231 stays on hold, because core's `wps.schema.json` rejects a `notes` field until core #5072 lands. #223 writes its answers to `spec.md` until core #1739 adds `meta.json` fields.

**8. Sweeps.** #224 touches every graph file, and #233 touches every directive that carries `enforcement:`. Run them in a quiet window, after the content slices.

## Any time

These mostly add new files, so they only collide on graph registration and `CHANGELOG.md`:
- #238 (writing pack) and #217 (foundation), both tier-ruled;
- #239: the canonical path is `research/source-register.csv`, and core's gathering guard follows at its pin bump (core #4221);
- #147, tactic only;
- #154, #155, #156 and #215 (epic #157);
- #6 and #12, the future bundles;
- docsite #23 and #24, best after slice 1 fixes the reference generator.

## After slice 1

- #201: `policy.yaml` for the built-in members.
- #211 and #212: language-pack presets, and the `java-ddd` preset on `built-in`.
- #124: re-enable charter preflight.
- #221, #234 and #159: glossary, because #242 rewrites the core glossary pack.
- #229: the maintainer how-to, which should not describe `pack.md` or `org-charter.yaml`.

## Waiting on the charter or core

| Issue | Waits on |
|---|---|
| #139 | spec-kitty-charter #512 (a human-performed profile in the contract) |
| #231 | core #5072 (`notes` in the wps schema) |
| Next pin bump | charter slice C (#467); watch charter #110 (manifest restamping) |

## Open decisions

- **#228:** where the template authoring contract lives.
- **#140 and #142:** scope and home.
- **#239:** the research requirement family, to agree with core.

## Stale paths in issue bodies

Several issues cite paths from before the split, or from core. Their current homes:

| Issue | Path as written | Path today |
|---|---|---|
| #149, #164, #176 | `packs/built-in/missions/mission-steps/software-dev/<step>/prompt.md` | `packs/foundation/missions/software-dev/steps/<step>.prompt.md` |
| #159 | `packs/built-in/tactics/...` | `packs/foundation/tactics/communication/` |
| #220 | `packs/built-in/missions/software-dev/templates/` | `packs/foundation/missions/software-dev/templates/` |
| #227 | `packs/built-in/agent_profiles/` | the split packs' `agent_profiles/` |
| #235 | `packs/built-in/tactics/refactoring/` | `packs/refactoring/tactics/refactoring/` |
| #240 | `packs/built-in/styleguides/common-docs` | `packs/writing/styleguides/` |
| #142, #154–#157, #223, #232 | core `src/doctrine/...` | the matching pack paths |
| #147 | DIRECTIVE_052 | a free id or slug; 052 is taken |
