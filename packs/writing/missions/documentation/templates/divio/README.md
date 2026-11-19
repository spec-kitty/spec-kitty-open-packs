# Divio Content Templates

Content scaffolds following the Divio 4-type documentation system. Each template
provides the canonical structure for one documentation type, and the section of the
common-docs layout its pages go in.

| Template | Type | Orientation | Section |
|----------|------|-------------|---------|
| `tutorial-template.md` | Tutorial | Learning-oriented, teaches beginners step-by-step | `docs/guides/` |
| `howto-template.md` | How-To | Task-oriented, solves specific problems | `docs/guides/` |
| `reference-template.md` | Reference | Information-oriented, describes APIs | `docs/api/` |
| `explanation-template.md` | Explanation | Understanding-oriented, explains architecture and rationale | `docs/architecture/` |

Each template opens with the common-docs frontmatter: `title`, `description`, `type`,
`doc_status`, `updated`, `audience` and `related`. Its `{...}` slots are filled by the
documentation mission's `generate` step. A slot it cannot fill yet becomes
`[TODO: <what is missing>]`.
