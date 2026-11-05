---
verdict: pass_with_notes
mode: post-merge
reviewed_at: 2026-11-05T11:49:08.576459+00:00
findings: 4
gates_recorded:
  - id: gate_1
    name: wp_lane_check
    command: spec-kitty review (internal gate 1)
    exit_code: 0
    result: pass
  - id: gate_2
    name: dead_code_scan
    command: spec-kitty review (internal gate 2)
    exit_code: 1
    result: fail
  - id: gate_3
    name: ble001_audit
    command: spec-kitty review (internal gate 3)
    exit_code: 0
    result: pass
issue_matrix_present: true
mission_exception_present: false
---

# Mission Review Report: strict-pack-composition-01M6M0W4

**Reviewer**: claude (claude-opus-5-5), post-merge mission review per `skill://spec-kitty-mission-review`
**Date**: 2026-11-05
**Mission**: `strict-pack-composition-01M6M0W4` — Strict pack composition (epic #118, PR #121)
**Baseline commit**: `f85cf2365e78f75df3f0d842723b0f2002f9de81` (`git merge-base origin/main HEAD`, tag `pre-charter-cutover`). `meta.json` `baseline_merge_commit` (`5fb6ef4`) is the acceptance-finalize commit just before the merge and was deliberately not used.
**HEAD at review**: `cf8dcf165b129945533fb93bd8e611d0acf89008` (= PR #121 head; mission merge `8bc94dd`)
**WPs reviewed**: WP01..WP07 (all `done`, `spec-kitty agent tasks status`: 7/7, 100 %)
**Diff reviewed**: `git diff f85cf23..HEAD` — 95 files, +4411/−272. Production code: `scripts/ci/validate_pack_schemas.py` (+147/−9), `scripts/docs/gen_pack_reference.py` (+30/−84), `scripts/ci/{validate-packs.sh,check-built-in.sh,built_in_digest.py}`; pack content under `packs/`; tests under `tests/ci`, `tests/docs`; docs; `.kittify/config.yaml`.

The YAML frontmatter and the `## Findings` section below were written by `spec-kitty review --mission strict-pack-composition-01M6M0W4 --mode post-merge` and is kept as the tool wrote it. Its four `dead_code` findings are false positives; see Gate 4.

## Findings

- **dead_code** `scripts/ci/validate_pack_schemas.py` — `held_artifacts`: no non-test callers found
- **dead_code** `scripts/ci/validate_pack_schemas.py` — `split_qualifier`: no non-test callers found
- **dead_code** `scripts/ci/validate_pack_schemas.py` — `written_references`: no non-test callers found
- **dead_code** `scripts/ci/validate_pack_schemas.py` — `composition_violations`: no non-test callers found

---

## Gate Results

This repository has no `tests/contract/` or `tests/architectural/` and no cross-repo e2e scenario suite. Those gates are recorded as `not_applicable` and the repository's own equivalents (the same commands the required `Validate packs gate` runs, `.github/workflows/validate-packs.yml:59-86`) were run instead, at HEAD `cf8dcf1`, with Python 3.12.3 and `pyyaml==6.0.3`, `jsonschema==4.26.0` (the CI pins) in a throwaway venv outside the repository.

### Gate 1 — Contract tests
- `tests/contract/`: **not_applicable** (directory does not exist).
- Equivalents:

| Command | Exit | Result |
|---|---|---|
| `python -m unittest discover -s tests/ci` | 0 | 56 tests OK |
| `python -m unittest discover -s tests/docs` | 0 | 8 tests OK |
| `python -m unittest discover -s tests/release` | 0 | 8 tests OK |
| `python -m unittest discover -s tests/vocabulary` | 0 | 12 tests OK |
| `bash scripts/ci/validate-packs.sh` | 0 | contract `85c20fa1`, 25 schemas; 6 packs ok; `cross-pack checks over 6 packs (0 violations)`; invalid fixture fails as expected (7 violations) |
| `bash scripts/ci/check-built-in.sh` | 0 | digest matches `3bb5f106…a5b429e0` |
| `python scripts/ci/check_vocabulary.py` | 0 | 603 files, 0 findings |
| `python scripts/docs/gen_pack_reference.py --check` | 0 | 5 pages, no drift |

- Result: **PASS**. PR #121's own CI (`gh pr view 121`): `Charter Pack validation`, `Validate packs gate`, `Generated-content drift gate`, `build` all SUCCESS at `cf8dcf1`.

### Gate 2 — Architectural tests
- `tests/architectural/`: **not_applicable** (directory does not exist). The layering-like property here is NFR-002 "the charter remains the authority"; it is checked under NFR-002 below (PASS).

### Gate 3 — Cross-repo E2E
- Command: `gh pr checks 378 -R spec-kitty/spec-kitty-charter` → exit 0. Gradle not run (by instruction).
- Proof artifact: spec-kitty/spec-kitty-charter#378, **OPEN, draft**, branch `packs-real-compose`, head `297b8b1b`. All required checks pass, including `Service / verify`, `whole-pack`, `gate`; three skipped by design (`Freshness SLA (weekly)`, `deploy`, `service`).
- Pin: `gradle.properties` `openPacksRef=bd44674e75ac618492cabed3e46628579105a202` and `packs/open-packs.lock.yaml` `commit: bd44674…` (from `gh pr diff 378`). `bd44674` is an ancestor of HEAD, and `git diff bd44674 HEAD -- packs/ tests/fixtures/ scripts/` is **empty**. Only `.kittify/config.yaml` (+7, preflight off, commit `c8d798d`), one ADR description line, and `kitty-specs/` changed after the pin, so the pack content the charter composed is byte-identical to what lands.
- At `297b8b1`, `service/packs/src/test/resources/whole-pack/known-failures.yaml` is `known_failures: []`. `OpenPacksComposeTest` has each pack with `built-in`, all five together (served names asserted, `containsExactly("built-in","cave-kitty","event-driven","spec-kitty-internal","quality-assurance")`), and negative controls (`PACK_REFERENCE_UNQUALIFIED` for an edge and a typed reference, `PACK_REFERENCE_PACK_MISSING`, unknown dependency, malformed range, cave-kitty served-edge).
- Result: **PASS (pre-merge proof)**. No `mission-exception.md` needed. The final re-pin of #378 to the merged `main` commit is FR-014's post-merge part and is still open (DRIFT-1).

### Gate 4 — Issue Matrix
- Command: `spec-kitty review --mission strict-pack-composition-01M6M0W4 --mode post-merge` → exit 0, `Verdict: pass_with_notes (4 finding(s))`, `✓ Issue matrix: 17 row(s) validated`, `✓ WP lane check: all 7 WP(s) in done`, `✓ Review artifact consistency`, `✓ BLE001 audit`, `✗ Dead-code scan: 4 unreferenced public symbol(s)`.
- **Side effects of this command**: it wrote this file (frontmatter + `## Findings`) and re-materialized `kitty-specs/strict-pack-composition-01M6M0W4/status.json` (now shows `M` in `git status`). The rewrite fills `mission_number`/`mission_type`, adds `notes`/`subtasks`, sets each WP's `agent` to the reviewer identity and **drops `implementer_of_record`**. The reviewer did not edit it.
- **Dead-code findings are false positives.** All four symbols have live callers in the same module, on the production path `validate-packs.sh:42` → `main()` → `cross_pack_violations` (`validate_pack_schemas.py:971`): `held_artifacts` at :886, `composition_violations` at :924, `written_references` at :857, `split_qualifier` at :793, :809, :815, :919. The scan counts only cross-file callers.
- Rows: 17 (`issue-matrix.json` `rows`).

| Issue | Verdict | WP | Evidence check |
|---|---|---|---|
| #47 | fixed | WP02 (+WP01, WP06) | descriptors `packs/{qa,event-driven,cave-kitty}/pack.yaml`; glossary rename R99; descriptor guard `validate_pack_schemas.py:838-842`. Issue OPEN, closed by #121 `Closes #47` |
| #75 | fixed | WP03 | six sidecars + manifest + `built-in.source.yaml` in diff; mutation probe (below) red. Closed by #121 |
| #113 | fixed | WP06 | 78 `built-in::` in `packs/internal` (git grep). Closed by #121 |
| #116 | fixed | WP05 | 12 in `packs/event-driven`. Closed by #121 |
| #117 | fixed | WP04 | 3 in `packs/qa`. Closed by #121 |
| charter#363 | deferred-with-followup | WP04 | evidence_ref names spec-kitty-charter#378 (OPEN, draft); #363 OPEN, body corrected 2026-11-05 ("## Correction (2026-11-05)") |
| #105, #106, #114, #72, #73, #92, #93, #94, #118, charter#360, charter#365 | not-applicable | — | context / C-007 out of scope |

  - Empty / `unknown` verdicts: **0**. `in-mission` rows: **0**.
  - `deferred-with-followup` rows without a follow-up handle: **0** (1 row, handle charter#378 verified with `gh pr view 378`).
  - `not-applicable` (11 rows) is outside the skill's four-value allow-list, but it is a terminal verdict in the installed CLI (`specify_cli/cli/commands/review/_issue_matrix.py:61-83`, ADR `2026-09-20-1-issue-matrix-not-applicable-verdict`). The skill text is stale on this point. Accepted.
  - Hygiene: 11 rows still carry `"title": "<fill at WP-implementation time>"` (e.g. `#113`, `#116`, `#117`, `#47`, `#75`). Not a gate failure.
- Result: **PASS**.

---

## FR Coverage Matrix

Test adequacy uses mutation reasoning. Every test in `CompositionChecks` (`tests/ci/test_validate_pack_schemas.py:362-606`) calls the production `cross_pack_violations` with a positive control on the same fixture, so deleting a check turns its test red. Independent mutation probes on throwaway copies of HEAD (`git archive HEAD`, full `validate-packs.sh`) gave these results:

| Probe | rc | Gate output (first line) |
|---|---|---|
| unmodified HEAD | 0 | — |
| qa edge unqualified | 1 | `qa/drg/fragment.yaml: bare reference 'tactic:bdd-scenario-formulation' is held only by built-in` |
| event-driven typed ref unqualified | 1 | `…evd-event-bridge-port.tactic.yaml: bare reference 'tactic:reference-architectural-patterns'…` |
| internal agent_profile edge bare | 1 | `internal/drg/fragment.yaml: bare reference 'agent_profile:reviewer-renata'…` |
| internal procedure typed ref bare | 1 | `…cloud-session-dispatch.procedure.yaml: bare reference 'directive:DIRECTIVE_025'…` |
| event-driven / internal `depends_on` removed | 1 / 1 | `…names a pack outside this pack's depends_on closure` |
| cave-kitty `depends_on` removed | **0** | — (accepted SC-002 exception) |
| qa `pack.yaml` removed | 1 | `qa/pack.yaml: missing: every pack needs a descriptor…` |
| duplicate `pack_id` / duplicate `name` | 1 / 1 | `cave-kitty/pack.yaml, qa/pack.yaml: pack_id '01M6MF4FV4AMQF4RC8CY6JNESX' is declared by more than one pack` |
| qualified target missing | 1 | `reference 'built-in::tactic:no-such-tactic': built-in does not hold…` |
| qualifier naming an unknown pack | 1 | `reference 'nowhere::tactic:…' names a pack outside this pack's depends_on closure` |
| cave-kitty `depends_on` names an unknown `pack_id` | **0** | — (RISK-1) |
| built-in sidecar path re-anchored at `assets/` | 1 | `payload assets/assets/docs_structural_lint.py does not exist` |

| ID | Description (brief) | WP Owner | Test File(s) / evidence | Test Adequacy | Finding |
|---|---|---|---|---|---|
| FR-001 | Contract pinned at/after charter `88ed36e4` | WP01 | `validate_pack_schemas.py:50` `CHARTER_COMMIT = 85c20fa1…`; `gh api …/compare/88ed36e4...85c20fa1` → `ahead_by 20, behind_by 0` | ADEQUATE (gate run prints the pin) | — |
| FR-002 | Qualified refs pass in both forms | WP01 | `test_validate_pack_schemas.py:419,449,470,520,529,600`; real packs with 93 qualified refs pass | ADEQUATE | — |
| FR-003 | Five defect classes fail; real packs pass | WP01, WP07 | `:440` (bare→other), `:498` (closure), `:512,:549` (target not held), `:535` (no descriptor), `:541` (dup id/name); real run 0 violations; probes above | ADEQUATE. The fixtures are unit-test temp dirs, not on-disk `tests/fixtures/invalid/**` (owned by WP01, no diff) | DRIFT-5 |
| FR-004 | Compliant descriptors, unique tool-minted ids, v1.0.0, fixture has one | WP02 | `packs/{qa,event-driven,cave-kitty}/pack.yaml`, `tests/fixtures/valid/example-pack/pack.yaml` (ids `01M6MF4FV4…`, distinct); schema + uniqueness via gate; dup probe red | ADEQUATE (version value is data, checked by inspection) | — |
| FR-005 | Four packs `depends_on` built-in `>=1.0,<2` | WP02, WP04–06 | descriptor diffs; closure probes red for qa/evd/internal; cave-kitty not locally provable | PARTIAL (cave-kitty) | DRIFT-2 |
| FR-006 | Glossary stem rename + no-descriptor guard | WP06, WP01 | rename R99 `spk-internal-glossary.glossary-pack.yaml`; no stale stem (`grep`); `:535` | ADEQUATE | — |
| FR-007 | Six sidecars relative to `assets/`, manifest/digest/page together | WP03 | `:149` (incl. the WP07-L1 `templates/held.md` mutant fix); `check-built-in.sh` rc 0; sidecar probe red | ADEQUATE | — |
| FR-008 | qa 3 refs qualified | WP04 | `git grep -o 'built-in::' -- packs/qa` = 3; independent re-scan 0 bare→built-in | ADEQUATE (gate) | — |
| FR-009 | event-driven 12 refs | WP05 | = 12 (7 edges + 5 typed); re-scan 0 | ADEQUATE (gate) | — |
| FR-010 | internal 78 refs / 31 targets incl. 5 agent_profile | WP06 | = 78; `reference-inventory.txt` 31 targets; agent_profile probe red | ADEQUATE (gate) | — |
| FR-011 | 24 qa agent-profile refs checked: qualify or log | WP04, WP07 | left bare; open-packs#119 OPEN ("24 left bare in quality-assurance"); re-scan counts 6+13+1+4 = 24 bare profile scalars | ADEQUATE (decision outcome) | DRIFT-4 |
| FR-012 | Generator reads/publishes `depends_on`; no `purpose` field | WP01 | `tests/docs/test_gen_pack_reference.py:132,154`; `docs/packs/*.md:31` `**Depends on:** \`01ARWG13C000000000000000FG >=1.0,<2\``; `gen_pack_reference.py:159-188` | ADEQUATE | — |
| FR-013 | Charter compose test on real packs + negative controls | WP04/05/07 (charter) | charter#378 `OpenPacksComposeTest` (see Gate 3) | ADEQUATE (external, pre-merge pin) | — |
| FR-014 | Charter pin/lock/diagnostics/known-failures to final merged commit | WP07 | #378 still pins `bd44674`; draft | **MISSING (post-merge)**, accepted | DRIFT-1 |
| FR-015 | Docs state new reality; changelog records the break | WP03, WP07 | `docs/changelog/CHANGELOG.md:24-31`; ADR `2026-11-04-1-…`; `author-a-charter-pack.md:28,46-49`; `validate-a-pack.md:26,78`; digest wording `built_in_digest.py:55`, `check-built-in.sh:3-6`; no "re-seed" digest wording left (`git grep`) | ADEQUATE (inspection; no test by nature) | — |
| FR-016 | Stale issue text corrected; #72 noted; core issue links `_anchor_for` ↔ #7153 | WP07 | #72 comment 2026-11-05T01:37Z; #47/#113/#118/charter#363 bodies updated 01:37Z; charter#365 comment; spec-kitty#7193 body cites `_anchor_for` and #7153 | ADEQUATE (verified via `gh`) | — |
| NFR-001 | Gate grows < 5 s | WP01 | warm runs of `validate-packs.sh`: baseline `f85cf23` 5.34 s → HEAD 8.11 s (+2.77 s); WP01 review measured +1.2 s | PASS | — |
| NFR-002 | < 150 added validator lines; no ordering/level/range/sibling logic | WP01 | `git diff --numstat` +147/−9 raw, 124 non-blank non-comment; `composition_violations` docstring :834-835 and code judge none of those | PASS (3-line margin on the raw count) | — |
| NFR-003 | 100 % of 93 sites in inventory | WP07 | inventory lists 91 of 93 (WP07 cycle-2 note "L2") | **MISS**, accepted | DRIFT-3 |
| SC-001 | 5 configurations compose, 0 refusals | — | charter#378 CI green at pin `bd44674` | PASS (pre-merge) | — |
| SC-002 | Every negative control turns red | — | probes above; cave-kitty exception | PARTIAL, accepted | DRIFT-2 |
| SC-003 | 93 qualified, 0 bare held only by another pack | — | independent re-scan (does not import the validator): 0 bare `kind:id` / typed refs to built-in-only items across cave-kitty, event-driven, internal, qa; 3+12+78 = 93 `built-in::` occurrences | PASS | — |
| SC-004 | Charter known-failure/diagnostics lists empty | — | `known_failures: []` at #378 `297b8b1`; lands with FR-014 | PASS (pre-merge), final with DRIFT-1 | — |
| SC-005 | Each defect caught; allowance removed | WP07 | `git grep PENDING_PACKS\|PENDING_DESCRIPTORS -- scripts tests docs` empty; probes above | PASS | — |

**Legend**: ADEQUATE = test constrains the required behavior; PARTIAL = test exists but does not cover all of it; MISSING = no test or no delivery found; FALSE_POSITIVE = test passes even when the implementation is deleted. **No FALSE_POSITIVE tests were found.** `tests/ci/test_validate_pack_schemas.py` and `tests/docs/test_gen_pack_reference.py` drive the real entry points (`cross_pack_violations`, `validate_pack` via `main`, `build_reference`/`render_page`) on on-disk fixtures in the production shape. WP07 L1's surviving mutant (`kind == "payload"` without `startswith("assets/")`) is now killed by `:151-163`.

---

## Drift Findings

### DRIFT-1: FR-014 / User Story 3 are not delivered at merge (accepted, tracked)

**Type**: PUNTED-FR
**Severity**: HIGH (accepted known issue; does not block this verdict)
**Spec reference**: FR-014, User Story 3, SC-004 (final), C-006
**Evidence**:
- charter#378 is `OPEN`, `isDraft: true`, `openPacksRef=bd44674…` (`gh pr diff 378`). It does not point at a `main` commit, because none exists yet.
- `acceptance-matrix.json` FR-014 row: `"pass_fail": "pass"`, but its description is rewritten to "Pre-merge part only … FR-014 as written is NOT met by this verdict".
- ADR `docs/architecture/adr/2026-11-04-1-…md:152-165`: "One step of this decision remains, and the operator triggers it … FR-014 and User Story 3 of the mission are not met until this lands."

**Analysis**: C-006 forbids moving the pin before merge, so this cannot be met inside the mission. The step is tracked by charter#378 (open) and epic #118 (open; its body line 21 states the re-point as the last step). PR #121 does not close #118. Two things remain: the `pass` verdict on an FR whose acceptance row redefines its text is acceptance-record drift, and #378's intermediate pin commits (incl. stale lock `aa2f7ee`, per the PR #121 body) still need collapsing before it leaves draft. The second item is only recorded in PR #121's body.

### DRIFT-2: SC-002 / User Story 1 scenario 4 does not hold for cave-kitty (accepted, untracked)

**Type**: PUNTED-FR (partial SC)
**Severity**: MEDIUM (accepted known issue)
**Spec reference**: SC-002, US1 scenario 4, FR-005
**Evidence**: mutation probe `cave-depends-on-removed` → `validate-packs.sh` rc 0. Charter `OpenPacksComposeTest.java:207-214` `caveKittyWithoutItsDependencyIsNotRefused` asserts that it composes; only the served-edge assertion (`:116-121`) notices.
**Analysis**: cave-kitty writes no machine-checked reference, so neither the local gate nor the service can refuse a missing `depends_on`. The spec's Edge Cases anticipate the descriptor but not this SC exception. It is compensated by the charter's served-edge assertion. **No tracking issue** exists. The PR #121 body is the only record.

### DRIFT-3: NFR-003 inventory lists 91 of 93 sites (accepted, untracked)

**Type**: NFR-MISS
**Severity**: LOW
**Spec reference**: NFR-003
**Evidence**: WP07 approval note (status event `01M6N8YTT7…`, "L2 (inventory lists 91 of 93 sites) remains a small NFR-003 shortfall"); PR #121 Deferred.
**Analysis**: This is a classification-record gap only. SC-003 independently confirms all 93 sites qualified and 0 bare. **No tracking issue**, which is acceptable for a closed, historical record.

### DRIFT-4: FR-011 resolved by deferral (tracked)

**Type**: PUNTED-FR (permitted outcome)
**Severity**: LOW
**Spec reference**: FR-011
**Evidence**: `validate_pack_schemas.py:787` "Agent profiles mint none there, so none here." Independent re-scan finds 24 bare built-in ids in `packs/qa/agent_profiles` (`tactic-references` 13, `styleguide-references` 6, `toolguide-references` 1, `operating-procedures` 4). open-packs#119 OPEN, title matches.
**Analysis**: FR-011 explicitly permits "logged in a follow-up issue with the reason". Met.

### DRIFT-5: No on-disk composition fixtures; WP01-owned `tests/fixtures/invalid/**` unchanged

**Type**: PUNTED-FR (form only)
**Severity**: LOW
**Spec reference**: FR-003 ("Each has a fixture that fails")
**Evidence**: `git diff f85cf23..HEAD --stat -- tests/fixtures/invalid` is empty; WP01 frontmatter `owned_files` lists `tests/fixtures/invalid/**`. The defect fixtures are temp-dir packs in `CompositionChecks`.
**Analysis**: The behavior is tested and mutation-proof, so the FR is met in substance. `--expect-invalid` (`validate_pack_schemas.py:976-982`) runs only per-pack validation, so an on-disk cross-pack fixture could not be wired there without new code. Recorded for ownership accuracy only.

### DRIFT-6: The mission landed a governance setting outside every WP's ownership (preflight off), with no re-enable tracking

**Type**: NON-GOAL INVASION (scope)
**Severity**: MEDIUM
**Spec reference**: none. The spec does not mention preflight. C-001 covers CLI incompatibility, not disabling a check.
**Evidence**: commit `c8d798d` (pre-claim, planning phase) adds `.kittify/config.yaml:39-44` `preflight: enabled: false`. Recorded in ADR `2026-11-04-1-…md:104` and in PR #121 "Blast radius". It is not in any WP's `owned_files`.
**Analysis**: The setting reaches `main` with PR #121 and stays there. Charter-freshness checking is off for this repository with no stated exit condition. It was an operator decision, documented in the ADR and the commit, so it is not a defect. **No issue tracks re-enabling it.**

---

## Risk Findings

### RISK-1: The local gate accepts a `depends_on` naming an unknown `pack_id`

**Type**: BOUNDARY-CONDITION
**Severity**: LOW
**Location**: `scripts/ci/validate_pack_schemas.py:819-830` (`_depends_on_closure`)
**Trigger condition**: a pack whose `depends_on` `pack_id` matches no pack and which writes no qualified reference (today: cave-kitty).
**Analysis**: `target = by_id.get(pack_id)` → `None` is skipped silently. Probe `depends-on-unknown-pack-id` (cave-kitty → `01ARWG13C000000000000000ZZ`) gives rc 0. The charter refuses this with `PACK_DEPENDENCY_UNKNOWN`, per WP01 review-cycle-1 non-blocking item 6 and charter `OpenPacksComposeTest.anUnknownDependencyIsRefused`. A self-loop written with a self-qualifier (cycle-1 item 7) is the same kind of local/charter disagreement. Both are outside FR-003's five classes and consistent with NFR-002, and the charter remains the authority. The cost is that the "learn here, not later" goal of US2 does not cover them. **Untracked.**

### RISK-2: As-is CLI loses this repository's org layer quietly (accepted by design)

**Type**: ERROR-PATH
**Severity**: MEDIUM (accepted, C-001)
**Location**: `packs/*/pack.yaml` `depends_on` (all four org packs) × `.kittify/config.yaml` `charter_packs`
**Trigger condition**: any checkout at or after this merge used with the as-is CLI.
**Analysis**: Per PR #121 Blast radius and ADR, `charter status`/`charter context` exit 0 with `org_layer.packs: []`; only `doctor charter-packs` exits 1. This is deliberate (C-001, tag `pre-charter-cutover`). Core's side is tracked by spec-kitty#7153 and #7193 (both OPEN).

### RISK-3: WP01's substantive approval rationale is not in a review artifact; the force/identity history needs to be read with it

**Type**: CROSS-WP-INTEGRATION (process / traceability)
**Severity**: MEDIUM
**Location**: `kitty-specs/…/tasks/WP01-gate-understands-composition/review-cycle-{1,2,3}.md`, `status.events.jsonl`
**Trigger condition**: auditing why WP01 was approved.
**Analysis**:
- Cycle 1 (21:11Z, `reviewer_agent: claude`) rejected a real defect: "held" was judged from `declared_nodes`. The fix landed in `ee93dd7` and is verified. `held_artifacts` (`:758-775`) and tests `:549-598` match the reviewer's prescribed fix.
- The cycle-2 technical review left no review-cycle file. `review-cycle-2.md` is the administrative rework ("re-record identities, authorised by the operator", force rewind `in_review→planned` at 23:40:40Z). `review-cycle-3.md` is a one-line approval.
- The only record of the cycle-2 verdict is the event note "gate agrees with charter on 48 of 51 scenarios, the remaining three accepted". The three accepted disagreements are not listed anywhere in the repository. Two are probably cycle-1 items 6 and 7 (RISK-1) [INFERENCE].
- Cycle 1 recorded implementer and reviewer as the same bare identity `claude`, so independence for that cycle rests on the operator's re-record, not on the record.
- No `ReviewerSelfApproval` event exists. force_count 2 is explained by the cycle-1 rewind and the administrative rewind.
- WP07's single forced rewind (02:19:25Z) corresponds to a real rejection whose H1/M1/M2/M3/L1/L4 items are verified fixed: ADR `:152-165` (M1); `author-a-charter-pack.md:28,46-49` (M3); test `:151-163` (L1); `validate-packs.sh:9-11` (L4); charter#378 restamped `synthesis-manifest.yaml` with the reviewer's expected hashes (H1).

### RISK-4: `validate_pack_schemas.py` was edited by six WPs against single ownership

**Type**: CROSS-WP-INTEGRATION
**Severity**: LOW
**Location**: `scripts/ci/validate_pack_schemas.py`. History `5a57a69`, `ee93dd7` (WP01), `7dee429` (WP02), `843179b` (WP04), `2b99319` (WP05), `6203de4` (WP06), `ca5df04` (WP07).
**Analysis**: Only WP01 owns it. The other WPs shrank the `PENDING_*` allowances, recorded as operator-approved out-of-map edits (WP02/WP04 status notes). The final state has no allowance left (`git grep` empty) and all gates pass. Recorded for future ownership clarity only.

---

## Silent Failure Candidates

| Location | Condition | Silent result | Spec impact |
|---|---|---|---|
| `scripts/ci/validate_pack_schemas.py:826-827` | `depends_on` entry's `pack_id` matches no pack | entry ignored, no violation | US2 local signal misses what the charter refuses (`PACK_DEPENDENCY_UNKNOWN`); RISK-1 |
| `scripts/ci/validate_pack_schemas.py:696-700` (`_load_or_none`, pre-existing) used by `held_artifacts`/`written_references`/`composition_violations` | unreadable/invalid YAML | `None` → treated as empty descriptor / no refs | none: per-pack validation reports the same file and fails the gate first |
| `scripts/docs/gen_pack_reference.py:171-172` | `pack.yaml` parses to a non-mapping | empty `PackDescriptor()`; page omits version/depends_on | none in practice: the schema gate refuses such a descriptor in the same workflow |

---

## Security Notes

The mission adds no subprocess, network, credential or auth code. The only network fetch is pre-existing (`fetch_contract`, pinned SHA `CHARTER_COMMIT`, C-003 honored). New YAML reading uses `yaml.safe_load` (`gen_pack_reference.py:170`) and the validator's existing loader.

| Finding | Location | Risk class | Recommendation |
|---|---|---|---|
| Graph documents read without a symlink check | `validate_pack_schemas.py:788-789` (`drg/fragment.yaml`, `*.graph.yaml` in `written_references`) | PATH-TRAVERSAL (informational) | None needed: `validate_pack` already fails any symlinked file in a pack (`test_a_symlinked_file_or_directory_in_a_pack_fails`, `:267`), so the gate is red before this read matters; same pattern as pre-existing `declared_nodes` |

No blocking security finding.

---

## Final Verdict

**PASS WITH NOTES**

### Verdict rationale

All hard gates pass: Gate 1/2 equivalents (four unittest suites, `validate-packs.sh`, `check-built-in.sh`, vocabulary, generator drift, all exit 0), Gate 3 (charter#378 CI green on a pin whose pack content equals HEAD), and Gate 4 (17 matrix rows, 0 unknown/empty, the one deferral has a live handle; the CLI's dead-code "fail" is a verified false positive). Every FR except FR-014 has an adequate chain from spec to WP to test to code, and no test is a false positive under mutation reasoning. The counts were reproduced independently: 93 = 3 + 12 + 78 qualified sites, 0 bare cross-pack references, and 24 bare qa agent-profile references matching #119. NFR-001 (+2.8 s) and NFR-002 (147 raw / 124 code lines, no ordering/level/range/sibling logic) pass. No locked constraint is violated: C-002 tool-minted ids, C-003 SHA pin, C-004 ordering, C-006 pin not moved, C-007 scope respected. The one HIGH item, DRIFT-1 (FR-014 / US3 post-merge re-pin), is an accepted known issue, tracked by charter#378 and epic #118, both open. Every other finding is MEDIUM or lower.

### Open items (non-blocking)

Tracked:
- FR-014 / US3: re-point charter#378 to the merged `main` SHA, collapse its intermediate pin commits (incl. stale lock `aa2f7ee`), re-run CI and preflight, mark ready. Tracked by spec-kitty-charter#378 (OPEN, draft) and #118 (OPEN). The collapse step itself is recorded only in PR #121's body.
- charter#363 lands with #378 (OPEN, body corrected).
- open-packs#119 (24 bare agent-profile refs, FR-011), OPEN; open-packs#120 (checksum recipe), OPEN.
- spec-kitty#7193 (core asset resolver vs new sidecar paths), OPEN; spec-kitty#7153 (core qualifier/descriptor grammar), OPEN.
- #92 / #94 digest regeneration ordering (C-007), recorded in PR #121.

**Without a tracking issue** (accepted or recorded only in PR #121 / review notes):
1. DRIFT-2: cave-kitty `depends_on` removal is not refused (SC-002 exception). Compensated by the charter served-edge test.
2. DRIFT-3: NFR-003 inventory covers 91 of 93 sites.
3. DRIFT-6: `.kittify/config.yaml` `preflight: enabled: false`, with no exit condition or re-enable issue.
4. The mission's pre-review regression gate reported `no_coverage` (dangling `RED_MAIN_RELEASE_DISCIPLINE` edges in the CLI's view), so it checked nothing. No issue tracks fixing that gate's coverage.
5. RISK-1: the local gate does not refuse an unknown `depends_on` `pack_id` or a self-qualified self-loop (charter does), and WP01's "three accepted" gate/charter disagreements are not enumerated (RISK-3).
6. `issue-matrix.json`: 11 rows with placeholder titles `<fill at WP-implementation time>`.
7. `read_pack_descriptor` (`gen_pack_reference.py:170`) surfaces a raw `yaml` traceback on a malformed `pack.yaml` (WP01 cycle-1 item 9). Cosmetic.
8. Tooling: `spec-kitty review` reports intra-module callers as dead code, and its re-materialization of `status.json` drops `implementer_of_record`. These are spec-kitty CLI issues, not this mission's.

Follow-ups filed after the review: items 3 and 4 → #124 (turn preflight back on once the CLI loads these packs; item 4's root cause is spec-kitty/spec-kitty#6987). Items 1 and 5 → #123 (gate refuses an unknown `depends_on` pack id and a self-qualified self-loop, and lists WP01's three accepted disagreements). Items 2 and 6 belong to this mission's closed record, and item 7 is cosmetic, so they are recorded here only. Item 8 is upstream CLI behaviour. The `status.json` rewrite that `spec-kitty review` made was reverted, and the event log stays the source of truth.

## Retrospective Reminder

The canonical post-merge sequence is: **mission review → author or verify retrospective (`retrospect create`) → surface findings (`summary` aggregates; `synthesize` reviews proposals)**.

The record exists: `kitty-specs/strict-pack-composition-01M6M0W4/retrospective.yaml` (`provenance.kind: runtime_post_completion`, `findings_status: has_findings`, commit `b2daf1b`). It is not at `.kittify/missions/01M6M0W4DHJFR6XQ6K3YMKSW0M/retrospective.yaml`, which does not exist. It does not mention the open items above (no hits for cave-kitty, `91 of 93`, `no_coverage`, preflight).

Next:
- `spec-kitty retrospect summary` — cross-mission aggregation (read-only)
- `spec-kitty agent retrospect synthesize --mission strict-pack-composition-01M6M0W4` — inspect proposals (dry-run by default)
- `spec-kitty agent retrospect synthesize --mission strict-pack-composition-01M6M0W4 --apply` — apply proposals (mutates)
