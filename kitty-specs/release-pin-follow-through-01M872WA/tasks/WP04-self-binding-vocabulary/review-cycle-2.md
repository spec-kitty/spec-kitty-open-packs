---
affected_files: []
cycle_number: 2
mission_slug: release-pin-follow-through-01M872WA
reproduction_command:
reviewed_at: '2026-11-24T16:09:13Z'
reviewer_agent: claude::reviewer-renata
wp_id: WP04
---

# WP04 review cycle 2: REJECT (claude::reviewer-renata)

Reviewed lane-d @ fa4f131 (code 7b6b6af) against coordination 744b5ef (WP base 276e9e6).

## What holds
- All cycle-1 findings are fixed in behaviour. Every cycle-1 probe now gives the expected result: the 3 wrapped FPs are spared; the 2 "makes … rules binding for/in" cases and the 4 "rules are mandatory …" variants are flagged; npm "purely advisory" and "advisory-only notices" are spared; `*`/`**` emphasis is handled.
- The cycle-1 mutants are killed: reach 160, `[^.]`, no reading guard, no required-by guard, no join, no emphasis strip, `$`/unpunctuated end. I also killed: reach 60, no `only`, no `non-blocking`, `v\d` only, unscoped advisory context, no `_LEAD` strip, `index + 2`, and no truncation.
- Wraps at every position of each phrase are flagged or spared correctly. The probes covered 2-line wraps, CRLF, curly quotes, em/en dashes, and `- ` dashes.
- `python3 scripts/ci/check_vocabulary.py` reports 758 pack files and 0 findings. CI runs it the same way (validate-packs.yml:116).
- Suites, lane-d vs base:
  - vocabulary: 28 OK vs 22 OK;
  - release: 13 OK on both;
  - ci: 292 on both, with the same 4 setUpClass errors (environmental);
  - docs: 49 OK on both;
  - assets: 21 OK, 14 skipped, on both.
- No stray changes: the triple-dot diff touches only the two owned files.
- Anti-pattern checklist:
  1. Dead code: PASS.
  2. Synthetic-fixture test: PASS.
  3. Silent empty return: PASS.
  4. FR coverage: PASS (FR-009).
  5. Frozen surface: PASS.
  6. Locked decision: PASS.
  7. Shared-file ownership: PASS (lane-d only).
  8. Production fragility: PASS.

## Findings (blocking: 1–2)

1. **The new "binding at startup/the/a/an" guard is untested. The WP-mandated T015 case is still truncated.**
   - T015 requires this case: "Spring makes rules binding at startup, then the service reads every directive and its rules binding the request." It must give 0 findings. `NOT_A_LEVEL` still holds only "Spring makes rules binding at startup", which cycle 1 flagged.
   - Because the full sentence is missing, these mutants of `(?!\s+(?:at\s+startup|the|a|an)\b)` keep `tests/vocabulary` green:
     - `(?:at\s+startup|the)` (drops a/an);
     - `(?:at\s+startup)` (drops the/a/an);
     - `(?:at|the|a|an)` (spares every "binding at …", for example "makes these rules binding at every gate").
   - The pack scan stays at 0 under all three, so CI does not pin them either.
   - Fix:
     - Restore the full T015 sentence. Lane-d already spares it, so it kills the `the` mutant.
     - Add a spared "… rules binding a/an …" case.
     - Add a flagged "makes these rules binding at every gate." case.

2. **Joining reads across list items and headings, which is a recall regression versus base.**
   - The named-continuation lookaheads run on `head + next line` after `_LEAD` strips `- `/`#`. So the next list item or paragraph decides whether this line is a level claim:
     - `- This makes rules binding⏎- A second item.`: flagged on base, missed on lane-d.
     - `- This makes rules binding⏎- the next item.`: flagged on base, missed on lane-d.
     - `- These rules are mandatory⏎- reading list`: missed.
   - It also causes a false positive: `# Heading that makes⏎- rules binding happen on startup` is flagged on lane-d.
   - YAML string lists of rules (`- …` per item, often unpunctuated) are exactly this shape.
   - Fix: do not join when the next line starts a new block, and treat end of line as the end there.
     - Example: the next line is blank, starts with a list marker `^\s*(?:[-*+]|\d+[.)])\s`, or a heading `^\s*#`.
     - Also do not join when the current line is a heading.
     - Keep joining `>` continuations and indented wraps.
   - Add a test for each of the four cases above.

## Non-blocking
3. More surviving mutants, in alternatives this WP adds. Each mutation below leaves `tests/vocabulary` green:
   - the rules-are subjects `(?:these|the|its|all)` → `(?:these)`;
   - its levels → `mandatory` only;
   - `rules|directives` → `rules`;
   - advisory-only nouns → `directive` only;
   - `advisory-only\s+` → `\s*`;
   - `(?:is|as)\s+advisory\s+context` → `is\s+…`.

   One case per alternative would pin them. The enforcement-field next-line guard and `at the X level in` survive as well, but they are pre-existing.
4. Gaps, partly pre-existing:
   - `_underscore_`/`__bold__` emphasis is missed: "These rules are _mandatory_.", and "mandatory _reading_" is a false positive.
   - A level word in backticks, quotes or a link is missed: "These rules are `mandatory`.", `"mandatory"`, `[mandatory](x)`.
   - A three-line wrap is missed: "These⏎rules are⏎mandatory.".
   - "The rule is binding the request" is flagged; base flags it too.
   - A phrase inside a code span is flagged, which is arguably correct for packs.

   Consider stripping `_` emphasis like `*`. The rest can be accepted and documented.
