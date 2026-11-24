# Research: Release-pin follow-through

All findings were checked against `main` at `a7243e2` and charter `cb9b154` (`service-v0.1.0-rc.3`, the pin).

## R1. The lock already holds a release pin

- **Finding:** `charter.lock.yaml` pins `service-v0.1.0-rc.3` with both digests. The charter has rc.1, rc.2 and rc.3 only.
- **Decision:** the brief's "first release pin is manual" step is already done. The track never replaces a lock whose `release_tag` is empty (`charter_pin.py` `newest-release`: `newer = bool(current) and …`, now l.323–327). rc.4 and later will be proposed automatically.
- **Consequence:** the `PR_CREATION_TOKEN` secret matters from rc.4 on. It cannot be read from a session, so it was asked of the dispatcher (Q1).

## R2. `membership_mismatch` already equals the charter

- **Finding:** `ManifestRules.mismatch` at the pin (`service/packs/.../rules/ManifestRules.java` l.97–118) emits, in order:
  1. distinct listed entries the pack does not hold;
  2. repeated listings;
  3. derived entries left out.

  An entry that is both duplicated and unheld therefore yields two reasons. The Python port does the same.
- **Decision:** no code change. Pin it with a test (#262 item resolved as "matches the charter").
- **Alternative rejected:** dropping the "twice" reason for an unheld entry would diverge from the charter.

## R3. The symlinked-directory hole is real on CI's Python

- **Finding:** `derived_manifest` uses `pack_dir.rglob("*")` (l.476) and skips only link *files*. On Python ≤3.12, which CI uses, `rglob` descends into a linked directory. The charter's `PackFileSet` uses `Files.walkFileTree`, which does not follow links, and enters the root through its real path (#174).
- **Decision:** add a `pack_files()` helper over `os.walk(followlinks=False)` that resolves the root first.
- **Alternative rejected:** `rglob(recurse_symlinks=False)` is 3.13+ only.

## R4. The token beside the re-derivation

- **Finding:** in `charter-track.yml`, the "Push the bump branch" step (l.304–371) sets `GH_TOKEN: github.token` (`contents: write`) and runs `charter_pin.py apply` and `changelog`. `apply` parses the new release's contract content and imports third-party YAML and schema libraries. `PR_CREATION_TOKEN` is already confined to the "Open" step (#314).
- **Decision:** split the step into a lookup step (token, gh only), a re-derive step (no token) and a push step (token, gh and jq only).

## R5. Attestation verification

- **Finding:** `jar_digest` trusts the release's own `.sha256` asset. `gh attestation verify` checks a Sigstore build attestation against the source repository. Whether the charter publishes attestations is unknown, so the warn-only path is likely for now.
- **Decision:** a separate read-only job that never fails, with the outcome in the PR body. Verify both jars: the service jar and the pack-check jar (operator ruling).
- **Alternative rejected:** verifying inside `validate-packs.yml`'s jar download. That would touch every PR gate run and risk blocking it, against the warn-only ruling.

## R6. #331 remainder

- **Finding:** #336 made a stray `notes.md` a warning in the schema pass and the service check. The guide (l.273–275), `CHANGELOG.md` (l.939) and `charter_pack_check.py` (l.20) still say the decision is pending. No test pins that the gate fails an unmodelled stray file through `round_trip_red`.
- **Decision:** add one judge test with a same-fixture control: the `notes.md` notice passes, the `notes.txt` round-trip red fails. Reword the three texts to cite the ruling and spec-kitty-charter#631.
