# Implement (caveman)

## Role in the cave-dev lifecycle

This step maps 1:1 to the built-in software-dev `implement` action and inherits its full
contract: work inside the resolved worktree (never the repository root checkout), build the work
package to its acceptance criteria, run the blast-radius tests, and commit before moving to
`for_review` (`feat(WP##): …`). cave-dev overrides one thing only: the agent's OUTPUT prose —
the progress replies and step summaries — which it compresses to the caveman voice. The tests,
the types, the gates, the commit discipline, and the supply-chain check (`DIRECTIVE_051`) are
unchanged from software-dev.

## Bound agent-profile

`implementer-ivan` (built-in). cave-dev ships no personas of its own.

## Directive & styleguide citation

- `CAVE_001` (Caveman Terse Output) — governs this step's output prose; enforcement `required`.
- `cave-sty-001-communication` — the voice `CAVE_001` enforces.

## Canonical artifact & template

- Canonical artifact: none. Deliverables are code and tests committed in the WP worktree, not a
  document this step authors. Do not invent one.
- Template: not applicable — this step produces code.

## Voice at this step

- **Answer first.** Shape: `[thing] [action] [reason]. [next step].`
- **Payload exact.** Code, commands, paths, identifiers, error text, numbers, units, diffs, and
  the commit message — character for character. Never paraphrase a payload to save tokens; a
  rounded test count or a trimmed path fails `CAVE_001`.
- **Keep every negation.** `not`, `never`, `no`, `without`, `except`, `unless` stay.
- **Cliff edge → full sentences.** A destructive command, a force-push, a credential, a
  data-loss risk, or a stuck reviewer is answered in plain prose: state the risk, the
  precondition, and the recovery. Terseness is never worth a silent cliff.
- **The user's words are untouched.** Quoted requirements and prompts are reproduced verbatim,
  never re-voiced.

## Report (terse)

- One line: what you built, what is green, what is next.
- Evidence exact: the commands you ran and their pass/fail counts.
- Any risk or blocker: full sentences, not telegraphic.

Example reply:

> WP03 done. `pytest tests/status/ -q` → 1621 passed. Next: review.
