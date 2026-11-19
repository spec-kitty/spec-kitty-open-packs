# `qa` — QA Charter Pack

An open Spec Kitty Charter Pack for running quality assurance as governed work, and for keeping
a product's acceptance tests tied to what the product promises.

It does two jobs:

1. **A `qa` mission type.** The seven canonical steps redefined in QA terms (discovery, test
   strategy, test plan, test design, test execution, test report review, acceptance), with five
   QA agent profiles, its steps' substeps, templates, and two evidence tools. Ported from
   `spec-kitty-qa-pack`; see the README's Provenance section.
2. **Description to acceptance CI.** A standing loop from a human-readable product description to
   an automated release gate:

   ```
   promise page (DocKitty)  ->  Given/When/Then scenario  ->  bound acceptance test  ->  CI gate
        ratified by product        @promise:<id>              project's own runner     trace lint + run
   ```

The pack names no test runner. Your project runs its own tests; the pack governs what they must
cover and how honestly they report.

## What ships

| Kind | Artifacts |
| --- | --- |
| Directives | QA_001 traceability, QA_002 defect report quality, QA_003 no fake green, QA_004 exit criteria first, QA_005 risk-based prioritisation, QA_006 timeboxed exploratory charters, **QA_007 promise traceability**, **QA_008 reproductions gate releases** |
| Tactics | seven test-design tactics, plus **`qa-promise-elicitation`** |
| Procedures | coverage gap analysis, defect triage, go/no-go review, test plan review, plus **`qa-description-to-acceptance-ci`** |
| Styleguides | **`qa-promise-page`** |
| Toolguides and assets | `qa-carrier-lint`, `qa-result-ingest`, **`qa-promise-trace-lint`** (Python, stdlib plus ruamel.yaml); `sonar` |
| Agent profiles | strategist, test designer, executor, reporter, defect triager |
| Mission | `qa` mission type with its steps' substeps, step prompts, artifact templates, **promise page and scenario templates** |
| Glossary | ISTQB-grounded QA glossary |

The scenario-writing doctrine itself is not duplicated: the procedure points at Spec Kitty's
built-in `bdd-scenario-formulation` tactic, `given-when-then-authoring` styleguide and `gherkin`
toolguide.

## Adopt

Requires Spec Kitty 4.x with the Charter Pack cutover (`spec-kitty charter pack validate --help`
works). Register the pack in the consuming project's `.kittify/config.yaml`, pinned to a release
of this repository:

```yaml
charter_packs:
  org:
    packs:
      - name: qa
        local_path: "${SPEC_KITTY_PACK_HOME}/qa"
        source_type: git
        url: "https://github.com/spec-kitty/spec-kitty-open-packs.git"
        ref: "<commit SHA or pack/qa/vX.Y.Z tag>"   # never a branch; SPEC_KITTY_PACK_HOME is any directory
        subdir: packs/qa
```

Then:

```bash
spec-kitty charter fetch --pack qa
spec-kitty doctor charter-packs                       # pack healthy, no dangling endpoints
spec-kitty charter activate mission-type qa           # if you run QA missions
spec-kitty agent mission create <slug> --mission-type qa
spec-kitty charter context --include procedure:qa-description-to-acceptance-ci
```

See [Use a Charter Pack](../../docs/guides/use-a-charter-pack.md) for the configuration fields.

The pack activates nothing by itself. To put the promise layer in force for every project, add
a governing preset to the org's own pack, with its items marked `must_have: true` (the charter's
guide "Enforce presets on an organization's projects"):

```yaml
activated_directives:
  - id: QA_007
    must_have: true
  - id: QA_008
    must_have: true
activated_procedures:
  - id: qa-description-to-acceptance-ci
    must_have: true
```

Without one, the promise layer stays opt-in per project.

## The promise trace lint in CI

```bash
LINT="$(spec-kitty charter pack asset path qa-promise-trace-lint)"
python "$LINT" --promises docs --scenarios tests/scenarios --release "$VERSION" --json --out reports/promise-trace.json
```

Exit 0 when every ratified promise is checked and every scenario cites a ratified promise; 1 with
the list of what to fix; 2 when it cannot measure. Details: [toolguides/qa-promise-trace-lint.guide.md](toolguides/qa-promise-trace-lint.guide.md).

## Status

Pre-release. Not yet proven: a real QA mission with real content, and the promise loop run
against a real product. The first intended run is the Spec Kitty CLI itself.

## Known limitations

Checked on 2026-11-19 against spec-kitty-cli 4.0.0rc9, by reading its source and running it. The
pack follows the charter; these are gaps in that CLI release, not in the pack.

- **`blocking` outputs hold nothing yet.** `qa.mission-type.yaml` marks step outputs `blocking`:
  `spec.md`, `plan.md`, `tasks.md`, `test-report.md` and `qa-traceability.yaml` at `review`, and
  `qa-coverage.json` at `accept`. rc9 takes the artifacts that hold a step only from an
  `expected-artifacts.yaml` file. It does not read the step file, so no `qa` step and no
  `accept` waits for these outputs. Treat each blocking output as the step's contract and check
  it yourself before you move on.
- **No runtime hook runs the pack's tools.** `qa-result-ingest` and `qa-traceability-lint` run
  only when the agent runs them. The `review` and `accept` step prompts say when.
- **Action context does not load the pack.** `charter context --action <action> --mission-type qa`
  refuses `pack.yaml` because rc9 does not accept its `depends_on` field yet. Single lookups
  work: `charter context --include directive:QA_004`, `charter pack path qa` and
  `charter pack asset path qa-result-ingest` all resolve. The step prompts carry their
  directive citations.
- **Pack templates are not served by `--include template:`.** rc9 looks only in its built-in
  templates for that selector. Open `test-case-template.md` and `exploratory-charter-template.md`
  from the pack root that `spec-kitty charter pack path qa` prints, under
  `missions/qa/templates/`.

## Provenance

This pack is a port of [`spec-kitty/spec-kitty-qa-pack`](https://github.com/spec-kitty/spec-kitty-qa-pack)
at commit `e9ed31c` (2026-09-02), authored almost entirely by MOES-Media through eleven Spec Kitty
missions. It was first ported to `spec-kitty/private-packs` (draft PR #1, commit `e1aadcb`), which
added the promise layer, and then moved here: the source pack was prepared for donation upstream
(its `pack-donation-readiness` mission), and this repository is its public home. The source
repository carries no licence. **The author, MOES-Media, agreed on 2026-10-10 to distribute the pack
under this repository's MIT licence** (confirmed to the maintainers on that date).

The source repository keeps the full mission trail (`kitty-specs/`, `_rnd/`, `docs/install/`), the
authoring conventions (`CONVENTIONS.md`) and the pack's own 21-gate CI; this port does not copy
them. Read them there for the reasoning behind each artifact.
