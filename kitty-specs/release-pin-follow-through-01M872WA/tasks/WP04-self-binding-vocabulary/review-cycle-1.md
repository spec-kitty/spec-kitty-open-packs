---
affected_files: []
cycle_number: 1
mission_slug: release-pin-follow-through-01M872WA
reproduction_command:
reviewed_at: '2026-11-24T15:53:54Z'
reviewer_agent: claude::reviewer-renata
wp_id: WP04
---

# WP04 review: REJECT (claude::reviewer-renata)

Reviewed lane-d @ 9dd127b against base 1bb3985 (WP base 276e9e6).

## What holds
- The 9 cases match #304 exactly. All 9 tests are red on base and green on lane-d. The message test is also red on base.
- Every earlier REFUSED/WRAPPED/ALLOWED case still passes. `tests/vocabulary`: 25 OK (22 on base).
- `python3 scripts/ci/check_vocabulary.py`: 758 pack files, 0 findings. It reproduces, and CI (`validate-packs.yml:116`) invokes it the same way.
- Self-binding message is at most 200 characters and still names `term:spec-kitty-core/enforcement-level`.
- No stray changes. The diff touches only the two owned files plus the coord merge 1bb3985.
- CI suites, same on lane-d and base: release 13 OK, ci 292 with 4 errors (charter contract fetch 404, environmental), docs 49 OK, assets 21 OK (14 skipped).

## Findings (blocking: 1–3)

1. **A line wrap at the anchor brings the #304 false positives back.** `self_binding_in` checks each line on its own before joining it to the next line. On a lone line, `_CLAUSE_END`'s `$` and the `(?!\s+by\b)` / `(?!\s+reading\b)` lookaheads accept the end of the line. So when the ~80-column wrap the docstring describes falls right after the level word, the phrase is flagged again:
   - `Spring makes rules binding⏎at startup.` → flagged (the #304 case)
   - `the directive is required⏎by the charter` → flagged (the #304 case)
   - `These rules are mandatory⏎reading for reviewers.` → flagged (a new FP from the new pattern)

   Fix: when a next line exists, do not let end of line count as an anchor. For example, evaluate the anchored patterns on the joined text, or treat `$` as a boundary only at end of text. Add WRAPPED-style tests for each anchor.

2. **Recall regression: real binding claims that base caught now slip through.** Requiring `binding` to end the clause drops:
   - `This directive makes these rules binding for every mission.`
   - `The charter makes its rules binding in every lane.`

   Both are flagged on 1bb3985 and missed on 9dd127b. Spare the framework sense instead, by excluding verb or object continuations after `binding` (e.g. `(?!\s+(?:at\s+startup|the|a|an)\b)`), the same way `required(?!\s+by\b)` does. T016's suggested boundary also accepts `\s+(?:and|but|in|at|for|until)\b`.

   The same applies to the new `rules are <level>` pattern, which misses:
   - `These rules are mandatory for every mission.`
   - `These rules are mandatory and enforced.`
   - `These rules are mandatory—no exceptions.`
   - `These rules are mandatory”.` (unicode quotes are missing from `_CLAUSE_END`)

3. **Test gaps (surviving mutants).** Each mutation below leaves `tests/vocabulary` green:
   - reach `{0,120}` → `{0,160}`;
   - `[^.;:]` → `[^.]` (the "one clause" claim is not pinned: the WP's required sentence "Spring makes rules binding at startup, then the service reads every directive and its rules binding the request." was shortened to "Spring makes rules binding at startup", which does not exercise the reach);
   - the `rules are` pattern's `_CLAUSE_END` replaced by `\b` (no spared case such as "These rules are mandatory reading.");
   - `$` dropped from `_CLAUSE_END` (no case without trailing punctuation).

   Add a case that kills each.

## Non-blocking
4. Loose: bare `\b(?:strictly|purely|merely)\s+advisory\b` and `\badvisory-only\b` flag npm prose, which the module header says stays legal:
   - "The npm audit output is purely advisory."
   - "npm advisories are advisory-only notices."

   Consider requiring a directive/rule/guidance subject nearby, or accept this and document it.
5. `only advisory` (in T017's list) is not covered. Markdown emphasis defeats several anchors:
   - `This is *advisory context*.` (caught on base, missed now)
   - `This directive is *strictly* advisory.`
   - `These rules are **mandatory**.`
   - `mandatory *reading*` / `required *by*` (still FPs)

   Consider stripping `*`/`_` before matching.
6. The optional `(?:strictly|purely|merely)\s+` inside the directive pattern is dead: the standalone adverb pattern already covers it, and removing either one keeps every test green. Drop one.
