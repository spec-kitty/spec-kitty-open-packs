---
affected_files: []
cycle_number: 3
mission_slug: release-pin-follow-through-01M872WA
reproduction_command:
reviewed_at: '2026-11-24T16:19:34Z'
reviewer_agent: claude::reviewer-renata
wp_id: WP04
---

# WP04 review cycle 3: REJECT (claude::reviewer-renata)

Reviewed lane-d @ b2afd8e against coordination 114510b9 (WP base 276e9e6).

## What holds
- **B1 is fixed.** The full T015 sentence is in `BINDING_CONTINUATIONS`, together with "binding a" and "binding an". "makes these rules binding at every gate." is flagged. I re-ran all three cycle-2 mutants and each is KILLED:
  - drop a/an;
  - drop the/a/an;
  - `at\s+startup` → `at`.
- **Every cycle-1 and cycle-2 probe gives the expected result.** That covers the 3 wrapped false positives, the "makes … binding for/in" cases, the 4 "rules are mandatory …" variants, the npm prose, `*`/`**` emphasis, and the 4 cycle-2 list/heading cases.
- **The folded alternatives are pinned.** These mutants are KILLED: subjects reduced to `these`, subjects without `its`, levels reduced to `mandatory`, `rules|directives` → `rules`, advisory-only nouns reduced to `directive`, `(?:is|as)` → `is`, no `_` strip, left-only `_` strip, no `*` strip. The cycle-1 and cycle-2 mutants are also all KILLED: reach 160, `[^.;:]`, reading guard, required-by guard, no join, heading anchored with `^\s*#`.
- **The blank-line no-op claim is true.** An empty or whitespace-only following line joins to `head + " "`, and no pattern reads a trailing space differently. The `if following and` mutant survives, as expected.
- **Other block shapes are handled acceptably:**
  - Fenced code (```` ``` ````, `~~~`), front matter, `---`/`***` rules and setext `===`/`---` underlines: a claim right before them is still flagged, and none of them create a false positive.
  - Blockquote continuations (`> … mandatory⏎> reading`) are spared, and `> … mandatory⏎> for every mission` is flagged.
  - Tables are flagged, because the `|` blocks the continuation lookaheads.
  - Indented `-` and `1.` items are fine.
- **The pack scan is clean.** `python3 scripts/ci/check_vocabulary.py` reports 758 pack files and 0 findings. CI runs it the same way (validate-packs.yml:116).
- **Suites match base**, lane-d vs coordination base:

  | Suite | lane-d | base |
  | --- | --- | --- |
  | vocabulary | 31 OK | 22 OK |
  | release | 13 OK | 13 OK |
  | ci | 292, 4 errors | 292, 4 errors |
  | docs | 49 OK | 49 OK |
  | assets | 21 OK, 14 skipped | 21 OK, 14 skipped |

  The 4 ci errors are the same setUpClass errors on both branches (contract fetch, environmental).
- **No stray changes.** The code diff touches only `scripts/ci/check_vocabulary.py` and `tests/vocabulary/test_check_vocabulary.py`.
- **Anti-pattern checklist:** dead code PASS; synthetic fixture PASS; silent empty return PASS; FR coverage PASS; frozen surface PASS; locked decision PASS.

## Findings (blocking: 1)

1. **B2 is only half fixed: `*` bullets and blockquoted list items still join, so recall regresses against base.** Every case below is flagged on coordination 114510b9 and missed on lane-d b2afd8e:
   - `* This makes rules binding⏎* the next item.`
   - `* This makes rules binding⏎* A second item.`
   - `  * This makes rules binding⏎  * an item`
   - `* The directive is required⏎* by`
   - `- This directive is required⏎* by the gate`
   - `> - This makes rules binding⏎> - the next item.`

   Two causes:
   - `self_binding_in` removes every `*` (`line.replace("*", "")`) before `_STARTS_SOMETHING_NEW` sees the next line. A `* ` bullet therefore reads as indented prose and is joined. The cycle-2 fix asked for `[-*+]`. 11 shipped pack files use `* ` bullets, so the gap is real.
   - `_STARTS_SOMETHING_NEW` does not allow a `>` prefix, so a list item inside a blockquote is joined as well. `_LEAD` then strips both the `>` and the `-`.

   Fix:
   - Test the next line for a new block on the raw line, before the `*`/`_` strip, with `[-*+]`.
   - Allow an optional `(?:>\s*)*` prefix in front of the list marker and the heading.

   Add a test for each of the 6 cases above.

   Pin the guard alternatives as well. Each of these mutants leaves `tests/vocabulary` green today:
   - `[-+]` → `[-]`;
   - no numbered items;
   - `\d+[.)]` → `\d+[.]`;
   - no next-line heading.

   The numbered test (`1. … binding⏎2. A second item.`) does not kill its mutant: `2.` blocks the lookahead whether or not the lines are joined. Use cases whose outcome depends on the join. Each should give `[]`:
   - `+ This makes⏎+ rules binding.`;
   - `1) This makes⏎2) rules binding.`;
   - `This makes⏎# rules binding`.

## Non-blocking
2. The residual list leaves out `__bold__` emphasis. Cycle 2 named it, but only `_x_` was folded. "These rules are __mandatory__." is still missed, because `_` is a word character and `_EMPHASIS` strips neither underscore. Fold it or list it as a residual.
3. Pre-existing: the `enforcement:` next-line guard is still unpinned (its mutant survives). Removing `(?<!\w)`/`(?!\w)` from `_EMPHASIS` (stripping every `_`) also survives. That one is harmless for the current patterns.
4. Otherwise the residual list is honest and acceptable: level words in backticks, quotes or links; three-line wraps; advisory-only `\s+`→`\s*` (the mutant survives, as declared).
