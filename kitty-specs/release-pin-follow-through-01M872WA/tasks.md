# Tasks: Release-pin follow-through

**Mission**: `release-pin-follow-through-01M872WA` · **Planning branch / merge target**: `ci/release-pin-follow-through`
**Inputs**: [spec.md](spec.md), [plan.md](plan.md), [research.md](research.md), [quickstart.md](quickstart.md)

Work red-first: each behaviour WP writes its failing test first, then the change. A `[ratchet]` test pins behaviour that already holds. Its no-op control is a mutation: the reviewer reverts or breaks the code under test and watches the test fail.

## Subtask Index

| ID | Description | WP | Parallel |
| --- | --- | --- | --- |
| T001 | Gate-judge test: `notes.md` notice passes, `notes.txt` `round_trip_red` fails, on the same fixture | WP01 | [P] |
| T002 | Real-jar test: a scratch pack with `notes.txt` fails the gate via `round_trip_red`; with `notes.md` it passes | WP01 | |
| T003 | `charter_pack_check.py` docstring states the ruling and cites spec-kitty-charter#631 | WP01 | |
| T004 | Red test: a symlinked directory's artifact is not derived | WP02 | [P] |
| T005 | `pack_files()` helper; `derived_manifest` walks with it | WP02 | |
| T006 | Audit the other pack walks; switch the ones that mirror the charter's file set | WP02 | |
| T007 | Pin the duplicated-and-unheld `membership_mismatch` case | WP02 | |
| T008 | Derive-then-check test asserts the manifest bytes changed | WP02 | |
| T009 | `attestation_note()` + `attestation-note` subcommand, red-first unit tests | WP03 | [P] |
| T010 | Red workflow-structure tests: no token beside `charter_pin.py apply`; provenance job read-only and never failing; note reaches the PR body | WP03 | |
| T011 | Split the bump step into lookup (token) / re-derive (no token) / push (token) | WP03 | |
| T012 | `provenance` job: download both jars, `gh attestation verify`, warn only | WP03 | |
| T013 | Wire the provenance outputs into `bump` (`needs`, `!cancelled()`, PR body) | WP03 | |
| T014 | Update the workflow header comment (tokens, provenance) | WP03 | |
| T015 | Red tests: the four #304 false positives and the five false negatives | WP04 | [P] |
| T016 | Anchor the false-positive patterns to the end of a clause | WP04 | |
| T017 | Cover the false-negative variants | WP04 | |
| T018 | Shorten the `::error` message to 200 characters or fewer; run over the repo with 0 findings | WP04 | |
| T019 | Guide: stray-file paragraph states the accepted gap (#331 ruling, spec-kitty-charter#631) | WP05 | |
| T020 | Guide: the bump section covers the token split and the warn-only attestation check | WP05 | |
| T021 | Roadmap: Charter pin **Waits on** reflects rc.3 | WP05 | |
| T022 | Changelog entry in both changelog copies | WP05 | |

## Phase 1 – Independent behaviour WPs (parallel)

### WP01 – Stray-file gap pinned (#331) → [tasks/WP01-stray-file-gap-pinned.md](tasks/WP01-stray-file-gap-pinned.md)

**Goal**: the gate keeps failing an unmodelled stray file through pack-check's round trip, with no override (FR-001); the gate's docstring says why (part of FR-002). Priority P1.
**Independent test**: `python3 -m unittest tests.ci.test_charter_pack_check`.

T001 Gate-judge test, same-fixture control (WP01)
T002 Real-jar stray-file test (WP01)
T003 Docstring wording (WP01)

Dependencies: none. Risks: the real-jar test needs Java 25 and the jar. It runs in the `Charter service validation` job (`PACK_CHECK_JAR`) and is skipped locally without it.

### WP02 – Manifest mirror parity (#262) → [tasks/WP02-manifest-mirror-parity.md](tasks/WP02-manifest-mirror-parity.md)

**Goal**: the derived manifest walks the pack as the charter does, and the mismatch wording and derive test are pinned (FR-003, FR-004, FR-005). Priority P1.
**Independent test**: `python3 -m unittest tests.ci.test_validate_pack_schemas`.

T004 Red symlinked-dir test (WP02)
T005 `pack_files()` helper (WP02)
T006 Audit other walks (WP02)
T007 Mismatch pin test (WP02)
T008 Derive test proves a write (WP02)

Dependencies: none. Risks: the pack digests and manifests must not change for the shipped packs (no symlinks in `packs/`); `validate-packs.sh` confirms this.

### WP03 – Release bump hardening (#310) → [tasks/WP03-release-bump-hardening.md](tasks/WP03-release-bump-hardening.md)

**Goal**: no token in reach of the re-derivation, and a warn-only attestation check whose outcome is stated in the bump PR (FR-006, FR-007, FR-008). Priority P2.
**Independent test**: `python3 -m unittest tests.ci.test_charter_pin tests.ci.test_workflows`.

T009 `attestation_note` (WP03)
T010 Red workflow-structure tests (WP03)
T011 Split the bump step (WP03)
T012 `provenance` job (WP03)
T013 Wire into `bump` (WP03)
T014 Header comment (WP03)

Dependencies: none. Risks: the bump path runs only on `main`, so the live proof is the first rc.4 run or an operator dispatch from a fork. Structure tests are the gate here.

### WP04 – Self-binding vocabulary precision (#304) → [tasks/WP04-self-binding-vocabulary.md](tasks/WP04-self-binding-vocabulary.md)

**Goal**: the #304 false positives pass and its false negatives are flagged (FR-009). Priority P3.
**Independent test**: `python3 -m unittest discover -s tests/vocabulary`; `python3 scripts/ci/check_vocabulary.py`.

T015 Red tests (WP04)
T016 Anchor patterns (WP04)
T017 Cover variants (WP04)
T018 Error message and repo run (WP04)

Dependencies: none. Risks: a new pattern flags existing pack prose. The repo run must stay at 0 findings, or the prose is fixed in the same WP and named in the review.

## Phase 2 – Docs and changelog

### WP05 – Docs, roadmap and changelog → [tasks/WP05-docs-roadmap-changelog.md](tasks/WP05-docs-roadmap-changelog.md)

**Goal**: the guide, roadmap and changelog match the shipped behaviour of WP01–WP04 (FR-002, FR-010, FR-011). Priority P2.
**Independent test**: `python3 -m unittest discover -s tests/docs`; `scripts/docs/check_docs_freshness.py`, if wired.

T019 Guide stray-file paragraph (WP05)
T020 Guide bump section (WP05)
T021 Roadmap Waits on (WP05)
T022 Changelog entry (WP05)

Dependencies: WP01, WP02, WP03, WP04.

## Outside the WPs (runner, at hand-off)

- Close #252 (completed; the retirement is held by #330), with a comment.
- Rewrite #287's "State and order": rc.3 is pinned, pack-check ships from rc.3, and #139 and #295 are closed.
- #315 follow-on: waits on the dispatcher's answers on sources and cadence.

## MVP

WP01 (the operator's first item) and WP02. Both are small and independent.
