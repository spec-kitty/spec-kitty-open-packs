---
title: Validate a pack
description: Validate a Charter Pack against the charter pack schemas, the charter's pack-doctor and the charter service, read the findings, and understand the CI gate this repository runs on every pull request.
doc_status: wip
updated: '2026-11-28'
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
- `1` — at least one schema violation or a file in a retired layout. Each is
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
leaves an ignored file out without refusing it, and a registration reports it as `file_not_held`.
Operator ruling R34 (#331) lets authors keep notes and logs in a pack, so a stray file never fails here:
- orientation notes (a `README.md` at any depth) are carried silently;
- any other ignored file (a stray `docs/notes.md`, a guide or prompt in the wrong place, a skill body no
  skill's `body_path` names) is warned as `file_not_held`;
- a file no rule takes at all (a `.txt` or `.json` beside the artifacts, a misspelt artifact name, a shard
  below the pack root, a `charter.yaml`) is warned as `file_not_held` too, as the charter does (charter #554,
  ruling Q1).

**Misspelled companions (R38).** The schema pass lints companion names. Each finding is a PR annotation on the
file itself, never a failure:
- **Missing companion**, on an artifact whose `*_path` key (`prompt_path`, `guide_path`, `body_path`) names a
  file the pack lacks, read from the artifact's directory or, as a DRG node's `body_path` is, from the pack root.
  This also catches a stem typo whose name still matches a rule (`implemnet.prompt.md`).
- **Possible misspelled companion**, on a stray file with the companion it was probably meant to be:
  - a file beside such a missing companion with a similar name (`implement.promt.md` beside a missing
    `implement.prompt.md`);
  - otherwise, a file whose suffix is close to a companion suffix the contract models (`.guide.md`,
    `.prompt.md`, `.guidelines.md`, `.prompt-fragment.md`, or `.skill.md` for skill bodies). A suffix of five
    letters or fewer may differ by one inserted, dropped or swapped letter (`.gudie.md`, `.skil.md`), a
    six-to-nine-letter one by one edit (`.promt.md`), a longer one by two. So ordinary words such as
    `still.md` or `slide.md` are not flagged.

A reference that cannot be resolved (an overlong name, a NUL byte) is not judged by the lint.

A misnamed companion does not slip through: pack-doctor still refuses the pack, because the companion its
artifact names is missing (`<ref>: missing`, e.g. `steps/implement.prompt.md: missing`). Only a stray file that
nothing names is left as a warning.

A file a skill's `body_path` names is held as that skill's companion, whatever its name. pack-doctor warns on
the same stray files, as `file_not_held`, and its round trip leaves them out, so they never fail the gate. The
checks run on every pack, built-in-level ones included, which no registration sees.

## What the schemas catch

| Condition | Result |
| --- | --- |
| A required field is missing, or a field has the wrong type or pattern (for example a lowercase directive `id`) | Violation |
| A field the schema does not define (the schemas are closed), such as an `anti_patterns` list in a styleguide or a procedure | Violation |
| A DRG fragment with a provenance header, or an edge endpoint that is a bare id rather than `<kind>:<id>` | Violation |
| A preset in the old shape (`name`, bare id strings, `mission_type_activations`) | Violation |
| A file in a retired layout (for example `mission.yaml` beside a mission type), or a root case variant of a ruled file (`Readme.md`) | Violation |
| A file no rule models (`notes.txt`, `x.tactic.yml`, `drg/tactic.graph.yaml`) | Warning (`file_not_held`), not held |
| Markdown only the `ignored` rule takes, other than a `README.md` (an orphan skill body included) | Warning (`file_not_held`), not held (R34, #331) |

The schemas check each file on its own. The checks that look at packs together are the charter's:
pack-doctor and the charter service judge them, see [The charter service job](#the-charter-service-job).

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
3. checks the packs together for the house rules, what the charter does not judge by ruling (see
   [The house rules](#the-house-rules)).

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

### Pack manifests

Every pack, and every valid fixture, carries the `pack-manifest.yaml` the charter derives (#255; charter
ADR-0042 as amended 2026-11-12). Its lists come from the pack itself, never from an author:
- one constituent for each artifact file the pack holds, with its kind, id and path (an anti-pattern file
  included);
- one entry for each `presets/<id>.yaml`.

Both lists are in path order, and the hashes are stamped from the files. pack-doctor judges the manifest
(#347): a manifest with any other lists is `manifest_membership`, and a `content_hash` or `manifest_hash`
that does not match the pack's bytes is `manifest_stale`, one violation per field. The schema pass derives,
restamps and verifies no manifest.

After adding, removing, renaming or editing an artifact or a preset, restamp the manifests with the
pinned charter's `pack-doctor remediate`. The easiest way is to re-apply the pin you already have:

```bash
python3 scripts/ci/charter_pin.py apply \
  --commit "$(python3 scripts/ci/charter_lock.py commit)" \
  --release-tag "$(python3 scripts/ci/charter_lock.py release_tag)" \
  --jar-sha256 "$(python3 scripts/ci/charter_lock.py jar_sha256)" \
  --pack-doctor-sha256 "$(python3 scripts/ci/charter_lock.py pack_doctor_sha256)"
```

This leaves the lock's values as they are. It gets the jar of the pin with
[`charter_pack_doctor_jar.sh`](../../scripts/ci/charter_pack_doctor_jar.sh) (Java 25; on a `main` pin it builds
the jar, so it also needs github.com and the Gradle repositories). It then runs `remediate` once over every pack
and valid fixture, from the repository root, and restamps the digests (`pack_digest.py --update`) and the pack
pages. It exits non-zero when `remediate` refuses a pack or leaves the tree red, and prints the command that
restores the tree.

`remediate` does more than stamp the manifest: it rewrites every file the charter models in the round trip's
canonical form. The meaning stays the same, but comments, quoting, key order and line folding may change
(charter ADR-0036). A comment in a modelled file, a `pack.yaml` included, does not survive a restamp (operator
ruling `01M8A5ZNJTETCBFCC4H5G0VHQ6`). Files the charter does not hold are left as they are. What `remediate`
repairs and refuses is in the charter's guide,
[Check packs](https://github.com/spec-kitty/spec-kitty-charter/blob/main/docs/guides/check-packs.md#repair-a-pack).

The schema pass keeps one manifest check of its own, a house rule (#182; decision `01M8BMA8KVQH0CXKAT05RW7Z9X`):
a graph node that no file of the pack declares must still be listed as a constituent. `manifest_membership`
derives its lists from the files, so it does not see such a node. Actions, templates and mission types are
exempt (`MANIFEST_EXEMPT_NODE_KINDS` in
[`validate_pack_schemas.py`](../../scripts/ci/validate_pack_schemas.py)); a node kind the script does not know
fails closed.

## The charter service job

**`Charter service validation`** asks the charter service itself (charter
[ADR-0070](https://github.com/spec-kitty/spec-kitty-charter/blob/main/docs/adr/0070-charter-tests-own-example-packs-not-open-packs-content.md):
the charter no longer tests this repository's content, so this repository proves its own packs
valid through the service, at a pinned charter version). The job:

1. reads the pin, and obtains the service: the release jar `spec-kitty-charter-service-<version>.jar`
   with its SHA-256 checked when the pin names a `service-v*` release, otherwise the pinned commit
   built with `./gradlew :deployable:bootJar` (Java 25);
2. **gates every pack on the charter's pack-doctor** (#252, #345; charter ADR-0075 decision 9, ADR-0083,
   ADR-0070 decision 4 as amended 2026-11-13). pack-doctor is the charter's own whole-pack check, a CLI over
   the same validation a registration runs. The gate runs `pack-doctor validate --round-trip --full`, which
   runs four checks: each pack (`PACK`), the closure of the set with its presets (`CLOSURE`), each pack's
   substep delegations, references and step enhancements' targets over its `depends_on` closure
   (`REFERENCES`), and the round trip through the charter's model, compared by meaning (`ROUND_TRIP`). What
   each check judges, the report and the exit codes are in the charter's guide,
   [Check packs](https://github.com/spec-kitty/spec-kitty-charter/blob/main/docs/guides/check-packs.md).
   - **The jar.** [`charter_pack_doctor_jar.sh`](../../scripts/ci/charter_pack_doctor_jar.sh) gets the jar of
     the pin. On a release pin, it checks that the tag points at the lock's `commit`, downloads
     `pack-doctor-<version>.jar` from the pinned release, and refuses any digest but `pack_doctor_sha256`. On a
     `main` pin, the pin today, it fetches `commit` and builds the jar with `./gradlew :pack-doctor:packDoctorJar`
     (Java 25). Both release jars, this one and the service jar, pass the same two checks
     ([`charter_release_asset.sh`](../../scripts/ci/charter_release_asset.sh)): the tag must point at `commit`,
     and the download goes to `<jar>.part`, which takes the jar's name only once its digest matches. A failed,
     partial or mismatched download leaves nothing behind. Getting the jar and running it are one step, so a
     jar that cannot be had fails the gate.
   - **The run.** [`charter_pack_doctor.py`](../../scripts/ci/charter_pack_doctor.py) runs it over every pack
     and valid fixture together, one `--pack <dir>` each, built-in-level ones included, under
     `LC_ALL=C.UTF-8`. The JSON on standard output, the `PackDoctorReport`, is what the gate reads.
   - **What fails the job:**
     - any exit but 0, **exit 2 included**: exit 2 is a usage fault or a failure outside a pack read, and
       nothing was judged. That is a failure, never a skip;
     - a problem in the report;
     - a check that was skipped or did not run: all four must run;
     - a warning other than `file_not_held`, or a warning line it cannot read. `file_not_held` is printed as
       a notice: a stray file warns, never fails (R34, #331);
     - a report it cannot read as this run's `PackDoctorReport`: a top-level key besides `tool`, `inputs`,
       `checks`, `packs`, `skipped`, `problems` and `summary`, a `tool.name` other than `pack-doctor`, options
       that do not record `--full` and `--round-trip`, or a `summary.exit_code` that is not the run's own;
     - a pack left out of the verdict, or reported twice.
   - **The pin's own answers.** The same step then runs `tests.ci.test_charter_pack_doctor.RealPackDoctor`
     against the jar: the invalid fixtures, this checkout's packs, and scratch packs that pin what the jar
     judges and what it leaves to this repository (see
     [What pack-doctor covers and what stays here](#what-pack-doctor-covers-and-what-stays-here)).
   - **The report.** Each run's `--report` file and its standard error are uploaded as the
     `charter-pack-doctor-report` artifact. No registration sees a built-in-level pack, so this is the only
     check of their manifests that the charter itself makes.
   - **It replaced** the charter's `driftTest`, which the job used to build from the pinned source: the same
     round trip under the same rule.
3. **composes**: starts the service over a configuration root holding every pack of `packs/` and
   `tests/fixtures/valid/` as `<root>/packs/<directory name>/`, at the level its own `pack.yaml`
   declares (`pack_level`; there is no other configuration), and calls `GET /api/v1/offering`. It must
   answer 200 and name every pack at its level with every `depends_on` resolved. A refusal
   (`pack_unreadable` or a composition code) fails the job and prints the problem document;
4. **registers**: on a scratch root holding only the built-in-level packs (`built-in`, `foundation`, `writing`; they are read-only to registration,
   charter ADR-0065), sends each org and project pack whole with `PUT /api/v1/packs/{packId}`,
   dependencies first, and polls `GET /api/v1/pack-registrations/{id}` until it ends. A `refused`
   registration fails the job and prints its problem and violations. The whole tree is uploaded
   (less a fixture's `expected-code`). A registration holds only files the service models: a retired
   file (`pack.md`, `PROVENANCE.md`, `org-charter.yaml`, or a root case variant of a ruled file) is
   refused as `retired`, any other file the service does not model is warned as `file_not_held` and
   left out (charter #554, ruling Q1), and a file an exclusion or the `ignored` rule takes is left out and reported as a `file_not_held`
   diagnostic. Every diagnostic of a succeeded registration is printed as a notice. Each
   `file_not_held` file is classified with the schema validator's mirror of the pinned contract: a file the
   mirror also leaves out (excluded, ignored or unmodelled) stays a notice, as R34 (#331) asks; a file the
   mirror classifies as held content fails the job, because the mirror has drifted from the pin;
5. **proves it is not vacuous**: every pack under `tests/fixtures/invalid/` must be refused with the code
   its `expected-code` file names, once when composed and once when registered, and by pack-doctor. pack-doctor
   checks each fixture alone, from a copy without its `expected-code` (it models no such file), and must exit 1
   with the code in a problem or one of its violations. A fixture accepted, or refused with another code, fails
   the job.

The `expected-code` file of a fixture holds `key: value` lines:

```text
composition: pack_unreadable      # the code of the refusal of GET /offering
registration: validation_failed   # the code of the refused registration's problem
precheck: accepted                # optional: the schema pre-check cannot see this refusal
pack-doctor: case_variant         # a code pack-doctor's report must carry, in a problem or a violation
```

`legacy-shapes` holds 3.x-era files and is refused as unreadable and invalid;
`unknown-dependency` is well formed and refused only for composing with a pack nobody configured.
`malformed-pack-version` is the valid example pack with a `pack_version` that is not a version. The schema
pass accepts it, and the service and pack-doctor refuse it (`pack_version_invalid`).

Run it locally, with the jar of the pin (Java 25 on the `PATH` or in `JAVA_HOME`):

```bash
jar="$(scripts/ci/charter_service_jar.sh /tmp/charter-service)"
python3 scripts/ci/charter_service_check.py --jar "$jar"
```

and pack-doctor, at the pin (Java 25):

```bash
jar="$(scripts/ci/charter_pack_doctor_jar.sh /tmp/charter-service)"
python3 scripts/ci/charter_pack_doctor.py --jar "$jar"
```

`charter_service_check.py` takes any service jar, so a jar you built from a charter branch tells you
whether a pending charter change would break these packs. It exits `0` when everything passed, `1` when a
check failed and `2` when it could not run. `charter_pack_doctor.py` exits the same way; add
`--report-dir DIR` to keep each run's report and standard error.

### What pack-doctor covers and what stays here

<a id="what-pack-check-covers-and-what-stays-here"></a>

Each schema-pass rule that #348 maps to pack-doctor, and each one kept beside them, was tried against the jar
of the pin with a scratch pack holding the fault, run as the gate runs it (`RealPackDoctor`, above). What pack-doctor refuses is retired from
the schema pass: the charter's answer is the rule (#348). What it accepts stays here, until a pinned
pack-doctor refuses it.

| Fault | pack-doctor at the pin | Judged by |
| --- | --- | --- |
| A preset item that no pack of the preset pack's own closure (over `depends_on` and `parent_pack`) declares | refused: `preset_item_undeclared` (`CLOSURE`) | pack-doctor |
| A `must_have` preset item that no pack of that closure holds as a file | refused: `preset_item_not_held` (`CLOSURE`) | pack-doctor |
| A graph edge end that is bare and held only by another pack, qualified with a pack outside the `depends_on` closure, or qualified with a pack that does not hold it | refused: `pack_reference_unqualified`, `pack_reference_pack_missing`, `pack_reference_artifact_missing` (`REFERENCES`) | pack-doctor |
| A step enhancement whose target step does not exist | refused: `pack_reference_artifact_missing` or `pack_reference_pack_missing` (`REFERENCES`) | pack-doctor |
| A step enhancement whose target step's prompt is missing | refused: `artifact_schema_error` at the target's mission type file (`PACK`) | pack-doctor |
| A manifest whose lists differ from those the files derive (an unlisted anti-pattern file included) | refused: `manifest_membership` | pack-doctor |
| A stale `content_hash` or `manifest_hash` in `pack-manifest.yaml` | refused: `manifest_stale` | pack-doctor |
| An agent-profile reference that is bare and held only by another pack, qualified with a pack outside the `depends_on` closure, or qualified with a pack that does not hold it | accepted: `REFERENCES` does not read an agent profile's references at the pin | `--cross-pack`, until pack-doctor judges them (#356) |
| A graph node that no file of the pack declares, left out of the manifest | accepted: `manifest_membership` derives its lists from the files | the schema pass (`unlisted_nodes`) |
| A prompt-fragment slot the target step's prompt does not declare | accepted | `--cross-pack` |

**Stray files (R34, #331).** A stray file, ignored (`notes.md`) or unmodelled (`notes.txt`, a log), is a
`file_not_held` warning in the schema pass, the service check and pack-doctor alike: pack-doctor's round trip
leaves out a file the charter does not hold. Nothing fails it.

### The house rules

`--cross-pack` judges only the house rules: what the charter does not judge, by ruling (#348; C-005, charter
ADR-0083 decision 18). Each is named in [`validate_pack_schemas.py`](../../scripts/ci/validate_pack_schemas.py)
beside its ruling:

- an id re-declared by a pack of another level. The charter takes it as a layer override (charter ADR-0053
  decision 6); this repository does not allow it;
- a bare DRG edge end that resolves to no node of any pack (DIV-007);
- a prompt fragment whose slot the target step's prompt does not declare. The charter refuses one only for a
  stored activation that has it in force (C38). A step with no `prompt_path` has no prompt, so it declares no
  slot;
- a cycle among the agent profiles' `specializes_from` edges, named in order (`a -> b -> a`). This is the
  remainder of charter ruling R-s: pack-doctor does not judge it until charter epic
  [#636](https://github.com/spec-kitty/spec-kitty-charter/issues/636) lands it. The service refuses one only
  within the closure it registers (`specialization_cycle`, charter ADR-0078 decision 2); this check covers
  every pack at once;
- two agent-profile references that are not charter rules (charter `research/rule-coverage.md` row 6): a
  bare reference that no pack holds, and a reference qualified with the profile's own pack. The fields are
  `directive-`, `tactic-`, `styleguide-` and `toolguide-references` and `operating-procedures`;
- until pack-doctor judges them, three more agent-profile references: a bare one only another pack holds,
  one qualified with a pack outside the `depends_on` closure, and one the named pack does not hold. #348 maps
  them to `REFERENCES`, but the jar of the pin does not read an agent profile's references (decision
  `01M8BMA2EFXXS3DGD8CHGGBR2J`). `RealPackDoctor` fails once a pinned pack-doctor judges them; retire them then
  (#356).

The schema pass also keeps one per-pack house rule, the graph node no file declares (see
[Pack manifests](#pack-manifests)).

### What the service owns

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

## The charter pin

[`charter.lock.yaml`](../../charter.lock.yaml) is the one pin of the charter. The schema validator and
the service job both read it, so the schemas, the service and pack-doctor always come from the same charter.
Today it is a `main` pin:

```yaml
commit: f6f21e4c086cb37d42c7b93b903725e11bcaad8b   # 40 lowercase hex characters; never a branch or a tag
release_tag:          # the service-vX.Y.Z[-pre] release of `commit`; empty for a main pin
jar_sha256:           # the service jar's SHA-256; required with release_tag
pack_doctor_sha256:   # the pack-doctor jar's SHA-256; required with release_tag
```

Every script fails closed on anything but a full commit. The pin names a charter release or pre-release
by default (operator ruling, 2026-11-18). For a release pin, set:
- `release_tag`;
- `jar_sha256` and `pack_doctor_sha256`, from the release's two `.sha256` assets;
- `commit`, the commit the tag points at.

The job then downloads both jars and refuses any other digest. A bump takes those digests from the release's
own `.sha256` assets, so a tampered release would carry matching ones: the reviewer of a bump pull request is
the only independent check, and confirms both digests against the release page. No Gradle build runs. Pin a `main` HEAD
commit, with the three release keys empty, only on demand: the job then builds the service and pack-doctor
from `commit`.

The pin is on charter `main` at `f6f21e4c` on demand (operator ruling, 2026-11-25; #345). No `service-v*`
release carries pack-doctor yet: the charter cuts none before the work that brings it lands (charter ruling R-w),
and a release without a pack-doctor jar cannot be pinned. Move to the first release that carries it by hand
(see below): the release track never replaces a `main` pin.

The easiest way to move the pin is `scripts/ci/charter_pin.py apply`, which also re-derives everything the
pin decides: every pack restamped by that pin's `pack-doctor remediate`, every digest and the pack pages. Move
the pin in the pull request that migrates the packs to what changed.

### Following charter releases

[`charter-track.yml`](../../.github/workflows/charter-track.yml) moves the pin for you, or tells you why it
cannot (#253). It runs the required check's own jobs (it calls `validate-packs.yml` with a charter target),
so it judges exactly what the gate judges. A called run first moves the pin and re-derives every pack
manifest, digest and pack page at the target (`scripts/ci/charter_pin.py apply --allow-red`, so a tree that
`remediate` leaves red still reaches the gate's own checks, which report it).

- **Release track, daily.** It lists the charter's releases and takes the newest `service-v*` release or
  pre-release. When that is newer than the lock's `release_tag`, it runs the checks with that release's
  service and pack-doctor jars, each checked against its `.sha256` asset, and with `commit` set to the tag's
  commit. Only a run on
  `main` acts on the verdict:
  - green: it opens one pull request, from `charter/service-release-<tag>`, that bumps the four pin
    values and carries the re-derived files and a changelog entry. An open bump pull request for an
    older release is closed in its favour;
  - red: it opens one issue labelled `charter:release-red`, or rewrites the open one, naming the
    release and the errors of the failing jobs. A scheduled run that cannot resolve the release (the
    listing, the tag or one of its two `.sha256` assets) says so on the same issue. A release without a
    pack-doctor asset cannot resolve: the gate needs both jars.

  While the bump pull request of the newest release is open, the track does not check that release again.
  A bump pull request closed unmerged is not proposed again until a newer release. Once `main`'s lock
  reaches the release an open red issue names, by any pull request, the next run closes the issue.

  A lock without a `release_tag` (a `main` pin, taken on demand) is never replaced by this track. From
  the Actions tab, dispatch **Charter track** with `track: release` to run it now; a `release_tag` input
  checks a given release, which is acted on only when it is the newest and newer than the lock.
- **On demand, against unreleased charter.** Dispatch **Charter track** with `track: ref` and a
  `charter_ref` (default `main`; a branch, a tag, `pull/<n>/head` or a commit), or label a pull request
  `charter:head` to run its packs against charter `main`. The charter is built from source and every
  check runs, pack-doctor (built from the same source) included. The verdict is in the run's summary; this track never bumps the
  lock and uses no secret. Like every run against a target, it re-derives the manifests, digests and pack
  pages first, so a pull request's own gate, not this run, judges those files as committed.
- **Nightly, against charter `main`** (#311). At 02:23 UTC every night, at a different hour from the release
  track's 05:41, the track checks the packs against charter `main`, built from source, with the same
  checks as the on-demand track, pack-doctor included. It reports only: it never bumps the lock and it
  is not a required check. Only a run on `main` acts on the verdict:
  - red: it opens one issue labelled `charter:main-red`, or rewrites the open one, naming the charter
    commit and the errors of the failing jobs. A run that cannot resolve charter `main` says so on the
    same issue;
  - green: it closes the open `charter:main-red` issue.

  It keeps clear of the release track: its own label, its own issue and its own run queue. A red night
  blocks nothing; it warns that an unreleased charter change will fail the packs once it is released.
  Dispatch **Charter track** with `track: main` to run it now (any `charter_ref` is ignored); off `main`,
  it reports what it would open or close and touches no issue.

The bump job uses two tokens (operator ruling on #314; the organization does not let GitHub Actions
create pull requests):

- **The workflow's own token** pushes the bump branch and makes its commit through the GitHub API, so
  GitHub signs the commit. Only the bump job is given `contents: write`.
- **`PR_CREATION_TOKEN`**, a repository secret, opens the bump pull request and closes a superseded one.
  It is a fine-grained PAT on `spec-kitty-charter` and `spec-kitty-open-packs` with **Actions** and
  **Pull requests** read and write, and **no Contents** access. A pull request opened with it starts the
  `pull_request` workflows, so the required check runs on the bump pull request itself, like any other
  pull request. Only the step that opens and closes pull requests holds it, and that step runs nothing
  but `gh`. This workflow uses only its Pull requests scope. If the secret is missing, the bump job fails
  before it pushes anything, and its error names `PR_CREATION_TOKEN`.

A superseded bump pull request that cannot be closed, or whose branch cannot be deleted, fails the bump
job with an error naming it. Close or delete it by hand: no later run looks at a closed pull request again.

The required check judges the bump branch as cut from `main`. If `main` moves before the merge, use
**Update branch**: that push runs the gate on the merge result. A pack added since then needs its
manifest restamped at the new pin (see [Pack manifests](#pack-manifests)).

To move the pin by hand, the same tool resolves and applies a target:

```bash
python3 scripts/ci/charter_pin.py resolve-release service-v<version>   # commit=, release_tag=, jar_sha256=, pack_doctor_sha256=
python3 scripts/ci/charter_pin.py apply --commit <commit> --release-tag <tag> \
  --jar-sha256 <digest> --pack-doctor-sha256 <digest>
```

`apply` needs Java 25 to run `remediate`. It stops when `remediate` refuses a pack or leaves the tree red;
only the gate's own check jobs pass `--allow-red`.

Run it locally before opening a PR:

```bash
scripts/ci/validate-packs.sh
```

## Next

- [Publish a pack](publish-a-pack.md)
