# Analyze (caveman)

## Role in the cave-dev lifecycle

This step maps 1:1 to the built-in software-dev `analyze` action and inherits its full contract:
a cross-artifact consistency and quality check that runs after `tasks` and before `implement` —
it confirms `spec.md`, `plan.md`, `tasks.md` and every WP prompt (`tasks/WP*.md`) are mutually
coherent (every requirement traces to a work package, every WP traces back, no orphaned or
contradictory decision), that the task metadata passes the read-only finalize validation, that
the requirements are good enough to build from, and that the mission is ready to implement. It is an analysis-currency gate, not a document this step authors.
cave-dev overrides one thing only: the agent's OUTPUT prose — the analysis report — which it
compresses to the caveman voice. The consistency rubric and the readiness gate are unchanged from
software-dev.

> **Runtime note.** Under `spec-kitty next`, the analysis-currency gate that software-dev enforces
> ahead of `implement` is keyed to the built-in `software-dev` family and does not fire for a
> `cave-dev`-typed mission (the gate is core runtime behavior; no pack file declares it). Run
> `/spec-kitty.analyze` explicitly at this step; do not rely on the `next` loop to block
> `implement` on a stale analysis.

## Readiness checks (inherited, named here)

The software-dev `analyze` step owns the full procedure, the severities, the finding ids and the
report sections; follow it. In short, so nothing is skipped under cave-dev:

- **Finalize validation, read-only.** Run `spec-kitty --version` first. Below 3.1.0a5, or no CLI:
  do not run the check; record a HIGH `finalize-validation` finding naming `spec-kitty CLI >= 3.1.0a5`.
  Otherwise run `spec-kitty agent mission finalize-tasks --validate-only --mission <slug> --json`
  and nothing else: never the plain form, never `--refresh-planning-commit`, never `--allow-orphaned`.
  A refusal is CRITICAL. Could not run is HIGH (fail closed).
- **Every WP prompt.** Review each `tasks/WP*.md` with `foundation` tactic
  `wp-prompt-readiness-review` (`spec-kitty charter context --include tactic:wp-prompt-readiness-review`);
  Per-WP Readiness row per WP, blockers apart from improvements.
- **Requirement quality.** Judge requirements and audit scenarios with `foundation` tactic
  `requirement-quality-ears` (`spec-kitty charter context --include tactic:requirement-quality-ears`):
  five properties, EARS as a lens, scenario audit per user story with locations, clarification
  questions with concrete choices.
- **Judgement findings start with `Inferred:`.** No proof claimed.

## Requested role

This step asks for the `reviewer` role. cave-kitty ships no preset and no personas of its
own, so it activates no profile for it; a reviewer profile such as `reviewer-renata` (from the `foundation` pack) fills it
when the operator activates one.

## Directive & styleguide citation

- `CAVE_001` (Caveman Terse Output) — governs this step's output prose.
- `cave-sty-001-communication` — the voice `CAVE_001` enforces.

## Canonical artifact & template

- Canonical artifact: none required. The analysis is a consistency verdict over the existing
  `spec.md` / `plan.md` / `tasks.md`; this step authors no cave-dev-specific artifact. Do not
  invent one.
- Template: inherited from software-dev; cave-dev ships none. The voice applies to prose, not to
  document structure.

## Voice at this step

- **Verdict first, then the inconsistency.** One line per finding: what is inconsistent, where,
  before any narration.
- **Artifact references are payload — exact.** Requirement IDs (`FR-###`, `NFR-###`, `C-###`,
  `SC-###`), WP ids, `file:line`, and quoted spec/plan text are reproduced character for
  character. Terseness never touches a payload.
- **Keep every negation.** "Requirement FR-012 is not covered by any WP" is the finding — never
  drop the "not".
- **Cliff edge → full sentences.** A coverage gap that blocks implementation, a contradiction
  between plan and tasks, or any readiness blocker is stated in plain prose: what is wrong, what
  it blocks, and what must change before `implement` can start.
- Name every unresolved `[NEEDS CLARIFICATION]` and every orphaned requirement plainly; do not
  smooth them over to save tokens.
- **A refusal, a could-not-run, a WP blocker → full sentences.** Each is a cliff edge: say what
  failed, what it blocks, and what fixes it. Commands, finding ids, `error_code` values, CLI
  versions and severities are payload — exact.
