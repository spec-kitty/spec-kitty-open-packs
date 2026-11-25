# Decision Moment `01M88RHDGQSS6R5R5ZCDCH84A2`

- **Mission:** `pack-doctor-alignment-01M88RH1`
- **Origin flow:** `specify`
- **Slot key:** `specify.curation.dedupe`
- **Input key:** `anti_pattern_dedupe`
- **Status:** `resolved`
- **Created:** `2026-11-25T07:08:21.911938+00:00`
- **Resolved:** `2026-11-25T07:23:12.080449+00:00`
- **Opened by:** `cli`
- **Other answer:** `true`

## Question

Dedupe the 273 inline anti-pattern entries (270 distinct titles) only for same-practice duplicates within a pack or an existing depends_on (~265 files), or merge by meaning to ~150 with new cross-pack depends_on?

## Options

- within-pack only (~265 files)
- merge by meaning (~150)
- Other

## Final answer

Merge by MEANING across packs, aiming for ~150 files. Each shared anti-pattern lives in ONE home pack: the most foundational pack upstream of the others, preferring one existing depends_on already reaches. Other packs reject it with a pack-qualified rejects edge (<pack>::anti_pattern:<id>). Add depends_on only where needed, never a cycle. Record every merge in the ledger (merged entries, pack of origin, chosen home, why). A merge whose meanings genuinely differ becomes an operator question. Batch the ledger WPs by HOME pack so the home file exists before any dependent pack's rejects edge. (operator ruling 2026-11-25, relayed by the dispatcher session_01E5wJU9WQgVdyyBRFbVHcGL)

## Rationale

_(none)_

## Change log

- `2026-11-25T07:08:21.911938+00:00` - opened
- `2026-11-25T07:23:12.080449+00:00` - resolved (final_answer="Merge by MEANING across packs, aiming for ~150 files. Each shared anti-pattern lives in ONE home pack: the most foundational pack upstream of the others, preferring one existing depends_on already reaches. Other packs reject it with a pack-qualified rejects edge (<pack>::anti_pattern:<id>). Add depends_on only where needed, never a cycle. Record every merge in the ledger (merged entries, pack of origin, chosen home, why). A merge whose meanings genuinely differ becomes an operator question. Batch the ledger WPs by HOME pack so the home file exists before any dependent pack's rejects edge. (operator ruling 2026-11-25, relayed by the dispatcher session_01E5wJU9WQgVdyyBRFbVHcGL)")
