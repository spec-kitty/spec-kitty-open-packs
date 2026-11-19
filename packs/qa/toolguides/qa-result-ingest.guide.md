# QA Result Ingestion (JUnit-XML Producer)

## Overview

`qa_result_ingest.py` is the producer, not the validator. It reads the Requirement Register in
`spec.md`, the test cases in every `tasks/WP*.md` (including `automation_ref`), and JUnit-XML
result files. It then writes or refreshes `qa-traceability.yaml` in the `qa-traceability/v1`
schema that `qa_carrier_lint.py` validates. This guide covers how to resolve the script, its
flags, its exit codes and what it writes.

## Setup

This toolguide and the script's asset sidecar share the id `qa-result-ingest`, in different kinds
(`toolguide:qa-result-ingest` and `asset:qa-result-ingest`). Resolve the script's real filesystem
path through the asset:

```
spec-kitty charter pack asset path qa-result-ingest
```

`asset path` looks up assets only, so the shared string resolves to the script, not to this
toolguide. (`toolguides/qa-carrier-lint.guide.md` carries a related caution for its own
`qa-traceability-lint` asset and `qa-carrier-lint` toolguide, whose ids differ.)

**The sidecar path has no `assets/` prefix.** The sidecar's `path:` value is
`qa_result_ingest.py`, relative to the pack's `assets/` directory. That is correct for a pack
asset. Resolve the script with `asset path` and you never need this detail.

**The script carries no shebang and is never made executable.** Invoke it with `python` in front
of the resolved path — a bare resolved-path invocation fails "Permission denied," not a Python
traceback.

## Usage

```
qa_result_ingest.py --results PATH [--results PATH ...] --strategy path/to/spec.md
                     --tasks-dir tasks/ --since TIMESTAMP --mission-dir PATH [--json]
qa_result_ingest.py --self-test
```

| Flag | Meaning |
|---|---|
| `--results PATH` | Path to a JUnit-XML result file. Repeatable — pass it once per result file when a mission run produces more than one. **Required only when at least one `tasks/WP*.md` case declares a non-empty `automation_ref` anywhere in the mission** — a legitimately exploratory/manual-only mission has none, and invokes the ingester with `--results` omitted entirely. When at least one `automation_ref` is declared and `--results` is omitted anyway, that is exit 2 (`error`): declared automated evidence with nothing supplied to correlate against is not well-formed input at all. |
| `--strategy PATH` | Path to the mission's `spec.md`, the source of the Requirement Register. Only ids of the form `FR-NNN`, `NFR-NNN` or `C-NNN` (uppercase, three digits) are read, from a table row whose first cell is the id, or a bullet of the form `- **FR-001**: ...`. Required unless `--self-test` is passed. A missing file at this path is exit 2 (`error`) — a missing Requirement Register is unusable input, never a valid empty one. |
| `--tasks-dir PATH` | Path to the mission's `tasks/` directory, whose `WP*.md` files the ingester reads. Cases come from fenced ```yaml blocks in the WP body (the `test-case-template.md` shape); case keys in the frontmatter are also read. Required unless `--self-test` is passed. |
| `--since TIMESTAMP` | The boundary a `<testsuite>` result's effective timestamp is checked against for staleness: an ISO-8601 time, normally the moment test execution started (the `review` step prompt says how to find it). A result's time comes from its `<testsuite timestamp>`, else its last git commit, else its file modification time. Required unless `--self-test` is passed. |
| `--mission-dir PATH` | The mission-dir root `qa-traceability.yaml` is written (or refreshed) into. Required unless `--self-test` is passed. |
| `--json` | Additionally echo a six-key ingestion record (`status`, `exit_code`, `carrier_path`, `requirements_total`, `cases_total`, `unmapped_testcases`) to stdout (not the carrier itself), alongside writing `qa-traceability.yaml` unconditionally to `<mission-dir>/qa-traceability.yaml` regardless of this flag. |
| `--self-test` | Runs the script's own built-in fixture/assertion pairs — one fixture that trips each named guard, one compliant fixture that does not — printing its own derived pair count (the tool derives and prints the count itself, so this guide does not restate it), mirroring `qa_carrier_lint.py --self-test`'s own convention. Makes every other flag optional — when `--self-test` is passed, none of them are read. |

## Scope: what this ingester does not read

Not ingested in v1, named explicitly rather than left as a vague "other formats": **TAP**, **TRX**
(MSTest/VSTest's own native XML schema), **Cucumber JSON**, **Robot Framework**'s native XML, and
**CTRF**. Within JUnit-XML itself, only the outcome-as-child-element dialect
(`<failure>`/`<error>`/`<skipped/>`) is supported — the outcome-as-`status`-attribute dialect some
emitters use (e.g. `<testcase status="failed">` with no `<failure>` child) is explicitly
unsupported, and is detected and refused rather than silently mis-read as passing (see Exit codes
below).

## Exit codes

| Exit code | `status` | Meaning |
|---|---|---|
| `0` | `ingested` | The carrier was produced or refreshed from real, current-run evidence; no guard fired. |
| `1` | `blocked` | A specific, named guard fired on well-formed, interpretable input, and the carrier was deliberately not written or refreshed rather than written with a hole in it — for example a supplied JUnit-XML file that parses to zero `<testcase>` elements, results considered stale against `--since`, or a WP-declared `automation_ref` that resolves to no enumerated testcase. This is a measured negative, not an error. |
| `2` | `error` | Input this tool cannot use at all: **(a)** unparseable or absent (the XML does not parse, `spec.md` does not exist, an invalid `--since`, or no `--results` despite a declared `automation_ref`); or **(b)** well-formed but not interpretable (the unsupported `status=`-attribute JUnit dialect, or two cases declaring the same `automation_ref`). |

## `qa-traceability.yaml` — the produced/refreshed carrier

Written (or refreshed) at `<mission-dir>/qa-traceability.yaml`, in the closed
`qa-traceability/v1` schema:

```yaml
schema: qa-traceability/v1
mission: <mission-directory-name>
generated_at: "2026-11-19T10:00:00+00:00"
requirements:
  - id: FR-001
    case_ids: [TC-001]
  - id: FR-002
    case_ids: []
    rationale: "no automation_ref declared or resolved for this requirement in the current run"
cases:
  - id: TC-001
    wp: WP01                                   # WP plus two digits
    type: automated
    evidence:                                  # exactly one of junit, session, ctrf
      junit:
        file: evidence/results/unit.xml        # relative to --mission-dir
        testcase: "ClassName::test_name"
defects: []                                    # entries: id, description, severity, optional case_id
```

A session-backed case carries `evidence: {session: {file: <relative path>}}` instead. The
`qa-carrier-lint` toolguide gives every rule the validator applies. What the ingester writes:

- `schema: qa-traceability/v1`, `mission` (the mission directory's name) and `generated_at`.
- One `requirements[]` entry per register id, sorted by id. `case_ids` lists the cases that
  cover it. A requirement with no covering case gets a `rationale` saying so.
- One `cases[]` entry per `automation_ref` that matched a JUnit test case: `type: automated` and
  `evidence.junit` with the result file (relative to `--mission-dir`) and the `classname::name`.
- `defects: []`.

Cases without `evidence.junit` that are already in the file (for example hand-written,
session-backed exploratory cases) are kept, and their requirement links are kept. A case with no
`automation_ref` is never guessed into an automated match. Without `--json`, the file starts
with a comment listing JUnit test cases that no `automation_ref` claimed.

## Known limitations

Nothing in the runtime runs this ingester or acts on a `blocked` or `error` exit. Run it
yourself before the carrier lint. What the runtime enforces for the `qa` steps is stated, with
its date, in the pack README under "Known limitations".
