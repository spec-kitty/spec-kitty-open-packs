# Research: consumer packs reference this repo's tree, core paths and internal-only artifacts (#258, #259, #265)

Grounding note for #265 (P2), landed together with #258 and #259 (P3), all children of the content-audit
epic #263. Branch `fix/consumer-pack-references-258-259-265` off `main` `c0ec640`. Delivery shape: an Op
(content bugfix), not a Mission.

## Reference points

- Spec Kitty CLI: `/opt/spec-kitty` at `9e7272db84`, `spec-kitty-cli 4.0.0rc9`. A `git pull` there was
  refused in this session, so the checkout was used as found. Core reads project profile overrides from
  `.kittify/charter-packs/agent_profiles/` (`src/charter/activation/synthesizer/project_drg.py:168`).
  Nothing in `src/` reads `.kittify/charter/agents/`.
- Charter contract: spec-kitty-charter at the pin `eacbc3c` (`charter.lock.yaml`), cloned locally and passed
  through `CHARTER_CONTRACT_DIR` (the raw fetch returns 404 here).
- `depends_on` closures used below: foundation {}; writing, testing, cave-kitty {foundation}; refactoring
  {foundation, testing}; architecture {foundation, refactoring, testing, writing}; python, java, javascript
  {foundation, testing}; spdd {architecture, foundation, refactoring, testing, writing}; qa {foundation,
  planning-analysis, testing, architecture, refactoring, writing}.
- Line numbers are on `main` `c0ec640`. Where they drifted from the issue text, the issue's number is in
  parentheses.

## #258: `packs/built-in/...` paths

All ten re-verified. Each now names the artifact (and its pack when it is in another one) rather than a path.

| Instance | Fix |
| --- | --- |
| `writing/styleguides/common-docs.styleguide.yaml:168` (comment) | "assets/docs_structural_lint.config.yaml in this pack" |
| `writing/styleguides/divio-type-discipline.styleguide.yaml:77,85,94,102` | "the documentation mission's `divio/<q>-template.md` template" |
| `writing/styleguides/docs-accessibility.styleguide.yaml:122` | "the mermaid-diagramming and plantuml-diagramming toolguides" |
| `writing/styleguides/docs-freshness-sla.styleguide.yaml:140` | "the documentation-gap-prioritization procedure" |
| `writing/styleguides/publication-authority.styleguide.yaml:121` | "DIRECTIVE_037 (living-documentation-sync, foundation pack)" |
| `writing/assets/docs_structural_lint.config.yaml:9` (comment) | "the common-docs styleguide (styleguide:common-docs)" |
| `planning-analysis/styleguides/planning-and-tracking.styleguide.yaml:146` | "the github-tracker toolguide, foundation pack" |
| `planning-analysis/paradigms/brownfield-onboarding.paradigm.yaml:59` (comment) | "this pack's graph fragment (drg/fragment.yaml)" |
| `internal/drg/fragment.yaml:264` (comment) | `<pack>::<kind>:<id>` URNs "verified present in the named pack" (internal is maintainer-only, so a repo path is fine) |
| `internal/glossary_packs/spk-internal-glossary.glossary-pack.yaml:4` (comment) | `packs/foundation/glossary_packs/spec-kitty-core` |

After the fix `grep -rn "packs/built-in/" packs` hits only pack READMEs and `packs/built-in.source.yaml`.
The README provenance paragraphs are #273's (comment on #258). `internal/README.md:6,11,18,196,236` is the
pre-split internal README, tracked by #272.

## #259: core `src/` paths

| Instance | Fix |
| --- | --- |
| `python/toolguides/python-review-checks.guide.md:71` | `src/myproject/domain/` / `src/myproject/cli/` |
| `python/toolguides/python-review-checks.guide.md:135` | Already neutral on main (`mypackage.core*`, fixed by #264). No change |
| `testing/styleguides/testing-principles.styleguide.yaml:107,120,243,249` | `src/myproject/...`; the domain class becomes `Order` |
| `testing-principles.styleguide.yaml:222-225,250-256` (#259 comment: neutralise together) | `order_id` ULID fixture; `test_order_rejects_empty_customer_id`; an `orders list` CLI call replaces `agent tasks status` |
| `writing/toolguides/mermaid-diagramming.guide.md:245,271,281` | Theme/example claims removed; the guide's inline theme snippets stay; a "Templates" section says the pack ships none. The architecture pack's `c4-*-mermaid-template` nodes are file-less too (#196), so the guide does not point at them |
| `writing/toolguides/plantuml-diagramming.guide.md:60,205,279` | The render example uses `docs/diagrams/*.puml`; Theming says the pack ships no theme files (theme names kept as suggestions); "Templates" says none ship. The stickies-theme mentions at mermaid `:24,:248` and plantuml `:15` reworded with them |
| `writing/toolguides/contextive.guide.md:156` | The Bounded Context Canvas link becomes `architecture::tactic:bounded-context-canvas-fill`, when installed |

Porting core's diagram templates into writing (the other option in the #259 comment) was not done: it adds
content, and nothing asked for it. File a follow-up if the templates are wanted.

## #265: this repo's tree, internal-only ids, dead paths, closure

| Instance | Fix |
| --- | --- |
| `foundation/missions/software-dev/steps/implement.prompt.md:288-294` | Step 3 searches the project's own templates, scaffolds and project pack files |
| `implement.prompt.md:296-302` | Step 4 searches project-authored agent files (`AGENTS.md`, `CLAUDE.md`, custom commands or skills) and skips the generated ones |
| `implement.prompt.md:337-338` | Cites `DIRECTIVE_045` only |
| `implement.prompt.md:76` | Example profile is `implementer-ivan` (foundation), with its real directive references |
| `implement.prompt.md:163` (`:157`) | Supply-chain toolguides qualified (`javascript::toolguide:...` etc.) "when its language pack is installed" |
| `software-dev/steps/review.prompt.md:271` | "the python pack's `python-pedro` when that pack is installed" |
| `foundation/agent_profiles/README.md:18-19` | `.kittify/charter-packs/agent_profiles/`, with a new `profile-id`: core's synthesis refuses a project profile that reuses a shipped id (`project_drg.py:184`, INV-1), so the README says to author a specializing profile instead of a same-id override |
| `foundation/procedures/adversarial-squad-deployment.procedure.yaml:22` | Fallback reads `agent_profiles/<id>.agent.yaml` in the installed pack |
| `adversarial-squad-deployment.procedure.yaml:88-93` | Cast by role; names the three foundation profiles; others "need a pack that ships them". `doctrine-daphne` becomes an analyst |
| `foundation/tactics/reviewer-implementer-role-separation.tactic.yaml:69-76` | `mission_type:software-dev`; step prompts named by step |
| `foundation/tactics/ownership-map-leeway.tactic.yaml:47-48` | Step prompts named by step and `mission_type:software-dev` |
| `python/toolguides/python-mutation-tools.guide.md:6,7,195` | `testing::styleguide:mutation-aware-test-design`, `testing::tactic:mutation-testing-workflow` |
| `javascript/toolguides/typescript-mutation-tools.guide.md:6,7,195` | Same |
| `writing/toolguides/contextive.guide.md:148` | `foundation::tactic:glossary-curation-interview` |
| `testing/procedures/development-assist-test-cleanup.procedure.yaml:7,42-44,62` | Trigger "after acceptance, before merge"; tracer-files dropped. The sequencing edge already exists in internal (`mission-wrap-up-sequence` -> `testing::procedure:development-assist-test-cleanup`, `internal/drg/fragment.yaml:755`), so no new edge |
| `qa/procedures/qa-go-no-go-readiness-review.procedure.yaml:5` | "a mission close-out sequence", not the internal id |
| `writing/assets/audiences/README.md:3,42` | The persona is dropped from the frontmatter and table |
| `writing/tactics/communication/writing-audience-catalog.tactic.yaml:15-18` | Lists the four shipped personas |
| `writing/agent_profiles/comms-cleo.agent.yaml:122` | "four personas" |
| `writing/tactic.graph.yaml:83,87`, `writing/template.graph.yaml:11,13` | Both file-less template nodes and their two `suggests` edges removed (done-when option 2; #196 can add them back with files) |
| `writing/assets/audiences/README.md:17-18` | Names the `stakeholder-alignment` tactic only |
| `writing/tactics/communication/stakeholder-alignment.tactic.yaml:46` | "the project's context canvas (its problem statement, organisational context and stakeholder map) or prestudy" |
| `architecture/agent_profiles/architect-alphonso.agent.yaml:136,149` | "the javascript pack's javascript-supply-chain toolguide (when installed)" |
| `testing/tactics/testing/formalized-constraint-testing.tactic.yaml:83` | The safety warning stays (a testing-only consumer still needs it); its citation becomes "the java pack's java-conventions styleguide, when installed". java holds the full rule and the edge `testing::tactic:formalized-constraint-testing -> styleguide:java-conventions`. The issue's "move it to the java pack" read literally would drop the warning for testing-only consumers |
| `cave-kitty/styleguides/cave-sty-001-communication.styleguide.yaml:16` (comment) | "the writing pack's `professional-communications`, when installed" |
| `javascript/styleguides/typescript-conventions.styleguide.yaml:18-19` (comment) | "the testing pack's" (testing is in the closure) |
| `spdd/README.md:12` | Names the real dependencies |
| `writing/agent_profiles/diagram-daisy.agent.yaml:22,33` | The architecture pack's directive, "when installed" |
| `foundation/directives/red-main-release-discipline.directive.yaml:18-19` | "the testing pack's test-first-bug-fixing procedure, when installed" |

## Similar-surfaces sweep

Sweeps run on the branch: every `packs/built-in/`, `src/(specify_cli|charter)`, `packs/` and `.kittify/` mention
outside `packs/internal`; every relative Markdown link in `packs/` resolved on disk; every internal-pack
artifact id grepped in the consumer packs; every agent-profile, styleguide, tactic, procedure, toolguide and
paradigm id grepped in packs outside its owner's closure (graphs, manifests and presets excluded).

| Find | Disposition |
| --- | --- |
| `qa/toolguides/sonar.guide.md:7-8`: two `../styleguides/` links into testing | In scope (same class as the mutation guides): cited by id |
| `foundation/missions/software-dev/templates/plan-template.md:6`: `packs/foundation/.../plan.prompt.md` | In scope: "the software-dev mission's `plan` step prompt" |
| `foundation/missions/software-dev/steps/tasks-packages.prompt.md:239`: `packs/<pack>/agent_profiles/` fallback | In scope (same as the squad fallback): installed packs plus the project pack layer |
| `foundation/missions/research/steps/output.guidelines.md:9`: `packs/foundation/.../research-output.step-contract.yaml` | In scope: "the research mission's `output` step contract" (wording survives the #285 fold) |
| `writing/tactics/common-docs-find.tactic.yaml:24`: `packs/<pack>/...` graph files | In scope: pack-relative wording |
| `writing/agent_profile.graph.yaml:40`: "five personas" | In scope: "four" |
| Out-of-closure prose: `foundation/tactics/reviewer-implementer-role-separation.tactic.yaml:18-21` (python-pedro, java-jenny), `foundation/tactics/architecture/dependency-hygiene.tactic.yaml:13`, `foundation/procedures/test-first-cycle.procedure.yaml:13` (zombies-tdd), `foundation/missions/research/steps/{scoping,gathering,synthesis,methodology}.prompt.md:6` (researcher-robbie), research `gathering:48`, `synthesis:34`, `methodology:47` (research-citation-discipline), `{research,software-dev}/steps/retrospect.prompt.md:43` (kitty-glossary-writing) | In scope under #265's done-when ("each cross-pack prose reference is pack-qualified and optional, or in the closure"): pack named, "when installed" |
| `cave-kitty/missions/cave-dev/steps/{discovery,plan,tasks}.prompt.md` | Already pack-qualified and optional. No change |
| `foundation/missions/software-dev/steps/charter.prompt.md:304` (`domain-driven-design` in a sample charter) | Example config, not a reference. No change |
| `foundation/tactics/canonical-source-unification.tactic.yaml:19` (`packs/<pack>/missions/<type>/templates/`) | In scope (#265 done-when grep; also listed on #195): the one line is pack-relative now. Its core-symbol examples (`:17-18,27,41-45`) stay #274's |
| `testing-principles.styleguide.yaml:80` (`primary_feature_dir_for_mission`), `:233-237` (PR #2308, commits) | #274 / #273 respectively. Comment on #274 for `:80` |
| `development-assist-test-cleanup.procedure.yaml:55,65-67` (core issue numbers) | Already in #273 |
| `foundation/directives/034-test-first-development.directive.yaml:19-25` (comment naming testing/architecture ids) | Already in #273 |
| `drg/fragment.yaml:2` "Carved from packs/built-in by #73" in architecture, drupal, java, javascript, pack-authoring, planning-analysis, python, refactoring, testing | Provenance class: comment on #273 |
| Pack README links into `docs/` (go, rust, qa, `foundation/missions/README.md`) and `src/charter/offering` in `foundation/missions/README.md:38` | Already in #273 (`foundation/missions/README.md:32-39,43-44`); go/rust/qa README links are human-facing adoption links #273 asks for. No change |
| `foundation/README.md:22`, `foundation/agent_profiles/README.md:6` (writing/java/architecture profiles) | #195 (profile prose) / #273 (README). No change |
| `foundation/glossary_packs/spec-kitty-core.glossary-pack.yaml` (core paths, out-of-closure ids) | Out of scope per #259 (#221 / #234) |
| `planning-analysis/procedures/situational-assessment.procedure.yaml:9-13` ("System Context Canvas template") | #196 (it restores `situational-assessment -> system-context-canvas-template` with a file). Comment on #196 that the node is now gone |
| `planning-and-tracking.styleguide.yaml:104` (`.kittify/glossaries/...`) | Already in #274 |
| `pack-authoring/procedures/migrate-project-guidance-to-spec-kitty-charter.procedure.yaml:24` (`.kittify/glossaries/<scope>.yaml`) | Live: core still reads the seed files (`src/glossary/scope.py:73`). No change |
| Other `.kittify/` paths (`overrides/templates/`, `charter-packs/`, `memory/`, `config.yaml`, ...) | Not re-verified one by one; none is in this issue's class beyond `.kittify/charter/agents/`. No change |

## Tracked issues checked

- #263 children: #264 landed (it fixed `python-review-checks:135`); #275 landed. #266 (software-dev
  contradictions) touches `implement.prompt.md` in other sections; whoever lands second rebases.
- #139 (HiC): `contextive.guide.md:173` "HiC approval" is #139's; not touched.
- #273, #274: overlaps above stay theirs.
- #283 (glossary migration) and #285 / PR #289 (slice F: step contracts fold, scope edges): no shared lines.
  Both restamp foundation, writing, qa and testing digests and pages: whoever lands second rebases and
  restamps.
- #195 (profile prose): this branch resolves the #195 comment's path items (`implement.prompt.md:290,293`,
  `tasks-packages:239`, `plan-template:6`, `ownership-map-leeway:47-48`,
  `reviewer-implementer-role-separation:18-21,69,75-76`, `canonical-source-unification:19`). The
  collaboration lists stay #195's.
- #196: the two template nodes are removed here (comment there).
