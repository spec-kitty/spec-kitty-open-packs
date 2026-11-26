---
affected_files: []
cycle_number: 1
mission_slug: pack-doctor-alignment-01M88RH1
reproduction_command:
reviewed_at: '2026-11-26T09:43:58Z'
reviewer_agent: claude::reviewer-renata
wp_id: WP10
---

# WP10 review cycle 1: changes requested

Reviewer: claude::reviewer-renata, an in-session reviewer subagent (decision 01M8A5ZTVXJ59PNN56PC3WGR3Z). Reviewed c488bdba and a35f2118 on lane-d.

## Required

R1. In `validate_pack_schemas.py` (around :1347-1352), the retired "prompt cannot be read" branch also drops a case that pack-doctor does not judge (C-003).
- Python falls back to `steps/<id>.prompt.md` when a step has no `prompt_path`. The pinned schema has no such default.
- pack-doctor's `artifact_schema_error` fires only when a written `prompt_path` names a missing file.
- So an enhancement slot aimed at a step with no prompt is now refused by nobody:
  - the jar exits 0;
  - the code before WP10 refused it;
  - the new code returns `[]`.
- Fix:
  - `continue` only when `prompt_path` is written and its file is unreadable;
  - with no `prompt_path`, treat the declared slots as empty, so the kept C38 rule fires;
  - add a test for it.

## Nits

N1. Docs left stale by the retirements, and not owned by WP11's prompt:
- `docs/guides/author-a-charter-pack.md:65` says `--derive-manifest`, and that CI fails a stale manifest;
- `docs/contracts/index.md:66-70` mentions a stale-hash gate and `--regenerate-manifest`;
- `packs/README.md:49` says `--derive-manifest`.
- The operator ruled `packs/README.md` into WP11; the same applies to the two docs pages.

N2. The `--cross-pack` help lists all five profile-reference parts as "not judged by ruling". Three of them are only not judged at the pin. Match the distinction `validate-packs.sh` makes.

N3. `unlisted_constituents` is a strict subset of the charter's `manifest_membership`, and is kept with no ruling named. `unlisted_nodes` is not a copy. This is an operator call.

N4. #348's third comment (the `classify` port) is not addressed. Keeping `classify` is right, since the schema pass needs it; add a one-line comment saying why.

N5. Real-jar tests:
- the unreadable-prompt test should assert that its problem is the only one;
- the profile-references pin should add a control proving the profile file is read (`directive-references: 5` is refused with `artifact_schema_error`).

## Verified
- Every retired rule is judged by the jar: 55 real-jar tests pass, with clean and defect packs, exact codes and pointers.
- Keeping the three profile-reference parts is right under C-003. Both the jar probe and the charter source confirm it, and the pinning test is sound.
- All six house-rule comments are present, and each rule's removal fails a test.
- T050: missing `severity` fails, and an unlisted anti-pattern fails; `validate-packs.sh` exits 0.
- T052: no stray callers in code.
- The out-of-map test edits are justified, not weakened, and the long-id test still checks 64/65.
