# Data model: Strict pack composition

No new data structures. These are the file shapes the mission relies on; `contracts/packs` in spec-kitty-charter owns them.

## Pack descriptor (`pack.yaml`)

| Field | Rule |
|---|---|
| `pack_id` | ULID, generated once, unique across packs, never edited |
| `pack_version` | `1.0.0` |
| `parent_pack` | `null` |
| `name` | The qualifier: `quality-assurance`, `event-driven`, `cave-kitty`; existing `built-in`, `spec-kitty-internal` unchanged |
| `pack_level` | `org` (required when `depends_on` is present) |
| `active_charter`, `pack_drg` | As in `packs/internal/pack.yaml`, where the file exists |
| `depends_on` | `[{pack_id: 01ARWG13C000000000000000FG, range: ">=1.0,<2"}]`, by ULID, not name |

## References

| Where | Bare form | Qualified form |
|---|---|---|
| Graph edge end | `tactic:foo` | `built-in::tactic:foo` |
| Typed reference `id` | `foo` | `built-in::foo` |

**Invariants**

- A reference to the pack's own artifact stays bare.
- A bare reference no pack holds is not refused, and stays as it is.
- A qualified reference names a pack in the referrer's `depends_on` closure, and that pack holds the artifact.
- The dependency graph is a star: org packs point at `built-in`; nothing else.

## Gate state

`PENDING_PACKS` in `validate_pack_schemas.py`: directories still allowed bare cross-pack references. It only shrinks, and it does not exist at the end of the mission.
