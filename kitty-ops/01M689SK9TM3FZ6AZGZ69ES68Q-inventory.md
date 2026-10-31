# Stale mission-layout references: inventory (#100)

Op `01M689SK9TM3FZ6AZGZ69ES68Q`, a `spec-kitty dispatch` op. This is a docs-only sweep with no
work packages worth splitting, so a full Mission would be too heavy.

The retired names (charter ADR-0044 §6) are `mission.yaml`, `mission-runtime.yaml`,
`mission_types/<t>.yaml`, `governance-profile.yaml`, `expected-artifacts.yaml`,
`actions/<a>/index.yaml`, `mission-steps/**` and `command-templates/`. They are replaced by
`missions/<type>/<type>.mission-type.yaml`, `steps/<step>.prompt.md` and
`steps/<step>.guidelines.md`.

The inventory was built with
`git grep -nE 'mission\.yaml|mission-runtime|mission-steps|command-templates|governance-profile|expected-artifacts|mission_types/|actions/.*/index\.yaml|step\.yaml|agent-profile:|action ind(ex|ices)|command template'`
over the tree at `86d9284`.

## In scope (edited in this op)

| File | Lines | Divio | Replacement |
|---|---|---|---|
| `packs/built-in/missions/README.md` | 3–5, 20–25, 29–30, 38–40 | reference | Describe the one mission-type file and its `steps/` companions. Fix the glossary link, which pointed at core's `docs/context/orchestration.md` and is broken here. |
| `packs/built-in/missions/software-dev/README.md` | 14, 21–23, 38–47 | reference | "Contents" names the type file and `steps/`. Guards are core runtime behaviour. Drop the "action index" sentence. Roles, not profiles. |
| `packs/built-in/missions/documentation/README.md` | 6, 17–18 | reference | "State Machine" becomes "Step order". "Contents" names the type file and `steps/`. |
| `packs/built-in/missions/plan/README.md` | 6–9, 13–15 | reference | "Runtime DAG (v1.0.0)" becomes "Step order". The planner and reviewer *roles*. "Contents" names the type file and `steps/`. |
| `packs/built-in/missions/research/README.md` | 6, 12–14, 18–19 | reference | "Step order". The guard is the runtime's, not `mission.yaml`'s. "Contents" names the type file and `steps/`. |
| `docs/guides/author-a-charter-pack.md` | 39 | how-to | The `mission_types/` tree line becomes `missions/<type>/<type>.mission-type.yaml` plus `steps/`. |
| `docs/artefacts/index.md` | 36–37 | reference | `missions/<type>/<type>.mission-type.yaml` with `steps/` prompts and guidelines. No `mission_types/` and no action indices. |
| `.agents/skills/spec-kitty.implement/SKILL.md` | 334–339 | how-to | Grep `packs/*/missions/*/steps/`. |
| `packs/qa/PROVENANCE.md` | 31–33 (+47) | explanation | The paragraph on the present state is rewritten for the consolidated layout. The port-time rows (line 24, line 47) are history and are kept, with a dated note. |
| `packs/cave-kitty/PROVENANCE.md` | 32, 39–40 | explanation | "step prompts". The software-dev summary is anchored to runtime version 2.2.0 as history; the `version` field was retired with `mission-runtime.yaml`. |
| `packs/cave-kitty/README.md` | 11 | reference | "command templates" becomes "step prompts". |
| `packs/qa/README.md` | 33 | reference | "command templates" becomes "step prompts". |
| `packs/built-in/tactics/reviewer-implementer-role-separation.tactic.yaml` | 11–20, 61, 70–80 | how-to | **Reworded** (ADR-0032): a step names a role, and a preset activates profiles. The operator approved the rewrite (see below). |
| `packs/built-in/tactics/ownership-map-leeway.tactic.yaml` | 54–55 | how-to | `missions/software-dev/steps/tasks-packages.prompt.md`, `tasks.prompt.md`. |
| `packs/built-in/styleguides/plain-language.styleguide.yaml` | 78 | reference | `actions/discover/index.yaml` becomes `documentation.mission-type.yaml` (the `discover` step's references). |
| `packs/built-in/missions/built_in_step_contracts/research-{scoping,gathering,output}.step-contract.yaml` | 5, 25, 36, 45 | reference | Comment and guidance text only: the guards are the runtime's, not `mission.yaml`'s. |
| `packs/built-in/missions/software-dev/templates/plan-template.md` | 6 | (template payload) | Point at `steps/plan.prompt.md`. |
| `packs/built-in/missions/documentation/templates/documentation-plan-template.md` | 6 | (template payload) | "mission step prompts". |
| `packs/built-in/missions/research/templates/tasks-template.md` | 26 | (template payload) | Point at the mission type's `path_conventions`. |
| `packs/qa/toolguides/qa-carrier-lint.toolguide.yaml`, `qa-carrier-lint.guide.md` | 7, 118 | reference | Name the `blocking` field of a step's expected output in `qa.mission-type.yaml`. |
| `packs/qa/toolguides/qa-result-ingest-guide.guide.md` | 99 | reference | As above. |
| `packs/qa/assets/qa_carrier_lint.py`, `qa_result_ingest.py` | 36, 32 | reference (docstring) | Docstring only. Neither script reads `expected-artifacts.yaml` (checked with grep), so there is no behaviour issue. |
| `packs/built-in.source.yaml` | `tree_digest` | — | Re-seeded, because built-in content changed. |
| `docs/packs/**` | generated | reference | Regenerated with `gen_pack_reference`. |

## Out of scope, reported to @parent

| File | Lines | Why not here |
|---|---|---|
| `packs/built-in/missions/research/steps/{scoping,methodology,gathering,synthesis,output}.prompt.md`, `output.guidelines.md` | 28–72 | These are step prompts and guidelines, the sibling #96–#99 territory. They attribute guards to `mission.yaml`. |
| `packs/built-in/missions/software-dev/steps/implement.prompt.md` | 301–305 | A step prompt (sibling territory). It is the source of the `.agents/skills/spec-kitty.implement/SKILL.md` text fixed here, and core regenerates that copy. |
| `packs/cave-kitty/missions/cave-dev/steps/analyze.prompt.md` | 16 | A step prompt (sibling territory). It names `mission-runtime.yaml`. |
| `packs/qa/missions/qa/steps/review.prompt.md` | 79, 124 | A step prompt (sibling territory). It names `expected-artifacts.yaml`'s `blocking:`. |
| `.kittify/charter/charter.yaml` | 1481 | Generated by core from its installed packs (`source_path` of `TEMPLATE_SET:documentation-default`). Not hand-edited. |
| `docs/changelog/CHANGELOG.md` | 247 | A released history entry. Kept as written. |
| `kitty-specs/**` | — | Records of past Missions. Kept as written. |
| `packs/*/drg/fragment.yaml` `kind: mission_types` | — | A DRG kind token, not a path. Not stale. |

## Findings for the operator

- **software-dev `implement` and `review` name no `role`** in `software-dev.mission-type.yaml`.
  They named no profile before #95 either: `mission-runtime.yaml` had no `agent-profile` on
  those steps. So the tactic's old claim was already wrong. The rewrite no longer asserts any
  wiring, but a step role for these two steps is a mission-type change (sibling territory).
- The retired qa `expected-artifacts.yaml` comment said `blocking: true` *is* enforced by
  `evaluate_guards_strict` through the manifest path. The toolguides say the
  `gather_artifact_presence` gate ignores the flag. These are two different checkers, so the
  texts do not contradict each other, but the retired rationale is now gone from the pack (see
  ADR-0044 §8). Wording is kept; only the file it names changes.

## Operator rulings (2026-10-31, relayed by @parent)

1. The tactic rewrite is approved as proposed. The #96–#99 session adds `role: implementer` and
   `role: reviewer` to software-dev's `implement` and `review` steps. The tactic's notes are
   worded to hold once both PRs land.
2. The step-prompt and guideline fixes listed under "Out of scope" are made by the #96–#99
   session, with `Refs #100`. This op leaves those files alone.
