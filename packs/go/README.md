# Go

An opt-in org stack pack with general-purpose Go doctrine for teams that build in Go under Spec Kitty.

| Artifact | Kind | What it gives an agent |
| --- | --- | --- |
| `go-conventions` | styleguide | How to write the code: typed constants with a validated parse, errors wrapped with `%w` and matched with `errors.Is`/`errors.As`, `context.Context` first, an explicit dependency struct instead of package globals, money as a decimal or minor units with its currency, `defer` for cleanup, owned goroutines, table-driven tests. Each rule comes with bad and good examples. |
| `go-review-checks` | toolguide | What to run before approving: `gofmt`, `go vet`, `staticcheck` or `golangci-lint`, `go test -race`, fuzzing, `govulncheck`, `go mod verify`. Cheapest first. |
| `go-gwen` | agent profile | A Go implementer that requires `go-conventions` and self-reviews with `go-review-checks`. |
| `go` | preset | Puts the three above in force. |

## Adopt

Register the pack in `.kittify/config.yaml`, pinned to a release tag or commit (never a branch), with
the packs it depends on, `foundation` and `testing` (see
[Compose packs](../../docs/guides/compose-packs.md)):

```yaml
charter_packs:
  org:
    packs:
      - name: go
        local_path: "${SPEC_KITTY_PACK_HOME}/go"
        source_type: git
        url: "https://github.com/spec-kitty/spec-kitty-open-packs.git"
        ref: "<vX.Y.Z release tag or commit SHA>"   # never a branch
        subdir: packs/go
      # and its dependencies, the same way: foundation (subdir packs/foundation)
      # and testing (subdir packs/testing), at the same ref
```

Then fetch the pack and put its doctrine in force:

```bash
spec-kitty charter fetch --pack go
spec-kitty charter activate --pack go --preset go
```

The pack's `org-charter.yaml` activates nothing, so registering the pack alone changes nothing. See
[Use a Charter Pack](../../docs/guides/use-a-charter-pack.md).

`built-in` does not include this pack. Stack packs are opt-in
([#73](https://github.com/spec-kitty/spec-kitty-open-packs/issues/73)).

## Not covered

- Framework-specific guidance (web frameworks, ORMs, RPC stacks).
- cgo and platform-specific build concerns.
- Release and module-publishing workflow.

Where the content came from: [PROVENANCE.md](PROVENANCE.md).
