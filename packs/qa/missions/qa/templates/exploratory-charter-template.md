# Exploratory Charter Template

This template produces the session sheet behind an exploratory testing session inside a project's
`tasks/WP*.md` — an SBTM-shaped charter, timebox, notes, bugs, and debrief.

No step scaffolds this template. Open it from the pack root that
`spec-kitty charter pack path qa` prints: `missions/qa/templates/exploratory-charter-template.md`.

The six sections below are a floor, not a ceiling: they are the minimum this template must
declare. An author may add further sections beyond this list, provided each addition carries its
own one-line stated-purpose sentence in the same style as the sections below; omitting a section
listed here is non-compliant regardless of what else is added.

## Frontmatter

*Populate `requirement_refs:` via `spec-kitty agent tasks map-requirements`; do not hand-author
this field.*

`requirement_refs:` is populated by `spec-kitty agent tasks map-requirements`; this template does
not redefine or re-implement that command. The bridge check in `qa-carrier-lint` (this pack)
reads this same field.

```yaml
---
requirement_refs: []
---
```

## 1. Charter Statement

*State the mission this session pursues — what area, risk, or question it explores.*

## 2. Timebox

*State the session's fixed duration and its start/stop time.*

## 3. Areas / Coverage

*List the areas, features, or risk zones this session covers.*

## 4. Session Notes

*Record what was actually done during the session, as it happened.*

## 5. Bugs / Issues Found

*List each bug or issue discovered, with enough detail that it can be filed.*

## 6. Debrief Outcome

*State what was learned, what was covered, what was left uncovered, and how the timebox held up.*

A timebox overrun and its debrief must be recorded explicitly here — never silently treated as
on-schedule.
