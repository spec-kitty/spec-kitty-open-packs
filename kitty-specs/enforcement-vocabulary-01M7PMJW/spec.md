# Mission Specification: Directive enforcement vocabulary

**Mission Branch**: `issue-233-enforcement-vocabulary`
**Created**: 2026-11-18
**Status**: Draft
**Input**: Issue #233 (body, the 2026-11-12 triage comment, the 2026-11-14 audit comment and the 2026-11-18 operator ruling), dispatched by the orchestrator: "run the FULL #233 enforcement-vocabulary sweep BEFORE #216".

## Intent Summary

How strictly a directive binds is a property of **the adopting project's charter**, not of the directive (core #5207, carried here by #233). Today the packs say it twice and disagree with themselves: each directive carries an `enforcement:` level, and its prose separately claims to be "advisory in v1", "mandatory", "binding" or "not a runtime gate". The three level values are not defined anywhere in the packs.

- **Primary actor**: a pack author writing or reviewing a directive. Secondary actors: an adopting project's charter maintainer who chooses levels, and an agent that reads directive text at runtime.
- **Trigger**: a directive is authored, reviewed or loaded into an agent's context.
- **Outcome**: the level vocabulary is defined once (a glossary term plus the authoring guidance). Directive bodies and the content that cites them state *what* the rule requires, never *how strictly* it binds. The `enforcement:` field stays as the pack-supplied default, because the pinned charter schema requires it.
- **Invariant**: no directive body, and no step or tactic that cites one, makes a claim about its own enforcement level or criticality. A guard keeps that class closed.
- **Boundary**: this vocabulary (how strictly an in-force directive binds) is distinct from the activation-preset vocabulary (`must_have`, `policy.yaml` levels; #242, #201), which decides *which* artefacts are in force.

This mission is a bulk edit (`change_mode: bulk_edit`). The same phrases ("advisory in v1", "This is advisory", "binding", "mandatory") are removed or reworded across many files, and each occurrence is classified in `occurrence_map.yaml` during planning.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - One definition of the levels (Priority: P1)

A pack author choosing `enforcement:` for a new directive (for example #216's directive) looks the value up in one place, and finds what `required`, `lenient-adherence` and `advisory` mean and who decides the level that applies.

**Why this priority**: #216, #217 and #219 start out on this vocabulary (operator ruling); without a definition, authors keep inventing level prose.

**Independent Test**: the foundation glossary context carries a term defining the three values and the default-versus-charter split, and the authoring guide points to that term.

**Acceptance Scenarios**:

1. **Given** the foundation glossary context, **When** an author looks up the enforcement level, **Then** one term defines `required`, `lenient-adherence` and `advisory`, says the field is the pack-supplied default, and says the adopting charter decides the level that applies.
2. **Given** the pack-authoring guide, **When** an author reads the directive section, **Then** it points to that term and says the directive body must not restate the level.

### User Story 2 - Directive bodies say what, not how strictly (Priority: P1)

An agent loading DIRECTIVE_051 reads the five controls and the evidence they require, with no claim that the directive is "advisory in v1" that contradicts its `required` level.

**Why this priority**: the contradiction is the reported defect (051, 052, 028, 049).

**Independent Test**: no directive body in any pack carries self-binding prose; 051, 052, 028 and 049 read cleanly.

**Acceptance Scenarios**:

1. **Given** DIRECTIVE_051, **When** its body is read, **Then** it has no "advisory", "in v1" or gate-posture claims, and every control and evidence rule is intact.
2. **Given** DIRECTIVE_052, **When** its body is read, **Then** the investigation is still what a fix must produce, but it is not described as "mandatory".
3. **Given** DIRECTIVE_049, **When** its intent is read, **Then** the "advisory guidance, not a runtime gate" sentence is gone.

### User Story 3 - Steps and tactics stop restating the level (Priority: P2)

An implementer following the software-dev plan, implement or review step sees the supply-chain checklist and its evidence rule, without an "advisory in v1" caveat.

**Independent Test**: the phrase "advisory in v1" (and its variants) appears nowhere under `packs/`.

**Acceptance Scenarios**:

1. **Given** the software-dev plan, implement and review prompts, guidelines and substeps, **When** they cite DIRECTIVE_051, **Then** they state the checklist and the evidence requirement only.
2. **Given** the `supply-chain-install-safety` tactic, **When** it is read, **Then** it carries no level posture.

### User Story 4 - The class stays closed (Priority: P2)

A future pull request that adds "This directive is advisory in v1" to a pack fails CI.

**Independent Test**: the vocabulary guard refuses a fixture carrying self-binding phrasing and accepts the cleaned packs.

**Acceptance Scenarios**:

1. **Given** a pack file containing "advisory in v1", **When** the vocabulary guard runs, **Then** it reports an error naming the file and line.
2. **Given** a directive whose body says "This is advisory guidance" or "is binding", **When** the guard runs, **Then** it reports an error.
3. **Given** the cleaned packs, **When** the guard runs, **Then** it exits 0.

### Edge Cases

- A word such as "advisory" or "mandatory" used in another sense stays: an npm-audit *advisory* (drupal toolguide), a *mandatory* report field (QA_002), glossary *enforcement tiers* (writing pack), the `enforcement` *mode* of the glossary middleware. The occurrence map classifies each one.
- Prose describing a concrete check that a procedure or tool runs (for example "minutes with ownerless actions are refused") is behaviour, not criticality, and stays.
- "in v1" naming a tool's format version (QA toolguides, `qa-traceability/v1`) is out of scope.
- `explicit_allowances` that borrow a level name ("an acceptable lenient-adherence allowance") are reworded so the body does not use level vocabulary.
- Graph edge `reason` text ("the directive's binding rules") is content that cites a directive, so it is reworded too.

## Requirements *(mandatory)*

### Functional Requirements

| ID | Title | User Story | Priority | Status | Delivery | No-op passable? |
|----|-------|------------|----------|--------|----------|-----------------|
| FR-001 | Level term in the glossary | As a pack author, I want one glossary term in the foundation `spec-kitty-core` glossary context that defines `required`, `lenient-adherence` and `advisory`, states that the directive's `enforcement:` value is the pack-supplied default, and states that the adopting charter decides the effective level, so that the levels are defined once. | High | Open | [build] | no |
| FR-002 | Level vocabulary kept apart from activation vocabulary | As a charter maintainer, I want the term to say it is distinct from activation-preset `must_have` / `policy.yaml` levels, so that "which artefacts are in force" and "how strictly a directive binds" are not conflated. | Medium | Open | [build] | no |
| FR-003 | Authoring guidance points to the term | As a pack author, I want the pack-authoring guide and the artefact reference to point to the glossary term, and to say a directive body never restates its level or criticality, so that new directives start on the settled vocabulary. | High | Open | [build] | no |
| FR-004 | Seed directives cleaned | As an agent, I want DIRECTIVE_051, DIRECTIVE_052, DIRECTIVE_028 and DIRECTIVE_049 free of enforcement and criticality prose, with every rule's substance kept, so that the body and the level field no longer disagree. | High | Open | [build] | no |
| FR-005 | Every pack's directives swept | As an agent, I want every directive in every pack free of self-binding prose (level, criticality, gate posture, "makes X binding"), so that the defect is fixed for the whole class, not only for the four named directives. | High | Open | [build] | no |
| FR-006 | Steps, prompts and the tactic swept | As an implementer, I want the "advisory in v1" wording removed from the software-dev plan, implement and review prompts, guidelines and step substeps, and from the `supply-chain-install-safety` tactic, keeping the checklist and evidence rules, so that the content that cites DIRECTIVE_051 does not restate a level. | High | Open | [build] | no |
| FR-007 | Content citing directives swept | As a reader, I want graph edge reasons and pack READMEs that characterise a directive's bindingness reworded, so that no pack content outside directives claims a level. | Medium | Open | [build] | no |
| FR-008 | Field kept as the pack-supplied default | As a charter maintainer, I want every directive to keep its `enforcement:` field with its current value, and the decision (and the pin evidence for it) recorded in an ADR, so that packs stay valid at the pin and adopters see no change in behaviour. | High | Open | [ratchet] | yes — paired with FR-001/FR-003, which give the field its new reading |
| FR-009 | Guard keeps the class closed | As a maintainer, I want the vocabulary guard to refuse self-binding phrasing in pack content, with tests that prove a planted phrase is caught and the cleaned packs pass, so that the defect class cannot silently reopen (DIRECTIVE_043). | High | Open | [build] | no |
| FR-010 | Versions, changelog, digests and pages | As a consumer, I want each changed pack's version raised per DIRECTIVE_018, a changelog entry, restamped digests and regenerated pack pages, so that the release surface reflects the change. | High | Open | [build] | no |

### Non-Functional Requirements

| ID | Title | Requirement | Category | Priority | Status |
|----|-------|-------------|----------|----------|--------|
| NFR-001 | Gates green | `validate-packs.sh` (including `--cross-pack`), the digest check, `check_vocabulary.py`, `gen_pack_reference.py --check` and all four unit-test suites exit 0; the charter-service and drift jobs pass in CI. | Reliability | High | Open |
| NFR-002 | Software-dev content stays ASCII | 0 non-ASCII characters in changed software-dev mission files (`tests/ci/test_software_dev_ascii.py` passes). | Compatibility | High | Open |
| NFR-003 | No rule substance lost | 0 integrity rules or validation criteria removed from a directive except ones whose only content was a level claim; each such removal is listed in the occurrence map. | Correctness | High | Open |

### Constraints

| ID | Title | Constraint | Category | Priority | Status |
|----|-------|------------|----------|----------|--------|
| C-001 | Pinned contract | The `enforcement:` field stays: at charter `050d780` it is a required property of the directive schema, with the enum `required`, `lenient-adherence`, `advisory`. | Technical | High | Open |
| C-002 | Charter alignment | The work aligns to the charter, not to core; core compatibility does not block or reshape it (AGENTS.md). | Technical | High | Open |
| C-003 | No default-level changes | Directive `enforcement:` values are not changed in this mission (operator question Q2; recommendation A). | Business | High | Open |
| C-004 | Identity stable | No artefact id or file name changes; QA_001 is retitled only (operator question Q3; recommendation A). | Technical | Medium | Open |

### Key Entities

- **Enforcement level**: one of `required`, `lenient-adherence` or `advisory`; how strictly an in-force directive binds.
- **Pack-supplied default**: the `enforcement:` value a directive ships with. The adopting charter may override it.
- **Self-binding prose**: text in a directive, or in content that cites one, that claims the directive's level, criticality or gate posture.
- **Activation level** (out of scope, kept distinct): `must_have` and `policy.yaml` levels, which decide which artefacts are in force.

## Assumptions

- Q1 (which prose counts): recommendation A. Statements about how strictly a directive binds are removed; descriptions of a concrete check a procedure or tool performs stay. Sent to the operator 2026-11-18; revisit if overruled.
- Q2 (default values): recommendation A, values unchanged. Sent to the operator.
- Q3 (QA_001 title): recommendation A, retitle only. Sent to the operator.
- #266 and #273 have no open PR on 2026-11-18, so no rebase onto them is needed now. A rebase onto `main` restamps the changelog and digests.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 0 occurrences of "advisory in v1" (case-insensitive) or its variants under `packs/`, down from 14 (lines naming an advisory or gate posture "in v1"). — [build] · no-op passable: no
- **SC-002**: 0 directive bodies across all packs with self-binding prose, down from at least 8 (051, 052, 049, cloud-session-orchestration, action-item-attribution, 042, reconcile-change-scope-tensions, QA_001). — [build] · no-op passable: no
- **SC-003**: exactly 1 glossary term defines the three levels, and the pack-authoring guide links to it. — [build] · no-op passable: no
- **SC-004**: 59 directives still carry `enforcement:`, with the same values as before the mission. — [ratchet] · no-op passable: yes — paired with SC-002 on the same files
- **SC-005**: the guard catches a planted "advisory in v1" phrase in a test fixture, 100% of the time. — [build] · no-op passable: no
