# `event-driven` — Event-Driven Design Charter Pack

An open Spec Kitty Charter Pack for building systems where **events are the source of truth**
and state is a projection of them. It encodes the rules Spec Kitty's own core is moving to:
one canonical event writer behind an event-bridge port, a schema version on every event,
producers that emit the latest version and consumers that choose which versions they accept,
a pure domain core with side effects (git, filesystem, network) running in event consumers,
and producers and consumers that share nothing but published event contracts:

```
domain core --decides--> EventBridge port --> canonical writer --> ledger --> subscribers
  (pure)                                        (one per stream)   (truth)    projections, side effects
```

The pack names no framework, broker or storage. A JSONL file with one writer qualifies as a
ledger as much as an event store does.

## What ships

| Kind | Artifacts |
| --- | --- |
| Paradigm | `evd-event-sourced-design` — events as the source of truth, state as a projection |
| Directives | `EVD_001` every event carries a schema version · `EVD_002` one canonical writer per stream · `EVD_003` events are immutable past-tense facts · `EVD_004` producers emit the latest version, consumers declare what they accept · `EVD_005` side effects live in consumers · `EVD_006` share only published event contracts |
| Tactics | `evd-event-versioning-and-upcasting`, `evd-event-bridge-port`, `evd-projection-replay`, `evd-idempotent-consumer` |
| Styleguide | `evd-event-naming-and-payload` |
| Glossary | `evd-glossary` — event, event stream, ledger / event log, projection, replay, upcaster, schema version, publisher, subscriber, canonical writer, at-least-once and at-most-once delivery |
| Asset | `evd-worked-example-lane-board` — a worked example after Martin Fowler's [Event Sourcing](https://martinfowler.com/eaaDev/EventSourcing.html): work packages moving through Spec Kitty lanes as versioned events, a projection that rebuilds the board (also "as of" a past point), a v1 -> v2 change handled by an upcaster, and an idempotent consumer. Markdown with a runnable, standard-library Python listing; it ships no executable file. |
| Preset | `event-driven` — activates the paradigm, the six directives, the four tactics and the styleguide |

Built-in doctrine is referenced, not restated. The DRG fragment links to the built-in
`domain-event-capture` and `anti-corruption-layer` tactics, the `event-storming-discovery`
procedure, `reference-architectural-patterns`, and the `domain-driven-design` and
`deep-module-design` paradigms.

## Adopt

Requires Spec Kitty 4.x with the Charter Pack cutover (`spec-kitty charter pack validate --help`
works). Register the pack in the consuming project's `.kittify/config.yaml`, pinned to a
release of this repository:

```yaml
charter_packs:
  org:
    packs:
      - name: event-driven
        local_path: "${SPEC_KITTY_PACK_HOME}/event-driven"
        source_type: git
        url: "https://github.com/spec-kitty/spec-kitty-open-packs.git"
        ref: "<commit SHA or pack/event-driven/vX.Y.Z tag>"   # never a branch; SPEC_KITTY_PACK_HOME is any directory
        subdir: packs/event-driven
```

Then:

```bash
spec-kitty charter fetch --pack event-driven
spec-kitty doctor charter-packs                       # pack healthy, no dangling endpoints
spec-kitty charter activate --pack event-driven --preset event-driven
spec-kitty charter context --include directive:EVD_002
spec-kitty charter pack asset path evd-worked-example-lane-board
```

The pack activates nothing by itself. To make the rules binding for every mission instead of
opt-in per project, list them in the consuming org's charter:

```yaml
required_directives: [EVD_001, EVD_002, EVD_003, EVD_004, EVD_005, EVD_006]
```

## Status

Pre-release, net-new content (not carved from the built-in corpus). `charter pack validate`
and `charter org validate` report 0 errors and 0 advisories against the spec-kitty commit
pinned in CI, and `doctor charter-packs` loads it beside the other packs in this repository
with no collisions and no dangling endpoints. The worked example's code runs as printed
(its assertions pass) and is clean under `ruff` and `mypy --strict`. Not yet proven: the
pack governing a real mission.
