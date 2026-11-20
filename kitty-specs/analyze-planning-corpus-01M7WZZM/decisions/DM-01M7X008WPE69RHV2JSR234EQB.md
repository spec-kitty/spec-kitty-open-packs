# Decision Moment `01M7X008WPE69RHV2JSR234EQB`

- **Mission:** `analyze-planning-corpus-01M7WZZM`
- **Origin flow:** `specify`
- **Slot key:** `specify.coherence.severity`
- **Input key:** `coherence_severity`
- **Status:** `resolved`
- **Created:** `2026-11-20T17:27:55.542247+00:00`
- **Resolved:** `2026-11-20T17:27:56.805425+00:00`
- **Opened by:** `cli`
- **Other answer:** `false`

## Question

How do product-coherence findings affect severity and the readiness verdict?

## Options

- Advisory: capped at MEDIUM, never block
- Normal severity rules (can block)
- Other

## Final answer

Advisory: capped at MEDIUM, never block; a mandatory Recommendation line (revise spec | revise plan | revise tasks | proceed) is still emitted. Planning-artifact contradictions (#213) keep normal severity. (Operator ruling 2026-11-20.)

## Rationale

_(none)_

## Change log

- `2026-11-20T17:27:55.542247+00:00` - opened
- `2026-11-20T17:27:56.805425+00:00` - resolved (final_answer="Advisory: capped at MEDIUM, never block; a mandatory Recommendation line (revise spec | revise plan | revise tasks | proceed) is still emitted. Planning-artifact contradictions (#213) keep normal severity. (Operator ruling 2026-11-20.)")
