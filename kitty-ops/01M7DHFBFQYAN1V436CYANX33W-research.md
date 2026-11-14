# Research note: one pack-authoring story; house authoring rules out of foundation (#275)

Op `01M7DHFBFQYAN1V436CYANX33W` (profile `curator-carla`). Child 4 of the 2026-11-14 content audit epic #263. Grounded on `origin/main` at `fd7d644`, spec-kitty CLI 4.0.0rc9 (core `d7cedd7`, `make sync-packs` run), charter contracts at the pin `eacbc3c`. Kind: docs/doctrine fix.

## Issues read

- **#275** (P2, parent #263). pack-authoring contradicts itself (`doctrine-daphne` vs `onboard-external-agent-to-pack`, the migrate procedure), and foundation ships rules about how doctrine is written or that encode the team's tracker conventions (`DIRECTIVE_045` voice rules, `DIRECTIVE_018` + `doctrine-version-change`, MoSCoW `priority:Px`, `github-tracker` keyring advice).
- **#263** (epic). Gates for every child: `validate-packs.sh`, the charter service check, `check_vocabulary.py`, `gen_pack_reference.py --check`, digests restamped.
- **#271** (sibling, runs in parallel): owns the internal delivery rules. No file overlap with this slice.
- **#270** (sibling): internal must-have flows made repo-neutral. No file overlap.
- **#229**: maintainer how-to for authoring built-in doctrine (graph regeneration, DAG and scope rules). It owns the built-in-level authoring story this slice deliberately leaves out of the consumer profile.

## Ground truth used to reconcile the contradictions

| Question | What is true | Evidence |
| --- | --- | --- |
| Pack layout | Plural kind directory at the pack root, category subdirectory inside it. The project tier uses singular kind directories under `.kittify/charter-packs/`. | `docs/guides/author-a-charter-pack.md` §1; `spec-kitty charter new tactic x --pack <dir>` writes `<dir>/tactics/x.tactic.yaml`, without `--pack` it writes `.kittify/charter-packs/tactic/x.tactic.yaml` (run in a scratch project). |
| Org pack graph | Hand-authored `drg/fragment.yaml`, the only DRG file an org pack may ship; nothing to regenerate. | author guide §4; `docs/contracts/index.md`. |
| Built-in-level graph | `foundation`, `writing` ship generated per-kind `<kind>.graph.yaml` shards. `charter pack regenerate-graph` targets core's `packs/built-in/`. Not a consumer authoring surface. | `docs/contracts/index.md:35-37,149`; `regenerate-graph --help`; #229. |
| Project tier graph | `charter activate --cascade all` projects edges from a project profile's `directive-`/`tactic-references` (`requires`), `toolguide-`/`styleguide-references` (`suggests`) and `collaboration.operating-procedures` (`requires`). | core `src/charter/offering/drg/project_scan.py:225-249`, `migration/extractor.py:802-837`. Core behaviour; the charter service equivalent was not checked. |
| `applies` | No traversal follows it; no fragment in this repo uses it. | `grep -rn "relation: applies" packs` is empty. |

So the onboard procedure's "wire each new artifact into the references of the profile" was right for the project tier, and the profile's "never add to an inline `references:` list" was right for the legacy block on directives and tactics. They talk about different fields; both texts now say which.

## Placement decisions (per rule)

| Rule | Decision | Why |
| --- | --- | --- |
| `DIRECTIVE_045` "feature branch must not appear unquoted in canonical agent instructions" | Moved to a new `pack-authoring` styleguide `doctrine-instruction-voice`, generalised to "use the glossary's canonical terms; quote a deprecated surface". | It governs how doctrine is written, so it is pack-author doctrine, not a rule for agents doing git work. Generic (any pack author), so a consumer pack, not `internal`. The vocabulary itself is owned by foundation's glossary pack (`feature branch` deprecated, `topic branch` canonical). The directive's version also contradicted that glossary by canonising "PR branch", which the glossary lists as a synonym to avoid. |
| `DIRECTIVE_045` "no agent workflow example uses `git push origin main`" | Moved to the same styleguide ("examples are instructions too"). | It is a guidance-content rule. The operational ban itself stays in the directive's integrity rules. |
| `DIRECTIVE_045` hard-coded `main` | Now "the protected default branch". | #275. |
| `DIRECTIVE_018` + `doctrine-version-change` | **Kept in foundation**, rewritten to be consumer-actionable, with concrete steps (classify, bump `pack_version`, record rationale and migration notes, keep `schema_version`, validate with named commands). | Moving them changes what consumers load: `DIRECTIVE_018` is scoped by `action:*/retrospect` in all three mission types (`foundation/action.graph.yaml:145,322`, `writing/action.graph.yaml:120`) and required by `writing`'s `curator-carla` and `planning-analysis`'s `retrospective-facilitator`. `pack-authoring` depends on `writing`, so `writing` cannot depend on it (cycle). #275 allows "or add concrete steps". No DRG, preset or digest-of-activation change. |
| `moscow-scoping-lens` `priority:P0`..`P3` | Rewritten to "the project's priority scheme (if any)". | #275. |
| `github-tracker` keyring advice and Planning & Tracking citation | Rewritten to "check which token is active" and "check auth where the loop runs". | #275; the old advice breaks CI and cloud agents. |

No directive moved between packs, and no preset changed, so no consumer activation changes. The new styleguide adds one node and three edges to `pack-authoring/drg/fragment.yaml` (profile and onboard procedure `requires` it).

## Similar-surfaces sweep

Commands: `grep -rnE "regenerate-graph|compiled graph|<type>/<pack>|built_in_step_contracts|golden-count|composition ledger|relation: applies|shipped set|applies a procedure" packs docs/guides docs/contracts CONTRIBUTING.md`; `grep -rni "feature branch" packs`; `grep -rn "priority:P\|gho_\|keyring\|Planning & Tracking" packs/foundation`.

| Location | Disposition |
| --- | --- |
| `pack-authoring/agent_profiles/doctrine-daphne.agent.yaml` (all #275 lines) | fixed |
| `pack-authoring/procedures/onboard-external-agent-to-pack.procedure.yaml:39,41,64,91,125-135` (built-in catalog, `apply`, `applies`, references) | fixed (lines 39, 41, 64, 91 not named in #275; same defect) |
| `pack-authoring/procedures/migrate-project-guidance-to-spec-kitty-charter.procedure.yaml` | rewritten |
| `foundation/tactics/pr-agent-worktree-isolation.tactic.yaml:76-78` "PR branch and mission branch are canonical; do not use feature branch" | fixed in scope: the same foundation voice rule as `DIRECTIVE_045`, and it contradicts the glossary |
| `foundation/toolguides/github-tracker.guide.md:191` (keyring in the cautions table) | fixed (same defect) |
| `writing/tactics/common-docs-write.tactic.yaml:53,59`, `common-docs-find.tactic.yaml:27,49` (`regenerate-graph` as a consumer gate) | out of scope: owned by #267 |
| `docs/contracts/index.md:197` ("`regenerate-graph` regenerates the pack manifest and graph") | out of scope: maintainer docs, owned by #229 |
| `foundation/glossary_packs/spec-kitty-core.glossary-pack.yaml` (Spec Kitty vocabulary in foundation) | out of scope: not named by #275 |
| `foundation/directive.graph.yaml` edge `when: changes are ready to reach origin/main` (`DIRECTIVE_045`) | left: generated built-in-level shard, never hand-edited |
| pack-authoring template nodes (`decomposition-table-template`, `onboarded-artifact-set-template`, `source-agent-dossier-template`) have no body in any pack | out of scope, **untracked**: proposed as a follow-up issue |

## Tracked-issues sweep

`gh api search/issues` over open issues for `doctrine-daphne`, `DIRECTIVE_018`, `DIRECTIVE_045`, `github-tracker`, `moscow`, `onboard-external-agent`, `migrate-project-guidance`, `applies`, `feature branch`, `topic branch`, `decomposition-table-template`:

- #229: owns the built-in-level authoring how-to; asks that `doctrine-daphne` link to it once it exists. Not done here (the guide does not exist yet).
- #265: `DIRECTIVE_045` and `doctrine-daphne` named for other defects (internal-only `mission-wrap-up-sequence` cited from `implement.prompt.md`; squad casting). No overlap with these edits.
- #272, #156: `github-tracker` named for other defects. No overlap.
- #12: brownfield bundle names the migrate procedure as a member. Unaffected.
- No issue tracks the missing template bodies.
