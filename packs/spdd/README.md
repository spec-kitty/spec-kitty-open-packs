# SPDD / REASONS

Structured-Prompt-Driven Development (SPDD) treats structured prompts and
REASONS canvases as governed change-intent and decision-boundary artifacts.
This opt-in org pack holds the SPDD paradigm, its directive, the REASONS canvas
fill/review tactics and writing styleguide, and prompt enhancements for the
`software-dev` specify, plan, tasks, implement and review steps. Activating its `spdd`
preset selects the doctrine and all five step enhancements together.

## Adopt

Configure this pack with `built-in` in its dependency closure, then activate
the `spdd` preset. The preset selects the doctrine and all five step
enhancements together; beyond that selection there is no second test for SPDD
artifacts (charter ADR-0066 decision 4). An enhancement is still not in force
on selection alone: under charter rule E6 it is in force only while the
mission type of the step it enhances (`software-dev`) is in force too.
Activation cascades forward only (ADR-0059 A4): charter
`composition-and-activation-rules.md` §Artifacts gives a step no state of its
own, only its mission type's, and W20 cascades mission type → steps, not steps
→ mission type. A selected enhancement does not put `software-dev` in force,
and `software-dev` in force never pulls an unselected enhancement in.

The five base prompts retain only empty `spdd:reasons-block` slots. Without the
enhancements in force, those slots render as nothing. Each enhancement's
`enhances` edge lives in `drg/fragment.yaml`; its non-targeted Markdown fragment
companion lives beside the enhancement under
`missions/software-dev/enhancements/`.
