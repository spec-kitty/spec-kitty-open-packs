# #73 research 1: built-in membership inventory and per-artifact rulings

Read-only research. Repo spec-kitty-open-packs @ `5c489d6`; charter @ `fb24052`. Generated from `packs/built-in/*.graph.yaml` (398 nodes, 1091 edges), the step-contract `delegates_to` candidates (126) and the agent-profile YAML `*-references` and `collaboration` ids, reconciled against `pack-manifest.yaml` (310 constituents) and the filesystem (459 files).

## Baseline and rules applied

- **Baseline:** the charter census, `docs/plans/pack-ecosystem-work-breakdown.md` § "Foundation membership (census proposal)" (census at open-packs `1060bfc`), adopted as the starting cut by ADR-0053 d2. Every ruling below says "census" when it follows it; divergences are in group E with the reason.
- **built-in is a distribution pack that holds no artifacts** (ADR-0048 d12, #73 2026-11-08 body). Only `pack.yaml`, `pack.md`, the regenerated manifest and the two presets stay (ADR-0048 d12: presets stay on built-in). So group C ("stays in built-in") has **0 artifacts**; see § Pack metadata for the files.
- **Members:** `foundation` + `writing` (ADR-0053 d3, d9), both roots (`parent_pack: null`, ADR-0048 d15), released in lockstep with exact pins from built-in (d17).
- **Stack/topical packs are opt-in org packs** (ADR-0048 d14, ADR-0053 d1); the census names `java`, `python`, `drupal`, `javascript`, plus topical `architecture`, `refactoring`, `spdd` (done, #175), `qa` (exists), `pack-authoring`/`internal`.
- **Dependency direction assumed:** `writing` depends_on `foundation` (45 writing→foundation edges, see § Edges); `foundation` depends on nothing; opt-in packs depend on `built-in` (today) or directly on a member. A level/closure rule (ADR-0048 d7 amended, ADR-0053 d7 amended) means a pack may only reference packs in its own `depends_on` closure, so **every foundation→writing and member→opt-in edge is a defect** unless relocated.
- **Edge relocation pattern:** a specialist pack may add edges (ADR-0048 d9); since ADR-0064 graph documents are the only relationship source, an edge whose source is in a lower pack can be declared in the higher pack's graph with a qualified source (`foundation::mission_type:documentation scope styleguide:divio-type-discipline` declared in `writing`). This is the recommended fix for every P1/P2 edge below.

## Counts

| Group | Nodes |
|---|---|
| A. Uncontested → foundation | 230 |
| B. Uncontested → writing | 38 |
| D. Stack / opt-in topical pack (not a built-in member) | 68 |
| E. Contested — needs operator ruling | 62 |
| C. Stays in built-in | 0 artifacts (pack.yaml, pack.md, manifest, presets/default, presets/minimal; policy.yaml contested) |
| **Total graph nodes** | 398 |

By target:

| Target pack | Nodes |
|---|---|
| foundation | 230 |
| foundation (rec) | 58 |
| writing | 38 |
| refactoring (future) | 26 |
| javascript (future) | 12 |
| pack-authoring (future) | 6 |
| qa (exists) | 5 |
| python (future) | 5 |
| java (#5) | 4 |
| drupal (future) | 4 |
| internal (exists) | 4 |
| cut (rec) / foundation until ruled | 1 |
| cut (rec) | 1 |
| pack-authoring or internal (future) | 1 |
| architecture (future) | 1 |
| qa (rec) | 1 |
| foundation (rec) / cut with 039 | 1 |

Per kind × group:

| Kind | A foundation | B writing | D opt-in | E contested | total |
|---|---|---|---|---|---|
| agent_profile | 12 | 6 | 7 | 1 | 26 |
| directive | 29 | 4 | 1 | 4 | 38 |
| paradigm | 4 | 0 | 2 | 3 | 9 |
| styleguide | 5 | 9 | 10 | 3 | 27 |
| toolguide | 5 | 2 | 11 | 1 | 19 |
| tactic | 61 | 5 | 28 | 26 | 120 |
| procedure | 49 | 7 | 5 | 5 | 66 |
| asset | 0 | 5 | 1 | 0 | 6 |
| template | 18 | 0 | 3 | 3 | 24 |
| anti_pattern | 13 | 0 | 0 | 0 | 13 |
| glossary_pack | 1 | 0 | 0 | 0 | 1 |
| mission_type | 3 | 0 | 0 | 1 | 4 |
| mission_step_contract | 14 | 0 | 0 | 7 | 21 |
| action | 16 | 0 | 0 | 8 | 24 |

## E. Contested items — clusters and recommendations

| Cluster | Members | Recommendation | Why contested |
|---|---|---|---|
| E-DOC documentation mission bundle (18 nodes) | `mission_type:documentation`, its 7 step contracts, 8 `action:documentation/*`, 2 `template:documentation/*` | **foundation**, and relocate its 19 strong `scope` edges into writing's graph | ADR-0048 d13 / ADR-0050 d7 keep shipped mission types in foundation, and ADR-0053 d3's reason for making writing a member is exactly this mission's guidance. But 19 `scope` edges point from it into writing (P1 below). Alternative (cleaner graph, contradicts d13's wording): move the documentation mission type into writing. |
| E-DDD (11) | `paradigm:domain-driven-design`, `styleguide:aggregate-design-rules`, tactics bounded-context-canvas-fill, bounded-context-identification, context-boundary-inference, context-mapping-classification, entity-value-object-classification, strategic-domain-classification, aggregate-boundary-design, domain-event-capture, anti-corruption-layer | **foundation** (keep the cluster together) | Census keeps the DDD paradigm in foundation but sends "DDD analysis tactics and architecture/*" to `architecture`; the paradigm `requires` 9 of them and aggregate-design-rules, paula-patterns requires 2, the plan mission scopes bounded-context-identification, lexical-larry/glossary-maintenance-workflow require context-boundary-inference, and event-driven cites 3 of them as `built-in::`. Alternative: move the whole DDD cluster (paradigm, paula-patterns too) to `architecture`. |
| E-C4 (5) | `directive:USE_C4_MODEL_TECHNIQUES`, `paradigm:c4-incremental-detail-modeling`, `procedure:c4-diagram-authoring`, tactics architecture-diagram-review-checklist, c4-zoom-in-architecture-documentation | **foundation** | Census → architecture, but `mission_type:plan` scopes the C4 paradigm and diagram-daisy (writing) `requires` the directive; an opt-in architecture pack would sit outside both members' closures. |
| Architecture-path tactics needed by foundation (8) | dependency-hygiene, development-bdd, problem-decomposition, interface-variation-design, deepening-opportunity-assessment, language-driven-design, paula-patterns-architecture-scout-review, reference-architectural-patterns | **foundation** | Each is `required` by a foundation profile (ivan, alphonso, renata, paula-patterns) or scoped/delegated by a shipped mission step; #5 says dependency-hygiene "stays"; event-driven cites reference-architectural-patterns. After E-DDD/E-C4/this, the census `architecture` pack keeps only `toolguide:contextive` (D) — consider folding contextive into foundation and dropping the `architecture` pack idea. |
| Communication tactics needed by foundation (7) | adr-drafting-workflow, decision-marker-capture, traceable-decisions, usage-examples-sync, glossary-curation-interview, stakeholder-alignment, template:stakeholder-persona-template | **foundation** | Census: `tactics/communication/*` → writing. But DIRECTIVE_003 requires decision-marker-capture/traceable-decisions, 037 + SbE require usage-examples-sync, step contracts delegate to adr-drafting-workflow and usage-examples-sync, glossary-maintenance-workflow requires glossary-curation-interview, situational-assessment requires stakeholder-alignment. The other three communication tactics (writing-audience-catalog, documentation-curation-audit, common-docs-*) do go to writing. |
| Census omissions (4) | `directive:DIRECTIVE_037` (+ its `procedure:living-documentation-sync`), `styleguide:planning-and-tracking`, `toolguide:github-tracker` | **foundation** | Not listed anywhere in the census. 037 is scoped by software-dev/research actions and required by BDD/SbE/048; planning-and-tracking is scoped by the plan mission and suggested by 044; github-tracker hangs off planning-and-tracking (internal cites it too). |
| Testing items the census sends to qa (4) | `directive:DIRECTIVE_036` + `procedure:black-box-integration-test-design`; `styleguide:given-when-then-authoring`; `tactic:mutation-testing-workflow` | 036 & BBIT design & given-when-then → **foundation**; mutation-testing-workflow → **qa** | software-dev implement+review actions scope 036 (strong foundation→qa edge otherwise); bdd-scenario-lifecycle and bdd-scenario-formulation require given-when-then. mutation-testing-workflow is the reverse case: census leaves `testing/*` in foundation, but its directive and styleguide go to qa, and only weak edges reach it. |
| Cut candidates (3) | `directive:DIRECTIVE_039`, `paradigm:brownfield-onboarding`, `procedure:small-explicit-code-shaping` | cut 039 and brownfield-onboarding **only with** the edge fixes; keep small-explicit-code-shaping in foundation re-parented (e.g. under DIRECTIVE_024) or cut with 039 | Census cut candidates. `paradigm:deep-module-design` (foundation) **requires** DIRECTIVE_039 — cutting it needs that edge dropped; 039 is the only owner of small-explicit-code-shaping and co-owner of test-first-cycle. brownfield-onboarding is suggested by 025, mission-tracer-files and terminology-extraction-mapping (edges drop with it). Safe default for this PR: park both in foundation and cut in the curation pass. |
| drill-down-documentation (1) | `procedure:drill-down-documentation` | **foundation** | Docs-flavoured (ADR-0053 d29a: re-home as a styleguide rule in curation), but architect-alphonso requires it. |
| generic-agent + policy (1 + file) | `agent_profile:generic-agent`, `policy.yaml` | profile → **foundation**; foundation gets `policy.yaml` locking it and its own `fallback_profile: generic-agent`; built-in keeps `fallback_profile: generic-agent` in pack.yaml (resolves in closure, ADR-0068 d2) | ADR-0068 d5 says built-in declares the fallback "locked by built-in's policy file"; but built-in will hold no artifacts and ADR-0063 D2 makes policy keys bare URNs (never pack-qualified) for the pack's own artifacts. Whether built-in's policy may still lock a member's artifact needs a ruling (or a charter clarification). |

Process recommendation for group D (not E, but needs one decision): items whose target pack does not exist yet (`python`, `drupal`, `javascript`, `refactoring`, `pack-authoring`, `architecture`) should go to **foundation as a holding area** in this PR and be carved by their own issues (as #5 does for java), so #73 stays the foundation/writing split. Items for existing packs (`qa`, `internal`) can move in this PR or in a follow-up; #5 owns the 4 java items (if #73 lands first they go to foundation and #5 moves them from there).

## E. Contested — needs operator ruling — 62

Inbound referrers: `[pack]` marks a referrer that would sit in a different pack (those edges need `<pack>::` qualification or relocation).

### agent_profile (1)

| Artifact | Ruling | Reason | Inbound referrers |
|---|---|---|---|
| `generic-agent` | foundation (rec) | fallback_profile; census foundation. Lock/declaration placement needs ruling (built-in pack.yaml fallback_profile + policy.yaml vs foundation) | agent_profile:retrospective-facilitator |

### directive (4)

| Artifact | Ruling | Reason | Inbound referrers |
|---|---|---|---|
| `DIRECTIVE_036` | foundation (rec) | census folds 036 into qa, but software-dev implement+review actions SCOPE it (strong foundation->qa edge); keep in foundation | action:software-dev/implement, action:software-dev/review, tactic:semantic-compression-equivalence-verification [refactoring] |
| `DIRECTIVE_037` | foundation (rec) | census omits 037; scoped by software-dev/research actions, required by BDD/SbE paradigms and 048 -> foundation, else foundation->writing requires edges | action:documentation/accept, action:documentation/audit, action:documentation/generate, action:documentation/publish, action:documentation/validate, action:research/gathering +21 more |
| `DIRECTIVE_039` | cut (rec) / foundation until ruled | census cut candidate (culture bundle named after a person); it alone owns small-explicit-code-shaping and co-owns test-first-cycle | paradigm:deep-module-design [foundation] |
| `USE_C4_MODEL_TECHNIQUES` | foundation (rec) | E-C4: census architecture, but diagram-daisy (writing) REQUIRES it and the plan mission type scopes the C4 paradigm | agent_profile:architect-alphonso, agent_profile:diagram-daisy [writing] |

### paradigm (3)

| Artifact | Ruling | Reason | Inbound referrers |
|---|---|---|---|
| `brownfield-onboarding` | cut (rec) | census cut candidate (self-marked provisional); its required tactics/procedures stay in foundation regardless | directive:DIRECTIVE_025 [foundation], procedure:mission-tracer-files [internal], tactic:terminology-extraction-mapping [foundation] |
| `c4-incremental-detail-modeling` | foundation (rec) | E-C4: scoped by mission_type:plan (foundation) | directive:USE_C4_MODEL_TECHNIQUES, mission_type:plan |
| `domain-driven-design` | foundation (rec) | census foundation, but census sends its required DDD tactics to architecture: keep the DDD cluster together in foundation (see E-DDD) | action:software-dev/specify, agent_profile:architect-alphonso, agent_profile:paula-patterns, agent_profile:randy-reducer [refactoring], directive:USE_C4_MODEL_TECHNIQUES, mission_type:plan +1 more |

### styleguide (3)

| Artifact | Ruling | Reason | Inbound referrers |
|---|---|---|---|
| `aggregate-design-rules` | foundation (rec) | E-DDD: census architecture, but the foundation DDD paradigm REQUIRES it | paradigm:domain-driven-design |
| `given-when-then-authoring` | foundation (rec) | census qa, but bdd-scenario-lifecycle and bdd-scenario-formulation (foundation) REQUIRE it | directive:DIRECTIVE_034, paradigm:behaviour-driven-development, procedure:bdd-scenario-lifecycle, tactic:bdd-scenario-formulation |
| `planning-and-tracking` | foundation (rec) | census omits it; scoped by plan mission type and suggested by DIRECTIVE_044 (both foundation) | directive:DIRECTIVE_044, mission_type:plan |

### toolguide (1)

| Artifact | Ruling | Reason | Inbound referrers |
|---|---|---|---|
| `github-tracker` | foundation (rec) | census omits it; generic tracker usage, suggested only by planning-and-tracking | styleguide:planning-and-tracking |

### tactic (26)

| Artifact | Ruling | Reason | Inbound referrers |
|---|---|---|---|
| `adr-drafting-workflow` | foundation (rec) | census communication/* -> writing, but required by foundation directives (003/037), SbE paradigm, glossary procedure and/or delegated by step contracts | action:documentation/design, action:plan/plan, action:plan/review, action:research/methodology, action:software-dev/plan, action:software-dev/tasks +10 more |
| `aggregate-boundary-design` | foundation (rec) | E-DDD: census sends DDD tactics to architecture, but the foundation DDD paradigm (and paula-patterns / plan mission / lexical-larry / glossary procedure) REQUIRE them | paradigm:domain-driven-design, procedure:event-storming-discovery, styleguide:aggregate-design-rules, tactic:bounded-context-canvas-fill |
| `anti-corruption-layer` | foundation (rec) | E-DDD: census sends DDD tactics to architecture, but the foundation DDD paradigm (and paula-patterns / plan mission / lexical-larry / glossary procedure) REQUIRE them | agent_profile:paula-patterns, paradigm:domain-driven-design, tactic:context-mapping-classification, tactic:paula-patterns-architecture-scout-review |
| `architecture-diagram-review-checklist` | foundation (rec) | E-C4: suggested by USE_C4_MODEL_TECHNIQUES; go with the C4 cluster | directive:USE_C4_MODEL_TECHNIQUES, tactic:reference-architectural-patterns |
| `bounded-context-canvas-fill` | foundation (rec) | E-DDD: census sends DDD tactics to architecture, but the foundation DDD paradigm (and paula-patterns / plan mission / lexical-larry / glossary procedure) REQUIRE them | paradigm:domain-driven-design |
| `bounded-context-identification` | foundation (rec) | E-DDD: census sends DDD tactics to architecture, but the foundation DDD paradigm (and paula-patterns / plan mission / lexical-larry / glossary procedure) REQUIRE them | action:plan/research, action:plan/specify, mission_type:plan, paradigm:domain-driven-design, procedure:event-storming-discovery, tactic:aggregate-boundary-design +5 more |
| `c4-zoom-in-architecture-documentation` | foundation (rec) | E-C4: suggested by USE_C4_MODEL_TECHNIQUES; go with the C4 cluster | directive:USE_C4_MODEL_TECHNIQUES, tactic:architecture-diagram-review-checklist |
| `context-boundary-inference` | foundation (rec) | E-DDD: census sends DDD tactics to architecture, but the foundation DDD paradigm (and paula-patterns / plan mission / lexical-larry / glossary procedure) REQUIRE them | agent_profile:lexical-larry [writing], paradigm:domain-driven-design, procedure:glossary-maintenance-workflow |
| `context-mapping-classification` | foundation (rec) | E-DDD: census sends DDD tactics to architecture, but the foundation DDD paradigm (and paula-patterns / plan mission / lexical-larry / glossary procedure) REQUIRE them | paradigm:domain-driven-design, tactic:bounded-context-canvas-fill, tactic:strategic-domain-classification |
| `decision-marker-capture` | foundation (rec) | census communication/* -> writing, but required by foundation directives (003/037), SbE paradigm, glossary procedure and/or delegated by step contracts | action:plan/plan, directive:DIRECTIVE_003, mission_type:plan |
| `deepening-opportunity-assessment` | foundation (rec) | architecture/* by path, but required by a foundation profile or scoped/delegated by a shipped mission step | action:plan/research, action:software-dev/plan, mission_type:plan, tactic:interface-variation-design |
| `dependency-hygiene` | foundation (rec) | architecture/* by path, but #5 says it stays (java-jenny cites it); required by implementer-ivan, architect-alphonso, scoped by implement | action:software-dev/implement, agent_profile:architect-alphonso, agent_profile:drupal-dries [drupal], agent_profile:frontend-freddy [javascript], agent_profile:implementer-ivan, agent_profile:java-jenny [java] +3 more |
| `development-bdd` | foundation (rec) | architecture/* by path, but required by a foundation profile or scoped/delegated by a shipped mission step | agent_profile:architect-alphonso, directive:DIRECTIVE_034 |
| `domain-event-capture` | foundation (rec) | E-DDD: census sends DDD tactics to architecture, but the foundation DDD paradigm (and paula-patterns / plan mission / lexical-larry / glossary procedure) REQUIRE them | agent_profile:paula-patterns, paradigm:domain-driven-design, procedure:event-storming-discovery, styleguide:aggregate-design-rules, tactic:aggregate-boundary-design, tactic:paula-patterns-architecture-scout-review |
| `entity-value-object-classification` | foundation (rec) | E-DDD: census sends DDD tactics to architecture, but the foundation DDD paradigm (and paula-patterns / plan mission / lexical-larry / glossary procedure) REQUIRE them | paradigm:domain-driven-design, tactic:aggregate-boundary-design |
| `glossary-curation-interview` | foundation (rec) | census communication/* -> writing, but required by foundation directives (003/037), SbE paradigm, glossary procedure and/or delegated by step contracts | action:documentation/retrospect, action:research/retrospect, action:software-dev/retrospect, agent_profile:lexical-larry [writing], directive:DIRECTIVE_032, procedure:domain-aware-decision-interview +5 more |
| `interface-variation-design` | foundation (rec) | architecture/* by path, but required by a foundation profile or scoped/delegated by a shipped mission step | action:software-dev/plan |
| `language-driven-design` | foundation (rec) | architecture/* by path, but required by a foundation profile or scoped/delegated by a shipped mission step | agent_profile:reviewer-renata, directive:DIRECTIVE_032, procedure:domain-aware-decision-interview, tactic:bounded-context-canvas-fill, tactic:bounded-context-identification, tactic:code-documentation-analysis +5 more |
| `mutation-testing-workflow` | qa (rec) | census testing/* -> foundation, but its directive and styleguide go to qa (census flags the three mutation artifacts as an overlap) | directive:USE_MUTATION_TESTING_TO_VALIDATE_TEST_QUALITY, styleguide:mutation-aware-test-design, tactic:acceptance-criteria-non-vacuity [foundation] |
| `paula-patterns-architecture-scout-review` | foundation (rec) | architecture/* by path, but required by a foundation profile or scoped/delegated by a shipped mission step | agent_profile:paula-patterns, directive:DIRECTIVE_001 |
| `problem-decomposition` | foundation (rec) | architecture/* by path, but required by a foundation profile or scoped/delegated by a shipped mission step | action:plan/plan, action:software-dev/tasks, mission_step_contract:software-dev/tasks, mission_type:plan, procedure:situational-assessment |
| `reference-architectural-patterns` | foundation (rec) | census architecture/*, but event-driven (existing opt-in pack) cites built-in::tactic:reference-architectural-patterns; moving it to a future architecture pack forces event-driven to depend on that pack | — |
| `stakeholder-alignment` | foundation (rec) | census communication/* -> writing, but situational-assessment (foundation) REQUIRES it and documentation/discover scopes it | action:documentation/discover, procedure:situational-assessment, styleguide:professional-communications [writing], tactic:problem-decomposition |
| `strategic-domain-classification` | foundation (rec) | E-DDD: census sends DDD tactics to architecture, but the foundation DDD paradigm (and paula-patterns / plan mission / lexical-larry / glossary procedure) REQUIRE them | paradigm:domain-driven-design, procedure:legacy-codebase-triage, tactic:bounded-context-canvas-fill |
| `traceable-decisions` | foundation (rec) | census communication/* -> writing, but required by foundation directives (003/037), SbE paradigm, glossary procedure and/or delegated by step contracts | action:plan/plan, action:plan/review, directive:DIRECTIVE_003, mission_type:plan, tactic:interface-variation-design |
| `usage-examples-sync` | foundation (rec) | census communication/* -> writing, but required by foundation directives (003/037), SbE paradigm, glossary procedure and/or delegated by step contracts | action:software-dev/review, directive:DIRECTIVE_037, mission_step_contract:research/output, mission_step_contract:software-dev/review, mission_type:documentation, paradigm:specification-by-example +2 more |

### procedure (5)

| Artifact | Ruling | Reason | Inbound referrers |
|---|---|---|---|
| `black-box-integration-test-design` | foundation (rec) | follows DIRECTIVE_036 | directive:DIRECTIVE_036 |
| `c4-diagram-authoring` | foundation (rec) | E-C4: follows USE_C4_MODEL_TECHNIQUES | directive:USE_C4_MODEL_TECHNIQUES |
| `drill-down-documentation` | foundation (rec) | docs-flavoured (ADR-0053 d29a re-home as styleguide rule), but required by architect-alphonso (foundation) | agent_profile:architect-alphonso, directive:USE_C4_MODEL_TECHNIQUES, mission_type:documentation |
| `living-documentation-sync` | foundation (rec) | follows DIRECTIVE_037 (see 037) | directive:DIRECTIVE_037 |
| `small-explicit-code-shaping` | foundation (rec) / cut with 039 | only owner is DIRECTIVE_039 (cut candidate) | directive:DIRECTIVE_039 [cut] |

### template (3)

| Artifact | Ruling | Reason | Inbound referrers |
|---|---|---|---|
| `documentation/documentation-plan-template.md` | foundation (rec) | E-DOC: documentation mission template; follows the mission bundle | action:documentation/design |
| `documentation/documentation-spec-template.md` | foundation (rec) | E-DOC: documentation mission template; follows the mission bundle | action:documentation/discover |
| `stakeholder-persona-template` | foundation (rec) | graph-only node, NO template file in the pack (defect to fix or drop); placed with its referrers: stakeholder-alignment (E, rec foundation) | tactic:stakeholder-alignment |

### mission_type (1)

| Artifact | Ruling | Reason | Inbound referrers |
|---|---|---|---|
| `documentation` | foundation (rec) | E-DOC: documentation mission bundle; ADR-0048 d13 puts shipped mission types in foundation, but its scope edges point at writing | — |

### mission_step_contract (7)

| Artifact | Ruling | Reason | Inbound referrers |
|---|---|---|---|
| `documentation/accept` | foundation (rec) | E-DOC: documentation mission bundle; ADR-0048 d13 puts shipped mission types in foundation, but its scope edges point at writing | — |
| `documentation/audit` | foundation (rec) | E-DOC: documentation mission bundle; ADR-0048 d13 puts shipped mission types in foundation, but its scope edges point at writing | — |
| `documentation/design` | foundation (rec) | E-DOC: documentation mission bundle; ADR-0048 d13 puts shipped mission types in foundation, but its scope edges point at writing | — |
| `documentation/discover` | foundation (rec) | E-DOC: documentation mission bundle; ADR-0048 d13 puts shipped mission types in foundation, but its scope edges point at writing | — |
| `documentation/generate` | foundation (rec) | E-DOC: documentation mission bundle; ADR-0048 d13 puts shipped mission types in foundation, but its scope edges point at writing | — |
| `documentation/publish` | foundation (rec) | E-DOC: documentation mission bundle; ADR-0048 d13 puts shipped mission types in foundation, but its scope edges point at writing | — |
| `documentation/validate` | foundation (rec) | E-DOC: documentation mission bundle; ADR-0048 d13 puts shipped mission types in foundation, but its scope edges point at writing | — |

### action (8)

| Artifact | Ruling | Reason | Inbound referrers |
|---|---|---|---|
| `documentation/accept` | foundation (rec) | E-DOC: documentation mission bundle; ADR-0048 d13 puts shipped mission types in foundation, but its scope edges point at writing | mission_type:documentation |
| `documentation/audit` | foundation (rec) | E-DOC: documentation mission bundle; ADR-0048 d13 puts shipped mission types in foundation, but its scope edges point at writing | mission_type:documentation |
| `documentation/design` | foundation (rec) | E-DOC: documentation mission bundle; ADR-0048 d13 puts shipped mission types in foundation, but its scope edges point at writing | mission_type:documentation |
| `documentation/discover` | foundation (rec) | E-DOC: documentation mission bundle; ADR-0048 d13 puts shipped mission types in foundation, but its scope edges point at writing | mission_type:documentation |
| `documentation/generate` | foundation (rec) | E-DOC: documentation mission bundle; ADR-0048 d13 puts shipped mission types in foundation, but its scope edges point at writing | mission_type:documentation |
| `documentation/publish` | foundation (rec) | E-DOC: documentation mission bundle; ADR-0048 d13 puts shipped mission types in foundation, but its scope edges point at writing | mission_type:documentation |
| `documentation/retrospect` | foundation (rec) | E-DOC: documentation mission bundle; ADR-0048 d13 puts shipped mission types in foundation, but its scope edges point at writing | — |
| `documentation/validate` | foundation (rec) | E-DOC: documentation mission bundle; ADR-0048 d13 puts shipped mission types in foundation, but its scope edges point at writing | mission_type:documentation |

## A. Uncontested → foundation — 230

Inbound referrers: `[pack]` marks a referrer that would sit in a different pack (those edges need `<pack>::` qualification or relocation).

### agent_profile (12)

| Artifact | Ruling | Reason | Inbound referrers |
|---|---|---|---|
| `analyst-annie` | foundation | base profile; census foundation (strip stack-specific examples) | agent_profile:comms-cleo [writing], agent_profile:lexical-larry [writing] |
| `architect-alphonso` | foundation | base profile; census foundation (strip stack-specific examples) | agent_profile:analyst-annie, agent_profile:diagram-daisy [writing], agent_profile:lexical-larry [writing] |
| `curator-carla` | foundation | base profile; census foundation (strip stack-specific examples) | agent_profile:lexical-larry [writing] |
| `debugger-debbie` | foundation | base profile; census foundation (strip stack-specific examples) | — |
| `designer-dagmar` | foundation | base profile; census foundation (strip stack-specific examples) | — |
| `human-in-charge` | foundation | base profile; census foundation (strip stack-specific examples) | agent_profile:debugger-debbie, agent_profile:paula-patterns, agent_profile:randy-reducer [refactoring], agent_profile:retrospective-facilitator |
| `implementer-ivan` | foundation | base profile; census foundation (strip stack-specific examples) | agent_profile:analyst-annie, agent_profile:drupal-dries [drupal], agent_profile:frontend-freddy [javascript], agent_profile:java-jenny [java], agent_profile:node-norris [javascript], agent_profile:python-pedro [python] |
| `paula-patterns` | foundation | base profile; census foundation (strip stack-specific examples) | — |
| `planner-priti` | foundation | base profile; census foundation (strip stack-specific examples) | — |
| `researcher-robbie` | foundation | base profile; census foundation (strip stack-specific examples) | — |
| `retrospective-facilitator` | foundation | base profile; census foundation (strip stack-specific examples) | action:documentation/retrospect, action:research/retrospect, action:software-dev/retrospect |
| `reviewer-renata` | foundation | base profile; census foundation (strip stack-specific examples) | — |

### directive (29)

| Artifact | Ruling | Reason | Inbound referrers |
|---|---|---|---|
| `DIRECTIVE_001` | foundation | cross-cutting engineering directive; census foundation list | action:documentation/design, action:software-dev/implement, action:software-dev/review, agent_profile:architect-alphonso, agent_profile:debugger-debbie, agent_profile:paula-patterns +25 more |
| `DIRECTIVE_003` | foundation | cross-cutting engineering directive; census foundation list | action:documentation/audit, action:documentation/design, action:documentation/discover, action:documentation/retrospect, action:research/gathering, action:research/methodology +37 more |
| `DIRECTIVE_010` | foundation | cross-cutting engineering directive; census foundation list | action:documentation/accept, action:documentation/design, action:documentation/discover, action:documentation/generate, action:documentation/publish, action:documentation/retrospect +40 more |
| `DIRECTIVE_018` | foundation | cross-cutting engineering directive; census foundation list | action:documentation/retrospect, action:research/retrospect, action:software-dev/retrospect, agent_profile:curator-carla, agent_profile:doctrine-daphne [pack-authoring], agent_profile:retrospective-facilitator +3 more |
| `DIRECTIVE_024` | foundation | cross-cutting engineering directive; census foundation list | action:software-dev/implement, action:software-dev/review, action:software-dev/tasks, agent_profile:drupal-dries [drupal], agent_profile:frontend-freddy [javascript], agent_profile:java-jenny [java] +12 more |
| `DIRECTIVE_025` | foundation | cross-cutting engineering directive; census foundation list | action:software-dev/implement, action:software-dev/review, agent_profile:drupal-dries [drupal], agent_profile:frontend-freddy [javascript], agent_profile:java-jenny [java], agent_profile:node-norris [javascript] +7 more |
| `DIRECTIVE_028` | foundation | cross-cutting engineering directive; census foundation list | action:software-dev/implement, action:software-dev/review, agent_profile:generic-agent, procedure:legacy-codebase-triage, tactic:forensic-repository-audit, toolguide:execution-lanes |
| `DIRECTIVE_029` | foundation | cross-cutting engineering directive; census foundation list | action:software-dev/implement, action:software-dev/review, mission_step_contract:documentation/accept, mission_step_contract:documentation/audit, mission_step_contract:documentation/design, mission_step_contract:documentation/discover +17 more |
| `DIRECTIVE_030` | foundation | cross-cutting engineering directive; census foundation list | action:software-dev/implement, action:software-dev/review, agent_profile:debugger-debbie, agent_profile:drupal-dries [drupal], agent_profile:frontend-freddy [javascript], agent_profile:generic-agent +30 more |
| `DIRECTIVE_031` | foundation | cross-cutting engineering directive; census foundation list | agent_profile:architect-alphonso, agent_profile:designer-dagmar, directive:DIRECTIVE_032, mission_type:plan, paradigm:domain-driven-design |
| `DIRECTIVE_032` | foundation | cross-cutting engineering directive; census foundation list | agent_profile:analyst-annie, agent_profile:architect-alphonso, agent_profile:debugger-debbie, agent_profile:doctrine-daphne [pack-authoring], agent_profile:lexical-larry [writing], agent_profile:paula-patterns +8 more |
| `DIRECTIVE_033` | foundation | cross-cutting engineering directive; census foundation list | mission_step_contract:documentation/accept, mission_step_contract:documentation/audit, mission_step_contract:documentation/design, mission_step_contract:documentation/discover, mission_step_contract:documentation/generate, mission_step_contract:documentation/publish +15 more |
| `DIRECTIVE_034` | foundation | cross-cutting engineering directive; census foundation list | action:software-dev/implement, action:software-dev/review, agent_profile:drupal-dries [drupal], agent_profile:frontend-freddy [javascript], agent_profile:generic-agent, agent_profile:implementer-ivan +24 more |
| `DIRECTIVE_035` | foundation | cross-cutting engineering directive; census foundation list | — |
| `DIRECTIVE_040` | foundation | cross-cutting engineering directive; census foundation list | directive:DIRECTIVE_025, directive:DIRECTIVE_052 |
| `DIRECTIVE_041` | foundation | cross-cutting engineering directive; census foundation list | agent_profile:architect-alphonso, agent_profile:frontend-freddy [javascript], agent_profile:generic-agent, agent_profile:implementer-ivan, agent_profile:java-jenny [java], agent_profile:node-norris [javascript] +7 more |
| `DIRECTIVE_043` | foundation | cross-cutting engineering directive; census foundation list | agent_profile:architect-alphonso, agent_profile:doctrine-daphne [pack-authoring], agent_profile:implementer-ivan, agent_profile:python-pedro [python], directive:DIRECTIVE_052, procedure:post-merge-arch-gate-adjudication |
| `DIRECTIVE_044` | foundation | cross-cutting engineering directive; census foundation list | agent_profile:architect-alphonso, agent_profile:doctrine-daphne [pack-authoring], agent_profile:implementer-ivan, agent_profile:python-pedro [python], directive:DIRECTIVE_052 |
| `DIRECTIVE_045` | foundation | cross-cutting engineering directive; census foundation list | agent_profile:implementer-ivan, agent_profile:python-pedro [python], directive:DIRECTIVE_046, procedure:mission-wrap-up-sequence [internal], tactic:pr-agent-worktree-isolation |
| `DIRECTIVE_046` | foundation | cross-cutting engineering directive; census foundation list | action:software-dev/implement, action:software-dev/review |
| `DIRECTIVE_048` | foundation | cross-cutting engineering directive; census foundation list | agent_profile:lexical-larry [writing], agent_profile:scribe-sally [writing] |
| `DIRECTIVE_049` | foundation | cross-cutting engineering directive; census foundation list | agent_profile:minutes-mahad [writing] |
| `DIRECTIVE_050` | foundation | cross-cutting engineering directive; census foundation list | agent_profile:minutes-mahad [writing], procedure:meeting-minutes-pipeline [writing] |
| `DIRECTIVE_051` | foundation | cross-cutting engineering directive; census foundation list | action:software-dev/implement, action:software-dev/plan, action:software-dev/review, agent_profile:architect-alphonso, agent_profile:drupal-dries [drupal], agent_profile:frontend-freddy [javascript] +5 more |
| `DIRECTIVE_052` | foundation | cross-cutting engineering directive; census foundation list | procedure:disciplined-defect-diagnosis, procedure:test-first-bug-fixing |
| `DIRECTIVE_053` | foundation | cross-cutting engineering directive; census foundation list | agent_profile:planner-priti |
| `DISCIPLINED_REFACTORING` | foundation | cross-cutting engineering directive; census foundation list | agent_profile:frontend-freddy [javascript], agent_profile:generic-agent, agent_profile:implementer-ivan, agent_profile:java-jenny [java], agent_profile:node-norris [javascript], agent_profile:python-pedro [python] +2 more |
| `RECONCILE_CHANGE_SCOPE_TENSIONS` | foundation | cross-cutting engineering directive; census foundation list | directive:DIRECTIVE_052, styleguide:boring-code-review, tactic:avoid-gold-plating, tactic:easy-to-change |
| `RED_MAIN_RELEASE_DISCIPLINE` | foundation | cross-cutting engineering directive; census foundation list | directive:DIRECTIVE_030, procedure:test-first-bug-fixing |

### paradigm (4)

| Artifact | Ruling | Reason | Inbound referrers |
|---|---|---|---|
| `behaviour-driven-development` | foundation | census foundation paradigm | — |
| `deep-module-design` | foundation | census foundation paradigm | mission_type:plan, tactic:deepening-opportunity-assessment, tactic:interface-variation-design |
| `specification-by-example` | foundation | census foundation paradigm | — |
| `trunk-based` | foundation | census foundation paradigm | action:software-dev/implement, action:software-dev/review, mission_step_contract:software-dev/implement |

### styleguide (5)

| Artifact | Ruling | Reason | Inbound referrers |
|---|---|---|---|
| `boring-code-review` | foundation | census foundation styleguide | action:software-dev/implement, action:software-dev/review, directive:DIRECTIVE_039 [cut], tactic:generated-code-stewardship |
| `kitty-glossary-writing` | foundation | census foundation (glossary is foundation) although filed under styleguides/writing/ | action:documentation/retrospect, action:research/retrospect, action:software-dev/retrospect, directive:DIRECTIVE_032, procedure:glossary-maintenance-workflow, tactic:glossary-curation-interview |
| `quadruple-a-test-format` | foundation | census foundation styleguide | directive:DIRECTIVE_041, styleguide:testing-principles |
| `test-desiderata-and-boundaries` | foundation | census foundation styleguide | directive:DIRECTIVE_030, styleguide:testing-principles, tactic:bdd-scenario-formulation, tactic:test-scaffolding-as-design-smell, tactic:test-to-system-reconstruction |
| `testing-principles` | foundation | census foundation styleguide | directive:DIRECTIVE_030, directive:DIRECTIVE_041, tactic:bdd-scenario-formulation, tactic:function-over-form-testing, tactic:test-to-system-reconstruction |

### toolguide (5)

| Artifact | Ruling | Reason | Inbound referrers |
|---|---|---|---|
| `efficient-local-tooling` | foundation | census foundation toolguide | action:software-dev/implement, directive:DIRECTIVE_028 |
| `execution-lanes` | foundation | census lists execution-lanes (as paradigm); now a toolguide delegated by the implement step contract. NB missing from pack-manifest (#182 drift) | action:software-dev/implement, action:software-dev/review, mission_step_contract:software-dev/implement |
| `git-agent-commit-signing` | foundation | census foundation toolguide | directive:DIRECTIVE_029 |
| `git-worktree-pr-workflow` | foundation | census foundation toolguide | — |
| `powershell-syntax` | foundation | census: stays in foundation until a second PowerShell artifact exists | — |

### tactic (61)

| Artifact | Ruling | Reason | Inbound referrers |
|---|---|---|---|
| `acceptance-criteria-non-vacuity` | foundation | census: testing/* foundation | action:software-dev/review, tactic:acceptance-test-first, tactic:atdd-adversarial-acceptance |
| `acceptance-test-first` | foundation | census: testing/* foundation | action:software-dev/implement, action:software-dev/review, agent_profile:java-jenny [java], directive:DIRECTIVE_041, mission_step_contract:software-dev/implement, paradigm:specification-by-example +15 more |
| `adversarial-qa-handoff` | foundation | census: root tactics are foundation | directive:DIRECTIVE_030, directive:DIRECTIVE_039 [cut] |
| `ammerse-impact-analysis` | foundation | census: analysis tactics not taken by architecture | procedure:situational-assessment, tactic:reference-architectural-patterns |
| `analysis-extract-before-interpret` | foundation | census: analysis tactics not taken by architecture | — |
| `architectural-gate-non-vacuity` | foundation | census: root tactics are foundation | directive:DIRECTIVE_043, procedure:post-merge-arch-gate-adjudication |
| `atdd-adversarial-acceptance` | foundation | census: testing/* foundation | directive:DIRECTIVE_034, paradigm:specification-by-example, procedure:example-mapping-workshop |
| `autonomous-operation-protocol` | foundation | census: root tactics are foundation | action:documentation/retrospect, action:research/retrospect, action:software-dev/implement, action:software-dev/retrospect, action:software-dev/review, directive:DIRECTIVE_044 +1 more |
| `avoid-gold-plating` | foundation | census: root tactics are foundation | styleguide:boring-code-review, tactic:deepening-opportunity-assessment |
| `bdd-scenario-formulation` | foundation | census: testing/* foundation | agent_profile:frontend-freddy [javascript], agent_profile:java-jenny [java], agent_profile:node-norris [javascript], paradigm:behaviour-driven-development, procedure:bdd-scenario-lifecycle, tactic:development-bdd +2 more |
| `black-box-integration-testing` | foundation | census: testing/* foundation | action:software-dev/implement, tactic:formalized-constraint-testing, tactic:secure-design-checklist |
| `canonical-source-unification` | foundation | census: root tactics are foundation | directive:DIRECTIVE_044 |
| `chain-of-responsibility-rule-pipeline` | foundation | census: code-patterns/* foundation | — |
| `change-apply-smallest-viable-diff` | foundation | census: root tactics are foundation | action:software-dev/implement, directive:DIRECTIVE_025, directive:RECONCILE_CHANGE_SCOPE_TENSIONS, mission_step_contract:software-dev/implement, procedure:refactoring, tactic:code-review-incremental |
| `clean-linear-commit-history` | foundation | census: root tactics are foundation | directive:DIRECTIVE_046, procedure:mission-wrap-up-sequence [internal], tactic:pr-agent-worktree-isolation, toolguide:git-worktree-pr-workflow |
| `code-documentation-analysis` | foundation | census: analysis tactics not taken by architecture | directive:USE_C4_MODEL_TECHNIQUES, tactic:context-boundary-inference, tactic:terminology-extraction-mapping |
| `code-review-incremental` | foundation | census: root tactics are foundation | agent_profile:debugger-debbie, agent_profile:reviewer-renata, procedure:adversarial-squad-deployment, tactic:five-paradigm-parallel-debugging, tactic:reverse-speccing, tactic:secure-design-checklist |
| `connascence-analysis` | foundation | census: analysis tactics not taken by architecture | procedure:legacy-codebase-triage, tactic:forensic-repository-audit |
| `delete-the-assertion-not-the-test` | foundation | census: testing/* foundation | agent_profile:python-pedro [python], agent_profile:reviewer-renata, directive:DIRECTIVE_041, paradigm:brownfield-onboarding [cut], procedure:development-assist-test-cleanup |
| `dialectic-research` | foundation | census: analysis tactics not taken by architecture | mission_type:research, styleguide:research-citation-discipline [writing] |
| `easy-to-change` | foundation | census: root tactics are foundation | styleguide:boring-code-review, tactic:avoid-gold-plating, tactic:deepening-opportunity-assessment |
| `eisenhower-prioritisation` | foundation | census: root tactics are foundation | action:plan/plan, action:plan/review, mission_type:plan, procedure:legacy-codebase-triage, procedure:situational-assessment, tactic:forensic-repository-audit +1 more |
| `five-paradigm-parallel-debugging` | foundation | census: root tactics are foundation | agent_profile:debugger-debbie, directive:DIRECTIVE_040 |
| `focused-function-complexity-check` | foundation | census: root tactics are foundation | action:software-dev/implement, directive:DIRECTIVE_039 [cut] |
| `forensic-repository-audit` | foundation | census: analysis tactics not taken by architecture | mission_type:research, paradigm:brownfield-onboarding [cut], procedure:legacy-codebase-triage, tactic:split-brain-authority-detection |
| `formalized-constraint-testing` | foundation | census: testing/* foundation | directive:DIRECTIVE_034 |
| `frozen-baseline-shrink-only-ratchet` | foundation | census: root tactics are foundation | directive:DIRECTIVE_025, directive:DIRECTIVE_043, tactic:architectural-gate-non-vacuity |
| `function-over-form-testing` | foundation | census: testing/* foundation | action:software-dev/implement, styleguide:test-desiderata-and-boundaries, tactic:chain-of-responsibility-rule-pipeline, tactic:test-scaffolding-as-design-smell |
| `generated-code-stewardship` | foundation | census: root tactics are foundation | action:software-dev/implement, directive:DIRECTIVE_039 [cut] |
| `input-validation-fail-fast` | foundation | census: root tactics are foundation | action:software-dev/implement, tactic:atdd-adversarial-acceptance |
| `lane-recovery` | foundation | census: root tactics are foundation | action:software-dev/implement, toolguide:git-worktree-pr-workflow |
| `model-task-routing` | foundation | census: root tactics are foundation | directive:DIRECTIVE_044, procedure:adversarial-squad-deployment |
| `moscow-scoping-lens` | foundation | census: root tactics are foundation | action:plan/plan, action:plan/review, mission_type:plan |
| `no-parallel-duplicate-test-runs` | foundation | census: testing/* foundation | directive:DIRECTIVE_030 |
| `occurrence-classification-workflow` | foundation | census: root tactics are foundation | directive:DIRECTIVE_035 |
| `op-or-mission-selection` | foundation | census: root tactics are foundation | directive:DIRECTIVE_053 |
| `ownership-map-leeway` | foundation | census: root tactics are foundation | directive:DIRECTIVE_044, styleguide:planning-and-tracking |
| `pr-agent-worktree-isolation` | foundation | census: root tactics are foundation | directive:DIRECTIVE_043, toolguide:git-worktree-pr-workflow |
| `premortem-risk-identification` | foundation | census: analysis tactics not taken by architecture | action:documentation/discover, action:documentation/validate, action:plan/plan, action:plan/review, action:research/scoping, action:research/synthesis +8 more |
| `quality-gate-verification` | foundation | census: testing/* foundation | action:software-dev/implement, action:software-dev/review, mission_step_contract:plan/review, mission_step_contract:research/output, mission_step_contract:software-dev/review, tactic:adversarial-qa-handoff +2 more |
| `requirements-validation-workflow` | foundation | census: analysis tactics not taken by architecture | action:documentation/accept, action:documentation/audit, action:documentation/design, action:documentation/discover, action:documentation/generate, action:documentation/publish +30 more |
| `reverse-speccing` | foundation | census: analysis tactics not taken by architecture | agent_profile:reviewer-renata, mission_type:research, paradigm:brownfield-onboarding [cut], procedure:example-mapping-workshop, tactic:test-to-system-reconstruction |
| `review-intent-and-risk-first` | foundation | census: root tactics are foundation | action:software-dev/review, agent_profile:debugger-debbie, agent_profile:paula-patterns, directive:DIRECTIVE_046, mission_step_contract:plan/review, mission_step_contract:research/output +7 more |
| `reviewer-implementer-role-separation` | foundation | census: root tactics are foundation | directive:DIRECTIVE_044, directive:DIRECTIVE_046, styleguide:planning-and-tracking |
| `safe-to-fail-experiment` | foundation | census: analysis tactics not taken by architecture | mission_type:research, procedure:situational-assessment, procedure:spike-timebox-policy |
| `secure-design-checklist` | foundation | census: root tactics are foundation | action:software-dev/implement, directive:DIRECTIVE_050, tactic:dependency-hygiene, tactic:secure-regex-catastrophic-backtracking, tactic:supply-chain-install-safety |
| `secure-regex-catastrophic-backtracking` | foundation | census: root tactics are foundation | — |
| `split-brain-authority-detection` | foundation | census: analysis tactics not taken by architecture | tactic:semantic-compression-semantic-consolidation [refactoring] |
| `stopping-conditions` | foundation | census: root tactics are foundation | action:documentation/retrospect, action:research/retrospect, action:software-dev/implement, action:software-dev/retrospect, action:software-dev/review, mission_step_contract:plan/review +3 more |
| `supply-chain-install-safety` | foundation | census: security/* foundation | action:software-dev/implement, action:software-dev/plan, action:software-dev/review, agent_profile:architect-alphonso, agent_profile:drupal-dries [drupal], agent_profile:frontend-freddy [javascript] +10 more |
| `tdd-red-green-refactor` | foundation | census: testing/* foundation | action:software-dev/implement, agent_profile:drupal-dries [drupal], agent_profile:frontend-freddy [javascript], agent_profile:java-jenny [java], agent_profile:node-norris [javascript], agent_profile:python-pedro [python] +10 more |
| `terminology-extraction-mapping` | foundation | census: analysis tactics not taken by architecture | agent_profile:lexical-larry [writing], procedure:glossary-maintenance-workflow, toolguide:contextive [architecture] |
| `test-boundaries-by-responsibility` | foundation | census: testing/* foundation | action:software-dev/implement, procedure:test-first-bug-fixing, styleguide:test-desiderata-and-boundaries, styleguide:testing-principles, tactic:atdd-adversarial-acceptance, tactic:black-box-integration-testing +4 more |
| `test-minimisation` | foundation | census: testing/* foundation | styleguide:testing-principles, tactic:formalized-constraint-testing, tactic:work-package-completion-validation |
| `test-pyramid-progression` | foundation | census: testing/* foundation | styleguide:testing-principles, tactic:testing-select-appropriate-level |
| `test-readability-clarity-check` | foundation | census: testing/* foundation | agent_profile:reviewer-renata, directive:DIRECTIVE_041 |
| `test-scaffolding-as-design-smell` | foundation | census: testing/* foundation | agent_profile:python-pedro [python], agent_profile:randy-reducer [refactoring], agent_profile:reviewer-renata |
| `test-to-system-reconstruction` | foundation | census: testing/* foundation | paradigm:brownfield-onboarding [cut] |
| `testing-select-appropriate-level` | foundation | census: testing/* foundation | action:software-dev/implement, procedure:disciplined-defect-diagnosis, styleguide:testing-principles |
| `work-package-completion-validation` | foundation | census: root tactics are foundation | directive:DIRECTIVE_030 |
| `zombies-tdd` | foundation | census: testing/* foundation | directive:DIRECTIVE_041, tactic:delete-the-assertion-not-the-test |

### procedure (49)

| Artifact | Ruling | Reason | Inbound referrers |
|---|---|---|---|
| `adversarial-squad-deployment` | foundation | ADR-0053 d29(c): product guidance, not internal | agent_profile:planner-priti, agent_profile:reviewer-renata, directive:DIRECTIVE_043, directive:DIRECTIVE_046, directive:DIRECTIVE_052, paradigm:brownfield-onboarding [cut] +6 more |
| `agent-commit-signing` | foundation | follows its owning directive DIRECTIVE_029 | directive:DIRECTIVE_029 |
| `agent-self-declaration` | foundation | follows its owning directive DIRECTIVE_049 | directive:DIRECTIVE_049 |
| `bdd-scenario-lifecycle` | foundation | ADR-0052 d5 fit procedure (or d6 re-shape that keeps it product doctrine); used by shipped missions/foundation profiles | paradigm:behaviour-driven-development |
| `bounded-context-alignment` | foundation | follows its owning directive DIRECTIVE_031 | directive:DIRECTIVE_031 |
| `bulk-edit-occurrence-mapping` | foundation | follows its owning directive DIRECTIVE_035 | directive:DIRECTIVE_035 |
| `canonical-source-discipline` | foundation | follows its owning directive DIRECTIVE_044 | directive:DIRECTIVE_044 |
| `change-scope-tension-resolution` | foundation | follows its owning directive RECONCILE_CHANGE_SCOPE_TENSIONS | directive:RECONCILE_CHANGE_SCOPE_TENSIONS |
| `component-boundary-definition` | foundation | follows its owning directive DIRECTIVE_001 | directive:DIRECTIVE_001 |
| `credential-exposure-prevention` | foundation | follows its owning directive DIRECTIVE_050 | directive:DIRECTIVE_050 |
| `decision-record-keeping` | foundation | follows its owning directive DIRECTIVE_003 | directive:DIRECTIVE_003 |
| `defect-class-construction-gate` | foundation | follows its owning directive DIRECTIVE_043 | directive:DIRECTIVE_043 |
| `development-assist-test-cleanup` | foundation | ADR-0053 d29(b) not taken: stays a fit product procedure | procedure:mission-wrap-up-sequence [internal], styleguide:test-desiderata-and-boundaries |
| `disciplined-defect-diagnosis` | foundation | ADR-0052 d5 fit procedure (or d6 re-shape that keeps it product doctrine); used by shipped missions/foundation profiles | action:software-dev/implement, action:software-dev/review, procedure:issue-triage-state-machine |
| `disciplined-refactoring-cycle` | foundation | follows its owning directive DISCIPLINED_REFACTORING | directive:DISCIPLINED_REFACTORING |
| `doctrine-version-change` | foundation | follows its owning directive DIRECTIVE_018 | directive:DIRECTIVE_018 |
| `domain-aware-decision-interview` | foundation | ADR-0052 d5 fit procedure (or d6 re-shape that keeps it product doctrine); used by shipped missions/foundation profiles | action:software-dev/plan, mission_type:research |
| `durable-fix-investigation` | foundation | follows its owning directive DIRECTIVE_052 | directive:DIRECTIVE_052 |
| `event-storming-discovery` | foundation | ADR-0052 d5 fit procedure (or d6 re-shape that keeps it product doctrine); used by shipped missions/foundation profiles | agent_profile:architect-alphonso, mission_type:research, procedure:example-mapping-workshop |
| `example-mapping-workshop` | foundation | ADR-0052 d5 fit procedure (or d6 re-shape that keeps it product doctrine); used by shipped missions/foundation profiles | directive:DIRECTIVE_034, mission_step_contract:software-dev/specify, procedure:bdd-scenario-lifecycle, tactic:development-bdd |
| `failing-test-triage` | foundation | follows its owning directive DIRECTIVE_041 | directive:DIRECTIVE_041 |
| `five-paradigm-structural-intervention` | foundation | follows its owning directive DIRECTIVE_040 | directive:DIRECTIVE_040 |
| `git-flow` | foundation | branching workflow delegated by implement/review step contracts. NB missing from pack-manifest (#182 drift) | action:software-dev/implement, action:software-dev/review, mission_step_contract:software-dev/implement |
| `glossary-maintenance-workflow` | foundation | ADR-0052 d5 fit procedure (or d6 re-shape that keeps it product doctrine); used by shipped missions/foundation profiles | agent_profile:lexical-larry [writing], procedure:migrate-project-guidance-to-spec-kitty-charter [pack-authoring] |
| `issue-triage-state-machine` | foundation | ADR-0052 d5 fit procedure (or d6 re-shape that keeps it product doctrine); used by shipped missions/foundation profiles | action:software-dev/tasks |
| `keep-change-local` | foundation | follows its owning directive DIRECTIVE_024, RECONCILE_CHANGE_SCOPE_TENSIONS | directive:DIRECTIVE_024, directive:RECONCILE_CHANGE_SCOPE_TENSIONS, procedure:change-scope-tension-resolution |
| `land-changes-via-pull-request` | foundation | follows its owning directive DIRECTIVE_045 | directive:DIRECTIVE_045 |
| `legacy-codebase-triage` | foundation | ADR-0052 d5 fit procedure (or d6 re-shape that keeps it product doctrine); used by shipped missions/foundation profiles | action:software-dev/implement, action:software-dev/review, paradigm:brownfield-onboarding [cut] |
| `local-tooling-selection` | foundation | follows its owning directive DIRECTIVE_028 | directive:DIRECTIVE_028 |
| `observable-contract-test-authoring` | foundation | follows its owning directive DIRECTIVE_041 | directive:DIRECTIVE_041 |
| `op-or-mission-lifecycle` | foundation | follows its owning directive DIRECTIVE_053 | directive:DIRECTIVE_053 |
| `post-merge-arch-gate-adjudication` | foundation | ADR-0053 d29(c): product guidance, not internal | directive:DIRECTIVE_045, procedure:mission-wrap-up-sequence [internal] |
| `read-intent-before-high-risk-operation` | foundation | follows its owning directive DIRECTIVE_045 | directive:DIRECTIVE_045, procedure:failing-test-triage |
| `readable-pr-preparation` | foundation | follows its owning directive DIRECTIVE_046 | directive:DIRECTIVE_046 |
| `red-first-bug-reproduction` | foundation | follows its owning directive DIRECTIVE_034, DIRECTIVE_041 | directive:DIRECTIVE_034, directive:DIRECTIVE_041 |
| `red-main-handling` | foundation | follows its owning directive RED_MAIN_RELEASE_DISCIPLINE | directive:RED_MAIN_RELEASE_DISCIPLINE |
| `refactoring` | foundation | ADR-0052 d5 fit procedure (or d6 re-shape that keeps it product doctrine); used by shipped missions/foundation profiles | action:software-dev/implement, action:software-dev/review, tactic:deepening-opportunity-assessment |
| `situational-assessment` | foundation | ADR-0052 d5 fit procedure (or d6 re-shape that keeps it product doctrine); used by shipped missions/foundation profiles | mission_type:research, procedure:domain-aware-decision-interview, procedure:legacy-codebase-triage |
| `specification-traceability-check` | foundation | follows its owning directive DIRECTIVE_010 | directive:DIRECTIVE_010 |
| `spike-timebox-policy` | foundation | ADR-0052 d5 fit procedure (or d6 re-shape that keeps it product doctrine); used by shipped missions/foundation profiles | agent_profile:researcher-robbie, mission_type:research |
| `targeted-staging` | foundation | follows its owning directive DIRECTIVE_033 | directive:DIRECTIVE_033 |
| `tech-debt-point-cut-triage` | foundation | follows its owning directive DIRECTIVE_025 | directive:DIRECTIVE_025, procedure:keep-change-local |
| `term-interpretation-alignment` | foundation | follows its owning directive DIRECTIVE_032 | directive:DIRECTIVE_032 |
| `test-and-typecheck-gate-run` | foundation | follows its owning directive DIRECTIVE_030 | directive:DIRECTIVE_030 |
| `test-first-bug-fixing` | foundation | ADR-0052 d5 fit procedure (or d6 re-shape that keeps it product doctrine); used by shipped missions/foundation profiles | action:software-dev/implement, action:software-dev/review, agent_profile:drupal-dries [drupal], agent_profile:frontend-freddy [javascript], agent_profile:implementer-ivan, agent_profile:java-jenny [java] +3 more |
| `test-first-cycle` | foundation | owned by DIRECTIVE_034 (and 039) | directive:DIRECTIVE_034, directive:DIRECTIVE_039 [cut] |
| `tidy-first-campsite-clean` | foundation | follows its owning directive DIRECTIVE_025, RECONCILE_CHANGE_SCOPE_TENSIONS | directive:DIRECTIVE_025, directive:RECONCILE_CHANGE_SCOPE_TENSIONS, procedure:change-scope-tension-resolution, procedure:keep-change-local |
| `touched-area-cleanup` | foundation | follows its owning directive DIRECTIVE_025, RECONCILE_CHANGE_SCOPE_TENSIONS | directive:DIRECTIVE_025, directive:RECONCILE_CHANGE_SCOPE_TENSIONS, procedure:change-scope-tension-resolution, procedure:keep-change-local |
| `version-freshness-check` | foundation | follows its owning directive DIRECTIVE_048 | directive:DIRECTIVE_048 |

### template (18)

| Artifact | Ruling | Reason | Inbound referrers |
|---|---|---|---|
| `agent-brief-template` | foundation | graph-only node, NO template file in the pack (defect to fix or drop); placed with its referrers: foundation tactics/procedures/doc-design action | procedure:issue-triage-state-machine |
| `ammerse-analysis-template` | foundation | graph-only node, NO template file in the pack (defect to fix or drop); placed with its referrers: foundation tactics/procedures/doc-design action | procedure:situational-assessment, tactic:ammerse-impact-analysis |
| `bounded-context-canvas-template` | foundation | graph-only node, NO template file in the pack (defect to fix or drop); placed with its referrers: foundation tactics/procedures/doc-design action | tactic:bounded-context-canvas-fill |
| `c4-component-mermaid-template` | foundation | graph-only node, NO template file in the pack (defect to fix or drop); placed with its referrers: foundation tactics/procedures/doc-design action | action:documentation/design, tactic:c4-zoom-in-architecture-documentation |
| `c4-container-mermaid-template` | foundation | graph-only node, NO template file in the pack (defect to fix or drop); placed with its referrers: foundation tactics/procedures/doc-design action | action:documentation/design, tactic:c4-zoom-in-architecture-documentation |
| `c4-context-mermaid-template` | foundation | graph-only node, NO template file in the pack (defect to fix or drop); placed with its referrers: foundation tactics/procedures/doc-design action | action:documentation/design, tactic:c4-zoom-in-architecture-documentation |
| `glossary-template` | foundation | graph-only node, NO template file in the pack (defect to fix or drop); placed with its referrers: foundation tactics/procedures/doc-design action | tactic:bounded-context-canvas-fill |
| `lightweight-prestudy-template` | foundation | graph-only node, NO template file in the pack (defect to fix or drop); placed with its referrers: foundation tactics/procedures/doc-design action | procedure:situational-assessment, tactic:problem-decomposition |
| `out-of-scope-record-template` | foundation | graph-only node, NO template file in the pack (defect to fix or drop); placed with its referrers: foundation tactics/procedures/doc-design action | procedure:issue-triage-state-machine |
| `plan/plan-plan-skeleton.md` | foundation | mission template; follows its mission type (d13 base templates) | action:plan/plan |
| `plan/plan-spec-skeleton.md` | foundation | mission template; follows its mission type (d13 base templates) | action:plan/specify |
| `quality-attribute-assessment-template` | foundation | graph-only node, NO template file in the pack (defect to fix or drop); placed with its referrers: foundation tactics/procedures/doc-design action | procedure:situational-assessment |
| `research/research-plan-template.md` | foundation | mission template; follows its mission type (d13 base templates) | action:research/methodology |
| `research/research-spec-template.md` | foundation | mission template; follows its mission type (d13 base templates) | action:research/scoping |
| `risk-identification-assessment-template` | foundation | graph-only node, NO template file in the pack (defect to fix or drop); placed with its referrers: foundation tactics/procedures/doc-design action | tactic:premortem-risk-identification |
| `software-dev/plan-template.md` | foundation | mission template; follows its mission type (d13 base templates) | action:software-dev/plan |
| `software-dev/spec-template.md` | foundation | mission template; follows its mission type (d13 base templates) | action:software-dev/specify |
| `system-context-canvas-template` | foundation | graph-only node, NO template file in the pack (defect to fix or drop); placed with its referrers: foundation tactics/procedures/doc-design action | procedure:situational-assessment, tactic:stakeholder-alignment |

### anti_pattern (13)

| Artifact | Ruling | Reason | Inbound referrers |
|---|---|---|---|
| `anemic-domain-model` | foundation | ADR-0052 d15: the 13 file-less graph nodes seed the general set in foundation | paradigm:domain-driven-design |
| `big-ball-of-mud` | foundation | ADR-0052 d15: the 13 file-less graph nodes seed the general set in foundation | paradigm:brownfield-onboarding [cut], paradigm:domain-driven-design |
| `big-bang-rewrite` | foundation | ADR-0052 d15: the 13 file-less graph nodes seed the general set in foundation | tactic:refactoring-strangler-fig [refactoring] |
| `big-upfront-design` | foundation | ADR-0052 d15: the 13 file-less graph nodes seed the general set in foundation | paradigm:brownfield-onboarding [cut], paradigm:c4-incremental-detail-modeling |
| `code-is-the-documentation` | foundation | ADR-0052 d15: the 13 file-less graph nodes seed the general set in foundation | paradigm:c4-incremental-detail-modeling |
| `database-driven-design` | foundation | ADR-0052 d15: the 13 file-less graph nodes seed the general set in foundation | paradigm:domain-driven-design |
| `feature-envy` | foundation | ADR-0052 d15: the 13 file-less graph nodes seed the general set in foundation | tactic:refactoring-move-method [refactoring] |
| `global-data` | foundation | ADR-0052 d15: the 13 file-less graph nodes seed the general set in foundation | tactic:refactoring-encapsulate-variable [refactoring] |
| `implicit-concept` | foundation | ADR-0052 d15: the 13 file-less graph nodes seed the general set in foundation | tactic:refactoring-extract-first-order-concept [refactoring] |
| `misplaced-field` | foundation | ADR-0052 d15: the 13 file-less graph nodes seed the general set in foundation | tactic:refactoring-move-field [refactoring] |
| `repeated-switches-on-state` | foundation | ADR-0052 d15: the 13 file-less graph nodes seed the general set in foundation | tactic:refactoring-state-pattern-for-behavior [refactoring] |
| `single-diagram-architecture` | foundation | ADR-0052 d15: the 13 file-less graph nodes seed the general set in foundation | paradigm:c4-incremental-detail-modeling |
| `unencapsulated-record` | foundation | ADR-0052 d15: the 13 file-less graph nodes seed the general set in foundation | tactic:refactoring-encapsulate-record [refactoring] |

### glossary_pack (1)

| Artifact | Ruling | Reason | Inbound referrers |
|---|---|---|---|
| `spec-kitty-core` | foundation | census + ADR-0048 d13: glossary is foundation | agent_profile:lexical-larry [writing] |

### mission_type (3)

| Artifact | Ruling | Reason | Inbound referrers |
|---|---|---|---|
| `plan` | foundation | ADR-0048 d13: shipped mission types + step contracts in foundation | — |
| `research` | foundation | ADR-0048 d13: shipped mission types + step contracts in foundation | — |
| `software-dev` | foundation | ADR-0048 d13: shipped mission types + step contracts in foundation | — |

### mission_step_contract (14)

| Artifact | Ruling | Reason | Inbound referrers |
|---|---|---|---|
| `plan/plan` | foundation | ADR-0048 d13: shipped mission types + step contracts in foundation | — |
| `plan/research` | foundation | ADR-0048 d13: shipped mission types + step contracts in foundation | — |
| `plan/review` | foundation | ADR-0048 d13: shipped mission types + step contracts in foundation | — |
| `plan/specify` | foundation | ADR-0048 d13: shipped mission types + step contracts in foundation | — |
| `research/gathering` | foundation | ADR-0048 d13: shipped mission types + step contracts in foundation | — |
| `research/methodology` | foundation | ADR-0048 d13: shipped mission types + step contracts in foundation | — |
| `research/output` | foundation | ADR-0048 d13: shipped mission types + step contracts in foundation | — |
| `research/scoping` | foundation | ADR-0048 d13: shipped mission types + step contracts in foundation | — |
| `research/synthesis` | foundation | ADR-0048 d13: shipped mission types + step contracts in foundation | — |
| `software-dev/implement` | foundation | ADR-0048 d13: shipped mission types + step contracts in foundation | — |
| `software-dev/plan` | foundation | ADR-0048 d13: shipped mission types + step contracts in foundation | — |
| `software-dev/review` | foundation | ADR-0048 d13: shipped mission types + step contracts in foundation | — |
| `software-dev/specify` | foundation | ADR-0048 d13: shipped mission types + step contracts in foundation | — |
| `software-dev/tasks` | foundation | ADR-0048 d13: shipped mission types + step contracts in foundation | — |

### action (16)

| Artifact | Ruling | Reason | Inbound referrers |
|---|---|---|---|
| `plan/plan` | foundation | ADR-0048 d13: shipped mission types + step contracts in foundation | mission_type:plan |
| `plan/research` | foundation | ADR-0048 d13: shipped mission types + step contracts in foundation | mission_type:plan |
| `plan/review` | foundation | ADR-0048 d13: shipped mission types + step contracts in foundation | mission_type:plan |
| `plan/specify` | foundation | ADR-0048 d13: shipped mission types + step contracts in foundation | mission_type:plan |
| `research/gathering` | foundation | ADR-0048 d13: shipped mission types + step contracts in foundation | mission_type:research |
| `research/methodology` | foundation | ADR-0048 d13: shipped mission types + step contracts in foundation | mission_type:research |
| `research/output` | foundation | ADR-0048 d13: shipped mission types + step contracts in foundation | mission_type:research |
| `research/retrospect` | foundation | ADR-0048 d13: shipped mission types + step contracts in foundation | — |
| `research/scoping` | foundation | ADR-0048 d13: shipped mission types + step contracts in foundation | mission_type:research |
| `research/synthesis` | foundation | ADR-0048 d13: shipped mission types + step contracts in foundation | mission_type:research |
| `software-dev/implement` | foundation | ADR-0048 d13: shipped mission types + step contracts in foundation | mission_type:software-dev |
| `software-dev/plan` | foundation | ADR-0048 d13: shipped mission types + step contracts in foundation | mission_type:software-dev |
| `software-dev/retrospect` | foundation | ADR-0048 d13: shipped mission types + step contracts in foundation | — |
| `software-dev/review` | foundation | ADR-0048 d13: shipped mission types + step contracts in foundation | mission_type:software-dev |
| `software-dev/specify` | foundation | ADR-0048 d13: shipped mission types + step contracts in foundation | mission_type:software-dev |
| `software-dev/tasks` | foundation | ADR-0048 d13: shipped mission types + step contracts in foundation | mission_type:software-dev |

## B. Uncontested → writing — 38

Inbound referrers: `[pack]` marks a referrer that would sit in a different pack (those edges need `<pack>::` qualification or relocation).

### agent_profile (6)

| Artifact | Ruling | Reason | Inbound referrers |
|---|---|---|---|
| `comms-cleo` | writing | writing/comms profile; census writing | agent_profile:lexical-larry, agent_profile:minutes-mahad, agent_profile:scribe-sally, agent_profile:synthesizer-sam |
| `diagram-daisy` | writing | writing/comms profile; census writing | — |
| `lexical-larry` | writing | writing/comms profile; census writing | agent_profile:analyst-annie [foundation] |
| `minutes-mahad` | writing | writing/comms profile; census writing | agent_profile:scribe-sally |
| `scribe-sally` | writing | writing/comms profile; census writing | agent_profile:minutes-mahad |
| `synthesizer-sam` | writing | writing/comms profile; census writing | agent_profile:comms-cleo |

### directive (4)

| Artifact | Ruling | Reason | Inbound referrers |
|---|---|---|---|
| `ACTION_ITEM_ATTRIBUTION` | writing | docs/comms directive; census writing list | agent_profile:minutes-mahad, procedure:meeting-minutes-pipeline |
| `DIRECTIVE_042` | writing | docs/comms directive; census writing list | action:documentation/generate [foundation], directive:DIRECTIVE_047, mission_type:documentation [foundation], styleguide:publication-authority |
| `DIRECTIVE_047` | writing | docs/comms directive; census writing list | agent_profile:analyst-annie [foundation], agent_profile:comms-cleo, agent_profile:minutes-mahad, agent_profile:scribe-sally, agent_profile:synthesizer-sam, procedure:meeting-minutes-pipeline +2 more |
| `MINUTES_STAND_ALONE` | writing | docs/comms directive; census writing list | agent_profile:minutes-mahad, procedure:meeting-minutes-pipeline |

### styleguide (9)

| Artifact | Ruling | Reason | Inbound referrers |
|---|---|---|---|
| `common-docs` | writing | census writing styleguide | directive:DIRECTIVE_042, directive:DIRECTIVE_047, mission_type:documentation [foundation], styleguide:divio-type-discipline, styleguide:docs-accessibility, styleguide:docs-freshness-sla +2 more |
| `divio-type-discipline` | writing | census writing styleguide | mission_type:documentation [foundation] |
| `docs-accessibility` | writing | census writing styleguide | mission_type:documentation [foundation] |
| `docs-freshness-sla` | writing | census writing styleguide | mission_type:documentation [foundation] |
| `meeting-minutes-format` | writing | census writing styleguide | agent_profile:minutes-mahad, procedure:meeting-minutes-pipeline |
| `plain-language` | writing | census writing styleguide | mission_type:documentation [foundation] |
| `professional-communications` | writing | census writing styleguide | — |
| `publication-authority` | writing | census writing styleguide | mission_type:documentation [foundation], styleguide:docs-freshness-sla |
| `research-citation-discipline` | writing | census writing styleguide | mission_type:research [foundation] |

### toolguide (2)

| Artifact | Ruling | Reason | Inbound referrers |
|---|---|---|---|
| `mermaid-diagramming` | writing | census: 2 diagram toolguides -> writing | agent_profile:diagram-daisy, directive:USE_C4_MODEL_TECHNIQUES [foundation], mission_type:documentation [foundation], styleguide:docs-accessibility, tactic:architecture-diagram-review-checklist [foundation] |
| `plantuml-diagramming` | writing | census: 2 diagram toolguides -> writing | agent_profile:diagram-daisy, directive:USE_C4_MODEL_TECHNIQUES [foundation], mission_type:documentation [foundation], styleguide:docs-accessibility, tactic:architecture-diagram-review-checklist [foundation] |

### tactic (5)

| Artifact | Ruling | Reason | Inbound referrers |
|---|---|---|---|
| `common-docs-find` | writing | census: common-docs tactics leave foundation -> writing (with common-docs styleguide) | directive:DIRECTIVE_042, mission_type:documentation [foundation], styleguide:common-docs |
| `common-docs-scaffold` | writing | census: common-docs tactics leave foundation -> writing (with common-docs styleguide) | directive:DIRECTIVE_042, mission_type:documentation [foundation], styleguide:common-docs |
| `common-docs-write` | writing | census: common-docs tactics leave foundation -> writing (with common-docs styleguide) | directive:DIRECTIVE_042, mission_type:documentation [foundation], styleguide:common-docs |
| `documentation-curation-audit` | writing | census: communication/* -> writing | action:documentation/accept [foundation], action:documentation/validate [foundation] |
| `writing-audience-catalog` | writing | census: communication/* -> writing | agent_profile:comms-cleo, directive:DIRECTIVE_047 |

### procedure (7)

| Artifact | Ruling | Reason | Inbound referrers |
|---|---|---|---|
| `action-item-attribution-gate` | writing | follows its owning directive ACTION_ITEM_ATTRIBUTION | directive:ACTION_ITEM_ATTRIBUTION |
| `audience-oriented-drafting` | writing | follows its owning directive DIRECTIVE_047 | directive:DIRECTIVE_047 |
| `common-docs-page-authoring` | writing | follows its owning directive DIRECTIVE_042 | directive:DIRECTIVE_042 |
| `declare-page-audience` | writing | follows its owning directive DIRECTIVE_042, DIRECTIVE_047 | directive:DIRECTIVE_042, directive:DIRECTIVE_047 |
| `documentation-gap-prioritization` | writing | docs-maintenance procedure (ADR-0053 d29a re-home in curation); suggests docs-freshness-sla | mission_type:documentation [foundation], styleguide:docs-freshness-sla |
| `meeting-minutes-pipeline` | writing | ADR-0052 d6: becomes a writing mission type or a writing procedure; required by minutes-mahad | agent_profile:minutes-mahad, procedure:action-item-attribution-gate |
| `minutes-self-sufficiency-check` | writing | follows its owning directive MINUTES_STAND_ALONE | directive:MINUTES_STAND_ALONE |

### asset (5)

| Artifact | Ruling | Reason | Inbound referrers |
|---|---|---|---|
| `common-docs-structural-lint` | writing | Common Docs lint executable; goes with common-docs styleguide/DIRECTIVE_042 | directive:DIRECTIVE_042, styleguide:common-docs, tactic:common-docs-scaffold, tactic:common-docs-write |
| `writing-audience-automation-agent` | writing | census: audience assets -> writing | tactic:writing-audience-catalog |
| `writing-audience-line-manager` | writing | census: audience assets -> writing | tactic:writing-audience-catalog |
| `writing-audience-nontech-educator` | writing | census: audience assets -> writing | tactic:writing-audience-catalog |
| `writing-audience-software-engineer` | writing | census: audience assets -> writing | tactic:writing-audience-catalog |

## D. Stack / opt-in topical pack (not a built-in member) — 68

Inbound referrers: `[pack]` marks a referrer that would sit in a different pack (those edges need `<pack>::` qualification or relocation).

### agent_profile (7)

| Artifact | Ruling | Reason | Inbound referrers |
|---|---|---|---|
| `doctrine-daphne` | pack-authoring or internal (future) | census: "pack-curation profile" -> pack-authoring (or internal); sub-ruling which | — |
| `drupal-dries` | drupal (future) | stack profile | — |
| `frontend-freddy` | javascript (future) | stack profile (node/frontend) | agent_profile:node-norris |
| `java-jenny` | java (#5) | stack profile; #5 moves it | agent_profile:analyst-annie [foundation] |
| `node-norris` | javascript (future) | stack profile (node/frontend) | agent_profile:frontend-freddy |
| `python-pedro` | python (future) | stack profile | agent_profile:analyst-annie [foundation] |
| `randy-reducer` | refactoring (future) | census refactoring | — |

### directive (1)

| Artifact | Ruling | Reason | Inbound referrers |
|---|---|---|---|
| `USE_MUTATION_TESTING_TO_VALIDATE_TEST_QUALITY` | qa (exists) | testing extra; census folds into qa | agent_profile:debugger-debbie [foundation], agent_profile:frontend-freddy [javascript], agent_profile:generic-agent [foundation], agent_profile:implementer-ivan [foundation], agent_profile:java-jenny [java], agent_profile:node-norris [javascript] +4 more |

### paradigm (2)

| Artifact | Ruling | Reason | Inbound referrers |
|---|---|---|---|
| `atomic-design` | javascript (future) | census: frontend part of javascript stack pack | tactic:atomic-design-review-checklist |
| `semantic-compression` | refactoring (future) | census refactoring | tactic:semantic-compression-abstraction-extraction, tactic:semantic-compression-behavioral-boundary-mapping, tactic:semantic-compression-dead-weight-elimination, tactic:semantic-compression-equivalence-verification, tactic:semantic-compression-redundancy-discovery, tactic:semantic-compression-semantic-consolidation |

### styleguide (10)

| Artifact | Ruling | Reason | Inbound referrers |
|---|---|---|---|
| `css-conventions` | javascript (future) | stack (not in census, added after 1060bfc; node/frontend) | agent_profile:frontend-freddy, styleguide:html-conventions |
| `deployable-skill-authoring` | pack-authoring (future) | census pack-authoring | procedure:onboard-external-agent-to-pack |
| `drupal-conventions` | drupal (future) | stack | agent_profile:drupal-dries |
| `drupal-security-performance` | drupal (future) | stack | agent_profile:drupal-dries, styleguide:drupal-conventions |
| `html-conventions` | javascript (future) | stack (not in census, added after 1060bfc; node/frontend) | agent_profile:frontend-freddy |
| `java-conventions` | java (#5) | stack styleguide; #5 | agent_profile:java-jenny, tactic:formalized-constraint-testing [foundation] |
| `mutation-aware-test-design` | qa (exists) | census testing extras -> qa | directive:USE_MUTATION_TESTING_TO_VALIDATE_TEST_QUALITY, styleguide:test-desiderata-and-boundaries [foundation] |
| `python-conventions` | python (future) | stack | agent_profile:python-pedro, tactic:input-validation-fail-fast [foundation] |
| `tiered-standards` | internal (exists) | census moves to internal | directive:DIRECTIVE_030 [foundation], styleguide:planning-and-tracking [foundation] |
| `typescript-conventions` | javascript (future) | stack (not in census, added after 1060bfc; node/frontend) | agent_profile:frontend-freddy, agent_profile:node-norris |

### toolguide (11)

| Artifact | Ruling | Reason | Inbound referrers |
|---|---|---|---|
| `contextive` | architecture (future) | census architecture | tactic:bounded-context-canvas-fill [foundation] |
| `drupal-review-checks` | drupal (future) | stack | styleguide:drupal-conventions |
| `gherkin` | qa (exists) | census testing extras -> qa | directive:DIRECTIVE_034 [foundation], paradigm:behaviour-driven-development [foundation], procedure:bdd-scenario-lifecycle [foundation], tactic:bdd-scenario-formulation [foundation] |
| `java-supply-chain` | java (#5) | stack; #5 | tactic:supply-chain-install-safety [foundation] |
| `javascript-supply-chain` | javascript (future) | stack | styleguide:typescript-conventions, tactic:supply-chain-install-safety [foundation] |
| `maven-review-checks` | java (#5) | stack; #5 | styleguide:java-conventions |
| `python-mutation-tools` | python (future) | stack | directive:USE_MUTATION_TESTING_TO_VALIDATE_TEST_QUALITY [qa], tactic:mutation-testing-workflow [qa] |
| `python-review-checks` | python (future) | stack | styleguide:python-conventions |
| `python-supply-chain` | python (future) | stack | tactic:supply-chain-install-safety [foundation] |
| `sonar` | qa (exists) | census testing extras -> qa | directive:DIRECTIVE_030 [foundation] |
| `typescript-mutation-tools` | javascript (future) | stack | directive:USE_MUTATION_TESTING_TO_VALIDATE_TEST_QUALITY [qa], styleguide:typescript-conventions, tactic:mutation-testing-workflow [qa] |

### tactic (28)

| Artifact | Ruling | Reason | Inbound referrers |
|---|---|---|---|
| `atomic-design-review-checklist` | javascript (future) | census: atomic-design state and review tactics go with frontend | — |
| `atomic-state-ownership` | javascript (future) | census: atomic-design state and review tactics go with frontend | tactic:atomic-design-review-checklist, tactic:compositional-stream-boundaries |
| `compositional-stream-boundaries` | javascript (future) | census: atomic-design state and review tactics go with frontend | tactic:atomic-design-review-checklist |
| `cross-cutting-state-via-store` | javascript (future) | census: atomic-design state and review tactics go with frontend | tactic:atomic-design-review-checklist, tactic:atomic-state-ownership |
| `refactoring-change-function-declaration` | refactoring (future) | census refactoring | procedure:refactoring [foundation] |
| `refactoring-combine-functions-into-transform` | refactoring (future) | census refactoring | procedure:refactoring [foundation] |
| `refactoring-conditional-to-strategy` | refactoring (future) | census refactoring | tactic:refactoring-guard-clauses-before-polymorphism, tactic:refactoring-state-pattern-for-behavior |
| `refactoring-consolidate-conditional-expression` | refactoring (future) | census refactoring | procedure:refactoring [foundation] |
| `refactoring-encapsulate-record` | refactoring (future) | census refactoring | directive:DISCIPLINED_REFACTORING [foundation] |
| `refactoring-encapsulate-variable` | refactoring (future) | census refactoring | directive:DISCIPLINED_REFACTORING [foundation], tactic:refactoring-encapsulate-record |
| `refactoring-extract-class-by-responsibility-split` | refactoring (future) | census refactoring | procedure:refactoring [foundation] |
| `refactoring-extract-first-order-concept` | refactoring (future) | census refactoring | directive:DISCIPLINED_REFACTORING [foundation], tactic:chain-of-responsibility-rule-pipeline [foundation], tactic:refactoring-move-method, tactic:semantic-compression-abstraction-extraction |
| `refactoring-guard-clauses-before-polymorphism` | refactoring (future) | census refactoring | tactic:chain-of-responsibility-rule-pipeline [foundation], tactic:focused-function-complexity-check [foundation] |
| `refactoring-inline-temp` | refactoring (future) | census refactoring | procedure:refactoring [foundation] |
| `refactoring-introduce-null-object` | refactoring (future) | census refactoring | procedure:refactoring [foundation] |
| `refactoring-move-field` | refactoring (future) | census refactoring | directive:DISCIPLINED_REFACTORING [foundation] |
| `refactoring-move-method` | refactoring (future) | census refactoring | directive:DISCIPLINED_REFACTORING [foundation], tactic:refactoring-move-field |
| `refactoring-replace-magic-number-with-symbolic-constant` | refactoring (future) | census refactoring | procedure:refactoring [foundation] |
| `refactoring-replace-temp-with-query` | refactoring (future) | census refactoring | procedure:refactoring [foundation] |
| `refactoring-retry-pattern` | refactoring (future) | census refactoring | procedure:refactoring [foundation] |
| `refactoring-state-pattern-for-behavior` | refactoring (future) | census refactoring | directive:DISCIPLINED_REFACTORING [foundation] |
| `refactoring-strangler-fig` | refactoring (future) | census refactoring | directive:DISCIPLINED_REFACTORING [foundation], tactic:anti-corruption-layer [foundation], tactic:context-mapping-classification [foundation], tactic:refactoring-extract-first-order-concept, tactic:refactoring-move-method |
| `semantic-compression-abstraction-extraction` | refactoring (future) | census refactoring | agent_profile:randy-reducer |
| `semantic-compression-behavioral-boundary-mapping` | refactoring (future) | census refactoring | agent_profile:randy-reducer, tactic:semantic-compression-redundancy-discovery |
| `semantic-compression-dead-weight-elimination` | refactoring (future) | census refactoring | agent_profile:randy-reducer |
| `semantic-compression-equivalence-verification` | refactoring (future) | census refactoring | agent_profile:randy-reducer |
| `semantic-compression-redundancy-discovery` | refactoring (future) | census refactoring | agent_profile:randy-reducer |
| `semantic-compression-semantic-consolidation` | refactoring (future) | census refactoring | agent_profile:randy-reducer |

### procedure (5)

| Artifact | Ruling | Reason | Inbound referrers |
|---|---|---|---|
| `migrate-project-guidance-to-spec-kitty-charter` | pack-authoring (future) | census + ADR-0052 d6: become pack-authoring mission types | — |
| `mission-tracer-files` | internal (exists) | census + ADR-0052 d6 internal-pack candidates | directive:DIRECTIVE_045 [foundation], procedure:development-assist-test-cleanup [foundation], procedure:mission-wrap-up-sequence |
| `mission-wrap-up-sequence` | internal (exists) | census + ADR-0052 d6 internal-pack candidates | action:software-dev/review [foundation], directive:DIRECTIVE_046 [foundation] |
| `mutation-testing-review` | qa (exists) | follows its directive (036 / use-mutation-testing) into qa | directive:USE_MUTATION_TESTING_TO_VALIDATE_TEST_QUALITY |
| `onboard-external-agent-to-pack` | pack-authoring (future) | census + ADR-0052 d6: become pack-authoring mission types | agent_profile:doctrine-daphne |

### asset (1)

| Artifact | Ruling | Reason | Inbound referrers |
|---|---|---|---|
| `writing-audience-agentic-framework-core-team` | internal (exists) | census: the agentic-framework-core-team audience moves to internal | tactic:writing-audience-catalog [writing] |

### template (3)

| Artifact | Ruling | Reason | Inbound referrers |
|---|---|---|---|
| `decomposition-table-template` | pack-authoring (future) | graph-only node, NO template file in the pack (defect to fix or drop); placed with its referrers: onboard-external-agent-to-pack | procedure:onboard-external-agent-to-pack |
| `onboarded-artifact-set-template` | pack-authoring (future) | graph-only node, NO template file in the pack (defect to fix or drop); placed with its referrers: onboard-external-agent-to-pack | procedure:onboard-external-agent-to-pack |
| `source-agent-dossier-template` | pack-authoring (future) | graph-only node, NO template file in the pack (defect to fix or drop); placed with its referrers: onboard-external-agent-to-pack | procedure:onboard-external-agent-to-pack |

## C. Stays in built-in, and files that are not graph nodes

| File(s) | Ruling | Note |
|---|---|---|
| `pack.yaml` | built-in (rewrite) | keeps `pack_id 01ARWG13C000000000000000FG`, `pack_level: built-in`; adds `depends_on` foundation + writing with exact pins (ADR-0048 d17); keeps `fallback_profile: generic-agent` (ADR-0068 d2/d5). foundation/writing need new tool-minted pack_ids. |
| `pack.md` | built-in (rewrite) | describe it as the distribution pack. |
| `pack-manifest.yaml` | regenerate per pack | never hand-edit (#190). Drift today: `procedures/git-flow.procedure.yaml` and `toolguides/execution-lanes.toolguide.yaml` exist on disk and in the graph but are **not in the manifest** (#182). Manifest kinds cover 9 kinds only (no mission types, step contracts, templates, actions). |
| `presets/default.yaml`, `presets/minimal.yaml` | built-in | ADR-0048 d12. Every id they name lands in foundation (minimal: DIRECTIVE_001/010/024/028/030, acceptance-test-first; default: the four mission types). Caveat for another researcher: `default` relies on "absent key = unrestricted", which ADR-0053 d10 reverses at the split. |
| `policy.yaml` | **E** | see generic-agent cluster. |
| `*.graph.yaml` (14 files) | split | each edge goes to the pack of its source node (bare inside a pack); P1/P2 edges are relocated into the target pack's graph with a qualified source; edges into cut candidates are dropped. |
| `skills/.gitkeep` | drop | census: "the empty skills/ directory" is a cut. |
| `missions/**` non-node files (step prompts/guidelines, mission templates incl. divio, generators, research CSVs, READMEs; 112 files) | follow their mission type → foundation (documentation's go with E-DOC) | no prose reference to writing artifacts found in them (grep). |
| `templates/writing/meeting-minutes.md`, `meeting-discussion-notes.md` | writing | census "the 2 meeting templates"; not graph nodes. |
| `assets/docs_structural_lint.py` (+ `.asset.yaml`, `docs_structural_lint.config.yaml`) | writing | = `asset:common-docs-structural-lint`. |
| `assets/audiences/*.md` + sidecars, `assets/audiences/README.md` | writing (agentic-framework-core-team → internal) | census. |
| `assets/README.md`, `agent_profiles/README.md`, `missions/README.md` | foundation (copy/adapt for writing) | |
| `styleguides/writing/README.md` | writing | NB `kitty-glossary-writing` lives in this dir but is ruled foundation (census). |
| `toolguides/*.guide.md` (19) | follow their toolguide | |

## Edges that cross the proposed boundaries

Computed with every E item at its recommended placement. Strong = `requires`, `scope`, `delegates_to`, `instantiates`, `specializes_from`, profile `*-references`; weak = `suggests`, `rejects`, tension edges, profile `collaboration` ids.

| Class | Edges | Strong | Weak | Action |
|---|---|---|---|---|
| OK1: writing -> foundation (qualify foundation::) | 45 | 28 | 17 | qualify target `foundation::` in writing; requires writing depends_on foundation |
| OK2: opt-in -> member (qualify) | 199 | 158 | 41 | qualify (`foundation::`/`writing::`); fine |
| P1: foundation -> writing (reverse; cycle risk) | 25 | 19 | 6 | **problem**: lower→higher member; relocate into writing's graph (or move artifact) |
| P2: member -> opt-in pack (outside closure) | 48 | 1 | 47 | **problem**: target outside the member's closure; relocate into the opt-in pack's graph |
| P3: opt-in -> other opt-in | 9 | 0 | 9 | opt-in pack needs depends_on on the other opt-in pack, or relocate/drop |
| X2: edge out of a cut candidate (drops with it) | 20 | 10 | 10 | drops with the cut |
| X: edge into a cut candidate | 4 | 1 | 3 | drop edge (or keep the target) |

**No edge points at `built-in`** (it holds nothing) and none at `spdd`, so no member→aggregator dependency arises from the graph. The aggregator risk is in the *other packs*: see § External `built-in::` references.

### P1: foundation -> writing (reverse; cycle risk) (25)

| Strength | Source | Relation | Target | Target pack | Carrier |
|---|---|---|---|---|---|
| strong | `action:documentation/accept` (foundation) | scope | `tactic:documentation-curation-audit` | writing | graph |
| strong | `action:documentation/generate` (foundation) | scope | `directive:DIRECTIVE_042` | writing | graph |
| strong | `action:documentation/validate` (foundation) | scope | `tactic:documentation-curation-audit` | writing | graph |
| strong | `agent_profile:analyst-annie` (foundation) | requires | `directive:DIRECTIVE_047` | writing | graph |
| strong | `agent_profile:analyst-annie` (foundation) | directive-references | `directive:DIRECTIVE_047` | writing | profile yaml |
| strong | `mission_type:documentation` (foundation) | scope | `directive:DIRECTIVE_042` | writing | graph |
| strong | `mission_type:documentation` (foundation) | scope | `procedure:documentation-gap-prioritization` | writing | graph |
| strong | `mission_type:documentation` (foundation) | scope | `styleguide:common-docs` | writing | graph |
| strong | `mission_type:documentation` (foundation) | scope | `styleguide:divio-type-discipline` | writing | graph |
| strong | `mission_type:documentation` (foundation) | scope | `styleguide:docs-accessibility` | writing | graph |
| strong | `mission_type:documentation` (foundation) | scope | `styleguide:docs-freshness-sla` | writing | graph |
| strong | `mission_type:documentation` (foundation) | scope | `styleguide:plain-language` | writing | graph |
| strong | `mission_type:documentation` (foundation) | scope | `styleguide:publication-authority` | writing | graph |
| strong | `mission_type:documentation` (foundation) | scope | `tactic:common-docs-find` | writing | graph |
| strong | `mission_type:documentation` (foundation) | scope | `tactic:common-docs-scaffold` | writing | graph |
| strong | `mission_type:documentation` (foundation) | scope | `tactic:common-docs-write` | writing | graph |
| strong | `mission_type:documentation` (foundation) | scope | `toolguide:mermaid-diagramming` | writing | graph |
| strong | `mission_type:documentation` (foundation) | scope | `toolguide:plantuml-diagramming` | writing | graph |
| strong | `mission_type:research` (foundation) | scope | `styleguide:research-citation-discipline` | writing | graph |
| weak | `agent_profile:analyst-annie` (foundation) | collab.handoff-from | `agent_profile:lexical-larry` | writing | profile yaml |
| weak | `agent_profile:analyst-annie` (foundation) | collab.works-with | `agent_profile:lexical-larry` | writing | profile yaml |
| weak | `directive:USE_C4_MODEL_TECHNIQUES` (foundation) | suggests | `toolguide:mermaid-diagramming` | writing | graph |
| weak | `directive:USE_C4_MODEL_TECHNIQUES` (foundation) | suggests | `toolguide:plantuml-diagramming` | writing | graph |
| weak | `tactic:architecture-diagram-review-checklist` (foundation) | suggests | `toolguide:mermaid-diagramming` | writing | graph |
| weak | `tactic:architecture-diagram-review-checklist` (foundation) | suggests | `toolguide:plantuml-diagramming` | writing | graph |

### P2: member -> opt-in pack (outside closure) (48)

| Strength | Source | Relation | Target | Target pack | Carrier |
|---|---|---|---|---|---|
| strong | `action:software-dev/review` (foundation) | scope | `procedure:mission-wrap-up-sequence` | internal | graph |
| weak | `agent_profile:analyst-annie` (foundation) | collab.handoff-to | `agent_profile:java-jenny` | java | profile yaml |
| weak | `agent_profile:analyst-annie` (foundation) | collab.handoff-to | `agent_profile:python-pedro` | python | profile yaml |
| weak | `agent_profile:debugger-debbie` (foundation) | suggests | `directive:USE_MUTATION_TESTING_TO_VALIDATE_TEST_QUALITY` | qa | graph |
| weak | `agent_profile:generic-agent` (foundation) | suggests | `directive:USE_MUTATION_TESTING_TO_VALIDATE_TEST_QUALITY` | qa | graph |
| weak | `agent_profile:implementer-ivan` (foundation) | suggests | `directive:USE_MUTATION_TESTING_TO_VALIDATE_TEST_QUALITY` | qa | graph |
| weak | `agent_profile:reviewer-renata` (foundation) | suggests | `directive:USE_MUTATION_TESTING_TO_VALIDATE_TEST_QUALITY` | qa | graph |
| weak | `directive:DIRECTIVE_030` (foundation) | suggests | `directive:USE_MUTATION_TESTING_TO_VALIDATE_TEST_QUALITY` | qa | graph |
| weak | `directive:DIRECTIVE_030` (foundation) | suggests | `styleguide:tiered-standards` | internal | graph |
| weak | `directive:DIRECTIVE_030` (foundation) | suggests | `toolguide:sonar` | qa | graph |
| weak | `directive:DIRECTIVE_034` (foundation) | suggests | `toolguide:gherkin` | qa | graph |
| weak | `directive:DIRECTIVE_045` (foundation) | suggests | `procedure:mission-tracer-files` | internal | graph |
| weak | `directive:DIRECTIVE_046` (foundation) | suggests | `procedure:mission-wrap-up-sequence` | internal | graph |
| weak | `directive:DISCIPLINED_REFACTORING` (foundation) | suggests | `tactic:refactoring-encapsulate-record` | refactoring | graph |
| weak | `directive:DISCIPLINED_REFACTORING` (foundation) | suggests | `tactic:refactoring-encapsulate-variable` | refactoring | graph |
| weak | `directive:DISCIPLINED_REFACTORING` (foundation) | suggests | `tactic:refactoring-extract-first-order-concept` | refactoring | graph |
| weak | `directive:DISCIPLINED_REFACTORING` (foundation) | suggests | `tactic:refactoring-move-field` | refactoring | graph |
| weak | `directive:DISCIPLINED_REFACTORING` (foundation) | suggests | `tactic:refactoring-move-method` | refactoring | graph |
| weak | `directive:DISCIPLINED_REFACTORING` (foundation) | suggests | `tactic:refactoring-state-pattern-for-behavior` | refactoring | graph |
| weak | `directive:DISCIPLINED_REFACTORING` (foundation) | suggests | `tactic:refactoring-strangler-fig` | refactoring | graph |
| weak | `paradigm:behaviour-driven-development` (foundation) | suggests | `toolguide:gherkin` | qa | graph |
| weak | `procedure:bdd-scenario-lifecycle` (foundation) | suggests | `toolguide:gherkin` | qa | graph |
| weak | `procedure:development-assist-test-cleanup` (foundation) | suggests | `procedure:mission-tracer-files` | internal | graph |
| weak | `procedure:refactoring` (foundation) | suggests | `tactic:refactoring-change-function-declaration` | refactoring | graph |
| weak | `procedure:refactoring` (foundation) | suggests | `tactic:refactoring-combine-functions-into-transform` | refactoring | graph |
| weak | `procedure:refactoring` (foundation) | suggests | `tactic:refactoring-consolidate-conditional-expression` | refactoring | graph |
| weak | `procedure:refactoring` (foundation) | suggests | `tactic:refactoring-extract-class-by-responsibility-split` | refactoring | graph |
| weak | `procedure:refactoring` (foundation) | suggests | `tactic:refactoring-inline-temp` | refactoring | graph |
| weak | `procedure:refactoring` (foundation) | suggests | `tactic:refactoring-introduce-null-object` | refactoring | graph |
| weak | `procedure:refactoring` (foundation) | suggests | `tactic:refactoring-replace-magic-number-with-symbolic-constant` | refactoring | graph |
| weak | `procedure:refactoring` (foundation) | suggests | `tactic:refactoring-replace-temp-with-query` | refactoring | graph |
| weak | `procedure:refactoring` (foundation) | suggests | `tactic:refactoring-retry-pattern` | refactoring | graph |
| weak | `styleguide:planning-and-tracking` (foundation) | suggests | `styleguide:tiered-standards` | internal | graph |
| weak | `styleguide:test-desiderata-and-boundaries` (foundation) | suggests | `styleguide:mutation-aware-test-design` | qa | graph |
| weak | `tactic:acceptance-criteria-non-vacuity` (foundation) | suggests | `tactic:mutation-testing-workflow` | qa | graph |
| weak | `tactic:anti-corruption-layer` (foundation) | suggests | `tactic:refactoring-strangler-fig` | refactoring | graph |
| weak | `tactic:bdd-scenario-formulation` (foundation) | suggests | `toolguide:gherkin` | qa | graph |
| weak | `tactic:bounded-context-canvas-fill` (foundation) | suggests | `toolguide:contextive` | architecture | graph |
| weak | `tactic:chain-of-responsibility-rule-pipeline` (foundation) | suggests | `tactic:refactoring-extract-first-order-concept` | refactoring | graph |
| weak | `tactic:chain-of-responsibility-rule-pipeline` (foundation) | suggests | `tactic:refactoring-guard-clauses-before-polymorphism` | refactoring | graph |
| weak | `tactic:context-mapping-classification` (foundation) | suggests | `tactic:refactoring-strangler-fig` | refactoring | graph |
| weak | `tactic:focused-function-complexity-check` (foundation) | suggests | `tactic:refactoring-guard-clauses-before-polymorphism` | refactoring | graph |
| weak | `tactic:formalized-constraint-testing` (foundation) | suggests | `styleguide:java-conventions` | java | graph |
| weak | `tactic:input-validation-fail-fast` (foundation) | suggests | `styleguide:python-conventions` | python | graph |
| weak | `tactic:supply-chain-install-safety` (foundation) | suggests | `toolguide:java-supply-chain` | java | graph |
| weak | `tactic:supply-chain-install-safety` (foundation) | suggests | `toolguide:javascript-supply-chain` | javascript | graph |
| weak | `tactic:supply-chain-install-safety` (foundation) | suggests | `toolguide:python-supply-chain` | python | graph |
| weak | `tactic:writing-audience-catalog` (writing) | suggests | `asset:writing-audience-agentic-framework-core-team` | internal | graph |

### P3: opt-in -> other opt-in (9)

| Strength | Source | Relation | Target | Target pack | Carrier |
|---|---|---|---|---|---|
| weak | `agent_profile:frontend-freddy` (javascript) | suggests | `directive:USE_MUTATION_TESTING_TO_VALIDATE_TEST_QUALITY` | qa | graph |
| weak | `agent_profile:java-jenny` (java) | suggests | `directive:USE_MUTATION_TESTING_TO_VALIDATE_TEST_QUALITY` | qa | graph |
| weak | `agent_profile:node-norris` (javascript) | suggests | `directive:USE_MUTATION_TESTING_TO_VALIDATE_TEST_QUALITY` | qa | graph |
| weak | `agent_profile:python-pedro` (python) | suggests | `directive:USE_MUTATION_TESTING_TO_VALIDATE_TEST_QUALITY` | qa | graph |
| weak | `agent_profile:randy-reducer` (refactoring) | suggests | `directive:USE_MUTATION_TESTING_TO_VALIDATE_TEST_QUALITY` | qa | graph |
| weak | `directive:USE_MUTATION_TESTING_TO_VALIDATE_TEST_QUALITY` (qa) | suggests | `toolguide:python-mutation-tools` | python | graph |
| weak | `directive:USE_MUTATION_TESTING_TO_VALIDATE_TEST_QUALITY` (qa) | suggests | `toolguide:typescript-mutation-tools` | javascript | graph |
| weak | `tactic:mutation-testing-workflow` (qa) | suggests | `toolguide:python-mutation-tools` | python | graph |
| weak | `tactic:mutation-testing-workflow` (qa) | suggests | `toolguide:typescript-mutation-tools` | javascript | graph |

### X2: edge out of a cut candidate (drops with it) (20)

| Strength | Source | Relation | Target | Target pack | Carrier |
|---|---|---|---|---|---|
| strong | `directive:DIRECTIVE_039` (cut) | requires | `directive:DIRECTIVE_001` | foundation | graph |
| strong | `directive:DIRECTIVE_039` (cut) | requires | `directive:DIRECTIVE_030` | foundation | graph |
| strong | `directive:DIRECTIVE_039` (cut) | requires | `directive:DIRECTIVE_034` | foundation | graph |
| strong | `directive:DIRECTIVE_039` (cut) | requires | `procedure:small-explicit-code-shaping` | foundation | graph |
| strong | `directive:DIRECTIVE_039` (cut) | requires | `procedure:test-first-cycle` | foundation | graph |
| strong | `paradigm:brownfield-onboarding` (cut) | requires | `directive:DIRECTIVE_001` | foundation | graph |
| strong | `paradigm:brownfield-onboarding` (cut) | requires | `directive:DIRECTIVE_003` | foundation | graph |
| strong | `paradigm:brownfield-onboarding` (cut) | requires | `directive:DIRECTIVE_041` | foundation | graph |
| strong | `paradigm:brownfield-onboarding` (cut) | requires | `procedure:legacy-codebase-triage` | foundation | graph |
| strong | `paradigm:brownfield-onboarding` (cut) | requires | `tactic:forensic-repository-audit` | foundation | graph |
| weak | `directive:DIRECTIVE_039` (cut) | suggests | `styleguide:boring-code-review` | foundation | graph |
| weak | `directive:DIRECTIVE_039` (cut) | suggests | `tactic:adversarial-qa-handoff` | foundation | graph |
| weak | `directive:DIRECTIVE_039` (cut) | suggests | `tactic:focused-function-complexity-check` | foundation | graph |
| weak | `directive:DIRECTIVE_039` (cut) | suggests | `tactic:generated-code-stewardship` | foundation | graph |
| weak | `paradigm:brownfield-onboarding` (cut) | rejects | `anti_pattern:big-ball-of-mud` | foundation | graph |
| weak | `paradigm:brownfield-onboarding` (cut) | rejects | `anti_pattern:big-upfront-design` | foundation | graph |
| weak | `paradigm:brownfield-onboarding` (cut) | suggests | `procedure:adversarial-squad-deployment` | foundation | graph |
| weak | `paradigm:brownfield-onboarding` (cut) | suggests | `tactic:delete-the-assertion-not-the-test` | foundation | graph |
| weak | `paradigm:brownfield-onboarding` (cut) | suggests | `tactic:reverse-speccing` | foundation | graph |
| weak | `paradigm:brownfield-onboarding` (cut) | suggests | `tactic:test-to-system-reconstruction` | foundation | graph |

### X: edge into a cut candidate (4)

| Strength | Source | Relation | Target | Target pack | Carrier |
|---|---|---|---|---|---|
| strong | `paradigm:deep-module-design` (foundation) | requires | `directive:DIRECTIVE_039` | cut | graph |
| weak | `directive:DIRECTIVE_025` (foundation) | suggests | `paradigm:brownfield-onboarding` | cut | graph |
| weak | `procedure:mission-tracer-files` (internal) | suggests | `paradigm:brownfield-onboarding` | cut | graph |
| weak | `tactic:terminology-extraction-mapping` (foundation) | suggests | `paradigm:brownfield-onboarding` | cut | graph |

### OK1: writing -> foundation (qualify foundation::) (45) — by pack pair

| From | To | Edges |
|---|---|---|
| writing | foundation | 45 |

### OK2: opt-in -> member (qualify) (199) — by pack pair

| From | To | Edges |
|---|---|---|
| architecture | foundation | 3 |
| drupal | foundation | 20 |
| internal | foundation | 8 |
| java | foundation | 29 |
| javascript | foundation | 50 |
| pack-authoring | foundation | 17 |
| python | foundation | 34 |
| refactoring | foundation | 38 |

### External `built-in::` references in the existing opt-in packs

After the split `built-in` holds no artifact, so each of these is refused as `pack_reference_artifact_missing` (ADR-0053 d7 amended) until it is rewritten to the member that holds the artifact. Keeping `depends_on: built-in` is fine (its closure contains both members); only the qualifier changes. Refs whose artifact moves into the referring pack itself become bare.

| Referring pack | Reference (`built-in::…`) | Occurrences | Rewrite to |
|---|---|---|---|
| event-driven | `paradigm:deep-module-design` | 1 | `foundation::paradigm:deep-module-design` |
| event-driven | `paradigm:domain-driven-design` | 1 | `foundation::paradigm:domain-driven-design` (E) |
| event-driven | `procedure:event-storming-discovery` | 1 | `foundation::procedure:event-storming-discovery` |
| event-driven | `tactic:anti-corruption-layer` | 1 | `foundation::tactic:anti-corruption-layer` (E) |
| event-driven | `tactic:domain-event-capture` | 2 | `foundation::tactic:domain-event-capture` (E) |
| event-driven | `tactic:reference-architectural-patterns` | 1 | `architecture::tactic:reference-architectural-patterns` — opt-in, would need a new depends_on |
| internal | `agent_profile:planner-priti` | 4 | `foundation::agent_profile:planner-priti` |
| internal | `agent_profile:reviewer-renata` | 1 | `foundation::agent_profile:reviewer-renata` |
| internal | `directive:DIRECTIVE_025` | 1 | `foundation::directive:DIRECTIVE_025` |
| internal | `directive:DIRECTIVE_041` | 3 | `foundation::directive:DIRECTIVE_041` |
| internal | `directive:DIRECTIVE_042` | 1 | `writing::directive:DIRECTIVE_042` |
| internal | `directive:DIRECTIVE_044` | 1 | `foundation::directive:DIRECTIVE_044` |
| internal | `directive:DIRECTIVE_045` | 2 | `foundation::directive:DIRECTIVE_045` |
| internal | `directive:DIRECTIVE_047` | 1 | `writing::directive:DIRECTIVE_047` |
| internal | `directive:RECONCILE_CHANGE_SCOPE_TENSIONS` | 1 | `foundation::directive:RECONCILE_CHANGE_SCOPE_TENSIONS` |
| internal | `directive:RED_MAIN_RELEASE_DISCIPLINE` | 3 | `foundation::directive:RED_MAIN_RELEASE_DISCIPLINE` |
| internal | `procedure:adversarial-squad-deployment` | 5 | `foundation::procedure:adversarial-squad-deployment` |
| internal | `procedure:common-docs-page-authoring` | 1 | `writing::procedure:common-docs-page-authoring` |
| internal | `procedure:declare-page-audience` | 1 | `writing::procedure:declare-page-audience` |
| internal | `procedure:development-assist-test-cleanup` | 2 | `foundation::procedure:development-assist-test-cleanup` |
| internal | `procedure:issue-triage-state-machine` | 1 | `foundation::procedure:issue-triage-state-machine` |
| internal | `procedure:mission-tracer-files` | 1 | bare (moves into internal) |
| internal | `procedure:mission-wrap-up-sequence` | 4 | bare (moves into internal) |
| internal | `procedure:post-merge-arch-gate-adjudication` | 2 | `foundation::procedure:post-merge-arch-gate-adjudication` |
| internal | `procedure:refactoring` | 1 | `foundation::procedure:refactoring` |
| internal | `procedure:test-first-bug-fixing` | 3 | `foundation::procedure:test-first-bug-fixing` |
| internal | `styleguide:common-docs` | 1 | `writing::styleguide:common-docs` |
| internal | `styleguide:planning-and-tracking` | 3 | `foundation::styleguide:planning-and-tracking` (E) |
| internal | `styleguide:test-desiderata-and-boundaries` | 2 | `foundation::styleguide:test-desiderata-and-boundaries` |
| internal | `styleguide:testing-principles` | 1 | `foundation::styleguide:testing-principles` |
| internal | `styleguide:tiered-standards` | 1 | bare (moves into internal) |
| internal | `tactic:architectural-gate-non-vacuity` | 1 | `foundation::tactic:architectural-gate-non-vacuity` |
| internal | `tactic:canonical-source-unification` | 1 | `foundation::tactic:canonical-source-unification` |
| internal | `tactic:clean-linear-commit-history` | 3 | `foundation::tactic:clean-linear-commit-history` |
| internal | `tactic:frozen-baseline-shrink-only-ratchet` | 1 | `foundation::tactic:frozen-baseline-shrink-only-ratchet` |
| internal | `tactic:model-task-routing` | 3 | `foundation::tactic:model-task-routing` |
| internal | `tactic:moscow-scoping-lens` | 2 | `foundation::tactic:moscow-scoping-lens` |
| internal | `tactic:no-parallel-duplicate-test-runs` | 1 | `foundation::tactic:no-parallel-duplicate-test-runs` |
| internal | `tactic:occurrence-classification-workflow` | 1 | `foundation::tactic:occurrence-classification-workflow` |
| internal | `tactic:pr-agent-worktree-isolation` | 1 | `foundation::tactic:pr-agent-worktree-isolation` |
| internal | `toolguide:github-tracker` | 1 | `foundation::toolguide:github-tracker` (E) |
| qa | `styleguide:given-when-then-authoring` | 1 | `foundation::styleguide:given-when-then-authoring` (E) |
| qa | `tactic:bdd-scenario-formulation` | 1 | `foundation::tactic:bdd-scenario-formulation` |
| qa | `toolguide:gherkin` | 1 | bare (moves into qa) |
| spdd | `action:software-dev/implement` | 1 | `foundation::action:software-dev/implement` |
| spdd | `action:software-dev/plan` | 1 | `foundation::action:software-dev/plan` |
| spdd | `action:software-dev/review` | 1 | `foundation::action:software-dev/review` |
| spdd | `action:software-dev/specify` | 1 | `foundation::action:software-dev/specify` |
| spdd | `action:software-dev/tasks` | 1 | `foundation::action:software-dev/tasks` |
| spdd | `agent_profile:architect-alphonso` | 1 | `foundation::agent_profile:architect-alphonso` |

## missions/ → mission_types/ (ADR-0048 d16, ADR-0050 d4/d5)

Recommendation: **a follow-up, not this split.** The charter at the lock pin `fb24052` still reads mission types from `missions/<id>/<id>.mission-type.yaml` (ADR-0044) and its `contracts/packs/file-kinds.yaml` lists `*/mission_types/*.yaml` and `*/missions/mission_types/*.yaml` under **`retired:`** (refused by name). Renaming now would make foundation unreadable to the charter service. The work breakdown already separates it as P2 ("with P1", depends on charter item 9, the mission-type bundle schema, which is not done). d16 only requires both moves to land in the same *re-pin* — a core-side concern this repo does not gate on (AGENTS.md). So #73 should `git mv packs/built-in/missions packs/foundation/missions` unchanged.

## Census divergences found (besides group E)

- Census counts 14 paradigms; built-in now has 9. `execution-lanes` is now a toolguide, `git-flow` a procedure, `structured-prompt-driven-development` moved to spdd (#175); `shared-branch-ci` and `extract-then-publish-separation` are not in built-in at all (the census lists extract-then-publish for writing — nothing to move).
- Census lists 18 toolguides; now 19 nodes (execution-lanes added; it is missing from the manifest).
- Census names no ruling for: DIRECTIVE_037, planning-and-tracking, github-tracker, typescript/css/html-conventions (placed in javascript), the 13 anti-patterns (placed in foundation per ADR-0052 d15), most procedures (placed with their owning directive; ADR-0052 d5/d6 and ADR-0053 d29 applied where they speak).
- 16 `template:` nodes exist only in `template.graph.yaml` with **no file** (agent-brief, ammerse-analysis, bounded-context-canvas, c4-component/container/context-mermaid, decomposition-table, glossary, lightweight-prestudy, onboarded-artifact-set, out-of-scope-record, quality-attribute-assessment, risk-identification-assessment, source-agent-dossier, stakeholder-persona, system-context-canvas). They are placed with their referrers above; whether to author or drop them is a separate defect (ADR-0052 d14/ADR-0053 d31 already refuse file-less anti-pattern nodes after migration; the 13 anti-patterns are also file-less).
- Profile YAML `collaboration` lists name stack profiles from foundation profiles (analyst-annie → python-pedro, java-jenny) and writing profiles (analyst-annie → lexical-larry). These are ids, not URNs, so no load refusal, but they are soft cross-boundary links to tidy.
- The census says foundation profiles have "their stack-specific examples removed" — content work, not membership.
