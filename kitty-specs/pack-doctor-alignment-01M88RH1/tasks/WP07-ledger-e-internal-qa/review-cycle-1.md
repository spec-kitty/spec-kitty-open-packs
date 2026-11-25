---
affected_files: []
cycle_number: 1
mission_slug: pack-doctor-alignment-01M88RH1
reproduction_command:
reviewed_at: '2026-11-25T18:43:30Z'
reviewer_agent: claude::reviewer-renata
wp_id: WP07
---

# WP07 review cycle 1: changes requested

Reviewer: claude::reviewer-renata. Reviewed at fb6216c (coordination branch; ledger E in 258add6).

## Required

All three are authored bad examples (Q3, new doctrine) that misstate their host procedure (the WP05 lesson).

**R1. `decision-drip`: the example faults something the host allows.**
`procedures/cloud-session-dispatch.procedure.yaml#/anti_patterns/8`. The example ends "and implements its own
recommendation for the first before the answer comes". The host's prompt section (8) allows that: "Work started on a
recommendation must be reversible, and a later operator ruling overrides it." The anti-pattern is acting
*irreversibly* on a recommendation. Either drop that clause (the three piecemeal messages already show the drip), or
make the act irreversible, for example "and deletes the legacy table on its own recommendation before the answer
comes".

**R2. `landing-a-draft-pr-without-asking`: "approved and merged" are not this procedure's actions.**
`procedures/landing-contributor-prs.procedure.yaml#/anti_patterns/0`. Landing takes a PR to merge-ready; the
maintainer never merges unless the operator chose auto-merge, so "merged" mixes in a different anti-pattern
(`agent-merges-the-mainline`). The host's own words for the fault: "Do not rebase, push or comment on a draft PR
without the operator's explicit go-ahead." For example: "A contributor's draft PR is rebased and two landing fixes are
pushed to its branch without asking the operator."

**R3. `silent-acceptance-without-traceability-check`: the traceability runs the wrong way.**
`qa/procedures/qa-test-plan-review-workshop.procedure.yaml#/anti_patterns/0`. The example ("three requirements map
to no test area") is a requirement-coverage gap. The host's step traces the other way: "Walk the plan's test areas
and confirm each one maps to a stated requirement, feature, or identified risk rather than existing without a
traceable origin." For example: "The test plan is approved although two of its test areas trace to no requirement,
feature or risk item."

## Nits (fix if cheap; not blocking)

- N1. `recapturing-a-ci-owned-file-during-a-landing`: the host's own example of a CI-owned file is "a test-shard
  timing file"; prefer it to the invented "benchmark snapshot".
- N2. `retroactive-fill-in`: the host's entries are dated (`[YYYY-MM-DD][phase]`), not timestamped; "undated" fits
  the host better than "with no timestamps".
- N3. `catch-all-root`: "with no owner per bucket" presumes buckets; a catch-all has none. "with no buckets beneath
  it" says what the host describes.
- N4. `deferring-instead-of-finishing`: the grounding quote elides the parenthesis with "...". Each part is verbatim;
  fine, but a reader cannot paste it as one search string.

## Verified (no change needed)

- Coverage: 65 rows = the 65 members of the 59 merge-map clusters homed in qa (2) and internal (57); 6 merged rows.
  Ids, homes, `merged_into` and `merge_reason` agree with the map.
- Verbatim (scripted): every `source_title`, `owner`, `title`, `description`, `good_example` and source `bad_example`
  matches its source; merged-member good and bad examples match the named member. Every quoted span in every
  `severity_grounding`, authored `bad_example_source` clause and `merge_reason` is verbatim in the entry, the named
  member, or (one case) the host text.
- Merges (M1): the six multi-member clusters each make one claim (five charter-offering/feature-and-scenario pairs;
  landing-contributor-prs with mission-wrap-up-sequence on per-commit green). No theme merges. U3: each home row
  carries the earliest home-pack member's text.
- Authored examples: all 45 read against their host procedures. All are on clusters with no verbatim example among
  their members (WP04 R1). None cites a directive id or claims what a directive enforces. Apart from R1-R3 they are
  concrete, minimal and use the host's vocabulary and states (`status:claimed`, `priority:P0`, `in-mission`, section
  (1), the three-PR cap, `origin/main` against the canonical remote).
- Severity: the 13 open questions (E1-E13) are with the operator; not decided here. The non-question calls follow
  the rubric; "a mandatory rule is broken -> severe" has precedent in ledgers B and D. No grounding uses "default".
- Dry run (scratch copy, ledgers 00 and A-E, open questions cleared on the copy only): 61 inline blocks deleted, 265
  files written; `--check` exits 0 with 0 faults; a second apply writes nothing and leaves the tree byte-identical.
- **Not reproduced:** pack-doctor `validate --round-trip --full` (0 violations, 19 warnings). This sandbox could not
  attach the charter repository, and no jar is on disk.
- Gate: `spec-kitty agent action review` gave no BLOCK (one non-blocking bulk-edit note: the new ledger file).
