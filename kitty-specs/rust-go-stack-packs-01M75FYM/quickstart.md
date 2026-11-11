# Quickstart: verify the Rust and Go packs

From the repository root, with the pinned charter contracts checked out locally
(`git -C <dir> fetch --depth 1 origin <charter.lock.yaml commit>`):

```bash
export CHARTER_CONTRACT_DIR=<charter checkout>/contracts/packs
scripts/ci/validate-packs.sh                       # every pack, cross-pack checks, invalid fixtures
scripts/ci/check-built-in.sh                       # built-in unchanged
python3 scripts/ci/check_vocabulary.py
python3 scripts/docs/gen_pack_reference.py --check # docs/packs/{rust,go}.md current
for s in release vocabulary ci docs assets; do python3 -m unittest discover -s tests/$s; done
(cd site && npm ci && npm run build)               # docsite
# CI only (needs the charter service jar):
python3 scripts/ci/charter_service_check.py --jar <jar>
```

To adopt a pack in a project, register it under `charter_packs.org.packs` with `subdir: packs/rust`
(or `packs/go`) together with its `foundation` dependency, then activate the `rust` (or `go`) preset.
