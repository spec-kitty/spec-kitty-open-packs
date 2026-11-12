---
affected_files: []
cycle_number: 1
mission_slug: charter-slice-b-migration-01M78K20
reproduction_command:
reviewed_at: '2026-11-12T19:46:18Z'
reviewer_agent: claude:opus:reviewer-renata
wp_id: WP04
---

# WP04 review feedback, cycle 1 (reviewer-renata)

Verdict: **changes requested**. One gate fails on this tree; everything else checks out.

## MAJOR

1. `packs/foundation/pack-manifest.yaml:155` is stale. The glossary edit in
   `packs/foundation/glossary_packs/spec-kitty-core.glossary-pack.yaml:996` changed the file's
   sha256 from `da78fe1e…4a33e7` to `7870b3c3…f650b52a`, but the manifest still records the old
   `content_hash`. With `GITHUB_TOKEN` unset,
   `python3 scripts/ci/validate_pack_schemas.py --cross-pack packs/*/` exits 1:

   ```
   ::error file=packs/foundation::foundation/pack-manifest.yaml: stale manifest: constituents{glossary_packs/spec-kitty-core.glossary-pack.yaml}.content_hash; run `python3 scripts/ci/validate_pack_schemas.py --regenerate-manifest packs/foundation`
   FAIL: packs/foundation (217 files checked, 24 excluded or payload, 1 violations)
   ```

   Fix: run `python3 scripts/ci/validate_pack_schemas.py --regenerate-manifest packs/foundation`
   and commit the manifest. Then re-run the validator. The tree digest excludes
   `pack-manifest.yaml`, so `packs/foundation.source.yaml` should not change; confirm that
   `check-pack-digests.sh` still passes. The charter service check did not catch this because
   it does not register built-in-level packs.

## NIT

2. `docs/architecture/overview.md:70`: "except skills, where only required skills are in force
   until the project activates more" is carried over from the core/org-charter model. Check it
   against the charter's activation model, or drop the skills exception if the charter does not
   have one.

## Verified as correct

- No live mention of `pack.md`, `PROVENANCE.md`, `org-charter.yaml`, `active_charter`,
  `required_<kind>` or `skill_namespace` is left outside ADRs and the changelog. The remaining
  hits are retirement or history notes, `validate-a-pack.md` filename matches, or test fixtures.
- Every item 6 entry of #241 and #242 is addressed. The glossary wording matches the operator's
  choice exactly.
- The `BUILT_IN_DIGEST` is honest. `python3 scripts/ci/pack_digest.py built-in` gives `80bb107a…a32700`.
  The only change under `packs/built-in` since main is the `pack.md` → `README.md` rename, with
  a two-line wording edit.
- These pass: `check-pack-digests.sh` (19 ok), `check_vocabulary.py` (743 files, 0 findings),
  `gen_pack_reference.py --check` (19 pages, no drift), unit tests
  (release 13, vocabulary 15, ci 133, docs 13, assets 21 with 14 skipped) and `site npm run validate`.
