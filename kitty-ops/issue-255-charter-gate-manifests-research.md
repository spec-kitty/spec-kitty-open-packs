# Research: the charter round-trip gate and derived pack manifests (#252, #255, #250)

Grounding note, written before any change. Branch `issue-255-charter-gate-manifests` off `main` `736e613`.
Delivery shape: an Op (one surface: CI and the generated manifests), not a Mission.

## Starting state

- `charter.lock.yaml` pins spec-kitty-charter `17ce3f9`. The current charter `main` is `848170e`
  (2026-11-13T15:53+01:00), 85 commits later.
- Of those 85 commits, only one touches `contracts/packs/`: `asset.schema.json` now requires a kebab-case asset
  `id`. Every pack still validates against the new contract (`scripts/ci/validate-packs.sh`, exit 0), so the bump
  adds no schema drift.
- `848170e` contains charter #542 (the derived manifest membership, merged 2026-11-13T06:09Z) and #545 (the
  `org-fragment` round trip, merged 06:42Z). Charter #547 (the drift test passes silently over file kinds that
  nothing models) is still an open issue, so it is not fixed at this pin. #478 (`pack-check`) and #467 (slice C)
  are also open.
- #255 says only `built-in` carries a manifest. That is out of date: seven packs carry one (`architecture`,
  `built-in`, `foundation`, `planning-analysis`, `refactoring`, `testing`, `writing`), and the twelve org packs
  carry none.
- On #250, the driftTest result at open-packs `1692a3b` with #542 merged: `built-in` leaves out the presets
  `default` and `minimal`; `foundation` leaves out 31 constituents; `writing` leaves out 21.

## How the charter derives a manifest (`ManifestMembership`, `PackManifests` at 848170e)

- **Constituents.** One per artifact the whole-pack load holds, as `{kind token, local id, stored path}`, in the
  UTF-16 order of the paths. Graph-only kinds (`action`, `anti_pattern`) have no file, so they get no entry.
  Templates (payloads under `templates/` or `missions/<type>/templates/`) are listed with a path-derived id.
- **Presets.** One per `presets/<id>.yaml`, in path order.
- **Refusal.** A whole-pack registration and the round-trip gate refuse an uploaded manifest whose lists differ
  from the derived ones (`manifest_membership`). Entry order and hashes are not judged; every write restamps them.
- **Oracle check, done before any change.** I ported the derivation into `validate_pack_schemas.py`, reusing its
  existing `classify` port. On the charter's three example packs (`built-in`, `org-base`, `project`) it reproduces
  the committed manifests exactly: 40, 11 and 4 constituents, no mismatch, same order. On this repository's
  current manifests it reproduces #250's findings exactly: `built-in` has 2 preset mismatches, `foundation` 31
  and `writing` 21 (mission types, step contracts and templates), and the other four packs have none.

## Gates that touch manifests or digests, and how each stays green

| Gate | Where | What it checks | How it stays green |
|---|---|---|---|
| Schema pass | `validate-packs.sh` → `validate_pack_schemas.py` | manifest hashes (`stale_manifest_fields`); every file-backed constituent is listed (`unlisted_constituents`); every declared graph node of a non-exempt kind is listed (`unlisted_nodes`) | regenerated manifests carry fresh hashes and list a superset; the exempt-kind comment is updated, and no check or test expectation changes |
| New: derived membership | same, `--derived-manifests` | every pack under `packs/` and `tests/fixtures/valid/` carries a manifest equal to the derived lists | `--derive-manifest` writes them |
| Pack digests | `check-pack-digests.sh` → `pack_digest.py` | `packs/<pack>.source.yaml` digest over the pack tree | `pack_digest.py --update` after every content change; never hand-merged |
| Generated pages | `gen_pack_reference.py --check` | `docs/packs/*.md` reflect `pack.yaml` (versions) | regenerate after the version bumps |
| Vocabulary | `check_vocabulary.py` | retired ids and terms in pack files | manifests hold ids and paths only |
| Charter service | `charter_service_check.py` | compose all packs, register org/project packs (registration refuses `manifest_membership`), refuse invalid fixtures | derived manifests on every org pack; a fresh service per run, so no 409 in CI |
| New: round trip | `./gradlew :packs:driftTest` from the pinned checkout | every pack round-trips by meaning; violations (incl. `manifest_membership`), unmodelled files, load warnings | derived manifests; red first at the new pin |

Built-in-level packs are never registered (ADR-0065 D3). So before this change, only the driftTest could see a
membership mismatch in `built-in`, `foundation`, `writing` and the other built-in-level packs. That is why #252
asks for it as a gate.

## Versioning (one-time 409)

A pack registered before #542 answers `409 pack_version_conflict` when the same `pack_version` is sent again with
different content (`PackVersionHistory`). Only org and project packs can be registered, and each of the twelve org
packs gains a manifest, so each gets a patch bump. Built-in-level packs cannot be registered, so they get no 409
and no bump. Bumping them would also break the exact `==` pins between `built-in`, `foundation`, `writing` and
the other members.

## Similar surfaces

| Surface | Disposition |
|---|---|
| The 7 packs with a manifest | in scope: regenerate all 7 (3 refused today, 4 already match, regenerated anyway so every manifest comes from the same generator) |
| The 12 org packs without a manifest | in scope (#255): generate |
| `tests/fixtures/valid/example-pack` | in scope: it is registered by the charter-service job and validated like a pack, so it gets a derived manifest too |
| `tests/fixtures/invalid/*` | out of scope: their files are what they prove; the membership requirement skips invalid fixtures |
| `--regenerate-manifest` (restamp only, membership kept) | kept unchanged; `--derive-manifest` is added beside it |
| `MANIFEST_EXEMPT_NODE_KINDS` comment ("not listed in this repository's manifests") | in scope: the comment is now wrong; the exemption itself is kept |
| Docs that describe manifests (`docs/guides/validate-a-pack.md` and others) | in scope where they name the command |

## Tracked issues

| Issue | Disposition |
|---|---|
| #255 | Closes |
| #250 | Closes (its three refused manifests are regenerated) |
| #252 | Refs. Its gate and pin bullets are delivered. Its last bullet (run `pack-check` and retire the Python port) waits on charter #478, so the issue stays open |
| #249 | closed already; Refs only (the Python port of `classify`, which this derivation reuses) |
| #251 | that was the PR closing #249; nothing to do |
| #253 | out of scope (nightly against charter `main`); non-goal |
| #254 | out of scope (doc-kitty pack pages); non-goal |
| charter #478 | blocks #252's last bullet; not in scope |
| charter #542, #545 | held by the new pin |
| charter #547 | open; not at the pin. The gate runs today's driftTest; once #547 lands, a later pin bump tightens it |
| Slice 4 (#195, #227, #159) | in flight in another session; whichever lands second rebases and restamps the digests and manifests (never by hand) |

## Test seams and limits

- The charter build cannot run in this session: running the external Gradle build was refused. So the round trip
  is witnessed in CI: the gate is pushed first and goes red at the new pin, and the regenerated manifests follow.
- `raw.githubusercontent.com` answers 404 through this session's proxy, so the local validator runs use
  `CHARTER_CONTRACT_DIR` set to the pinned checkout's `contracts/packs`.
