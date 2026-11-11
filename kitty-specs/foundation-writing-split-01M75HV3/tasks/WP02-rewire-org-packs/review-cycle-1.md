---
affected_files: []
cycle_number: 1
mission_slug: foundation-writing-split-01M75HV3
reproduction_command:
reviewed_at: '2026-11-11T16:37:40Z'
reviewer_agent: claude-reviewer-subagent
wp_id: WP02
---

# WP02 review: Rewire the org packs (foundation-writing-split-01M75HV3, #73)

Commit under review: 146844f "feat(packs): rewire the org packs onto foundation, writing and the bundles (#73)", diffed against its parent 0064771.
Worktree: /home/user/spec-kitty-open-packs/.worktrees/foundation-writing-split-01M75HV3-lane-b

## Verdict: REJECT (one narrow fix)

The rewiring itself is correct and complete. Every check passes except one: T010 is only partly done. The internal README's file-tree list does not include the four items internal received.

## Checks (scripted)

1. **Reference rewrites: PASS.**
   - There were 102 `built-in::` references before the change and 0 after: internal 62, qa 27 (3 in the fragment and 24 in profiles), event-driven 7, spdd 6. These counts match research §3.
   - Fragments: I rebuilt each file from `git show HEAD^:` by replacing `built-in::<kind:id>` with `<owner>::<kind:id>`, using membership.json. Where the owner is the referrer's own pack, I wrote the id bare. All four fragments came out byte-identical to the committed files, so no other line changed.
   - internal: six references to its received `procedure:mission-wrap-up-sequence`, `procedure:mission-tracer-files` and `styleguide:tiered-standards` are now bare.
   - qa profiles: the ids have no kind, so I resolved each one by the kind of its section (tactic, styleguide, procedure or toolguide). All 24 match the owning pack, with no ambiguity. Only the reference lines changed.
   - `grep -rn "built-in::" packs` returns nothing.
2. **depends_on: PASS.** Each pack's dependencies equal the qualifiers its content uses. The pack_ids match membership.json `pack_ids`, and the range is `>=1.0,<2`. Every version went from 1.0.0 to 1.1.0.

   | Pack | depends_on | Qualifiers used |
   |---|---|---|
   | spec-kitty-internal | adversarial-review, foundation, planning-analysis, refactoring, testing, writing | the same six |
   | quality-assurance | foundation, planning-analysis, testing | the same three; testing is required by FR-004 |
   | event-driven | architecture | architecture |
   | spdd | architecture, foundation | the same two |
   | cave-kitty | foundation | none; the dependency is the prose binding, and implementer-ivan and reviewer-renata are named in the cave-dev implement, accept, analyze and review prompts |

   There are no cycles. Every org pack depends on org bundles or on foundation and writing, which are at built-in level, so there is no level violation. No old built-in pack_id remains. The other `x::` matches in these packs (`py::`, `li::`, `classname::` and so on) are pytest node ids, CSS and code, not pack references.
3. **validate-packs.sh with the charter contract: PASS.** Exit code 0. All 19 packs report 0 violations, the cross-pack checks report 0 violations, and the invalid fixtures fail as expected.
4. **Fragment endpoints in the closure: PASS.** Every qualified endpoint is in the pack's transitive depends_on closure, which I computed from the pack.yaml files:
   - internal: 72 qualified endpoints, 0 outside the closure
   - qa: 4, 0 outside
   - event-driven: 7, 0 outside
   - spdd: 6, 0 outside
   - cave-kitty: 0
5. **README and PROVENANCE: partly done.**
   - The qa PROVENANCE note and README row are accurate. sonar (`.toolguide.yaml` and `.guide.md`) moved as R100 renames in eeda028, and the gherkin and mutation items are owned by testing in membership.json.
   - The internal PROVENANCE note is accurate. All four items are R100 renames in eeda028, and the ids match membership.json.

## Findings

- **MEDIUM (blocking): T010 is incomplete for internal's README.**
  - T010 says: "Add WP01's moved qa/internal items to their packs' README/pack.md lists ... where those lists exist."
  - `packs/internal/README.md` has a complete file tree, and the fragment line says it "declares every node and edge below". That tree does not list:
    - `procedures/mission-tracer-files.procedure.yaml`
    - `procedures/mission-wrap-up-sequence.procedure.yaml`
    - `styleguides/tiered-standards.styleguide.yaml`
    - `assets/audiences/agentic-framework-core-team.md` and its `.asset.yaml`
  - The commit did not touch the internal README at all.
  - Fix: add the four items to the tree, marked "(moved from built-in by #73)", the way `terminology-guard` is already marked.
- **LOW: one comment in internal's pack.yaml is inaccurate.** The depends_on comment says "Its DRG fragment and profiles reference ...", but `packs/internal/agent_profiles/` does not exist. Change it to "Its DRG fragment references ...".
- **INFO, no action in WP02: the org rows of membership.json `depends_on` are stale.**
  - The table predicts these dependency sets:
    - internal: adversarial-review, foundation, planning-analysis, writing
    - qa: foundation, testing
    - event-driven: foundation
    - spdd: foundation
  - The implementation follows the WP/FR-010 rule instead: depend on exactly the referenced packs, which is the operator ruling DM 01M75HVY66EHV8YYBAY4C4QXAG. The references need testing and refactoring for internal, planning-analysis for qa, and architecture for event-driven and spdd.
  - The implementation is right, and the planning artifact should be reconciled later.
- **INFO: some README prose still says "built-in".** Examples are "the built-in test doctrine" and "refines built-in RED_MAIN_RELEASE_DISCIPLINE". The WP says prose "built-in" means the distribution, so these are not defects.
