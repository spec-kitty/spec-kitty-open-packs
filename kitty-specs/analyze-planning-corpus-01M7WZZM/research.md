# Research: Analyze: full planning corpus and product coherence

Grounding was verified on `t3/analyze-planning-corpus-coherence` at `3bedeef` (= `origin/main`).

## R-01 — What the CLI inventory gives the analyze step

- **Decision**: Read the planning corpus only from `spec-kitty agent mission check-prerequisites --json --include-tasks` (`artifact_files`, `artifact_dirs`) plus `<mission_dir>/meta.json` and the canonical fixed path `<mission_dir>/occurrence_map.yaml` (not inventoried; core's `mission.yaml` lists only data-model, contracts, quickstart, research and checklists). Treat every entry whose path the step has not already loaded (spec, plan, tasks, WP prompts) as a planning input, except `feature_dir`, which is the mission directory itself. Never hard-code the key list. `available_docs` adds nothing (file names only) and is not relied on.
- **Rationale**: core's `validate_feature_structure` (`src/specify_cli/core/worktree.py:110-245`) fills `artifact_files` with `spec_file`, `plan_file`, `tasks_file` and every writer-produced `*_file` present on disk, and `artifact_dirs` with structural `*_dir` keys plus `feature_dir` (the mission dir, legacy alias). `_inventory_writer_artifacts` derives the rest from writer metadata (`research.md`, `data-model.md`, `quickstart.md`, `contracts/`, …), so new artifact kinds appear without a prompt change. `meta.json` is **not** in the payload; the prompt must read it directly. #213's comment proposal asked for exactly this: "no second discovery mechanism".
- **Alternatives considered**: a hard-coded artifact list in the prompt (rots as the writer gains artifacts; rejected); a glob over the mission dir (second discovery mechanism, picks up status/event files; rejected).

## R-02 — Where the check detail lives

- **Decision**: Two new tactics under `packs/foundation/tactics/analysis/`: `planning-corpus-consistency` and `product-coherence-review`, shaped like `requirement-quality-ears` (purpose, steps with examples, failure_modes, notes saying the citing step owns severities, ids and layout). The prompt carries one short pass per tactic, the severity lines, the report sections and the prefix rows.
- **Rationale**: the analyze prompt is 380 lines against a 500-line CI cap (`tests/ci/test_analyze_readiness_prompts.py:27`). The #247 delivery set the pattern: detail in a tactic, a fetch line in the prompt (`spec-kitty charter context --include tactic:<id>`), wiring in `tactic.graph.yaml`, `action.graph.yaml` (scope edge from `action:software-dev/analyze`), `pack-manifest.yaml` (derived), and the cave-kitty `drg/fragment.yaml` scope edge from `action:cave-dev/analyze`.
- **Alternatives considered**: one combined tactic (mixes a normal-severity traceability check with an advisory judgement; rejected); inline detail in the prompt (breaks the line budget).

## R-03 — Splitting "intent" between #213 and #214

- **Decision**: *Ungrounded behaviour* (a task or WP builds something no requirement, plan decision, planning artifact or creation intent asks for) is a #213 planning-artifact finding (prefix `X`) at normal severity. "Ungrounded" means no trace at all; a WP mapped to no requirement is already a `V`/`W`/`C` defect and is cited, not re-raised. *Intent drift* (the plan as a whole no longer serves the creation intent) and *overbuild* are #214 product-coherence judgements (prefix `M`), capped at MEDIUM. One defect, one finding: the earliest step that detects a defect owns it (2a, 2b, A-G, H, J) and later steps cite its id; when a WP is both ungrounded and overbuild, it is raised once as `X` and the Product Coherence section cites that id. Behaviour that traces to a source but exceeds the intent's need is overbuild (`M`).
- **Rationale**: #213 AC "flags tasks/WPs that implement behavior not grounded in user intent" is a traceability check; #214 "user-intent drift" is a product judgement. The operator ruling keeps the former's severity and caps the latter.

## R-04 — Severity and the verdict

- **Decision**: Planning-artifact findings follow the normal heuristic: a contradiction that changes what gets built (contract vs data model, a research decision the tasks reverse, ungrounded behaviour) is HIGH; an unreflected decision, entity, operation or quickstart scenario with no task is MEDIUM unless it blocks baseline functionality (then it is a coverage-class HIGH); wording drift is LOW. Product-coherence findings are MEDIUM or LOW, never higher, and therefore never move the carrier's computed verdict. The carrier verdict rule is unchanged.
- **#214 "readiness verdict accounts for product coherence"**: met by the mandatory `Recommendation:` line printed in the Product Coherence section and repeated in Next Actions beside the verdict. The recommendation weighs all findings; it is never `proceed` while the verdict is `blocked`, and it may be `revise spec`, `revise plan` or `revise tasks` while the verdict is `ready`.
- **Vocabulary guard**: pack prose may not say a rule "is advisory" or "remains advisory" (`scripts/ci/check_vocabulary.py`, SELF_BINDING). The prompt says "capped at MEDIUM; never blocks the verdict" instead.

## R-05 — MVP and the neighbours

- **Decision**: The coherence pass reads the MVP slice from `tasks.md` (the tasks template's "MVP Scope" note, `templates/tasks-template.md:174`, and the `MVP` marker on a WP heading) and reports "MVP unclear" as a finding when neither exists; it does not define what an MVP is. The tasks/tasks-finalize prompts' MVP recommendation is chat output, never persisted, so analyze cannot read it. #147 (vertical-skeleton-first tactic) and #215 (product-to-execution patterns) stay untouched: the tactic's vertical-slice lens names the observation, not a doctrine.

## R-06 — Prompt content rules this repo already enforces

- Shipped prompts cite no core issue numbers (`c55ea1d`); the new prompt and tactics cite no issue numbers at all.
- `writing_finalize_lines` must stay empty for both analyze prompts.
- Pack content changes need derived manifests, restamped digests (`scripts/ci/pack_digest.py --update <pack>`; the built-in digest constant in `tests/ci/test_pack_digest.py`), regenerated `docs/packs/` pages and a minor version bump of the foundation lockstep and its exact pins (precedent `6dce39c`).

## R-07 — #247 folds (Step-0 squad)

Lens A (acceptance-criteria fidelity): all #247 criteria met on main. Lens B (executability): "change helpful": (1) say which scenario-audit rows become `S` findings, add a Finding column and fix the kind order; (2) say where `Inferred:` goes and which steps it covers; (3) pin the #247 report content in tests. Nits folded too: the duplicated "untestable" severity rule (`analyze.prompt.md:207-208`), the `file:Lnn` location form, the lowercase category in the example row (`:241`). Per the operator ruling these fold into this mission and the PR closes #247.

## R-08 — Finding prefixes and pass labels

- **Decision**: `X` = `planning-artifact` (cross-artifact), `M` = `product-coherence` (MVP/market fit). Passes H and J; I is skipped because `I` is already a prefix.
- **Rationale**: free letters are A E F G H J L M N O P R T X Y Z. A-G label passes; O/L look like 0/1; T clashes with task ids; P with `Priority: P1` and `[P]`; F/N with `FR-`/`NFR-`; H with HIGH; R with Recommendation (post-spec feasibility lens).

## R-09 — Post-spec squad dispositions

Fidelity lens (reviewer-renata): 2 blockers, 5 should-fix, 3 nits — all folded into spec (prefixes named, `Inferred:` scope stated, five quality properties pinned, #247 nits as FR-018, decisions + deferred markers, unknown-artifact edge case, recommendation-vs-verdict rule, section placement, Finding column values, issue-matrix location). Feasibility lens (planner-priti): prefixes `X`/`M`, earliest-step ownership rule, `occurrence_map.yaml` fixed path, no double loading, MVP from `tasks.md` only, `source_description` rarely present, cave-dev inventory statement, vocabulary-guard phrasing, versioning decided explicitly (R-06, plan Technical Context). None rejected.

## R-10 — Post-tasks squad dispositions

Coverage lens (reviewer-renata): quickstart/plan stale pass and prefix names (fixed); WP prompt directory counts as loaded; `meta.json` missing never aborts; Next Actions defers to the recommendation line; SC-003 trace owned by WP05 (add-history → PR body and matrix); WP04 tests tagged red-first vs ratchet (FR-016 no-op note updated); cave size guard ≤ 90; pass J also reads an MVP-marked WP heading; C-006 label. Doctrine lens (doctrine-daphne): `decisions/DM-*.md` read from its fixed path (C-002 updated); split-brain edge dropped; graph ordering positions given; NON-REMEDIATING paragraph extended; "passes A-H and J"; whole recommendation literal pinned; cave-kitty foundation range tightened to `>=3.2,<4`; digests restamped after commit. Versioning: the 2026-11-18 "share one bump" ruling covered the #300/#302/#303 batch; the latest analyze precedent `6dce39c` bumped while unreleased, so this mission minor-bumps and flags in the PR that the bump can fold into 3.1.0 on request. `tasks_dir` is not excluded by name (operator steer: name only `feature_dir`); the "files already loaded" rule covers it.
