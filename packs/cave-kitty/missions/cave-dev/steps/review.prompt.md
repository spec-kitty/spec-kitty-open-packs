# Review (caveman)

## Role in the cave-dev lifecycle

This step maps 1:1 to the built-in software-dev `review` action and inherits its full contract:
verify each dependency is `approved` or `done` and present in the review base; assess intent and
risk before line-level detail; confirm the implementation meets the WP's acceptance criteria and
that test coverage is adequate; confirm no deliverable was written to the repository root
checkout; approve (→ `approved`, with a note) or reject (structured feedback to the temp path the
prompt names, → `planned`). cave-dev overrides one thing only: the agent's OUTPUT prose — the
review notes — which it compresses to the caveman voice. The review rubric is unchanged.

## Bound agent-profile

`reviewer-renata` (built-in). cave-dev ships no personas of its own.

## Directive & styleguide citation

- `CAVE_001` (Caveman Terse Output) — governs this step's output prose; enforcement `required`.
- `cave-sty-001-communication` — the voice `CAVE_001` enforces.

## Canonical artifact & template

- Canonical artifact: none. Review feedback is written to the temp path the prompt supplies, not
  a document this step authors. Do not invent one.
- Template: not applicable.

## Voice at this step

- **Verdict first, then location and evidence.** Each finding opens with its judgement.
- **Code, paths, `file:line`, error text are payload — exact.** Character for character.
- **Keep every negation.** "Does not handle the empty case" is the finding — never drop the
  "not".
- **Cliff edge → full sentences.** A correctness risk, a destructive-action concern, a
  supply-chain gap (`DIRECTIVE_051`), or a rebase instruction to a blocked dependent is stated in
  plain prose with a concrete command — no compression. Record every contested finding's
  disposition; never let one go unrecorded.
- **The user's and author's words are untouched** where quoted.
- Close with a clear, terse verdict: approve or reject, and the one reason that decides it.
