# Quickstart: verify the citation-and-docs-writing mission

```bash
uv venv && uv pip install pyyaml jsonschema pytest
source .venv/bin/activate
bash scripts/ci/validate-packs.sh
python3 -m pytest -q tests
python3 scripts/ci/check_vocabulary.py
python3 scripts/docs/gen_pack_reference.py --check
bash scripts/ci/check-pack-digests.sh
python3 scripts/docs/check_docs_freshness.py --base origin/main
```

Restamp after editing a pack:

```bash
python3 scripts/ci/validate_pack_schemas.py --derive-manifest packs/<pack>
python3 scripts/ci/pack_digest.py --update
python3 scripts/docs/gen_pack_reference.py
```

Spot checks (NFR-004, NFR-005):

```bash
grep -rn "repo-relative .md path\|audience: \.\./" packs/writing packs/internal          # expect only lines labelled legacy
grep -rn "adr/4.x\|adr/3.x\|adr/1.x\|Charter Activation\|StatusGateError\|6 of 565" packs/writing packs/foundation/procedures/adversarial-squad-deployment.procedure.yaml   # expect none
grep -rn "ai-writing-tells" packs | wc -l
```
