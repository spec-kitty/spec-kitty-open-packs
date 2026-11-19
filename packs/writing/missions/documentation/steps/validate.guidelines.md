# Validate Action — Governance Guidelines

The rules for the **validate** step live in its prompt, `steps/validate.prompt.md`. This file keeps only the quality gates the validate step's output must pass.

## Quality Gates

- `audit-report.md` exists, is complete, and carries an explicit verdict.
- The structural lint exits `0` with `--extended`, and every page passes the Divio type, freshness and placeholder gates.
- Plain-language, accessibility and source-of-truth findings are recorded per page.
- Every claimed gate has cited evidence (page path, command output, screenshot, or diff).
- Risks marked `block-publish` are addressed before the verdict flips to `ready-to-publish`.
- The report is reproducible: rerunning the gates produces the same outcome on the same content.
