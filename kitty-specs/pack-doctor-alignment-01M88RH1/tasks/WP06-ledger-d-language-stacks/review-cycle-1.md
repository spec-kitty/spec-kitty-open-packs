---
affected_files: []
cycle_number: 1
mission_slug: pack-doctor-alignment-01M88RH1
reproduction_command:
reviewed_at: '2026-11-25T17:57:29Z'
reviewer_agent: claude::reviewer-renata
wp_id: WP06
---

# WP06 review 1: changes requested

Reviewer: claude::reviewer-renata. Reviewed at eca1f6e (feat commit 86c6030).

## Blocking

1. **The merge-map edit is not ids-only.** Besides renaming the 14 drupal `cluster` ids, 86c6030 adds a new key to each
   of those 14 clusters:
   `text: authored anti-pattern title (decision 01M89KEM7HW8675J5V54JPGE24); description verbatim`.
   A parsed diff of the map (250 clusters before and after) shows no other change. The commit message and the
   for_review note both say "ids only", and the dispatcher's acceptance condition for this out-of-scope edit to WP03's
   file was "only if nothing else in the map changed".
   The annotation does follow the README's own `text:` convention (set when the operator ruled authored text; see the
   M2 clusters), and `apply_curation.py` does not read it. The edit itself is reasonable, but it is not the change
   that was authorised. Fix it one of two ways:
   - (a) drop the 14 `text:` lines, so that the map edit is ids-only; or
   - (b) get a dispatcher ruling that keeps them, and correct the "ids only" claim in the for_review note.

## Verified (no action)

- 50 rows: go 8, java 5, javascript 13, python 4, rust 6, drupal 14. The rows match the 50 clusters homed in these
  packs one for one; each is a singleton, and its id and home agree with the map.
- Scripted against `packs/`: `source_title`, `owner`, `description`, `bad_example` and `good_example` are verbatim for
  all 50 rows, every `bad_example_source` is `bad_example` (no authored examples), and every `severity_grounding` quote
  appears verbatim in its entry. Non-drupal titles are verbatim.
- M6: each of the 14 drupal retitles names the rejected practice the description and bad example show, without a change
  of meaning. Each has `title_source: authored (decision …)` and quotes the original title. Descriptions are verbatim.
- Dry run on a scratch copy (ledgers 00, A, B, C and D, with their questions cleared on the copy only):
  - 45 blocks deleted (all 9 stack files among them) and 5 internal blocks kept;
  - a second apply writes nothing;
  - `--check` faults only on qa and internal (WP07).
  - The applied drupal files and their fragment edges look right.
- **Not reproduced:** the pack-doctor counts (artifact_schema_error 25→16, then 34). Building the jar from charter
  4b95b9151 was blocked in this session.

## Non-blocking, for the operator batch (not decided here)

- D1–D4 (the 4 open severity questions) are with the operator.
- Two drupal rows reach `severe` on rule wording alone, with no outcome: `fetching-services-via-drupal-inside-a-class`
  ("never fetch them via \Drupal:: inside a class") and `business-logic-in-the-module-file` ("it never carries business
  logic itself"). The criterion "never/always = mandatory = severe" is applied consistently, and it separates these rows
  from D2–D4 ("Prefer", "rather than", a contrast). The operator may want to confirm that line when answering D1–D4.
