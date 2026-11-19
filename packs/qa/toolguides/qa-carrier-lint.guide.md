# QA Traceability Carrier Lint (Coverage Validator)

## Overview

`qa_carrier_lint.py` validates a `qa-traceability/v1` carrier (`qa-traceability.yaml`) and
computes `qa-coverage.json`, this pack's machine-readable coverage record. This guide covers how
to resolve the script, its flags, its exit codes, the carrier schema it checks and the record it
writes.

## Setup

Two different ids are in play here and they are not interchangeable:

- **This toolguide's own id is `qa-carrier-lint`.** It is not a resolvable asset id — it names
  this toolguide document, nothing else.
- **The script ships as an asset sidecar whose own id is the different string
  `qa-traceability-lint`.** Resolve the script's real filesystem path with:

  ```
  spec-kitty charter pack asset path qa-traceability-lint
  ```

  Never pass this toolguide's own id (`qa-carrier-lint`) to `asset path` — it will not resolve,
  because it is not an asset id.

**The sidecar path has no `assets/` prefix.** The sidecar's `path:` value is
`qa_carrier_lint.py`, relative to the pack's `assets/` directory. That is correct for a pack
asset; do not add an `assets/` prefix. Resolve the script with `asset path` and you never need
this detail.

## Usage

```
qa_carrier_lint.py --carrier PATH --mission-dir PATH [--json]
qa_carrier_lint.py --self-test
```

| Flag | Meaning |
|---|---|
| `--carrier PATH` | Path to `qa-traceability.yaml`, the carrier to validate. Required unless `--self-test` is passed. |
| `--mission-dir PATH` | The mission-dir root that evidence paths (JUnit-XML files, `*.session.yaml` files) resolve under, and the directory `qa-coverage.json` is written into. Required unless `--self-test` is passed. |
| `--json` | Additionally echo the identical `qa-coverage.json` structure to stdout. `qa-coverage.json` is written to `<mission-dir>/qa-coverage.json` unconditionally on every run regardless of this flag — `--json` only adds the stdout echo, it does not gate whether the file itself is written. |
| `--self-test` | Runs the script's built-in fixture/assertion pairs (the tool prints the count) and exits `0` only if every pair passes. Makes `--carrier`/`--mission-dir` optional — when `--self-test` is passed neither is read. |

Invoking the script with neither `--self-test` nor both of `--carrier`/`--mission-dir` is itself
an error: it prints a usage message to stderr and exits `2`.

## Exit codes

| Exit code | `status` | Meaning |
|---|---|---|
| `0` | `measured`, `verdict: ready` | Every requirement with non-empty `case_ids` has every referenced case's evidence resolved to a passing outcome, and the bridge check (below) found no violation. |
| `1` | `measured`, `verdict: blocked` | The carrier is well-formed and every reference resolves, but at least one requirement's covering evidence did not resolve to a passing outcome, or `requirements_uncovered` is non-empty. This is a measured **negative**, not an error. |
| `2` | `not_measured` (carrier absent) **or** `error` (carrier present but malformed) | The two `2`-exit states are distinguished by `qa-coverage.json`'s own `status` field, never conflated. `not_measured` means no carrier file was found at `--carrier`'s path. `error` means a carrier file was found but is invalid: a schema-version mismatch, an unrecognised top-level/entry/evidence key (a closed-schema violation), non-zero `results_missing`, or a non-empty `bridge_violations` / `duplicate_case_ids` / `dangling_case_refs` / `evidence_unparseable` list. Any one of these conditions alone forces `error`; more than one may fire on the same run. |

## The `qa-traceability/v1` carrier

`qa-traceability.yaml` sits at the mission-dir root. `qa-result-ingest` writes it; you may also
write cases by hand (for example session-backed exploratory cases), and the ingester keeps them.
The schema is closed: an unknown key at any level is an `error`.

```yaml
schema: qa-traceability/v1          # exact string; another qa-traceability/* version is an error
mission: <mission-slug>
generated_at: "2026-11-19T10:00:00+00:00"
requirements:
  - id: FR-001                      # required
    case_ids: [TC-001, TC-002]      # required; may be [] only with a non-empty rationale
    rationale: "Why no case covers this."   # optional otherwise
cases:
  - id: TC-001                      # all four keys required
    wp: WP01                        # exactly WP plus two digits; the bridge check reads tasks/WP01*.md
    type: automated                 # free text; the ingester writes automated
    evidence:                       # exactly one of junit, session, ctrf
      junit:
        file: evidence/results/unit.xml     # relative, inside --mission-dir
        testcase: "ClassName::test_name"    # JUnit classname::name
  - id: TC-002
    wp: WP02
    type: exploratory
    evidence:
      session:
        file: evidence/sessions/login.session.yaml   # relative, inside --mission-dir
defects:
  - id: D-001                       # required
    description: "Login fails after password reset."   # required
    severity: high                  # required
    case_id: TC-002                 # optional
```

All six top-level keys are required. `requirements`, `cases` and `defects` are lists (an empty
list is allowed). `evidence.ctrf` is reserved: it takes no keys and is always scored
`not_measured`.

A session evidence file is a YAML mapping with all of `charter`, `timebox_minutes`, `overrun`,
`areas`, `bugs_found`, `bug_ids`, `status` and `debrief`. `status` is `completed` or `aborted`.
`overrun` must be a real boolean; a string or number is an `error`.

Cross-checks:

- A case id may appear only once in `cases` (`duplicate_case_ids`).
- Every id in a requirement's `case_ids` must exist in `cases` (`dangling_case_refs`).
- **Bridge check:** for every case covering a requirement, the work package named in `wp` must
  list that requirement id in its frontmatter `requirement_refs`. A WP file that is not on disk
  yet is reported in `bridge_not_measured`, which is not an error.

## `qa-coverage.json` — the computed-output record

Written unconditionally to `<mission-dir>/qa-coverage.json` on every run; `--json` only
additionally echoes the identical structure to stdout. Its fields:

- **Identity and outcome**: `schema` (`"qa-coverage/v1"`), `status`
  (`measured`/`not_measured`/`error`), `verdict` (`ready`/`blocked`, populated only when
  `status == measured`), `reason` (populated only when `status` is `not_measured`/`error`).
- **Requirement coverage**: `requirements_total`, `requirements_covered` (a count),
  `requirements_uncovered` (a list of requirement ids with empty `case_ids`, each with its own
  rationale in `reasons`), `requirements_blocked` (a list of requirement ids whose `case_ids` are
  non-empty but did not resolve to a fully-passing outcome — the state distinct from both
  "covered" and "uncovered").
- **Case/evidence resolution**: `cases_total`, `results_parsed` (cases whose evidence actually
  resolved and was classified), `passed`, `failed`, `skipped`, `overrun` (JUnit-XML and
  session-evidence outcome buckets — see below), `results_missing` (a JUnit-XML `testcase`
  reference that did not match any `<testcase>` in its named file — forces `status: error`),
  `evidence_unparseable` (a list of `{case_id, file, evidence_kind, reason}` objects for evidence
  files that exist but fail to parse — forces `status: error`), `evidence_file_missing` (a count
  of evidence files that simply do not exist yet on disk — a benign, non-error state, never
  forcing `status: error`).
- **Referential-integrity errors**: `duplicate_case_ids` (a list of `{id, count}` objects — forces
  `status: error`), `dangling_case_refs` (a list of `{requirement_id, case_id}` objects for a
  `requirements[].case_ids` entry with no matching `cases[].id` — forces `status: error`).
- **Bookkeeping**: `defects_total`, `reasons` (an id-keyed map carrying every
  `requirements_uncovered` rationale plus every `results_missing` resolution-failure detail, plus
  the top-level `reason` duplicated under `_carrier` when `status != measured`).
- **Bridge check**: `bridge_violations` (a list of `{requirement_id, case_id, wp_file}`
  objects — a requirement whose covering `tasks/WP*.md` file(s) do not list that requirement id;
  forces `status: error`), `bridge_not_measured` (a list of `{requirement_id, case_id, wp_file,
  reason}` objects for a covering WP file that does not exist on disk yet — a normal authoring
  state, never forcing `status: error`).
- **CTRF (reserved, not implemented)**: `ctrf_pending`, a list of `{case_id, reason}` objects for
  every case using the reserved `evidence.ctrf` key; each is individually `not_measured`, with
  `reason` always the fixed string `"CTRF not implemented in v1"`.

**JUnit-XML and session-evidence classification, briefly**: a JUnit-XML outcome classifies as
`passed`, `failed` (failure and error folded into one bucket), or `skipped` — `skipped` is never
folded into `passed`. A session-typed case (`*.session.yaml` evidence) counts as `passed` only
when `status: completed` **and** `overrun: false`; `status: completed` with `overrun: true` counts
in its own dedicated `overrun` bucket, never `passed` or `failed`; `status: aborted` counts as
`failed`.

## Known limitations

Nothing in the runtime runs this validator or acts on its verdict. Run it yourself and treat its
verdict as binding. What the runtime enforces for the `qa` steps is stated, with its date, in
the pack README under "Known limitations".
