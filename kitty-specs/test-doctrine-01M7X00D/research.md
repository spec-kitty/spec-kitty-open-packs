# Research: Test doctrine: mock boundary and red-first value

Sources: issues #216, #209, #151 and #218 (folded into #216); the core research note on mocking boundaries and test slicing, whose section 8 is superseded by its companion artefact-series proposal (both are background only; nothing from core paths or core issue numbers is copied into consumer packs, see #273); the post-spec squad (reviewer and curator lenses, 2026-11-20).

## R1. Owner map (NFR-004)

| Rule | Owner | Others say (one sentence, naming the owner) |
|------|-------|---------------------------------------------|
| Mock only at the responsibility boundary; the allow-list; the "pin a call contract on owned logic" anti-pattern; border substitutes keep the real contract | `DIRECTIVE_054` | `test-boundaries-by-responsibility`, `test-scaffolding-as-design-smell`, `black-box-integration-testing`, `function-over-form-testing`, `testing-select-appropriate-level`, DIRECTIVE_036, reviewer-renata, testing `test-desiderata-and-boundaries`, testing `testing-principles` |
| How to unfake an over-mocked test | `procedure:unfake-an-over-mocked-test` | DIRECTIVE_054 requires it |
| Red-first scope (lasting regression risk) and the evidence carve-out | `DIRECTIVE_034` | `acceptance-test-first`, `tdd-red-green-refactor`, `test-first-cycle`, implement prompt, `atdd-adversarial-acceptance`, internal surfaces |
| `[evidenced-by-run]` label, "when it fails, does that mean something is broken?", the six-month long-term-value question | `acceptance-criteria-non-vacuity` | spec template, specify prompt, review step 4b |
| Red shape that keeps collection working | `DIRECTIVE_034` (integrity rule, already present) | `red-first-bug-reproduction` cites it |
| Record the failure text; invert a characterization test that pins the defect; strict expected failure across work packages | `red-first-bug-reproduction` | testing `test-first-bug-fixing`, DIRECTIVE_041, `observable-contract-test-authoring`, reviewer-renata |
| Spec Kitty CI-workflow worked example | internal tactic `spec-kitty-ci-workflow-evidence-exemplar` | internal procedures and skill |

## R2. Surface inventory (from the post-spec squad, verified)

Unconditional red-first wording to align:
- `packs/foundation/directives/034-test-first-development.directive.yaml:13,14,17`
- `packs/foundation/directives/039-lynn-cole-engineering-culture.directive.yaml:15` and its graph edge reason at `directive.graph.yaml:309`
- `packs/foundation/procedures/test-first-cycle.procedure.yaml` (description "Drive every production change from a failing test", exit condition, step 2)
- `packs/foundation/tactics/testing/tdd-red-green-refactor.tactic.yaml:25` ("block merge when new code has no corresponding tests")
- `packs/foundation/tactics/testing/acceptance-test-first.tactic.yaml` (purpose, step 1)
- `packs/foundation/missions/software-dev/steps/implement.prompt.md:14,159`
- `packs/testing/tactics/testing/atdd-adversarial-acceptance.tactic.yaml` (triage step)
- internal: `procedures/cloud-session-dispatch.procedure.yaml:33,39`, `skills/mission-from-issue.skill.md:13`, `procedures/landing-contributor-prs.procedure.yaml:43`

Seam lists and mocking rules to align:
- `packs/foundation/tactics/testing/test-boundaries-by-responsibility.tactic.yaml:17` ("DO mock/stub ... services outside the current module")
- `packs/foundation/tactics/testing/test-scaffolding-as-design-smell.tactic.yaml:5-8`
- `packs/foundation/tactics/testing/black-box-integration-testing.tactic.yaml:77`
- `packs/foundation/tactics/testing/function-over-form-testing.tactic.yaml:57`
- `packs/foundation/tactics/testing/testing-select-appropriate-level.tactic.yaml:13,20`
- `packs/foundation/agent_profiles/reviewer-renata.agent.yaml:154`
- `packs/foundation/directives/036-black-box-integration-testing.directive.yaml:20-21,27-29`
- `packs/testing/styleguides/test-desiderata-and-boundaries.styleguide.yaml:50,55-56,245-248`
- `packs/testing/styleguides/testing-principles.styleguide.yaml:26-27,134-138`

xfail and deletion rules to reconcile:
- `packs/foundation/directives/041-tests-as-scaffold-not-friction.directive.yaml:18,23`
- `packs/foundation/procedures/observable-contract-test-authoring.procedure.yaml:16`
- `packs/foundation/agent_profiles/reviewer-renata.agent.yaml:132`
- `packs/testing/procedures/test-first-bug-fixing.procedure.yaml:23-25,35-37`

Language profiles ("tests before production code", python, java, rust, go, drupal, javascript) describe product code and stay as they are.

## R3. Graph edge map

Decision: hand-edit the graph files (no generator exists; the `generated_by: drg-migration-v1` headers are frozen labels). One edge per unordered pair per pack (`tests/ci/test_graph_edge_identity.py`).

Foundation (`packs/foundation/*.graph.yaml`):
- nodes: `directive:DIRECTIVE_054` (directive.graph.yaml), `procedure:unfake-an-over-mocked-test` (procedure.graph.yaml)
- `directive:DIRECTIVE_054 --requires--> directive:DIRECTIVE_041`
- `directive:DIRECTIVE_054 --requires--> procedure:unfake-an-over-mocked-test` (with `when`/`reason`)
- `directive:DIRECTIVE_054 --suggests--> tactic:test-boundaries-by-responsibility`
- `directive:DIRECTIVE_054 --suggests--> tactic:function-over-form-testing`
- `directive:DIRECTIVE_036 --requires--> directive:DIRECTIVE_054`
- `procedure:unfake-an-over-mocked-test --suggests--> procedure:observable-contract-test-authoring`
- `procedure:unfake-an-over-mocked-test --requires--> tactic:test-boundaries-by-responsibility`
- `action:software-dev/implement --scope--> directive:DIRECTIVE_054`; `action:software-dev/review --scope--> directive:DIRECTIVE_054`
- `agent_profile:reviewer-renata --requires--> directive:DIRECTIVE_054`; `agent_profile:implementer-ivan --suggests-->`; `agent_profile:generic-agent --suggests-->` (with `when`/`reason`, as the 034 and 041 edges)
- no new 034-041 edge: `DIRECTIVE_041 --requires--> DIRECTIVE_034` already exists.

Cross-pack (fragments, `foundation::` URNs):
- qa `drg/fragment.yaml`: `agent_profile:qa-test-designer-tessa --suggests--> foundation::directive:DIRECTIVE_054`
- internal `drg/fragment.yaml`: the new tactic node and `tactic:spec-kitty-ci-workflow-evidence-exemplar --refines--> foundation::tactic:acceptance-criteria-non-vacuity`, following the sibling `spec-kitty-gate-non-vacuity-exemplar` precedent (node entry plus a `refines` edge, no inbound edge).

No `tension` edge is needed: DIRECTIVE_041's text is reconciled directly. `refines` is valid at the pin; it is used only for the internal exemplar, as its sibling does.

Existing reason to reword: `DIRECTIVE_039 requires procedure:test-first-cycle` ("Starts every production change from a failing test").

Alternatives considered: `054 refines 041` (curator suggestion). Rejected for `requires`, which matches the house directive-to-directive pattern (036 requires 034, 041 requires 034) and pulls 041 in wherever 054 is scoped.

## R4. Versioning (DIRECTIVE_018)

Decision: minor. DIRECTIVE_054 codifies what DIRECTIVE_036 ("must not patch ... inside-boundary collaborators"), DIRECTIVE_041 ("mocked-out behavior") and `test-boundaries-by-responsibility` already require, and DIRECTIVE_034 is loosened. Conforming work does not stop conforming. Nothing is removed or renamed.

- Foundation lockstep (foundation, writing, testing, refactoring, architecture, planning-analysis): 3.1.0 -> 3.2.0; exact `==3.1.0` pins move to `==3.2.0`.
- built-in: 5.1.0 -> 5.2.0.
- qa: 5.0.0 -> 5.1.0 (new edge); internal: 4.1.0 -> 4.2.0 (new tactic). Their `>=2.0,<4` ranges still admit 3.2.0.
- cave-kitty or other packs pinning the lockstep exactly move with it (follow precedent commit `6dce39c`).
- qa narrows its foundation range to `>=3.2,<4` (its new edge needs 054). Sidecars hold only `tree_digest`.
- Restamp: `validate_pack_schemas.py --derive-manifest` for changed packs, `pack_digest.py --update <pack>`, `BUILT_IN_DIGEST` in `tests/ci/test_pack_digest.py`, `gen_pack_reference.py` pages.

Alternative: major (4.0.0), on the reading that a new rule tightens. Rejected: it would break about 12 packs' `<4` ranges for a rule that is already in force through 036/041.

## R5. Glossary

Terms go in `packs/foundation/glossaries/spec-kitty-core.glossary.yaml` (`id`, `name`, `definition`, `status`, optional `aliases`, `see_also`), following `characterization-test`. `test_glossary_content.py` rejects `#NNN`, `ADR-N`, `.py`, `FR-NNN`, `tests/`, `src/` in definitions.

## R6. Vocabulary guard

`check_vocabulary.py` refuses self-binding phrasing ("this directive is required/binding/mandatory", "remains advisory", "enforcement `required`"). Directive bodies say what to do; the `enforcement:` field carries the level.
