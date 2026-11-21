# Research: Test doctrine 2

## R1 — Source of the #216 residue

- **Decision**: build from the core `docs/plans/doctrine/test_quality/doctrine-artefact-series-proposal.md` (spec-kitty/spec-kitty, read at HEAD `51e5783d`) and its companion research note, taking only what the first test-doctrine mission did not deliver.
- **Rationale**: the proposal is the operator-endorsed design; its directive and remediation procedure already shipped as DIRECTIVE_054 and `unfake-an-over-mocked-test`.
- **Alternatives considered**: a fresh design (rejected: duplicates settled curation work).

## R1b — Reachability of the paradigm and the new edge kinds

- **Finding**: the charter cascade crosses exactly `Rc = {requires, suggests, refines, scope, instantiates, enhances}` (charter `docs/architecture/composition-and-activation-rules.md`, W19), so `DIRECTIVE_041 --refines--> paradigm` and `DIRECTIVE_054 --refines--> paradigm` pull the paradigm whenever either directive is in force; 054 is scoped to the software-dev implement and review actions. `rejects` is not crossed: anti-pattern nodes are named targets, not context.
- **Endpoint check**: charter ADR-0077 decision 5 allows `refines` G -> G and `rejects` G -> anti_pattern, where G covers directive, tactic, styleguide, toolguide, paradigm and procedure; so directive/procedure/tactic/paradigm `rejects` edges and directive -> paradigm `refines` edges are valid. A `refines` edge already exists in foundation (`tactic.graph.yaml`, five-paradigm-parallel-debugging).
- **Proposal edges**: `paradigm --requires--> test-desiderata-and-boundaries` (testing fragment) and `--suggests--> connascence-analysis` (architecture fragment) are authored; `--suggests--> testing-principles` is dropped because the desiderata styleguide already reaches it.

## R2 — Pack tier of each new artefact

- **Decision**: paradigm, anti-pattern nodes and exemplar assets in foundation; checklist assets in testing; `vertical-skeleton-first` in planning-analysis; measurement tactic in testing; house specifics in internal.
- **Rationale**: foundation depends on no pack, so the mindset and smells sit next to 041 and 054 there; the checklists belong with the testing styleguides that own them; the 2026-11-12 ruling on #147 names planning-analysis. Cross-pack edges are authored in the depending pack (precedent: testing already authors 27 `foundation::`-sourced edges).
- **Alternatives considered**: paradigm in testing beside BDD and SbE (rejected: a foundation-only consumer would load 041 without its mindset).

## R3 — Quad-A asset vs the existing styleguide

- **Decision** (operator, 2026-11-21): asset `quad-a-test-structure` holds the language-neutral skeleton and a review checklist; `quadruple-a-test-format` keeps its principles and language examples and requires the asset; python, java and typescript cut their restated definition to a pointer and require the asset.
- **Rationale**: the styleguide was added after the core proposal; the operator kept the asset and made it the skeleton/checklist owner.

## R4 — Exemplars without core incidents

- **Decision**: the core #2934 exemplar becomes `exemplar-unfake-an-over-mocked-test`, a full before/after of the neutral order-fulfilment example already in the procedure; the user-registration slicing case comes from the Clear Test Boundaries page (https://patterns.sddevelopment.be/practices/define_test_boundaries/), not from Spec Kitty.
- **Rationale**: #273/#274 forbid core numbers, symbols and incidents in consumer packs.

## R5 — Upstream re-grounding for #154

- **Decision**: cite mattpocock/skills commit `abeeaf95660ba9e8b7c753eb38f441ca707a8823` and only these verified paths: `skills/engineering/tdd/SKILL.md`, `skills/engineering/tdd/tests.md`, `skills/engineering/tdd/mocking.md`, `skills/engineering/codebase-design/SKILL.md`. Upstream is MIT.
- **Findings**: the tdd skill now holds the vertical-slice/tracer-bullet rule, the horizontal-slicing and tautological-test anti-patterns, "test only at pre-agreed seams", and "refactoring is not part of the loop". `codebase-design` holds "the interface is the test surface". `deep-modules.md`, `interface-design.md` and `refactoring.md` are gone.
- **Divergence handled**: upstream's mocking list ("databases sometimes", "file system sometimes") is looser than DIRECTIVE_054; 054 stays the owner and the tactic cites it, not upstream's list.

## R6 — Refactoring out of the loop

- **Decision** (operator, 2026-11-21): follow upstream; refactoring is green mode, owned by the existing `disciplined-refactoring-cycle` procedure under `DISCIPLINED_REFACTORING`, reachable from the TDD surfaces and linked to the refactoring catalog procedure.
- **Feasibility of a full extraction**: the "own set of interconnected artefacts" already largely exists (directive, procedure, the refactoring pack's catalog procedure, 18 refactoring tactics, 7 anti-pattern smells). This mission wires the TDD surfaces into it and defines green mode once; mapping every catalog smell to its tactics is recorded as a follow-up (C-007).
- **Kept**: the tactic id `tdd-red-green-refactor` (C-003); "red-green-refactor" in profile prose names the practice and stays.

## R7 — #147 shape

- **Decision**: tactic only, with the 2026-11-12 dialectical cuts and five spine-event bounds; no directive (C-004), so no directive number is taken.
- **Rationale**: operator ruling recorded on #147 and restated 2026-11-21.

## R8 — #152 shape

- **Decision**: a sibling testing tactic `shared-machine-test-measurement`, suggested by `no-parallel-duplicate-test-runs`, scoped to implement and review; QA_003 (qa pack) is cited in prose only when it is reachable, otherwise described generically; host specifics go to internal `targeted-mission-test-run` as a pointer.
- **Rationale**: extending `no-parallel-duplicate-test-runs` would mix a per-suite rule with machine-wide measurement honesty.

## R9 — Versioning

- **Decision**: minor. Foundation lockstep set (foundation, writing, testing, refactoring, architecture, planning-analysis) and built-in to their next minor; python, java, javascript, pack-authoring and internal to their next minor.
- **Rationale**: DIRECTIVE_018; 041 keeps every rule; the rest adds guidance.

## R10 — Post-tasks squad (doctrine coherence), dispositions

1 refines reachability: resolved by R1b (charter W19). 2 endpoints: verified (ADR-0077 d5); risk note corrected. 3 "seam" ambiguity: TDD tactic says "test surface (public interface)"; "seam" stays DIRECTIVE_054's term. 4 "side channel": narrowed to bypassing a public read interface the system offers. 5 restatement in the TDD tactic: replaced by `rejects` edges to both anti-patterns and one pointer; the "never on red" clause dropped. 6 green mode: the glossary defines it; the procedure owns the practice. 7 upstream review-stage placement: recorded as not adopted. 8 refactoring follow-ups: listed in C-007; edge `when` and tactic `purpose` rewording added. 9 US4 test amended. 10 testing-principles Fast/Isolated/Specific: cut to a pointer to the checklist. 11 "no measurement": a glossary term both tactics use. 12 proposal edges: authored or recorded in R1b. 13 anti-pattern reachability: inbound `rejects` counts for NFR-005 (named target, never loaded as context). 14 shared files: WP03 and WP04 depend on WP02. 15 `kind: anti_pattern` on nodes.

## R11 — Post-tasks squad (brownfield), dispositions

1 lane collisions: WP03 and WP04 depend on WP02. 2 WP01 DoD counts 9 rejects edges. 3 refines precedent: corrected. 4 "binding rules": avoided in 041's intent. 5 measurement tactic scoped directly (no testing tactic is scoped today). 6 testing-principles overlap: cut to a pointer (WP02). 7 other Quad-A mentions: language examples and one-line phase mentions stay; recorded in WP02. 8 edge prose putting refactoring in the cycle: reworded in WP03; profile narratives stay. 9 DISCIPLINED_REFACTORING scope: amended so code just written is in scope once green (WP03). 10 tasks-outline layer-sliced example: reworked to vertical slices (WP03). 11 glossary is unsorted: terms placed beside related ones. 12 existing core references in touched files: out of scope, recorded. 13 255-character principle limit named in WP01.
