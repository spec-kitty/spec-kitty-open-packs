# Quickstart: verifying the split

```bash
export CHARTER_CONTRACT_DIR=<charter checkout at the lock pin>/contracts/packs   # local only; CI fetches it
scripts/ci/validate-packs.sh
scripts/ci/check-built-in.sh
JAVA_HOME=/usr/lib/jvm/temurin-25 python3 scripts/ci/charter_service_check.py   # needs the service jar for the pin
python3 scripts/ci/check_vocabulary.py
python3 scripts/docs/gen_pack_reference.py --check
for d in tests/*/; do python3 -m unittest discover -s "$d" -t . ; done
```

Re-run the migration (idempotent; it refuses to run if `packs/built-in` no longer holds the artifacts):

```bash
python3 kitty-specs/foundation-writing-split-01M75HV3/tools/split_built_in.py --membership kitty-specs/foundation-writing-split-01M75HV3/membership.json
```
