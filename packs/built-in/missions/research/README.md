# Research Mission

Mission type for structured research workflows that produce findings, evidence, and
synthesized knowledge artifacts.

## Step order

```
scoping → methodology → gathering → synthesis → output → accept
```

The Spec Kitty runtime guards the gathering → synthesis transition with
`event_count("source_documented", 3)`: at least 3 documented sources before
synthesis can begin. The guard is runtime behaviour, not a field of the mission type.

## Contents

- `research.mission-type.yaml` — The mission type: its steps in run order, the on-demand
  `retrospect` step, and each step's role, expected artifacts and references
- `steps/` — The step prompts (`<step>.prompt.md`) and guidelines (`<step>.guidelines.md`)
- `templates/` — Content scaffolds (spec, plan, tasks, data-model, task-prompt)
- `templates/research/` — Research-specific artifacts (evidence-log.csv, source-register.csv)
