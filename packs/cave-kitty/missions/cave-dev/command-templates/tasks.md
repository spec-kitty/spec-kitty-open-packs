# Tasks (caveman)

## Role in the cave-dev lifecycle

This step maps 1:1 to the built-in software-dev `tasks` action and inherits its full contract:
decompose into work packages that trace to a requirement or a locked plan decision
(`DIRECTIVE_010`), each WP declaring a coherent owned-files set without editing a sibling's
surfaces (`DIRECTIVE_024`) and an explicit acyclic `dependencies:` list; hand off to
`spec-kitty agent mission finalize-tasks`, then run `/spec-kitty.analyze` (the readiness gate
`implement` enforces). cave-dev overrides one thing only: the agent's OUTPUT prose, which it
compresses to the caveman voice. The decomposition rules and the analyze gate are unchanged.

## Bound agent-profile

`planner-priti` (built-in). cave-dev ships no personas of its own.

## Directive & styleguide citation

- `CAVE_001` (Caveman Terse Output) — governs this step's output prose; enforcement `required`.
- `cave-sty-001-communication` — the voice `CAVE_001` enforces.

## Canonical artifact & template

- Canonical artifact: `tasks.md` plus the per-WP files `tasks/WP##*.md` (blocking at this step).
- Template: inherited from software-dev's `tasks-template.md` / `task-prompt-template.md`;
  cave-dev ships none.

## Voice at this step

- **Each work package: one line of intent, then its exact deps and acceptance.** Compress the
  intent, never the wiring.
- **Dependencies, repo-root-relative file paths, requirement IDs, owned-files sets are payload —
  exact.** They must match the form the ownership validator accepts; a paraphrased path fails.
- **Keep every negation** in scope notes — "this WP does not touch the reducer" is a boundary,
  not filler.
- **Cliff edge → full sentences.** A dependency cycle, an oversized WP, or an unresolved
  spec/plan reference is an ERROR stated plainly, not telegraphed — say what is wrong and what it
  blocks.
- This step stops at `planned`; it starts no implementation and moves no WP status.
