# Plan Mission

Mission type for standalone planning workflows that produce structured plans without
necessarily proceeding to implementation.

## Step order

4 sequential steps: specify → research → plan → review.

## Contents

- `plan.mission-type.yaml` — The mission type: its steps in run order with their prompts and
  expected output artifacts, and the guidance it references
- `steps/` — The step prompts for specify, research, plan and review (`<step>.prompt.md`)
- `templates/` — Skeletons for the spec and the plan
