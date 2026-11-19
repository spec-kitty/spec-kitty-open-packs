# Documentation Content Templates

Output artifact scaffolds for the documentation mission. Includes Divio-type content
templates, generator configuration templates, and the scaffolds the mission's steps
bind to.

| Template | Step | Output |
|----------|------|--------|
| `documentation-spec-template.md` | `discover` | `spec.md` |
| `documentation-plan-template.md` | `design` | `plan.md` |
| `release-template.md` | `publish` | `release.md` |

## Subdirectories

| Directory | Purpose |
|-----------|---------|
| `divio/` | Divio 4-type content templates (tutorial, how-to, reference, explanation), used by `generate` |
| `generators/` | Configuration templates for API documentation generators (JSDoc, Sphinx) |
