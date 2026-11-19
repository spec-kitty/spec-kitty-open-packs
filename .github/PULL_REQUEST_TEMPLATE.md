<!--
Use this template for pull requests to spec-kitty-open-packs.

This repository distributes charter *content* (packs) and docs. Charter *logic*
is owned by spec-kitty/spec-kitty-charter — if your change is about resolution,
validation, or the pack schemas, it probably belongs there instead.
-->

## Summary

- Briefly describe the change in 1-3 bullets.

## Type of change

- [ ] New or updated Charter Pack
- [ ] Documentation (guide, README, changelog)
- [ ] Repository scaffolding / tooling
- [ ] Other (describe)

## Pack changes (if applicable)

- Pack name(s):
- [ ] `scripts/ci/validate-packs.sh` passes locally (it validates every pack against the charter pack schemas)
- [ ] Pack digests restamped: `python3 scripts/ci/pack_digest.py --update` and the changed `packs/<pack>.source.yaml` committed (`scripts/ci/check-pack-digests.sh` passes)
- [ ] IDs are namespaced (or intentional built-in overrides are called out)
- [ ] No pack ships executable gate assets, OR the executable surface is declared and the [security position](../SECURITY.md) was reviewed

## New pack (if applicable)

See [Contribute a pack](../docs/guides/contribute-a-pack.md).

- [ ] Agreed in a Pack proposal issue: #
- [ ] `pack_id` is a newly minted ULID, not copied from another pack, and `name` is not used by another pack
- [ ] `README.md` preamble holds only the description; the `docs/packs/` page is regenerated (`python3 scripts/docs/gen_pack_reference.py`), not hand-edited

## Tickets / Contracts

| Ticket | Relationship |
|--------|--------------|
| # | |

## Validation

- [ ] Docs render / links checked
- [ ] Changelog updated under `docs/changelog/CHANGELOG.md`

## Follow-ups

- None.
