# Research note: stale paths left by the pack split (#195, #227, #159)

Op `01M7B0J0DT203DRBJJFR1ZT5HF` (profile `curator-carla`). Slice 4 of the November 2026 slice plan (`docs/plans/next-slices-2026-11.md`, unmerged, on `docs/catalog-disposition-2026-11`). Grounded on `origin/main` at `736e613`, spec-kitty CLI 4.0.0rc9 (core `1fb3b55`). Kind: tidy-first, so content changes preserve behaviour.

## Issues read

- **#195** (Bug, P2, parent #190). Collaboration lists in `analyst-annie`, `diagram-daisy` and `lexical-larry` name profiles outside their pack's `depends_on` closure. Prose calls bundle profiles "built-in". A comment widens the scope to moved content that still points at `packs/built-in/...` paths: seven locations, including `.agents/skills/spec-kitty.tasks-packages/SKILL.md:276`.
- **#227** (Bug, P2). The `adversarial-squad-deployment` procedure has no harness-aware read-only wording, no injected-profile route and no diff pre-loading. Its fallback path, `packs/built-in/agent_profiles/<id>.agent.yaml`, is stale. Acceptance: (1) the procedure names the harness modes that block the CLI and says what the orchestrator then does; (2) the profile-load step gives the injected-profile route first and a corrected on-disk fallback second; (3) the dispatch step requires the review target's diff in the delegate prompt when delegates cannot run `git`.
- **#159** (Task, P3, parent #221). The `glossary-curation-interview` tactic cites core `src/specify_cli/...` paths. The fix lands here; the provenance baseline in core shrinks through a later pin bump.

## Pack closure (from `pack.yaml` `depends_on`)

| Pack | Closure |
| --- | --- |
| foundation | foundation |
| writing | foundation, writing |
| testing | foundation, testing |
| refactoring | foundation, testing, refactoring |
| architecture | + refactoring, testing, writing |
| planning-analysis | + architecture (and its closure) |
| cave-kitty | foundation, cave-kitty |
| qa | + planning-analysis, testing (and their closures) |

## Similar-surfaces sweep

Command: `grep -rn "packs/built-in/" packs .agents`, plus `grep -rnE "\bsrc/"` for core paths. A generic `src/` path in a consumer example (for example `src/myapp/...`) is not a core path.

### In scope now

| Location | Defect | Fix |
| --- | --- | --- |
| `foundation/procedures/adversarial-squad-deployment.procedure.yaml:19` | stale path; #227 wording | rewrite the dispatch step (#227) |
| `foundation/missions/software-dev/steps/tasks-packages.prompt.md:239` | stale `packs/built-in/agent_profiles/` | per-pack `packs/<pack>/agent_profiles/` |
| `foundation/missions/software-dev/steps/implement.prompt.md:290,293` | stale step-prompt path and grep | `packs/<pack>/missions/<type>/steps/` |
| `foundation/missions/software-dev/templates/plan-template.md:6` | stale path | `packs/foundation/...` |
| `foundation/missions/research/steps/output.guidelines.md:9` | stale step-contract path (not named in #195; same defect) | `packs/foundation/...` |
| `foundation/tactics/ownership-map-leeway.tactic.yaml:47-48` | stale paths | `packs/foundation/...` |
| `foundation/tactics/reviewer-implementer-role-separation.tactic.yaml:69,75-76` | stale paths | `packs/foundation/...` |
| `foundation/tactics/canonical-source-unification.tactic.yaml:19` | stale path | the per-pack templates directory |
| `writing/tactics/common-docs-find.tactic.yaml:23` | stale graph path (not named in #195; same defect, a tactic) | each pack's per-kind graph files |
| `foundation/tactics/communication/glossary-curation-interview.tactic.yaml:16,30` | core `src/specify_cli/...` and `docs/adr/4.x/` (#159) | neutral `src/myproject/...`, `docs/adr/` |
| `foundation/agent_profiles/analyst-annie.agent.yaml` collaboration | `lexical-larry`, `architect-alphonso`, `python-pedro`, `java-jenny` outside closure | role words |
| `writing/agent_profiles/diagram-daisy.agent.yaml` collaboration | `architect-alphonso` outside closure | role word |
| `writing/agent_profiles/lexical-larry.agent.yaml` collaboration | `architect-alphonso` outside closure | role word |
| `cave-kitty/missions/cave-dev/steps/*.prompt.md` (8) | "a built-in <role> profile such as `<id>`" | name the pack that ships the profile |
| `qa/missions/qa/steps/discovery.prompt.md:11` | "`researcher-robbie` (built-in)" | name the pack |
| `writing/agent_profiles/comms-cleo.agent.yaml:32` (comment) | "The built-in profile keeps..." | "This profile keeps..." |

Every other profile's collaboration list already uses role words (`architect`, `reviewer`, ...) or profile ids inside its pack's closure. The script that checked this against the closure is reproduced in the PR's Tests run section.

### File and link (out of scope: not a prompt, procedure or tactic)

- **Styleguides, assets, a paradigm and graph comments that cite `packs/built-in/...`.** Affected: `writing/styleguides/{common-docs,divio-type-discipline,docs-accessibility,docs-freshness-sla,publication-authority}`, `writing/assets/docs_structural_lint.config.yaml`, `planning-analysis/styleguides/planning-and-tracking`, `planning-analysis/paradigms/brownfield-onboarding` (a comment), `internal/drg/fragment.yaml` (a comment) and `internal/glossary_packs/spk-internal-glossary` (a comment). One follow-up issue. `common-docs` overlaps #240.
- **Toolguides and styleguides that cite core `src/` paths.** Affected: `python/toolguides/python-review-checks.guide.md` (`src/specify_cli/status/`), `testing/styleguides/testing-principles` (`src/specify_cli/...`), `writing/toolguides/{mermaid,plantuml}-diagramming.guide.md` and `contextive.guide.md` (`src/charter/offering/templates/...`). One follow-up issue.
- **`.agents/skills/spec-kitty.tasks-packages/SKILL.md:276`.** This is a generated agent copy, and the rc9 renderer can't regenerate it narrowly (it changes layout and directory names). Escalated to the operator; see the PR.

### No change (correct as written)

- **Pack `README.md` provenance paragraphs** ("carved out of `packs/built-in/` by #73"): history, not a pointer.
- **`internal/README.md`:** a maintainer document about the tiers; not shipped.
- **`packs/built-in.source.yaml`:** a provenance sidecar.
- **`foundation/missions/README.md:38`:** describes where core reads the data; core's own layout.
- **`doctrine-daphne.agent.yaml:149`:** a dated measurement ("16 built-in profiles carry..."), not a profile pointer.
- **Profile names in prose outside a collaboration list:** the squad procedure's "Example casting" notes and `reviewer-implementer-role-separation` ("such as python-pedro or java-jenny"). These are labelled examples, not pointers, and they don't claim the profiles are installed.
- **"the built-in software-dev `<action>`" and "default built-in template chain" in the `cave-kitty` step prompts:** these name core's `software-dev` mission family, which the CLI keys on. They don't name a profile or a path.
- **`canonical-source-unification.tactic.yaml:27`:** a generic `grep ... src/ tests/`.
- **`foundation/glossary_packs/spec-kitty-core.glossary-pack.yaml`:** cites core `src/` deliberately as the core glossary. Glossary work waits on #221 and #234.

## Tracked-issues sweep

| Issue | Relation | Disposition |
| --- | --- | --- |
| #190 | parent epic of #195 | Refs |
| #221 | parent of #159 | Refs |
| #207 | prompt and template hygiene epic | Refs; no child is fixed here |
| #164 | edits `implement.prompt.md` (charter-section names), different lines | Refs, not folded; slice 5 |
| #161 | research prompts cite slugs, not ids | unrelated defect; not folded |
| #240 | `common-docs` styleguide frontmatter | Refs: the stale-path follow-up for styleguides touches the same file |
| #245 | DRG and graph hygiene epic | unrelated (graph content, not prose paths) |
| #229 | maintainer how-to for built-in artefacts | unrelated |
| #250, #252, #255 | slice 1 (manifests, digests, charter pin), running in parallel | sequencing only: whoever lands second restamps digests |
| core #2304, core #3811 | core half of #227 (skill and injection mechanism) | Refs; core's shipped `adversarial-squad` skill is out of scope |

No duplicate or superseding issue was found.

## Notes

- The plan lists #159 under "After slice 1", because #242 rewrites the core glossary pack. #241 and #242 have already merged (`1692a3b`). #159 edits a tactic, not the glossary pack, so the two don't collide.
- Running `spec-kitty charter context` / `doctor skills` in rc9 auto-migrated the 14 `.agents/skills/spec-kitty.*` directories to `spec-kitty-*` in the working tree. The migration was reverted because it is outside this scope.
