# Lens A: graph clusters of the 217 `specialist-staging` nodes

Read-only, data-driven. The inputs were `research/edges.json` (1091), `delegates.json` (126), `profrefs.json` (only the `*-references` entries: 154 checked body refs) and `strict-membership.json`. Names and the census were ignored while clustering. Names were used only afterwards, to label clusters.
Scripts are in `scratchpad/A/` (`louv.py`, `analyze.py`, `final2.py`, `dag2.py`). The machine-readable result is in `A-clusters.json`.

## 1. Method

- **Weights.**
  - Strong edges, weight 3: requires, scope, instantiates, specializes_from, step-contract `delegates_to`, profile `*-references`.
  - reconciles_tension: weight 2.
  - Weak edges: suggests 1, refines 1, vocabulary 0.5.
  - rejects and in_tension_with: weight 0. They are kept as signals: they place anti-patterns and mark tensions.
- **Louvain.** Written in plain Python (networkx is absent), with modularity resolution γ ∈ {0.5, 1.0, 1.5} and 20 random seeds each. Two variants were run:
  - *free*: the subgraph induced by staging nodes only.
  - *anchored*: foundation, writing, qa and internal each collapsed into a fixed, unmovable community. Staging nodes may join an anchor.
- **Consensus.** Two nodes share a cluster when they are co-assigned in ≥70% of the 60 free runs. Afterwards:
  - one hub-driven cluster was split (see C13–C16);
  - anti-patterns were placed by their `rejects` source;
  - four cycle-breaking moves were applied (§4).

### Stability

| Variant | γ | Clusters (non-singleton) | Singletons | Seed-to-seed ARI |
|---|---|---|---|---|
| free | 0.5 / 1.0 / 1.5 | 14 / 18 / 21 | 62 | 0.94 / 0.88 / 0.98 |
| anchored | 0.5 / 1.0 / 1.5 | 6 / 14 / 18 (+ anchors) | 15–16 | 0.82 / 0.85 / 0.96 |

Cross-resolution ARI:
- free: 0.74 (γ 0.5→1.0) and 0.86 (γ 1.0→1.5).
- anchored: 0.22 and 0.72. At γ 0.5 the foundation anchor swallows 148 nodes.

The consensus cores are very stable: the mean pairwise co-assignment is 1.00 for every core except the K01 language/BDD core, which is 0.97. The only resolution-dependent splits are:
- refactoring: one cluster at γ ≤ 1.0, two (15 + 10) at γ 1.5;
- C4 vs glossary/terminology: one cluster of 16 at γ 1.0, 9 + 7 in the consensus.

The anchored variant agrees with the free one on every specialist core (ARI 0.30 overall, almost entirely because foundation absorbs nodes).

**The headline structural fact.** Staging is **not a graph of bundles; it is a star around foundation plus ~20 small islands**:
- 62 of the 217 nodes have no staging-to-staging edge at all.
- Among the islands there are only **6 strong cross-cluster edges** (§4).

## 2. Candidate clusters

Key to the columns:
- iS/iW: internal strong and weak edges.
- dens: internal strong edges / n(n−1).
- OUT→F/W: edges to foundation or writing (fine).
- IN←F/W/I: inbound strong edges from foundation, writing or internal. These must be relocated, or they argue for pulling the node into the anchor.

| # | Inferred theme | n | Kinds | iS / iW | dens | Strong OUT → other bundles | Strong IN ← F / W / I | Verdict |
|---|---|---|---|---|---|---|---|---|
| C01 | refactoring catalogue | 29 | 19 tactic, 7 anti_pattern, 2 procedure, 1 directive (DISCIPLINED_REFACTORING) | 1 / 26 (+7 rejects) | .001 | – | F2 (implement/review scope `procedure:refactoring`) | org bundle. Cohesion is by `suggests` only. |
| C02 | domain-driven design | 16 | paula-patterns, DDD paradigm, 8 tactic, 2 template, 1 styleguide, 3 anti_pattern | 14 / 14 | .058 | C09 (DDD requires context-boundary-inference) | F2 (software-dev/specify and plan mission_type scope DDD) | org bundle |
| C03 | brownfield / situational assessment | 13 | 5 template, 3 tactic, 3 procedure, paradigm, 1 anti_pattern | 5 / 8 | .032 | – | F5, W1, I0 | org bundle. legacy-codebase-triage and domain-aware-decision-interview are foundation-pull. |
| C04 | semantic compression | 9 | randy-reducer, paradigm, 7 tactic | 12 / 8 | .167 | – | none | the cleanest org bundle |
| C05 | C4 / architecture diagrams | 12 | USE_C4 directive, c4 paradigm, 3 c4 templates, 3 tactic, 2 procedure (+drill-down-documentation), 2 anti_pattern | 1 / 9 | .008 | – | **W6**: diagram-daisy body ref → USE_C4; documentation/design instantiates the 3 templates; documentation scope drill-down. F1. | **pulled into writing** |
| C06 | testing craft (test styleguides, pyramid) | 9 | 3 styleguide, 5 tactic, 1 procedure | 1 / 8 | .014 | – | I1 (mission-wrap-up requires development-assist-test-cleanup). F: 9 weak. | org bundle, or merge with qa |
| C07 | simple / deep-module design | 8 | DIRECTIVE_039, deep-module paradigm, 2 procedure, 3 tactic, boring-code-review | 3 / 5 | .054 | – | F4 (DIRECTIVE_034 requires test-first-cycle; implement/review scope boring-code-review; plan scopes deep-module) | borderline foundation |
| C08 | specification-by-example + BDD | 10 | architect-alphonso, SbE and BDD paradigms, example-mapping, event-storming, bdd-lifecycle, gwt styleguide, 3 tactic | 8 / 7 | .089 | C05 (alphonso requires USE_C4) | F2 incl. **step-contract delegate** specify → example-mapping-workshop (body ref) | org bundle; example-mapping-workshop is foundation-pull |
| C09 | glossary / terminology | 7 | kitty-glossary-writing, contextive, 3 tactic, 2 procedure | 3 / 4 | .071 | – | **W5**: lexical-larry body refs → terminology-extraction-mapping and context-boundary-inference. F2 (retrospect actions scope kitty-glossary-writing). | **pulled into writing** |
| C10 | squad / orchestration | 6 | planner-priti, debugger-debbie, adversarial-squad-deployment, model-task-routing, op-or-mission-selection, five-paradigm-parallel-debugging | 3 / 3 | .100 | – | F3 (reviewer-renata requires squad-deployment; DIRECTIVE_040 and _053 require two tactics) | org bundle with 3 relocations, or split |
| C11 | pack authoring / agent onboarding | 6 | doctrine-daphne, procedure, styleguide, 3 template | 1 / 4 | .033 | – | none | clean org bundle |
| C12 | atomic design (front-end state) | 5 | paradigm, 4 tactic | 0 / 6 | 0 | – | none; no anchor edges at all | clean org bundle (or fold into C13) |
| C13 | language: web (JS/TS/CSS/HTML) | 6 | frontend-freddy, node-norris, 3 styleguide, javascript-supply-chain | 4 / 2 | .133 | C08 (body ref → bdd-scenario-formulation), C22 | F1 weak | org bundle |
| C14 | language: java | 4 | java-jenny, java-conventions, maven-review-checks, java-supply-chain | 1 / 1 | .083 | C08 (body ref), C22 | – | org bundle; exactly the operator's java #5 |
| C15 | language: python | 4 | python-pedro, python-conventions, python-review-checks, python-supply-chain | 1 / 1 | .083 | – | – | org bundle |
| C16 | language: drupal | 4 | drupal-dries, 2 styleguide, 1 toolguide | 1 / 3 | .083 | C22 (requires test-first-bug-fixing) | – | org bundle |
| C17 | change-scope discipline | 4 | keep-change-local, tidy-first-campsite-clean, touched-area-cleanup, change-scope-tension-resolution | 0 / 3 | 0 | – | **F7** (DIRECTIVE_024, _025, RECONCILE_CHANGE_SCOPE_TENSIONS require all four) | **foundation** |
| C18 | planning & tracking | 4 | planning-and-tracking, github-tracker, 2 tactic | 0 / 3 | 0 | – | F1 (plan scopes planning-and-tracking) | merge C18 + C19 + C20 |
| C19 | architecture gates | 3 | post-merge-arch-gate-adjudication, 2 tactic | 1 / 1 | .167 | – | I1 (wrap-up requires it) | → internal or delivery-workflow |
| C20 | git / PR workflow | 3 | clean-linear-commit-history, pr-agent-worktree-isolation, git-worktree-pr-workflow | 0 / 3 | 0 | – | I1 | → internal or delivery-workflow |
| C21 | research spike | 2 | researcher-robbie, spike-timebox-policy | 1 / 0 | .5 | – | F1 (research mission_type scope) | foundation, or with C03 |
| C22 | defect workflow | 5 | test-first-bug-fixing, disciplined-defect-diagnosis, issue-triage-state-machine, agent-brief-template, out-of-scope-record-template | 2 / 3 | .1 | – | **F6** (implement/review/tasks scope; implementer-ivan requires test-first-bug-fixing) | **foundation** |
| C23 | foundation orbit | 44 | 30 procedure, 6 tactic, 3 toolguide, 3 profile (curator-carla, designer-dagmar, retrospective-facilitator), trunk-based, risk template | 0 / 0 | 0 | – | F43, W1 | foundation, or one "how-to" org bundle |
| C24 | orphans | 2 | human-in-charge, powershell-syntax | 0 / 0 | – | – | – | no edges at all |
| C25 | move to qa | 2 | python-mutation-tools, typescript-mutation-tools | – | – | – | qa suggests both | → qa |

### Notes on the splits and placements

- **K01 hub split (C08, C13, C14, C22).** The raw consensus had a 19-node cluster: three language profiles plus BDD plus bug-fixing. It formed only because frontend-freddy, node-norris and java-jenny all `require` the two hubs bdd-scenario-formulation and test-first-bug-fixing. With the hubs removed, the cluster falls apart into web, java, BDD and the defect chain. drupal-dries requires the same hub. The four language clusters are therefore leaf bundles that depend on BDD (C08) and on the defect workflow (C22, or foundation).
- **Anti-pattern placement.** Anti-patterns have only `rejects` edges, so they are singletons in every run. Each goes to its rejecter:
  - Rejected by the refactoring tactics: 7, to C01.
  - DDD: anemic-domain-model, database-driven-design, big-ball-of-mud, to C02. big-ball-of-mud is shared with C03, and C03 already depends on C02.
  - C4: code-is-the-documentation, single-diagram-architecture, to C05.
  - big-upfront-design is shared by C03 and C05. It goes to C03, because C05 already depends on C03.
- **Weak cohesion of the refactoring catalogue.** C01 is held together almost entirely by `suggests` (26) and `rejects` (7); it has 1 strong internal edge. It is stable only because nothing competes for those nodes.

## 3. Foundation-pull nodes

Criterion: target of strong edges from 3+ foundation artifacts, or of a step-contract `delegates_to`. Foundation holds **43 `requires` edges into staging**: 41 from directives, plus implementer-ivan and reviewer-renata.

| Tier | Node | Foundation strong sources |
|---|---|---|
| 1, delegate (body ref, cannot be relocated) | toolguide:execution-lanes, procedure:git-flow, paradigm:trunk-based | software-dev/implement step contract, plus implement and review action scope (3 each) |
| 1, delegate | procedure:example-mapping-workshop (C08) | software-dev/specify step contract |
| 1, ≥3 sources | procedure:test-first-bug-fixing (C22) | implement and review scope; implementer-ivan requires |
| 2, 2 sources | retrospective-facilitator (+ writing documentation/retrospect) | research/retrospect and software-dev/retrospect scope |
| 2 | styleguide:kitty-glossary-writing (+ writing) | retrospect actions |
| 2 | disciplined-defect-diagnosis, legacy-codebase-triage, procedure:refactoring, styleguide:boring-code-review | software-dev implement + review scope |
| 2 | domain-aware-decision-interview; paradigm:domain-driven-design | plan/research; specify/plan |
| 2 | keep-change-local, tidy-first-campsite-clean, touched-area-cleanup, red-first-bug-reproduction | 2 directives each |
| 3, 1 directive `requires` | 31 more procedures/tactics (C23 plus change-scope-tension-resolution, five-paradigm-parallel-debugging, op-or-mission-selection, test-first-cycle, adversarial-squad-deployment via reviewer-renata) | one directive each |

Of these 43 edges:
- 31 land in C23 (orbit), 7 in C17, 3 in C10, 1 in C22 and 1 in C07.

The orbit nodes have **zero cohesion with each other**: no internal edges at all. As a bundle, "the procedures of the foundation directives" has no data justification of its own: it exists only as foundation's how-to layer. If they leave foundation, they form one org bundle whose graph carries 43 relocated `foundation::` source edges. This is the operator's open question 6.

## 4. Bundle dependency DAG

**Strong edges between bundles: 6, acyclic.**
- C13 → C08: bdd-scenario-formulation (body refs).
- C14 → C08: bdd-scenario-formulation (body ref).
- C13, C14, C16 → C22: test-first-bug-fixing.
- C02 → C09: DDD requires context-boundary-inference.
- After the drill-down move, also C08 → C05 (alphonso requires drill-down-documentation).

**All reference edges (closure also needs `suggests` and `rejects`).** Before the fixes there was one strongly connected component: {C02, C03, C05, C06, C08, C09, C14}. Two further cycles ran through anchors: internal ↔ C06 ↔ C03, and qa ↔ C13/C15. Four moves break them; each is supported by the data:
1. **C09 → writing.** This is forced anyway by lexical-larry's body refs. It breaks C02 ↔ C09 and C09 → C03 → C02. The edges terminology-extraction-mapping → DDD and → brownfield-onboarding become relocated edges in C02 and C03.
2. **drill-down-documentation C08 → C05.** It is scoped by the writing documentation mission, and C4's directive suggests it. This breaks C05 ↔ C08.
3. **Relocate** `formalized-constraint-testing –suggests→ java-conventions` (C06 → C14) into the java pack's graph. This breaks C06 → C14 → C08 → C06.
4. **Mutation tools → qa.** The anchored Louvain already put them there. This breaks qa ↔ lang. Also relocate `development-assist-test-cleanup –suggests→ mission-tracer-files` into internal, which breaks internal ↔ C06.

**Resulting DAG.** Everything also depends on foundation; C05 and C09 belong in writing.

```
writing ⊇ {C05 c4, C09 glossary}
C01 refactoring      ← C02, C04, C13, C14, C15
C10 squad            ← C02, C03, internal
C06 testing-craft    ← C03, C08, internal
C02 ddd              ← C03, C04, C05(w), C08
C03 brownfield       ← C05(w), internal
C08 sbe-bdd          ← C13, C14
C22 defect (→ foundation) ← C13, C14, C16
qa                   ← C04, C06, C08, C10, C13, C14, C15
internal             → C03, C06, C10, C19, C20
C18 planning         → internal(w)
leaves: C04, C11, C12, C13–C16, C21
```

Topological order:
1. qa
2. C01, C06, C07, C10, C11, C19, C20, C22
3. C02, C15, C16
4. C03, C04
5. C05 (writing)
6. internal
7. C08, C18
8. C13, C14

Separately, the pre-existing writing ↔ foundation cycle remains: foundation has 3 strong edges into writing. This is outside staging and should be checked by phase 1.

### Suggested merges

These reduce pack count without creating cycles:
- **delivery-workflow** = C18 + C19 + C20 (10 nodes). Internal requires two of them; it could instead be folded into internal.
- **architecture-modelling** = C02 + C03 + C08 (+C21) = 41. This is only if fewer, larger bundles are wanted. C03 → C02 ← C08 are all weak edges.
- **C12 into C13** (front-end). The two are thematically related, but there is no data edge between them.
- **C06 into qa.**

## 5. Orphans and weakly connected nodes

- **No edges at all:** human-in-charge and powershell-syntax. They have no gravity, so they can go anywhere or be dropped. powershell-syntax could go to a future windows/tooling pack.
- **Only foundation ties (62 free-run singletons):**
  - The 44 orbit nodes. Their gravity is foundation.
  - curator-carla, which requires DIRECTIVE_018 only, and designer-dagmar, which requires DIRECTIVE_031 only: both gravitate to foundation.
  - The 13 anti-patterns, placed by `rejects` as above.
  - java/python-supply-chain, which foundation's supply-chain-install-safety suggests. They are joined to their language bundles.
- **Weakly anchored islands:** C12 has no edges outside itself. C11 and C04 have no inbound edges. These three are the cheapest bundles to carve first.
