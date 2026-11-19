# Generate Action — Governance Guidelines

The rules for the **generate** step live in its prompt, `steps/generate.prompt.md`. This file keeps only the quality gates the generate step's output must pass.

## Quality Gates

- Every required Divio cell from `plan.md` is filled or explicitly deferred with a recorded reason.
- Every page sits in the common-docs section its Divio type maps to and carries the common-docs frontmatter, with `type:` set.
- No `{...}` template slot remains in any page, and no `[TODO: ...]` marker remains in pages flagged for publication.
- The structural lint passes with `--extended`.
- Generator output is reproducible: the recorded command and configuration produce the same result in a clean environment.
- Reference content is aligned with the source of truth at the moment of generation.
