# Quickstart: verify Test doctrine 2

```bash
export CHARTER_CONTRACT_DIR=<checkout of spec-kitty-charter at the charter.lock.yaml commit>/contracts/packs  # when raw fetch is unavailable
bash scripts/ci/validate-packs.sh
python3 -m pytest -q tests
python3 scripts/ci/check_vocabulary.py
python3 scripts/docs/gen_pack_reference.py --check
bash scripts/ci/check-pack-digests.sh
```

Spot checks: `grep -n "refines" packs/foundation/directive.graph.yaml` shows 041 and 054 refining the paradigm; `grep -rn "Refactor" packs/foundation/tactics/testing/tdd-red-green-refactor.tactic.yaml` shows only the green-mode hand-off.
