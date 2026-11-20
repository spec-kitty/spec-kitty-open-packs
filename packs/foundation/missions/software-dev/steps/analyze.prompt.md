---
description: Cross-artifact consistency and quality analysis
---
## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

**In repos with multiple missions, pass `--mission <handle>` to every command that accepts `--mission`.** The `<handle>` can be the mission's `mission_id` (ULID), `mid8` (first 8 chars of the ULID), or `mission_slug`. The resolver disambiguates by `mission_id` and returns a structured `MISSION_AMBIGUOUS_SELECTOR` error on ambiguity - there is no silent fallback.

## Goal

Identify inconsistencies, duplications, ambiguities, and underspecified items across the planning corpus before implementation: `spec.md`, `plan.md`, `tasks.md`, every WP prompt (`tasks/WP*.md`), the other planning artifacts and the creation intent (step 1); confirm that the machine-checkable task metadata would pass `finalize-tasks` validation; judge whether the requirements are good enough to build from; and judge whether the plan still serves the intent the Mission was created for. This command MUST run only after `/tasks` has successfully produced a complete `tasks.md`.

## Operating Constraints

**NON-REMEDIATING**: Do **not** modify `spec.md`, `plan.md`, `tasks.md`, WP files, any other planning artifact, `meta.json`, `occurrence_map.yaml`, `decisions/`, source code, or any remediation target. The only permitted file mutation is persisting this command's report to `kitty-specs/<mission>/analysis-report.md` via `spec-kitty agent mission record-analysis`. Offer an optional remediation plan only after the report is persisted (user must explicitly approve before any follow-up editing commands would be invoked manually).

**READ-ONLY VALIDATION**: The only `finalize-tasks` invocation this command may make is `--validate-only` (step 2a). Never run `finalize-tasks` without `--validate-only`, and never pass `--refresh-planning-commit` or `--allow-orphaned`: those are the finalization write and commit paths. A `--validate-only` run writes nothing to disk; it only previews the frontmatter bootstrap, the lane computation and the topology decision in memory. Treat everything it reports as a preview of what finalization would do, never as something that happened; a `topology_decision` in the output carries `"preview": true` for the same reason.

**Charter Authority**: The project charter (`.kittify/charter/charter.md`) is **non-negotiable** within this analysis scope. Charter conflicts are automatically CRITICAL and require adjustment of the spec, plan, or tasks - not dilution, reinterpretation, or silent ignoring of the principle. If a principle itself needs to change, that must occur in a separate, explicit charter update outside `/analyze`.

**Issue-Matrix Approval Heads-Up (non-gating)**: if any artifact cites a GitHub
issue number (`#NNNN`), a bare/unmarked reference will later require an issue-matrix row
before its owning work package can be approved. A context-only citation (e.g.
`Follow-up:`, `see #`, `parent`, `epic`) or a PR/commit reference (`PR #NNNN`, a
`/pull/NNNN` URL) is non-gating and needs no row; if an issue genuinely owes the mission
no work, it can later be recorded with the `not-applicable` verdict. This is
informational only - it does not gate `/spec-kitty.analyze`.

## Execution Steps

### 1. Initialize Analysis Context

Run `spec-kitty agent mission check-prerequisites --json --include-tasks --mission <mission-slug>` once from repo root and parse JSON for mission_dir, `artifact_files`, `artifact_dirs`, target_branch, and base_branch (`artifact_files` and `artifact_dirs` map keys to paths; read them in step 2). Derive absolute paths:

- SPEC = mission_dir/spec.md
- PLAN = mission_dir/plan.md
- TASKS = mission_dir/tasks.md

Abort with an error message if SPEC, PLAN or TASKS is missing (instruct the user to run missing prerequisite command).

- META = mission_dir/meta.json: the creation intent is `purpose_tldr`, `purpose_context` and `source_description`; note which are absent. It is not in the inventory. `meta.json` missing: say so in the report and compare against what exists; never abort for it.
- PLANNING ARTIFACTS = every `artifact_files` and `artifact_dirs` entry whose path is not already loaded above or in step 2 (spec, plan, tasks, the WP prompts), except `feature_dir`, which is the mission directory itself; plus `mission_dir/occurrence_map.yaml` when it exists (bulk-edit Missions) and, when present, the recorded decisions: list `mission_dir/decisions/` and read the decision records it holds (not `index.json`); neither is inventoried. A directory whose files are already loaded (the WP prompt directory) counts as loaded. Use no glob and no fixed list of key names.

### 2. Load Artifacts (Progressive Disclosure)

Load only the minimal necessary context from each artifact:

**From spec.md:**

- Overview/Context
- Functional Requirements
- Non-Functional Requirements
- User Stories
- Edge Cases (if present)

**From plan.md:**

- Architecture/stack choices
- Data Model references
- Phases
- Technical constraints

**From tasks.md:**

- Task IDs
- Descriptions
- Phase grouping
- Parallel markers [P]
- Referenced file paths

**From every `tasks/WP*.md` (the prompts implementation agents execute; `tasks.md` alone is not enough):**

- Frontmatter first, then the body's section headings; read a body section only when a step 2b check needs it

**From meta.json:** the three creation-intent fields.

**From every planning artifact:** headings first (for a directory, its file list and then each file's headings); read a body section only when a pass H or J check needs it. Record which inventory entries were read.

**From charter:**

- Load `.kittify/charter/charter.md` for principle validation

### 2a. Validate Task Finalization (read-only)

After loading the artifacts and before any detection pass, check the CLI version first:

```bash
spec-kitty --version
```

`--validate-only` exists from 3.0.0 but writes nothing only from 3.1.0a5. **If the version is below 3.1.0a5, or `spec-kitty` is not installed, stop here: do not run the check.** Record the could-not-run finding below and go on to step 2b. Otherwise run the read-only finalization check once from repo root:

```bash
spec-kitty agent mission finalize-tasks --validate-only --mission <mission-slug> --json
```

Parse the JSON it prints. Record the exit code, and keep the payload's keys and values verbatim for the report (step 6). Do not edit any artifact in response and do not re-run the check after a "fix": this command is non-remediating.

**The check is fail-fast.** Each gate refuses on its first failure and the run stops there, so a refusal reports one failure class only. Never read a single refusal as the only problem: the gates after it did not run. Say so in the report's residual-risk section.

Classify the result in this order; the first case that matches wins.

**1. The check could not run.** The CLI is older than 3.1.0a5 or missing, the command prints no JSON, or it fails to resolve the mission or the repository rather than judging the artifacts (an `error_code` such as `MISSION_AMBIGUOUS_SELECTOR`, `MISSION_CONTEXT_UNRESOLVED` or another `MISSION_*` resolution code, or the `error` "Could not locate project root"), or it refuses because of where it runs rather than what the artifacts say (a branch-contract or checkout `error_code` such as `PLANNING_BRANCH_NOT_PERSISTED`, `PR_BOUND_PLANNING_BRANCH_REQUIRED`, `PR_BOUND_RECOVERY_FOREIGN_META_DELTA` or `CHECKOUT_WRITE_OWNERSHIP_REFUSED`). This fails closed: add one **HIGH** finding in category `finalize-validation` that names `spec-kitty CLI >= 3.1.0a5`, the installed version (or "not installed") and how to get the check running (upgrade the CLI; pass an unambiguous `--mission` handle; run from the Mission's planning checkout), and add a Residual Risk entry saying requirement mappings, dependency cycles, ownership overlaps and WP metadata were not machine-checked. Continue with step 2b; do not re-implement the CLI's checks by hand as a substitute.

**2. Exit code non-zero with an `error` payload: a validation refusal.** `finalize-tasks` would refuse to finalize these artifacts, so the lanes implementation runs from cannot be computed from them. Report each refusal as a **CRITICAL** finding in category `finalize-validation`, quoting `error` and naming the WPs and ids from the payload. Recognise the refusal by the keys that carry a non-empty value (the requirement-mapping refusal lists all four of its keys, empty ones included):

| Payload key(s) | What it means |
|---|---|
| `missing_requirement_refs_wps` | WPs that map to no requirement |
| `unknown_requirement_refs` | WP requirement refs that name no id declared in `spec.md` (per WP) |
| `unmapped_functional_requirements` | Functional requirements no WP maps |
| `bare_prose_requirement_ids` | Requirement ids cited in prose but not declared in a recognised shape |
| `missing_wp_sections`, `extra_wp_sections` | WP prompt files with no matching `tasks.md` section, or `tasks.md` sections with no WP file |
| `cycles` | Circular WP dependencies (no valid execution order) |
| `wp_id` with `errors` | Invalid dependencies of one WP (for example a dependency on a WP that does not exist) |
| `dependency_conflicts` | WP frontmatter `dependencies` disagree with the dependencies parsed from `tasks.md` |
| `ownership_errors` | Ownership validation failed, for example two WPs that can run in parallel claiming overlapping `owned_files` (WPs ordered by a dependency may share files) |
| `ownership_literal_path_errors` | Literal `owned_files` paths that match no file and are not declared in `create_intent` |
| `ownership_contradiction_wp_ids`, `ownership_contradictions` | A `code_change` WP with an explicitly empty `owned_files` |
| `error_code: STALE_CANCELED_DEPENDENCIES` | Executable WPs that depend on canceled WPs |
| `risk_report` | Parallelization risk exceeds the project's blocking threshold |
| any other `error` or `error_code` (not a case-1 resolution code) | Report it verbatim: invalid WP metadata, an unloadable `wps.yaml`, a refused re-finalization of started work, or another gate |

**3. Exit code 0 with `"result": "validation_passed"`: the gates passed.** Still read the payload:

- `"validation_stage": "tasks-outline"`: only the `wps.yaml` outline exists and no WP prompt files were generated. Implementation cannot start: **CRITICAL**; Recommendation: run `/spec-kitty.tasks-packages`. Step 2b cites this finding for the missing prompts.
- `tasks_md_stale: true`: `tasks.md` is out of step with `wps.yaml`. **HIGH**; Recommendation: re-run `/spec-kitty.tasks-finalize`.
- `would_modify` not empty: finalization would still rewrite the frontmatter of the listed WPs (each entry names the `wp_id` and the `changes`). Either finalization has not run, or the WP files changed after it ran; either way the WP files are not the finalized metadata implementation will use. **HIGH**; Recommendation: run `/spec-kitty.tasks-finalize`.
- `ownership_warnings`, `requirement_extraction_warnings`, `post_integration_acceptance_warnings`: one **MEDIUM** finding per warning; they do not stop finalization.
- `success_criteria_coverage`: success criteria no WP references are informational; fold them into the coverage summary rather than raising findings.
- `validation.lanes_preview.collapse_report`: independent WPs collapsed into one lane are a **LOW** finding (lost parallelism), not a blocker.

### 2b. Review Every WP Prompt

Apply tactic `wp-prompt-readiness-review` (fetch: `spec-kitty charter context --include tactic:wp-prompt-readiness-review`) to every `tasks/WP*.md`. Read-only: never edit a WP prompt. In one line each, it checks:

- pairing both ways between `tasks.md` and the WP prompt files;
- each prompt against the WP prompt template **as resolved for this Mission**, naming gaps as the template names them (never from a list kept here);
- the agent-profile load as the first body section;
- size: target 200-500 lines; warn above 700 lines or more than 10 subtasks;
- dependency order, cohesive boundaries (an undeclared dependency on another WP's files is a blocker), and the mapping to requirements and user value.

Category `wp-readiness`. A blocker is **HIGH** (missing or orphaned WP prompt; a template field or section implementation depends on is missing or a placeholder; a WP mapped to no requirement; an undeclared dependency). A quality improvement is **MEDIUM** or **LOW** (profile load not first, size, overbroad scope, vague mapping wording). Where a `V` finding already covers a defect (pairing, `tasks-outline`, a cycle, a WP mapped to no requirement), cite its id in the Per-WP Readiness row instead of raising a `W` finding (see the one-defect rule in step 4).

### 3. Build Semantic Models

Create internal representations (do not include raw artifacts in output):

- **Requirements inventory**: Each functional + non-functional requirement with a stable key (derive slug based on imperative phrase; e.g., "User can upload file" -> `user-can-upload-file`)
- **User story/action inventory**: Discrete user actions with acceptance criteria
- **Task coverage mapping**: Map each task to one or more requirements or stories (inference by keyword / explicit reference patterns like IDs or key phrases)
- **Charter rule set**: Extract principle names and MUST/SHOULD normative statements

### 4. Detection Passes (Token-Efficient Analysis)

Focus on high-signal findings. Limit to 50 findings total; aggregate remainder in overflow summary.

**One defect, one finding.** The earliest step that detects a defect owns it - 2a, 2b, then passes A-G, H, J - and later steps cite its id (in the table's Notes, the Per-WP Readiness row or the section text) instead of raising their own. For example: a requirement with zero tasks (`unmapped_functional_requirements`), a WP mapped to no requirement (`missing_requirement_refs_wps`), an unknown requirement ref, a cycle, or a missing WP prompt.

#### A. Duplication Detection

- Identify near-duplicate requirements
- Mark lower-quality phrasing for consolidation

#### B. Ambiguity Detection

- Flag vague adjectives (fast, scalable, secure, intuitive, robust) lacking measurable criteria
- Flag unresolved placeholders (TODO, TKTK, ???, `<placeholder>`, etc.)

#### C. Underspecification

- Requirements with verbs but missing object or measurable outcome
- User stories missing acceptance criteria alignment
- Tasks referencing files or components not defined in spec/plan

#### D. Charter Alignment

- Any requirement or plan element conflicting with a MUST principle
- Missing mandated sections or quality gates from charter

#### E. Coverage Gaps

- Requirements with zero associated tasks
- Tasks with no mapped requirement/story
- Non-functional requirements not reflected in tasks (e.g., performance, security)

#### F. Inconsistency

- Terminology drift (same concept named differently across files)
- Data entities referenced in plan but absent in spec (or vice versa)
- Task ordering contradictions (e.g., integration tasks before foundational setup tasks without dependency note)
- Conflicting requirements (e.g., one requires Next.js while other specifies Vue)

#### G. Requirement Quality and Scenario Audit

Apply tactic `requirement-quality-ears` (fetch: `spec-kitty charter context --include tactic:requirement-quality-ears`). Pass B reports vague adjectives and placeholders; a `Q` finding covers only the properties B did not report, and cites the B id when both apply to one requirement. In one line each:

- each requirement is testable, solution-free, unambiguous, consistent and complete (category `requirement-quality`);
- behavioural requirements read against the EARS patterns as a lens, not a template, and state a response an actor or a test can observe (category `requirement-quality`);
- each user story gets a scenario audit in five kinds - accepted, rejected, missing edge, surprising accepted, surprising rejected - each row citing a `spec.md`, `plan.md` or `tasks.md` location (category `scenario`); a spec with no user stories gets "None." and no invented stories. Only missing-edge, surprising-accepted and surprising-rejected rows become `S` findings; accepted and rejected rows are context;
- every HIGH or CRITICAL ambiguity or requirement-quality finding gets a clarification question with two to four concrete choices and a recommendation, or a concrete remediation (the reworded requirement) in its Recommendation cell;
- a finding reached by judgement starts with `Inferred:` in both its carrier `summary` and its table Summary cell, and never claims proof. This applies to every judgement finding of step 2b and passes A-H and J; a `V` finding quotes the command output and never carries the label.

#### H. Intent & Planning-Artifact Consistency

Apply tactic `planning-corpus-consistency` (fetch: `spec-kitty charter context --include tactic:planning-corpus-consistency`) to the planning artifacts and creation intent loaded in step 2. Category `planning-artifact`. In one line each:

- each research, plan or recorded (`decisions/`) decision, and each deferred-decision marker, is implemented by a task or WP, explicitly deferred, or flagged; one implemented the other way is a contradiction;
- data-model entities, invariants and state transitions, contract operations and quickstart scenarios agree with the spec and are built or covered by a task or WP;
- `occurrence_map.yaml` (when present): every category's action is reflected in the WPs that own those files;
- any other planning artifact: content it states that no task or WP reflects;
- ungrounded behaviour: a task or WP that builds something no requirement, plan decision, planning artifact or creation-intent field asks for. A WP mapped to no requirement is a `V`, `W` or `C` defect: cite it.

Evidence for an `X` finding sits in a planning artifact, a `plan.md` or recorded decision, or `meta.json`: a `plan.md` decision no task implements is an `X` finding. Other differences among spec, plan and tasks stay with pass F.

#### J. Product Coherence

Apply tactic `product-coherence-review` (fetch: `spec-kitty charter context --include tactic:product-coherence-review`). Category `product-coherence`. Every finding starts with `Inferred:` and is MEDIUM or LOW; it never blocks the verdict. Review against the creation intent:

- intent drift; the MVP slice named in tasks.md (an MVP Scope note or any heading containing MVP; none: "MVP unclear") - never define MVP here;
- whether the first WPs deliver a vertical slice or only scaffolding (setup or foundation WPs the MVP slice directly needs are not scaffolding; flag only layers beyond what the first story consumes); overbuild beyond the stated need (work with no trace at all is an `X` finding: cite it);
- user journeys, actors, triggers, outcomes or failure cases lost between spec, plan and tasks; sequencing that delays all value or leaves a risky unknown last; WPs grouped by technical layer rather than user value.

End with exactly one recommendation: revise spec, revise plan, revise tasks, or proceed (step 6).

### 5. Severity Assignment

Use this heuristic to prioritize findings:

- **CRITICAL**: Violates charter MUST, missing core spec artifact, requirement with zero coverage that blocks baseline functionality, or a `finalize-tasks --validate-only` refusal (step 2a)
- **HIGH**: Duplicate or conflicting requirement, ambiguous security/performance attribute, or stale finalization reported by a passing validation (`tasks_md_stale`, non-empty `would_modify`)
- **HIGH** also: a finalize validation that could not run (fail closed), a WP-prompt blocker (step 2b), an untestable or ambiguous requirement that changes what gets built, a scenario gap on a security or data-loss path, a planning-artifact contradiction or ungrounded behaviour that changes what gets built (pass H)
- **MEDIUM**: Terminology drift, missing non-functional task coverage, underspecified edge case, a finalize-validation warning, a WP-prompt quality improvement, other requirement-quality or scenario findings, a planning-artifact decision, element or scenario no task reflects
- **LOW**: Style/wording improvements, minor redundancy not affecting execution order, EARS wording suggestions, a collapsed lane
- **Product-coherence findings** (pass J) are MEDIUM or LOW, never higher, so they never block the verdict: MEDIUM for intent drift, a lost scenario or an unclear MVP; LOW otherwise; their weight goes into the recommendation (step 6).

### 6. Produce Compact Analysis Report

The report MUST begin with a structured **`analysis-findings/v1`** YAML frontmatter carrier, immediately followed by the human-readable Markdown body. The recorder computes the verdict and issue counts **from this carrier's `findings[]` only** - report prose is presentation and is NEVER parsed for severity. Emit the carrier exactly in this shape:

```yaml
---
schema: analysis-findings/v1
findings:
  - id: C1            # stable finding id (same id used in the body table)
    severity: high    # one of: low | medium | high | critical (closed vocabulary; no other values)
    category: coverage
    summary: "One-line description of the finding."
verdict_hint: blocked   # OPTIONAL author hint; the recorder COMPUTES the verdict - if your hint disagrees, recording FAILS LOUDLY
---
```

Carrier rules (binding - a violation makes `record-analysis` fail on the write path):
- `findings[].severity` MUST be one of `low`, `medium`, `high`, `critical`. Any other value fails schema validation.
- Do not emit `counts`. The recorder tallies `findings[]` per severity itself. A `counts` block is still accepted, but one that disagrees with the tally fails recording.
- The verdict is derived from structure: **any `high` or `critical` finding -> `blocked`; otherwise -> `ready`.** Do not rely on prose wording.
- If you include `verdict_hint`, it MUST match the computed verdict, or recording fails loudly.
- A report with **no** findings emits `findings: []` -> verdict `ready`.
- `summary` is a double-quoted YAML string (escape an inner `\"`); an unquoted `Inferred:` prefix breaks the carrier.

After the closing `---`, draft the Markdown body with the following structure:

## Specification Analysis Report

| ID | Category | Severity | Location(s) | Summary | Recommendation |
|----|----------|----------|-------------|---------|----------------|
| D1 | duplication | HIGH | spec.md:L120-134 | Two similar requirements ... | Merge phrasing; keep clearer version |

One row per finding. Finding ids use one fixed prefix per category, numbered within each prefix by step (2a, 2b, then passes A-G, H, J), then by artifact (spec.md, plan.md, tasks.md, WP prompts in id order, other planning artifacts in inventory order, then occurrence_map.yaml, then decision files by name, meta.json, charter; a finding citing several artifacts sorts by its first cited location), then by line, so a rerun on unchanged artifacts yields the same ids. Table rows are sorted by step (2a, 2b, then passes A-G, H, J), then by id number; when rows overflow the 50-row cap, every HIGH and CRITICAL row stays in the table. Locations use `file:Lnn` (or `file:Lnn-mm`); use a heading only when no stable line exists:

| Prefix | Category | Prefix | Category |
|---|---|---|---|
| D | duplication | V | finalize-validation |
| B | ambiguity | W | wp-readiness |
| U | underspecification | Q | requirement-quality |
| K | charter | S | scenario |
| C | coverage | I | inconsistency |
| X | planning-artifact | M | product-coherence |

Then these sections, always in this order and always present (write "None." when a section has nothing to report):

**Finalize Validation:** the CLI version, the exit code, `result` or `error`, and each `V` finding with the payload keys and ids it came from. If the check refused, state that later gates did not run.

**Per-WP Readiness:**

| WP | Prompt file | In tasks.md | Blockers | Improvements |
|----|-------------|-------------|----------|--------------|

(finding ids in the last two columns; one row per WP named in `tasks.md` or present as a prompt file)

**Requirement Quality:** the `Q` findings, grouped by requirement.

**Scenario Audit:** one table per user story:

| Kind | Scenario | Location | Finding |
|------|----------|----------|---------|

Rows in this order: accepted, rejected, missing edge, surprising accepted, surprising rejected. Finding is the `S` id, or `-` for accepted and rejected rows.

**Intent & Planning-Artifact Consistency:** the inventory entries read (and `meta.json` fields absent), then the `X` findings grouped by artifact. With no planning artifacts beyond spec, plan and tasks, say so.

**Product Coherence:** the creation intent in one line, the `M` findings, then exactly one line: `Recommendation: revise spec | revise plan | revise tasks | proceed` - choose one. Weigh every finding in the report: never `proceed` while the verdict is `blocked`. Owners by category first: `C`, `V` and `W` -> tasks; `M` -> the owner of its first cited location; others by first cited location: spec.md and meta.json -> spec; plan.md and every other planning artifact (research, data-model, contracts, quickstart, checklists, decisions, occurrence_map.yaml) -> plan; tasks.md and WP prompts -> tasks; a charter (`K`) finding -> the owner of the other artifact it cites, else plan. Verdict `blocked`: revise the owner of the first HIGH or CRITICAL finding in table order. Verdict `ready`: proceed, unless an `M` finding of MEDIUM severity exists; then revise the owner of the first such finding in table order (a LOW `M` finding or an ordinary MEDIUM finding of another category does not force a revise).

**Clarification Questions:** one entry per HIGH or CRITICAL ambiguity or requirement-quality finding without a concrete remediation: the finding id, the question, two to four choices with their implications, and the recommended choice.

**Coverage Summary Table:**

| Requirement Key | Has Task? | Task IDs | Notes |
|-----------------|-----------|----------|-------|

**Residual Risk:** what was not machine-checked and why, including a validation that could not run or stopped at its first refusal, and mission-directory entries neither inventoried nor read (for example extra research/ or tools/ files).

**Charter Alignment Issues:**

**Unmapped Tasks:**

**Metrics:**

- Total Requirements
- Total Tasks
- Coverage % (requirements with >=1 task)
- Ambiguity Count
- Duplication Count
- Critical Issues Count
- Finalize Validation (passed | refused | not run)
- WP prompts reviewed, and WP blockers
- Requirement-quality findings
- Scenarios audited
- Inferred findings
- Planning artifacts reviewed
- Planning-artifact findings
- Product-coherence findings
- Coherence recommendation

### 7. Persist Report Artifact

Save the Markdown report body to `kitty-specs/<mission>/analysis-report.md` by running the recorder with a temp report file outside the repository checkout:

```bash
spec-kitty agent mission record-analysis --mission <mission-slug> --input-file <path-to-temp-report.md> --json
```

If your host supports piping reliable multiline stdin, this equivalent form is acceptable:

```bash
spec-kitty agent mission record-analysis --mission <mission-slug> --input-file - --json
```

The report file you pass MUST start with the `analysis-findings/v1` carrier from step 6. The recorder derives the verdict and counts from it; a malformed carrier (unknown severity, a declared `counts` block that does not match the `findings[]` tally, or a disagreeing `verdict_hint`) makes the recorder fail loudly - fix the carrier and re-run.

Treat persistence failure as command failure. The command is not complete until the JSON response reports success and names `analysis-report.md`.

> **Caution - write the report to a path OUTSIDE the repository checkout**
>
> The `analysis-findings/v1` carrier (step 6) is the **input format** for `record-analysis`,
> not the **persisted format**. `record-analysis` wraps the carrier in the outer-wrapper
> format (`artifact_type: spec-kitty.analysis-report`) that the implement gate accepts.
>
> Write the report body to a scratch file **outside the repository checkout** (a temp or
> scratch directory) and pass that path to `record-analysis`. Writing the report body into
> the checkout - including writing `analysis-report.md` directly - both leaves the file in
> carrier format (the implement gate then rejects it with `carrier_format_not_wrapped`) and
> dirties the worktree, so `record-analysis` refuses with `DIRTY_WORKTREE`. Recover by
> writing the body to a path outside the repository checkout and re-running `record-analysis`
> against that path:
> ```bash
> TMP_REPORT="$(mktemp -t analysis-report.XXXXXX.md)"   # outside the repository checkout
> # write the report body (starting with the analysis-findings/v1 carrier) to "$TMP_REPORT"
> spec-kitty agent mission record-analysis --mission <mission-slug> --input-file "$TMP_REPORT" --json
> ```

### 7a. Report Currency (staleness rule)

The recorded `analysis-report.md` is current only while the planning inputs it
was computed against are unchanged. Editing the spec, plan, tasks or the
charter after the report is recorded makes it **stale**. A stale (or missing)
report is refused downstream: `spec-kitty next` re-issues the analyze step, and
`spec-kitty agent action implement` refuses to claim a work package with
`analysis_report_required`. Re-run `/spec-kitty.analyze` and record a fresh
report whenever any of those inputs change. Editing any other planning artifact the report judged (research, data-model, contracts, quickstart, decisions, occurrence_map.yaml, meta.json or a WP prompt) also invalidates its findings even though the staleness check does not track it: re-run /spec-kitty.analyze.

### 8. Provide Next Actions

At end of report, output a concise Next Actions block:

- If CRITICAL issues exist: Recommend resolving before `/implement`
- A finalize-validation refusal or stale finalization: name `/spec-kitty.tasks-finalize` (after fixing the artifacts it names); a validation that could not run: name the CLI upgrade or the `--mission` handle fix; when the first blocking finding is a could-not-run `V`, name that CLI fix first
- A WP-prompt blocker: name the WP and what it lacks
- Repeat the Product Coherence recommendation line and name the artifact to revise, chosen by the owner rule above
- If only LOW/MEDIUM: the verdict is ready; follow the Product Coherence recommendation (proceed, or the artifact it names to revise)
- Provide explicit command suggestions: e.g., "Run /spec-kitty.specify with refinement", "Run /plan to adjust architecture", "Manually edit tasks.md to add coverage for 'performance-metrics'"

### 9. Offer Remediation

Ask the user: "Should all of these findings be addressed before moving on to implementation? I can suggest concrete remediation edits for the findings you want to resolve." (Do NOT apply edits automatically.)

## Operating Principles

### Context Efficiency

- **Minimal high-signal tokens**: Focus on actionable findings, not exhaustive documentation
- **Progressive disclosure**: Load artifacts incrementally; don't dump all content into analysis
- Planning artifacts load headings-first; read a body section only when a check needs it
- **Token-efficient output**: Limit findings table to 50 rows; summarize overflow
- **Deterministic results**: Rerunning without changes should produce consistent IDs and counts

### Analysis Guidelines

- **NEVER modify source/planning files** other than the required `analysis-report.md` persistence step
- **NEVER run a writing `finalize-tasks`**: `--validate-only` is the only permitted form
- **NEVER hallucinate missing sections** (if absent, report them accurately)
- **Label judgement-based findings `Inferred:`**; never claim formal proof
- **Prioritize charter violations** (these are always CRITICAL)
- **Use examples over exhaustive rules** (cite specific instances, not generic patterns)
- **Report zero issues gracefully** (emit success report with coverage statistics)

## Context

(User's invocation context is provided in the User Input section above.)
