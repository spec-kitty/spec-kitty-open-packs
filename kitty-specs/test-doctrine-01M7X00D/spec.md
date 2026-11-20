# Mission Specification: Test doctrine: mock boundary and red-first value

**Mission Branch**: `t3/test-doctrine-mock-boundary`
**Created**: 2026-11-20
**Status**: Draft
**Input**: Issues #216 and #209, with #151 folded in, and the #218 field note carried on #216. Dispatched by the orchestrator with operator rulings of 2026-11-20 (allow-list, evidence carve-out, pack tier, DIRECTIVE_041 edit).

## Intent Summary

Two test-quality failures recur in missions that consume these packs:

1. **Mocking code the system under test owns.** A test stubs an internal helper to pin a call contract. The stub can produce a state the real code never reaches, so the test raises a false alarm (or gives false confidence). In the motivating incident, a stubbed status-marking step produced a run with zero status events, and a "data-loss" investigation chased a state only the stub could create.
2. **Pro-forma red-first tests.** Red-first discipline is applied mechanically to configuration and glue work. The resulting tests restate the configuration, go red only because the configuration does not exist yet, and afterwards fail only when someone changes the configuration on purpose.

- **Primary actors**: an implementer agent writing tests for a work package; a reviewer agent (and the adversarial squad) judging those tests.
- **Trigger**: a work package adds or changes tests, or a reviewer reviews them.
- **Outcome**: a citable foundation directive says where a test may mock (the responsibility border, with an explicit allow-list). The red-first rule is scoped to behaviour with a lasting regression risk; for configuration and glue work, a real run or an existing gate is recorded as the evidence instead of a test. The red-first procedure makes the red verifiable (the failure text is recorded, the red shape does not break collection). Review guidance flags internal mocks and configuration-restatement tests as defects.
- **Invariants**: (a) every test that *is* written still meets the non-vacuity rules; (b) no surface still reads as "every work package needs a failing-first test" without the carve-out; (c) consumer-facing packs name no core issue numbers or core paths.
- **Boundary**: "responsibility boundary" (the issues say "border") is the edge of what the system under test owns for the behaviour under test, drawn by responsibility, not by layer or module (the existing `test-boundaries-by-responsibility` tactic). It is not the deployment boundary.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - A citable rule for where tests may mock (Priority: P1)

A reviewer sees a test that patches an internal helper of the module under test and asserts it was called once. The reviewer cites one directive that says this is not allowed, lists the seams that may be mocked, and points to the remediation steps.

**Why this priority**: #216 is the GA-milestone deliverable; without a citable rule, reviewers argue from taste.

**Independent Test**: the directive loads through the charter context for the implement and review actions and for the implementer and reviewer profiles, and it names the allow-list and the remediation procedure.

**Acceptance Scenarios**:

1. **Given** the foundation pack, **When** an agent loads `DIRECTIVE_054`, **Then** it reads the rule (mock only at the responsibility border), the exhaustive allow-list from the 2026-11-20 ruling, the named anti-pattern (mocking owned logic to pin a call contract, which can manufacture unreachable states), and a pointer to the remediation procedure.
2. **Given** an over-mocked test, **When** an implementer follows the remediation procedure, **Then** each mock is classified as border or owned, owned mocks are removed in favour of real collaborators with real seeded state, and assertions move from call arguments to observable outcomes.
3. **Given** the review action of the software-dev mission, **When** a reviewer reviews tests, **Then** the review guidance tells them to flag mocks of owned logic and cite `DIRECTIVE_054`.

### User Story 2 - Red-first where it earns its keep (Priority: P1)

An implementer delivers a work package that adds a CI workflow. Instead of writing tests that restate the workflow's YAML, they label the requirement `[evidenced-by-run]` and record the first real run of the workflow as the evidence. For the router script the workflow calls, which carries real logic, they still write a red-first test.

**Why this priority**: #209 reports the waste directly; the operator ruled that evidence replaces the test for configuration and glue work.

**Independent Test**: DIRECTIVE_034, the ATDD tactics, the non-vacuity tactic and the review guidance all state the same carve-out and the long-term-value question.

**Acceptance Scenarios**:

1. **Given** DIRECTIVE_034, **When** an agent reads it, **Then** red-first is required for product logic, gate and classifier scripts, invariants that must hold across future edits, and security or permission policy; for other work a recorded real run or an existing gate is the evidence.
2. **Given** the non-vacuity tactic, **When** an author labels a criterion, **Then** `[evidenced-by-run]` is a defined delivery label that names the run or gate, and the tactic asks the long-term-value question: would the test catch a real regression in six months, or only fail when someone changes the configuration on purpose?
3. **Given** a test that only restates configuration, **When** a reviewer reviews it, **Then** the review guidance tells them to flag it as waste, not to reward it as ATDD compliance.
4. **Given** a test that is written under the carve-out (for example a policy invariant), **When** it is reviewed, **Then** the non-vacuity rules still apply to it.

### User Story 3 - A red that proves the right thing (Priority: P2)

An implementer writing a bug reproduction records the failure text it produced on the unfixed code, picks a red shape that fails only that test (without breaking collection of the rest of the module), and, where an existing characterization test pins the defect, inverts that test rather than adding a parallel one. When the reproduction lands in a different work package from the fix, it is marked as an expected failure that turns into an error once it passes.

**Why this priority**: #151 is a P3 refinement of the same procedure; folding it avoids a second edit to the same file.

**Independent Test**: the red-first bug-reproduction procedure carries each of the four points exactly once, without duplicating DIRECTIVE_034 or `delete-the-assertion-not-the-test`.

**Acceptance Scenarios**:

1. **Given** the procedure, **When** an implementer proves red, **Then** they record the observed failure text as evidence in the work package.
2. **Given** a reproduction that needs a symbol the fix introduces, **When** it is written, **Then** the procedure tells them to import it lazily inside the test so the module still collects.
3. **Given** an existing test that asserts the buggy behaviour, **When** the fix is planned, **Then** the procedure points to inverting that test, with a reference to `delete-the-assertion-not-the-test`.

### User Story 4 - Spec Kitty's own CI example lives in the house pack (Priority: P3)

A Spec Kitty maintainer adding a docs-site CI job finds a worked example in the `internal` pack that separates the workflow-shape pins (drop them; the first real run is the evidence) from the router logic and the read-only, no-secrets policy (keep them, preferably as a general workflow policy check).

**Independent Test**: the internal pack carries the worked example, and the foundation and testing packs carry no Spec Kitty-specific CI wording.

### Edge Cases

- A configuration file that encodes a security or permission policy (for example "no secrets, read-only permissions") carries lasting regression risk: red-first or a general policy check applies, not `[evidenced-by-run]`.
- A real run that cannot happen before merge (for example a workflow triggered only on the default branch): the work package records which existing gate stands in, or how the first run will be confirmed; "no evidence" is never acceptable.
- A boundary mock that only supports the single scenario the author imagined relocates the anti-pattern one step out; the directive requires border substitutes to preserve the real dependency's observable contract.
- A unit test that "needs" an internal mock signals a misdrawn boundary; the remedy is to widen the slice or extract a pure seam, not to add the mock.
- Deleting a change-detector test: DIRECTIVE_041 currently says deleting a test deletes coverage. The edit must reconcile this with removing a pure restatement whose evidence is recorded elsewhere.
- A Python-specific mechanism (`xfail(strict=True)`) is given as an example of a language-neutral rule, not as the rule itself.

## Requirements *(mandatory)*

### Functional Requirements

| ID | Title | User Story | Priority | Status | Delivery | No-op passable? |
|----|-------|------------|----------|--------|----------|-----------------|
| FR-001 | Mock-boundary directive | As a reviewer, I want a foundation directive `DIRECTIVE_054` "Mock Only at the Responsibility Boundary" that states the rule, the exhaustive allow-list (another domain or bounded context; filesystem; database; network and external APIs; clock; randomness; git and other processes; narrow system cases such as DTO validation and hook or notification sends), that the allow-list permits a substitute and never requires one, the named anti-pattern with a neutral worked example, and that border substitutes preserve the real dependency's observable contract, so that I can cite one rule. | High | Open | [build] | no |
| FR-002 | Remediation procedure | As an implementer, I want a foundation procedure that walks an over-mocked test back to the boundary (identify the behaviour, draw the boundary, classify each mock, drive real collaborators with seeded state, move assertions to observable outcomes by pointing to `observable-contract-test-authoring`, check the border substitutes keep the real contract), so that the fix is repeatable. | High | Open | [build] | no |
| FR-003 | Sibling mock surfaces agree | As an agent, I want every surface that lists mock seams or mocking rules to agree with the FR-001 allow-list and to name `DIRECTIVE_054` as the owner: foundation `test-boundaries-by-responsibility` (no "services outside the current module", no "DO mock"), `test-scaffolding-as-design-smell`, `black-box-integration-testing`, `function-over-form-testing`, `testing-select-appropriate-level`, the reviewer-renata profile, DIRECTIVE_036 (unit-level tests point at 054, not "their own directives"), and testing `test-desiderata-and-boundaries` (seam lines and its quality test) and `testing-principles` (its "one owner" note), so that no two surfaces give different seam lists. | High | Open | [build] | no |
| FR-004 | Directive wired into the graph | As an agent, I want `DIRECTIVE_054` scoped to the software-dev implement and review actions, required by reviewer-renata, suggested by implementer-ivan and generic-agent (and by the qa test-designer profile, cross-pack), requiring DIRECTIVE_041 and its procedure, and required by DIRECTIVE_036, so that it loads when tests are written or reviewed. | High | Open | [build] | no |
| FR-005 | Red-first scoped to lasting regression risk | As an implementer, I want DIRECTIVE_034 to own the carve-out: red-first is required for product logic, gate and classifier scripts, invariants and security or permission policy; for configuration and glue work a recorded real run or existing gate is the evidence. Its "explicit justification in the commit or PR" rule and its "each new behavior" criterion are replaced by this, so that there is one mechanism. | High | Open | [build] | no |
| FR-006 | Evidenced-by-run label and long-term-value question | As a spec author, I want the non-vacuity tactic to own the `[evidenced-by-run]` label (beside `[build]`, `[ratchet]`, `[folded]`; it names the run or gate and where the record lives, generalising the mission's `workflow-evidence.md`) and the long-term-value question ("would it catch a real regression in six months, or only fail when someone changes the configuration on purpose?"), next to "could this test fail?" and "when it fails, does that mean something is broken?", so that config restatement is recognisable. | High | Open | [build] | no |
| FR-007 | ATDD and TDD surfaces carry the carve-out | As an implementer, I want `acceptance-test-first`, `tdd-red-green-refactor` (including "block merge when new code has no corresponding tests"), the `test-first-cycle` procedure, the software-dev implement prompt ("Follow TDD practices", "Write tests first (TDD)"), the spec template and specify prompt label legend, and the testing pack's `atdd-adversarial-acceptance`, to state the carve-out in at most one sentence pointing to DIRECTIVE_034 and the non-vacuity tactic, so that no surface reads as "every work package needs a failing-first test". | High | Open | [build] | no |
| FR-008 | Review guidance flags both defects | As a reviewer, I want the software-dev review step to tell me to flag mocks of owned logic (citing DIRECTIVE_054) and pure configuration-restatement tests (as waste, not ATDD compliance), and to check that every `[evidenced-by-run]` row cites a run or gate that exists, so that both defects and carve-out abuse are caught at review. | High | Open | [build] | no |
| FR-009 | Red for the right reason, verifiably | As an implementer, I want `red-first-bug-reproduction` to own: recording the observed failure text; inverting an existing characterization test that pins the defect (pointing to `delete-the-assertion-not-the-test`); and marking a reproduction that lands in a different work package from its fix as a strict expected failure that the fix removes. The red-shape point stays in DIRECTIVE_034 and the procedure cites it. The testing pack's `test-first-bug-fixing` points to the procedure and its "commit test and fix together" step allows the cross-work-package case, so that the red is evidence. | Medium | Open | [build] | no |
| FR-010 | DIRECTIVE_041 and its xfail rule reconciled | As an agent, I want a minimal edit to DIRECTIVE_041 that keeps "never delete a test to dodge a failure" but allows retiring a change-detector test once real-run or gate evidence is recorded, and that does not count a strict expected failure on a reproduction whose fix is planned in a named sibling work package as masking a defect; `observable-contract-test-authoring` and the reviewer-renata profile say the same, so that 041 and the new rules do not contradict. | High | Open | [build] | no |
| FR-011 | House specifics in the internal pack | As a Spec Kitty maintainer, I want the CI-workflow worked example (which pins to drop, which logic and policy to keep) in the `internal` pack, linked to the foundation rule, and the internal surfaces that say "ATDD-first" or "red-first" (`cloud-session-dispatch`, the `mission-from-issue` skill, `landing-contributor-prs` test-economy rule) aligned to the carve-out by a pointer, so that house specifics stay out of consumer packs. | Medium | Open | [build] | no |
| FR-012 | Glossary terms | As a reader, I want foundation glossary terms "responsibility boundary" (alias "responsibility border") and "change-detector test", so that the new wording uses defined vocabulary and does not add a competing synonym. | Medium | Open | [build] | no |
| FR-013 | Release surface | As a consumer, I want the changed packs versioned per DIRECTIVE_018 (minor: the foundation lockstep set and built-in, plus each changed org pack), digests, manifests and the built-in digest constant restamped, pack reference pages regenerated, docs freshness kept and a changelog entry, so that the release surface reflects the change. | High | Open | [evidenced-by-run] | n/a -- evidence: the digest, manifest, pack-reference and freshness gates |

### Non-Functional Requirements

| ID | Title | Requirement | Category | Priority | Status |
|----|-------|-------------|----------|----------|--------|
| NFR-001 | Gates green | `validate-packs.sh`, `pytest tests`, `check_vocabulary.py`, `gen_pack_reference.py --check`, `check-pack-digests.sh` and `check_docs_freshness.py --base origin/main` all exit 0; the charter-service check and the charter drift test pass. | Reliability | High | Open |
| NFR-002 | Software-dev content stays ASCII | 0 non-ASCII characters in changed software-dev mission files (`tests/ci/test_software_dev_ascii.py` passes). | Compatibility | High | Open |
| NFR-003 | No consumer-pack core references | 0 core issue numbers, core PR numbers or core repository paths in the new or changed foundation, testing and qa content (#273). | Portability | High | Open |
| NFR-004 | One canonical home per rule | Each new rule is defined in exactly 1 artefact (owner map: allow-list and anti-pattern -> DIRECTIVE_054; carve-out -> DIRECTIVE_034; label and long-term-value question -> `acceptance-criteria-non-vacuity`; failure text, characterization inversion and cross-work-package expected failure -> `red-first-bug-reproduction`; CI example -> internal); every other surface states it in at most one sentence and names the owner. | Maintainability | Medium | Open |

### Constraints

| ID | Title | Constraint | Category | Priority | Status |
|----|-------|------------|----------|----------|--------|
| C-001 | Charter alignment | Validate against the charter pin in `charter.lock.yaml`; core compatibility does not block or reshape the work (AGENTS.md). | Technical | High | Open |
| C-002 | Pack tier split | General rules in `foundation`, and in `testing` (and `qa`) only for the sibling surfaces that must agree; Spec Kitty house specifics only in `internal` (operator ruling). | Business | High | Open |
| C-003 | Minimal 041 edit | DIRECTIVE_041 changes are limited to what FR-010 needs; its id, title and other rules stay. | Business | High | Open |
| C-004 | Graph edge identity | At most one edge per unordered pair in a pack (the edge-identity test); no new 034-041 edge (the existing 041 requires 034 edge covers it). Any `tension` edge uses the charter spelling, source the lexicographically smaller owned URN. None is planned. | Technical | Medium | Open |
| C-005 | Directive id | The new directive takes the next free id, `DIRECTIVE_054` (verified free across all packs on 2026-11-20; `DIRECTIVE_047` is taken). | Technical | High | Open |
| C-006 | No enforcement prose | Directive bodies state what the rule requires, never how strictly it binds (the enforcement-vocabulary guard). | Technical | High | Open |
| C-007 | Out of scope | #154; the doctrine validator gap from #218; and these #218 items carried on #216: a tests-as-scaffold paradigm and the split of 041's mindset into it, the two anti-pattern nodes and four reference assets, checklist de-duplication into assets, and the curator profile update. They stay open on #216, which the PR references without closing. | Business | Medium | Open |

### Key Entities

- **Responsibility boundary** (alias responsibility border): the edge of what the system under test owns for the behaviour under test; collaborators inside it run for real.
- **Allow-listed seam**: a dependency outside the border that a test may replace with a substitute that keeps its observable contract.
- **Change-detector test**: a test that restates configuration or structure, goes red only because the thing does not exist yet, and afterwards fails only on intentional change.
- **Lasting regression risk**: behaviour a future edit could break without meaning to: product logic, gate and classifier scripts, invariants, security and permission policy.
- **Evidence record**: the named real run or existing gate that stands in for a red-first test under `[evidenced-by-run]`.

## Assumptions

- Operator rulings of 2026-11-20 (recorded as decision moments): widened allow-list; evidence replaces the test for configuration and glue work; tier split; DIRECTIVE_041 edited here, minimally.
- #151's triage named a `bug-fixing-checklist` tactic; it was folded into the testing pack's `test-first-bug-fixing` procedure. The foundation `red-first-bug-reproduction` procedure, which DIRECTIVE_034 requires, becomes the owner; `test-first-bug-fixing` points to it. The red-shape point already lives in DIRECTIVE_034 and is not duplicated.
- Versioning: minor. DIRECTIVE_054 codifies what DIRECTIVE_036, DIRECTIVE_041 and `test-boundaries-by-responsibility` already forbid (patching inside-boundary collaborators), and DIRECTIVE_034 is loosened, so conforming work does not stop conforming (DIRECTIVE_018). Precedent: the additive readiness-gate release (foundation lockstep 3.1.0).
- The #218 delivery items listed in C-007 stay open on #216 for a follow-up. The core research note's §8 is superseded by its artefact-series proposal; this mission takes the genuine deltas from that proposal (allow-list, failure mode, remediation procedure) without creating a third tests authority.
- A new foundation procedure is preferred over assets for the worked example, because foundation ships no assets today and a short neutral example fits inline.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 1 directive, `DIRECTIVE_054`, carries the allow-list, and it is reachable from 2 software-dev actions (implement, review) and 4 agent profiles. — [build] · no-op passable: no
- **SC-002**: 0 testing surfaces in foundation, testing or internal state an unconditional "every change needs a failing test first" rule without the carve-out, across the 9 surfaces named in FR-005, FR-007 and FR-011. — [build] · no-op passable: no
- **SC-003**: Each surface named in FR-003 either names `DIRECTIVE_054` as the owner of the seam list or states seams that are a subset of its 8 allow-list categories, with none saying a seam must be mocked. — [build] · no-op passable: no
- **SC-004**: Each of the 3 owned points of FR-009 appears in exactly 1 artefact (`red-first-bug-reproduction`), and the red-shape point only in DIRECTIVE_034. — [build] · no-op passable: no
- **SC-005**: 0 Spec Kitty-specific CI wording in foundation or testing; 1 worked example in internal. — [build] · no-op passable: no
- **SC-006**: All gates in NFR-001 green at the PR head. — [evidenced-by-run] · no-op passable: n/a -- evidence: the CI run on the PR head
