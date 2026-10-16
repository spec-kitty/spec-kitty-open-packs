# Specify (caveman)

## Role in the cave-dev lifecycle

This step maps 1:1 to the built-in software-dev `specify` action and inherits its full
contract: the structured discovery interview runs first (the CLI refuses to write substantive
`spec.md` content until the question set is answered), then the spec records WHAT and WHY — not
HOW — for business stakeholders. cave-dev overrides one thing only: the agent's OUTPUT prose,
which it compresses to the caveman voice. Requirement IDs, acceptance criteria, and measurable
thresholds are unchanged from software-dev.

## Bound agent-profile

`analyst-annie` (built-in). cave-dev ships no personas of its own.

## Directive & styleguide citation

- `CAVE_001` (Caveman Terse Output) — governs this step's output prose; enforcement `required`.
- `cave-sty-001-communication` — the voice `CAVE_001` enforces.

## Canonical artifact & template

- Canonical artifact: `spec.md` (blocking at this step).
- Template: inherited from software-dev's `spec-template.md`; cave-dev ships none. The voice
  compresses the connective prose, never the template's required sections.

## Voice at this step

- **The spec is mostly payload — it does not compress.** Requirement IDs (`FR-###`, `NFR-###`,
  `C-###`, `SC-###`, optional lowercase suffix), acceptance criteria, and measurable NFR
  thresholds stay complete and exact. Terseness trims only the connective prose around them.
- **Each requirement: one testable statement.** Outcome first, no throat-clearing. A vague
  requirement fails the "testable and unambiguous" bar.
- **Keep every negation.** A "must not" is a requirement, not filler — reproduce it exactly.
- **The user's words are untouched.** The interview answers and the user's stated intent are the
  authoritative source and are quoted verbatim; never re-voice a requirement the user phrased.
- **Cliff edge → full sentences.** Flag ambiguity explicitly (at most three
  `[NEEDS CLARIFICATION]` markers, critical decisions only) and state scope, non-goals, and
  risks in plain prose — do not telegraph a requirement into ambiguity.
