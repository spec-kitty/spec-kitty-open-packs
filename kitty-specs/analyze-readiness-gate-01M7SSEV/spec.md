# Mission Specification: Analyze readiness gate: finalize validation, WP prompts, requirement quality

**Mission Branch**: `kitty/mission-analyze-readiness-gate-01M7SSEV` (merges into `feat/analyze-finalize-validate-246`, PR #319)
**Created**: 2026-11-19
**Status**: Draft
**Input**: Issues #246 ("integrate finalize-tasks validation into /spec-kitty.analyze readiness checks", P1), #237 ("have /spec-kitty.analyze inspect every WP prompt before implementation") and #247 ("analyze/specify prompts: requirement-quality, EARS and scenario-audit report sections"), parent epic #244, dispatched by the orchestrator with operator-approved scope.

## Intent Summary (confirmed by the orchestrator, 2026-11-19)

- **Primary actor**: an agent running the `analyze` step of a software-dev (or cave-dev) Mission, after `tasks` and before `implement`. Secondary actor: the human operator who reads the recorded analysis report and decides whether implementation starts.
- **Trigger**: the analyze step prompt today reads only `spec.md`, `plan.md` and `tasks.md`. It can return `ready` while the task metadata that `finalize-tasks` checks is broken, while WP prompt files are missing, orphaned or underspecified, or while requirements are untestable or ambiguous.
- **Outcome**: the analysis report reflects (1) the result of the read-only `finalize-tasks --validate-only` check, (2) a per-WP readiness review of every `tasks/WP*.md` file, and (3) requirement-quality, EARS and scenario-audit sections; the specify step prompt holds requirements to the same quality bar when they are written.
- **Invariant**: analyze stays read-only and non-remediating. It never invokes a writing `finalize-tasks` path, never edits a planning artifact, and its only write remains `record-analysis`.
- **Operator rulings**: proceed before #266 (no file overlap); fold #237 in, checking WP files against the WP prompt template as resolved, without restating its key list (#230 reconciles that template); fold both halves of #247; give cave-kitty's analyze copy the same checks; run as a full Mission with independent review per WP; a validation that cannot run is HIGH (fail closed).

## Domain Language

| Term | Meaning | Avoid |
|------|---------|-------|
| finalize validation | The read-only run `spec-kitty agent mission finalize-tasks --validate-only --mission <slug> --json`. It previews finalization and writes nothing. | "dry finalize", "finalize check" (ambiguous with a writing run) |
| refusal | A finalize validation that exits non-zero with an `error` payload: finalization would refuse these artifacts. | "failure" when the check could not run at all |
| could not run | The finalize validation did not produce a usable verdict: command missing, CLI older than 3.1.0a5, no JSON, or a mission/repository resolution error. | |
| WP prompt | One `tasks/WP##-*.md` file that an implementation agent executes. | "task file" |
| WP prompt template | `task-prompt-template.md` as the command's template resolver returns it for the Mission. | a hand-copied key list |
| readiness blocker | A finding that must be fixed before `implement` (severity `high` or `critical`). | |
| quality improvement | A finding that should be fixed but does not block `implement` (severity `low` or `medium`). | |
| inferred finding | A finding the agent reached by judgement rather than by a machine check; labelled as such in the report. | "proven", "verified" |

## User Scenarios & Testing *(mandatory)*

### User Story 1 - The report catches broken task metadata (Priority: P1)

An agent runs analyze on a Mission whose WP frontmatter leaves a functional requirement unmapped, or whose WPs form a dependency cycle. Today the report can say `ready`.

**Why this priority**: #246 is P1; machine-checkable breakage must never pass the readiness gate.

**Independent Test**: on a Mission with an unmapped FR, following the analyze prompt yields a CRITICAL `finalize-validation` finding naming the FR, and the verdict is `blocked`.

**Acceptance Scenarios**:

1. **Given** WP prompts that map no WP to FR-002, **When** analyze runs, **Then** the report carries a CRITICAL finding that names FR-002 and quotes the validation `error`.
2. **Given** two WPs that depend on each other, **When** analyze runs, **Then** the report carries a CRITICAL finding naming the cycle.
3. **Given** two WPs that can run in parallel and claim the same file, **When** analyze runs, **Then** the report carries a CRITICAL ownership-overlap finding.
4. **Given** any refusal, **When** the report is written, **Then** it says that later validation gates did not run.

### User Story 2 - The report says when the check could not run (Priority: P1)

An agent runs analyze on a host whose spec-kitty CLI is older than 3.1.0a5, or where the command is unavailable.

**Independent Test**: following the prompt on such a host yields a HIGH finding naming `spec-kitty CLI >= 3.1.0a5` and the installed version, a residual-risk entry, and a `blocked` verdict; the check is not run on a CLI below 3.1.0a5.

**Acceptance Scenarios**:

1. **Given** CLI 3.0.x, **When** analyze runs, **Then** it does not invoke the check and records a HIGH finding naming the required version.
2. **Given** an unknown Mission handle, **When** the check returns `MISSION_CONTEXT_UNRESOLVED`, **Then** the report records a HIGH "could not run" finding, not a validation refusal.

### User Story 3 - The report reviews every WP prompt (Priority: P2)

An agent runs analyze on a Mission where `tasks.md` names WP03 but no `WP03-*.md` exists, WP04's file is not referenced from `tasks.md`, and WP02's prompt is 900 lines with 14 subtasks.

**Independent Test**: the report's per-WP readiness section has one row per WP prompt and per `tasks.md` WP, flags WP03 as missing (blocker), WP04 as orphaned (blocker) and WP02 as oversized (quality improvement).

**Acceptance Scenarios**:

1. **Given** a WP prompt whose first body section does not load its agent profile, **When** analyze runs, **Then** that WP gets a finding.
2. **Given** a WP prompt missing a section the WP prompt template defines, **When** analyze runs, **Then** that WP gets a finding that names the section and cites the template, not a list in the analyze prompt.
3. **Given** a WP that maps to no requirement or user value, **When** analyze runs, **Then** that WP gets a finding.

### User Story 4 - The report judges requirement quality (Priority: P2)

An agent runs analyze on a spec whose FR-003 says "the system should be fast" and whose user story 2 has no rejected scenario.

**Independent Test**: the report carries a requirement-quality finding on FR-003 (not testable, not measurable), an EARS observation, a scenario-audit table for story 2 with a "missing edge" row, and a clarification question with concrete answer choices for the HIGH ambiguity.

**Acceptance Scenarios**:

1. **Given** a HIGH or CRITICAL ambiguity finding, **When** the report is written, **Then** it carries a clarification question with concrete choices or a remediation proposal.
2. **Given** a scenario finding, **When** the report is written, **Then** it cites a `spec.md`, `plan.md` or `tasks.md` location.
3. **Given** a finding reached by judgement, **When** the report is written, **Then** it is labelled inferred and claims no formal proof.

### User Story 5 - Specify writes requirements to the same bar (Priority: P3)

An agent runs specify. The specify prompt tells it the requirement-quality bar (testable, solution-free, unambiguous, consistent, complete) and the EARS patterns analyze will check.

**Independent Test**: the specify prompt names the five quality properties and the EARS patterns, and the analyze prompt checks the same five properties.

### User Story 6 - cave-dev gets the same gate (Priority: P3)

An agent runs analyze on a cave-dev Mission. The cave-kitty analyze prompt names the finalize validation, the per-WP review and the requirement-quality sections, in caveman voice, while keeping its "inherits the software-dev contract" framing.

**Independent Test**: the cave-kitty analyze prompt names `finalize-tasks --validate-only`, the per-WP readiness section and the requirement-quality sections, and keeps payload (ids, severities, commands) exact.

### Edge Cases

- `finalize-tasks` has not run yet: a passing validation reports a non-empty `would_modify`; that is a HIGH stale-finalization finding, not a refusal.
- Only `wps.yaml` exists (`validation_stage: tasks-outline`): no WP prompts were generated; CRITICAL.
- WPs ordered by a dependency share a file: the validation passes; analyze must not report an ownership overlap for them.
- The requirement-mapping refusal lists all four mapping keys, empty ones included: only non-empty keys are findings.
- An older CLI emits refusal keys this prompt does not name: report the `error` verbatim.
- A Mission with no user stories: the scenario audit says so instead of inventing stories.
- More than 50 findings: the existing overflow rule applies across all sections.

## Requirements *(mandatory)*

### Functional Requirements

| ID | Title | User Story | Priority | Status | Delivery | No-op passable? |
|----|-------|------------|----------|--------|----------|-----------------|
| FR-001 | Run finalize validation | As an operator, I want analyze to run `finalize-tasks --validate-only --mission <slug> --json` after loading the artifacts and before any detection pass or verdict, so that machine-checkable breakage reaches the report. | High | Open | [build] | no - the step and command are absent from today's analyze prompt (main) |
| FR-002 | Refusals are CRITICAL and named | As an operator, I want each refusal reported as a CRITICAL finding that quotes `error` and names the failure class from its non-empty payload keys (missing/unknown requirement refs, unmapped FRs, bare-prose ids, tasks.md/WP pairing, cycles, invalid or disagreeing dependencies, ownership overlap, ownership contradiction, literal-path errors, stale canceled dependencies, risk policy, any other error verbatim), and I want the report to say later gates did not run. | High | Open | [build] | no - each named key is asserted present in the prompt |
| FR-003 | Passing-run signals | As an operator, I want a passing validation's `tasks_md_stale` or non-empty `would_modify` reported HIGH, its warnings MEDIUM and a collapsed lane LOW, so that stale finalization blocks and soft signals do not. | High | Open | [build] | no - the severities are absent today |
| FR-004 | Could-not-run is HIGH | As an operator, I want analyze to check the CLI version first, not run the check below 3.1.0a5, and record a HIGH finding (naming `spec-kitty CLI >= 3.1.0a5` and the installed version) plus a residual-risk entry whenever the check could not run (old CLI, command missing, no JSON, mission/repository resolution error). | High | Open | [build] | no - the version gate is absent today |
| FR-005 | Read-only only | As an operator, I want analyze forbidden from running `finalize-tasks` without `--validate-only`, with `--refresh-planning-commit` or with `--allow-orphaned`, so that analyze never writes or commits finalization. | High | Open | [build] | no - the prohibition is absent today |
| FR-006 | WP pairing | As an operator, I want every WP named in `tasks.md` matched to a WP prompt file and every WP prompt file matched to `tasks.md`, missing and orphaned ones reported as blockers. | High | Open | [build] | no - analyze reads no WP files today |
| FR-007 | Template conformance | As an operator, I want each WP prompt's frontmatter and body sections checked against the WP prompt template as resolved for the Mission, without the analyze prompt restating the template's key or section list. | High | Open | [build] | no - analyze reads no WP files today |
| FR-008 | Profile load and size | As an operator, I want analyze to check that a WP prompt's first body section loads its agent profile, and to apply the size guidance (target 200-500 lines; warn above 700 lines or 10 subtasks). | Medium | Open | [build] | no - the thresholds are absent today |
| FR-009 | WP scoping | As an operator, I want analyze to judge dependency order, cohesive and independently implementable WP boundaries, and each WP's mapping to requirements and user value. | Medium | Open | [build] | no - absent today |
| FR-010 | Per-WP readiness section | As an operator, I want a per-WP readiness section in the report, one row per WP, separating blockers from quality improvements. | High | Open | [build] | no - the section is absent today |
| FR-011 | Requirement quality | As an operator, I want each requirement checked for being testable, solution-free, unambiguous, consistent and complete. | Medium | Open | [build] | no - the five properties are absent today |
| FR-012 | EARS and observable behaviour | As an operator, I want requirements checked against the EARS patterns and for observable behaviour. | Medium | Open | [build] | no - EARS is absent today |
| FR-013 | Scenario audit | As an operator, I want a scenario-audit table per user story with rows accepted, rejected, missing edge, surprising accepted and surprising rejected, each citing a `spec.md`, `plan.md` or `tasks.md` location. | Medium | Open | [build] | no - absent today |
| FR-014 | Clarification questions | As an operator, I want every HIGH or CRITICAL ambiguity finding to carry a clarification question with concrete answer choices, or a concrete remediation proposal. | Medium | Open | [build] | no - absent today |
| FR-015 | Inferred labelling | As an operator, I want findings reached by judgement labelled inferred, and the report to claim no formal proof. | Medium | Open | [build] | no - absent today |
| FR-016 | Specify quality bar | As a spec author, I want the specify prompt to state the same five quality properties and the EARS patterns analyze checks. | Medium | Open | [build] | no - absent from today's specify prompt |
| FR-017 | cave-kitty parity | As a cave-dev operator, I want cave-kitty's analyze prompt to name the finalize validation, the per-WP review and the requirement-quality sections in caveman voice, keeping its "inherits software-dev" framing and exact payloads. | Medium | Open | [build] | no - absent from today's cave-kitty prompt |

### Non-Functional Requirements

| ID | Title | Requirement | Category | Priority | Status |
|----|-------|-------------|----------|----------|--------|
| NFR-001 | ASCII | Software-dev mission content has 0 non-ASCII characters (`tests/ci/test_software_dev_ascii.py`). | Compatibility | High | Open |
| NFR-002 | Deterministic report | The report's sections appear in one fixed order with fixed headings; finding ids use stable category prefixes; a rerun on unchanged artifacts yields the same ids (0 renumbered). | Reliability | High | Open |
| NFR-003 | One carrier | 100% of findings, new sections included, go through the `analysis-findings/v1` carrier with severities from its closed set (`low`, `medium`, `high`, `critical`). | Reliability | High | Open |
| NFR-004 | Prompt size | `analyze.prompt.md` (software-dev) is at most 500 lines. | Maintainability | Medium | Open |

### Constraints

| ID | Title | Constraint | Category | Priority | Status |
|----|-------|------------|----------|----------|--------|
| C-001 | Read-only | Analyze stays non-remediating: its only write is `record-analysis`. | Technical | High | Open |
| C-002 | Defer to the template | No WP frontmatter key list or section list is restated in the analyze prompt; #230 owns reconciling the template. | Technical | High | Open |
| C-003 | Gates green | `validate-packs.sh`, the charter service job, `check_vocabulary.py`, `gen_pack_reference.py --check`, the digest gate and the ASCII test report 0 errors. | Technical | High | Open |
| C-004 | Core half out of scope | Solver-backed analysis and core's report fixture tests (core #1131) are not part of this mission. | Business | High | Open |
| C-005 | Siblings out of scope | #213 (planning corpus and user intent) and #214 (product-coherence checks) are not part of this mission. | Business | Medium | Open |
| C-006 | Versioning | Pack versions follow DIRECTIVE_018 (additive change: minor bump; exact pins move in lockstep), and the changelog's `[Unreleased]` names the change. | Business | High | Open |

### Key Entities

- **Finalize validation result**: exit code; on success `result`, `validation_stage`, `tasks_md_stale`, `would_modify[]` (`wp_id`, `changes`), warning lists, `validation.lanes_preview`; on refusal `error`, optional `error_code` and class-specific keys.
- **Finding**: id, severity, category, summary, location, recommendation, optional inferred label, optional clarification question.
- **WP readiness row**: WP id, prompt file, `tasks.md` reference, blockers, quality improvements.
- **Scenario audit row**: user story, kind (accepted / rejected / missing edge / surprising accepted / surprising rejected), scenario, location.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: On a Mission with an unmapped requirement, a dependency cycle or a parallel ownership overlap, an agent following the analyze prompt records a `blocked` verdict in 3 of 3 cases. - [build] · no-op passable: no
- **SC-002**: On a host where the validation cannot run, an agent following the analyze prompt records a `blocked` verdict that names the required CLI version, in 100% of runs. - [build] · no-op passable: no
- **SC-003**: The per-WP readiness section lists 100% of WPs named in `tasks.md` or present as prompt files. - [build] · no-op passable: no
- **SC-004**: An operator reading the report can tell, for every finding, whether it blocks implementation and whether it was machine-checked or inferred. - [build] · no-op passable: no
- **SC-005**: A reviewer finds the same validation, WP-review and requirement-quality checks named in both the software-dev and the cave-kitty analyze prompts. - [build] · no-op passable: no

## Decisions (recorded Decision Moments, resolved)

1. **Requirement set** (`01M7SSFJVQ5KSDH5SADRB69M1H`): confirmed by the operator as sent, with the FR-004 version gate.
2. **Could-not-run severity** (`01M7SSFNB9DQCMCD4PVEBP92R7`): HIGH, fail closed; the finding names the CLI version that provides the check.

## Assumptions

- The finalize validation's behaviour and payload keys are those of spec-kitty CLI 4.0.0rc9 (source and a scratch-Mission run, 2026-11-19); `--validate-only` exists from 3.0.0 and is non-writing from 3.1.0a5 (core CHANGELOG).
- The WP prompt template is resolved by the command's template resolver; the analyze prompt names the template, not its path layout.
- #237's "role/agent/model fields where applicable, and history" and its section list are covered by deferring to the template (C-002).
