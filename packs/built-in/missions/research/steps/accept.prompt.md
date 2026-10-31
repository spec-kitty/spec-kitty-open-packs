---
description: Accept the published research report as the mission's final, traceable result
---
# /spec-kitty.accept - Accept Research Output

**Path reference rule:** When you mention directories or files, provide either the absolute path or a path relative to the project root (for example, `kitty-specs/<mission>/report.md`). Never refer to a folder by name alone.

**In repos with multiple missions, always pass `--mission <handle>` to every spec-kitty command.** The `<handle>` can be the mission's `mission_id` (ULID), `mid8` (first 8 chars of the ULID), or `mission_slug`.

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Location Pre-flight Check

**BEFORE PROCEEDING:** Verify you are working in the repository root checkout.

```bash
pwd
git branch --show-current
```

## What This Step Produces

An explicit **acceptance decision** — not new research. This is the final checkpoint that the approved report is complete, faithful to its evidence, and ready to stand as the mission's result.

## Goal

Confirm the research chain holds end to end — question, methodology, sources, findings, report — and record the mission as accepted, or block and route the gap back to the step it belongs to.

## What to Do

1. **Confirm `report.md` exists and was approved at `output`.** The `publication_approved` gate is the output step's review event; a report that was written but never approved is not acceptable here.

2. **Trace the chain.** Spot-check that each conclusion in `report.md` maps to a finding in `findings.md`, each finding to rows in `research/evidence-log.csv`, and each cited source to a row in `research/source-register.csv`. A claim that cannot be traced is a blocker, not a footnote.

3. **Confirm the question was answered.** Compare `report.md` with the research question and success criteria in `spec.md`. A report that answers a narrower or different question than the one scoped is a scope drift to surface, not to wave through.

4. **Confirm limitations are visible.** Limitations and threats to validity recorded in `findings.md` must still appear in `report.md`.

5. **Do not introduce new content here.** If acceptance surfaces a gap, block and name the step it belongs to — `scoping` for the question, `methodology` for the design, `gathering` for missing sources, `synthesis` for unsupported findings, `output` for report fidelity — rather than patching it in this step.

## Success Criteria

- `report.md` is approved and answers the question in `spec.md`.
- Every conclusion traces through `findings.md` and the evidence log to a registered source.
- Limitations and alternative interpretations are carried into the report.
- No unresolved blocker is hidden in prose-only notes.

## Handoff

This step does **not** re-scope, gather, synthesize, or rewrite the report. It only records whether the research result is accepted. If acceptance is blocked, name the specific earlier step the gap belongs to and stop here — do not attempt to close the gap yourself in this step.
