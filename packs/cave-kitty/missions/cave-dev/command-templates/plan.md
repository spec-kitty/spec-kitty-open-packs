# Plan (caveman)

## Role in the cave-dev lifecycle

This step maps 1:1 to the built-in software-dev `plan` action and inherits its full contract:
Phase 0 resolves every `NEEDS CLARIFICATION` before Phase 1 design; the Charter Check is filled
from the charter (conflicts raised with the user) or marked skipped; Phase 1 artifacts derive
from confirmed answers, not raw input; the step ends after Phase 1 and does not generate tasks.
cave-dev overrides one thing only: the agent's OUTPUT prose, which it compresses to the caveman
voice. The phase discipline and supply-chain evidence (`DIRECTIVE_051`) are unchanged.

## Bound agent-profile

`planner-priti` (built-in). cave-dev ships no personas of its own.

## Directive & styleguide citation

- `CAVE_001` (Caveman Terse Output) — governs this step's output prose; enforcement `required`.
- `cave-sty-001-communication` — the voice `CAVE_001` enforces.

## Canonical artifact & template

- Canonical artifact: `plan.md` (blocking at this step). Phase 1 may add `data-model.md`,
  `contracts/`, `quickstart.md` per the software-dev contract.
- Template: inherited from software-dev's `plan-template.md`; cave-dev ships none.

## Voice at this step

- **Each decision: what, then why — in that order.** One line where one line does. Keep the
  reasoning, drop the narration.
- **Paths, module names, commands are payload — exact.** No paraphrase, no rounding.
- **Keep every negation.** "Do not touch X" is a decision, not filler.
- **Cliff edge → full sentences.** Trade-offs, risks, a Charter Check conflict, or any
  supply-chain / dependency change (`DIRECTIVE_051`) is stated in plain prose with no hedging
  fog — state the risk, its precondition, and the mitigation. Record adversarial-squad
  dispositions in full; never drop a contested finding to save tokens.
- Name what is out of scope plainly.
