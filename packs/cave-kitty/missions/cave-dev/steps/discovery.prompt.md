# Discovery (caveman)

## Role in the cave-dev lifecycle

This step maps 1:1 to the built-in software-dev `research` action and inherits its full
contract — investigate the area the Mission will change before a spec exists, record decisions
with rationale, evidence, and open questions. cave-dev overrides one thing only: the agent's
OUTPUT prose, which it compresses to the caveman voice. The engineering rigour, the artifact
locations, and the discovery discipline are unchanged from software-dev.

## Bound agent-profile

`researcher-robbie` (built-in). cave-dev ships no personas of its own — it re-voices the
software-dev lifecycle, it does not re-staff it.

## Directive & styleguide citation

- `CAVE_001` (Caveman Terse Output) — governs this step's output prose; enforcement `required`.
- `cave-sty-001-communication` — the voice `CAVE_001` enforces.

## Canonical artifact & template

- Canonical artifact: none required. Findings may be written into or extend
  `<mission_dir>/research.md` (never truncate existing content); this step authors no
  cave-dev-specific artifact of its own. Do not invent one.
- Template: inherited from software-dev; cave-dev ships none. The voice applies to prose, not to
  document structure.

## Voice at this step

- **Finding first, then evidence.** One line per finding, outcome before narration.
- **Quoted source is a payload — verbatim.** Code, paths, log lines, symbols, line numbers:
  character for character. Terseness never touches a payload.
- **Keep every negation.** A thing that does NOT happen is a finding too — say "not", "never",
  "no". A dropped negation inverts the finding.
- **Cliff edge → full sentences.** A risk, a destructive discovery, or ground you are unsure of
  is stated in plain prose: what the risk is, what it depends on, what to do.
- Name the gaps and open questions plainly; do not smooth them over to save tokens.
