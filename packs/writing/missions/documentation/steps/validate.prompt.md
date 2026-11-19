---
description: Validate generated documentation against explicit quality gates and record the verdict
---
# /spec-kitty.validate - Validate Documentation Quality

**Path reference rule:** When you mention directories or files, provide either the absolute path or a path relative to the project root (for example, `kitty-specs/<mission>/audit-report.md`). Never refer to a folder by name alone.

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

- **`kitty-specs/<mission>/audit-report.md`** — the canonical evidence artifact recording which gates passed, which failed, what risks remain, and whether the documentation is fit to publish.

This is the last checkpoint before content meets readers.

## Goal

Gate the content produced in `generate` against explicit quality criteria and record a reproducible, evidence-backed verdict.

## What to Do

1. **Treat validation as a set of explicit gates, not an impressionistic skim.** Each gate needs an objective check, an evidence trail, and a pass/fail outcome. The writing pack's docs styleguides name this step as the check for their rules; run each gate below and record its result in `audit-report.md`.

2. **Run the structural lint with `--extended`** over the docs root. The `common-docs-structural-lint` toolguide says how to resolve the script and its policy file (load it with `spec-kitty charter context --include toolguide:common-docs-structural-lint`):

   ```bash
   python3 "$(spec-kitty charter pack asset path common-docs-structural-lint)" \
     --styleguide "$(spec-kitty charter pack asset path common-docs-structural-lint-config)" \
     --extended docs
   ```

   Pass `--styleguide` the project's own policy file instead if it keeps one. The gate passes on exit `0`. Exit `1` lists each violation with its check id; fix it in `generate` and rerun. Exit `2` means the policy file did not load, so nothing was checked. Record the command, the page count and the output. A count of `0` pages means the wrong docs root.

3. **Verify the Divio type declaration** (divio-type-discipline styleguide). Every page produced in `generate` declares exactly one `type:` in its frontmatter: `tutorial`, `how-to`, `reference` or `explanation`. The page sits in the section its type maps to (tutorials and how-tos in `docs/guides/`, reference in `docs/api/`, explanation in `docs/architecture/`), and its content keeps to that type. A page tagged `tutorial` that reads like reference fails the type contract regardless of how good the content is. A tutorial must not branch on reader choices.

4. **Verify freshness** (docs-freshness-sla styleguide). Every page carries `updated: YYYY-MM-DD`, set to the date its content was last checked against the product. Compare each date with the staleness threshold of the page's tier, as the project sets the tiers (the styleguide's illustrative defaults: tutorial and how-to 90 days, hand-written reference 180 days, explanation 365 days, generated reference re-freshened on every build). Flag every page past its threshold as stale.

5. **Verify that no placeholder is left.** A page is unresolved if it carries a `[TODO:` marker or any `{...}` slot of the Divio template it was built from. Check each page produced in `generate` against its own template, so braces in a code sample are not mistaken for slots:

   ```bash
   slots() {  # the {...} slots of one Divio template
     spec-kitty charter context --include "template:documentation/divio/$1" --json \
       | python3 -c 'import json,re,sys; print("\n".join(sorted(set(re.findall(r"\{[^{}\n]+\}", json.load(sys.stdin)["context"])))))'
   }
   grep -n '\[TODO:' docs/guides/getting-started.md
   grep -nF -f <(slots tutorial-template.md) docs/guides/getting-started.md
   ```

   Both greps print nothing for a page that may publish. A hit fails the gate.

6. **Verify completeness against `plan.md`**: every required cell is either filled or deferred-with-reason; no orphaned drafts.

7. **Review plain language** (plain-language styleguide). This is a human-in-the-loop review, not an automated grade. Check each page for audience fit, active voice and consistent terminology, and record each finding.

8. **Verify accessibility** (docs-accessibility styleguide) appropriate to the publication target: every non-decorative image has non-empty alt text, the heading outline descends without skipping a level (H1 → H2 → H3), no link text is a bare "click here" or URL, and themed elements have sufficient color contrast. Accessibility failures discovered post-publish are user-visible — catch them here.

9. **Verify source-of-truth fidelity** (publication-authority styleguide): reference matches code and documents only behaviour the code ships; reference is generated where a generator exists; tutorials and how-tos run verbatim as written; explanations cite the architecture they describe; each fact has one canonical page that the others link to.

10. **Verify cross-link integrity**: every internal link and every `related:` entry resolves; the link graph matches `plan.md`.

11. **Verify generator reproducibility**: rerun the documented generator commands in a clean environment and confirm they reproduce the published artifacts.

12. **Run a pre-mortem against publication.** What fails after readers arrive? Stale screenshots, broken commands, contradictory pages, missing prerequisites. Pre-publication risks include drift (the code moved, the docs did not), unstable examples (the API changes after publish), and audience mismatches (the page targets a reader the `discover` spec did not promise). Surface each such risk now, not after publish.

13. **Give every surfaced risk a disposition**: accept (with a rationale), mitigate (with the action), or block-publish. This vocabulary maps onto the `adversarial-squad-deployment` procedure's findings-disposition contract (load it with `spec-kitty charter context --include procedure:adversarial-squad-deployment`): accept -> `deferred_with_rationale` (the risk stands and the page publishes unchanged; record the rationale and where it is tracked), mitigate -> `accepted` (the page changed accordingly; record where the action landed, or use `changed` when the concern is resolved another way), block-publish -> `deferred_with_rationale` while the rework is pending (deferred back to `generate` or `design` with the blocking rationale recorded), then replaced by `accepted` once the rework lands (each finding carries exactly one disposition at a time; record where the rework landed). Risks that block publish go back to `generate` or `design` as appropriate — do not silently downgrade a blocking risk to a warning.

14. **Write `audit-report.md` as the canonical evidence artifact.** Record each gate above with its result and evidence. Cite concrete page paths, concrete failures, concrete fixes — "some pages have issues" is a note-to-self, not a validation. Assign a verdict: `ready-to-publish`, `needs-rework`, or `blocked`. The `publish` step reads this verdict and does not bypass it. If a previous `audit-report.md` exists, compare trends — a metric that worsened across cycles is itself a finding.

## Success Criteria

- `audit-report.md` exists, is complete, and carries an explicit verdict.
- The structural lint exits `0` with `--extended`, and every page passes the type, freshness and placeholder gates.
- Every claimed gate has cited evidence (page path, command output, screenshot, or diff).
- Risks marked `block-publish` are addressed before the verdict flips to `ready-to-publish`.
- The report is reproducible: rerunning the gates produces the same outcome on the same content.

## Handoff

This step gates content against quality criteria only. It does **not** reopen scope, audience, or iteration mode (`discover` decisions), reopen the gap analysis (`audit` decisions), reopen the architecture or generator selection (`design` decisions), author new content beyond the fix-it loops needed to clear gates (`generate`'s job), or publish the result (`publish`'s job). A validate report that proposes new sections or new architecture is overstepping — surface the need and send it back to the appropriate step.
