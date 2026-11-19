---
description: Generate documentation content against the locked design — Divio-typed pages plus generator output
---
# /spec-kitty.generate - Generate Documentation Content

**Path reference rule:** When you mention directories or files, provide either the absolute path or a path relative to the project root (for example, `docs/api/`). Never refer to a folder by name alone.

**In repos with multiple missions, always pass `--mission <handle>` to every spec-kitty command.** The `<handle>` can be the mission's `mission_id` (ULID), `mid8` (first 8 chars of the ULID), or `mission_slug`.

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Location Pre-flight Check

**BEFORE PROCEEDING:** Verify you are working in the mission's working checkout. Unless the mission set up another, that is the repository root checkout, on the mission branch.

```bash
pwd
git branch --show-current
```

## What This Step Produces

- Documentation content pages under `docs/`, in the common-docs section each Divio type maps to (per `plan.md`'s navigation hierarchy):

  | Divio type | Section | Template |
  |------------|---------|----------|
  | Tutorial | `docs/guides/` | `template:documentation/divio/tutorial-template.md` |
  | How-to | `docs/guides/` | `template:documentation/divio/howto-template.md` |
  | Reference | `docs/api/` | `template:documentation/divio/reference-template.md` |
  | Explanation | `docs/architecture/` | `template:documentation/divio/explanation-template.md` |

  Load a template with `spec-kitty charter context --include template:documentation/divio/<name>`. Do not create `tutorials/`, `how-to/`, `reference/` or `explanation/` directories: the common-docs standard does not sanction them, and the structural lint fails them.
- Generator output for reference content: Sphinx `autodoc`/`napoleon` for Python, JSDoc for JavaScript/TypeScript, rustdoc for Rust — whichever the `design` step selected.

## Goal

Produce the documentation content itself — Divio-typed pages written against the design's templates, plus any auto-generated reference output. This step is **execution**: the planning is already done in `discover`/`audit`/`design`.

## What to Do

1. **Stay faithful to `plan.md` and the design's architecture.** This is not the place to redesign; if the design has a defect, fix it in `design` and rerun this step — do not silently patch around it here.

2. **Honor the Divio type contract for every page.** Tutorial pages teach (learning-oriented, hands-on). How-to pages solve a stated task (goal-oriented). Reference pages describe a stable surface (information-oriented). Explanation pages give context and rationale (understanding-oriented). Mixing voices inside one page is a defect.

3. **Drive every reference-style page from the source of truth** — code, schemas, configuration. Invoke the configured generator (for example: `sphinx-build -b html docs/ docs/_build/html/`, `npx jsdoc -c jsdoc.json`, `cargo doc --no-deps`) and capture the exact command and configuration in your notes so a future author can rerun it. Hand-maintained reference drifts; generated reference stays aligned.

4. **Leave deferred Divio cells deferred.** Where `plan.md` deferred a cell, filling it here silently expands scope and breaks the discover→design→generate trace. If you believe a deferred cell must be filled now, that's a re-scoping decision — escalate, don't just write it.

5. **Start each page from its Divio template and fill every slot.** A slot is a `{...}` token the template carries, such as `{TUTORIAL_TITLE}`, `{YYYY-MM-DD}` or `{link}`. Replace each slot with real content. If you cannot fill a slot yet, replace it with `[TODO: <what is missing>]`, so the gap is named and searchable. Never leave a `{...}` slot in a page. A page flagged for publication carries no `[TODO:` marker either — `validate` fails it.

6. **Fill the common-docs frontmatter on every page.** Keep `type:` as the template sets it: it is the page's Divio type. Set `doc_status: draft` (or the project's own starting value), `updated:` to today's date as `YYYY-MM-DD`, a `description` of 50-180 characters, and `audience` and `related` in the shape the common-docs styleguide gives. Name each file in lowercase kebab-case, and keep file names unique across sections.

7. **Keep `docs/architecture/index.md` complete.** `architecture/` is curated-complete: link every explanation page you add from its `index.md`, or the structural lint's `index_completeness` check fails. Give every new section an `index.md`.

8. **Link as designed.** Cross-links from reference into how-to, how-to into tutorial, explanation into the rest follow `plan.md`'s link graph. Do not invent ad-hoc links the navigation does not anticipate.

9. **Make tutorials and how-tos verbatim runnable.** Every command, every code block, every URL is something a reader will actually type. If it does not work in your environment, it will not work in the reader's — test it before you write it down.

10. **Mark unstable-API examples with their stability status** so readers can self-protect, and declare the living-documentation cadence and owner for pages expected to evolve with the code.

11. **Keep reference aligned with its surface.** Reference content must match the code, schema or configuration it describes. If the surface changes during this step, update both, or stop and record the drift for `validate`. Reference output that cannot be regenerated is technical debt.

12. **Run the structural lint before handoff.** The `common-docs-structural-lint` toolguide says how to resolve and run it. Run it with `--extended` over `docs/` and fix what it reports. `validate` runs it again.

13. **Commit content in small, reviewable increments.** A single commit covering an entire section is hard to review and harder to revert.

## Success Criteria

- Every required Divio cell from `plan.md` is filled or explicitly deferred with a recorded reason.
- Generator output is reproducible: the recorded command and configuration produce the same result in a clean environment.
- Reference content is aligned with the source of truth at the moment of generation.
- No `{...}` template slot remains in any page, and no `[TODO:` marker remains in any page flagged for publication.
- Every page sits in the section its Divio type maps to, carries the common-docs frontmatter, and passes the structural lint with `--extended`.

## Handoff

This step produces documentation content against the locked design only. It does **not** reopen needs, audience, or scope (`discover` decisions), reopen the gap analysis (`audit` decisions), reopen the architecture or generator selection (`design` decisions), or decide whether the result is fit to publish (`validate`'s job). A generate output that includes new design decisions or revised audit findings is a leaked planning step — keep the phases clean.
