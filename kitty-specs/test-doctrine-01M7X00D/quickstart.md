# Quickstart: verify the test-doctrine mission

```bash
uv venv && uv pip install pyyaml==6.0.3 jsonschema==4.26.0 tree-sitter==0.25.2 tree-sitter-java==0.23.5 pytest
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
python3 scripts/ci/pack_digest.py --update packs/<pack>
python3 scripts/docs/gen_pack_reference.py
```

Spot checks:

```bash
spec-kitty charter context --include directive:DIRECTIVE_054
grep -rn "DIRECTIVE_054" packs | wc -l
grep -rn -i "services outside the current module\|DO mock" packs   # expect none
```
