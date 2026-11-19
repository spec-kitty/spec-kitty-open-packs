# Research: Analyze readiness gate

## R1 - What `finalize-tasks --validate-only` really checks

- **Decision**: the analyze prompt names the refusal keys and success fields of spec-kitty CLI 4.0.0rc9 and reports anything else verbatim.
- **Evidence**: CLI source (`specify_cli/cli/commands/agent/mission_finalize*.py`, core `01e577d`) and a scratch-Mission run on 2026-11-19:

| Case | Exit | Payload |
|---|---|---|
| unmapped FR | 1 | `error: "Requirement mapping validation failed"`, `unmapped_functional_requirements: ["FR-002"]`; the other mapping keys present but empty |
| two parallel WPs own one file | 1 | `ownership_errors: ["Overlap: ..."]` |
| same overlap, ordered by a dependency | 0 | passes |
| dependency cycle | 1 | `cycles: [["WP02","WP01","WP02"]]` |
| passing, never finalized | 0 | `would_modify` lists both WPs; `topology_decision.preview: true` |
| unknown mission | 1 | `error_code: MISSION_CONTEXT_UNRESOLVED` |

  The worktree stayed clean after every run. The gates are fail-fast: one refusal per run.
- **Alternatives**: restate only the issue's five classes (rejected: misses tasks.md pairing, dependency disagreement, literal paths, stale canceled deps, risk policy).

## R2 - Minimum CLI version

- **Decision**: require spec-kitty CLI >= 3.1.0a5; below it, do not run the check.
- **Evidence**: core CHANGELOG: `--validate-only` flag added in 3.0.0; "validate-only is genuinely non-mutating" in 3.1.0a5.
- **Alternatives**: require 4.0.0rc9 (rejected: blocks hosts whose check is read-only and only lacks newer keys, which the prompt reports verbatim).

## R3 - Where the checklists live

- **Decision**: two foundation tactics, cited from the prompts (operator ruling, Decision Moment `01M7SV0083VK137H0ZRRHHAC58`).
- **Rationale**: one source for specify and analyze; analyze stays under 500 lines; cave-kitty cites the same doctrine.
- **Alternatives**: inline in the prompts (rejected: duplicated quality bar, near the line cap).

## R4 - WP template deferral

- **Decision**: the WP review compares each WP prompt to `task-prompt-template.md` as the command's template resolver returns it, and names no keys or sections.
- **Rationale**: #230 reconciles the template and the tasks prompts; a list here would drift (#230's own suggested fix is to defer).

## R5 - EARS

- **Decision**: the tactic names the five EARS patterns (ubiquitous, event-driven `When`, state-driven `While`, unwanted-behaviour `If ... then`, optional-feature `Where`) and treats EARS as a check of observable, testable wording, not a mandatory sentence template; a requirement in another clear, testable form is not a finding.
- **Rationale**: #247 asks for EARS-pattern and observable-behaviour checks; forcing the template would turn style into blockers.

## R6 - Overlap between step 2a and the per-WP review

- **Decision**: when step 2a reports `missing_wp_sections` / `extra_wp_sections`, the per-WP section cites that finding id instead of raising a second finding.
- **Rationale**: one defect, one finding; keeps counts deterministic.
