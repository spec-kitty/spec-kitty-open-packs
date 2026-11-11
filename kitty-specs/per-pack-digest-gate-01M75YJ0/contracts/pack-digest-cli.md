# Contract: `scripts/ci/pack_digest.py`

```
python3 scripts/ci/pack_digest.py [PACK ...]          # print "<digest>  packs/<name>" per pack
python3 scripts/ci/pack_digest.py --check [PACK ...]  # verify; with no PACK also report orphan sidecars
python3 scripts/ci/pack_digest.py --update [PACK ...] # restamp stale, create missing; refuse malformed
```
- `PACK` is a directory name under `packs/`; default is every discovered pack.
- Exit: 0 all fresh / update done; 1 any violation (check) or refusal (update); 2 usage error (unknown PACK).
- Failure line: `::error file=packs/<name>.source.yaml::<reason>; run \`python3 scripts/ci/pack_digest.py --update <name>\``.
- Success line (check): `ok: packs/<name>/ digest matches <value>`.
- Importable: `snapshot_sha256(root: Path) -> str`, `discover_packs(packs_root: Path) -> list[Path]`.
- `--update` is idempotent: second run changes no bytes.

# Contract: `scripts/ci/built_in_digest.py` (compatibility shim)
- No args: prints built-in's digest only (one line, hex) — kitty-stack `open-packs digest`.
- `--check`: checks `packs/built-in` only, same exit codes as before.

# Contract: `scripts/ci/check-pack-digests.sh`
- Runs `python3 scripts/ci/pack_digest.py --check` from the repo root. Called by the `validate` job step "Check every pack's recorded digest".

# Contract: release asset `<pack>-vX.Y.Z.source.yaml`
- Written by `scripts/release/release_assets.py build vX.Y.Z` for every released pack, next to
  `<pack>-vX.Y.Z.tar.gz` and `<pack>-vX.Y.Z.tar.gz.sha256`.
- Bytes: exactly `packs/<pack>.source.yaml` at the tagged commit (git tree, never the working tree).
- A released pack without that file at the tag fails the build before any archive is written.
- Published by the release workflow's existing `dist/*` upload; covered by its reproducibility diff.
