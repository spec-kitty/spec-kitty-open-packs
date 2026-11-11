# Quickstart: pack digests

After editing anything under `packs/<name>/`:

```bash
python3 scripts/ci/pack_digest.py --update        # restamp every stale sidecar
python3 scripts/ci/pack_digest.py --check         # what CI runs (via scripts/ci/check-pack-digests.sh)
git add packs/*.source.yaml
```

New pack: create `packs/<name>/pack.yaml`, then `--update` writes `packs/<name>.source.yaml`.
Removed pack: delete its sidecar too, or `--check` reports it as an orphan.
Legacy: `python3 scripts/ci/built_in_digest.py` still prints built-in's digest.
