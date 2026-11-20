# Mission Specification: Analyze: full planning corpus and product coherence

**Mission Branch**: `kitty/mission-analyze-planning-corpus-01M7WZZM` (lands on `t3/analyze-planning-corpus-coherence`)
**Created**: 2026-11-20
**Status**: Draft
**Input**: Issues #213 ("Expand /spec-kitty.analyze to review full planning corpus and user intent") and #214 ("Add product-coherence checks to /spec-kitty.analyze"), parent epic spec-kitty/spec-kitty#849, plus the follow-up folds a two-lens review squad found on #247 (requirement-quality, EARS and scenario-audit report sections). Dispatched by the orchestrator with operator-approved scope and rulings (2026-11-20).

## Intent Summary (confirmed by the dispatch brief and the issues)

- **Primary actor**: an agent running the software-dev `analyze` step (`/spec-kitty.analyze`) after `/spec-kitty.tasks`, and the operator who reads its persisted `analysis-report.md` before letting implementation start. Secondary actor: an agent running the cave-dev `analyze` step, which inherits the software-dev contract.
- **Trigger**: today the analyze prompt reads only `spec.md`, `plan.md`, `tasks.md`, the WP prompts and the charter (`analyze.prompt.md:16, 38-44`). It never reads the planning artifacts that `check-prerequisites` already inventories (`research.md`, `data-model.md`, `contracts/`, `quickstart.md`, checklists), nor a bulk-edit Mission's `occurrence_map.yaml`, nor the intent recorded at creation in `meta.json` (`purpose_tldr`, `purpose_context`, `source_description`). It never asks whether an internally consistent plan is still the right plan for the user's goal.
- **Outcome**: the analyze step loads the full planning corpus through the inventory the CLI already provides, reports contradictions between planning artifacts and tasks/WPs under the normal severity rules, and adds an advisory product-coherence review that ends in one mandatory recommendation: revise spec, revise plan, revise tasks, or proceed.
- **Invariants**: the step stays read-only and non-remediating; product-coherence findings never exceed MEDIUM and never block the readiness verdict (operator ruling); the report keeps a fixed section order and deterministic finding ids; the cave-dev copy names the same checks.

Three scoping calls were recorded as Decision Moments and resolved from the operator's rulings (see Decisions); no question is left open.

## Domain Language

| Term | Meaning | Avoid |
|------|---------|-------|
| planning corpus | Every planning input of a Mission: `meta.json` intent fields, `spec.md`, `plan.md`, `tasks.md`, the WP prompts, every further artifact the `check-prerequisites` inventory names (`research.md`, `data-model.md`, `contracts/`, `quickstart.md`, checklists, …), and `<mission_dir>/occurrence_map.yaml` when present. | "all the docs" |
| planning artifact | A planning-corpus member other than spec, plan, tasks, WP prompts and `meta.json`. | "supporting doc" |
| creation intent | `purpose_tldr`, `purpose_context` and (when present) `source_description` in `meta.json`: what the Mission was created to do. | "original prompt" |
| ungrounded behaviour | A task or WP that builds something no spec requirement, plan decision, planning artifact or creation intent asks for. A traceability defect (#213). | "scope creep" (ambiguous) |
| product coherence | Whether the plan as a whole still serves the creation intent: smallest valuable slice, vertical slice vs scaffolding, overbuild, lost journeys or failure cases, sequencing risk, grouping by user value (#214). A judgement, always labelled `Inferred:`. | "intent fidelity" as a second name |
| coherence recommendation | The single mandatory line `Recommendation: revise spec | revise plan | revise tasks | proceed` that closes the Product Coherence section. | |

## User Scenarios & Testing *(mandatory)*

### User Story 1 - A planning artifact contradicts the tasks (Priority: P1)

The plan phase wrote `research.md` choosing an event log over polling, and `contracts/orders.yaml` with a `cancel` operation. `tasks.md` and the WPs implement polling and never mention cancel. Today analyze reads neither file and reports the mission ready.

**Why this priority**: an implementation agent faithfully executes the wrong thing (#213's core ask).

**Independent Test**: the analyze prompt names the inventory keys it reads, a planning-artifact consistency pass, and a report section where these contradictions land with a stable prefix.

**Acceptance Scenarios**:

1. **Given** a `research.md` decision that no task implements, defers or flags, **When** analyze runs, **Then** the report raises a planning-artifact finding citing the decision and the tasks/WPs it should appear in.
2. **Given** a contract operation, data-model entity or invariant, or quickstart scenario that no task or WP covers, **When** analyze runs, **Then** the report raises a planning-artifact finding naming the artifact location.
3. **Given** a WP that builds behaviour grounded in no spec requirement, plan decision, planning artifact or creation intent, **When** analyze runs, **Then** the report raises a planning-artifact finding (ungrounded behaviour).
4. **Given** a bulk-edit Mission with an `occurrence_map.yaml`, **When** analyze runs, **Then** the map's categories are checked against the tasks/WPs.

### User Story 2 - The plan is consistent but not what the user needed (Priority: P1)

Every requirement maps to a WP and every WP traces back, yet WP01-WP04 are scaffolding, the first user-visible result lands in WP06, and two WPs build an admin dashboard the creation intent never mentioned.

**Why this priority**: #214's product-owner question, "is this the right plan for the user's goal?", is unanswered today.

**Independent Test**: the prompt names a product-coherence pass with the seven review lenses, a Product Coherence report section, an advisory severity cap and the mandatory recommendation line.

**Acceptance Scenarios**:

1. **Given** a task breakdown whose first WPs deliver no user-visible slice, **When** analyze runs, **Then** the Product Coherence section carries an `Inferred:` finding (weak vertical slice) at MEDIUM or LOW.
2. **Given** any Mission, **When** analyze runs, **Then** the Product Coherence section ends with exactly one `Recommendation:` line choosing revise spec, revise plan, revise tasks or proceed.
3. **Given** only product-coherence findings, **When** the report is recorded, **Then** the verdict is `ready` (they never block).

### User Story 3 - Analyze stays cheap and read-only on a large corpus (Priority: P2)

A Mission has a 1,200-line `data-model.md` and twelve contract files. The analyze agent must not load every file whole, and must never edit one.

**Independent Test**: the prompt instructs headings-first progressive loading for planning artifacts, keeps the 500-line prompt cap, and its read-only guards still pass.

### User Story 4 - The #247 report sections are deterministic (Priority: P2)

Two reruns of analyze on unchanged artifacts must produce the same finding count. Today an agent may turn accepted and rejected scenario-audit rows into `S` findings, and `Inferred:` placement is unstated.

**Independent Test**: the prompt states which scenario kinds become `S` findings, the audit table carries a finding column, the five kinds have a fixed row order, and `Inferred:` placement is stated; tests pin the #247 report content.

### User Story 5 - The cave-dev analyze step names the same checks (Priority: P3)

An agent running cave-dev's analyze reads its short "inherited checks" list and must not skip the new passes.

**Independent Test**: the cave-kitty analyze prompt names the planning-corpus pass and the advisory product-coherence pass with their tactics.

### Edge Cases

- A Mission with no planning artifacts beyond spec/plan/tasks: the Intent & Planning-Artifact Consistency section still appears and says which inventory was read and that it held nothing more (or "None.").
- `meta.json` missing, or missing `source_description`: the coherence pass compares against the fields that exist and says which were absent; it never invents intent.
- `occurrence_map.yaml` absent on a non-bulk-edit Mission: no finding.
- A non-software-dev Mission (cave-dev) whose inventory holds fewer artifact kinds: the report states which inventory entries were read.
- A defect already reported by a `V` finding, a `C` coverage finding or another pass: cited, not raised twice (one defect, one finding).
- An ungrounded WP that is also overbuild: raised once as a planning-artifact finding at its normal severity; the coherence section cites that id instead of a second finding. Ungrounded means no trace at all; behaviour that traces to a source but exceeds what the intent needs is overbuild (product coherence).
- A WP mapped to no requirement: already a `V` / `W` / `C` defect; pass H cites it and does not re-raise it.
- `tasks.md` has no `MVP Scope` note: one product-coherence finding (MVP unclear).
- The `check-prerequisites` inventory includes the mission directory itself (`feature_dir`): it is not a planning artifact and is skipped.
- A very large artifact: headings first, body sections only when a check needs them.
- An inventory artifact no named check covers: read headings-first and cross-checked against tasks/WPs for unreflected content; never skipped silently.

## Requirements *(mandatory)*

### Functional Requirements

| ID | Title | User Story | Priority | Status | Delivery | No-op passable? |
|----|-------|------------|----------|--------|----------|-----------------|
| FR-001 | Full corpus inputs named | As an analyze agent, I want the prompt to name every supported planning input (spec, plan, tasks, WP prompts, charter, `meta.json` creation intent, every `artifact_files` / `artifact_dirs` entry whose path the step has not already loaded, except `feature_dir`, and `<mission_dir>/occurrence_map.yaml` when present), so that no planning artifact is skipped and none is loaded twice. | High | Open | [build] | no — the test asserts `artifact_files`, `artifact_dirs` and `meta.json` are named; today's prompt names none |
| FR-002 | Creation intent loaded | As an analyze agent, I want to read `<mission_dir>/meta.json` for `purpose_tldr`, `purpose_context` and `source_description`, stating which were absent, so that intent comparisons start from what was recorded. | High | Open | [build] | no — asserted by name in the prompt and tactic |
| FR-003 | Planning-artifact consistency pass | As an operator, I want a detection pass that checks research and plan decisions and every deferred-decision marker (each implemented, explicitly deferred, or flagged), data-model entities/invariants/state transitions, contract operations, quickstart scenarios and (when present) `occurrence_map.yaml` against spec, tasks and WPs, so that contradictions and omissions are reported. | High | Open | [build] | no — a new pass and tactic absent on main |
| FR-004 | Ungrounded behaviour | As an operator, I want tasks/WPs that build behaviour grounded in no requirement, plan decision, planning artifact or creation intent flagged, so that agents do not build unasked work. | High | Open | [build] | no — named in the prompt and tactic |
| FR-005 | Planning-artifact severity | As an operator, I want planning-artifact findings to use the normal severity rules (a contradiction that changes what gets built is HIGH), so that real contradictions block. | High | Open | [build] | no — severity lines asserted |
| FR-006 | Product-coherence pass | As an operator, I want an advisory pass covering intent drift, MVP slice clarity, vertical slice vs scaffolding, overbuild, lost journeys/actors/triggers/outcomes/failure cases, sequencing risk and grouping by user value, reading the MVP slice from the `MVP Scope` note in `tasks.md` rather than redefining MVP; a missing note is an "MVP unclear" finding. | High | Open | [build] | no — a new pass and tactic absent on main |
| FR-007 | Advisory cap | As the operator, I want product-coherence findings capped at MEDIUM and never counted towards a blocked verdict, so that judgement calls inform but do not gate (operator ruling 2026-11-20). | High | Open | [build] | no — the cap wording is asserted; a positive control asserts planning-artifact findings may be HIGH |
| FR-008 | Coherence recommendation | As the operator, I want one mandatory line `Recommendation: revise spec | revise plan | revise tasks | proceed` in the Product Coherence section and echoed in Next Actions, so that the report says what to do next. The recommendation weighs all findings: it is never `proceed` while the verdict is `blocked`, and it may be a `revise` choice while the verdict is `ready`. | High | Open | [build] | no — the literal line shape is asserted |
| FR-009 | Report sections | As a reader, I want two new always-present sections, "Intent & Planning-Artifact Consistency" and "Product Coherence", placed immediately after Scenario Audit and before Clarification Questions in the fixed order. | High | Open | [build] | no — section order asserted |
| FR-010 | Finding prefixes | As a fixture author, I want two new prefixes, `X` (category `planning-artifact`, which includes ungrounded behaviour) and `M` (category `product-coherence`), distinct from the ten in use, in the prefix table, with the new passes ordered after A-G as H and J (I is skipped: it is already a prefix) in the id-ordering rule, and the one-defect rule stated as "the earliest step that detects a defect owns it (2a, 2b, A-G, H, J); later steps cite its id". | High | Open | [build] | no — prefix rows asserted and checked for uniqueness |
| FR-011 | Metrics | As a reader, I want metrics lines for planning artifacts reviewed, planning-artifact findings, product-coherence findings and the coherence recommendation. | Medium | Open | [build] | no — metric labels asserted |
| FR-012 | Inferred labelling | As a reader, I want every product-coherence finding to start with `Inferred:`, and the prompt to state where the label goes (carrier `summary` and table Summary cell) and that `V` findings never carry it. The same placement rule applies to every judgement finding from step 2b and passes A-J. | High | Open | [build] | no — asserted in prompt and tactic |
| FR-013 | Scenario rows to findings (#247) | As a fixture author, I want only missing-edge, surprising-accepted and surprising-rejected scenario-audit rows to become `S` findings, the audit table to carry a Finding column (`—` for accepted and rejected rows, the `S` id otherwise), and the five kinds in the tactic's fixed row order. | Medium | Open | [build] | no — today's prompt leaves it open |
| FR-014 | Tactics carry the detail | As a maintainer, I want the check detail in two new tactics under `packs/foundation/tactics/analysis/` (planning-corpus consistency, product-coherence review), cited from the prompt with their fetch command and wired into the pack graphs, following the `requirement-quality-ears` pattern. | High | Open | [build] | no — tactic files and citations asserted |
| FR-015 | cave-dev parity (repo invariant, not issue AC) | As a cave-dev agent, I want the cave-kitty analyze prompt to name both new passes, the advisory cap and the recommendation line, citing the foundation tactics. | Medium | Open | [build] | no — asserted for the cave-kitty prompt |
| FR-016 | Tests | As CI, I want `tests/ci/test_analyze_readiness_prompts.py` extended to pin the prefixes, section order, tactic citations, the named inventory keys and `meta.json`, the advisory cap and recommendation line, the #247 report content (section headings and order, five scenario kinds, two-to-four choices, the question-or-remediation rule, `Inferred:` in the software-dev and cave-dev analyze prompts, the five quality properties in `requirement-quality-ears`), the read-only guards and the line budget. | High | Open | [build] | no — the red-first assertions (corpus inputs, passes, prefixes, sections, cap, recommendation) fail on main; the #247 anti-deletion pins are ratchets that pass on main by design |
| FR-018 | #247 wording nits | As a fixture author, I want the duplicated "untestable" severity rule folded into one line, the `file:Lnn` location form preferred (a heading only when no stable line exists), and the example row's category written as the lowercase category id. | Low | Open | [build] | no — today's prompt carries both rules and the capitalised example |
| FR-017 | Changelog | As a reader, I want an `[Unreleased]` entry naming #213, #214 and #247. | Medium | Open | [build] | no — entry names the issues |

### Non-Functional Requirements

| ID | Title | Requirement | Category | Priority | Status |
|----|-------|-------------|----------|----------|--------|
| NFR-001 | Prompt budget | The software-dev analyze prompt stays at or under 500 lines (the CI cap), and the cave-dev analyze prompt grows by at most 15 lines. | Maintainability | High | Open |
| NFR-002 | Token bound | Planning artifacts are loaded headings-first; a body section is read only when a named check needs it. The prompt states this for every planning artifact. | Performance | High | Open |
| NFR-003 | Gates green | `validate-packs.sh`, `pytest tests`, the vocabulary guard, the pack-reference check, the digest gate and the docs-freshness check report 0 errors. | Reliability | High | Open |
| NFR-004 | Determinism | Rerunning on unchanged artifacts yields the same finding ids and counts: the id-ordering rule covers the new steps and prefixes. | Reliability | High | Open |

### Constraints

| ID | Title | Constraint | Category | Priority | Status |
|----|-------|------------|----------|----------|--------|
| C-001 | Prompt-only, read-only | No CLI or core change. The analyze step still mutates nothing but `analysis-report.md` through `record-analysis`. | Technical | High | Open |
| C-002 | One discovery mechanism | Planning artifacts come only from the `check-prerequisites` inventory, `meta.json` and the canonical fixed paths `<mission_dir>/occurrence_map.yaml` and `<mission_dir>/decisions/`; no glob or second file-discovery mechanism, and no hard-coded list of inventory key names. | Technical | High | Open |
| C-003 | Existing carrier | Findings use the existing `analysis-findings/v1` carrier and severity vocabulary; the verdict rule (any high/critical → blocked) is unchanged. | Technical | High | Open |
| C-004 | Do not pre-empt neighbours | #147 and #215 are not pre-empted; MVP is read from the `MVP Scope` note `tasks.md` carries (`tasks-template.md`), not redefined. | Business | High | Open |
| C-005 | Charter alignment | The repository aligns to spec-kitty-charter; core loading or rendering compatibility does not block this work (AGENTS.md). | Technical | High | Open |
| C-006 | Generated files by tool | Pack manifests, digests and `docs/packs/` pages change only through their generators. | Technical | Medium | Open |

### Key Entities

- **check-prerequisites inventory**: `artifact_files` (key → file path), `artifact_dirs` (key → directory path, includes `feature_dir` = the mission dir), `available_docs` (file names).
- **Creation intent**: `meta.json` fields `purpose_tldr`, `purpose_context`, optional `source_description`.
- **Finding**: id (prefix + number), severity, category, summary; carried in `analysis-findings/v1`.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: An agent following the prompt on a mission with a research decision no task implements reports exactly one planning-artifact finding for it. — [build] · no-op passable: no
- **SC-002**: A report whose only findings are product-coherence findings records as `ready`; its Product Coherence section ends with exactly one recommendation line. — [build] · no-op passable: no
- **SC-003**: 100% of the #213, #214 and #247 acceptance criteria map to a pinned assertion or a named prompt line, recorded in the mission's issue matrix and the PR body. — [build] · no-op passable: no
- **SC-004**: The analyze prompt is at most 500 lines and all repository gates pass. — [ratchet] · no-op passable: yes — paired with SC-001/SC-002, which a no-op fails

## Decisions

| Decision | Answer | Source |
|---|---|---|
| Coherence severity (`01M7X008WPE69RHV2JSR234EQB`) | Advisory: capped at MEDIUM, never blocks; mandatory recommendation line; #213 contradictions keep normal severity. | Operator ruling 2026-11-20 |
| #247 fold (`01M7X00BBTFW4S3C1V62SZ9YNT`) | Fold the helpful squad findings; close #247 via this PR. | Operator ruling; Step-0 squad (lens B: "change helpful") |
| Mission shape (`01M7X00DWXNK88D71G5TTP7D9H`) | One prompt-only, read-only mission for #213 + #214. | Operator ruling |

## Assumptions

- #214's "the readiness verdict accounts for product coherence" is met by reporting the coherence recommendation beside the verdict and in Next Actions, not by changing the carrier's verdict rule; the operator ruling makes coherence advisory.
- Intent overlap between the two issues is split as: ungrounded behaviour (traceability, #213, normal severity) vs intent drift of the plan as a whole (judgement, #214, advisory).
- `occurrence_map.yaml` is not in the inventory; it is read at its canonical path `<mission_dir>/occurrence_map.yaml` when present.
- `source_description` is rarely present (1 of 13 local missions); its absence is stated, not a finding.

## Out of Scope

- Core-side snapshot pins, deterministic checkers and fixture tests (core #1131, #849).
- A new intent artifact, mutating planning files, auto-reconciliation.
- #147, #215, #237 and #246 beyond what already shipped.
