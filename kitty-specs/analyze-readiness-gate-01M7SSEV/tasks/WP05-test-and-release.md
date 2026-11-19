---
work_package_id: WP05
title: Prompt invariant test, versions, derived outputs, changelog
dependencies:
- WP04
requirement_refs:
- NFR-004
- C-001
- C-003
- C-006
planning_base_branch: feat/analyze-finalize-validate-246
merge_target_branch: feat/analyze-finalize-validate-246
branch_strategy: Planning artifacts for this mission were generated on feat/analyze-finalize-validate-246. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/analyze-finalize-validate-246 unless the human explicitly redirects the landing branch.
subtasks:
- T020
- T021
- T022
- T023
- T024
phase: Phase 4 - Release
history:
- at: '2026-11-19T12:07:01Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: implementer-ivan
authoritative_surface: tests/ci/
create_intent:
- tests/ci/test_analyze_readiness_prompts.py
execution_mode: code_change
model: ''
owned_files:
- tests/ci/test_analyze_readiness_prompts.py
- packs/*/pack.yaml
- packs/*.source.yaml
- packs/*/pack-manifest.yaml
- docs/packs/*.md
- docs/changelog/CHANGELOG.md
role: implementer
tags: []
task_type: implement
tracker_refs: []
---

# Work Package Prompt: WP05 - Prompt invariant test, versions, derived outputs, changelog

## Do This First: Load Agent Profile

Use the `/spk-charter-profile-load` skill to load an agent profile for the role below, and behave according to its guidance before parsing the rest of this prompt. If your host cannot run skills, do what the skill does: run `spec-kitty agent profile show <profile-id>` and apply the profile it prints.

- **Role**: `implementer`
- **Profile override**: `implementer-ivan`
- **Agent/tool**: `claude`

If no profile override is set, use the profile the active preset activates for the role; otherwise run `spec-kitty agent profile list` and load a profile whose `role` is it.

---

## IMPORTANT: Review Feedback

- **Has review feedback?**: Check the `review_ref` field in the event log (via `spec-kitty agent tasks status --mission analyze-readiness-gate-01M7SSEV`).
- **You must address all feedback** before your work is complete.
- **Report progress** with `spec-kitty agent tasks add-history WP05 --note "..."`.

---

## Review Feedback

*[If this WP was returned from review, the reviewer feedback reference appears in the status event log.]*

---

## Markdown Formatting

Wrap HTML/XML tags in backticks. Use language identifiers in code blocks.

---

## Objectives & Success Criteria

- `tests/ci/test_analyze_readiness_prompts.py` (unittest style, like the other `tests/ci` tests) pins:
  1. the software-dev analyze prompt instructs `finalize-tasks` only with `--validate-only`: every line naming `finalize-tasks` either carries `--validate-only` or is a prohibition ("never" / "Never" / "NEVER"); and `--refresh-planning-commit` appears only in a prohibition (C-001, FR-005);
  2. the version gate `3.1.0a5` is named in both the software-dev and the cave-kitty analyze prompts (FR-004, FR-017);
  3. both tactic ids are cited by the software-dev analyze prompt, `requirement-quality-ears` by the specify prompt, and both by the cave-kitty analyze prompt;
  4. the software-dev analyze prompt is at most 500 lines (NFR-004);
  5. both tactic files exist and parse as YAML with the expected `id`;
  6. a **positive control on the same fixture** for check 1 (tactic `acceptance-criteria-non-vacuity`): the line classifier flags a synthetic line `spec-kitty agent mission finalize-tasks --mission x --json` as a violation, proving it can see one.
- Lockstep minor bumps per DIRECTIVE_018: foundation 2.1.0 -> 2.2.0; every pack whose `depends_on` pins foundation exactly (`==2.1.0`) moves its pin to `==2.2.0` and takes a minor bump itself, and so on transitively (as #301 did: architecture, planning-analysis, refactoring, testing, built-in; check writing too); cave-kitty 2.2.1 -> 2.3.0 (new prompt content; its `>=2.0,<3` range already admits 2.2.0).
- Manifests derived, digests restamped, pack pages regenerated, changelog `[Unreleased]` entry.
- All gates green locally; CI green on the PR head.

## Context & Constraints

- Spec NFR-001, NFR-004, C-001, C-003, C-006. Plan IC-05. Charter: tests only where they guard real behaviour (DIRECTIVE_041) - this test guards the read-only invariant a prompt edit could silently break.
- Precedent commit for the release footprint: `45aa77c` (#301) - read `git show --stat 45aa77c` and its message. CONTRIBUTING.md: "After editing a pack, run `python3 scripts/ci/pack_digest.py --update` and commit the changed `packs/<name>.source.yaml`".
- How manifests are derived: find the tool before editing by hand (`grep -rn "pack-manifest" scripts/`); C-005-style rule from earlier missions: generated files change only through their generators.
- Changelog file: `docs/changelog/CHANGELOG.md` (the root `CHANGELOG.md` is a symlink). House style: bold lead sentence, issue refs, what changed, "What to do" if consumers must act. Put it under `[Unreleased]` in the right subsection (Added / Changed).
- No model names in commits; signed commits.

## Branch Strategy

- **Strategy**: populated by `finalize-tasks`.
- **Planning base branch**: `feat/analyze-finalize-validate-246`
- **Merge target branch**: `feat/analyze-finalize-validate-246`

```bash
spec-kitty agent action implement WP05 --agent claude --mission analyze-readiness-gate-01M7SSEV
```

## Subtasks & Detailed Guidance

### Subtask T020 - CI test pinning the prompt invariants

- **Steps**:
  1. Model the file on `tests/ci/test_software_dev_ascii.py` (paths from `Path(__file__).resolve().parents[2]`).
  2. Write a small pure function `writing_finalize_lines(text) -> list[str]` and test it on the real prompt (expect `[]`) and on the synthetic positive-control line (expect one hit) in the same test class.
  3. Keep assertions literal and few; no snapshot of prose.
  4. Run `python3 -m pytest -q tests/ci/test_analyze_readiness_prompts.py` and then the whole `tests/ci`.
- **Files**: `tests/ci/test_analyze_readiness_prompts.py` (new, about 80-120 lines).

### Subtask T021 - Lockstep version bumps

- **Steps**:
  1. `grep -rn '"==2.1.0"' packs/*/pack.yaml` and the foundation pack_id `01M75HSYR9S9KPA372PHGT0EX3` to find exact pins; follow the chain until no exact pin is stale.
  2. Bump `pack_version` minor in each affected `pack.yaml`; move the exact pins.
  3. cave-kitty: minor bump only (range pin).

### Subtask T022 - Manifests, digests, pack pages

```bash
# derive manifests with the repository's tool (find it first)
python3 scripts/ci/pack_digest.py --update
python3 scripts/docs/gen_pack_reference.py
python3 scripts/docs/gen_pack_reference.py --check
python3 scripts/ci/built_in_digest.py --check
```

### Subtask T023 - Changelog entry

One entry under `[Unreleased]` (Added): the analyze step's finalize validation (#246), the per-WP readiness review (#237), the requirement-quality, EARS and scenario-audit sections (#247), the two new tactics, cave-kitty parity, and the version bumps. Include "What to do: nothing for consumers; agents running analyze need spec-kitty CLI >= 3.1.0a5 for the validation, otherwise the report blocks with a HIGH finding."

### Subtask T024 - Full gate run and PR body update

```bash
scripts/ci/validate-packs.sh
python3 -m pytest -q tests/ci
python3 scripts/ci/check_vocabulary.py
python3 scripts/ci/pack_digest.py --check
python3 scripts/docs/gen_pack_reference.py --check
```

Record each result in the WP history. The PR body update itself is done by the orchestrating implementer after merge into the PR branch.

## Risks & Mitigations

- A concurrent PR bumps the same packs: rebase and restamp; never hand-edit digests.
- A vacuous test: the positive control is mandatory.

## Review Guidance

- The test fails if the prompt instructs a writing finalize (try it: add the synthetic line to a copy) and passes now.
- Every exact pin on a bumped pack moved; no stale digest; pages regenerated by tool.
- Changelog entry names #246, #237, #247 and the CLI requirement.

## Progress & Status

- **Record a progress note**: `spec-kitty agent tasks add-history WP05 --note "<what you did>"`
- **Change WP status**: `spec-kitty agent tasks move-task WP05 --to <status>`
- **View history and status**: `spec-kitty agent tasks status --mission analyze-readiness-gate-01M7SSEV`
