# Data Model: Align open-packs to charter main with pack-doctor

## Anti-pattern file

The path is `packs/<pack>/anti_patterns/<id>.anti-pattern.yaml`, and the charter's
`contracts/packs/schemas/anti-pattern.schema.json` governs it.

| Field | Rule |
|---|---|
| `schema_version` | `'1.0'` |
| `id` | kebab-case, ≤64 characters, equal to the file stem, unique among the pack's anti-patterns |
| `title` | the source entry's `name` or `title`, verbatim |
| `description` | the source's `description` or `content`, verbatim (after the merge rule, when merged) |
| `severity` | `smell` \| `severe` \| `breaking`, a per-entry call with a ledger grounding, never a default |
| `bad_example` | the source's `bad_example`, or a grounded extract (see the ledger) |
| `good_example` | the source's `good_example`, when present, verbatim |

**Invariant:** the file is the only form. A graph node of the same URN declares it, and a `rejects` edge targets it.

## Graph additions (per former owner)

- **Node** (the layout the pack already uses):
  - `drg/fragment.yaml`: `{id, kind: anti_patterns, title}`.
  - `*.graph.yaml`: `{urn: anti_pattern:<id>, kind: anti_pattern, label}`, in `anti_pattern.graph.yaml`.
- **Edge:** `{source: <styleguide|procedure>:<owner-id>, target: anti_pattern:<id>, relation: rejects, reason}`.
  - The reason is "the <kind> <owner-id> names this anti-pattern", matching the charter's example pack.
  - Across packs, the target is `<pack>::anti_pattern:<id>`, and `<pack>` is in the owner's `depends_on`. This happens
    only when a merge crosses packs.

## Curation ledger row

The path is `kitty-specs/pack-doctor-alignment-01M88RH1/curation/<pack>.ledger.yaml`, with `entries: [...]`.

| Field | Meaning |
|---|---|
| `source` | `<pack-relative file>#/anti_patterns/<index>`, or `<graph doc>#/nodes/<index>` for a file-less node |
| `id` | the target file's id |
| `merged_into` | null, or the id of the row whose file this entry merges into (with the reason) |
| `title`, `description`, `good_example` | as written to the file |
| `severity` | the call |
| `severity_grounding` | one line quoting the source text (or the charter example-pack precedent) that grounds the call |
| `bad_example` | as written to the file |
| `bad_example_source` | `bad_example` (verbatim), `content` sentence N (verbatim), or `tactic <id> …` for a file-less node |
| `operator_question` | set when the row cannot be grounded. The apply refuses a row that has one until it is answered. |

**Checks (`apply_curation.py --check`):**
- every row maps to exactly one file, or merges into one;
- every file has a row;
- the row text equals the file text;
- no inline `anti_patterns` key remains;
- no row has an empty grounding or an open `operator_question`.

## Charter lock

| Key | A main pin | A release pin |
|---|---|---|
| `commit` | the charter `main` commit, 40 hex | the commit `release_tag` points at |
| `release_tag` | empty | `service-v<version>` |
| `jar_sha256` | empty | the service jar digest |
| `pack_doctor_sha256` | empty | the `pack-doctor-<version>.jar` digest (renamed from `pack_check_sha256`) |

## The gate's reading of a `PackDoctorReport`

- **Accepted top-level keys:** `tool`, `inputs`, `checks`, `packs`, `skipped`, `problems`, `summary`. Any other key
  fails closed.
- **Pass** only when every one of these holds:
  - the exit code is 0;
  - `summary.exit_code` is 0;
  - `checks` holds all of PACK, CLOSURE, REFERENCES and ROUND_TRIP;
  - `skipped` is empty;
  - `problems` is empty;
  - `packs[].name` equals the given set;
  - the only warning is `file_not_held`.
- **Fail closed** when `summary.exit_code` is not the process exit code.
- **Expectation lines:** an invalid fixture's `expected-code` line `pack-doctor: <code>` is a code with exit 1. The
  `failed` kind is retired.
