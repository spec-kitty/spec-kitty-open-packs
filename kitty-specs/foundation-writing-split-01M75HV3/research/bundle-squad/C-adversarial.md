# Lens C: adversarial review of rulings 1–6

Read-only. Source: `packs/built-in/` at main 5c489d6, `research/{edges,delegates,profrefs,strict-membership}.json`, charter ADR-0053, 0063, 0065, 0068, 0069 at fb24052. Every count below comes from a script run over `edges.json` and `strict-membership.json`. The 4 groups are foundation 115, writing 57, qa 6, internal 4 and staging 217, for 399 nodes in all.

## 0. Headline findings (things the approved split gets wrong)

1. **A hard defect: the split as approved is invalid.** `analyst-annie` (in foundation) has `directive-references: 047` in its body (`agent_profiles/analyst-annie.agent.yaml:106`). `DIRECTIVE_047` is in writing. Writing must depend on foundation, because all 7 documentation step contracts delegate to 010/029/033/037/003/001 and to the tactics requirements-validation-workflow, adr-drafting-workflow and premortem. Foundation therefore cannot see writing without a cycle, and a body reference cannot be relocated. Ruling 1 contradicts itself here: its own rule ("directives the seeds reference directly") puts 047 in foundation, and ruling 2 put it in writing. The census in the work breakdown (`:94`) carries the same latent defect.
2. **Writing has hard defects of its own.** Writing is at built-in level, so it cannot depend on the org-level staging. Yet these body references point into staging:
   - `lexical-larry` → `tactic:terminology-extraction-mapping` and `tactic:context-boundary-inference`;
   - `diagram-daisy` → `directive:USE_C4_MODEL_TECHNIQUES`.

   Each must be removed, or its target pulled into writing.
3. **Foundation alone does not staff its own mission types.** Steps name roles, and selection is by role (ADR-0069 d4):
   - research: 4 of its 6 steps ask for `researcher`, and `researcher-robbie` is in staging; every research prompt names him.
   - software-dev, research and documentation: `retrospect` asks for `facilitator`, and `retrospective-facilitator` is in staging. The graph also has the edges `action:*/retrospect scope retrospective-facilitator`.
   - documentation (writing) asks for `architect` once and `researcher` twice; neither profile is in writing.

   Every one of these steps is served by the fallback, or answers `no_profile_matched` when no built-in is in the closure (see §6). Meanwhile no base mission step and no graph edge ever asks for `analyst`, so `analyst-annie` is the one seed nothing consumes.
4. **Deleting the step-contract delegates removes extension points, and opting in later does not restore them.** In `implement.step-contract.yaml`, the `branching_paradigm` and `branching_procedure` steps each have exactly one candidate (trunk-based and git-flow), and the schema has `candidates minItems: 1`. Deleting the candidate makes the whole step vacuous, so the step is deleted with it. A project whose charter selects Git Flow then has nothing to bind to, even after it installs the bundle holding git-flow. Restoring the hook would need a step enhancement (ADR-0066).
5. **The 37 required how-tos have no specialist home.** For 33 of the 37 procedures and tactics that the kept directives `require`, the only `requires` inbound comes from a foundation directive. Parking them in staging creates orphans that no future specialist bundle naturally owns. The "bundle" they would form is, by definition, foundation.
6. **The default experience shrinks to 43%.** Built-in cannot depend on the org-level staging. After `--preset default` (which today means "every built-in artifact"), 227 of 399 nodes are no longer effective until a project opts into staging. Those 227 include execution-lanes, the facilitator and researcher profiles, and every directive how-to.

## 1. Base mission types: named artifacts outside foundation (strict)

Classes: **B** means the mission cannot run correctly without it; **D** means it degrades quality; **N** means nice to have.

### Step-contract bodies (`delegates_to`)

These are unrelocatable: under the strict rule they get deleted.

| Artifact | Where | Class | Why |
|---|---|---|---|
| toolguide:execution-lanes | implement/workspace | **D, high** (borders on B) | The step text calls it "the only supported worktree mechanism". The CLI enforces the topology, and the step's own `guidance` still says "do not create lane worktrees by hand", so the mission runs but loses the lane and status cautions. |
| paradigm:trunk-based | implement/branching_paradigm (sole candidate) | **B** for charter selection | The step dies with its candidate. The charter's branching selection then binds to nothing. |
| procedure:git-flow | implement/branching_procedure (sole candidate) | **B** for git-flow projects | Same as trunk-based. |
| procedure:example-mapping-workshop | specify/map_examples (sole candidate) | **D** | The step description survives as prose. |

### Graph scope edges from foundation actions and mission types into staging

There are 32 of these edges (they can be relocated).

| Class | Artifacts |
|---|---|
| D | retrospect → retrospective-facilitator (×2) and kitty-glossary-writing (×2; both retrospect prompts also name it); implement/review → execution-lanes, trunk-based, git-flow |
| N/D | implement/review → refactoring, test-first-bug-fixing, disciplined-defect-diagnosis, legacy-codebase-triage, boring-code-review, efficient-local-tooling |
| N | specify → domain-driven-design; plan → domain-aware-decision-interview; tasks → issue-triage-state-machine; mission_type:plan → c4-incremental, deep-module, DDD, planning-and-tracking; mission_type:research → domain-aware-decision-interview, event-storming, situational-assessment, spike-timebox-policy |

There are also 2 scope edges that leave foundation for other packs:

- `mission_type:research scope styleguide:research-citation-discipline` goes to **writing**. It can be relocated, but the coupling is inverted: 4 research prompts say "Apply the research-citation-discipline styleguide throughout".
- `action:software-dev/review scope procedure:mission-wrap-up-sequence` goes to **internal**.

### Prompt and guideline prose

| Artifact | Where | Class |
|---|---|---|
| researcher-robbie | 4 research step headers | **D** (falls back to generic) |
| procedure:adversarial-squad-deployment | sd plan.prompt:259 says "mandatory for plan/research" when a security-impacting dependency decision is made; also plan/review guidelines, review.prompt and doc validate | **D**, and **B** in that conditional case: `charter context --include procedure:adversarial-squad-deployment` resolves nothing |
| java-, javascript- and python-supply-chain toolguides | implement.prompt | D for dependency changes |
| python-pedro | implement and review prompts (as an example) | N |
| mission-wrap-up-sequence (internal) | implement.prompt:338 | N; it is awkward for a product prompt to name a team-internal procedure |
| paradigm:domain-driven-design | charter.prompt (as an example) | N |

## 2. The four foundation profiles

| Profile | Body references | Graph edges leaving foundation | Coherent alone? |
|---|---|---|---|
| generic-agent | 028 (in foundation) | suggests DISCIPLINED_REFACTORING (staging) and mutation (qa) | Yes. Its fallback lock lives in **built-in's** `policy.yaml`, not foundation's (see §6). |
| implementer-ivan | 010, 043, 044, 045, 051 and dependency-hygiene (all in foundation) | requires procedure:test-first-bug-fixing (staging) | Mostly. Its only `collaboration.operating-procedures` entry is test-first-bug-fixing, which dangles. 5 specialists (pedro, jenny, norris, dries, freddy) `specializes_from` it from staging, which is the right direction. |
| reviewer-renata | 001, 024, 030, 032, 041, 051 and 7 tactics (all in foundation) | requires adversarial-squad-deployment (staging) | Degraded. Its sole operating procedure dangles, and that procedure is the one the plan and review prompts call mandatory. |
| analyst-annie | 003, 032, **047 (writing): a cycle** | none else | **No.** The reference is invalid, nothing consumes her, and her ATDD procedure (bdd-scenario-lifecycle) is in staging. |

Note: `profrefs.json` treats `collab.*` entries as role words. `operating-procedures` is the exception: its entries are real procedure ids. They are unchecked today, but they are dangling names.

## 3. The 30 kept directives and what they `require`

| Directive | Requires (st = staging, fo = foundation) |
|---|---|
| 001 | component-boundary-definition (st) |
| 003 | decision-record-keeping (st); tactics decision-marker-capture and traceable-decisions (fo) |
| 010 | specification-traceability-check (st) |
| 018 | doctrine-version-change (st) |
| 024 | keep-change-local (st) |
| 025 | tech-debt-point-cut-triage, tidy-first-campsite-clean, touched-area-cleanup (st) |
| 028 | local-tooling-selection (st) |
| 029 | agent-commit-signing (st) |
| 030 | test-and-typecheck-gate-run (st) |
| 031 | bounded-context-alignment (st) |
| 032 | term-interpretation-alignment (st) |
| 033 | targeted-staging (st) |
| 034 | red-first-bug-reproduction, test-first-cycle (st) |
| 035 | bulk-edit-occurrence-mapping, tactic occurrence-classification-workflow (st) |
| 036 | black-box-integration-test-design (st) |
| 037 | living-documentation-sync (st); usage-examples-sync (fo) |
| 040 | five-paradigm-structural-intervention, tactic five-paradigm-parallel-debugging (st) |
| 041 | failing-test-triage, observable-contract-test-authoring, red-first-bug-reproduction (st) |
| 043 | defect-class-construction-gate (st) |
| 044 | canonical-source-discipline (st) |
| 045 | land-changes-via-pull-request, read-intent-before-high-risk-operation (st) |
| 046 | readable-pr-preparation (st) |
| 048 | version-freshness-check (st) |
| 049 | agent-self-declaration (st) |
| 050 | credential-exposure-prevention (st) |
| 051 | none outside foundation |
| 052 | durable-fix-investigation (st) |
| 053 | op-or-mission-lifecycle, tactic op-or-mission-selection (st) |
| RECONCILE_CHANGE_SCOPE_TENSIONS | change-scope-tension-resolution, keep-change-local, tidy-first-campsite-clean, touched-area-cleanup (st) |
| RED_MAIN_RELEASE_DISCIPLINE | red-main-handling (st) |

In total: 34 procedures and 3 tactics, 37 distinct nodes. Each procedure is 16 to 28 lines.

### Sample of 8 pairs: is the directive actionable without its procedure?

| Pair | Verdict |
|---|---|
| 033 / targeted-staging | **Yes.** The directive already forbids `git add -A/./--all` and requires a diff review. The procedure is redundant. |
| 024 / keep-change-local | **Yes.** The procedure adds only "review the diff for scope creep". |
| 045 / land-via-PR + read-intent | **Yes.** The directive lists the forbidden commands. It loses the revert-PR recovery and "never delete a test to make a build pass". |
| 030 / test-and-typecheck-gate-run | **Mostly.** It loses "run typecheck as a separate gate, recording the command and exit code". |
| 029 / agent-commit-signing | **Partly.** The directive states the goal; the actual `--no-gpg-sign` / `-c commit.gpgsign=false` command is only in the procedure. |
| 050 / credential-exposure-prevention | **Partly.** It loses "stop the line on exposure", the incident step. That is a material security gap. |
| 010 / specification-traceability-check | **No.** The directive says only "traceability must remain inspectable". The coverage table and the rule to cite IDs in every change live in the procedure. 010 is the directive delegated most often (13 step contracts), so the most-used directive is the most hollow without its procedure. |
| 053 / op-or-mission-lifecycle + op-or-mission-selection | **No.** Its body prose names `tactic:op-or-mission-selection` as "the decision heuristic that applies it", and the "Mission triggers" it relies on are defined only in that tactic and procedure. |

Result: 3 of 8 stay actionable, 3 degrade and 2 are hollow. Directives state *what*; the procedures are short and give *how*. Splitting them saves little and costs real fidelity.

## 4. Presets and policy

- `minimal` activates software-dev, directives 001/010/024/028/030 and tactic acceptance-test-first. All of them are in foundation. Fine.
- `default` activates software-dev, documentation, research and plan. Documentation is in writing, which built-in aggregates. Fine.
- But "every built-in artifact is effective" now covers only 172 nodes. **The 227 in staging, qa and internal leave the default experience** (finding 0.6).
- `policy.yaml` locks generic-agent, and `fallback_profile: generic-agent` is declared on built-in. Both are consistent with ADR-0068 d2/d3, because built-in's closure includes foundation. See §6 for the cost.

## 5. Three alternative cuts (plus one)

"Out-edges" are graph edges that leave foundation and must be relocated as qualified sources into the higher pack's graph. "+047" means the annie fix applied.

| Cut | Nodes | Out-edges (to staging) | Out `requires` | Unrelocatable problems | What breaks or degrades | Risk |
|---|---|---|---|---|---|---|
| (i) strict as approved | 115 | 146 (133) | 44 | 4 delegate deletions (2 vacuous steps removed); **047 cycle** | Branching selection is lost; 3 of 8 sampled directives are hollow; research and retrospect run on the fallback; 37 orphans sit in staging; the default experience falls to 43% | **High; invalid until 047 is fixed** |
| (i)+047 | 116 | 150 (133) | 45 | 4 delegate deletions | Same as (i), minus the cycle | High |
| (ii) + 4 delegates (+047) | 120 | 145 (128) | 45 | none in contracts | Hooks are kept; the directives stay hollow; the role gaps remain | Medium |
| (iii) + delegates + 37 required (+047) | 157 | 106 (89) | 4 (ivan→test-first-bug-fixing, renata→adversarial-squad, 047→2 writing procedures) | none | Role gaps remain; 2 profile how-tos dangle | Low–medium |
| (iv) (iii) + researcher-robbie, spike-timebox-policy, retrospective-facilitator, adversarial-squad-deployment, kitty-glossary-writing, test-first-bug-fixing | 163 | 90 (73) | 2 (047→writing procedures, relocatable into writing) | none | Only "suggests" and "scope" enrichment is lost | **Low** |

Without the 047 fix the counts are: (ii) 119 nodes / 141 out-edges, (iii) 156 / 102, both still carrying the cycle. Cut (iii) is requires-closed: the 37 added nodes pull nothing further.

## 6. Challenges to ruling 2 and ruling 4

**Ruling 2 (the documentation mission in writing).** The direction is right: writing → foundation, through 52 edges and every documentation delegate. The awkward parts:

- 047 is split away from annie (finding 0.1).
- Larry's and Daisy's body references point into staging (finding 0.2).
- `action:documentation/design instantiates` the 3 c4-*-mermaid templates, which are in staging. Daisy is in writing while her C4 directive and templates are not.
- The documentation mission's researcher, architect and facilitator steps have no profile in writing.
- The inverse coupling, research (foundation) → research-citation-discipline (writing), suggests that styleguide belongs with the research mission in foundation.

None of this argues against ruling 2 itself. It argues for a writing curation pass.

**Ruling 4 (org packs depend directly on foundation and writing).** It has a real cost:

- Built-in holds `policy.yaml` (the generic-agent lock) and `fallback_profile`. Both are judged along the written pack's closure (ADR-0063 D3, ADR-0065 D5, ADR-0068 d2/d3/d5).
- An org pack whose closure is {org, foundation} sees **neither**. Its writes are not bound by the generic-agent lock, so it could replace the fallback profile.
- A context composed only of such a closure has no fallback in force, so a role gap answers `no_profile_matched` (404) instead of the fallback.
- **Fix:** move `policy.yaml`, or a copy of the lock, and a `fallback_profile` declaration onto foundation. Built-in may keep its own declaration; both name the same id, so ADR-0068 sees no conflict.
- A further cost: org packs now pin foundation and writing version ranges directly, so 2 ranges must be kept in step.

**Ruling 7 (aside, not decided here).** Under the level rule built-in may depend only on built-in-level packs, so it can never aggregate an org-level `java`. That question is open only if java becomes built-in level.

## 7. Recommendation

**Steelman of strict.**
- Foundation should be small, stable and low on opinion.
- Procedures are opinionated *how*: GitHub-PR landing, `--no-gpg-sign`, Git Flow. Directives are the portable *what*.
- Keeping the how-tos out keeps the reviewable and lockable surface small, makes every opinion an explicit opt-in, and lets orgs supply their own procedures.
- A 115-node base is also easier for core to align to later.

**Why it does not hold.**
- The layer merge already lets an org override a foundation procedure by id. The replaceability gain is mostly illusory.
- The how-tos have no other consumer, and therefore no bundle to be carved into.
- Several directives are hollow without them (010, 053).
- The strict cut deletes extension points that opting in cannot restore.
- The strict cut ships mission types whose requested roles foundation cannot fill.
- As approved, the cut is invalid (047).

**Recommended: cut (iv), about 163 nodes, 90 relocated edges.** It keeps the strict spirit: still no architect, diagram or planner profiles, no stacks, no DDD or C4. Concretely:

1. Pull in the 4 step delegates and the 37 required how-tos.
2. Fix 047 by moving it to foundation, as ruling 1's own rule requires. The alternative is to drop the reference from annie.
3. Add the two role-filling profiles the base missions request (researcher-robbie with spike-timebox-policy, and retrospective-facilitator), plus adversarial-squad-deployment, kitty-glossary-writing and test-first-bug-fixing.
4. Consider moving research-citation-discipline into foundation.
5. Fix writing's 3 body references into staging.
6. Put the fallback lock and declaration on foundation.

If the operator wants to stay minimal, **(ii)+047 is the floor**: it is the smallest valid cut that does not remove step-contract hooks. **(i) as approved should not ship.**
