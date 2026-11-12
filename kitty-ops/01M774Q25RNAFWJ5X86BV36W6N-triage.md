# Issue triage pass, 2026-11-12

Op `01M774Q25RNAFWJ5X86BV36W6N` (profile `planner-priti`). Every open issue was read in full, with its comments. Code-state checks used `origin/main` at `a6cfeab`; no PR merged during the pass.

**Open issues:** 56 before, 41 after (16 closed, 1 epic opened).

## Closed

| Issue | Reason | Evidence |
| --- | --- | --- |
| #1, #3, #4, #7, #8, #10, #13, #15, #16 | completed: delivered under the #198 pack names | foundation, testing, python, architecture, writing, refactoring, planning-analysis, pack-authoring, internal |
| #2, #9, #11 | completed: folded into existing packs | DDD into architecture, foundation and planning-analysis; git delivery and adversarial review into foundation |
| #18 | completed | `glossary_packs/*.glossary-pack.yaml` is a first-class kind |
| #144 | completed | directive 051 is ecosystem-neutral, with per-ecosystem supply-chain toolguides; `dependency-hygiene` delegates instead of restating the controls |
| #148 | completed | PR #101 and PR #95: no `## State Machine` sections and no `expected-artifacts.yaml` remain |
| #163 | completed | pack half filed as #112 and fixed by PR #166; the templates and step prompts are ASCII |

## Re-scoped, narrowed and re-parented

- **#6:** future `frontend` bundle (operator ruling). Parent #190, P3.
- **#12:** future `brownfield` bundle (operator ruling). Parent #190, P3.
- **#204:** narrowed to the java-conventions rules. Its `applies_to_languages` item duplicated #202, which keeps it (Bug, P2, parent #190).
- **#201:** parented under #190 (P2).
- **#156:** parented under #157, joining #154 and #155.
- **#23, #24:** now native children of #19. #23 is partly delivered; its comment lists what remains.
- **#207 (new epic): mission-type prompt and template hygiene.** Children: #146, #149, #158, #161, #164, #168, #176 and #180. #146, #149 and #158 had parents on core epics; those links were replaced.
- **#190 and #19:** bodies synced with the tracker.
- **#17:** comment re-bases the compound stacks on today's pack names.

## Classification

- **Types:** every non-epic issue now has a native type. Retyped or newly typed: #6, #12, #18, #23, #24, #37, #153, #160, #161, #168, #176, #180, #195 (Bug), #196, #197, #201, #202 (Bug).
- **Priorities:**
  - P1: #205, #206 (unchanged).
  - P2: #124, #140, #142, #149, #152, #158, #164, #176, #180, #195, #196, #201, #202.
  - P3: everything else.
- **Retired label:** `enhancement` removed from #37 and #139; the native type carries the kind.
- **Area label:** `doctrine` added to doctrine-content issues that lacked one.
- **Milestones:** none set. No open issue has a core 4.0.0 release-scope dependent, which is the milestone's stated rule.

## Left for the operator

- **#139:** core runtime behaviour, routing a mission step to a human for `role: operator`. The pack half has landed. Keep it here, or move it to core?
- **#17:** do compound stacks still earn their keep, now that `built-in` aggregates the core bundles? If they do, the stack table needs re-basing.
- **#150:** pack-tier decision pending since 2026-09-26: options A, B or C in its comments.
- **#147:** open design question on the spine-event re-run cost; needs adversarial review.
- **#205 and #206:** sequenced behind the charter slice B pin bump (spec-kitty-charter#501).

## Docs out of sync with the codebase (for the docs topic branch)

- `docs/packs/catalog-proposal.md`: disposition table added on branch `docs/catalog-disposition-2026-11`. The compound-stack table still uses the July names.
- `scripts/docs/gen_pack_reference.py --check` reports drift for all 19 generated pack pages on clean `main` (a6cfeab). This predates the pass.
- `packs/*/README.md` still points at `PROVENANCE.md` and `pack.md`. That work is #205.
- Stale `packs/built-in/...` paths in foundation prompts and tactics. That work is #195.
- `docs/research/blockers-and-core-dependencies.md` still frames blockers as core issues. #19 re-scoped them to the charter's pack schemas on 2026-11-09.
