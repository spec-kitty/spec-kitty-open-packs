---
affected_files: []
cycle_number: 4
mission_slug: release-pin-follow-through-01M872WA
reproduction_command: spec-kitty agent tasks move-task WP04 --to approved --mission release-pin-follow-through-01M872WA --agent claude::reviewer-renata
reviewed_at: '2026-11-24T16:28:48Z'
reviewer_agent: claude::reviewer-renata
wp_id: WP04
---

Approved by claude::reviewer-renata: approval:WP04

# WP04 review cycle 4: APPROVE (claude::reviewer-renata)

Reviewed lane-d @ 3708fc9d against coordination 8d8b9f47 (WP base 276e9e6).

## What holds
- B2 fixed. All 6 cycle-3 cases are flagged on line 1; all 6 join-only cases return []. New-item and heading checks run on the raw lines.
- Every cycle-1/2/3 probe gives the expected result (T015's 9 cases, wrapped FPs, makes…binding for/in, rules-are variants, npm prose, `*`/`**`/`_`/`__` emphasis, list/heading/blockquote cases).
- New probes behave: `*reading*` / `**reading**` at line start continue (spared); `+1 …` and `2026 is …` continue (claim kept); nested `> > -` lists are not joined, `> >` prose is; tab-indented and `-\t` bullets are new items; indented `#` continues the line.
- Mutants KILLED (34): [-*+] narrowed 3 ways, no numbered items, [.)]→[.], no next-line heading, no `>` prefix, no current-line heading, stripped next line, single `_`, indented heading (both), reach 160, [^.], reading guard, required-by guard, a/an, the/a/an, at-startup→at, no join, no `*`/`_` strip, no non-blocking, no only, v-only, adv-ctx scope (2), subjects, rules-only, levels, no _LEAD, no truncation.
- Pack scan: 758 files, 0 findings, rc 0, run as CI does (validate-packs.yml:116).
- Suites lane-d vs base: vocabulary 34 OK vs 22 OK; release 13 OK both; ci 292 with the same 4 setUpClass errors both (environmental); docs 49 OK both; assets 21 OK (14 skipped) both.
- No stray changes: code diff touches only the two owned files.

## Non-blocking
1. The enforcement-next equivalence argument in the commit body does not hold. `\blenient-adherence\s+[a-z]` crosses the join into "enforcement": "This tactic is lenient-adherence⏎enforcement: lenient-adherence" is [] on lane-d and flagged by the mutant (also "The rules that⏎enforcement: makes binding"). The guard is a real precision guard, preserved from base; pin it with that case in a follow-up and drop the "equivalent" claim.
2. `\d+[.)]` → `\d+[)]` survives, contrary to "both ways". "1. This makes⏎2. rules binding." does not depend on the join (`2.` blocks `[^.;:]`). Killing case: "Advisory in version⏎1. A list item." ([] on lane-d, flagged by the mutant; base gives [] too).
3. Residual, same on base: a 1–3-space-indented Markdown heading is joined like a YAML comment ("  # Heading that makes⏎rules binding happen on startup" is flagged). Acceptable trade for YAML comments.
4. Surviving, harmless: `match.start() < len(head)` → `<=` (no pattern can start at the join space); current-line enforcement skip (pinned by the pack scan, 10 findings).
