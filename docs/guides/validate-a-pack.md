---
title: Validate a pack
description: Validate a Charter Pack against the charter pack schemas, read the findings, and understand the CI gate this repository runs on every pull request.
doc_status: wip
updated: '2026-10-10'
related:
- guides/author-a-charter-pack
- guides/publish-a-pack
---
# Validate a pack

A Charter Pack is valid when every file in it matches the JSON Schema the charter assigns to
that kind of file. The schemas are owned by
[`spec-kitty-charter`](https://github.com/spec-kitty/spec-kitty-charter) (`contracts/packs/schemas/`,
mapped to files by `contracts/packs/file-kinds.yaml`). This repository validates against them
directly; it does not use the spec-kitty core CLI as its validator, and compatibility with core's
own pack validator is not a requirement.

## Run the validator

```bash
pip install pyyaml jsonschema
python3 scripts/ci/validate_pack_schemas.py ./packs/my-pack
```

The script fetches the schemas from the charter commit it pins (the `CHARTER_COMMIT` constant in
the script). Point `--contract DIR` (or `$CHARTER_CONTRACT_DIR`) at a local copy of
`contracts/packs` to work offline. Name several directories to check several packs in one run.

Exit codes:

- `0` — every pack passes.
- `1` — at least one schema violation, or a file in a retired layout. Each is printed with the
  file, the schema and the location inside the file. Fix and re-run.
- `2` — the validator cannot judge and fails closed: a schema that does not load, a file of a
  known kind with no schema mapping, or a pack with no file checked.

Each file is mapped to its schema by name: `*.directive.yaml` to the directive schema,
`pack.yaml` to the pack descriptor, `presets/<id>.yaml` to the preset schema, `*.mission-type.yaml`
to the mission-type schema, and so on. Markdown companions (`pack.md`, toolguide guides, mission
step prompts and guidelines) are read into a title, preamble and sections model and validated as
that. Assets, templates, READMEs and other files the contract lists as exclusions or payloads are
not schema-checked.

## What the schemas catch

| Condition | Result |
| --- | --- |
| A required field is missing, or a field has the wrong type or pattern (for example a lowercase directive `id`) | Violation |
| A field the schema does not define (the schemas are closed) | Violation |
| A DRG fragment with a provenance header, or an edge endpoint that is a bare id rather than `<kind>:<id>` | Violation |
| A preset in the old shape (`name`, bare id strings, `mission_type_activations`) | Violation |
| A file in a retired layout (for example `mission.yaml` beside a mission type) | Violation |

The schemas check each file on its own. They do not check that an `id` is unique across packs
or that an edge endpoint resolves to a node; check those by registering the packs in a project
and running the consumer's own tooling.

## The CI gate in this repository

Every pull request runs [`scripts/ci/validate-packs.sh`](../../scripts/ci/validate-packs.sh)
(`.github/workflows/validate-packs.yml`). It:

1. validates every pack under `packs/` (`packs/built-in` included) and `tests/fixtures/valid/`
   against the charter schemas;
2. checks that every pack under `tests/fixtures/invalid/` **fails** schema validation, so a
   validator that passes everything turns the job red.

[`scripts/ci/check-built-in.sh`](../../scripts/ci/check-built-in.sh) checks that the tree digest of
`packs/built-in` matches `packs/built-in.source.yaml`. The vocabulary guard and the release and
vocabulary tests run even when validation fails, so one run shows all the red.

To move to newer schemas, change `CHARTER_COMMIT` in `scripts/ci/validate_pack_schemas.py` to a
full commit SHA of `spec-kitty-charter`. The current pin is a commit of the open
mission-type-consolidation branch (charter PR #275); move it to a `main` commit once that merges.

Run it locally before opening a PR:

```bash
scripts/ci/validate-packs.sh
```

## Next

- [Publish a pack](publish-a-pack.md)
