---
affected_files: []
cycle_number: 1
mission_slug: pack-doctor-alignment-01M88RH1
reproduction_command:
reviewed_at: '2026-11-25T17:35:36Z'
reviewer_agent: claude::reviewer-renata
wp_id: WP04
---

# WP04 review 1: changes requested

Reviewer: claude::reviewer-renata. Reviewed content commit 436da07 (coordination branch @ 41fdfae).

## Required changes

### R1. Three home rows author new doctrine where a merged member has a verbatim bad example

These clusters have a title/content home row with an authored `bad_example`. Each also has a merged `name`/`bad_example` member whose source carries a verbatim `bad_example`:

| Cluster | Home row (authored) | Member with a verbatim bad example |
|---|---|---|
| `imperative-gherkin` | `procedures/bdd-scenario-lifecycle.procedure.yaml#/anti_patterns/0` | `styleguides/given-when-then-authoring.styleguide.yaml#/anti_patterns/0` |
| `merge-the-scaffolding-clean-it-up-later` | `procedures/development-assist-test-cleanup.procedure.yaml#/anti_patterns/0` | `styleguides/test-desiderata-and-boundaries.styleguide.yaml#/anti_patterns/6` |
| `shared-mutable-state-between-scenarios` | `procedures/bdd-scenario-lifecycle.procedure.yaml#/anti_patterns/2` | `styleguides/testing-principles.styleguide.yaml#/anti_patterns/0` |

Decision `01M89Q9JT79VYFMBRNPS9BHHP1` (M4 Q3) ruled that a member's verbatim bad example (and its good example) replaces an authored one, "since authored examples are for entries with no verbatim instance". Ledger A never authors an example where a verbatim one exists. Its four clusters with verbatim member examples use them, under M2 and M4. Ledger B authors new doctrine in that case.

Fix: in each of the three rows, use the member's verbatim `bad_example`, and its `good_example` where the home row has none. Set `bad_example_source` to name the member source and the decision, for example `bad_example of merged member <source>, verbatim (decision 01M89Q9JT79VYFMBRNPS9BHHP1)`. If you think Q3 governs these rows instead, send it to the dispatcher as an operator question and don't resolve it yourself.

### R2. The "default" guard lets a quoted bare "default" through

`says_default` strips every double-quoted span, whether or not that span quotes the source. So a grounding that puts the word itself in quotes passes:

```
says_default('severity "default"')   -> False
says_default('smell ("default")')    -> False
says_default('"x": the "default" call') -> False
```

The guard is meant to stop a defaulted call, and these strings are defaulted calls.

Fix: discount a quoted span only when it occurs verbatim in the row's source text (title, description or content, or the host file). That check can run in `--check`/apply, where `source_entry` is available. As a fallback, discount a quote only when it is more than the bare word "default". Add a test that each of the three strings above refuses, and keep the existing test that the verbatim "a drifted default state" quote passes.

## Verified (no change needed)

- Coverage: 80 rows equal 80 merge-map members homed in testing and writing; 71 clusters. No row is missing, extra or duplicated. `id`, `merged_into` and the home agree with the map on every row.
- Text: `source_title`, `title`, `description`, `good_example` and the verbatim `bad_example` match the source on every home row. Owners match the owner files' `id`.
- U3: every home row is the home-pack member. Five clusters have two home-pack members, and the earliest source in map order was taken each time (non-blocking: consider stating that tie-break in README's merged-text rule).
- Severity groundings: every quoted span appears verbatim in its entry. I checked the three elided ("...") quotes fragment by fragment. The quotes in `bad_example_source` are also verbatim.
- I read all 25 authored bad examples. Each is concrete, accurate to its content clause, and adds no claim beyond it. Apart from R1 they need no change.
- Merges (9): each joins texts that make the same claim, and none is a theme merge. `shared-mutable-state-between-scenarios` (data dependency vs. shared-state pollution) is the nearest to the line, but it is the merge map's (WP03) call and the merge_reason quotes both texts.
- The five open severity questions (B1-B5) are with the operator and were not reviewed for outcome. The history records that they were sent.
- The 37 tests pass. On a scratch copy (ledgers 00+A+B, questions cleared on the copy): 25 inline blocks deleted, 8 kept, and a second apply writes nothing. `--check` faults only for later batches, with none in testing or writing.
- Not reproduced: the pack-doctor counts (57→36, and 64 after remediate). Charter could not be built in the reviewer session. Non-blocking: 25 blocks were deleted but `artifact_schema_error` falls by 21. Add a line to the history saying which 4 files still answer it, or why.
