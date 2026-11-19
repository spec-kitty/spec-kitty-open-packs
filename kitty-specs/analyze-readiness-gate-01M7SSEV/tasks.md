# Tasks: Analyze readiness gate: finalize validation, WP prompts, requirement quality

**Mission**: `analyze-readiness-gate-01M7SSEV` | **Spec**: [spec.md](spec.md) | **Plan**: [plan.md](plan.md)
**Planning base / merge target**: `feat/analyze-finalize-validate-246` (PR #319)

Five work packages in one dependency chain. The chain is real for WP03 to WP05 (the analyze prompt cites the two tactics' final wording; the DRG wiring and cave-kitty cite the final prompt; the release step restamps everything). WP02 follows WP01 because the WP review tactic points at `requirement-quality-ears` for judging a WP's requirement mapping. One implementer works the chain, so the Mission stays on one lane.

## Subtask Index

| ID | Description | WP | Parallel |
|----|-------------|----|----------|
| T001 | Author `requirement-quality-ears` tactic | WP01 | |
| T002 | Cite the quality bar from the specify prompt | WP01 | |
| T003 | Trace the tactic against #247's list | WP01 | |
| T004 | Validate WP01 content (schema, ASCII, vocabulary) | WP01 | |
| T005 | Author `wp-prompt-readiness-review` tactic | WP02 | |
| T006 | Prove the template deferral (no restated key or section list) | WP02 | |
| T007 | Trace the tactic against #237's list | WP02 | |
| T008 | Validate WP02 content | WP02 | |
| T009 | Step 2a: CLI version gate and HIGH could-not-run | WP03 | |
| T010 | Fixed report layout and finding-id prefixes | WP03 | |
| T011 | Step 2b: per-WP readiness pass and section | WP03 | |
| T012 | Pass G: requirement quality, EARS, scenario audit, clarification questions, inferred labels | WP03 | |
| T013 | Severity heuristic, metrics, next actions | WP03 | |
| T014 | Line budget and ASCII check | WP03 | |
| T015 | Tactic graph nodes and edges | WP04 | |
| T016 | Action graph scope edges | WP04 | |
| T017 | cave-kitty analyze prompt parity | WP04 | |
| T018 | cave-kitty DRG fragment edges | WP04 | |
| T019 | Cross-pack validation of the wiring | WP04 | |
| T020 | CI test pinning the prompt invariants | WP05 | |
| T021 | Lockstep version bumps (DIRECTIVE_018) | WP05 | |
| T022 | Manifests, digests, pack pages | WP05 | |
| T023 | Changelog entry | WP05 | |
| T024 | Full gate run and PR body update | WP05 | |

## Phase 1 - Doctrine

### WP01 - Requirement-quality tactic and the specify quality bar

**Prompt**: [tasks/WP01-requirement-quality-tactic.md](tasks/WP01-requirement-quality-tactic.md)
**Goal**: one canonical checklist for requirement quality, EARS, observable behaviour, scenario-audit kinds, clarification questions and inferred labelling (#247), cited by the specify prompt.
**Priority**: P2 | **Depends on**: none
**Independent test**: the tactic validates against the pinned tactic schema; the specify prompt names the tactic and the five properties; ASCII guard green.

T001 Author `requirement-quality-ears` tactic (WP01)
T002 Cite the quality bar from the specify prompt (WP01)
T003 Trace the tactic against #247's list (WP01)
T004 Validate WP01 content (schema, ASCII, vocabulary) (WP01)

**Risks**: the vocabulary guard; specify is software-dev content (ASCII only).

### WP02 - WP prompt readiness tactic

**Prompt**: [tasks/WP02-wp-prompt-readiness-tactic.md](tasks/WP02-wp-prompt-readiness-tactic.md)
**Goal**: one canonical checklist for reviewing every WP prompt before implementation (#237), deferring to the WP prompt template as resolved.
**Priority**: P2 | **Depends on**: WP01
**Independent test**: the tactic validates; it names no WP frontmatter key or body section of the template.

T005 Author `wp-prompt-readiness-review` tactic (WP02)
T006 Prove the template deferral (no restated key or section list) (WP02)
T007 Trace the tactic against #237's list (WP02)
T008 Validate WP02 content (WP02)

**Risks**: accidentally restating the template (C-002).

## Phase 2 - Step prompt

### WP03 - Analyze prompt: validation gate, per-WP readiness, requirement quality

**Prompt**: [tasks/WP03-analyze-prompt-integration.md](tasks/WP03-analyze-prompt-integration.md)
**Goal**: complete #246 in the analyze prompt (version gate, HIGH could-not-run) and add the #237 and #247 passes and report sections, citing the two tactics, in a fixed deterministic layout.
**Priority**: P1 | **Depends on**: WP02
**Independent test**: the prompt is at most 500 lines, ASCII, names `--validate-only` as the only finalize form, the 3.1.0a5 gate, both tactics, and the fixed section order and id prefixes.

T009 Step 2a: CLI version gate and HIGH could-not-run (WP03)
T010 Fixed report layout and finding-id prefixes (WP03)
T011 Step 2b: per-WP readiness pass and section (WP03)
T012 Pass G: requirement quality, EARS, scenario audit, clarification questions, inferred labels (WP03)
T013 Severity heuristic, metrics, next actions (WP03)
T014 Line budget and ASCII check (WP03)

**Risks**: the 500-line cap; the drafted step 2a still says MEDIUM for could-not-run.

## Phase 3 - Wiring and parity

### WP04 - DRG wiring and cave-kitty parity

**Prompt**: [tasks/WP04-drg-wiring-and-cave-kitty.md](tasks/WP04-drg-wiring-and-cave-kitty.md)
**Goal**: register the two tactics in foundation's graph, scope them to the specify and analyze actions, and give cave-kitty's analyze step the same checks in its voice.
**Priority**: P2 | **Depends on**: WP03
**Independent test**: cross-pack validation reports 0 violations; the cave-kitty prompt names the same checks, tactics and severities.

T015 Tactic graph nodes and edges (WP04)
T016 Action graph scope edges (WP04)
T017 cave-kitty analyze prompt parity (WP04)
T018 cave-kitty DRG fragment edges (WP04)
T019 Cross-pack validation of the wiring (WP04)

**Risks**: a qualified cross-pack reference outside cave-kitty's `depends_on` closure.

## Phase 4 - Release

### WP05 - Prompt invariant test, versions, derived outputs, changelog

**Prompt**: [tasks/WP05-test-and-release.md](tasks/WP05-test-and-release.md)
**Goal**: pin the prompt invariants with one CI test and ship the change: lockstep minor bumps, manifests, digests, pack pages, changelog.
**Priority**: P1 | **Depends on**: WP04
**Independent test**: every gate green: `validate-packs.sh`, `tests/ci`, digests, pages, vocabulary; CI on the PR head.

T020 CI test pinning the prompt invariants (WP05)
T021 Lockstep version bumps (DIRECTIVE_018) (WP05)
T022 Manifests, digests, pack pages (WP05)
T023 Changelog entry (WP05)
T024 Full gate run and PR body update (WP05)

**Risks**: concurrent PRs collide on the changelog and digests; restamp on every rebase.

## MVP

WP03 carries the P1 behaviour (#246). WP01 and WP02 come first only because WP03 cites them.
