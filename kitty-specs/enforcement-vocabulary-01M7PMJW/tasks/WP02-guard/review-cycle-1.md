---
affected_files: []
cycle_number: 1
mission_slug: enforcement-vocabulary-01M7PMJW
reproduction_command:
reviewed_at: '2026-11-18T06:37:43Z'
reviewer_agent: reviewer-renata
wp_id: WP02
---

Changes requested:
1 HIGH: the scan is line-wise, so a phrase wrapped across lines escapes ("Advisory in\n  v1:"). Also match across one line join, and add a wrapped test.
2 HIGH: coverage gaps for the classes R5 removed: "this is not optional", "not a recommendation", "non-negotiable rule", "directive binds", "lenient-adherence allowance", "rule is a hard gate".
3 False-positive risk: "makes ... binding" (DI/data binding), "advisory:" as a YAML key or an advisory label, "the rule is required reading". Narrow these, and add allowed controls.
