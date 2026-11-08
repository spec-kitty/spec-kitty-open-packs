# SPDD / REASONS

Structured-Prompt-Driven Development (SPDD) treats structured prompts and
REASONS canvases as governed change-intent and decision-boundary artifacts.
This opt-in org pack holds the SPDD paradigm, its directive, the REASONS canvas
fill/review tactics and writing styleguide, and prompt enhancements for the
`software-dev` specify, plan, tasks, implement and review steps.

## Adopt

Configure this pack with `built-in` in its dependency closure, then activate
the `spdd` preset. The preset selects the doctrine and all five step
enhancements together. Enhancement activation is the only gate for a fragment;
there is no second test for SPDD artifacts (charter ADR-0066 decision 4).

The five base prompts retain only empty `spdd:reasons-block` slots. Without the
enhancements in force, those slots render as nothing. Each enhancement's
`enhances` edge lives in `drg/fragment.yaml`; its non-targeted Markdown fragment
companion lives beside the enhancement under
`missions/software-dev/enhancements/`.
