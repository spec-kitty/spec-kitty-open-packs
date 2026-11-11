# Lens B: doctrine curation of the opt-in org bundles (#73 squad)

Read-only research. open-packs `packs/built-in/` at `5c489d6`; charter at `fb24052`. Inputs: the census and design notes,
ADR-0048 (d13, d14), ADR-0052, ADR-0053 (d1, d3, d9, d29a), `docs/packs/catalog-proposal.md`, issues #1–#16 and #190
(read via the REST API), the YAML of every one of the 217 staging nodes (title, description, scope; graph-only nodes from
their graph entries and referrers), and the precomputed `edges.json`, `delegates.json`, `profrefs.json`.
Appendix: `B-bundles.json` (bundle → URNs, a reason per URN, and the proposed `depends_on`).

## 1. Verdict in brief

- **Ten org bundles, plus small returns to the members and three cuts.** The bundles are `core-engineering` (52),
  `refactoring` (35), `architecture` (35), `testing` (20), `planning-analysis` (14), `javascript` (13),
  `pack-authoring` (7), `git-delivery` (6), `adversarial-review` (5), and the stacks `python` (5), `java` (4) and
  `drupal` (4). Also: 11 nodes return to `writing`, 3 to `foundation`, and 3 are cut candidates. That accounts for all 217.
- **The largest finding: about a quarter of staging is foundation's own "how-to" layer.** 34 procedures are each the
  `requires` target of a foundation directive (029 → agent-commit-signing, 024 → keep-change-local, and so on). Add their
  toolguides and tactics and you get 52 nodes and 57 edges from foundation into them. They are not specialist content.
  I group them as one bundle, `core-engineering` (the catalog's #1 name), so that the operator's open question 6 can be
  answered with **one** move: keep the bundle opt-in, or fold it back into foundation whole.
- **The DAG works.** All 535 cross-bundle graph edges either point down the proposed `depends_on` closure (368) or can
  be relocated into the depending pack's graph (167). Only the cuts' own edges (23) are left over. The hard breaks are
  the five body references below (D1–D5). They cannot be relocated, so they need a ruling.
- **Two corrections to rulings already taken.** (a) gherkin and the mutation-testing cluster belong in `testing`, not
  `qa`. (b) `java` (#5) cannot depend on foundation alone: java-jenny `requires` test-first-bug-fixing and
  bdd-scenario-formulation, which are in `testing`. The same holds for python, drupal and javascript.

## 2. Grounding: what the charter intends a bundle to be

- ADR-0048 d13: foundation keeps "the cross-cutting directives, paradigms, glossary, base templates and assets, the
  shipped mission types and their step contracts, and the base agent profiles". d14: stack packs are opt-in. d9:
  specialist packs only add. d11: topical packs are full top-level packs.
- ADR-0053 d1: our opt-in packs are `org`. d3: built-in = foundation + writing. d7: cross-pack references are
  `<pack>::<urn>` and must lie in the referrer's `depends_on` closure. d22, with ADR-0066: a pack plugs into another
  pack's step through a **step enhancement** (guards, emits, prompt fragments, plus `enhances` and graph edges). That is
  the tool for re-attaching a bundle to a foundation step whose step-contract candidate is deleted.
- ADR-0052 AP3: "an anti-pattern lives in the pack whose guidance rejects it". d29a: situational-assessment,
  legacy-codebase-triage, bdd-scenario-lifecycle, drill-down-documentation and documentation-gap-prioritization are to be
  re-homed during curation.
- Catalog principle 2: "a pack is a slice a team would adopt *as a unit*, not an alphabetical bucket." I used it as the
  test for every bundle. A bundle needs one audience and a lead profile, or else a single rule that explains its contents.

## 3. Proposed bundles

All are `pack_level: org`. "F" = foundation and "W" = writing (both built-in members).

| Bundle | Purpose | Audience (who opts in) | Members by kind | Lead profile(s) | depends_on | Counterpart |
|---|---|---|---|---|---|---|
| `core-engineering` | The how-to layer under foundation's directives: the procedure, toolguide or tactic each foundation directive `requires`, plus generic engineering-practice tactics | Every team that wants the foundation directives to come with their procedures; in practice almost everyone | procedure 35, tactic 12, toolguide 3, directive 1, styleguide 1 | none (implementer-ivan and reviewer-renata in F use it) | F, W | catalog #1 `core-engineering` (as a how-to layer, not as the base) |
| `testing` | Developer test discipline: test-first, BDD/SbE, test design styleguides, defect diagnosis | Teams practising TDD/BDD; a prerequisite for the stack packs | tactic 8, procedure 5, styleguide 4, paradigm 2, agent_profile 1 (+5 proposed from qa) | debugger-debbie | core-engineering | catalog #3 `test-and-bdd`; census "testing extras fold into qa" |
| `refactoring` | Behaviour-preserving restructuring: the refactoring catalog, semantic compression, and the code smells they remove | Teams paying down legacy or bloat | tactic 25, anti_pattern 7, paradigm 1, procedure 1, agent_profile 1 | randy-reducer | testing (and core-engineering through it) | census `refactoring`; catalog #10 |
| `architecture` | DDD (strategic and tactical), deep modules, C4 modelling, architecture-scout review | Teams designing or evolving systems with DDD/C4 | tactic 14, anti_pattern 6, template 5, paradigm 3, procedure 3, agent_profile 2, directive 1, styleguide 1 | architect-alphonso, paula-patterns | refactoring, adversarial-review, W | census `architecture (with DDD)`; catalog #2 + #7 |
| `planning-analysis` | Pre-design context and backlog work: situational assessment, legacy triage, decision interview, spikes, issue triage, plan styleguide | Planners, researchers, brownfield onboarding | procedure 5, template 5, agent_profile 2, styleguide 1, tactic 1 | planner-priti, researcher-robbie | architecture, git-delivery, adversarial-review | catalog #13, with #12 brownfield merged in |
| `adversarial-review` | Adversarial squads, arch-gate adjudication, gate non-vacuity, shrink-only ratchet | Teams running multi-lens review and architectural gates | procedure 2, tactic 3 | none (reviewer-renata, in F, requires the squad procedure) | testing | catalog #11 |
| `git-delivery` | Optional branching models and PR or worktree hygiene | Teams on git-flow or trunk-based development, or with heavy PR workflows | paradigm 1, procedure 1, tactic 2, toolguide 2 | none | core-engineering | catalog #9 |
| `pack-authoring` | Onboarding external agents into packs, migrating guidance into a charter, skill authoring | Pack and charter authors | procedure 2, template 3, agent_profile 1, styleguide 1 | doctrine-daphne | core-engineering, W | census `pack-authoring`; catalog #15 |
| `javascript` | Node and browser stack: TS/HTML/CSS conventions, atomic design, JS supply chain, Stryker | JS/TS teams, both front and back end | agent_profile 3, tactic 4, styleguide 3, toolguide 2, paradigm 1 | node-norris, frontend-freddy, designer-dagmar | testing | census `javascript`; catalog #6 |
| `python` | Python conventions, review checks, supply chain, mutmut | Python teams | agent_profile 1, styleguide 1, toolguide 3 | python-pedro | testing | census; catalog #4 |
| `java` | Java conventions, Maven review checks, supply chain | Java teams | agent_profile 1, styleguide 1, toolguide 2 | java-jenny | testing (**not foundation only**, see §5) | #5 |
| `drupal` | Drupal conventions, security and performance, review checks | Drupal teams | agent_profile 1, styleguide 2, toolguide 1 | drupal-dries | testing | census `drupal` |

The proposed DAG has no cycles:
F ← W ← core-engineering ← {testing, git-delivery, pack-authoring}; testing ← {refactoring, adversarial-review, the stacks, qa};
refactoring ← architecture ← planning-analysis; `internal` → planning-analysis, adversarial-review, git-delivery, W;
`event-driven` → architecture (it cites reference-architectural-patterns and, in its catalog entry, DDD).

**Bundles under about 5 nodes, and what I did with them.**
- **Merged:** `brownfield-onboarding` (#12) into `planning-analysis`, because its paradigm is a cut candidate and
  forensic-repository-audit and reverse-speccing are already in F.
- **Kept small:** `java`, `drupal` and `adversarial-review`. A stack pack is named after its stack, which is a reason
  in its own right (#5). `adversarial-review` has exactly 5 nodes and a distinct audience; folding it into
  `core-engineering` is an acceptable alternative.
- **No `glossary` or `modelling` bundle.** Those nodes return to `writing` (D2).

## 4. Returns to the members, and the body-reference decisions

Graph edges can always be relocated. Body references (step-contract `delegates_to`, profile `*-references`) cannot.
After the split above, exactly five remain:

| # | Body reference | Breaks because | Recommendation |
|---|---|---|---|
| D1 | `software-dev/implement` → `toolguide:execution-lanes` | F → org | **Return execution-lanes to foundation.** It describes the default lane worktrees that `spec-kitty implement` creates. It is product mechanics, not an option. git-flow's own text says "the execution-lanes toolguide describes the supported lane worktrees". |
| D2 | `software-dev/implement` → `paradigm:trunk-based`, `procedure:git-flow` | F → org | Agree with the operator: delete both candidates and put them in `git-delivery`. If they should still reach the implement step when opted in, `git-delivery` adds a step enhancement (ADR-0053 d22). |
| D3 | `software-dev/specify` → `procedure:example-mapping-workshop` | F → org | Delete the candidate and re-attach it from `testing` with a step enhancement. This is a mild counter-argument: example mapping is a good specify technique, but it is BDD-specific. |
| D4 | `diagram-daisy` (W) `directive-references` `USE_C4_MODEL_TECHNIQUES` | W → org | Either drop the reference (daisy keeps mermaid and plantuml), or move the C4 sub-cluster (directive, paradigm, c4-diagram-authoring, 2 tactics, 3 templates) into `writing`. I prefer to drop it: census and catalog both file C4 under architecture. |
| D5 | `lexical-larry` (W) `tactic-references` terminology-extraction-mapping and context-boundary-inference | W → org | **Return the glossary-stewardship cluster to writing** (below). Dropping these references would gut larry's role. |

Not in scope, but found: `analyst-annie` (F seed) has a `directive-references` entry to `DIRECTIVE_047`, which is in
writing. That is an F → W body reference, and it breaks the foundation closure today.

**→ writing (11):**
- glossary stewardship: terminology-extraction-mapping, context-boundary-inference, code-documentation-analysis,
  glossary-maintenance-workflow, kitty-glossary-writing (scoped by every retrospect action, including writing's
  documentation/retrospect), contextive, glossary-template, and curator-carla (catalog #8);
- communication: stakeholder-alignment (`tactics/communication/*`, which the census sends to writing; scoped by
  documentation/discover), with its stakeholder-persona and system-context-canvas templates.

**→ foundation (3):**
- execution-lanes (D1);
- retrospective-facilitator, which every shipped `retrospect` step scopes; the catalog keeps "retrospective mechanics"
  in core;
- human-in-charge, the work-package workflow sentinel (a runtime concept; the census puts it in foundation).

## 5. qa (6) and internal (4), re-examined

- **gherkin → testing, not qa.** Its referrers are DIRECTIVE_034 (F), the BDD paradigm, bdd-scenario-lifecycle and
  bdd-scenario-formulation. None of them is a qa artifact. qa's own content (exploratory charters, defect triage,
  promise traceability) never mentions Gherkin.
- **Mutation-testing cluster** (directive USE_MUTATION_TESTING…, mutation-testing-review, mutation-aware-test-design,
  mutation-testing-workflow) **→ testing** is my recommendation; keeping it in qa is defensible but costly.
  - The directive is `suggests`ed by generic-agent, implementer-ivan and reviewer-renata (F), and by debbie, randy,
    jenny, pedro, norris and freddy.
  - In qa, each of python, java and javascript would have to depend on qa (the whole QA mission pack) to keep one
    `suggests` edge. The python-mutation-tools and typescript-mutation-tools toolguides would also be edge targets out
    of qa into the stacks.
  - In testing, the stacks already depend on it, so it costs nothing.
  - The census grouped these as "testing extras into qa" before any `testing` bundle existed. With `testing` in place,
    `qa` should `depends_on: testing` and keep its own QA-function content.
- **sonar → qa: agree.** Static analysis quality gate, suggested only by DIRECTIVE_030.
- **internal (4): agree** with census, catalog #16 and ADR-0053 d29.
  - Three edges into internal must be relocated into internal's graph: `software-dev/review` scope → mission-wrap-up-sequence (a shipped product step scoping a team-internal procedure, worth flagging),
    DIRECTIVE_030 → tiered-standards, and writing-audience-catalog → the agentic-framework-core-team audience.
  - The planning-and-tracking → tiered-standards edge moves the same way.
  - internal then depends on planning-analysis, adversarial-review (squad, arch-gate adjudication), git-delivery
    (clean-linear-commit-history) and testing (development-assist-test-cleanup). That matches catalog #16's
    `depends_on`.
- **java (#5): its body text says it depends on built-in only.** That is not enough under ruling 4. java-jenny
  `requires` procedure:test-first-bug-fixing and tactic:bdd-scenario-formulation, and `suggests` DISCIPLINED_REFACTORING
  and the mutation directive. java needs `depends_on: testing` (and core-engineering through it), or those edges must be
  dropped. The same applies to drupal-dries, python-pedro, node-norris and frontend-freddy.

## 6. Divergences from the census and the catalog

**From the census (work-breakdown "Foundation membership").**

Most "census said foundation" items are in staging because of the operator's strict one-hop ruling, not because of
this lens: the profiles alphonso, paula, priti, robbie, carla, debbie and dagmar; the paradigms DDD, SbE, BDD,
deep-module, trunk-based, execution-lanes and git-flow; the testing styleguides; boring-code-review; `testing/*`,
`security/*` and `code-patterns/*`. My own divergences:

| Item | Census | Mine | Reason |
|---|---|---|---|
| execution-lanes, retrospective-facilitator, human-in-charge | F | F (return) | Runtime mechanics of the shipped missions (D1, §4) |
| kitty-glossary-writing | F | W | Glossary stewardship cluster with lexical-larry; scoped by every retrospect step |
| contextive | architecture | W | A glossary tool (Contextive YAML is a projection of glossary contexts, ADR-0049); it sits with larry |
| DISCIPLINED_REFACTORING (+ its cycle) | F | core-engineering | Cross-cutting directive: under "all cross-cutting directives in F" it should be **F**; until then it sits beside the other how-tos |
| given-when-then-authoring | qa | testing | Required by the BDD procedures and tactic |
| gherkin, mutation cluster | qa | testing | §5 |
| designer-dagmar | F | javascript | UX/UI and design-system specialist; only requires 031; catalog #6 |
| html, css, typescript-conventions | (not in census) | javascript | Stack styleguides that freddy and norris require |
| deep-module-design, DDD paradigm, alphonso, paula, connascence, ammerse | F / analysis | architecture | Design-paradigm content; ammerse goes here because reference-architectural-patterns suggests it, which avoids an architecture ↔ planning cycle |
| chain-of-responsibility-rule-pipeline | F (code-patterns) | refactoring | Suggests only refactoring tactics |
| 13 graph-only anti-patterns | F (ADR-0052 d15: "seed the general set in the foundation pack") | topical (AP3) | Each is rejected only by DDD, C4 or refactoring guidance. **ADR-0052 d15 and AP3 disagree; d15 needs a ruling.** |
| New bundles `core-engineering`, `testing`, `git-delivery`, `planning-analysis`, `adversarial-review` | none | new (catalog names) | They exist because the strict foundation leaves their content out |

**From the catalog (#1–#16).**
- **#1:** this bundle holds no directives, which are all in F. It is the how-to layer, not "the base".
- **#2 + #7:** merged as `architecture`. mermaid and plantuml stay in W. dependency-hygiene, deepening-opportunity,
  interface-variation, problem-decomposition and language-driven-design are already in F.
- **#3:** 034, 036 and 041 are in F. development-bdd goes to architecture (alphonso requires it; its path is
  tactics/architecture). five-paradigm-parallel-debugging goes to core-engineering, because DIRECTIVE_040 requires it.
- **#6:** renamed `javascript` per the census and #73's "name a stack pack after the stack". interface-variation-design
  is in F.
- **#8 → writing:** the existing writing member plus the §4 returns.
- **#9:**
  - The directives 029, 033, 045 and 046 are in F, and their procedures are in core-engineering.
  - execution-lanes goes to F; issue-triage-state-machine to planning-analysis, because it `requires`
    disciplined-defect-diagnosis.
  - `tracker-organisation-workflow` and `shared-branch-ci` (listed in #9 and the census) do not exist in this
    built-in tree.
- **#11:** renata, 040, 043 and code-review-incremental are in F. `adversarial-squad-cadence` and
  `iterative-deepening-review` are not in built-in.
- **#12:** merged into planning-analysis (§3).
- **#13:**
  - tiered-standards, mission-tracer-files and mission-wrap-up go to internal.
  - premortem, moscow, eisenhower, requirements-validation, safe-to-fail and dialectic are already in F.
  - ammerse goes to architecture (DAG).
- **#15:**
  - 018 and 028 are in F; efficient-local-tooling is in core-engineering.
  - terminology-guard already lives in `internal`, and `rtk-search-tooling` does not exist.
  - doctrine-version-change is the how-to of DIRECTIVE_018, so it goes to core-engineering.
- **#16 internal, #14 spdd (done):** agree.
- **#17 event-driven:** its `depends_on` should name `architecture` (and F), not built-in.

## 7. Cut candidates and duplication clusters

**Cut:**
- `DIRECTIVE_039` "Lynn Cole Engineering Culture" is person-named. Its rules duplicate 001, 030 and 034 together with
  boring-code-review. `paradigm:deep-module-design` `requires` it; re-point that edge to 024 or 030.
- `procedure:small-explicit-code-shaping`: its only owner is 039. Cut it with 039, or re-parent it under 024 in
  core-engineering.
- `paradigm:brownfield-onboarding` is self-marked "DRAFT / PROVISIONAL (2026-05-08)". Its anti-patterns stay, because
  DDD and C4 reject them too. Its required items (forensic-repository-audit, legacy-codebase-triage) stay.

**Rename (person-named):** `tactic:paula-patterns-architecture-scout-review` embeds a profile name in a tactic id.
Rename it, for example to architecture-scout-review.

**Defects:** 16 templates and 13 anti-patterns exist only as graph nodes, with no file. Under ADR-0053 d31 the
anti-patterns need files (with `bad_example` and severity) or they are refused. Each template needs a file, or it should
be dropped.

**Overlaps to merge during curation** (all inside staging or touching it):
- **Refactoring discipline:** DISCIPLINED_REFACTORING, disciplined-refactoring-cycle, the refactoring procedure,
  tidy-first-campsite-clean, touched-area-cleanup (the census's "five"), with keep-change-local and
  change-scope-tension-resolution next to them.
- **Test-first:** test-first-cycle, red-first-bug-reproduction, test-first-bug-fixing, zombies-tdd, and F's
  tdd-red-green-refactor.
- **BDD:** the behaviour-driven-development paradigm, bdd-scenario-formulation, development-bdd,
  bdd-scenario-lifecycle, given-when-then-authoring.
- **Black-box:** 036, the black-box-integration-testing tactic (F), black-box-integration-test-design.
- **Debugging:** durable-fix-investigation, disciplined-defect-diagnosis, five-paradigm-structural-intervention.
- **Local tooling:** 028, local-tooling-selection, efficient-local-tooling.
- **Canonical source:** 044, canonical-source-discipline, canonical-source-unification.
- **Commit signing:** agent-commit-signing (procedure) and git-agent-commit-signing (toolguide).
- **Mutation testing:** the three (four) mutation artifacts.

**To re-home, not cut** (ADR-0052 d6 and d29a): spike-timebox-policy (becomes a directive), issue-triage-state-machine
(becomes a lifecycle), migrate-project-guidance and onboard-external-agent (become small mission types),
situational-assessment, legacy-codebase-triage, bdd-scenario-lifecycle and drill-down-documentation.

## 8. One `specialist-staging` pack, or carve now?

**For one holding pack:**
- It keeps #73 to the foundation/writing split and leaves the content decisions to one PR per bundle (curation is per
  artifact, ADR-0048 Consequences).
- Open rulings (D1–D5, core-engineering in or out, AP3 vs d15, qa vs testing) would otherwise fix pack names before
  they are decided. ADR-0053 makes pack names stable identifiers, and a rename breaks dependents.
- It gives the core upgrade step (ADR-0048) one opt-in that brings back everything the old built-in shipped.
- Inside one pack, no reference crosses a pack boundary, so the 167 relocations wait until the bundles exist.

**Against:**
- It rebuilds the monolith the catalog exists to remove ("why carve"), only now opt-in.
- `specialist-staging` becomes a name others depend on. Any pack carved early (java #5, rust and go are fine) whose
  profiles require testing or core-engineering content must `depends_on: specialist-staging`, and then repoint later.
  Every carve-out is a breaking change for anyone who opted in, and the upgrade path changes twice
  (built-in → staging → bundle).
- About a quarter of staging (core-engineering) is not specialist at all, so the name is wrong for it. Parking it hides
  the most important open question.

**Recommendation: a hybrid, carved in dependency order.**
1. Rule now on `core-engineering`: fold it into foundation, or carve it as an org bundle. Together with D1 this settles
   52 of the 217 nodes and 57 of the edge relocations.
2. Carve `testing` next, with gherkin and mutation from qa. It is the hub that every stack, `refactoring`,
   `adversarial-review` and `qa` depend on. Until it exists, every early carve-out has to point at staging.
3. Then the leaves, in parallel, one PR each: the stacks (java first, since #5 already exists), `pack-authoring`,
   `git-delivery`, `refactoring`.
4. Then `architecture` and `adversarial-review`, then `planning-analysis`.

Staging is a good interim step only for what is not yet carved, and only if it is documented as transitional and not
advertised to consumers.

## Appendix A: per-node assignment (217)

Each node, its proposed bundle and the one-line reason, generated from `B-bundles.json`.

#### ->foundation (3)

| Node | Reason |
|---|---|
| `agent_profile:human-in-charge` | workflow sentinel for WP assignment, a runtime concept; census foundation |
| `agent_profile:retrospective-facilitator` | scoped by every shipped retrospect step; catalog "retrospective mechanics stay in core" |
| `toolguide:execution-lanes` | delegated by software-dev/implement body; it IS the default lane workspace model, not an option |

#### ->writing (11)

| Node | Reason |
|---|---|
| `agent_profile:curator-carla` | knowledge-base and doctrine-docs curator (catalog #8 documentation-and-glossary) |
| `procedure:glossary-maintenance-workflow` | glossary stewardship cluster with lexical-larry; scoped by every retrospect action |
| `styleguide:kitty-glossary-writing` | glossary stewardship cluster with lexical-larry; scoped by every retrospect action |
| `tactic:code-documentation-analysis` | glossary stewardship cluster with lexical-larry; scoped by every retrospect action |
| `tactic:context-boundary-inference` | glossary stewardship: lexical-larry (writing) body-references these two tactics |
| `tactic:stakeholder-alignment` | tactics/communication/* (census -> writing); scoped by documentation/discover |
| `tactic:terminology-extraction-mapping` | glossary stewardship: lexical-larry (writing) body-references these two tactics |
| `template:glossary-template` | glossary stewardship cluster with lexical-larry; scoped by every retrospect action |
| `template:stakeholder-persona-template` | tactics/communication/* (census -> writing); scoped by documentation/discover |
| `template:system-context-canvas-template` | tactics/communication/* (census -> writing); scoped by documentation/discover |
| `toolguide:contextive` | glossary stewardship cluster with lexical-larry; scoped by every retrospect action |

#### adversarial-review (5)

| Node | Reason |
|---|---|
| `procedure:adversarial-squad-deployment` | catalog #11 adversarial review and gate adjudication |
| `procedure:post-merge-arch-gate-adjudication` | catalog #11 adversarial review and gate adjudication |
| `tactic:adversarial-qa-handoff` | catalog #11 adversarial review and gate adjudication |
| `tactic:architectural-gate-non-vacuity` | catalog #11 adversarial review and gate adjudication |
| `tactic:frozen-baseline-shrink-only-ratchet` | catalog #11 adversarial review and gate adjudication |

#### architecture (35)

| Node | Reason |
|---|---|
| `agent_profile:architect-alphonso` | lead profiles: system architect and architecture-scout reviewer |
| `agent_profile:paula-patterns` | lead profiles: system architect and architecture-scout reviewer |
| `anti_pattern:anemic-domain-model` | graph-only anti-pattern rejected by the DDD or C4 paradigm (AP3) |
| `anti_pattern:big-ball-of-mud` | graph-only anti-pattern rejected by the DDD or C4 paradigm (AP3) |
| `anti_pattern:big-upfront-design` | graph-only anti-pattern rejected by the DDD or C4 paradigm (AP3) |
| `anti_pattern:code-is-the-documentation` | graph-only anti-pattern rejected by the DDD or C4 paradigm (AP3) |
| `anti_pattern:database-driven-design` | graph-only anti-pattern rejected by the DDD or C4 paradigm (AP3) |
| `anti_pattern:single-diagram-architecture` | graph-only anti-pattern rejected by the DDD or C4 paradigm (AP3) |
| `directive:USE_C4_MODEL_TECHNIQUES` | C4 cluster (E-C4); see decision D3 on diagram-daisy |
| `paradigm:c4-incremental-detail-modeling` | C4 cluster (E-C4); see decision D3 on diagram-daisy |
| `paradigm:deep-module-design` | Ousterhout deep modules; scoped by plan mission (edge relocates) |
| `paradigm:domain-driven-design` | DDD paradigm and its required styleguide/tactics (E-DDD cluster) |
| `procedure:c4-diagram-authoring` | C4 cluster (E-C4); see decision D3 on diagram-daisy |
| `procedure:drill-down-documentation` | required by architect-alphonso; ADR-0053 d29a re-homes it as a styleguide rule |
| `procedure:event-storming-discovery` | DDD discovery workshop (catalog #2) |
| `styleguide:aggregate-design-rules` | DDD paradigm and its required styleguide/tactics (E-DDD cluster) |
| `tactic:aggregate-boundary-design` | DDD paradigm and its required styleguide/tactics (E-DDD cluster) |
| `tactic:ammerse-impact-analysis` | AMMERSE values impact analysis of architectural choices; suggested by reference-architectural-patterns |
| `tactic:anti-corruption-layer` | DDD paradigm and its required styleguide/tactics (E-DDD cluster) |
| `tactic:architecture-diagram-review-checklist` | C4 cluster (E-C4); see decision D3 on diagram-daisy |
| `tactic:bounded-context-canvas-fill` | DDD paradigm and its required styleguide/tactics (E-DDD cluster) |
| `tactic:c4-zoom-in-architecture-documentation` | C4 cluster (E-C4); see decision D3 on diagram-daisy |
| `tactic:connascence-analysis` | coupling taxonomy |
| `tactic:context-mapping-classification` | DDD paradigm and its required styleguide/tactics (E-DDD cluster) |
| `tactic:development-bdd` | tactics/architecture path, required by architect-alphonso |
| `tactic:domain-event-capture` | DDD paradigm and its required styleguide/tactics (E-DDD cluster) |
| `tactic:entity-value-object-classification` | DDD paradigm and its required styleguide/tactics (E-DDD cluster) |
| `tactic:paula-patterns-architecture-scout-review` | architecture-scout review recipe for paula-patterns |
| `tactic:reference-architectural-patterns` | reference-architecture selection; event-driven cites it (event-driven depends on architecture) |
| `tactic:strategic-domain-classification` | DDD paradigm and its required styleguide/tactics (E-DDD cluster) |
| `template:ammerse-analysis-template` | AMMERSE values impact analysis of architectural choices; suggested by reference-architectural-patterns |
| `template:bounded-context-canvas-template` | graph-only templates of DDD canvas / C4 tactics |
| `template:c4-component-mermaid-template` | graph-only templates of DDD canvas / C4 tactics |
| `template:c4-container-mermaid-template` | graph-only templates of DDD canvas / C4 tactics |
| `template:c4-context-mermaid-template` | graph-only templates of DDD canvas / C4 tactics |

#### core-engineering (52)

| Node | Reason |
|---|---|
| `directive:DISCIPLINED_REFACTORING` | cross-cutting directive (census foundation; seeds generic-agent and implementer-ivan suggest it) and its how-to; flagged for foundation under the "all cross-cutting directives" rule |
| `procedure:agent-commit-signing` | how-to procedure `requires`d by foundation directive 029; kept beside its siblings so the whole layer can fold back into foundation in one move |
| `procedure:agent-self-declaration` | how-to procedure `requires`d by foundation directive 049; kept beside its siblings so the whole layer can fold back into foundation in one move |
| `procedure:black-box-integration-test-design` | how-to procedure `requires`d by foundation directive 036; kept beside its siblings so the whole layer can fold back into foundation in one move |
| `procedure:bounded-context-alignment` | how-to procedure `requires`d by foundation directive 031; kept beside its siblings so the whole layer can fold back into foundation in one move |
| `procedure:bulk-edit-occurrence-mapping` | how-to procedure `requires`d by foundation directive 035; kept beside its siblings so the whole layer can fold back into foundation in one move |
| `procedure:canonical-source-discipline` | how-to procedure `requires`d by foundation directive 044; kept beside its siblings so the whole layer can fold back into foundation in one move |
| `procedure:change-scope-tension-resolution` | how-to procedure `requires`d by foundation directive RECONCILE_CHANGE_SCOPE_TENSIONS; kept beside its siblings so the whole layer can fold back into foundation in one move |
| `procedure:component-boundary-definition` | how-to procedure `requires`d by foundation directive 001; kept beside its siblings so the whole layer can fold back into foundation in one move |
| `procedure:credential-exposure-prevention` | how-to procedure `requires`d by foundation directive 050; kept beside its siblings so the whole layer can fold back into foundation in one move |
| `procedure:decision-record-keeping` | how-to procedure `requires`d by foundation directive 003; kept beside its siblings so the whole layer can fold back into foundation in one move |
| `procedure:defect-class-construction-gate` | how-to procedure `requires`d by foundation directive 043; kept beside its siblings so the whole layer can fold back into foundation in one move |
| `procedure:disciplined-refactoring-cycle` | cross-cutting directive (census foundation; seeds generic-agent and implementer-ivan suggest it) and its how-to; flagged for foundation under the "all cross-cutting directives" rule |
| `procedure:doctrine-version-change` | how-to procedure `requires`d by foundation directive 018; kept beside its siblings so the whole layer can fold back into foundation in one move |
| `procedure:durable-fix-investigation` | how-to procedure `requires`d by foundation directive 052; kept beside its siblings so the whole layer can fold back into foundation in one move |
| `procedure:failing-test-triage` | how-to procedure `requires`d by foundation directive 041; kept beside its siblings so the whole layer can fold back into foundation in one move |
| `procedure:five-paradigm-structural-intervention` | how-to procedure `requires`d by foundation directive 040; kept beside its siblings so the whole layer can fold back into foundation in one move |
| `procedure:keep-change-local` | how-to procedure `requires`d by foundation directive 024; kept beside its siblings so the whole layer can fold back into foundation in one move |
| `procedure:land-changes-via-pull-request` | how-to procedure `requires`d by foundation directive 045; kept beside its siblings so the whole layer can fold back into foundation in one move |
| `procedure:living-documentation-sync` | how-to procedure `requires`d by foundation directive 037; kept beside its siblings so the whole layer can fold back into foundation in one move |
| `procedure:local-tooling-selection` | how-to procedure `requires`d by foundation directive 028; kept beside its siblings so the whole layer can fold back into foundation in one move |
| `procedure:observable-contract-test-authoring` | how-to procedure `requires`d by foundation directive 041; kept beside its siblings so the whole layer can fold back into foundation in one move |
| `procedure:op-or-mission-lifecycle` | how-to procedure `requires`d by foundation directive 053; kept beside its siblings so the whole layer can fold back into foundation in one move |
| `procedure:read-intent-before-high-risk-operation` | how-to procedure `requires`d by foundation directive 045; kept beside its siblings so the whole layer can fold back into foundation in one move |
| `procedure:readable-pr-preparation` | how-to procedure `requires`d by foundation directive 046; kept beside its siblings so the whole layer can fold back into foundation in one move |
| `procedure:red-first-bug-reproduction` | how-to procedure `requires`d by foundation directive 034/041; kept beside its siblings so the whole layer can fold back into foundation in one move |
| `procedure:red-main-handling` | how-to procedure `requires`d by foundation directive RED_MAIN_RELEASE_DISCIPLINE; kept beside its siblings so the whole layer can fold back into foundation in one move |
| `procedure:specification-traceability-check` | how-to procedure `requires`d by foundation directive 010; kept beside its siblings so the whole layer can fold back into foundation in one move |
| `procedure:targeted-staging` | how-to procedure `requires`d by foundation directive 033; kept beside its siblings so the whole layer can fold back into foundation in one move |
| `procedure:tech-debt-point-cut-triage` | how-to procedure `requires`d by foundation directive 025; kept beside its siblings so the whole layer can fold back into foundation in one move |
| `procedure:term-interpretation-alignment` | how-to procedure `requires`d by foundation directive 032; kept beside its siblings so the whole layer can fold back into foundation in one move |
| `procedure:test-and-typecheck-gate-run` | how-to procedure `requires`d by foundation directive 030; kept beside its siblings so the whole layer can fold back into foundation in one move |
| `procedure:test-first-cycle` | how-to procedure `requires`d by foundation directive 034; kept beside its siblings so the whole layer can fold back into foundation in one move |
| `procedure:tidy-first-campsite-clean` | how-to procedure `requires`d by foundation directive 025; kept beside its siblings so the whole layer can fold back into foundation in one move |
| `procedure:touched-area-cleanup` | how-to procedure `requires`d by foundation directive 025; kept beside its siblings so the whole layer can fold back into foundation in one move |
| `procedure:version-freshness-check` | how-to procedure `requires`d by foundation directive 048; kept beside its siblings so the whole layer can fold back into foundation in one move |
| `styleguide:boring-code-review` | scoped by software-dev implement+review; census foundation styleguide |
| `tactic:avoid-gold-plating` | catalog #1 core-engineering; generic over-engineering check |
| `tactic:canonical-source-unification` | catalog #1; the technique behind foundation directive 044 |
| `tactic:easy-to-change` | catalog #1 core-engineering; generic over-engineering check |
| `tactic:five-paradigm-parallel-debugging` | required by foundation directive 040; also the technique debugger-debbie and adversarial squads refine |
| `tactic:model-task-routing` | model routing; catalog lists it as runtime mechanics "staying in core" |
| `tactic:occurrence-classification-workflow` | required by foundation directive 035 (bulk-edit gate); runtime mechanic the catalog keeps "in core" |
| `tactic:op-or-mission-selection` | required by foundation directive 053 (Op or Mission) |
| `tactic:ownership-map-leeway` | Spec Kitty work-package mechanics suggested by 044/046 (owned_files, role separation, completion gates) |
| `tactic:reviewer-implementer-role-separation` | Spec Kitty work-package mechanics suggested by 044/046 (owned_files, role separation, completion gates) |
| `tactic:secure-regex-catastrophic-backtracking` | security/* tactic; census security/* -> foundation |
| `tactic:split-brain-authority-detection` | pairs with canonical-source-unification (split-brain surfaces); census "analysis tactics" -> foundation |
| `tactic:work-package-completion-validation` | Spec Kitty work-package mechanics suggested by 044/046 (owned_files, role separation, completion gates) |
| `toolguide:efficient-local-tooling` | tool mechanics of foundation directive 028; scoped by software-dev/implement |
| `toolguide:git-agent-commit-signing` | tool mechanics of foundation directive 029 (unsigned agent commits) |
| `toolguide:powershell-syntax` | shell conventions for agents on Windows; census keeps in foundation until a 2nd PowerShell artifact exists |

#### cut (3)

| Node | Reason |
|---|---|
| `directive:DIRECTIVE_039` | census cut: culture bundle named after a person; fallback core-engineering |
| `paradigm:brownfield-onboarding` | census cut: self-marked DRAFT/PROVISIONAL (2026-05-08); fallback planning-analysis |
| `procedure:small-explicit-code-shaping` | only owner is 039; cut with it, or re-parent under 024 in core-engineering |

#### drupal (4)

| Node | Reason |
|---|---|
| `agent_profile:drupal-dries` | census drupal stack |
| `styleguide:drupal-conventions` | census drupal stack |
| `styleguide:drupal-security-performance` | census drupal stack |
| `toolguide:drupal-review-checks` | census drupal stack |

#### git-delivery (6)

| Node | Reason |
|---|---|
| `paradigm:trunk-based` | opt-in branching model; delegated by software-dev/implement body -> re-attach by step enhancement |
| `procedure:git-flow` | opt-in branching model; delegated by software-dev/implement body -> re-attach by step enhancement |
| `tactic:clean-linear-commit-history` | commit-history and PR-branch hygiene (catalog #9) |
| `tactic:pr-agent-worktree-isolation` | commit-history and PR-branch hygiene (catalog #9) |
| `toolguide:git-worktree-pr-workflow` | multi-worktree/PR-landing gotchas |
| `toolguide:github-tracker` | GitHub-specific tracker operations (gh CLI) |

#### java (4)

| Node | Reason |
|---|---|
| `agent_profile:java-jenny` | #5 java stack |
| `styleguide:java-conventions` | #5 java stack |
| `toolguide:java-supply-chain` | #5 java stack |
| `toolguide:maven-review-checks` | #5 java stack |

#### javascript (13)

| Node | Reason |
|---|---|
| `agent_profile:designer-dagmar` | UX/UI and design systems; catalog #6 (census put it in foundation) |
| `agent_profile:frontend-freddy` | census javascript (node + frontend); catalog #6 |
| `agent_profile:node-norris` | census javascript (node + frontend); catalog #6 |
| `paradigm:atomic-design` | census javascript (node + frontend); catalog #6 |
| `styleguide:css-conventions` | census javascript (node + frontend); catalog #6 |
| `styleguide:html-conventions` | census javascript (node + frontend); catalog #6 |
| `styleguide:typescript-conventions` | census javascript (node + frontend); catalog #6 |
| `tactic:atomic-design-review-checklist` | census javascript (node + frontend); catalog #6 |
| `tactic:atomic-state-ownership` | census javascript (node + frontend); catalog #6 |
| `tactic:compositional-stream-boundaries` | census javascript (node + frontend); catalog #6 |
| `tactic:cross-cutting-state-via-store` | census javascript (node + frontend); catalog #6 |
| `toolguide:javascript-supply-chain` | census javascript (node + frontend); catalog #6 |
| `toolguide:typescript-mutation-tools` | census javascript (node + frontend); catalog #6 |

#### pack-authoring (7)

| Node | Reason |
|---|---|
| `agent_profile:doctrine-daphne` | census pack-authoring; catalog #15 doctrine-authoring |
| `procedure:migrate-project-guidance-to-spec-kitty-charter` | census pack-authoring; catalog #15 doctrine-authoring |
| `procedure:onboard-external-agent-to-pack` | census pack-authoring; catalog #15 doctrine-authoring |
| `styleguide:deployable-skill-authoring` | census pack-authoring; catalog #15 doctrine-authoring |
| `template:decomposition-table-template` | census pack-authoring; catalog #15 doctrine-authoring |
| `template:onboarded-artifact-set-template` | census pack-authoring; catalog #15 doctrine-authoring |
| `template:source-agent-dossier-template` | census pack-authoring; catalog #15 doctrine-authoring |

#### planning-analysis (14)

| Node | Reason |
|---|---|
| `agent_profile:planner-priti` | lead profiles: planner and researcher |
| `agent_profile:researcher-robbie` | lead profiles: planner and researcher |
| `procedure:domain-aware-decision-interview` | pre-design context, legacy triage and decision interview procedures (catalog #12/#13) |
| `procedure:issue-triage-state-machine` | backlog triage into one workflow state, requires defect diagnosis (testing); ADR-0052 d6 re-homes it as a lifecycle |
| `procedure:legacy-codebase-triage` | pre-design context, legacy triage and decision interview procedures (catalog #12/#13) |
| `procedure:situational-assessment` | pre-design context, legacy triage and decision interview procedures (catalog #12/#13) |
| `procedure:spike-timebox-policy` | spike policy (ADR-0052 d6: becomes a directive) |
| `styleguide:planning-and-tracking` | plan-mission styleguide (scope edge relocates) |
| `tactic:analysis-extract-before-interpret` | analysis tactic (catalog #13) |
| `template:agent-brief-template` | graph-only templates suggested only by issue-triage-state-machine |
| `template:lightweight-prestudy-template` | graph-only templates of situational assessment / risk tactics |
| `template:out-of-scope-record-template` | graph-only templates suggested only by issue-triage-state-machine |
| `template:quality-attribute-assessment-template` | graph-only templates of situational assessment / risk tactics |
| `template:risk-identification-assessment-template` | graph-only templates of situational assessment / risk tactics |

#### python (5)

| Node | Reason |
|---|---|
| `agent_profile:python-pedro` | #4 python stack |
| `styleguide:python-conventions` | #4 python stack |
| `toolguide:python-mutation-tools` | #4 python stack |
| `toolguide:python-review-checks` | #4 python stack |
| `toolguide:python-supply-chain` | #4 python stack |

#### refactoring (35)

| Node | Reason |
|---|---|
| `agent_profile:randy-reducer` | census refactoring; lead profile |
| `anti_pattern:big-bang-rewrite` | graph-only anti-pattern rejected only by a refactoring tactic (AP3 placement) |
| `anti_pattern:feature-envy` | graph-only anti-pattern rejected only by a refactoring tactic (AP3 placement) |
| `anti_pattern:global-data` | graph-only anti-pattern rejected only by a refactoring tactic (AP3 placement) |
| `anti_pattern:implicit-concept` | graph-only anti-pattern rejected only by a refactoring tactic (AP3 placement) |
| `anti_pattern:misplaced-field` | graph-only anti-pattern rejected only by a refactoring tactic (AP3 placement) |
| `anti_pattern:repeated-switches-on-state` | graph-only anti-pattern rejected only by a refactoring tactic (AP3 placement) |
| `anti_pattern:unencapsulated-record` | graph-only anti-pattern rejected only by a refactoring tactic (AP3 placement) |
| `paradigm:semantic-compression` | census refactoring; lead profile |
| `procedure:refactoring` | the refactoring workflow that selects among the catalog tactics (catalog #10) |
| `tactic:chain-of-responsibility-rule-pipeline` | code-patterns pipeline that suggests refactoring tactics |
| `tactic:refactoring-change-function-declaration` | refactoring/* catalog tactic |
| `tactic:refactoring-combine-functions-into-transform` | refactoring/* catalog tactic |
| `tactic:refactoring-conditional-to-strategy` | refactoring/* catalog tactic |
| `tactic:refactoring-consolidate-conditional-expression` | refactoring/* catalog tactic |
| `tactic:refactoring-encapsulate-record` | refactoring/* catalog tactic |
| `tactic:refactoring-encapsulate-variable` | refactoring/* catalog tactic |
| `tactic:refactoring-extract-class-by-responsibility-split` | refactoring/* catalog tactic |
| `tactic:refactoring-extract-first-order-concept` | refactoring/* catalog tactic |
| `tactic:refactoring-guard-clauses-before-polymorphism` | refactoring/* catalog tactic |
| `tactic:refactoring-inline-temp` | refactoring/* catalog tactic |
| `tactic:refactoring-introduce-null-object` | refactoring/* catalog tactic |
| `tactic:refactoring-move-field` | refactoring/* catalog tactic |
| `tactic:refactoring-move-method` | refactoring/* catalog tactic |
| `tactic:refactoring-replace-magic-number-with-symbolic-constant` | refactoring/* catalog tactic |
| `tactic:refactoring-replace-temp-with-query` | refactoring/* catalog tactic |
| `tactic:refactoring-retry-pattern` | refactoring/* catalog tactic |
| `tactic:refactoring-state-pattern-for-behavior` | refactoring/* catalog tactic |
| `tactic:refactoring-strangler-fig` | refactoring/* catalog tactic |
| `tactic:semantic-compression-abstraction-extraction` | semantic-compression/* tactic, required by randy-reducer |
| `tactic:semantic-compression-behavioral-boundary-mapping` | semantic-compression/* tactic, required by randy-reducer |
| `tactic:semantic-compression-dead-weight-elimination` | semantic-compression/* tactic, required by randy-reducer |
| `tactic:semantic-compression-equivalence-verification` | semantic-compression/* tactic, required by randy-reducer |
| `tactic:semantic-compression-redundancy-discovery` | semantic-compression/* tactic, required by randy-reducer |
| `tactic:semantic-compression-semantic-consolidation` | semantic-compression/* tactic, required by randy-reducer |

#### testing (20)

| Node | Reason |
|---|---|
| `agent_profile:debugger-debbie` | defect diagnosis and test-first bug fixing (catalog #3) |
| `paradigm:behaviour-driven-development` | BDD/SbE collaboration paradigms (catalog #3) |
| `paradigm:specification-by-example` | BDD/SbE collaboration paradigms (catalog #3) |
| `procedure:bdd-scenario-lifecycle` | BDD discovery/formulation procedures |
| `procedure:development-assist-test-cleanup` | retires development-assist tests; ADR-0053 d29 keeps it a product procedure |
| `procedure:disciplined-defect-diagnosis` | defect diagnosis and test-first bug fixing (catalog #3) |
| `procedure:example-mapping-workshop` | BDD discovery/formulation procedures |
| `procedure:test-first-bug-fixing` | defect diagnosis and test-first bug fixing (catalog #3) |
| `styleguide:given-when-then-authoring` | Gherkin scenario style; required by bdd-scenario-formulation/lifecycle |
| `styleguide:quadruple-a-test-format` | census foundation testing styleguides; topical testing guidance |
| `styleguide:test-desiderata-and-boundaries` | census foundation testing styleguides; topical testing guidance |
| `styleguide:testing-principles` | census foundation testing styleguides; topical testing guidance |
| `tactic:atdd-adversarial-acceptance` | testing/* technique (census testing/* -> foundation; catalog #3) |
| `tactic:bdd-scenario-formulation` | testing/* technique (census testing/* -> foundation; catalog #3) |
| `tactic:formalized-constraint-testing` | testing/* technique (census testing/* -> foundation; catalog #3) |
| `tactic:no-parallel-duplicate-test-runs` | testing/* technique (census testing/* -> foundation; catalog #3) |
| `tactic:test-minimisation` | testing/* technique (census testing/* -> foundation; catalog #3) |
| `tactic:test-pyramid-progression` | testing/* technique (census testing/* -> foundation; catalog #3) |
| `tactic:test-to-system-reconstruction` | testing/* technique (census testing/* -> foundation; catalog #3) |
| `tactic:zombies-tdd` | testing/* technique (census testing/* -> foundation; catalog #3) |

## Appendix B: edge check of the proposed DAG

Built with `edges.json` (1091 edges), with gherkin and the mutation cluster counted in `testing`:

| Result | Edges |
|---|---|
| Points down the referrer's closure (qualify with `<pack>::`) | 368 |
| Points up; relocatable into the depending pack's graph with a qualified source | 167 (57 of them F → core-engineering: 38 directive→procedure `requires`, 3 directive→tactic `requires`, the rest `suggests`/`scope`) |
| Unrelated packs | 23, all edges of the three cut candidates (they go with the cuts) |
| Body references outside closure | 5 (D1–D5), plus the pre-existing analyst-annie → 047 |
