# Provenance: spec-kitty-internal Charter Pack (canonical home)

This is the **canonical home** of the in-house (org-tier) **internal** Charter
Pack. It is registered for `spec-kitty-open-packs`' own governance via
`.kittify/config.yaml` → `charter_packs.org.packs`, and it is the source other
repositories vendor from.

## Identity is minted and owned here

`pack.yaml` pins the canonical `pack_id`. `spec-kitty-open-packs` is the single
minting authority for the `spec-kitty-internal` identity. Downstream repositories
that need this pack (for example `spec-kitty-charter`) hold a **vendored mirror**:
they copy this `pack_id` verbatim and must never re-mint or diverge it.

## Mirrors

- `spec-kitty-charter` carries a vendored mirror of this pack (tracked by
  `spec-kitty-charter#37`). Changes land here first; the mirror is re-vendored to
  match.
