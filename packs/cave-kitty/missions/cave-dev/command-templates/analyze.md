# Analyze (caveman)

## Role in the cave-dev lifecycle

This step maps 1:1 to the built-in software-dev `analyze` action and inherits its full contract:
a cross-artifact consistency and quality check that runs after `tasks` and before `implement` —
it confirms `spec.md`, `plan.md` and `tasks.md` are mutually coherent (every requirement traces
to a work package, every WP traces back, no orphaned or contradictory decision) and that the
mission is ready to implement. It is an analysis-currency gate, not a document this step authors.
cave-dev overrides one thing only: the agent's OUTPUT prose — the analysis report — which it
compresses to the caveman voice. The consistency rubric and the readiness gate are unchanged from
software-dev.

> **Runtime note.** Under `spec-kitty next`, the analysis-currency gate that software-dev enforces
> ahead of `implement` is keyed to the built-in `software-dev` family and does not fire for a
> `cave-dev`-typed mission (see `mission-runtime.yaml`). Run `/spec-kitty.analyze` explicitly at
> this step; do not rely on the `next` loop to block `implement` on a stale analysis.

## Bound agent-profile

`reviewer-renata` (built-in). cave-dev ships no personas of its own — it re-voices the
software-dev lifecycle, it does not re-staff it.

## Directive & styleguide citation

- `CAVE_001` (Caveman Terse Output) — governs this step's output prose; enforcement `required`.
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
