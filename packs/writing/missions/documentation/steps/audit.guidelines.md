# Audit Action — Governance Guidelines

The rules for the **audit** step live in its prompt, `steps/audit.prompt.md`. This file keeps only the quality gates the audit step's output must pass.

## Quality Gates

- The coverage matrix is complete: every `(area, Divio type)` cell carries a status.
- Every gap has a stated user impact and a target audience tied back to the discover spec.
- Drift findings cite the conflicting docs path and the contradicting source-of-truth location.
- Low-confidence classifications are flagged for the validate phase rather than silently promoted.
