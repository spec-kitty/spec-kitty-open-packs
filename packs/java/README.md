# Java pack (`java`)

The Java stack: the Java Jenny profile, Java conventions, Maven review checks and Java supply-chain guidance. The supply-chain guidance also applies to Kotlin on Maven or Gradle.

## Contents

- **Contents:** 2 toolguides, 1 agent profile, 1 styleguide.
- **Agent profiles:** `java-jenny`.

## Who opts in

Java teams, and the enterprise packs built on Java.

## Adopt

Register the pack and its dependencies (see `depends_on` in `pack.yaml`), then activate what you
need per project with `spec-kitty charter activate ...`. Reference its artifacts from another pack as
`java::<kind>:<id>`.

## Provenance

Every artifact in this pack was carved out of `packs/built-in/` by #73 (mission
`kitty-specs/foundation-writing-split-01M75HV3/`), with `git mv`, so `git log --follow <file>` shows
its full history. The ids and content are unchanged; only cross-pack references were qualified and
graph edges re-homed (see that mission's `research.md`, D4 and D11).

`packs/built-in/` was itself seeded from spec-kitty core (`packs/built-in` at commit
`f166339300dfe207ea7635a285e498beb877f1a0`, 2026-10-19) and has been authored in this repository since;
see `packs/built-in.source.yaml`.
