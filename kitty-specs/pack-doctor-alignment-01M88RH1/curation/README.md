# Anti-pattern curation: the ledger contract

Mission `pack-doctor-alignment-01M88RH1` moves the 273 inline `anti_patterns` entries (61 files) and the 15 file-less
`anti_pattern` nodes into `anti_patterns/<id>.anti-pattern.yaml` files (#350). Judgement lives in reviewable ledgers;
`apply_curation.py` applies them mechanically. Every ledger work package (WP03-WP07) follows this contract exactly.

## Files

| File | Written in | What it holds |
|---|---|---|
| `merge-map.yaml` | WP03, before any inline-entry row | Every inline entry, clustered by meaning; each cluster's home pack and id |
| `ledger-00-nodes.yaml` | WP02 | The 15 file-less nodes |
| `ledger-a-foundation.yaml` | WP03 | Rows homed in `foundation` |
| `ledger-b-testing-writing.yaml` | WP04 | Rows homed in `testing`, `writing` |
| `ledger-c-architecture-planning.yaml` | WP05 | Rows homed in `architecture`, `event-driven`, `pack-authoring`, `planning-analysis` (and `refactoring`, `spdd`) |
| `ledger-d-language-stacks.yaml` | WP06 | Rows homed in `go`, `java`, `javascript`, `python`, `rust`, `drupal` |
| `ledger-e-internal-qa.yaml` | WP07 | Rows homed in `qa`, `internal` |
| `apply_curation.py`, `test_apply_curation.py` | WP02 | The apply and `--check`, and their tests |

The batch order is the home-pack order of the packs' `depends_on` graph, so a home file exists before any dependent
pack's `rejects` edge (decision Q1).

## The operator's decisions

Quoted from `../decisions/`. They govern every row.

- **Q1, dedupe** (`DM-01M88RHDGQSS6R5R5ZCDCH84A2`): "Merge by MEANING across packs, aiming for ~150 files. Each shared
  anti-pattern lives in ONE home pack: the most foundational pack upstream of the others, preferring one existing
  depends_on already reaches. Other packs reject it with a pack-qualified rejects edge (<pack>::anti_pattern:<id>). Add
  depends_on only where needed, never a cycle. Record every merge in the ledger (merged entries, pack of origin, chosen
  home, why). A merge whose meanings genuinely differ becomes an operator question. Batch the ledger WPs by HOME pack so
  the home file exists before any dependent pack's rejects edge."
- **Q2, severity** (`DM-01M88RHFTS2X5HK1ZNP74G3WZ7`): "approve rubric: decide each entry by the schema's definitions
  (smell is worth a remark, severe should block review, breaking must block), with a one-line grounding that quotes the
  entry or its host text, in the ledger. Batch no-signal entries to the dispatcher for the operator; never guess."
- **Q3, bad example** (`DM-01M88RHJ9HN4N8HDE97SJ6ZBAH`): "For the 131 title/content entries, the curator WRITES a short,
  concrete bad example grounded in the content. The content is the description. Each authored example is marked
  authored in the ledger (bad_example_source: authored, grounded in <content clause>). These are new doctrine, and WP
  review must read every one."

## The merge map (`merge-map.yaml`)

```yaml
clusters:
  - cluster: float-money              # the home file's id
    home_pack: foundation
    merge_reason: "both: money held in binary floating point drifts"   # the shared claim, quoted from the members
    members:                          # every inline entry in the cluster
      - {pack: go, source: styleguides/go-conventions.styleguide.yaml#/anti_patterns/0}
      - {pack: rust, source: styleguides/rust-conventions.styleguide.yaml#/anti_patterns/3}
    depends_on_added: []              # [{pack: <member pack>, depends_on: <home pack>, range: "<range>"}]
    operator_question: null
    text: null                        # set when the operator ruled authored text for the cluster (e.g. M2)
    assessment: null                  # set when a ruling asked for a recorded curation assessment (e.g. M4)
```

- One cluster per practice. A singleton cluster is a practice with one member. About 150 clusters is the expected
  count, not a quota.
- `home_pack`: the most foundational pack upstream of every member's pack, preferring one an existing `depends_on`
  already reaches.
- `depends_on_added`: only where a member's pack does not already reach the home, and never a cycle. The `range` is
  written in the form the member pack already uses for its other dependencies (dispatcher ruling, 2026-11-25); the tool
  does not choose it.
- `operator_question`, raised in one batch to the dispatcher, and never decided by the map:
  - when the members' meanings may differ;
  - when the home rule would move a stack- or domain-specific practice into a more general pack (for example go
    `float64 Money` with rust `Float Money`, whose only common upstreams are `foundation` and `testing`).
- `--check` proves that the map covers every inline-entry row exactly once, and that each row's home and id agree
  with it.

## Ledger files and rows

A ledger is `ledger-<00|a-e>-<name>.yaml` with `batch: <name>` and `entries: [rows]`. A row lives in the ledger of the
batch that owns its **home** pack: a `rust` entry merged into a `foundation` home is a row of ledger A.

| Field | Rule |
|---|---|
| `source` | `<pack-relative path>#/anti_patterns/<index>` for an inline entry (e.g. `styleguides/go-conventions.styleguide.yaml#/anti_patterns/0`); `<graph doc>#/nodes/<index>` for a file-less node |
| `source_title` | the source's `name`/`title` (or the node's `title`/`label`), verbatim; the apply refuses when the source has drifted from it |
| `pack` | the pack the source lives in (the former owner's pack) |
| `owner` | `styleguide:<id>` or `procedure:<id>`, the owner file's own `id`; null for a node |
| `home_pack` | the pack the file lives in; omitted when it is `pack`. Needed when no member of a cluster lives in its home |
| `id` | the file's id (the cluster id). On a merged row, the home row's id |
| `merged_into` | null, or `<home pack>::anti_pattern:<id>`; always pack-qualified, even within one pack |
| `merge_reason` | on a merged row: the cluster's shared claim, quoting both texts |
| `title`, `description`, `good_example` | the file's text (see the text rules); not on a merged row |
| `title_source`, `description_source` | `authored (<decision>)` where the operator ruled authored text (the drupal titles, the cross-language foundation files); omitted when the text is verbatim |
| `severity` | `smell`, `severe` or `breaking`; not on a merged row |
| `severity_grounding` | one line quoting the deciding words (Q2); not on a merged row |
| `bad_example` | the file's bad example; not on a merged row |
| `bad_example_source` | `bad_example`, `authored, grounded in <content clause>` (Q3), or `tactic <id> …` / `directive <id> …` for a file-less node; not on a merged row |
| `operator_question` | one line, answerable with a choice. The apply and `--check` refuse a row that has one |
| `also_rejects` | optional: further `<pack>::anti_pattern:<id>` targets the row's owner rejects (a split source, M4) |
| `also_rejected_by` | optional: `[{owner: <kind>:<id>, pack, reason}]`, other guidance that rejects the row's file; the target must sit in that pack's `depends_on` closure |
| `reason_update` | optional, on a non-merged row: `{from, to}`; every `rejects` edge to the file whose reason still reads `from` is rewritten to `to` (an authored-by-merge description edit, M4) |
| `merge_note` | optional: a free-text note on a row another row enhances |

A merged row's file, severity and bad example are its home row's, so it owes only its `merge_reason`. Its owner still
gets its own `rejects` edge to the home file, pack-qualified when the home is another pack.

### The id rule

- kebab-case of the title: ASCII-fold, drop punctuation, collapse hyphens;
- at most 64 characters, cut at a word boundary;
- unique among the home pack's anti-patterns. On a clash, prefer the owner's distinguishing word, and record why in
  the merge map's cluster.

### Text rules

- `title` and `description` are **verbatim** from the source: `name` or `title`, and `description` or `content`. Only
  a block scalar's trailing line break is dropped.
- Never rewrite or "improve" doctrine text. A description that needs a change for the schema gets an
  `operator_question`.
- `good_example` is verbatim, when present.
- **Merged text** (operator ruling 2026-11-25, decision `01M89KDY2KWCN62K4RD9HCRPMN`, analysis U3): a cluster's
  home file carries the verbatim text of its home-pack member, else of the earliest source in the merge map (sorted by
  pack, path, index). Its id derives from that member's title.
- **Authored text** only where the operator ruled it: the drupal titles, rephrased as anti-patterns (decision
  `01M89KEM7HW8675J5V54JPGE24`), each marked `title_source: authored` on its row.

### Severity (Q2)

- The schema's meaning: `smell` is worth a remark; `severe` should block review; `breaking` must block.
- `severity_grounding` is one line that quotes the words of the entry or its host that decide the call. Examples:
  "totals drift and equality checks fail" is a wrong result, so `breaking`; "sends the runner after stale scope"
  defeats the guidance's purpose, so `severe`; "harder to scan" is `smell`.
- Where the charter's example pack curated the same entry, cite it:
  `charter example-pack precedent: <file> severity <x>`, and say if the texts differ.
- No signal in the text is an `operator_question`, never a guess. Each WP batches its no-signal entries to the
  dispatcher for the operator.
- A grounding never says "default"; `--check` refuses one that does.

### Bad example (Q3)

- A `name`/`bad_example` entry: the source `bad_example`, verbatim, with `bad_example_source: bad_example`.
- A `title`/`content` entry: the curator writes a short, concrete instance grounded in the content, with
  `bad_example_source: authored, grounded in <content clause>`. It is new doctrine: keep it minimal and faithful to
  the content. The WP review reads every one.
- A file-less node: a concrete instance from the rejecting tactic's or directive's own text, named in
  `bad_example_source`. Where that text gives none, an `operator_question`.

### Operator questions

One line each, answerable with a choice. A WP collects its questions, and the implementer sends them to the
dispatcher in one numbered batch ("WPnn operator questions (N)"). The row keeps its `operator_question` until the
answer is applied.

## The tool

```bash
# From the repository root (or a scratch copy holding packs/):
python3 kitty-specs/pack-doctor-alignment-01M88RH1/curation/apply_curation.py [--root <dir>] [--ledger <file> ...] [--dry-run]
python3 kitty-specs/pack-doctor-alignment-01M88RH1/curation/apply_curation.py --check [--root <dir>]
python3 -m pytest kitty-specs/pack-doctor-alignment-01M88RH1/curation/test_apply_curation.py
```

Without `--ledger`, every `ledger-*.yaml` beside the script applies, sorted. `--merge-map` defaults to the
`merge-map.yaml` beside it.

**Apply**, for the given ledgers:

1. the map's `depends_on_added` for the clusters these rows belong to (refusing a cycle);
2. per row: the file in the home pack (keys in schema order, multi-line text as a literal block), its graph node, and a
   `rejects` edge from the owner (reason "the <kind> <owner-id> names this anti-pattern"), in the layout the pack
   already uses:
   - `drg/fragment.yaml`: node `{id, kind: anti_patterns, title}`; edges in the same file;
   - per-kind `*.graph.yaml`: node `{urn, kind: anti_pattern, label}` in `anti_pattern.graph.yaml` (created with
     `foundation`'s header when missing); edges in the owner kind's file;
3. each inline block is deleted textually once **every** entry of it has been applied, by any ledger beside the given
   ones. Comments and formatting elsewhere survive; a re-parse proves the rest of the document unchanged.

It refuses, writing nothing, on: an open `operator_question`; an id that is not kebab-case of at most 64 characters;
two non-merged rows with one id in one pack; a `merged_into` that resolves to no row or file; a source that does not
resolve, or whose title drifted; an owner that is not the source file's own; a cross-pack target outside the owner
pack's `depends_on` closure; a `depends_on` cycle; an empty or "default" grounding.

An inline block with an entry that no ledger covers yet is **kept**, not refused: the batches are applied one by one,
so a file's entries can be spread over several ledgers. `--check` reports the block.

A second run writes nothing.

**`--check`** exits 0 when clean, or 1 with one line per fault. It proves:

- every `anti_patterns/*.anti-pattern.yaml` has exactly one non-merged row, and every non-merged row its file, with
  field-for-field equal text;
- every file's node, and every row's `rejects` edge, exist;
- no `styleguides/**` or `procedures/**` file carries `anti_patterns`;
- no `anti_pattern` node in any graph lacks a file in its pack;
- every row's groundings (or merge reason) are present and never "default", and no row or cluster has an open
  `operator_question`;
- every `merged_into` resolves to a non-merged row, and every cross-pack target is in the owner's `depends_on` closure;
- the packs' `depends_on` graph is acyclic;
- the merge map covers every inline-entry row exactly once, and agrees with each row's home and id.
