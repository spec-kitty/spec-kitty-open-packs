# Mission Specification: Test doctrine 2: tests-as-scaffold paradigm, tracer bullets and measurement discipline

**Mission Branch**: `t3/test-doctrine-2`
**Created**: 2026-11-21
**Status**: Draft
**Input**: Issues #216 (residue), #154 and #147 (one work package), #152, with the testing-principles and DIRECTIVE_034 parts of #273 and #274 folded in. Dispatched under epic #288 with operator rulings of 2026-11-21 (scope, order, upstream re-grounding) and two operator answers of the same day (Quad-A asset, refactoring outside the TDD loop), all recorded as resolved decision moments.

## Intent Summary

The first test-doctrine mission shipped the mock-boundary rule (`DIRECTIVE_054`), the remediation procedure `unfake-an-over-mocked-test` and the red-first carve-out. This mission finishes #216 and sharpens the neighbouring test-first guidance.

1. **Mindset vs rule.** `DIRECTIVE_041` "Tests as Scaffold, Not Friction" carries a mindset (why tests exist, false confidence vs false friction) inside a binding directive. The mindset moves to a new paradigm; 041 keeps its rules and refines the paradigm.
2. **Named anti-patterns.** "Mocking owned logic to pin a call contract" and "asserting on mock interactions" become graph nodes the good artefacts reject, so review and context resolution can name them.
3. **Reference assets.** Checklists that are restated in several places (Beck's test desiderata, the Quad-A test skeleton) and the long worked examples (functional slicing, unfaking an over-mocked test) move into four shared assets that the artefacts using them require or suggest.
4. **Curator.** The curator profile `doctrine-daphne` carries the canonical layout for assets and anti-pattern nodes, so the next curator does not rediscover it.
5. **Tracer bullets.** Test-first guidance says plainly: work in vertical slices (one behaviour, one failing test, one minimal implementation, repeat), test only through the public interface at agreed seams, never write all tests first. At mission scale, a mission whose work packages cross owners proves one thin composed path (the spine) before scaling out (`vertical-skeleton-first`). Both levels use one defined "tracer bullet" vocabulary.
6. **Green mode.** Refactoring leaves the red-green loop. It is a separate, green-only technique (already governed by `DISCIPLINED_REFACTORING` and its procedure) that an implementer switches into whenever the suite is green.
7. **Measurement discipline.** Agents sharing a machine cap concurrent heavy test runs, treat a killed, timed-out or piped run as no measurement, keep test temp space off small quotas, and attribute a red by re-running on the mission's recorded base commit.

- **Primary actors**: an implementer agent writing tests and code for a work package; a reviewer agent and the adversarial squad judging them; a planner slicing a mission; a curator authoring doctrine.
- **Trigger**: a work package adds tests or production code, a reviewer reviews them, a planner decomposes a mission, a curator authors pack content, or several agents run tests on one machine.
- **Outcome**: each idea above has exactly one canonical home, is reachable through graph edges from the artefacts that load at the right action, and no other surface contradicts it.
- **Invariants**: (a) no rule is stated with full force in two artefacts; (b) consumer packs (foundation, testing, planning-analysis, python, java, javascript) name no Spec Kitty core issue, PR, commit, symbol or path; (c) every resolved-only node (asset, anti-pattern) has at least one inbound edge from an activatable artefact; (d) `DIRECTIVE_041` keeps its id, title, enforcement and every rule.
- **Boundary**: "tracer bullet" means a thin path through the real system, end to end, that is kept and grown, not thrown away. It is not a prototype or a spike.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - The mindset has its own home (Priority: P1)

A reviewer cites `DIRECTIVE_041` for a test that stays green when the code regresses. An agent that wants to know why the rule exists follows 041's `refines` edge to the `tests-as-scaffold-not-friction` paradigm, which explains false confidence and false friction, the desiderata as the value system, the connascence framing, and that "never mock owned logic" is a project policy choice stronger than its sources.

**Why this priority**: the operator ruled the paradigm and the 041 split first; every later edge hangs off the paradigm.

**Independent Test**: the paradigm validates and loads, 041 refines it, 041's intent is a short pointer and its integrity rules and validation criteria are byte-for-byte unchanged.

**Acceptance Scenarios**:

1. **Given** the foundation pack, **When** an agent loads the paradigm, **Then** it reads the mindset 041's old intent carried, plus the tensions the sources leave open (desiderata do not mention mocks; connascence is a lens, not proof; removing owned mocks moves residual risk to runtime, so contract tests at real boundaries stay).
2. **Given** `DIRECTIVE_041` and `DIRECTIVE_054`, **When** the graph is resolved, **Then** both refine the paradigm and the paradigm rejects the two anti-pattern nodes.

### User Story 2 - Anti-patterns and reference assets (Priority: P1)

A reviewer sees a test that patches an internal helper and asserts it was called once. They cite `DIRECTIVE_054`, and the anti-pattern node "mock owned logic to pin a call contract" names the smell. An implementer remediating it follows `unfake-an-over-mocked-test`, which suggests the unfake exemplar asset with a full neutral before/after.

**Why this priority**: the core of the #216 residue.

**Independent Test**: two anti-pattern nodes and four asset nodes exist, each with an inbound edge from an activatable artefact; the desiderata list and the Quad-A skeleton each have exactly one full statement.

**Acceptance Scenarios**:

1. **Given** the test-desiderata styleguide, **When** an agent resolves it, **Then** it requires the desiderata checklist asset, and the styleguide no longer restates the twelve properties one by one.
2. **Given** the python, java and typescript conventions, **When** an agent reads their Quad-A line, **Then** it is one pointer, and each styleguide requires the Quad-A asset through an edge.
3. **Given** the slicing exemplar, **When** an agent reads it, **Then** it walks the user-registration case: the over-mocked API-level test, the Captcha change that broke it, and the re-scoped functional-slice test that substitutes only the database.

### User Story 3 - A curator starts from the pinned model (Priority: P2)

A curator asked to add a worked example places it under the pack's `assets/` with a sidecar, declares the node in the pack's graph, and adds an inbound `requires` or `suggests` edge, because `doctrine-daphne` says so.

**Independent Test**: the profile names the asset layout, the anti-pattern node rule (declared as a node, a `rejects` target, emits no edges) and the inbound-edge requirement exactly once.

### User Story 4 - Tracer bullets at test and mission scale (Priority: P2)

An implementer about to write five tests for a feature writes one, makes it pass with the least code, and only then writes the next. A planner decomposing a mission with three owners names the spine and its first composed path before sizing the owner work packages, and holds second-wave work until that path runs green.

**Independent Test**: `tdd-red-green-refactor` carries the vertical-slice rule, the horizontal-slicing anti-pattern and the agreed-test-surface rule, and `test-first-cycle` points to it in one line; `vertical-skeleton-first` exists in planning-analysis with the bounded spine-event rule; both use the glossary terms "tracer bullet" and "horizontal slicing".

**Acceptance Scenarios**:

1. **Given** the TDD tactic, **When** an agent reads it, **Then** the loop is red then green, one behaviour per cycle, each test a tracer bullet through the public interface, and refactoring is handed to green mode.
2. **Given** the software-dev plan and tasks guidance, **When** a planner reads them, **Then** one line asks whether the mission has a cross-owner spine and points to `vertical-skeleton-first`.
3. **Given** a spine event (a work package discovery that changes a transition another owner consumes), **When** the tactic is followed, **Then** only the consuming work packages pause, the spine re-runs once within its recorded budget, a second amendment of the same row or more than three events escalates to replanning, and a flaky smoke counts as no measurement.

### User Story 5 - Refactoring in green mode (Priority: P2)

An implementer finishes a red-green cycle with duplicated logic. They switch to green mode: they follow `disciplined-refactoring-cycle` (name the smell, one move, tests after each move), the same procedure they would use for a standalone refactor. No step of the TDD loop restates it.

**Independent Test**: no TDD surface carries its own refactoring steps; each points to green mode.

### User Story 6 - Honest test measurement on a shared machine (Priority: P2)

Three agents share a machine. One finds its suite killed after a timeout and does not report it as failed; another sees a red and re-runs that test on the mission base commit before claiming it did not cause it.

**Independent Test**: the measurement tactic exists in testing, is reachable at implement and review, and the internal pack carries the host specifics by pointer only.

### Edge Cases

- A test that "needs" an internal mock in a unit test: the slicing exemplar and the boundary tactic say widen the slice or extract a pure seam.
- "Avoid gold plating" read as licence to mock owned logic for speed: the desiderata styleguide names that misread.
- Beck's "Isolated" read as "isolate from collaborators with mocks": already corrected in the desiderata styleguide; the checklist asset keeps the correction.
- A mission with genuinely independent work packages: `vertical-skeleton-first` says it does not apply.
- A run whose exit status was lost through a pipe: no measurement, re-run with the status captured.
- A red that also fails on the mission base: pre-existing, recorded, not attributed to the work package.

## Requirements *(mandatory)*

### Functional Requirements

| ID | Title | User Story | Priority | Status | Delivery | No-op passable? |
|----|-------|------------|----------|--------|----------|-----------------|
| FR-001 | Tests-as-scaffold paradigm | As an agent, I want a foundation paradigm `tests-as-scaffold-not-friction` that carries the mindset now in DIRECTIVE_041's intent (tests protect change; false confidence from mocked-out behaviour vs false friction from implementation-coupled assertions), the desiderata as its value system, the connascence framing of a mock, and the honest-tension clause (desiderata never mention mocks; connascence is a diagnostic lens; boundary-only mocking is a project policy choice; contract tests at real boundaries stay), so that the why has one home. | High | Open | [build] | no |
| FR-002 | DIRECTIVE_041 split | As an agent, I want DIRECTIVE_041's intent shrunk to a short pointer to the paradigm, its id, title, enforcement, scope, integrity rules and validation criteria unchanged, and `refines` edges from DIRECTIVE_041 and DIRECTIVE_054 to the paradigm, so that the binding rule and its mindset are separate and linked. | High | Open | [build] | no |
| FR-003 | Two anti-pattern nodes | As a reviewer, I want foundation anti-pattern nodes `mock-owned-logic-to-pin-a-call-contract` and `assert-on-mock-interactions`, rejected by the paradigm, DIRECTIVE_054, `unfake-an-over-mocked-test`, `test-boundaries-by-responsibility` (the first) and `function-over-form-testing` (the second), emitting no edges themselves, so that the smells are named graph targets. | High | Open | [build] | no |
| FR-004 | Desiderata checklist asset | As a reviewer, I want a testing asset `test-desiderata-checklist` that holds Beck's twelve desiderata as a review checklist (one line each, with the "Isolated is not isolate-via-mocks" note), required by `test-desiderata-and-boundaries` and `testing-principles` and suggested by the paradigm, with the styleguide's twelve per-property principles replaced by one principle pointing to it, so that the list exists once. | High | Open | [build] | no |
| FR-005 | Quad-A skeleton and checklist asset | As an implementer, I want a testing asset `quad-a-test-structure` with the language-neutral four-phase skeleton and a short review checklist, required by `quadruple-a-test-format` and by the python, java and typescript conventions, whose Quad-A principle and pattern shrink to a one-line pointer (language-specific code examples stay inline); each language pack keeps its testing dependency and gains the reference edge, so that the definition exists once. | High | Open | [build] | no |
| FR-006 | Slicing exemplar asset | As an implementer, I want a foundation asset `exemplar-slicing-user-registration` that walks the functional-slicing case (an API-level test mocking an internal service and asserting a call; a Captcha step breaking it; the re-scoped slice test substituting only the database and asserting the registration outcome), attributed to its source, suggested by `test-boundaries-by-responsibility` and the paradigm, so that test slicing has a full worked example. | High | Open | [build] | no |
| FR-007 | Unfake exemplar asset | As an implementer, I want a foundation asset `exemplar-unfake-an-over-mocked-test` with a full, neutral before/after of the order-fulfilment example already summarised in `unfake-an-over-mocked-test` (no Spec Kitty incident), suggested by that procedure and by DIRECTIVE_054, so that the remediation has a complete worked example. | High | Open | [build] | no |
| FR-008 | Test-slicing content on existing surfaces | As an implementer, I want `test-boundaries-by-responsibility` to state the slicing heuristics (identify the functionality, not the class; a well-scoped unit test needs few substitutes; write tests as if unaware of internal structure, so extracting a helper does not change the suite) and the boundary re-audit clause, and `test-desiderata-and-boundaries` to name the gold-plating misread and the connascence of a mock in one line each, so that slicing guidance lives where boundaries are drawn. | Medium | Open | [build] | no |
| FR-009 | Curator profile update | As a curator, I want `doctrine-daphne` to state, once: assets live under the pack's `assets/` (a category subdirectory allowed) with a `<file>.asset.yaml` sidecar, declared as an asset node; anti-patterns are declared as nodes, are `rejects` targets and emit no edges; worked examples are referenced from the good artefacts; every resolved-only node needs an inbound edge, so that the canonical structure is pinned. | Medium | Open | [build] | no |
| FR-010 | Vertical slices in the TDD tactic | As an implementer, I want `tdd-red-green-refactor` (id unchanged) to state the loop as red then green, one behaviour, one failing test, one minimal implementation per cycle, each test a tracer bullet through the public interface at seams agreed before testing; to name horizontal slicing (all tests first, then all code) and tautological expected values as anti-patterns; and to hand refactoring to green mode, with attribution to mattpocock/skills at commit `abeeaf9` and only verified paths, so that test-first guidance carries the tracer-bullet rules. | High | Open | [build] | no |
| FR-011 | Green-mode refactoring | As an implementer, I want refactoring defined once as green mode (switch in only on a green suite, inside or outside a TDD cycle), owned by `disciplined-refactoring-cycle`, with `tdd-red-green-refactor`, `test-first-cycle`, `acceptance-test-first` and the testing pack's `test-first-bug-fixing` pointing to it instead of restating refactor steps, and edges from the TDD surfaces to the procedure and to the refactoring catalog, so that refactoring is its own interconnected technique. | High | Open | [build] | no |
| FR-012 | Vertical-skeleton-first tactic | As a planner, I want a planning-analysis tactic `vertical-skeleton-first` per #147 with the 2026-11-12 cuts (no gates-on-SHA, no per-class repair rule beyond a pointer, no review-narrowing rule, mission-199 specifics only in notes, the four-hour threshold a heuristic) and the five spine-event bounds (pause scope, one re-run within the recorded smoke budget, escalation cap, flaky smoke is no measurement, the integration owner classifies), so that integration order has guidance. The directive half stays deferred. | High | Open | [build] | no |
| FR-013 | Spine pointer in plan and tasks | As a planner, I want one line in the software-dev plan and tasks guidance asking whether the mission has a cross-owner spine (name it and its first composed path, see `vertical-skeleton-first`), and the tactic linked from `product-coherence-review` (whose notes ask for a vertical-slice tactic to cite), so that the tactic is reached when slicing happens. | Medium | Open | [build] | no |
| FR-014 | Coordinated tracer-bullet vocabulary | As a reader, I want foundation glossary terms "tracer bullet", "horizontal slicing", "spine", "green mode" and "no measurement", used with the same meaning by FR-010, FR-011, FR-012 and FR-015 (the glossary defines each term; the owning artefacts use it), so that the test-scale and mission-scale wording agree. | Medium | Open | [build] | no |
| FR-015 | Measurement discipline tactic | As an implementer sharing a machine, I want a testing tactic for multi-agent test measurement (cap concurrent heavy suites per machine; a killed, timed-out, out-of-memory or piped run whose exit status is lost is no measurement; test temp and cache paths on storage with enough quota; attribute a red by re-running it on the mission's recorded base commit), linked from `no-parallel-duplicate-test-runs`, scoped to implement and review, with host specifics (ports, quotas, make targets) only in the internal pack by pointer, so that agents stop reading contended runs as results. | High | Open | [build] | no |
| FR-016 | Core residue removed from the fold-in files | As a consumer, I want the provenance comment at the end of DIRECTIVE_034 removed and `testing-principles` free of core PR and commit numbers and core symbols (the literal-scan story and the frozen-gate-key example), keeping each rule, so that the #273 and #274 parts for these files are done. | Medium | Open | [build] | no |
| FR-017 | Release surface | As a consumer, I want the changed packs versioned per DIRECTIVE_018 (minor for the foundation lockstep set and built-in, and for each changed org pack), digests, manifests and the built-in digest constant restamped, pack reference pages regenerated, docs freshness kept and a changelog entry, so that the release surface reflects the change. | High | Open | [evidenced-by-run] | n/a -- evidence: the digest, manifest, pack-reference and freshness gates |

### Non-Functional Requirements

| ID | Title | Requirement | Category | Priority | Status |
|----|-------|-------------|----------|----------|--------|
| NFR-001 | Gates green | `validate-packs.sh`, `pytest tests`, `check_vocabulary.py`, `gen_pack_reference.py --check`, `check-pack-digests.sh` and `check_docs_freshness.py --base origin/main` exit 0; the charter-service check and the charter drift test pass in CI. | Reliability | High | Open |
| NFR-002 | Software-dev content stays ASCII | 0 non-ASCII characters in changed software-dev mission files (`tests/ci/test_software_dev_ascii.py` passes). | Compatibility | High | Open |
| NFR-003 | No consumer-pack core references | 0 Spec Kitty core issue numbers, PR numbers, commit hashes, core symbols or core paths in new or changed consumer-pack content; mission-199 detail only in the tactic's `notes`. | Portability | High | Open |
| NFR-004 | One canonical home per idea | Each new idea is fully stated in exactly 1 artefact (mindset -> paradigm; smells -> anti-pattern nodes; desiderata list and Quad-A skeleton -> their assets; vertical slices -> `tdd-red-green-refactor`; green mode -> `disciplined-refactoring-cycle`; spine -> `vertical-skeleton-first`; measurement -> the new tactic); any other surface uses at most one sentence and names the owner. | Maintainability | Medium | Open |
| NFR-005 | No orphan resolved-only nodes | 6 of 6 new resolved-only nodes (2 anti-patterns, 4 assets) have at least 1 inbound edge from an activatable artefact. | Maintainability | High | Open |

### Constraints

| ID | Title | Constraint | Category | Priority | Status |
|----|-------|------------|----------|----------|--------|
| C-001 | Charter alignment | Validate against the charter pin in `charter.lock.yaml`; core compatibility does not block or reshape the work (AGENTS.md). | Technical | High | Open |
| C-002 | Pack tiers | Paradigm, anti-pattern nodes and exemplar assets in foundation (with DIRECTIVE_041 and DIRECTIVE_054); checklist assets and the measurement tactic in testing; `vertical-skeleton-first` in planning-analysis (operator ruling of 2026-11-12); house specifics only in internal. A cross-pack edge is authored in the depending pack's graph. | Business | High | Open |
| C-003 | Stable ids | No existing id is renamed: `tdd-red-green-refactor` keeps its id; DIRECTIVE_041 keeps id, title, enforcement and rules. | Technical | High | Open |
| C-004 | No new directive | #147's directive half stays deferred; this mission adds no directive, so no directive number is taken. | Business | High | Open |
| C-005 | Graph conventions | New edges carry `when` (or `reason` on `rejects`); at most one edge per unordered pair per pack (edge-identity test); no inline `references:` block is created or grown. | Technical | High | Open |
| C-006 | Verified citations | Upstream citations name only paths verified at mattpocock/skills `abeeaf9` (`skills/engineering/tdd/SKILL.md`, `tests.md`, `mocking.md`, `skills/engineering/codebase-design/SKILL.md`); the slicing exemplar cites the Clear Test Boundaries page. | Business | High | Open |
| C-007 | Out of scope | The DIRECTIVE_052-successor prove-composition directive (#147); the other files of #273 and #274; beyond the green-mode links, these refactoring follow-ups: merging the refactoring pack's `refactoring` procedure with `disciplined-refactoring-cycle`, edges from the profiles' `refactoring` modes to green mode, and a smell-to-tactic map of the catalog; tooling that enforces the concurrency cap. | Business | Medium | Open |
| C-008 | Parallel mission | Mission D (`citation-and-docs-writing`) overlaps only in the foundation digest and the version restamp; rebase and restamp after whichever merges first. | Technical | Medium | Open |

### Key Entities

- **Paradigm** `tests-as-scaffold-not-friction`: the mindset; refined by DIRECTIVE_041 and DIRECTIVE_054.
- **Anti-pattern node**: a resolved-only graph node naming a smell; a `rejects` target that emits no edges.
- **Asset**: a resolved-only Markdown blob with a sidecar, reached through inbound `requires`/`suggests` edges.
- **Tracer bullet**: a thin path through the real system, end to end, kept and grown; at test scale one test through the public interface, at mission scale the spine's first composed path.
- **Spine**: the cross-owner flow whose composed success retires the most integration risk, with its transition matrix.
- **Green mode**: the state in which refactoring is allowed: the suite is green and no behaviour changes.
- **No measurement**: a test run whose outcome cannot be trusted (killed, timed out, out of memory, exit status lost); neither pass nor fail.

## Assumptions

- The core artefact-series proposal is the design source; its DIRECTIVE_047 and remediation procedure were delivered by the first test-doctrine mission as DIRECTIVE_054 and `unfake-an-over-mocked-test`. Its asset ids are adapted: the core-incident exemplar becomes the neutral `exemplar-unfake-an-over-mocked-test` (#273, #274).
- `refines` is a first-class relation in the pinned charter contract; the paradigm is a valid `refines` target.
- Versioning is minor (DIRECTIVE_018): the 041 split keeps every rule, and the other changes add guidance or point to existing owners.
- Issue claims (comments and labels on the tracker) are left to the dispatcher; the issue matrix records each issue.
- #216 closes with this mission; #154, #147 (tactic half; the directive half stays deferred on it), and #152 close; #273 and #274 stay open for their other files.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 1 paradigm carries the tests-as-scaffold mindset and 2 directives refine it; DIRECTIVE_041's rules are unchanged. — [build] · no-op passable: no
- **SC-002**: 6 new resolved-only nodes (2 anti-patterns, 4 assets), each with at least 1 inbound edge. — [build] · no-op passable: no
- **SC-003**: The twelve desiderata and the Quad-A skeleton each appear in full in exactly 1 artefact. — [build] · no-op passable: no
- **SC-004**: 0 TDD surfaces carry their own refactoring steps; each of the 4 named in FR-011 points to green mode. — [build] · no-op passable: no
- **SC-005**: 1 `vertical-skeleton-first` tactic reachable from the plan and tasks guidance and from `product-coherence-review`; 5 glossary terms define the shared vocabulary. — [build] · no-op passable: no
- **SC-006**: 1 measurement tactic reachable at implement and review; 0 host-specific ports, quotas or make targets in testing. — [build] · no-op passable: no
- **SC-007**: All gates in NFR-001 green at the PR head. — [evidenced-by-run] · no-op passable: n/a -- evidence: the CI run on the PR head
