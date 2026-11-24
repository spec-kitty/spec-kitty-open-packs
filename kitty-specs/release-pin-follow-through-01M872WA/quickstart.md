# Quickstart: verifying this mission locally

```bash
python3 -m unittest discover -s tests/ci            # every CI test
python3 scripts/ci/check_vocabulary.py              # vocabulary lint, incl. self-binding
scripts/ci/validate-packs.sh && scripts/ci/validate-packs.sh --cross-pack
python3 scripts/docs/gen_pack_reference.py --check
python3 -m unittest tests.ci.test_workflows   # the bump boundary and the provenance job (attestation-note was retired, plan Amendment 1)
```

The bump job only runs on `main` of this repository. Its live proof is the first rc.4 run, or an operator dispatch from a fork (#310).
