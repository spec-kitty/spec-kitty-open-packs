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

   The lint needs Python 3 with the `ruamel.yaml` package; without it the script stops with an import error, which is not a lint result, so install the package and rerun. If your installed Spec Kitty does not know the `common-docs-structural-lint-config` asset id, the toolguide gives the fallback paths. Pass `--styleguide` the project's own policy file instead if it keeps one. The gate passes on exit `0`. Exit `1` lists each violation with its check id; fix it in `generate` and rerun. Exit `2` means the policy file did not load, so nothing was checked. Record the command, the page count and the output. A count of `0` pages means the wrong docs root.

3. **Verify the Divio type declaration** (divio-type-discipline styleguide). Every page produced in `generate` declares exactly one `type:` in its frontmatter: `tutorial`, `how-to`, `reference` or `explanation`. The page sits in the section its type maps to (tutorials and how-tos in `docs/guides/`, reference in `docs/api/`, explanation in `docs/architecture/`), and its content keeps to that type. A page tagged `tutorial` that reads like reference fails the type contract regardless of how good the content is. A tutorial must not branch on reader choices.

4. **Verify freshness** (docs-freshness-sla styleguide). Every page carries `updated: YYYY-MM-DD`, set to the date its content was last checked against the product. Compare each date with the staleness threshold of the page's tier, as the project sets the tiers (the styleguide's illustrative defaults: tutorial and how-to 90 days, hand-written reference 180 days, explanation 365 days, generated reference re-freshened on every build). Flag every page past its threshold as stale.

5. **Verify that no placeholder is left.** A page is unresolved if it carries a `[TODO:` marker or a `{...}` template slot. Every Divio template slot is a `{...}` token, so check the pages themselves; this needs no template lookup and cannot pass because a lookup failed. Run it over every page produced in `generate`:

   ```bash
   python3 - docs/guides/getting-started.md docs/api/status.md <<'EOF'
   import re, sys
   if len(sys.argv) < 2:
       sys.exit("placeholder check: no page given; pass every page generate produced")
   SLOT = re.compile(r"\{[^{}\n]+\}")
   FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
   failed = False
   for path in sys.argv[1:]:
       fence = None  # the opening fence run while inside a fenced block
       for n, line in enumerate(open(path, encoding="utf-8"), 1):
           m = FENCE.match(line.rstrip("\n"))
           if m and fence is None and not (m.group(1)[0] == "`" and "`" in m.group(2)):
               fence = m.group(1)
               continue
           if m and fence and m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence) and not m.group(2).strip():
               fence = None
               continue
           if "[TODO:" in line:
               print(f"FAIL {path}:{n}: [TODO: marker"); failed = True
           spans = [line] if fence else re.findall(r"`[^`]*`", line)
           prose = "" if fence else re.sub(r"`[^`]*`", "", line)
           for slot in SLOT.findall(prose):
               print(f"FAIL {path}:{n}: {slot}"); failed = True
           for slot in (s for span in spans for s in SLOT.findall(span)):
               print(f"REVIEW {path}:{n}: {slot}")
       if fence:
           print(f"FAIL {path}: a {fence} fence is never closed"); failed = True
   sys.exit(1 if failed else 0)
   EOF
   ```

   A `{...}` token in prose, or a `[TODO:` marker, prints `FAIL` and the command exits `1`: the page may not publish. A `{...}` token inside code prints `REVIEW`: decide for each one whether it is a leftover slot (fix it in `generate`) or real code (record it as reviewed). The gate passes when the command exits `0` and every `REVIEW` line is resolved. Any other exit status, an error, or a run with no page fails the gate. A fence closes only on the same character, at least as long as the one that opened it, so a fence nested in a longer one does not end the outer block. A fence left open at the end of a page fails, since everything after it would only be reviewed.

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
