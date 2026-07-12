# Security Position: Spec Kitty Open Packs

**Last updated**: 2026-07-12
**Status**: Work in progress — this repository is an early, evolving product direction (see [README](README.md)).

## What this repository is

`spec-kitty-open-packs` distributes **doctrine content** — YAML artifacts (directives,
tactics, styleguides, paradigms, procedures, toolguides, agent profiles) plus, over time,
shared **pack-validation code** that pack authors can reuse. Doctrine content is data that
Spec Kitty resolves into agent context; it does not, by itself, execute.

## Trust surface

Most doctrine artifacts are inert data. Two categories carry a real trust surface and are
treated with care here:

1. **Executable gate assets.** As the doctrine-controlled transition-gate work matures
   (see [`Priivacy-ai/spec-kitty#2535`](https://github.com/Priivacy-ai/spec-kitty/issues/2535)
   and the trust epic [`#2539`](https://github.com/Priivacy-ai/spec-kitty/issues/2539)),
   packs may ship code that runs behind a trust envelope. Any such asset in this repository
   must declare its executable paths and requirements, and consumers are warned at
   activation time.
2. **Pack integrity.** Pack authors and operators need provenance and tamper-evidence
   before running third-party doctrine. Content-hash integrity and a graduated trust signal
   (built-in / org-pack / third-party / verified) are tracked upstream and will be reflected
   in this repository's authoring and validation guidance as they land.

## Reporting

Report suspected security issues (a malicious pack, an integrity concern, or an
unconfined executable asset) privately to the maintainers rather than opening a public
issue. See the upstream [Spec Kitty security position](https://github.com/Priivacy-ai/spec-kitty/blob/main/SECURITY-POSITION.md)
for the broader core stance.

## Operator guidance

- Pin pack versions (git tag or commit SHA) in consumer `.kittify/config.yaml`.
- Review a pack's contents before activation; prefer packs whose IDs are namespaced and
  whose artifacts are inert data.
- Run any AI coding agent under your organization's approved sandbox / approval / network
  controls, independent of the doctrine it loads.
