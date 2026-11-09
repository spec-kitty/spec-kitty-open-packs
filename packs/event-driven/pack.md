# event-driven Charter Pack

An open Spec Kitty Charter Pack for building systems where events are the source of truth and
state is a projection of them: one canonical event writer behind an event-bridge port, a schema
version on every event, producers that emit the latest version and consumers that choose which
versions they accept, a pure domain core with side effects running in event consumers, and
producers and consumers that share nothing but published event contracts.

The pack names no framework, broker or storage. A JSONL file with one writer qualifies as a
ledger as much as an event store does.
