---
affected_files: []
cycle_number: 1
mission_slug: strict-pack-composition-01M6M0W4
reproduction_command:
reviewed_at: '2026-11-05T02:19:25Z'
reviewer_agent: claude:claude-opus-5-5:reviewer-renata
wp_id: WP07
---

# WP07 review, cycle 1: changes requested

Reviewer: claude:claude-opus-5-5:reviewer-renata. Reviewed open-packs `ca5df04` and charter PR 378 at `da172296`.

**Verdict: reject**, for H1, M1, M2 and M3 below. Please fix L1 and L4 in the same pass.

The validator work itself is sound. Gates at `ca5df04`: tests/ci 56, tests/docs 8, tests/release 8, tests/vocabulary 12; `validate-packs.sh`, `check-built-in.sh` and `gen_pack_reference.py --check` all pass. Charter at `da172296`: `openPacksRoundTrip` 54, `wholePackRoundTrip` 8, `spotlessCheck` and `checkstyleTest` pass; CI 18 pass, 3 skipped by design. SC-001 to SC-005 hold at the draft pin. Do not rework these.

## Not yours to fix

- **H2 (untracked `review-feedback-1.md` in the coord worktree blocked `consolidate`):** already fixed, coord commit `9d51722`.
- **H3 (`consolidate`'s default squash strategy is refused) and H4 (the charter repo loses its org layer under the as-is CLI after `syncPacks` at the new pin):** with the coordinator and the operator.
- **T027's three new issues:** with the operator. Do not file them, and do not retry. T027 reads `done`, but FR-016 and FR-011's follow-up stay unmet until they are filed.

## H1 (HIGH, charter PR 378): the `charter.yaml` edit blocks the charter repo's preflight

`.kittify/charter/charter.yaml` changes `spk-internal` to `spk-internal-glossary`, but `.kittify/charter/synthesis-manifest.yaml` is not restamped. Its `bundle_content_hash` is a content hash of that file, so `synthesized_drg` goes stale.

Reproduced in scratch clones under an isolated `HOME`, CLI 4.0.0rc8:

| Tree | `spec-kitty charter preflight` |
|---|---|
| `85c20fa1` with `f85cf23` packs | `PASSED` |
| `85c20fa1` plus only that one-line edit | `BLOCKED`: `synthesized_drg stale; run spec-kitty charter synthesize` |
| `85c20fa1` with only the `ca5df04` packs, `charter.yaml` unchanged | `PASSED` |
| `da172296`, any pack state | `BLOCKED` |

I ran `charter preflight`, not a real `implement` in that repo. This repo's ADR records the same preflight refusing `implement`.

**The fix I will accept:** run `spec-kitty charter synthesize` on the PR branch and commit the tool's restamped `.kittify/charter/synthesis-manifest.yaml`, with these conditions:

- Today the command exits 1 in every pack state I tried: `ca5df04` packs (the `depends_on` rejection), `f85cf23` packs (dangling `directive:RED_MAIN_RELEASE_DISCIPLINE`) and no synced packs. So do not wait for a clean exit, and do not treat rc 1 as success by silence: state the exit code and its reason in the PR body.
- The manifest diff must be exactly two value changes. In all three states I got the same result: `bundle_content_hash` `sha256:0f867d21...5916` and `manifest_hash` `40bb4510...5a33`. If anything else changes, stop and report it.
- Prove it on a fresh clone of the new head: `charter preflight` says `PASSED`, with and without the pack sync. In my scratch runs the stamp held after syncing `ca5df04` packs.
- Stage only that file, and do not commit anything else the command leaves behind.

**I will not accept:**

- hand-editing the hashes;
- turning preflight off in the charter repo (its preflight passes today, and that is an operator decision);
- reverting the `charter.yaml` edit, which would activate a stem the pack no longer has.

The stamp hashes `charter.yaml`, so moving the pin later should not disturb it. Re-check preflight at the re-point anyway.

## M1 (MEDIUM, open-packs ADR): FR-014's follow-through is implied, not stated

`docs/architecture/adr/2026-11-04-1-strict-pack-composition-and-the-end-of-cli-compatibility.md`, Neutral consequences, says only that the pin moves after this work reaches `main`. A stranger cannot tell that a step remains or who owns it. Add an explicit statement:

- spec-kitty-charter#378 stays a draft until the mission's pull request merges;
- the **operator triggers** the re-point to the final `main` SHA, because a rebase merge changes the commit;
- what moves in that one change: `openPacksRef`, `packs/open-packs.lock.yaml` and the comment in `gradle.properties`, with CI green, and only then is the PR marked ready;
- FR-014 and User Story 3 are not met until that lands.

## M2 (MEDIUM, charter PR 378): `docs/guides/compose-packs.md:173-176` is now false

The **Known gap** paragraph still says "`GET /offering` cannot serve it until spec-kitty-open-packs#75 lands". The PR's own `OpenPacksComposeTest` serves `built-in`, and known-failures is empty. Remove or rewrite it in the same change. Check the docs gates pass.

## M3 (MEDIUM, open-packs): `docs/guides/author-a-charter-pack.md` omits `pack.yaml`

The `my-pack/` layout at lines 27-42 does not list `pack.yaml`, and the guide never mentions a descriptor, `depends_on` or qualifying a cross-pack reference. Following it now produces a pack this repository's gate refuses: `<pack>/pack.yaml: missing: every pack needs a descriptor with its pack_id and name`. The T026 grep could not catch an omission. This falls short of FR-015.

Add `pack.yaml` to the layout, say it is required, and link `compose-packs.md` for `depends_on` and both reference forms. Bump `updated:`. Older core-era command wording stays out of scope.

## L1 (LOW, tests): a surviving mutant on the sidecar check

In `validate_pack`, changing `if kind == "payload" and inside.startswith("assets/"):` to `if kind == "payload":` leaves `tests/ci` green. A sidecar naming `templates/x` would then pass, which `SidecarPayloads` refuses because a template is not under `assets/`.

Fix in `test_an_asset_sidecar_names_a_payload_the_pack_holds_under_assets`: add a template payload rule to `payloads`, hold a file such as `templates/held.md`, and add `templates/held.md` to the refused names. Confirm the mutant goes red.

## L4 (LOW, docs): the sidecar check is described in the wrong place

- `docs/guides/validate-a-pack.md` puts it in step 2, with the invalid fixtures. It runs per pack in step 1, in `validate_pack`.
- The header of `scripts/ci/validate-packs.sh` omits it from step 1.

Move it to step 1 in both. Step 1 runs over `packs/` and `tests/fixtures/valid/`.

## After the fixes

Lane-e's head moves, so re-pin PR 378 and re-lock to the new head. Rerun the gates and both charter tasks, and confirm CI at the new charter head. `packs/internal` and `packs/qa` digests change only if those trees change.
