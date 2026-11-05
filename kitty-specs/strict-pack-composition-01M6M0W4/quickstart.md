# Quickstart: verifying strict pack composition

Local gates, from the repository root (`PY` must have `pyyaml` and `jsonschema`; `~/Documents/code/kitty/spec-kitty/.venv/bin` works here):

```bash
export PATH=~/Documents/code/kitty/spec-kitty/.venv/bin:$PATH
python -m unittest discover -s tests/ci
python -m unittest discover -s tests/docs
bash scripts/ci/validate-packs.sh
bash scripts/ci/check-built-in.sh
```

Real compose, from a spec-kitty-charter worktree, against a local open-packs checkout:

```bash
JAVA_HOME=/usr/lib/jvm/temurin-25 ./gradlew :packs:test --tests '*<ComposeTest>*' \
  -PopenPacksDir=<path to this repository>
```

Mission runtime on migrated content (C-005): run `spec-kitty charter context --action plan --json`, `spec-kitty dispatch` and `spec-kitty next --mission <handle> --json` in a scratch copy whose `packs/` holds the migrated tree.
