# Worked example: an event-sourced work-package board

This example applies the event-sourcing ideas Martin Fowler describes in
[Event Sourcing](https://martinfowler.com/eaaDev/EventSourcing.html) to a setting Spec Kitty
users know: work packages (WPs) moving through the lanes of a mission board. Fowler uses a
different domain; the text and code here are written for this pack.

It shows, in one small Python module (standard library only):

1. lane moves recorded as **versioned, past-tense events** (EVD_001, EVD_003);
2. a **pure domain core** that decides which events happened and touches nothing (EVD_005);
3. an **event-bridge port** with **one canonical writer** behind it (EVD_002);
4. a **projection** that rebuilds the board from the ledger, including "as of" a past point;
5. a **v1 -> v2 contract change** handled by an **upcaster**, with producers emitting only v2
   (EVD_004);
6. an **idempotent consumer** that performs a side effect once per event.

The code blocks below, concatenated in order, form one runnable module. It is a teaching
example, not Spec Kitty's implementation.

## 1. The board and its contract

The lanes are the 4.x lifecycle: `planned -> claimed -> in_progress -> for_review ->
in_review -> approved -> done`. The event type is `WorkPackageMoved`. Its contract has two
versions:

| Version | Payload | Notes |
| --- | --- | --- |
| 1 | `wp`, `lane` | `lane` could hold the alias `doing`; the lane moved from was not recorded. |
| 2 | `wp_id`, `from_lane`, `to_lane`, `reason` | Canonical lane names only. `from_lane` is `null` only on events lifted from v1. |

The ledger already holds v1 events from before the change. Nobody rewrites them.

```python
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Iterable, Protocol

LANES = ("planned", "claimed", "in_progress", "for_review", "in_review", "approved", "done")
ALLOWED = {
    "planned": {"claimed"},
    "claimed": {"in_progress", "planned"},
    "in_progress": {"for_review"},
    "for_review": {"in_review"},
    "in_review": {"approved", "in_progress"},  # approve, or send back for rework
    "approved": {"done"},
    "done": set(),
}
LATEST_VERSION = 2


@dataclass(frozen=True)
class Event:
    """The envelope is the same for every event type; the payload is type-specific."""

    event_id: str
    event_type: str
    schema_version: int
    seq: int  # ordering key, assigned by the one writer
    actor: str
    payload: dict[str, Any]
```

## 2. The domain core decides; it does not write

`decide` takes the current board and a request and returns the events that happened, or
raises a refusal. It performs no I/O, reads no clock and knows nothing about the ledger, so a
test needs nothing but values. The envelope fields the core cannot know (`event_id`, `seq`)
are left for the writer.

```python
class Refused(Exception):
    """The request is not allowed from the current state; no event is produced."""


@dataclass(frozen=True)
class MoveRequest:
    wp_id: str
    to_lane: str
    actor: str
    reason: str | None = None


def decide(board: dict[str, str], request: MoveRequest) -> list[dict[str, Any]]:
    current = board.get(request.wp_id, "planned")
    if request.to_lane not in ALLOWED[current]:
        raise Refused(f"{request.wp_id}: {current} -> {request.to_lane} is not allowed")
    return [{
        "event_type": "WorkPackageMoved",
        "actor": request.actor,
        "payload": {
            "wp_id": request.wp_id,
            "from_lane": current,
            "to_lane": request.to_lane,
            "reason": request.reason,
        },
    }]
```

## 3. One port, one writer

The core's application service hands decided events to an `EventBridge` port. The only
production implementation, `JsonlLedgerWriter`, is the stream's canonical writer: it fills
the envelope, always stamps the **latest** schema version, appends durably, and only then
publishes to subscribers. Nothing else opens the ledger for writing.

```python
class EventBridge(Protocol):
    def emit(self, decided: Iterable[dict[str, Any]]) -> list[Event]: ...


class JsonlLedgerWriter:
    def __init__(self, path: Path, subscribers: Iterable[Callable[[Event], None]] = ()):
        self.path = path
        self.subscribers = list(subscribers)

    def _next_seq(self) -> int:
        if not self.path.exists():
            return 1
        lines = [line for line in self.path.read_text().splitlines() if line.strip()]
        return len(lines) + 1

    def emit(self, decided: Iterable[dict[str, Any]]) -> list[Event]:
        written = []
        seq = self._next_seq()
        with self.path.open("a") as ledger:
            for item in decided:
                event = Event(
                    event_id=f"evt-{seq:04d}",  # a ULID in real code
                    event_type=item["event_type"],
                    schema_version=LATEST_VERSION,  # producers emit only the latest version
                    seq=seq,
                    actor=item["actor"],
                    payload=item["payload"],
                )
                ledger.write(json.dumps(event.__dict__, sort_keys=True) + "\n")
                written.append(event)
                seq += 1
        for event in written:  # publish only after the append is durable
            for subscriber in self.subscribers:
                subscriber(event)
        return written


def move(bridge: EventBridge, board: dict[str, str], request: MoveRequest) -> list[Event]:
    """Application service: decide in the pure core, hand the result to the port."""
    return bridge.emit(decide(board, request))
```

## 4. Upcasting v1 to v2 on read

Old v1 lines stay in the ledger as written. A reader lifts each one to the version it
declares through a chain of pure upcasters. The v1 -> v2 upcaster renames fields, resolves
the `doing` alias, and sets `from_lane` to `null`: v1 never recorded it, and an upcaster must
not guess it from current state, because then replaying the same ledger could give different
answers.

```python
def upcast_wp_moved_v1_to_v2(event: Event) -> Event:
    old = event.payload
    lane = "in_progress" if old["lane"] == "doing" else old["lane"]
    return Event(
        event_id=event.event_id,
        event_type=event.event_type,
        schema_version=2,
        seq=event.seq,
        actor=event.actor,
        payload={"wp_id": old["wp"], "from_lane": None, "to_lane": lane, "reason": None},
    )


UPCASTERS = {("WorkPackageMoved", 1): upcast_wp_moved_v1_to_v2}


def upcast(event: Event, target_version: int) -> Event:
    while event.schema_version < target_version:
        step = UPCASTERS.get((event.event_type, event.schema_version))
        if step is None:
            raise ValueError(f"no upcaster for {event.event_type} v{event.schema_version}")
        event = step(event)
    return event


def read_ledger(path: Path) -> list[Event]:
    events = [Event(**json.loads(line)) for line in path.read_text().splitlines() if line.strip()]
    return sorted(events, key=lambda e: e.seq)
```

## 5. The projection rebuilds the board

The board is not stored anywhere authoritative. It is a fold of the ledger. The projection
declares the one version it is written against (`ACCEPTS`) and gets every older event lifted
to it first. Stopping the fold at a sequence number answers "what did the board look like
then", which is the kind of temporal query Fowler's article highlights.

```python
ACCEPTS = {("WorkPackageMoved", 2)}


def apply(board: dict[str, str], event: Event) -> dict[str, str]:
    if (event.event_type, event.schema_version) not in ACCEPTS:
        version = f"{event.event_type} v{event.schema_version}"
        raise ValueError(f"board projection does not accept {version}")
    updated = dict(board)
    updated[event.payload["wp_id"]] = event.payload["to_lane"]
    return updated


def rebuild_board(path: Path, as_of_seq: int | None = None) -> dict[str, str]:
    board: dict[str, str] = {}
    for event in read_ledger(path):
        if as_of_seq is not None and event.seq > as_of_seq:
            break
        board = apply(board, upcast(event, target_version=2))
    return board
```

## 6. An idempotent consumer performs the side effect

Writing a file, committing to git or posting a notification belongs in a consumer, not in
`decide`. Delivery is at-least-once, so the consumer remembers which event ids it has handled
and does nothing for a duplicate. Replay feeds the projection only; it never calls this
consumer, so rebuilding the board never repeats an effect.

```python
@dataclass
class ReviewQueueNotifier:
    """Side effect: append a line to a review queue file when a WP becomes ready for review."""

    queue: Path
    handled: set[str] = field(default_factory=set)

    def __call__(self, event: Event) -> None:
        if event.event_id in self.handled:
            return  # duplicate delivery: the effect already happened
        if event.event_type == "WorkPackageMoved" and event.payload["to_lane"] == "for_review":
            with self.queue.open("a") as out:
                out.write(f"{event.payload['wp_id']} ready for review ({event.event_id})\n")
        self.handled.add(event.event_id)  # record only after the effect succeeded
```

## 7. Putting it together

```python
def demo(workdir: Path) -> None:
    ledger = workdir / "status.events.jsonl"
    queue = workdir / "review-queue.txt"

    # History written before the v2 contract existed: two v1 lines, one using the alias.
    legacy = [
        Event("evt-0001", "WorkPackageMoved", 1, 1, "alice", {"wp": "WP01", "lane": "claimed"}),
        Event("evt-0002", "WorkPackageMoved", 1, 2, "alice", {"wp": "WP01", "lane": "doing"}),
    ]
    ledger.write_text("".join(json.dumps(e.__dict__, sort_keys=True) + "\n" for e in legacy))

    notifier = ReviewQueueNotifier(queue)
    writer = JsonlLedgerWriter(ledger, subscribers=[notifier])

    board = rebuild_board(ledger)
    assert board == {"WP01": "in_progress"}  # v1 'doing' lifted to the canonical lane

    for request in (
        MoveRequest("WP01", "for_review", "alice"),
        MoveRequest("WP02", "claimed", "bob"),
    ):
        move(writer, board, request)
        board = rebuild_board(ledger)

    assert board == {"WP01": "for_review", "WP02": "claimed"}
    assert rebuild_board(ledger, as_of_seq=2) == {"WP01": "in_progress"}  # temporal query

    try:
        move(writer, board, MoveRequest("WP02", "done", "bob"))
    except Refused:
        pass  # refused in the core: nothing reaches the ledger
    assert len(read_ledger(ledger)) == 4

    # New events are written at v2 only; old lines are untouched v1.
    versions = [e.schema_version for e in read_ledger(ledger)]
    assert versions == [1, 1, 2, 2]

    # A redelivered event does not repeat the side effect.
    redelivered = read_ledger(ledger)[2]
    notifier(redelivered)
    assert queue.read_text().count("WP01 ready for review") == 1


if __name__ == "__main__":
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        demo(Path(tmp))
    print("ok")
```

## How the example maps to the pack

| Pack artifact | Where it shows |
| --- | --- |
| EVD_001 schema version on every event | `Event.schema_version`; `ACCEPTS` and `UPCASTERS` are keyed by `(type, version)`. |
| EVD_002 one canonical writer | `JsonlLedgerWriter` is the only code that appends; the core reaches it through `EventBridge`. |
| EVD_003 immutable past-tense facts | `WorkPackageMoved`; a refused move produces no event, and v1 lines are never rewritten. |
| EVD_004 latest version out, declared versions in | The writer stamps `LATEST_VERSION`; the projection declares `ACCEPTS` and upcasts the rest. |
| EVD_005 side effects in consumers | `decide` is pure; the review-queue file is written by `ReviewQueueNotifier`. |
| EVD_006 shared contracts only | The notifier and the projection read only the envelope and the published payload fields. |
| `evd-event-versioning-and-upcasting` | Section 4. |
| `evd-event-bridge-port` | Sections 2 and 3. |
| `evd-projection-replay` | Section 5, including the `as_of_seq` query. |
| `evd-idempotent-consumer` | Section 6. |

## What a production version adds

- ULIDs for `event_id`, and an ordering key that survives merged copies of a ledger (a
  Lamport clock rather than a line count), with ties broken by event id.
- The writer checks the expected stream position before appending, so two concurrent
  producers cannot both append "the next" event.
- The consumer stores `handled` durably, next to its own state.
- The event contract (schemas per version and an example of each) lives in a package both
  sides import, and the `ACCEPTS` sets are checked against it in CI.
