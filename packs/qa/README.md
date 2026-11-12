# `qa` — QA Charter Pack

An open Spec Kitty Charter Pack for running quality assurance as governed work, and for keeping
a product's acceptance tests tied to what the product promises.

It does two jobs:

1. **A `qa` mission type.** The seven canonical steps redefined in QA terms (discovery, test
   strategy, test plan, test design, test execution, test report review, acceptance), with five
   QA agent profiles, step contracts, templates, and two evidence tools. Ported from
   `spec-kitty-qa-pack`; see Provenance below.
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
| Toolguides and assets | `qa-carrier-lint`, `qa-result-ingest`, **`qa-promise-trace-lint`** (Python, stdlib plus ruamel.yaml); `sonar` (moved from built-in by #73) |
| Agent profiles | strategist, test designer, executor, reporter, defect triager |
| Mission | `qa` mission type, step contracts, step prompts, artifact templates, **promise page and scenario templates** |
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

Pre-release. On Spec Kitty 4.0.0rc7 (`spec-kitty/spec-kitty@3b7c6dde`, plus spec-kitty#6004 where
`charter activate` is used on typer ≥ 0.26) the pack validates cleanly, and a scratch `qa` mission was driven through all seven steps to `terminal: done`:
`next` served the pack's own step prompts, the pack's plan-field declaration refused the unfilled
test-plan template, `review` held until `qa-traceability.yaml` and `test-report.md` existed,
`accept` held until `qa-coverage.json` existed, and `qa-result-ingest` plus
`qa-traceability-lint` turned a template-shaped work package and a JUnit file into
`verdict: ready`. `QA_001`–`QA_008` resolve for the `specify`, `plan` and `review` actions. Not
yet proven: a real QA mission with real content, and the promise loop run against a real
product. The first intended run is the Spec Kitty CLI itself.

### Known limitations

- **Step artifacts are read from two places.** In the probe run the `plan` guard read `plan.md`
  from the primary checkout's `kitty-specs/<mission>/`, while the `review` and `accept` guards
  read the coordination worktree. Write each artifact where the blocking `next` result's
  `guard_failure_paths` points.

- **`discovery` gets no charter governance.** It is a QA-only step that aliases the built-in
  `research` action, and `charter context --action discovery` resolves no directives. The step
  prompt itself still carries its directive citations.
- **`charter activate directive QA_00N` refuses the id** ("Unknown directive ID") although
  `charter context --include directive:QA_00N` resolves it. Put the directives in force through
  a governing preset in your org's pack, as above.
- **Only the first org pack answers `charter context --include`**
  ([spec-kitty/spec-kitty#5779](https://github.com/spec-kitty/spec-kitty/issues/5779)). With
  this pack registered after another org pack (for example `spec-kitty-internal`),
  `--include directive:QA_007` reports "No directive found" while the action context and
  `doctor charter-packs` are fine. List `qa` first, or wait for the fix.
- **`charter activate mission-type qa` needs typer < 0.26 or spec-kitty/spec-kitty#6004.** A
  `pip`/`uv tool` install that resolves typer 0.26+ refuses every positional `charter activate`
  with `--pack, --force, --json only apply with --preset.` until that fix ships.

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

### What changed in the port

| Change | Why |
| --- | --- |
| Directive ids `QA-00N` became `QA_00N`. | Current Spec Kitty resolves org-pack directives only in the underscore form. Before the change, `charter context --include directive:QA-001` found nothing for any of the six directives. |
| `spec-kitty doctrine asset path` became `spec-kitty charter pack asset path`. | The `doctrine` command group was removed in the 4.x Charter Pack cutover. |
| `drg/fragment.yaml` carries no provenance header (the pack name `qa` comes from the consumer's registration); `org-charter.yaml` named the org `spec-kitty-qa` and used schema version 2 (the file is retired since #242). | Namespacing, and the schema version `charter org init` writes. |
| Added QA_007 (promise traceability), QA_008 (reproductions gate releases), the `qa-promise-elicitation` tactic, the `qa-promise-page` styleguide, the `qa-description-to-acceptance-ci` procedure, the `qa-promise-trace-lint` asset and toolguide, and two templates. | The promise -> scenario -> acceptance CI layer (from private-packs PR #1). |
| `qa_result_ingest.py` reads test cases from fenced ```yaml blocks in the work-package body, with self-test Pair15. | Fixes spec-kitty-qa-pack#5: the template puts cases in the body (WPMetadata forbids them in the frontmatter), but the ingester read only the frontmatter, so a template-conformant mission ingested `cases_total: 0` with exit 0. |
| Removed `qa.graph.yaml`, `missions/qa/governance-profile.yaml`, the `qa-reviewer-quinn` placeholder profile, the empty `paradigms/` and every `.gitkeep`. | The empty pack-root graph and the duplicate governance profile are not read (the mission type still activates and creates missions without them); the placeholder profile carried no content and nothing referenced it. |
| Step-contract bootstrap commands are `charter context --action <a> --mission-type qa --json`. | The source's `--role` flag and `--profile`/`--tool` inputs do not exist on 4.x; all seven bootstrap commands failed with "No such option". |
| `qa-test-designer-tessa` cites the tactic `bdd-scenario-formulation`. | Its old reference, `behavior-driven-development`, was retired in 4.0.0rc5 in favour of that tactic. |
| The `test-case-template.md` examples (`TC-014`, `TC-015`) use `text` fences, and the ingester reads every CommonMark yaml fence form (`YAML`, `yml`, info-string attributes, tildes, longer and indented fences), warning on a repeated case id or an unclosed fence (self-test Pair16). | With the #5 fix the template's own examples would otherwise be ingested as cases, and other valid fence forms were dropped without a word. |
| Internal finding ids (`SK-NNN`) replaced by plain descriptions. | They point at a ledger outside this repository. |
| Not ported: `scripts/`, `kitty-specs/`, `_rnd/`, `kitty-ops/`, `.kittify/`, `docs/install/`, `CONVENTIONS.md`. | History and tooling pinned to older Spec Kitty builds; `pack_ci.py` imports APIs that no longer exist (`DoctrineService`, `save_pack_registry`). This repository's `scripts/ci/validate-packs.sh` replaces its validation role. |

At port time the step prompts were `missions/qa/command-templates/<step>.md`, and the runtime built
the `qa` action sequence from `mission-steps/`. Since spec-kitty-open-packs#95 (charter ADR-0044)
the `qa` mission type is one file, `missions/qa/qa.mission-type.yaml`. It holds the seven steps in
run order, each with its role and, from `specify` on, its expected output artifacts. The step
prompts are `missions/qa/steps/<step>.prompt.md`. The `blocking` flag of the retired
`expected-artifacts.yaml` is now the `blocking` field of a step's expected output in that file.
The port-time rows above and the checks below record the layout of that time.

### Verified at port time

Against Spec Kitty `main` at `3b7c6dde` (4.0.0rc7), in a scratch project with this pack registered
under `charter_packs.org.packs`:

- `spec-kitty charter pack validate packs/qa` and `charter org validate packs/qa`: 0 errors,
  0 advisories. `doctor charter-packs`: no collisions, no dangling endpoints, alone and together
  with `spec-kitty-internal` (core `packs/internal`) in either order. With both registered,
  `charter context --include` resolves only the first-listed pack's artifacts
  (spec-kitty/spec-kitty#5779).
- `charter activate mission-type qa` succeeds (with spec-kitty/spec-kitty#6004 on typer 0.27);
  `agent mission create --mission-type qa` creates a `qa` mission, not `software-dev`; `next`
  serves the `discovery` step from `missions/qa/command-templates/discovery.md`.
- `charter context --mission-type qa` resolves `QA_001`–`QA_008` for `specify`, `plan` and `review`.
- A scratch `qa` mission ran all seven steps to `terminal: done` (`discovery` → `accept`). The
  plan-field declaration refused the unfilled test-plan template; `review` and `accept` held until
  their blocking artifacts existed; on a work package written to `test-case-template.md`,
  `qa-result-ingest` reported `cases_total: 1` (0 before the #5 fix) and `qa-traceability-lint`
  reported `verdict: ready`, 1 of 1 requirements covered.
- Asset self-tests: `qa_result_ingest.py` 16 of 16, `qa_carrier_lint.py` 38 of 38,
  `qa_promise_trace_lint.py` 12 of 12.

### Received from built-in (#73)

The `sonar` toolguide (`toolguides/sonar.toolguide.yaml`, `sonar.guide.md`) moved here from
`packs/built-in/` with `git mv` when #73 split built-in; its history follows the file. The mutation
and Gherkin items once proposed for qa went to the `testing` bundle, which this pack now depends on.
