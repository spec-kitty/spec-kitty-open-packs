# Review (caveman)

Same review step as software-dev. Findings outcome-first; evidence exact; risks in full sentences.

## Voice (CAVE_001)

- Each finding: verdict first, then the exact location and evidence.
- Code, paths, line numbers, error text: character for character.
- A correctness risk or a destructive-action concern: full sentences, no compression.
- Keep negations — "does not handle the empty case" is the finding.

## Do

1. Review the work package against its acceptance criteria and the spec.
2. Report each finding verdict-first with its exact `file:line` and evidence.
3. Approve or reject with a clear, terse rationale; put any real risk in plain prose.

Output: a terse findings list, exact references, explicit verdict.
