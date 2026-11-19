# Test Suite Template

This template produces a project's `tasks.md`, read as a suite manifest — a plan of test suites,
each naming the requirement id(s) it targets and a priority/risk ordering — rather than an
undifferentiated work-package list.

The section below is a floor, not a ceiling: it is the minimum this template must declare. An
author may add further sections beyond it, provided each addition carries its own one-line
stated-purpose sentence in the same style as the section below; omitting the section listed here
is non-compliant regardless of what else is added.

## Frontmatter

*Populate `requirement_refs:` via `spec-kitty agent tasks map-requirements`; do not hand-author
this field.*

`requirement_refs:` is populated by `spec-kitty agent tasks map-requirements`; this template does
not redefine or re-implement that command. The bridge check in `qa-carrier-lint` (this pack)
reads this same field.

```yaml
---
requirement_refs: []
---
```

## 1. Suite Manifest

*List one row per test suite: the requirement id(s) it targets, and its priority/risk ordering —
in the literal shape below, not a prose paraphrase of it.*

| Suite | Targets | Priority | Risk |
|---|---|---|---|
| Login smoke suite | FR-001, FR-003 | P1 | High |

This manifest's row shape follows the same three-digit, uppercase `FR-`/`NFR-`/`C-` id discipline
as `test-strategy-template.md`'s requirement register — restated here, not redefined. The live
enforcement mechanism differs, though: a malformed id in `spec.md`/`plan.md`'s own register
silently loses auto-commit, while a malformed id in this manifest instead surfaces through
`spec-kitty agent tasks map-requirements`/`finalize-tasks`'s own orphan-reference reconciliation —
a different check catches it, not no check at all.
