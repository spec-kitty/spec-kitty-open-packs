# QA Templates

| Template | Step | Artifact |
|---|---|---|
| `test-strategy-template.md` | `specify` (bound) | `spec.md` |
| `test-plan-template.md` | `plan` (bound) | `plan.md` |
| `plan-field-declaration.yaml` | `plan` (gate input) | none; tells the plan gate which `plan.md` sections must be filled |
| `test-suite-template.md` | `tasks` (bound) | `tasks.md` |
| `test-case-template.md` | `tasks`, `implement` | a fenced case block in a `tasks/WP*.md` body |
| `exploratory-charter-template.md` | `tasks`, `implement` | an exploratory session sheet in a `tasks/WP*.md` |
| `defect-log-template.md` | `implement` (bound) | `defect-log.md` |
| `test-report-template.md` | `review` (bound) | `test-report.md` |
| `promise-page-template.md` | procedure `qa-description-to-acceptance-ci` | a promise page in the product docs |
| `scenario-template.feature` | procedure `qa-description-to-acceptance-ci` | a `.feature` file citing `@promise:<id>` |

"Bound" means the step's expected output in `qa.mission-type.yaml` names the template through
`template_path`. The other templates are not scaffolded by any step: open them from the pack
root that `spec-kitty charter pack path qa` prints.
