# Implementation Plan: Content audit P2

**Branch**: `fix/content-audit-p2-266-270` | **Date**: 2026-11-19 | **Spec**: [spec.md](spec.md)

## Summary

Five content-only slices of epic #263, one per pack, so the work packages touch disjoint files and can proceed in parallel. No schema, tooling or charter change. Each slice is checked against `spec-kitty-cli 4.0.0rc9`, then the generated pack pages and the pack digests are refreshed once, centrally.

## Technical Context

- **Content**: YAML artefacts and Markdown prompts, templates and toolguides under `packs/`.
- **Contracts**: charter pack schemas at the commit pinned in `charter.lock.yaml`.
- **Gates**: `scripts/ci/validate-packs.sh`, the charter service job, `scripts/ci/check_vocabulary.py`, `scripts/docs/gen_pack_reference.py --check`, `scripts/ci/check-pack-digests.sh`, and `pytest tests` (including `test_software_dev_ascii.py`).

## Decisions (operator rulings, 2026-11-19)

| # | Decision | Default |
|---|----------|---------|
| D1 | Bundling | One Mission, one PR, one WP per issue |
| D2 | #277 | Folded in: all eight listed files, glossary included, name `spec-kitty agent action implement`; this PR closes #277 |
| D3 | `charter context` in implement/review | Keep the bootstrap substep; the prompt says not to reload it for the same action |
| D4 | Software-dev template copies in documentation | Delete |
| D5 | Placeholder convention | Templates keep `{PLACEHOLDER}` slots; generate fills each or writes `[TODO: <what is missing>]`; validate greps for both; `[NEEDS CONTENT: ...]` retired (overrules the recommendation) |
| D6 | What `blocking` enforces | Verify from the rc9 runtime, time-boxed; dated statement |
| D7 | `base` preset description | "every project whose closure holds this pack" |

## Work packages

| WP | Issue | Pack | Files |
|----|-------|------|-------|
| WP01 | #266, #277 | foundation (+ cave-kitty README) | software-dev mission type, steps, tactics, toolguide, glossary |
| WP02 | #267 | writing | common-docs directive, styleguides, tactics, new lint toolguide |
| WP03 | #268 | writing | documentation mission type, steps, templates |
| WP04 | #269 | qa | qa mission templates, steps, toolguides, directive, procedures, README |
| WP05 | #270 | internal | base must-have procedures, skills, toolguides, docs-conventions directive |
| WP06 | all | repo | regenerate `docs/packs/`, restamp digests, changelog |

WP02 and WP03 share the writing pack and are done together.

## Risks

- **Overlap with epics #207 and #244** on the same software-dev and writing files: there are no open PRs at plan time, so no conflict now. This PR lands first, per the epic's order.
- **Docs drift** between this PR and another pack PR: fix it with a follow-up (CONTRIBUTING).
