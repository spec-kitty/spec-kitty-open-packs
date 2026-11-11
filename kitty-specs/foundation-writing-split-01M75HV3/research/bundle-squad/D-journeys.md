# Lens D: consumer journeys for the #73 bundle split

Read-only research. Inputs: `research/strict-membership.json` (current rulings: foundation 115, writing 57, qa 6,
internal 4, staging 217), `edges.json` (1091), `delegates.json`, `profrefs.json`, `3-consumers.md`, the org packs'
`pack.yaml` and `drg/fragment.yaml`, charter `docs/plans/pack-ecosystem-work-breakdown.md` (census), ADR-0048,
ADR-0065, and open-packs `docs/packs/catalog-proposal.md`.
Scratch script: `D-work/split.py`. It carves staging into census-named bundles by name rules. Treat it as an
approximation of the census, not a ruling.

Frame used throughout:
- **"Place"** means a deployer copies a pack directory into the configuration root. Every `pack_level: built-in` pack
  is placed this way and is read-only to registration (ADR-0065 D3).
- **"Register"** means a whole-pack `PUT` of an org or project pack (ADR-0065 D1).
- Activation is per artifact. There is no whole-pack switch-off (ADR-0048 d18), and an empty charter activates
  nothing (ADR-0053 d10). So an extra bundle in a compose costs closure checks and impact radius, not context noise.
  The one exception is the `default` preset, which leaves every kind unrestricted.

## 1. What the org packs actually reference today

`built-in::` references re-mapped against the strict split (distinct targets):

| Org pack | refs | → foundation | → writing | → own pack (become bare) | → **staging** | Staging targets by census bundle |
|---|---|---|---|---|---|---|
| internal | 35 | 8 | 5 | 3 (tracer, wrap-up, tiered-standards) | **19** | testing 5 (test-first-bug-fixing, dev-assist-test-cleanup, testing-principles, test-desiderata, no-parallel-duplicate-test-runs); delivery 5 (issue-triage, clean-linear-commit, pr-agent-worktree, github-tracker, occurrence-classification); planning/review 7 (planner-priti, planning-and-tracking, adversarial-squad, post-merge-arch-gate, architectural-gate-non-vacuity, model-task-routing, frozen-baseline); refactoring 1 (`procedure:refactoring`); practice 1 (canonical-source-unification) |
| qa | 22 | 8 | 1 (rhea `traceable-decisions`) | 3 (gherkin, mutation-aware, mutation-workflow) | **11** | testing 9 (bdd-scenario-formulation, bdd-scenario-lifecycle, atdd, given-when-then, disciplined-defect-diagnosis, test-pyramid, testing-principles, test-desiderata, no-parallel-duplicate); delivery 1 (issue-triage); planning 1 (spike-timebox) |
| event-driven | 6 | 0 | 0 | 0 | **6** | architecture 6 (DDD, deep-module, event-storming, ACL, reference-architectural-patterns, domain-event-capture) |
| spdd | 6 | 5 (software-dev actions) | 0 | 0 | **1** | architecture (architect-alphonso) |
| cave-kitty | 0 | prose only (implementer-ivan, reviewer-renata) | – | – | 0 | – |

Under the strict foundation rule, **4 of the 5 org packs need specialist-staging**. Only cave-kitty does not, and
spdd needs it for a single profile.

Stack packs (from edges and profile bodies):

| Stack | requires into foundation | requires into non-foundation | suggests into non-foundation |
|---|---|---|---|
| java (#5) | 10 (6 directives, 4 tactics) + `specializes_from implementer-ivan` | **testing: `procedure:test-first-bug-fixing`, `tactic:bdd-scenario-formulation`** (graph and profile body) | refactoring (`DISCIPLINED_REFACTORING`), qa (`USE_MUTATION_TESTING…`) |
| python | 14 + specializes_from ivan | none | refactoring, qa (plus qa→python `python-mutation-tools` edges) |
| javascript (freddy, norris) | 19 body refs | testing ×4 (the same two nodes) | refactoring, qa |
| drupal | 9 | testing ×1 (test-first-bug-fixing) | – |
| rust/go (PR B, #191/#192) | modelled on java/python profiles | likely the same two testing nodes if modelled on java-jenny | likely the same |

Under the ruling "java depends on foundation only", **java-jenny's two `requires` edges have no home.** Java must
then either depend on the temporary specialist-staging pack, drop the edges, or have those two nodes moved into
foundation. The same applies to javascript and drupal.

Foundation's own outward needs, which strict foundation cuts:
- 39 `requires` targets: the directive how-to procedures plus 3 tactics.
- 59 `suggests`/`scope` targets.
- 4 step-contract `delegates_to` candidates (`software-dev/implement` → execution-lanes, trunk-based, git-flow;
  `software-dev/specify` → example-mapping-workshop). These are body references, so they are **deleted, not
  relocated**. They are lost even for a consumer who registers staging, unless a bundle later restores them with a
  step `enhances` (ADR-0053 d22).
- In total, 157 edges leave a built-in-level source for an org target. They can only live in the org bundle's graph,
  with a qualified source.

Writing has 3 body references into staging that must be removed: diagram-daisy → `USE_C4_MODEL_TECHNIQUES`, and
lexical-larry → `terminology-extraction-mapping` and `context-boundary-inference`. It also has 12 graph edges into
staging that must be relocated: `documentation/design instantiates` 3 C4 templates, `mission_type:documentation
scope drill-down-documentation`, retrospect → retrospective-facilitator and kitty-glossary-writing, and others.

Side finding: `agent_profile:analyst-annie` (foundation) has a body reference to `DIRECTIVE_047` (writing). Writing
depends on foundation (44 body references), so this reference would make a cycle. Either 047 moves to foundation or
the reference goes.

## 2. Five journeys under the current rulings (R)

R means: place built-in + foundation + writing (3 directories, exact-pinned, read-only), and optionally register
`specialist-staging` (217 nodes, org, temporary).

| Journey | Places | Registers | Needs staging? | Loses vs today's monolith if staging not registered | Loses even with staging |
|---|---|---|---|---|---|
| **(a) Python web team**, software-dev | 3 | 0 or 1 (staging) | yes: python-pedro, frontend-freddy, node-norris, css/html/ts conventions, testing styleguides, git/PR workflow | all stack profiles; 39 directive how-to procedures; testing-principles, quadruple-a; planner, architect, researcher, debugger profiles | 4 step-contract candidates (git-flow, trunk-based, execution-lanes, example-mapping) |
| **(b) Docs-only team** | 3 | 0 | wants it for C4 templates, curator-carla, drill-down-documentation, living-documentation-sync, decision-record-keeping, glossary maintenance | the 3 writing body references; documentation/design C4 templates; documentation scope → drill-down; retrospective-facilitator; how-tos for directives 037 and 003. It still receives software-dev, plan and research plus ivan and renata (writing → foundation), which is harmless because activation is per artifact | same 3 body references |
| **(c) Spec Kitty core team** (internal + qa) | 3 | internal, qa, **staging** | yes, mandatory: 19 + 11 qualified `specialist-staging::` references | n/a: internal and qa cannot compose without staging | step-contract candidates |
| **(d) Java/COBOL enterprise** | 3 | java, staging (for jenny's 2 requires and for COBOL modernisation: strangler-fig, legacy-codebase-triage, brownfield, ACL, connascence, test-to-system-reconstruction), n private COBOL packs, rust/go if used | yes | jenny's test-first and BDD requires; every modernisation tactic | step-contract candidates |
| **(e) "Just give me missions"** | 3 | 0 | no | 39 how-to procedures (directives keep their text, but their `requires` edges are gone); human-in-charge, planner, architect; retrospect-action facilitator; mutation/sonar/gherkin suggestions | step-contract candidates. The `minimal` preset is intact: all of its ids are in foundation |

**What R costs consumers:**
- Staging is one all-or-nothing org pack, so for (a), (c) and (d) it amounts to a reinstated "monolith minus core".
- Staging is temporary, and each carve PR removes artifacts from it, which is a major bump.
  - With about 9 carve PRs, every consumer that wrote `specialist-staging::X` must re-qualify X and move its range,
    about 9 times.
  - internal (19 references) and qa (11) are the worst hit.
  - Each carve also changes a pack in every closure that contains staging. Under ADR-0065 D6, staging's blast radius
    is every org pack except cave-kitty.
- **Recommendation for the R interim:** in-repo org packs and java should **not** be migrated to
  `specialist-staging::`. Either carve the bundles they need first (§6 order) or leave them on `built-in::` until
  then.

## 3. The same journeys under a multi-bundle split (M)

Bundles follow census names. Sizes come from the heuristic carve of the 217 staging nodes:
- architecture (+DDD) 40
- refactoring 39
- testing 32
- planning-and-analysis (with brownfield and review/adversarial) 27
- delivery (git/PR) 19
- pack-authoring 15
- javascript 13
- python 5
- drupal 4
- "practice" leftovers 19: the directive how-to procedures, efficient-local-tooling, easy-to-change, avoid-gold-plating
- java 4 (#5)

Two variants are counted:
- **M1, strict foundation:** practice is a bundle.
- **M2, foundation re-widened by ~27 nodes:** the practice how-tos, plus 8 "hot" nodes that every journey needs.
  The hot nodes are test-first-bug-fixing, bdd-scenario-formulation, execution-lanes, trunk-based, git-flow,
  example-mapping-workshop, retrospective-facilitator and human-in-charge. With them in foundation, no step-contract
  reference is lost.

| Journey | M1: org registrations (depends_on depth) | M2: org registrations (depth) | Gains vs R |
|---|---|---|---|
| (a) Python web | python, javascript, testing, delivery, practice = **5** (javascript → testing → foundation: depth 2) | python, javascript (+ testing, delivery optional) = **2–4** (depth 1) | registers what it uses; nothing temporary |
| (b) Docs-only | 0, or architecture + practice + planning to recover C4, how-tos and facilitator = **3** for 6 nodes | 0, plus architecture for C4 only; 0 if the C4 templates and `USE_C4` move to writing (census gives writing diagram-daisy and both diagram toolguides already) | – |
| (c) Core team | internal depends on foundation, writing, testing, delivery, planning, refactoring, practice = **7 deps**; qa on foundation, writing, testing, delivery, planning; registrations = 5 bundles + internal + qa = **7** | internal on foundation, writing, testing, delivery, planning (+ refactoring for the one † reference) = **5–6**; qa on foundation, writing, testing, delivery, planning; registrations = **6** | stable qualifiers; each bundle carve touches only the packs that use it |
| (d) Java/COBOL | java → foundation **and testing** (requires); COBOL → java, refactoring, architecture, planning, testing, delivery; registrations = 5–6 bundles + java + n private (depth 3: COBOL → java → testing → foundation) | java → foundation only; COBOL → java, refactoring, architecture, planning (+testing) = **4–5 + java + n** (depth 2) | no temporary pack in a private pack's `depends_on` |
| (e) Minimal | 0 | 0 | M2 restores the 4 step-contract candidates and the how-tos with nothing to register |

Other org packs under M:
- event-driven → foundation, architecture. Its 6 references all land in one bundle, a clean fit.
- spdd → foundation, architecture, for **one profile**. Alternative: architect-alphonso back in foundation, as in the
  census (it listed 13 base profiles).
- cave-kitty → foundation (the prose names only ivan and renata).

### Registration, version and blast-radius cost (ADR-0065)

- **Registration** is whole-pack. The same `pack_version` with new content gives `409 pack_version_conflict`, so
  every bundle content change is a version bump plus a `PUT`.
  - Built-in-level members are not registrable at all. A foundation or writing fix reaches a deployer only by
    re-placing the release, in lockstep and exact-pinned by built-in (d17).
  - The stricter foundation is, the more doctrine fixes are cheap org PUTs. That is the real upside of R/M1.
- **Range maintenance:** org packs use ranges (`>=1.0,<2`).
  - A minor bump of a bundle costs dependents nothing.
  - A **major** bump of foundation costs: about 9–10 bundles + 5 in-repo org packs + java/rust/go + every private
    pack each edit a range and bump their own version. That cost is the same for M1 and M2 and grows linearly with
    bundle count.
  - Under R, staging takes a major bump on **every carve PR**.
- **Blast radius (D6 impact check)** = every closure that contains the re-registered pack.

  | Hub bundle | M1 dependents | M2 dependents |
  |---|---|---|
  | testing | java, javascript, drupal, architecture, delivery, internal, qa, COBOL (8+) | internal, qa, optional consumers (javascript/java/drupal leave) |
  | planning | internal, qa, architecture, testing, COBOL | same |
  | delivery | internal, qa | same |
  | architecture | event-driven, spdd, COBOL | same |
  | python | – | – |

  Leaf stack bundles have none: python, javascript, drupal, java (except the private COBOL packs on java).

- **Cross-bundle edge overhead** (graph edges between two org bundles, each one a qualified reference and a
  `depends_on` obligation):

  | Shape | Org specialist bundles | Org↔org edges | Distinct bundle pairs | Built-in→org edges relocated | Step-contract refs lost |
  |---|---|---|---|---|---|
  | R (one staging) | 1 | ~25 (staging↔qa/internal) | 4 | 157 | 4 |
  | M1 fine | 11 | 82 | 45 | 157 | 4 |
  | M2 (foundation +27) | 10 | 64 | 36 | 130 | 0 |
  | M3 coarse ("engineering" = architecture+refactoring+planning+delivery+testing) | 6 | 41 | 15 | 130 | 0 |

  Of the 45 M1 pairs, 14 are bidirectional and must be broken by relocating one direction's edges into the pack that
  depends on both. Examples: architecture↔planning, architecture↔refactoring, testing↔planning, delivery↔testing,
  python↔qa, javascript↔qa.
  - The **requires-class** org↔org edges are few (21). testing is the hub: every stack profile and architect-alphonso
    require it.
  - The one apparent requires-cycle is architecture ↔ pack-authoring. It comes from directive 039 (a cut candidate)
    and the brownfield paradigm, both mis-homed by the heuristic. It vanishes when 039 is cut and brownfield sits in
    planning.

## 4. Granularity

- **Too many small bundles** (M1 at 11, or more if refactoring is split from semantic-compression, or review from
  planning):
  - internal reaches 7 dependencies and the COBOL chain reaches depth 3.
  - About 45 bundle pairs need qualified references, and 14 bidirectional pairs need edge relocation.
  - A foundation major means 15–20 range edits across the ecosystem.
  - The docs team needs 3 registrations to recover 6 nodes.
  - Bundles of 4–5 items (python, drupal, java) are fine as **leaves**: they have no dependents, so their overhead is
    one registration.
  - Small **hubs** are the expensive case. The testing hub is the one to avoid.
- **Too few** (R, or M3):
  - Opt-in becomes all or nothing. A Python team that wants python-pedro also takes 40 architecture and 39
    refactoring nodes.
  - Harmless for activation (d18, per-artifact), but every change to any part re-runs the impact check for every
    consumer.
  - A coarse "engineering" pack is in practice the census foundation under another name, and it reintroduces the
    monolith ADR-0048 set out to remove.
- **Rule of thumb from the journeys:**
  - A node that ≥4 of the 5 journeys and ≥3 org or stack packs need is foundation by definition. Examples: the
    practice how-tos, test-first-bug-fixing, bdd-scenario-formulation, the git-flow/trunk/execution-lanes trio,
    retrospective-facilitator.
  - Topical clusters that only some journeys need become bundles.
  - Stack bundles stay leaves.

**Proposed target: 7–9 opt-in org bundles**, plus the stack leaves (java, python, javascript, drupal, rust, go) and the
existing org packs:
- architecture (DDD + C4 + its anti-patterns)
- refactoring (refactoring catalog + semantic-compression + randy)
- testing-extras folded into qa per the census, or a separate testing bundle if the operator keeps qa opinionated
- planning-and-analysis (with brownfield)
- delivery (git/PR workflow)
- review/adversarial, split out only if internal is not its sole consumer
- pack-authoring (or fold into internal)

Reasoning for the range:
- No journey then needs more than 4 specialist registrations, besides its stacks.
- The longest chain is 2 (private → stack → foundation).
- No bundle except the testing/qa hub has more than 3 in-repo dependents.

This holds **if** foundation is re-widened by the ~27 hot nodes (M2). If strict foundation stands (M1), add
`practice` as a 10th bundle that every software journey needs. That bundle is the clearest signal it belongs in
foundation.

## 5. Interaction with the java question (not decided here)

If built-in aggregated java:
- **Level consequence:** built-in may depend only on built-in-level packs (ADR-0048 d7 amended). So java would have
  to become `pack_level: built-in`.
  - That contradicts ADR-0048 d14 ("stack packs are opt-in … not members of built-in"), which is why a charter ADR is
    needed.
  - Java would become **read-only to registration** (ADR-0065 D3), exact-pinned and lockstep-released with
    foundation and writing.
  - Java's own dependencies must also be built-in level. Java-jenny's two testing requires then force those nodes
    into foundation, or drag a `testing` bundle into built-in. Under strict foundation (R/M1) this cascades.
- **Journey (a), Python web team:**
  - Gets java-jenny, java-conventions, java-supply-chain and maven-review-checks placed whether wanted or not.
  - Under the `default` preset (no kind keys, everything effective) java-jenny becomes **effective** for a Python
    team, and profile routing gains a Java candidate.
  - Under `minimal`, or an interview-built charter, nothing changes beyond closure size.
  - Foundation's `supply-chain-install-safety suggests java-supply-chain` edge could stay in a built-in graph instead
    of being relocated.
  - It sets a precedent: python and javascript would then ask for the same treatment.
- **Journey (d), Java/COBOL:**
  - One fewer registration, and java is guaranteed present, so private COBOL packs can rely on it without
    registering it.
  - But a Java fix becomes a built-in release, not an org PUT.
  - The team cannot pin java independently of foundation.
  - It cannot override java-jenny by re-registering java, only by an org-level `overrides` or `enhances`.
- **rust/go** would face the same question. If they are not aggregated, the asymmetry is visible to consumers.

## 6. Should qa, internal and event-driven depend on future bundles?

Yes, directly (option B of `3-consumers.md`), on exactly the bundles they reference, and not on staging.

| Org pack | depends_on (M2) | depends_on (M1 adds) | Notes |
|---|---|---|---|
| qa | foundation, writing (rhea), testing\*, delivery (issue-triage), planning (spike-timebox) | practice | \*If the census "testing extras fold into qa" is widened to absorb given-when-then, bdd-scenario-lifecycle, atdd and test-pyramid, qa's testing dependency shrinks to the foundation hot nodes, and qa becomes the testing hub itself. Then java, javascript and drupal must not depend on qa (it ships a mission and an org-charter), which is another argument for moving the two stack-required nodes into foundation. |
| internal | foundation, writing, testing, delivery, planning (+ refactoring for `procedure:refactoring`) | practice | The heaviest consumer: 19 staging references. Several items could move *into* internal instead: issue-triage-state-machine, frozen-baseline, model-task-routing, post-merge-arch-gate-adjudication, adversarial-squad-deployment. The catalog's `spec-kitty-internal` lists them. Moving them would cut internal to 2–3 bundle dependencies, but makes qa depend on internal for issue-triage (allowed, org→org) or duplicates it. |
| event-driven | foundation, architecture | – | Clean single-bundle fit. Its references to `anti-corruption-layer` and `reference-architectural-patterns` are already the † "later architecture pack" items. |
| spdd | foundation, architecture (alphonso only) | – | Or alphonso back to foundation. |
| cave-kitty | foundation | – | prose only |

**Carve order the journeys suggest** (one PR per bundle, as ruled):
1. testing (or the foundation hot-node move): unblocks java #5, qa, internal, javascript and drupal.
2. architecture: unblocks event-driven, spdd and COBOL.
3. delivery and planning: unblock internal and qa.
4. refactoring.
5. stacks (python, javascript, drupal).
6. pack-authoring.

With this order, no in-repo org pack ever needs a `specialist-staging::` qualifier.
