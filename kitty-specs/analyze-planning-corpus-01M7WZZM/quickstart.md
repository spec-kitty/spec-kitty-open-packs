# Quickstart: validating the analyze changes

## Gates (from the repository root)

```bash
uv venv && uv pip install pyyaml==6.0.3 jsonschema==4.26.0 tree-sitter==0.25.2 tree-sitter-java==0.23.5 pytest
.venv/bin/python -m pytest -q tests/ci/test_analyze_readiness_prompts.py
.venv/bin/python -m pytest -q tests
bash scripts/ci/validate-packs.sh
.venv/bin/python scripts/ci/check_vocabulary.py
.venv/bin/python scripts/docs/gen_pack_reference.py --check
bash scripts/ci/check-pack-digests.sh
.venv/bin/python scripts/docs/check_docs_freshness.py --base origin/main
wc -l packs/foundation/missions/software-dev/steps/analyze.prompt.md   # ≤ 500
```

## Validation scenarios

1. **Corpus inputs named** (US1, FR-001/FR-002): the analyze prompt's step 1 names `artifact_files`, `artifact_dirs` (every entry not already loaded, except `feature_dir`), `meta.json` and `occurrence_map.yaml` (`available_docs` is not relied on) with `purpose_tldr`, `purpose_context`, `source_description`.
2. **Planning-artifact pass** (US1, FR-003/FR-004/FR-005): pass H cites tactic `planning-corpus-consistency`; the tactic names research/plan decisions, data model, contracts, quickstart, `occurrence_map.yaml`, other inventory artifacts and ungrounded behaviour.
3. **Coherence pass** (US2, FR-006..FR-008): pass J cites tactic `product-coherence-review`; severity says MEDIUM or LOW only; the Product Coherence section ends with the `Recommendation:` line; Next Actions repeats it.
4. **Report shape** (FR-009..FR-011, FR-013): prefix table has `X` and `M`, all prefixes unique; passes H and J, no pass I; sections in order … Scenario Audit, Intent & Planning-Artifact Consistency, Product Coherence, Clarification Questions …; the Scenario Audit table has a `Finding` column.
5. **cave-dev parity** (US5, FR-015): the cave-kitty analyze prompt names both tactics, the cap and the recommendation line.
6. **Read-only** (C-001): `writing_finalize_lines` stays empty for both prompts.

## Manual dry run (optional)

Run `/spec-kitty.analyze` on this mission after `/spec-kitty.tasks`: the report must include both new sections and the recommendation line, and record as `ready` when only `M` findings exist.
