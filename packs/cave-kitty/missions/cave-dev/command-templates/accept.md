# Accept (caveman)

## Role in the cave-dev lifecycle

This step maps 1:1 to the built-in software-dev `accept` action and inherits its full contract:
record every acceptance-criterion verdict through `spec-kitty agent mission acceptance-verdict`
(never hand-edit `acceptance-matrix.json`), run the acceptance gate (`spec-kitty accept
--mission <handle>`), resolve every blocker it reports, and surface the operator-run consolidate
instructions once the gate passes. cave-dev overrides one thing only: the agent's OUTPUT prose —
the acceptance decision summary — which it compresses to the caveman voice. The gate and the
evidence discipline are unchanged.

## Bound agent-profile

`reviewer-renata` (built-in). cave-dev ships no personas of its own.

## Directive & styleguide citation

- `CAVE_001` (Caveman Terse Output) — governs this step's output prose; enforcement `required`.
- `cave-sty-001-communication` — the voice `CAVE_001` enforces.

## Canonical artifact & template

- Canonical artifact: none. The verdicts live in `acceptance-matrix.json`, written only through
  the `acceptance-verdict` command; this step authors no document of its own. Do not invent one.
- Template: not applicable.

## Voice at this step

- **Decision first:** accepted or not, and the one reason, in one line.
- **Per-criterion evidence is payload — exact.** The criteria checked, the verification method,
  the commands and their counts, the recomputed `overall_verdict` — character for character.
- **Keep every negation.** An unmet criterion is "not met", stated plainly; never soften it to a
  pass.
- **Cliff edge → full sentences.** A release risk, a failing gate, or a forced acceptance you are
  refusing is stated in plain prose: the risk, the precondition, and what must happen first. Do
  not force the gate past an unresolved blocker.
- Consolidation is the operator's step after the gate passes — surface its instructions, do not
  run it.
