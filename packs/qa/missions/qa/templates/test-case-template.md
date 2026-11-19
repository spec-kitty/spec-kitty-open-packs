# Test Case Template

This template produces a single test case **inside the body of** a project's `tasks/WP*.md`:
a fenced YAML block plus one Gherkin-notation scenario.

No step scaffolds this template. Open it from the pack root that
`spec-kitty charter pack path qa` prints: `missions/qa/templates/test-case-template.md`.

> **This block is not the work package's frontmatter.** A `tasks/WP*.md` file has one
> frontmatter section, at the top, and it belongs to the work package. Spec Kitty rejects
> unknown keys there, so the test-case keys below (`id`, `type`, `preconditions`) do not belong
> in it. A work package with these keys in its frontmatter is skipped with only a warning, and
> drops out of the mission without an error.
>
> Write test-case blocks in the WP **body**, below the frontmatter, as fenced ```yaml blocks.

## Test-case block fields

*Fill in every field: `id`, `requirement_refs`, `priority`, `type`, `preconditions`.* `automation_ref`
is optional — populate it only when this case has a corresponding automated JUnit-XML
implementation; leave it unset otherwise.

`requirement_refs:` is populated by `spec-kitty agent tasks map-requirements`; this template does
not redefine or re-implement that command. `assets/qa_carrier_lint.py`'s own bridge invariant
checks this same field (this pack's shipped `qa-traceability/v1` validator), and
`assets/qa_result_ingest.py` (this pack's shipped `qa-traceability/v1` producer) reads it directly
when correlating a case's declared `automation_ref` to the requirement(s) it covers.

`automation_ref` is an optional string naming the exact JUnit `classname::name` pair this case's
automated implementation resolves to (e.g.
`"TestCarrierSchema::test_schema_rejects_unknown_key"`). **Its condition is its own presence — not
the `type:` field.** A non-empty `automation_ref` declares that this case has real, automated
JUnit evidence to correlate for the current run; `qa-result-ingest` (shipped in this pack)
resolves it against ingested JUnit-XML and, on success, writes this case's carrier entry as
`type: automated` with `evidence.junit` populated. An absent or empty `automation_ref` means this
case has no automated evidence to correlate for this run; no JUnit correlation is attempted for
it, and its carrier-side classification (`exploratory`/`manual`, `evidence.session`) follows the
pre-existing session-evidence-pointer mechanism, unchanged and untouched by this field.

```yaml
id: TC-001
requirement_refs: []
priority: P1
type: functional
preconditions: []
```

The two examples below use `text` fences on purpose: `qa-result-ingest` reads every ```yaml block
in a work-package body as a case, so a work package that keeps these examples would ingest them.
Write your own cases as ```yaml blocks, like the `TC-001` block above.

### Example: automated case

```text
id: TC-014
requirement_refs: [FR-001]
priority: P1
type: functional
preconditions: []
automation_ref: "IngestPipelineTests::test_zero_testcase_guard_blocks_carrier_write"
```

When a case has a corresponding automated implementation, as here, `automation_ref` names it: this
case has a real, automated JUnit-XML implementation identified by the given `classname::name` pair,
and an ingester resolving this file's evidence looks for exactly that pair in the supplied
JUnit-XML results.

### Example: exploratory/manual case, no automated evidence

```text
id: TC-015
requirement_refs: [FR-002]
priority: P2
type: exploratory
preconditions: []
```

This case carries no `automation_ref` key, so the ingester attempts no JUnit correlation for it;
its evidence, if any, is a session-evidence pointer this case's frontmatter already carries by the
pre-existing mechanism — untouched by this field.

**Optional field.** A case with no `automation_ref` key is read like the exploratory example
above: no validation failure and no JUnit correlation. The `type:` field and its vocabulary are
independent of it.

## 1. Scenario

*Write the scenario in Given/When/Then form.*

The notation, the dialect, and any runner-binding rules live in
`styleguide:given-when-then-authoring` and `toolguide:gherkin` — this template cites both by name
as delegation targets and does not restate, narrow, or contradict either one's own content.

This template adds exactly one rule on top of that cited doctrine: each scenario's `Then` must be
independently observable, so a result row can be emitted per case.

**Operational test.** A `Then` clause is independently observable when it names a concrete,
checkable value or state transition — not a summary-judgment word ("correctly", "as expected",
"works") — that can be evaluated for that one scenario alone, without running any other scenario
first and without inspecting internal implementation state.

Compliant — a concrete, checkable `Then`, evaluable for this scenario alone:

```gherkin
Scenario: Order ships successfully
  Given an order with status "processing"
  When the warehouse marks the order as shipped
  Then the order's status field reads "shipped"
```

Rejected by this rule — a summary judgment naming no checkable value at all:

```gherkin
Scenario: Order ships successfully
  Given an order with status "processing"
  When the warehouse marks the order as shipped
  Then the system behaves correctly
```
