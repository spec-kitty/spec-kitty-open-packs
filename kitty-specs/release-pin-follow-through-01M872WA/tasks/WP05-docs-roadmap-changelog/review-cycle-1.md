---
affected_files: []
cycle_number: 1
mission_slug: release-pin-follow-through-01M872WA
reproduction_command:
reviewed_at: '2026-11-24T16:37:24Z'
reviewer_agent: claude::reviewer-renata
wp_id: WP05
---

**Issue 1 (blocking): spec-kitty-charter#631 is closed, not outstanding.**

The charter tracker shows #631 closed as *completed* on 2026-11-21T10:55Z. Charter PR #633, "the round trip leaves out every file the census does not hold (#631)", merged on 2026-11-21T10:55Z. That is after `service-v0.1.0-rc.3` (release PR #622, merged 2026-11-20). No charter release has been merged since. So the fix is on charter `main` but in no release, and the open-packs pin is still rc.3.

Three sentences treat #631 as a charter fix that has yet to land. (The WP05 prompt itself carried the stale premise: "the charter fixes #629, #630 and #631".)
- `docs/plans/roadmap.md`, **Waits on**: "spec-kitty-charter#631, before a stray file other than a Markdown note may stay".
- `docs/guides/validate-a-pack.md`, Stray files: "Until spec-kitty-charter#631 lets the round trip skip the files the store does not hold".
- `docs/changelog/CHANGELOG.md`, the #331 bullet: "Only Markdown notes may stay in a pack until spec-kitty-charter#631."

Fix: say that the remedy is a charter release that carries #631 (fixed on charter `main` by #633, not in rc.3), plus the pin bump to it. In the roadmap, list it apart from the still-open fixes #629 and #630, for example: "a charter release that carries spec-kitty-charter#631 (fixed on main), before a stray file other than a Markdown note may stay (#331)". The guide and changelog take the same wording ("until the pin moves to a charter release that carries spec-kitty-charter#631").

The same stale premise appears in WP01's approved code. It is out of WP05's scope and is not part of this verdict, but it should go into the hand-off. The `charter_pack_check.py` docstring and the `RealPackCheck` test comment both read "Until spec-kitty-charter#631 lets…" and "Expected to flip once #631 lets…". The flip now happens at the pin bump. The nightly main check should already see `notes.txt` pass.

**Verified accurate (no change needed):**
- The workflow description matches `charter-track.yml` on lane-e:
  - `provenance` has `contents: read` and `attestations: read`. A SHA mismatch is `::error`, the job fails, and `derive` and `bump` are skipped. An attestation failure is `::warning` with state `unverified`.
  - `derive` has `contents: read`, uses `persist-credentials: false`, and puts no token in any step's env. It hands on `file-changes.json` and `head`.
  - `bump` has `contents: write`. It does no checkout and runs no Python. Its allowlist regex covers the lock, the CHANGELOG, `packs/*.source.yaml`, the pack and fixture manifests, and `docs/packs/*.md`. It checks that `head` equals `github.sha`. Only its last step holds `PR_CREATION_TOKEN`.
- The attestation flags match the doc: `--signer-workflow spec-kitty/spec-kitty-charter/.github/workflows/service-release.yml --source-ref refs/tags/<tag>`.
- The stray-file text matches the WP01 tests: `notes.md` is a notice, and `notes.txt` is `round_trip_red` and fails with exit 1.
- The #262 wording ("never followed links … a test now holds it there") matches the WP02 tests (`linked_pack`, the twice-and-unheld ordering, and the derive-wrote check).
- The #304 examples all appear verbatim in the WP04 tests (spared and flagged). The 48-character message truncation is in `check_vocabulary.py`.
- #629 and #630 are open.

**Non-blocking nits (take them while you are in there):**
1. `derive` "holds no token and no secret". GitHub still mints a read-only `GITHUB_TOKEN` for the job, and `actions/checkout` uses it. More precise: "holds no write token and no secret, and exposes none to the pin tooling".
2. The Release-provenance flags omit `--repo spec-kitty/spec-kitty-charter`. The `…` covers it, so mentioning it is optional.
3. A jar that cannot be downloaded is also recorded as *not verified* and only warns. The guide could say "a missing jar or attestation".
4. The changelog quotes "Advisory in version 1" as an example. `findings_in` flags that line (CHANGELOG line 946). The guard scans only `packs/`, so no gate fails, and older entries quote the same way. Ignore it unless you want backticks around the examples.
