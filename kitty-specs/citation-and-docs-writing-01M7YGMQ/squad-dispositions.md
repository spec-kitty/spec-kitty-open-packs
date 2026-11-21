# Pre-merge squad: findings and dispositions

Squad (adversarial-squad-deployment, pre-merge point-cut): reviewer-renata, architect-alphonso, curator-carla, read-only, over `feat/citation-and-docs-writing-clean` at the "docs(changelog): citation rules, first-hand squad checks ..." commit. Every finding below carries exactly one disposition.

| # | Lens | Severity | Finding | Disposition | Evidence |
|---|------|----------|---------|-------------|----------|
| 1 | reviewer, curator | MAJOR | `common-docs-page-authoring` still teaches "resolvable repo-relative paths" | accepted | procedure step "Express cross-references as `related:` page slugs ..." |
| 2 | reviewer | MAJOR | Divio templates give `audience` as one scalar | accepted | the four `templates/divio/*-template.md` frontmatter blocks |
| 3 | reviewer | MAJOR | specify/plan reminder restates both rules in three sentences | accepted | one-sentence reminder in both prompts, naming the styleguide |
| 4 | architect, curator | MAJOR | figure labelling has two homes; "every figure" fails reference pages | changed | ai-writing-tells "Label gathered versus synthesized figures" scoped to measured or reported results; report-writing "Attribute every number" keeps sourcing and points to it; pointer sentence narrowed |
| 5 | reviewer | MINOR | squad procedure requires `file:line` findings | accepted | "[SEVERITY] file:anchor ..." in the structured-output step |
| 5a | reviewer | MINOR | `durable-fix-investigation` and DIRECTIVE_052 use `file:line` too | deferred_with_rationale | outside this mission's surfaces; tracked in #339 |
| 6 | architect, curator | MINOR | `styleguide.graph.yaml` edge text says "related: paths" | accepted | edge `when:` now "related: page slugs" |
| 7 | architect | MINOR | intensifier pattern overlaps plain-language meta-narration | changed | pattern names plain-language as owner of hedging, filler and meta-narration and adds only emphasis words and openers |
| 8 | architect | MINOR | the ADR tactic and squad procedure name the citation styleguide, but the graph does not deliver it there | accepted | writing `tactic.graph.yaml` and `procedure.graph.yaml` `suggests` edges from the two foundation nodes (precedent: refactoring's foundation::tactic sources) |
| 9 | architect | NIT | em-dash rule vs meeting-minutes separators | accepted | structural-separator clause in "Ration the em-dash" |
| 10 | curator | MINOR | "a handful" is not checkable | accepted | "at most two per page, none in headings or bullets" |
| 11 | curator | MINOR | "genuinely necessary" undefined | accepted | condition stated: no PR, issue, ADR id or tag exists yet |
| 12 | curator | MINOR | ADR tactic said "not by commit SHA" and omitted descriptions | accepted | "or a description of the change, not by a bare commit SHA" |
| 13 | curator | MINOR | unverified claim that doc-kitty link-checks external_references | accepted | claim removed |
| 14 | curator | MINOR | `context/audience/` relative to what; soft miss wording | accepted | "under the docs root"; "only warns ... never fails the build, so review enforces the rule" |
| 15 | curator | NIT | `git grep -c` does not give one total | accepted | example uses `git grep -n ... | wc -l` excluding the definition file |
| 16 | curator | NIT | principles cross-link each other and the patterns too | deferred_with_rationale | the operator default asks for the two rules to be stated once and cross-referenced; the principle-level pointer is what charter context surfaces |
| 17 | reviewer | MINOR | changelog omits surfaces and overstates | accepted | Changed entry lists every surface; Added entry names the anchor format |
| 18 | reviewer | NIT | tactic omits `{type, id}` | accepted | "or type and id" |
| 19 | reviewer | NIT | internal page-audience asserts doc-kitty unconditionally | accepted | "Where the repository builds its docs with doc-kitty ...; otherwise use the location the charter names" |
| 20 | reviewer | NIT | plan.md cites the earlier charter pin | deferred_with_rationale | plan.md records the pin at authoring time; main moved the pin to release `service-v0.1.0-rc.3` afterwards, and the PR validates against that |

## PR-level review (reviewer-renata, approved)

| # | Severity | Finding | Disposition | Evidence |
|---|----------|---------|-------------|----------|
| R1 | MINOR | the #219 reminder covers only software-dev prompts | accepted | the plan mission's and qa's specify and plan prompts carry the same sentence; qa 5.2.0 |
| R2 | MINOR | deferred finding 5a needs a tracking issue | accepted | #339 |
| R3 | MINOR | foundation pointers to writing drop "(when installed)" | accepted | all foundation pointers carry the qualifier |
| R4 | NIT | "retired" vs "legacy" | accepted | internal page-audience says "legacy form" |
| R5 | NIT | rule 4 sits only in cloud-session-dispatch | deferred_with_rationale | the issue asks for "a step in an existing internal procedure"; the reviewer rated it acceptable |
