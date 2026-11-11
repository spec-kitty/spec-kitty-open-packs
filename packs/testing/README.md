# Testing pack (`testing`)

Test design and test-first practice beyond the foundation basics: BDD and specification by example, test minimisation and reconstruction, mutation testing, Gherkin, and the debugging profile.

- **Level:** built-in. Aggregated by `built-in` (exact `==2.0.0` pin); read-only to registration.
- **pack_id:** `01M75PCTC6HS38NX8HJGT26VTP`
- **Depends on:** `foundation`
- **Contents:** 9 tactics, 5 procedures, 5 styleguides, 2 paradigms, 1 agent profile, 1 directive, 1 toolguide.
- **Agent profiles:** `debugger-debbie`.

## Adopt

Place the pack beside `built-in` and its dependencies (see `depends_on` in `pack.yaml`; it is not registered at org level), then activate what you
need per project with `spec-kitty charter activate ...`. Reference its artifacts from another pack as
`testing::<kind>:<id>`.

## Provenance

Carved from `packs/built-in/` by #73; see [PROVENANCE.md](PROVENANCE.md).
