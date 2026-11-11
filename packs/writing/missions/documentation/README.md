# Documentation Mission

Mission type for structured documentation creation and gap-filling. Follows the
Divio 4-type documentation system (Tutorial, How-To, Reference, Explanation).

## Step order

```
discover → audit → design → generate → validate → publish → accept
```

Supports three iteration modes: `initial` (from scratch), `gap_filling` (audit existing
docs), and `mission_specific` (targeted documentation).

## Contents

- `documentation.mission-type.yaml` — The mission type: its steps in run order, the on-demand
  `retrospect` step, and each step's role, expected artifacts and references
- `steps/` — The step prompts (`<step>.prompt.md`) and guidelines (`<step>.guidelines.md`)
- `templates/divio/` — Divio-type content scaffolds (tutorial, how-to, reference, explanation)
- `templates/generators/` — Configuration templates for API doc generators (JSDoc, Sphinx)
- `templates/` — Plan, spec, tasks, and release templates
