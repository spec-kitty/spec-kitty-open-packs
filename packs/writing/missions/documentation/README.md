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
- `steps/` — The step prompts (`<step>.prompt.md`), which hold each step's rules, and guidelines
  (`<step>.guidelines.md`), which hold only its quality gates
- `templates/divio/` — Divio-type content scaffolds (tutorial, how-to, reference, explanation), each
  mapped to its common-docs section
- `templates/generators/` — Configuration templates for API doc generators (JSDoc, Sphinx)
- `templates/` — The spec, plan and release templates the `discover`, `design` and `publish` steps bind to
