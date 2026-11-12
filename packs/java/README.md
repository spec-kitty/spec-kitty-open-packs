# Java pack (`java`)

The Java stack: the Java Jenny profile, Java conventions, Maven review checks and Java supply-chain guidance. The supply-chain guidance also applies to Kotlin on Maven or Gradle.

- **Level:** org (opt-in). Not aggregated by `built-in`.
- **pack_id:** `01M75PCTK534T6D38GECDYXYG0`
- **Depends on:** `foundation`, `testing`
- **Contents:** 2 toolguides, 1 agent profile, 1 styleguide.
- **Agent profiles:** `java-jenny`.

## Adopt

Register the pack and its dependencies (see `depends_on` in `pack.yaml`), then activate what you
need per project with `spec-kitty charter activate ...`. Reference its artifacts from another pack as
`java::<kind>:<id>`.

## Provenance

Carved from `packs/built-in/` by #73; see [PROVENANCE.md](PROVENANCE.md).
