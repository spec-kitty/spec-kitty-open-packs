# Rust

An opt-in org stack pack with general-purpose Rust doctrine for teams that build in Rust under Spec
Kitty.

| Artifact | Kind | What it gives an agent |
| --- | --- | --- |
| `rust-conventions` | styleguide | How to write the code: validated newtypes, parsing at the boundary, `thiserror` in libraries and `anyhow` at binary edges, money as a decimal or a currency-carrying minor-units type, exhaustive matches, documented `unsafe`, `///` docs. Each rule comes with bad and good examples. |
| `rust-review-checks` | toolguide | What to run before approving: `cargo fmt`, `clippy -D warnings`, tests and doc-tests, `cargo doc`, `cargo deny` / `cargo audit`, and where they apply `cargo hack`, `cargo semver-checks`, Miri and `cargo mutants`. Cheapest first. |
| `rust-ruben` | agent profile | A Rust implementer that requires `rust-conventions` and self-reviews with `rust-review-checks`. |
| `rust` | preset | Puts the three above in force. |

## Adopt

Register the pack in `.kittify/config.yaml`, pinned to a release tag or commit (never a branch), with
the packs it depends on, `foundation` and `testing` (see
[Compose packs](../../docs/guides/compose-packs.md)):

```yaml
charter_packs:
  org:
    packs:
      - name: rust
        local_path: "${SPEC_KITTY_PACK_HOME}/rust"
        source_type: git
        url: "https://github.com/spec-kitty/spec-kitty-open-packs.git"
        ref: "<vX.Y.Z release tag or commit SHA>"   # never a branch
        subdir: packs/rust
      # and its dependencies, the same way: foundation (subdir packs/foundation)
      # and testing (subdir packs/testing), at the same ref
```

Then fetch the pack and put its doctrine in force:

```bash
spec-kitty charter fetch --pack rust
spec-kitty charter activate --pack rust --preset rust
```

The pack's `org-charter.yaml` activates nothing, so registering the pack alone changes nothing. See
[Use a Charter Pack](../../docs/guides/use-a-charter-pack.md).

`built-in` does not include this pack. Stack packs are opt-in
([#73](https://github.com/spec-kitty/spec-kitty-open-packs/issues/73)).

## Not covered

- Framework-specific guidance (async runtimes, web frameworks, ORMs) beyond what the conventions
  say about keeping them at the adapters.
- Embedded and `no_std` specifics.
- Release and publishing workflow.

Where the content came from: [PROVENANCE.md](PROVENANCE.md).
