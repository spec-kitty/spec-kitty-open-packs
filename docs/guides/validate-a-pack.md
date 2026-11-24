---
title: Validate a pack
description: Validate a Charter Pack against the charter pack schemas and the charter service, read the findings, and understand the CI gate this repository runs on every pull request.
doc_status: wip
updated: '2026-11-24'
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

A misnamed companion does not slip through: pack-check still refuses the pack, because the companion its
artifact names is missing (`<ref>: missing`, e.g. `steps/implement.prompt.md: missing`). Only a stray file that
nothing names is left as a warning.

A file a skill's `body_path` names is held as that skill's companion, whatever its name. Note that the
pack-check gate is stricter on the last group: its round trip reds an unmodelled file (#331 tracks that). The
checks run on every pack, built-in-level ones included, which no registration sees.

## What the schemas catch

| Condition | Result |
| --- | --- |
| A required field is missing, or a field has the wrong type or pattern (for example a lowercase directive `id`) | Violation |
| A field the schema does not define (the schemas are closed) | Violation |
| A DRG fragment with a provenance header, or an edge endpoint that is a bare id rather than `<kind>:<id>` | Violation |
| A preset in the old shape (`name`, bare id strings, `mission_type_activations`) | Violation |
| A file in a retired layout (for example `mission.yaml` beside a mission type), or a root case variant of a ruled file (`Readme.md`) | Violation |
| A file no rule models (`notes.txt`, `x.tactic.yml`, `drg/tactic.graph.yaml`) | Warning (`file_not_held`), not held |
| Markdown only the `ignored` rule takes, other than a `README.md` (an orphan skill body included) | Warning (`file_not_held`), not held (R34, #331) |

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
constituent. Actions and anti-patterns have no file, so they are never listed. Templates and mission types
are exempt from this older check, but the derived membership below lists them. To
exempt a new node kind from this check, add it to `MANIFEST_EXEMPT_NODE_KINDS` in
[`validate_pack_schemas.py`](../../scripts/ci/validate_pack_schemas.py); a kind in neither place fails.

### Derived pack manifests

Every pack, and every valid fixture, carries the `pack-manifest.yaml` the charter derives (#255; charter
ADR-0042 as amended 2026-11-12). Its lists come from the pack itself, never from an author:
- one constituent for each artifact file the pack holds, with its kind, id and path;
- one entry for each `presets/<id>.yaml`.

Both lists are in path order, and the hashes are stamped from the files. The charter refuses a
manifest with any other lists: as `manifest_membership` at registration, and in the round trip as
`pack-manifest.yaml: refused: leaves out ...`.
So `validate-packs.sh` passes `--derived-manifests`, which fails a pack whose manifest is missing or
whose lists differ. After adding, removing or renaming an artifact or preset, regenerate the
manifest, then restamp the digests:

```bash
python3 scripts/ci/validate_pack_schemas.py --derive-manifest packs/<name>
python3 scripts/ci/pack_digest.py --update
```

`--derive-manifest` mirrors the charter's `ManifestMembership` at the pin. The round trip below is
the authority: if the two ever disagree, the mirror has drifted from the pin.

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
   refused as `retired`, any other file the service does not model is warned as `file_not_held` and
   left out (charter #554, ruling Q1), and a file an exclusion or the `ignored` rule takes is left out and reported as a `file_not_held`
   diagnostic. Every diagnostic of a succeeded registration is printed as a notice. Each
   `file_not_held` file is classified with the schema validator's mirror of the pinned contract: a file the
   mirror also leaves out (excluded, ignored or unmodelled) stays a notice, as R34 (#331) asks; a file the
   mirror classifies as held content fails the job, because the mirror has drifted from the pin;
4. **gates every pack on the charter's pack-check** (#252; charter ADR-0075 decision 9, ADR-0070 decision 4
   as amended 2026-11-13). pack-check is the charter's own whole-pack check. It checks each pack, the closure
   of the set, and, with `--round-trip`, loads each pack through the charter's store, writes it back and
   compares it by meaning.
   - **The jar.** On a release pin, the job checks that the tag points at the lock's `commit`, downloads
     `pack-check-<version>.jar` from the pinned release, and refuses any digest but `pack_check_sha256`
     ([`charter_pack_check_jar.sh`](../../scripts/ci/charter_pack_check_jar.sh)). On a main pin it builds the
     jar from `commit`. Both release jars, this one and the service jar, pass the same two checks
     ([`charter_release_asset.sh`](../../scripts/ci/charter_release_asset.sh)): the tag must point at `commit`, and
     the download goes to `<jar>.part`, which takes the jar's name only once its digest matches. A failed, partial
     or mismatched download leaves nothing behind.
   - **The run.** [`charter_pack_check.py`](../../scripts/ci/charter_pack_check.py) runs it over every pack
     and valid fixture together, built-in-level ones included.
   - **What fails the job:**
     - any exit but 0, **exit 2 included**: rc.3 crashes with exit 2, and no report, on a malformed
       `pack_version` (spec-kitty-charter#624). That is a failure, never a skip;
     - a problem in the report: a violation, an unmodelled file, a file that does not round-trip, or a
       manifest whose lists differ from the derived ones;
     - a warning other than `file_not_held`, or a warning line it cannot read;
     - a report with a key besides `checks`, `packs`, `problems` and `skipped`: the gate cannot judge what it
       does not read, so a changed report format fails instead of passing;
     - a check that did not run;
     - a pack left out of the verdict.
   - **The report** is uploaded as the `charter-pack-check-report` artifact. No registration sees a
     built-in-level pack, so this is the only check of their manifests that the charter itself makes.
   - **It replaced** the charter's `driftTest`, which the job used to build from the pinned source: the same
     round trip under the same rule.
5. **proves it is not vacuous**: every pack under `tests/fixtures/invalid/` must be refused with the code
   its `expected-code` file names, once when composed and once when registered, and by pack-check (checked
   alone, less its `expected-code`). A fixture accepted, or refused with another code, fails the job.

The `expected-code` file of a fixture holds `key: value` lines:

```text
composition: pack_unreadable      # the code of the refusal of GET /offering
registration: validation_failed   # the code of the refused registration's problem
precheck: accepted                # optional: the schema pre-check cannot see this refusal
pack-check: retired               # a code pack-check's report must carry (in a problem or a violation),
                                  # or `failed`: the spec-kitty-charter#624 crash (exit 2, no report,
                                  # an internal error naming pack_version), and nothing else
```

`legacy-shapes` holds 3.x-era files and is refused as unreadable and invalid;
`unknown-dependency` is well formed and refused only for composing with a pack nobody configured.
`malformed-pack-version` is the valid example pack with a `pack_version` that is not a version. The schema
pass accepts it, the service refuses it (`pack_version_invalid`), and pack-check rc.3 crashes on it
(`pack-check: failed`). Once spec-kitty-charter#624 lands, that line no longer matches. Change only that line:
name the code pack-check then reports. Nothing else needs an edit.

Run it locally, with the jar of the pin (Java 25 on the `PATH` or in `JAVA_HOME`):

```bash
jar="$(scripts/ci/charter_service_jar.sh /tmp/charter-service)"
python3 scripts/ci/charter_service_check.py --jar "$jar"
```

and pack-check, at the pin (Java 25):

```bash
jar="$(scripts/ci/charter_pack_check_jar.sh /tmp/charter-service)"
python3 scripts/ci/charter_pack_check.py --jar "$jar"
```

`charter_service_check.py` takes any service jar, so a jar you built from a charter branch tells you
whether a pending charter change would break these packs. It exits `0` when everything passed, `1` when a
check failed and `2` when it could not run.

### What pack-check covers and what stays here

pack-check rc.3 was tried against scratch packs with each fault below, run as the gate runs it (with
`--round-trip`). It exits 0 on every one of them, so the schema pass keeps judging them. Retire a rule here
only once the pinned pack-check refuses its case (#330):

| Fault | pack-check rc.3 | Judged here by |
| --- | --- | --- |
| A preset `must_have` item no pack of the preset pack's closure holds | accepted | `--cross-pack` (`requiredNotHeld`, the required floor), until spec-kitty-charter#629 |
| A preset id no pack declares | accepted | `--cross-pack` |

**Stray files (R34, #331).** A stray ignored file (a note such as `notes.md`) is a `file_not_held` warning in
pack-check and, since R34, a warning here too: nothing fails it. An unmodelled stray file (`notes.txt`, a log)
is also only a warning in the schema pass and the service check, but pack-check's round trip still refuses it
as `round_trip_red`, and the gate keeps that verdict: it fails. The operator accepted this gap on 2026-11-21
(#331), with no override here. Until spec-kitty-charter#631 lets the round trip skip the files the store does
not hold, only Markdown notes may stay in a pack.

pack-check also refuses a stale `content_hash` or `manifest_hash` in `pack-manifest.yaml` (`round_trip_red`;
spec-kitty-charter#630). The schema pass keeps its own stale-hash check anyway: it is the fast pre-check, and
it names the command that restamps the manifest.

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
  pack's `depends_on` closure holds as a file (a graph node without one is held by nobody);
- a bare DRG edge end that resolves to no node of any pack;
- an id re-declared by a pack of another level (the service takes it as a layer override; this
  repository does not allow it);
- an agent-profile reference (`directive-`, `tactic-`, `styleguide-` and `toolguide-references`,
  `operating-procedures`) that is bare but held by another pack or by none, qualified with the profile's
  own pack, outside its `depends_on` closure, or not held by the named pack;
- a prompt fragment whose `enhances` target step does not exist, or whose slot the step's prompt does
  not declare;
- a cycle among the agent profiles' `specializes_from` edges, named in order (`a -> b -> a`). The
  service refuses one only within the closure it registers (`specialization_cycle`, charter ADR-0078
  decision 2); this check covers every pack at once.

## The charter pin

[`charter.lock.yaml`](../../charter.lock.yaml) is the one pin of the charter. The schema validator and
the service job both read it, so the schemas and the service always come from the same charter:

```yaml
commit: cb9b15426d17c402b06204185a17ebfbc65f22ff   # 40 lowercase hex characters; never a branch or a tag
release_tag: service-v0.1.0-rc.3                   # the service-vX.Y.Z[-pre] release of `commit`; empty for a main pin
jar_sha256: 763536af1c56cc29d3e08720461546ac63f9ddab4989c6db89c3b7b7e2aaf42c          # the service jar's SHA-256; required with release_tag
pack_check_sha256: adde1dfff5d02efbb3a02fafde8222951d0e1f0fafccde29d7fb39be3ea9ccbe   # the pack-check jar's SHA-256; required with release_tag
```

Both scripts fail closed on anything but a full commit. The pin names a charter release or pre-release
by default (operator ruling, 2026-11-18). Set:
- `release_tag`;
- `jar_sha256` and `pack_check_sha256`, from the release's two `.sha256` assets;
- `commit`, the commit the tag points at.

The job then downloads both jars and refuses any other digest. A bump takes those digests from the release's
own `.sha256` assets, so a tampered release would carry matching ones. Two checks stand apart from those
assets: the build attestation of each jar, which the release track verifies before a bump, and the
reviewer of the bump pull request, who confirms both digests against the release page. No Gradle build runs. Pin a `main` HEAD
commit, with the three release keys empty, only on demand: the job then builds the service and pack-check
from `commit`. The easiest way to move the pin is `scripts/ci/charter_pin.py apply`, which also re-derives
everything the pin decides. Move the pin in the
pull request that migrates the packs to what changed.

### Following charter releases

[`charter-track.yml`](../../.github/workflows/charter-track.yml) moves the pin for you, or tells you why it
cannot (#253). It runs the required check's own jobs (it calls `validate-packs.yml` with a charter target),
so it judges exactly what the gate judges. A called run first moves the pin and re-derives every pack
manifest, digest and pack page at the target (`scripts/ci/charter_pin.py apply`).

- **Release track, daily.** It lists the charter's releases and takes the newest `service-v*` release or
  pre-release. When that is newer than the lock's `release_tag`, it runs the checks with that release's
  service and pack-check jars, each checked against its `.sha256` asset, and with `commit` set to the tag's
  commit. Only a run on
  `main` acts on the verdict:
  - green: it opens one pull request, from `charter/service-release-<tag>`, that bumps the four pin
    values and carries the re-derived files and a changelog entry. An open bump pull request for an
    older release is closed in its favour. Before that, both jars are checked once more (see *Release
    provenance* below): a jar that is not the file the pin names stops the bump;
  - red: it opens one issue labelled `charter:release-red`, or rewrites the open one, naming the
    release and the errors of the failing jobs. A scheduled run that cannot resolve the release (the
    listing, the tag or one of its two `.sha256` assets) says so on the same issue. A release without a
    pack-check asset cannot resolve: the gate needs both jars.

  While the bump pull request of the newest release is open, the track does not check that release again.
  A bump pull request closed unmerged is not proposed again until a newer release. Once `main`'s lock
  reaches the release an open red issue names, by any pull request, the next run closes the issue.

  A lock without a `release_tag` (a `main` pin, taken on demand) is never replaced by this track. From
  the Actions tab, dispatch **Charter track** with `track: release` to run it now; a `release_tag` input
  checks a given release, which is acted on only when it is the newest and newer than the lock.
- **On demand, against unreleased charter.** Dispatch **Charter track** with `track: ref` and a
  `charter_ref` (default `main`; a branch, a tag, `pull/<n>/head` or a commit), or label a pull request
  `charter:head` to run its packs against charter `main`. The charter is built from source and every
  check runs, pack-check (built from the same source) included. The verdict is in the run's summary; this track never bumps the
  lock and uses no secret. Like every run against a target, it re-derives the manifests, digests and pack
  pages first, so a pull request's own gate, not this run, judges those files as committed.
- **Nightly, against charter `main`** (#311). At 02:23 UTC every night, at a different hour from the release
  track's 05:41, the track checks the packs against charter `main`, built from source, with the same
  checks as the on-demand track, pack-check included. It reports only: it never bumps the lock and it
  is not a required check. Only a run on `main` acts on the verdict:
  - red: it opens one issue labelled `charter:main-red`, or rewrites the open one, naming the charter
    commit and the errors of the failing jobs. A run that cannot resolve charter `main` says so on the
    same issue;
  - green: it closes the open `charter:main-red` issue.

  It keeps clear of the release track: its own label, its own issue and its own run queue. A red night
  blocks nothing; it warns that an unreleased charter change will fail the packs once it is released.
  Dispatch **Charter track** with `track: main` to run it now (any `charter_ref` is ignored); off `main`,
  it reports what it would open or close and touches no issue.

A green release is turned into a pull request by two jobs, so that no token is in reach of the code that
reads the new release's contract (#310):

- **`derive`** runs `charter_pin.py apply` and the changelog entry. It holds no token and no secret, and
  hands on only the changed files and the commit it started from.
- **`bump`** holds the tokens and runs no repository code: no checkout, no Python. It accepts only the
  files a bump writes (`charter.lock.yaml`, the changelog, the pack digests, the pack and fixture
  manifests and the pack pages) and refuses anything else before it pushes. It builds the commit
  request itself, on this run's commit.

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

**Release provenance** (#310). Before a bump, a read-only job downloads both jars of the release again:

- A jar that is not the file the pin names (another SHA-256) is an error, and nothing is derived or
  opened.
- Each jar's build attestation is verified against the charter's release workflow and the tag
  (`gh attestation verify --signer-workflow … --source-ref refs/tags/<tag>`, as the charter's release
  notes prescribe). A missing or failing attestation is only a warning (operator ruling): the pull
  request is opened anyway, and its body says, per jar, *verified* or *not verified*. When either is not
  verified, compare both digests with the release page by hand before merging.

A superseded bump pull request that cannot be closed, or whose branch cannot be deleted, fails the bump
job with an error naming it. Close or delete it by hand: no later run looks at a closed pull request again.

The required check judges the bump branch as cut from `main`. If `main` moves before the merge, use
**Update branch**: that push runs the gate on the merge result. A pack added since then needs its
manifest re-derived at the new pin.

To move the pin by hand, the same tool resolves and applies a target:

```bash
python3 scripts/ci/charter_pin.py resolve-release service-v0.1.0-rc.1   # commit=, release_tag=, jar_sha256=
python3 scripts/ci/charter_pin.py apply --commit <commit> --release-tag <tag> --jar-sha256 <digest>
```

Run it locally before opening a PR:

```bash
scripts/ci/validate-packs.sh
```

## Next

- [Publish a pack](publish-a-pack.md)
