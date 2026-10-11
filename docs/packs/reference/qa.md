---
title: "Pack: qa"
description: "Generated reference for the qa Charter Pack: 8 directives, 8 tactics, 5 procedures, 1 styleguide, 3 toolguides, 5 agent profiles, 1 glossary pack, 7 mission step contracts, 3 asse…"
doc_status: active
updated: '2026-10-11'
type: API
kind: Reference
tags:
- pack-reference
- generated
generated:
  by: scripts/docs/generate_pack_reference.py
  at: '2026-10-11'
related:
- packs/reference
---

# Pack: qa

> **Generated — do not edit.** This page is rendered from `packs/` by `scripts/docs/generate_pack_reference.py`; CI fails on drift. Change the pack, then re-run the generator.

> **⚠ This pack ships executable code.** 3 assets in this pack are code a consumer may run: `assets/qa_carrier_lint.py`, `assets/qa_promise_trace_lint.py`, `assets/qa_result_ingest.py`. Read them before you adopt the pack (see the repository's `SECURITY.md`); the checksum below only proves the files match this repository.

## Summary

| Field | Value |
| --- | --- |
| Source | [`packs/qa/`](../../../packs/qa/) |
| Purpose | — (no `pack.yaml`) |
| Depends on | — |
| Artifacts | 8 directives, 8 tactics, 5 procedures, 1 styleguide, 3 toolguides, 5 agent profiles, 1 glossary pack, 7 mission step contracts, 3 assets, 1 mission type, 1 mission, 7 mission steps |
| DRG fragment | 35 node(s), 16 edge(s) ([`drg/fragment.yaml`](../../../packs/qa/drg/fragment.yaml)) |
| Org charter | org `spec-kitty-qa`; keys: `org_name`, `schema_version` ([`org-charter.yaml`](../../../packs/qa/org-charter.yaml)) |

## Provenance & integrity

- **Content checksum** (`open-packs-sha256-v1`, 82 file(s)): `sha256:b2708d2910511618a62cadf6b358f3e62d20f2efb8ac7dcc254f6648e30321aa`
- **File set:** the git-shipped files (tracked, plus untracked files that are not ignored). A clean checkout or release tarball of the pack contains exactly
  these files. Symlinks and file names containing a backslash or newline are rejected.
- **Verify** a fetched copy from inside the pack directory:

  ```sh
  # in a git checkout (matches what CI hashes):
  git ls-files -z --cached --others --exclude-standard -- . | tr '\0' '\n' | LC_ALL=C sort \
    | while IFS= read -r f; do sha256sum "./$f"; done | sha256sum
  # in a plain download of exactly those files:
  find . -type f ! -path './.git/*' | LC_ALL=C sort \
    | while IFS= read -r f; do sha256sum "$f"; done | sha256sum
  ```

  (`shasum -a 256` in place of `sha256sum` on macOS.) This is tamper-evidence for the published
  content, not a signature: it tells you the copy matches this repository, not who to trust
  (ADR 2026-07-18-3).

## Directives

| ID | Title | Summary | Enforcement | Source |
| --- | --- | --- | --- | --- |
| `QA_001` | QA Traceability Mandatory | Every requirement a test\-strategy\/test\-report artifact declares must trace to a test case\, checked at strategy authoring and every report submission\, by recomputing from enumerated ids — never a free… | `required` | [`directives/qa-001-traceability-mandatory.directive.yaml`](../../../packs/qa/directives/qa-001-traceability-mandatory.directive.yaml) |
| `QA_002` | QA Defect Report Quality | A defect report is judged incomplete unless it carries seven distinct\, present fields\: repro steps\, expected result\, actual result\, environment\, severity\, priority\, and attached evidence\. This direct… | `required` | [`directives/qa-002-defect-report-quality.directive.yaml`](../../../packs/qa/directives/qa-002-defect-report-quality.directive.yaml) |
| `QA_003` | QA No Fake Green | A test report\/CI run record must never read greener than the run\. Forbidden\: did\-not\-run into absent\, timeout into failed\, retries into final attempt\, skipped into passed\, inapplicable into either\. E… | `required` | [`directives/qa-003-no-fake-green.directive.yaml`](../../../packs/qa/directives/qa-003-no-fake-green.directive.yaml) |
| `QA_004` | QA Exit Criteria Precede Execution | Exit criteria for a test run are frozen before execution begins\. Execution begins at the timestamp the first suite named in the declared test strategy starts running\, or an equivalent explicit marker… | `lenient-adherence` | [`directives/qa-004-exit-criteria-precede-execution.directive.yaml`](../../../packs/qa/directives/qa-004-exit-criteria-precede-execution.directive.yaml) |
| `QA_005` | QA Risk\-Based Prioritization | Suite execution order is governed by the current risk register\'s rank\, so the riskiest declared work is tested first by default\. Any departure from that order — including the absence of a risk regist… | `lenient-adherence` | [`directives/qa-005-risk-based-prioritization.directive.yaml`](../../../packs/qa/directives/qa-005-risk-based-prioritization.directive.yaml) |
| `QA_006` | QA Exploratory Charters Timeboxed | Exploratory testing is governed by a written charter set before the session begins\, stating a timebox\, and closing with a recorded debrief\. A session missing any of the three has no basis for evaluat… | `lenient-adherence` | [`directives/qa-006-exploratory-charters-timeboxed.directive.yaml`](../../../packs/qa/directives/qa-006-exploratory-charters-timeboxed.directive.yaml) |
| `QA_007` | QA Promise Traceability | What the product promises decides what must be verified\, not the tests that happen to exist\. Every gating scenario cites a ratified promise\, every ratified promise is checked by a scenario or carries… | `required` | [`directives/qa-007-promise-traceability.directive.yaml`](../../../packs/qa/directives/qa-007-promise-traceability.directive.yaml) |
| `QA_008` | QA Known\-Defect Reproductions Gate Releases | \"Green\" means no known open defect of the agreed kind\. A confirmed defect in the agreed scope becomes a scenario that fails until the fix lands\, and a release candidate is cut only when every gating… | `required` | [`directives/qa-008-reproductions-gate-releases.directive.yaml`](../../../packs/qa/directives/qa-008-reproductions-gate-releases.directive.yaml) |

## Tactics

| ID | Title | Summary | Steps | Source |
| --- | --- | --- | --- | --- |
| `qa-boundary-equivalence-partitioning` | Boundary and Equivalence Partitioning | Derive test cases for a requirement\'s input domain using two black\-box techniques as the primary method itself\: equivalence partitioning \(\`qa\-glossary\`\) divides the domain into partitions where every… | 5 steps | [`tactics/qa-boundary-equivalence-partitioning.tactic.yaml`](../../../packs/qa/tactics/qa-boundary-equivalence-partitioning.tactic.yaml) |
| `qa-exploratory-charter-writing` | Exploratory Charter Writing | Write a timeboxed exploratory\-testing charter — mission\, areas to explore\, risks\/resources\, and time budget — before an exploratory testing session begins \(per this pack\'s \`exploratory testing\`\/\`test… | 5 steps | [`tactics/qa-exploratory-charter-writing.tactic.yaml`](../../../packs/qa/tactics/qa-exploratory-charter-writing.tactic.yaml) |
| `qa-flaky-test-quarantine` | Flaky Test Quarantine | Detect and isolate tests that fail nondeterministically so they stop masking real signal in a run\'s verdict\. A test is flagged when an immediate rerun of the same code and environment produces a fals… | 5 steps | [`tactics/qa-flaky-test-quarantine.tactic.yaml`](../../../packs/qa/tactics/qa-flaky-test-quarantine.tactic.yaml) |
| `qa-pairwise-test-reduction` | Pairwise Test Reduction | Reduce a combinatorial input\-parameter space to a pairwise\-covering test set\: rather than testing every combination of every parameter\'s values\, construct the smallest set of test cases such that eve… | 4 steps | [`tactics/qa-pairwise-test-reduction.tactic.yaml`](../../../packs/qa/tactics/qa-pairwise-test-reduction.tactic.yaml) |
| `qa-promise-elicitation` | Promise Elicitation \(seed candidates\, then ratify\) | Build a product\'s promise set from what it already tells its users\, without letting those sources decide what the product owes\. Every surface that asserts behaviour \(user docs\, command help\, error me… | 6 steps | [`tactics/qa-promise-elicitation.tactic.yaml`](../../../packs/qa/tactics/qa-promise-elicitation.tactic.yaml) |
| `qa-regression-suite-selection` | Regression Suite Selection | Select which regression tests \(per this pack\'s \`regression testing\` glossary term\, \`qa\-glossary\`\) to run for a given change\, based on the change\'s impact and test history\, rather than re\-running the… | 5 steps | [`tactics/qa-regression-suite-selection.tactic.yaml`](../../../packs/qa/tactics/qa-regression-suite-selection.tactic.yaml) |
| `qa-risk-based-test-prioritization` | Risk\-Based Test Prioritization | Rank test cases by risk — likelihood times impact of failure\, per this pack\'s \`risk\`\/ \`product risk\` glossary terms \(\`qa\-glossary\`\) — to decide execution order when time does not allow running every… | 5 steps | [`tactics/qa-risk-based-test-prioritization.tactic.yaml`](../../../packs/qa/tactics/qa-risk-based-test-prioritization.tactic.yaml) |
| `qa-test-data-minimization` | Test Data Minimization | Reduce the volume and complexity of the test data \(per this pack\'s \`qa\-glossary\` term\) a test case uses\, while preserving its coverage intent\. Distinct from \`test\-minimisation\`\, which removes redunda… | 5 steps | [`tactics/qa-test-data-minimization.tactic.yaml`](../../../packs/qa/tactics/qa-test-data-minimization.tactic.yaml) |

## Procedures

| ID | Title | Summary | Steps | Source |
| --- | --- | --- | --- | --- |
| `qa-coverage-gap-analysis` | QA Coverage Gap Analysis | Identify gaps between what the test basis requires and what the current test suite actually covers — a test\-coverage gap analysis\, per this pack\'s \`test coverage\` glossary term \(\`qa\-glossary\`\)\. The n… | 5 steps | [`procedures/qa-coverage-gap-analysis.procedure.yaml`](../../../packs/qa/procedures/qa-coverage-gap-analysis.procedure.yaml) |
| `qa-defect-triage-ritual` | QA Defect Triage Ritual | A periodic ISTQB severity\/priority classification governance meeting over defects surfaced by test execution\. This ritual is neither of two near\-neighbor built\-ins\: it is not issue\-triage\-state\-machi… | 5 steps | [`procedures/qa-defect-triage-ritual.procedure.yaml`](../../../packs/qa/procedures/qa-defect-triage-ritual.procedure.yaml) |
| `qa-description-to-acceptance-ci` | Description to Acceptance CI \(promise \-\> scenario \-\> gating run\) | The standing loop that turns a human\-readable product description into automated acceptance checks that gate a release\. Product describes what the product promises on DocKitty promise pages\; QA and s… | 10 steps | [`procedures/qa-description-to-acceptance-ci.procedure.yaml`](../../../packs/qa/procedures/qa-description-to-acceptance-ci.procedure.yaml) |
| `qa-go-no-go-readiness-review` | QA Go\/No\-Go Readiness Review | An ISTQB\-style go\/no\-go release\-readiness review meeting\, evaluating exit criteria and outstanding defects before a release decision\. This review is cited as adjacent to\, and distinct from\, three rel… | 5 steps | [`procedures/qa-go-no-go-readiness-review.procedure.yaml`](../../../packs/qa/procedures/qa-go-no-go-readiness-review.procedure.yaml) |
| `qa-test-plan-review-workshop` | QA Test Plan Review Workshop | A peer\-review \(per this pack\'s \`review\` glossary term\, \`qa\-glossary\`\) workshop over an already\-drafted test plan \(per this pack\'s \`test plan\` glossary term\, \`qa\-glossary\`\) or test strategy document\,… | 5 steps | [`procedures/qa-test-plan-review-workshop.procedure.yaml`](../../../packs/qa/procedures/qa-test-plan-review-workshop.procedure.yaml) |

## Styleguides

| ID | Title | Summary | Source |
| --- | --- | --- | --- |
| `qa-promise-page` | Promise Page Authoring \(DocKitty\) | — | [`styleguides/qa-promise-page.styleguide.yaml`](../../../packs/qa/styleguides/qa-promise-page.styleguide.yaml) |

## Toolguides

| ID | Title | Summary | Source |
| --- | --- | --- | --- |
| `qa-carrier-lint` | QA Traceability Carrier Lint \(Coverage Validator\) | Validates a qa\-traceability\/v1 carrier \(qa\-traceability\.yaml\) and computes qa\-coverage\.json\, a machine\-readable coverage record\: requirement\/case coverage counts\, JUnit\-XML and session\-evidence class… | [`toolguides/qa-carrier-lint.toolguide.yaml`](../../../packs/qa/toolguides/qa-carrier-lint.toolguide.yaml) |
| `qa-promise-trace-lint-guide` | QA Promise Trace Lint \(promise \-\> scenario chain\) | Reconciles promise pages in a DocKitty docs tree with the \`\@promise\:\<id\>\` tags on Gherkin scenarios\, and reports untraced scenarios\, dangling or candidate citations\, uncovered ratified promises\, decl… | [`toolguides/qa-promise-trace-lint.toolguide.yaml`](../../../packs/qa/toolguides/qa-promise-trace-lint.toolguide.yaml) |
| `qa-result-ingest-guide` | QA Result Ingestion \(JUnit\-XML Producer\) | Resolve the script via \`spec\-kitty charter pack asset path qa\-result\-ingest\` — the asset sidecar\'s own id\, distinct from this toolguide\'s own id \(qa\-result\-ingest\-guide\) — then invoke it with \`\-\-resu… | [`toolguides/qa-result-ingest.toolguide.yaml`](../../../packs/qa/toolguides/qa-result-ingest.toolguide.yaml) |

## Agent profiles

| ID | Title | Summary | Roles | Source |
| --- | --- | --- | --- | --- |
| `qa-defect-triager-dmitri` | qa\-defect\-triager\-dmitri | qa\-defect\-triager\-dmitri is the cross\-cutting defect\-triage profile\: it gatekeeps the seven\-field defect report\, enforces that severity and priority are set independently rather than collapsed into o… | `defect-triager` | [`agent_profiles/qa-defect-triager-dmitri.agent.yaml`](../../../packs/qa/agent_profiles/qa-defect-triager-dmitri.agent.yaml) |
| `qa-reporter-rhea` | qa\-reporter\-rhea | qa\-reporter\-rhea owns the reporting step of the QA lifecycle\: recomputing mapped\, unmapped\, and measured coverage at report time directly from enumerated requirement ids \(QA\_001\)\, ensuring the go\/no\-… | `qa-reporter` | [`agent_profiles/qa-reporter-rhea.agent.yaml`](../../../packs/qa/agent_profiles/qa-reporter-rhea.agent.yaml) |
| `qa-strategist-quinn` | qa\-strategist\-quinn | qa\-strategist\-quinn owns the strategy step of the QA lifecycle\: authoring the requirement register\, defining and freezing exit criteria\, and owning and maintaining the risk register\. qa\-strategist\-qu… | `qa-strategist` | [`agent_profiles/qa-strategist-quinn.agent.yaml`](../../../packs/qa/agent_profiles/qa-strategist-quinn.agent.yaml) |
| `qa-test-designer-tessa` | qa\-test\-designer\-tessa | qa\-test\-designer\-tessa owns the test\-design step of the QA lifecycle\: authoring test suites\, test cases\, and exploratory\-testing charters\, and linking each of them back into the requirement register… | `test-designer` | [`agent_profiles/qa-test-designer-tessa.agent.yaml`](../../../packs/qa/agent_profiles/qa-test-designer-tessa.agent.yaml) |
| `qa-test-executor-elena` | qa\-test\-executor\-elena | qa\-test\-executor\-elena owns the execution step of the QA lifecycle\: running timeboxed suites\, individual cases\, and exploratory sessions\. It records the execution\-start marker that freezes exit crite… | `test-executor` | [`agent_profiles/qa-test-executor-elena.agent.yaml`](../../../packs/qa/agent_profiles/qa-test-executor-elena.agent.yaml) |

## Glossary packs

| ID | Title | Summary | Terms | Source |
| --- | --- | --- | --- | --- |
| `qa-glossary` | qa\-glossary | Canonical ISTQB\-grounded QA vocabulary for this pack\'s tactics and procedures — the single\-mint source for terms this pack\'s shipped content cites by surface rather than re\-enumerates\, above all seve… | 19 terms | [`glossary_packs/qa-glossary.glossary-pack.yaml`](../../../packs/qa/glossary_packs/qa-glossary.glossary-pack.yaml) |

## Mission step contracts

| ID | Title | Summary | Binds | Source |
| --- | --- | --- | --- | --- |
| `qa-accept` | qa\-accept | — | mission `qa`, action `accept`, 3 steps | [`mission_step_contracts/qa-accept.step-contract.yaml`](../../../packs/qa/mission_step_contracts/qa-accept.step-contract.yaml) |
| `qa-discovery` | qa\-discovery | — | mission `qa`, action `discovery`, 3 steps | [`mission_step_contracts/qa-discovery.step-contract.yaml`](../../../packs/qa/mission_step_contracts/qa-discovery.step-contract.yaml) |
| `qa-implement` | qa\-implement | — | mission `qa`, action `implement`, 3 steps | [`mission_step_contracts/qa-implement.step-contract.yaml`](../../../packs/qa/mission_step_contracts/qa-implement.step-contract.yaml) |
| `qa-plan` | qa\-plan | — | mission `qa`, action `plan`, 4 steps | [`mission_step_contracts/qa-plan.step-contract.yaml`](../../../packs/qa/mission_step_contracts/qa-plan.step-contract.yaml) |
| `qa-review` | qa\-review | — | mission `qa`, action `review`, 3 steps | [`mission_step_contracts/qa-review.step-contract.yaml`](../../../packs/qa/mission_step_contracts/qa-review.step-contract.yaml) |
| `qa-specify` | qa\-specify | — | mission `qa`, action `specify`, 2 steps | [`mission_step_contracts/qa-specify.step-contract.yaml`](../../../packs/qa/mission_step_contracts/qa-specify.step-contract.yaml) |
| `qa-tasks` | qa\-tasks | — | mission `qa`, action `tasks`, 3 steps | [`mission_step_contracts/qa-tasks.step-contract.yaml`](../../../packs/qa/mission_step_contracts/qa-tasks.step-contract.yaml) |

## Assets

| ID | Title | MIME | Path | Executable | Descriptor |
| --- | --- | --- | --- | --- | --- |
| `qa-traceability-lint` | QA traceability carrier lint \(coverage validator\) | `text/x-python` | [`assets/qa_carrier_lint.py`](../../../packs/qa/assets/qa_carrier_lint.py) | **yes** | [`assets/qa_carrier_lint.py.asset.yaml`](../../../packs/qa/assets/qa_carrier_lint.py.asset.yaml) |
| `qa-promise-trace-lint` | QA promise trace lint \(promise \-\> scenario chain\) | `text/x-python` | [`assets/qa_promise_trace_lint.py`](../../../packs/qa/assets/qa_promise_trace_lint.py) | **yes** | [`assets/qa_promise_trace_lint.py.asset.yaml`](../../../packs/qa/assets/qa_promise_trace_lint.py.asset.yaml) |
| `qa-result-ingest` | QA result ingestion \(JUnit\-XML producer\) | `text/x-python` | [`assets/qa_result_ingest.py`](../../../packs/qa/assets/qa_result_ingest.py) | **yes** | [`assets/qa_result_ingest.py.asset.yaml`](../../../packs/qa/assets/qa_result_ingest.py.asset.yaml) |

## Mission types

| ID | Title | Summary | Actions | Source |
| --- | --- | --- | --- | --- |
| `qa` | QA | — | `discovery` → `specify` → `plan` → `tasks` → `implement` → `review` → `accept` (from [`missions/qa/mission-runtime.yaml`](../../../packs/qa/missions/qa/mission-runtime.yaml)) | [`mission_types/qa.yaml`](../../../packs/qa/mission_types/qa.yaml) |

## Missions

| ID | Name | Steps | Command templates | Templates | Source |
| --- | --- | --- | --- | --- | --- |
| `qa` | QA | `discovery` → `specify` → `plan` → `tasks` → `implement` → `review` → `accept` | 7 | 12 | [`missions/qa/`](../../../packs/qa/missions/qa/) |

## Mission steps

| Mission | Step | Title | Agent profile | Depends on | Source |
| --- | --- | --- | --- | --- | --- |
| `qa` | `accept` | Acceptance | `qa-reporter-rhea` | `review` | [`mission-steps/qa/accept/step.yaml`](../../../packs/qa/mission-steps/qa/accept/step.yaml) |
| `qa` | `discovery` | Discovery | `researcher-robbie` | — | [`mission-steps/qa/discovery/step.yaml`](../../../packs/qa/mission-steps/qa/discovery/step.yaml) |
| `qa` | `implement` | Test Execution | `qa-test-executor-elena` | `tasks` | [`mission-steps/qa/implement/step.yaml`](../../../packs/qa/mission-steps/qa/implement/step.yaml) |
| `qa` | `plan` | Test Plan | `qa-strategist-quinn` | `specify` | [`mission-steps/qa/plan/step.yaml`](../../../packs/qa/mission-steps/qa/plan/step.yaml) |
| `qa` | `review` | Test Report Review | `qa-reporter-rhea` | `implement` | [`mission-steps/qa/review/step.yaml`](../../../packs/qa/mission-steps/qa/review/step.yaml) |
| `qa` | `specify` | Test Strategy | `qa-strategist-quinn` | `discovery` | [`mission-steps/qa/specify/step.yaml`](../../../packs/qa/mission-steps/qa/specify/step.yaml) |
| `qa` | `tasks` | Test Design | `qa-test-designer-tessa` | `plan` | [`mission-steps/qa/tasks/step.yaml`](../../../packs/qa/mission-steps/qa/tasks/step.yaml) |
