# Mission Specification: Java conventions rules and one language vocabulary

**Mission Branch**: `feat/java-rules-and-language-vocabulary`
**Created**: 2026-11-12
**Status**: Accepted for planning
**Input**: Issues #204 (java-conventions rules) and #202 (`jvm` vs `java`), both under epic #190. Operator: "both".

## Purpose

The `java` pack (delivered by #198) has two remaining gaps.

1. **A Java project loses its supply-chain guidance.** In the charter service usability run of 2026-11-09, an
   activation with `languages: [java]` filtered out `toolguide:java-supply-chain` (`languageFiltered`). The two Java
   toolguides declare `applies_to_languages: [jvm]`, while the styleguide and the profile declare `java`.
   `applies_to_languages` is a free string in the charter schema, and the service gets no language-family alias (#202
   decision). The fix belongs in the pack data.
2. **`java-conventions` lacks three general rules** that a Java reviewer needs on business code: decimal money with an
   explicit `MathContext`, safe decoding of coded enums, and a codec layer kept apart from the persistence model.

All new content is Spec Kitty-authored under MIT, general-purpose, and not tied to any migration domain.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - A Java project keeps every JVM toolguide in force (Priority: P1)

A team activates the `java` pack with `languages: [java]`.

**Acceptance Scenarios**:

1. **Given** the `java` pack and an activation filtered to `languages: [java]`, **When** the charter resolves it,
   **Then** `toolguide:java-supply-chain` and `toolguide:maven-review-checks` are in force (no `languageFiltered`).
2. **Given** a Kotlin project on Maven or Gradle with `languages: [kotlin]`, **When** the charter resolves the `java`
   pack, **Then** `toolguide:java-supply-chain` is in force (its mechanics are build-tool level). Maven Review
   Checks names Java-only tools (Checkstyle, PIT defaults), so it stays `java` only.
3. **Given** any pack in this repository, **When** `check_vocabulary.py` runs, **Then** no `applies_to_languages`
   entry names a runtime or platform family (`jvm` and its like) instead of a language.

### User Story 2 - A pack author knows which language names to use (Priority: P2)

**Acceptance Scenarios**:

1. **Given** the authoring guide, **When** an author fills `applies_to_languages`, **Then** the guide states the
   rule: the language's own lowercase name, one entry per language, never a runtime family, and an empty list for
   language-neutral content.

### User Story 3 - A Java reviewer gets the three business-code rules (Priority: P1)

**Acceptance Scenarios**:

1. **Given** `java-conventions`, **When** a reviewer checks money arithmetic, **Then** a principle and a pattern
   require `BigDecimal` with an explicit `MathContext` (or scale) and `RoundingMode`, never `double`/`float`, and
   comparison by `compareTo`.
2. **Given** `java-conventions`, **When** a reviewer checks how a stored or wire code becomes an enum, **Then** a
   principle and a pattern require a `fromCode`/`fromByte` factory that throws a named exception on an unknown value,
   never `values()[ordinal]` or a silent default.
3. **Given** `java-conventions`, **When** a reviewer checks a positional or wire-format record, **Then** an
   anti-pattern refuses JPA `@Entity` mapped straight over the layout and shows a codec plus an explicit mapper.

### Edge Cases

- The new principle names must be unique within the list (ADR-0067); the names must not collide with existing ones.
- Bumping `java` must not break dependants: no pack in this repository depends on `java` today; check again.
- The `java` tree digest sidecar (`packs/java.source.yaml`, #194) must be regenerated.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `java-supply-chain` declares `applies_to_languages: [java, kotlin]`; `maven-review-checks` declares
  `[java]`. (#202)
- **FR-002**: No artifact under `packs/` names `jvm` (or another runtime family) as a language; `check_vocabulary.py`
  refuses it, with a unit test. (#202)
- **FR-003**: The authoring guide records the language vocabulary rule. (#202)
- **FR-004**: `java-conventions` gains the money, enum-decoding and codec-separation rules as principles with a
  pattern or anti-pattern each, with bad and good examples. (#204)
- **FR-005**: `java` is bumped a minor version (2.0.0 → 2.1.0); the CHANGELOG gets a "Changed" entry (#204) and a
  "Fixed" entry (#202).
- **FR-006**: Generated pack pages and the `java` digest sidecar are regenerated, never hand-edited.

### Non-Functional Requirements

- **NFR-001**: Gates green: `validate-packs.sh`, `check-pack-digests.sh`, `check-built-in.sh`, the charter service
  check, `check_vocabulary.py`, `gen_pack_reference.py --check` (for the pages this change touches),
  `python3 -m unittest discover`, docs-site build.

## Success Criteria *(mandatory)*

- **SC-001**: Every Java toolguide is in force for `languages: [java]`.
- **SC-002**: Zero `jvm` language entries in `packs/`, and the guard refuses a new one.
- **SC-003**: The three rules appear in `java-conventions`, each with an example a reviewer can act on.

## Out of scope

- #211 (presets for the stack packs), #17 (compound stacks: under separate dialectical research).
- The repo-wide generated-page drift reported by the 2026-11-12 triage, beyond the pages this mission touches.

## Assumptions

- Kotlin is listed on the supply-chain toolguide only, as #202 suggests ("also `kotlin` if it is meant to cover other
  JVM languages"); its commands are Maven/Gradle-level and language-agnostic.
