---
title: Validate a pack
description: Validate a Charter Pack against the charter pack schemas and the charter service, read the findings, and understand the CI gate this repository runs on every pull request.
doc_status: wip
updated: '2026-11-11'
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

The script fetches the schemas from the charter commit it pins (`commit` in
[`charter.lock.yaml`](../../charter.lock.yaml), see [The charter pin](#the-charter-pin)). Point `--contract DIR` (or `$CHARTER_CONTRACT_DIR`) at a local copy of
`contracts/packs` to work offline. Name several directories to check several packs in one run.

Exit codes:

- `0` — every pack passes.
- `1` — at least one schema violation, a file in a retired layout, a file no rule models
  (`unmodelled`), or Markdown the charter would not hold outside the allowlist (`not_held`). Each is
  printed with the file, and a schema violation with the schema and the location inside the file.
  Fix and re-run.
- `2` — the validator cannot judge and fails closed: a schema that does not load, a file of a
  known kind with no schema mapping, or a pack with no file checked.

Each file is mapped to its schema by name: `*.directive.yaml` to the directive schema,
`pack.yaml` to the pack descriptor, `presets/<id>.yaml` to the preset schema, `*.mission-type.yaml`
to the mission-type schema, and so on. Markdown files (the pack document `README.md`, toolguide guides, mission
step prompts and guidelines) are read into a title, preamble and sections model and validated as
that. Assets, templates, other READMEs (a mission template's or an asset's notes) and other files the contract lists as exclusions or payloads are
not schema-checked.

The validator classifies a file as the charter at the pin does (`file-kinds.yaml`): the `files`,
`exclusions`, `retired` and `payloads` rules first; then a root file that differs only in letter case
from a ruled root file (`Readme.md`, `PROVENANCE.MD`, `Pack.yaml`), refused as `retired` under the rule it
shadows; last the `ignored` rule, which takes Markdown nothing else models, in any letter case. The charter
leaves an ignored file out without refusing it, and a registration reports it as `file_not_held`. This
repository allows only orientation notes (a `README.md` at any depth) and `*.skill.md` skill bodies to be
carried that way: any other ignored file (a stray `docs/notes.md`, a guide or prompt in the wrong place)
fails as `not_held`. A file no rule takes at all (a `.txt` or `.json` beside the artifacts, a misspelt
artifact name) fails as `unmodelled`, as the charter refuses it at registration. Both checks run on
every pack, built-in-level ones included, which no registration sees.

## What the schemas catch

| Condition | Result |
| --- | --- |
| A required field is missing, or a field has the wrong type or pattern (for example a lowercase directive `id`) | Violation |
| A field the schema does not define (the schemas are closed) | Violation |
| A DRG fragment with a provenance header, or an edge endpoint that is a bare id rather than `<kind>:<id>` | Violation |
| A preset in the old shape (`name`, bare id strings, `mission_type_activations`) | Violation |
| A file in a retired layout (for example `mission.yaml` beside a mission type), or a root case variant of a ruled file (`Readme.md`) | Violation |
| A file no rule models (`notes.txt`, `x.tactic.yml`) | Violation (`unmodelled`) |
| Markdown only the `ignored` rule takes, other than a `README.md` or a `*.skill.md` | Violation (`not_held`) |

The schemas check each file on its own. Composition and registration, which look at packs
together, are the charter service's to judge: see [The charter service job](#the-charter-service-job).

## The CI gate in this repository

Every pull request runs two jobs of `.github/workflows/validate-packs.yml`, and the one required
check, `Validate packs gate`, needs both.

**`Charter Pack validation`** is the fast pre-check. It runs
[`scripts/ci/validate-packs.sh`](../../scripts/ci/validate-packs.sh), which:

1. validates every pack under `packs/` (`packs/built-in` included) and `tests/fixtures/valid/`
   against the charter schemas, and checks that every asset sidecar names, by a `path` relative to
   `assets/`, a payload the pack holds;
2. checks that every pack under `tests/fixtures/invalid/` **fails** schema validation, so a
   validator that passes everything turns the job red (a fixture marked `precheck: accepted` in its
   `expected-code` file is well formed file by file, so it must pass here and is refused by the
   service instead);
3. checks the packs together for what the charter service does not (see
   [What the service owns and what stays here](#what-the-service-owns-and-what-stays-here)).

The vocabulary guard and the release and vocabulary tests run even when validation fails, so one
run shows all the red.

### Recorded pack digests

Every pack records a digest of its own files, so no pack content changes unnoticed. The digest
covers every file in the pack directory except the root `pack-manifest.yaml`, and is recorded in
`packs/<name>.source.yaml`, beside the directory and outside what it hashes. A pack with a
`pack.yaml` and no sidecar fails, as does a stale sidecar or a sidecar with no pack.

- After editing a pack, run `python3 scripts/ci/pack_digest.py --update` and commit the changed
  sidecar. It restamps stale sidecars, creates missing ones and leaves a fresh one untouched. The
  script needs pyyaml: `pip install pyyaml`, or `uv run --with pyyaml python3 scripts/ci/pack_digest.py --update`.
  Only git-tracked files count, so `git add` a new file first; untracked and ignored files never
  change the digest.
- To run what CI runs, use
  [`scripts/ci/check-pack-digests.sh`](../../scripts/ci/check-pack-digests.sh), which calls
  [`pack_digest.py --check`](../../scripts/ci/pack_digest.py).

Three digests are not interchangeable. The sidecar's `tree_digest.value` is the snapshot with
`pack-manifest.yaml` excluded. A core pin's `tree_digest.value` is the clean-tree-sha256, and a core
pin's `snapshot_sha256` includes the manifest. Never copy one into the other's place.

A pack that ships a `pack-manifest.yaml` must also list every graph node it declares as a
constituent, except actions, anti-patterns, templates, mission types and step contracts. To exempt a
new node kind, add it to `MANIFEST_EXEMPT_NODE_KINDS` in
[`validate_pack_schemas.py`](../../scripts/ci/validate_pack_schemas.py); a kind in neither place fails.

## The charter service job

**`Charter service validation`** asks the charter service itself (charter
[ADR-0070](https://github.com/spec-kitty/spec-kitty-charter/blob/main/docs/adr/0070-charter-tests-own-example-packs-not-open-packs-content.md):
the charter no longer tests this repository's content, so this repository proves its own packs
valid through the service, at a pinned charter version). The job:

1. reads the pin, and obtains the service: the release jar `spec-kitty-charter-service-<version>.jar`
   with its SHA-256 checked when the pin names a `service-v*` release, otherwise the pinned commit
   built with `./gradlew :deployable:bootJar` (Java 25);
2. **composes**: starts the service over a configuration root holding every pack of `packs/` and
   `tests/fixtures/valid/` as `<root>/packs/<directory name>/`, at the level its own `pack.yaml`
   declares (`pack_level`; there is no other configuration), and calls `GET /api/v1/offering`. It must
   answer 200 and name every pack at its level with every `depends_on` resolved. A refusal
   (`pack_unreadable` or a composition code) fails the job and prints the problem document;
3. **registers**: on a scratch root holding only the built-in-level packs (`built-in`, `foundation`, `writing`; they are read-only to registration,
   charter ADR-0065), sends each org and project pack whole with `PUT /api/v1/packs/{packId}`,
   dependencies first, and polls `GET /api/v1/pack-registrations/{id}` until it ends. A `refused`
   registration fails the job and prints its problem and violations. The whole tree is uploaded
   (less a fixture's `expected-code`). A registration holds only files the service models: a retired
   file (`pack.md`, `PROVENANCE.md`, `org-charter.yaml`, or a root case variant of a ruled file) is
   refused as `retired`, any other file the service does not model is refused as `unmodelled`, and a
   file an exclusion or the `ignored` rule takes is left out and reported as a `file_not_held`
   diagnostic. Every diagnostic of a succeeded registration is printed as a notice, and a
   `file_not_held` file other than a `README.md`, a hidden file or a mission template's
   `plan-field-declaration.yaml` fails the job;
4. **proves it is not vacuous**: every pack under `tests/fixtures/invalid/` must be refused with the code
   its `expected-code` file names, once when composed and once when registered. A fixture the service
   accepts, or refuses with another code, fails the job.

The `expected-code` file of a fixture holds `key: value` lines:

```text
composition: pack_unreadable      # the code of the refusal of GET /offering
registration: validation_failed   # the code of the refused registration's problem
precheck: accepted                # optional: the schema pre-check cannot see this refusal
```

`legacy-shapes` holds 3.x-era files and is refused as unreadable and invalid;
`unknown-dependency` is well formed and refused only for composing with a pack nobody configured.

Run it locally, with the jar of the pin (Java 25 on the `PATH` or in `JAVA_HOME`):

```bash
jar="$(scripts/ci/charter_service_jar.sh /tmp/charter-service)"
python3 scripts/ci/charter_service_check.py --jar "$jar"
```

`charter_service_check.py` takes any service jar, so a jar you built from a charter branch tells you
whether a pending charter change would break these packs. It exits `0` when everything passed, `1` when a
check failed and `2` when it could not run.

### What the service owns and what stays here

The Python composition rules this repository used to run under `--cross-pack` were each tried against
the service with a deliberately broken scratch pack. The service refuses these, so they are no longer
judged by the validator:

| Rule (was `--cross-pack`) | The service refuses it as |
| --- | --- |
| A pack with no `pack.yaml` | `pack_unreadable` |
| A shared `pack_id` / a shared `name` | `pack_duplicate_id` / `pack_name_conflict` |
| A `depends_on` naming no pack | `pack_dependency_unknown` |
| A `depends_on` cycle | `pack_dependency_cycle` |
| An edge joining a node to itself | `pack_unreadable` |
| A bare edge end held only by another pack | `pack_reference_unqualified` |
| A qualifier outside the pack's `depends_on` closure | `pack_reference_pack_missing` |
| A qualified edge end the named pack does not hold | `pack_reference_artifact_missing` |
| The same id declared by two packs of one level | `pack_sibling_conflict` |
| An enhancement without exactly one `enhances` edge, or one whose target is not `action:<type>/<step>` | `pack_unreadable` (`validation_failed` at registration) |

The service accepts these, at composition and at registration, so `--cross-pack` still judges them:

- a preset naming an id no pack declares, or a `must_have: true` item that no pack in the preset
  pack's `depends_on` closure declares;
- a bare DRG edge end that resolves to no node of any pack;
- an id re-declared by a pack of another level (the service takes it as a layer override; this
  repository does not allow it);
- an agent-profile reference (`directive-`, `tactic-`, `styleguide-` and `toolguide-references`,
  `operating-procedures`) that is bare but held by another pack or by none, qualified with the profile's
  own pack, outside its `depends_on` closure, or not held by the named pack;
- a prompt fragment whose `enhances` target step does not exist, or whose slot the step's prompt does
  not declare.

## The charter pin

[`charter.lock.yaml`](../../charter.lock.yaml) is the one pin of the charter. The schema validator and
the service job both read it, so the schemas and the service always come from the same charter:

```yaml
commit: f4acac975522e4bf8d423d552672f9d1d78e8186   # 40 lowercase hex characters; never a branch or a tag
release_tag:                                        # service-vX.Y.Z once the charter publishes a release; empty until then
jar_sha256:                                         # the release jar's SHA-256; required with release_tag
```

Both scripts fail closed on anything but a full commit. With `release_tag` empty (no `service-v*`
release exists yet) the job builds the service from `commit`; once a release exists, set `release_tag` and
`jar_sha256` and the job downloads that jar and refuses any other digest. To move to newer schemas
and a newer service, change `commit` to a full commit SHA of `spec-kitty-charter`'s `main` branch in the
pull request that migrates the packs to what changed.

Run it locally before opening a PR:

```bash
scripts/ci/validate-packs.sh
```

## Next

- [Publish a pack](publish-a-pack.md)
