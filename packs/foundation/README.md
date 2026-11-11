# Foundation pack (`foundation`)

The basis of every Spec Kitty project, and a member of the `built-in` distribution.

- **Level:** built-in. **pack_id:** `01M75HSYR9S9KPA372PHGT0EX3`. **Depends on:** nothing.
- **Agent profiles:** `generic-agent` (Generic Giannis, the fallback), `implementer-ivan`,
  `reviewer-renata`, `analyst-annie`, `human-in-charge`.
- **Mission types:** `software-dev`, `plan`, `research`.
- **Doctrine:** every cross-cutting directive with its how-to procedures, tactics and toolguides.

Build on it from another pack with `depends_on` (`range: ">=1.0,<2"`) and reference its artifacts
as `foundation::<kind>:<id>`. Mission roles no installed profile fills (for example `researcher`
without the `planning-analysis` bundle) go to a profile that lists the role as an alt-role (for
example `comms-cleo` or `synthesizer-sam` in `writing`, for `researcher`), else to Generic Giannis.

Carved from `packs/built-in/` by #73; see [PROVENANCE.md](PROVENANCE.md).
