# Research: commands and tools agents run that are wrong (#264)

Grounding note for #264 (P1, size S, child of the content-audit epic #263). Branch
`fix/264-wrong-agent-commands` off `main` `fd7d644`. Delivery shape: an Op (bugfix, content), not a Mission.

## Reference points

- Spec Kitty CLI: `/opt/spec-kitty` at `d7cedd7` (equal to `origin/main`), `spec-kitty-cli 4.0.0rc9`.
  `make sync-packs` there ran clean.
- mutmut: 3.8.1 installed in a scratch venv and run against a toy `src/mypackage` project. The 3.3.0, 3.4.0 and
  3.5.0 wheels were inspected for config keys.
- Charter contract: spec-kitty-charter at the pin `eacbc3c` (from `charter.lock.yaml`), cloned locally and passed
  through `CHARTER_CONTRACT_DIR` (the raw fetch returns 404 in this environment).
- PowerShell: no `pwsh` in the container. The 5.1 and 7 claims below come from PowerShell's documented behaviour
  (pipeline chain operators arrived in 7.0) and were not run here.

## Instances from #264 and how each was checked

| Instance | Check | Fix |
| --- | --- | --- |
| PowerShell `-Json` advice (`:162-165`) | `spec-kitty … --help`: every flag is `--`-spelled | The error is scoped to cmdlets; spec-kitty flags keep `--` |
| `.worktrees\001-mission-name`, branch `001-…` (`:79-82`) | Core `lanes/branch_naming.py`: lane branches are `kitty/mission-…`; `NNN-` is display-only | "the checkout `spec-kitty agent action implement` prints"; no guessed branch name |
| `tasks\planned` (`:125`) | `tasks/` is flat (#230 item 1) | Neutral `notes` directory |
| `SPEC_KITTY_TEMPLATE_ROOT` (`:86-104`) | Core dev/test override, not consumer guidance | Neutral `$env:MY_VARIABLE` example |
| `;` instead of `&&`, backslash-only (`:61`, `:131-132`, `:166-172`) | `;` never stops on failure; `&&` exists from pwsh 7.0; both separators work | New 5.1 vs 7 section; `&&` on 7, `$LASTEXITCODE` on 5.1 |
| `pip show spec-kitty-cli` (`:174-177`) | `spec-kitty verify-setup --diagnostics` exits 0 on rc9; `doctor` is a command group | `Get-Command spec-kitty`, then `verify-setup --diagnostics` |
| `mutmut run --paths-to-mutate=…` (`python-review-checks:135`) | mutmut 3.8.1: `Error: No such option '--paths-to-mutate'`; `uv run mutmut run "mypackage.core*"` runs | mutmut 3 form, neutral `mypackage` |
| cave-kitty `--type` (`README:25,49-64,79,137`) | `spec-kitty agent mission create --help`: only `--mission-type`, slug is positional | `--mission-type`; `create <slug> --mission-type cave-dev` |
| `scripts.docs.description_length_check` (`landing-contributor-prs:52`) | Core lists it in `tests/docs/test_legacy_docsite_retired.py`; `docs/development/how-to/pr-landing.md:996` names `tests/docs/test_docs_seo.py` (band 50-180) | `uv run pytest tests/docs/test_docs_seo.py` |
| `/investigate` skill (`five-paradigm-parallel-debugging:19-20`) | No pack, `.agents/` or `.claude/` skill named `investigate` | `failing-test-triage` / `durable-fix-investigation` (both in `foundation`, same pack) |
| model-to-task_type catalog (`model-task-routing:25-35,57-59`) | The catalog is core source (`src/charter/offering/model_task_routing/`); no command or `charter context --include` selector prints it. `spec-kitty dispatch` (and `--dry-run`) prints its pick as a "Model Routing Recommendation (advisory)" panel (`dispatch.py:253`); found by the pre-PR squad | Step names the `dispatch` panel, with a fallback when none is shown; purpose and failure mode reworded |

## Similar-surfaces sweep

Repo-wide grep (all of the tree, `.agents/` and `.claude/` included) for `paths-to-mutate`, `rerun-all`,
`description_length_check`, `/investigate`, `mission create --type`, `SPEC_KITTY_TEMPLATE_ROOT`, `tasks\planned`,
the catalog wording, and every `--type ` in `packs/`.

| Find | Disposition |
| --- | --- |
| `python-mutation-tools.guide.md`: `--rerun-all=false` and `runner = …` (no mutmut 3.x has either; 3.8.1 refuses the flag and ignores the key), `paths_to_mutate` (deprecated since 3.4 for `source_paths`), `show all` (3.8.1: `Could not find mutant all`), `<id>` where 3.x takes a mutant name | **In scope.** #264 names this guide as the reference form for `python-review-checks`, so it must itself be right. Same tool, same pack, same failure class |
| `testing::mutation-aware-test-design` `tooling:` line (`mutmut>=3.5.0 — run: uv run mutmut run`) | Correct; no change. Its scope is #276 |
| `python-review-checks:135` path `src/specify_cli/status/` | Replaced by the neutral `mypackage` as a side effect of the mutmut 3 form (the flag that carried the path is gone). `:71` stays for #259 |
| `.kittify/memory/templates/POWERSHELL_SYNTAX.md`: an older copy of the guide with every PowerShell instance | Out of scope (repo state, not a pack). Filed #278 |
| `spec-kitty implement` (CLI help: "Internal") named in ~10 agent-facing pack lines, cave-kitty `:24` included | Out of scope: the command works, nothing breaks. Filed #277 as a decision |
| `rg --type py` (`efficient-local-tooling:31`), `--type Bug` (`issue-triage-pass`) | Valid flags of other tools; no change |
| Siblings #266, #269, #272, #276 | Each defers its overlapping item here (#272: the retired script; #276: the routing catalog). Nothing else of theirs is touched |
| PowerShell guide example | Uses `move-task` rather than a plain `git commit -m`, so it does not add an unsigned-commit example (#276, DIRECTIVE_029) |

## Gates

`validate-packs.sh`, `check-pack-digests.sh`, `check_vocabulary.py`, `gen_pack_reference.py --check` and the
unit-test suites run locally (results in the PR). The charter service check needs the service jar; the jar build
cannot resolve `kotlin-stdlib 2.4.10` through this environment's network, so that job is left to CI.

## Pre-PR adversarial squad

Three read-only delegates ran with their profiles loaded: reviewer-renata (correctness), curator-carla (doctrine
curation and conventions) and scribe-sally (agent-facing clarity). Each finding was checked against the source before
it was folded.

| Finding | Disposition |
| --- | --- |
| MAJOR (renata): "no command shows a routing recommendation" is false; `spec-kitty dispatch` prints one | Reproduced with `dispatch … --dry-run`. Folded: the tactic names the panel; the changelog and this note are corrected |
| MAJOR (sally): the routing tactic's purpose still promised a recommendation "alongside the task" | Folded |
| MINOR (carla): the tactic states a CLI absence that rots | Superseded by the MAJOR fold; the absence claim is gone |
| MINOR (renata): `mutmut show all` fails, `results` is mis-described, `<id>` should be a mutant name | Reproduced on 3.8.1. Folded, including the "shows only survivors" gotcha (`--all true`) |
| MINOR (sally): 5.1 `$LASTEXITCODE` cell needs the cmdlet case; review-checks wording; tactic's bare "stop" and procedure ids; changelog wording | Folded |
| NIT (sally): `$PID` tip, `tasks status` without `--mission`, undefined "lane branch", where to record an override | Folded. `--shell-pid` is named on `move-task` only: `agent action implement` has no such flag on rc9 |
| NIT (carla): changelog "error or wrong thing" misses dead ends | Folded |
| MINOR (carla): add a `Co-Authored-By` trailer | Rejected: the operator brief for this delivery says no `Co-Authored-By` trailer |
| NIT (carla): no `kitty-ops/<ULID>.jsonl` Op record | Not done: this delivery was not opened through `spec-kitty dispatch`, so there is no Op to record |
| NIT (renata): `also_copy` repeats the mutated directory | Pre-existing and harmless (it ran on 3.8.1); left alone |
