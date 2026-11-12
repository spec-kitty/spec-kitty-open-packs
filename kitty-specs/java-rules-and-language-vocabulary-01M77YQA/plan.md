# Implementation Plan: Java conventions rules and one language vocabulary

**Branch**: `feat/java-rules-and-language-vocabulary` | **Date**: 2026-11-12 | **Spec**: [spec.md](spec.md)
**Input**: Mission specification from `kitty-specs/java-rules-and-language-vocabulary-01M77YQA/spec.md`

## Summary

Content-only change to the `java` org pack plus one narrow guard. Fix the toolguides' `jvm` language tag (#202),
refuse runtime-family language names in `check_vocabulary.py`, document the vocabulary rule, and add three
business-code rules to `java-conventions` (#204). Bump `java` to 2.1.0, restamp its digest, regenerate its page.

## Technical Context

- **Artifacts**: YAML under `packs/java/` validated against the charter pack schemas pinned in `charter.lock.yaml`.
- **Guard**: `scripts/ci/check_vocabulary.py` (stdlib only, scans tracked `packs/` text files) with unit tests in
  `tests/vocabulary/`.
- **Generated outputs**: `packs/java.source.yaml` (`scripts/ci/pack_digest.py --update`), `docs/packs/java.md`
  (`scripts/docs/gen_pack_reference.py`). Never hand-edited.
- **Constraints**: principle `description` 1-255 characters, names unique ignoring case (ADR-0067). No pack depends
  on `java`, so a minor bump moves no dependant range.

## Charter Check

- DIRECTIVE_003: no new architectural decision; the vocabulary rule implements #202's recorded decision (no service
  alias, pack data uses one vocabulary). No ADR needed.
- DIRECTIVE_041: the guard protects a real failure (a Java project silently losing guidance), so it earns a test.
- DIRECTIVE_044: the doc states the rule; the guard's family list is the generated-evidence side, so the doc names
  the rule and points to the guard instead of restating its list.
- Changelog entry for user-facing change: yes ("Changed" for #204, "Fixed" for #202).

## Design decisions

1. **Language names**: `java-supply-chain` → `[java, kotlin]` (Maven/Gradle mechanics are language-agnostic on the
   JVM); `maven-review-checks` → `[java]` (Checkstyle, SpotBugs/PIT configuration is Java-oriented).
2. **Guard shape**: a `RUNTIME_FAMILY_LANGUAGES` set (`jvm`, `dotnet`, `clr`, `beam`, `node`, `nodejs`, `web`)
   refused when it appears as a list entry under `applies_to_languages:` (block or flow form). Line-based, stdlib.
3. **Rules in `java-conventions`**: three principles ("Decimal money with an explicit MathContext", "Decode coded
   values through a checked factory", "Keep the wire codec out of the persistence model"), plus two patterns
   (money, enum decoding) and one anti-pattern (`@Entity` over a wire layout), each with bad and good examples.

## Work packages

- **WP01 – language vocabulary (#202)**: toolguide tags, guard + tests, authoring-guide section.
- **WP02 – java-conventions rules (#204)**: three principles, patterns and anti-pattern; version bump; digest; page;
  CHANGELOG.

## Risks

- Generated-page drift on clean `main` (triage record): only regenerate `docs/packs/java.md`; verify `--check`
  for it and report the pre-existing drift elsewhere as out of scope.
