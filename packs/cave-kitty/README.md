# `cave-kitty` — Caveman Communication Charter Pack

An open Spec Kitty Charter Pack that makes an agent answer in a **compressed, token-saving
"caveman" voice** — outcome-first, filler cut — while keeping every payload and every negation
exact and restoring full sentences at a cliff edge.

> **Scope note.** The styleguide and directive are complete and usable today, and are the clean
> instrument for the pack's purpose (see "Which path for a token A/B?" below). The `cave-dev`
> mission type **re-states the built-in `software-dev` step contract as prose** and overrides one
> thing only — the agent's output prose, which it compresses to the caveman voice. Its eight
> command templates follow the same structured shape the canonical `qa` open pack uses (role +
> software-dev mapping, bound built-in profile, directive & styleguide citation, artifact/template
> binding, and the per-step voice specialization). cave-dev deliberately ships no templates and no
> personas of its own: the voice applies to prose, not to document structure, and not to the
> engineering rigour, which is `software-dev`'s.
>
> **Runtime caveat.** "Re-states the contract" is a documentation relationship, not a runtime one.
> Under `spec-kitty next`, the per-WP iteration and the step guards the loop runs for
> `implement`/`review`, and the analysis-currency gate ahead of `implement`, are keyed to the
> built-in `software-dev` family in the CLI and do **not** fire for a `cave-dev`-typed mission —
> its `implement`/`review` steps advance as generic single-shot DAG steps. The lane/worktree
> execution path (`spec-kitty implement WP##`) is unaffected. For a WP-iterating, guarded run in
> the caveman voice, use the voice-activation path (`--type software-dev` + activate the voice).

## What it is — and isn't

Inspired by the [`caveman`](https://github.com/JuliusBrussee/caveman) token-saving instruction
set. This pack captures caveman's **communication-voice rules** as Spec Kitty doctrine,
authored fresh under this repository's MIT licence. It does **not** reproduce caveman's runtime
`/caveman` toggle, its CLI proxy, or its input/log/JSON compression ("rocks") — those are
*tooling*, not doctrine. A Spec Kitty styleguide/directive is advisory context an agent applies
when it writes; it is not an enforced runtime switch.

## What ships

| Kind | Artifact | Purpose |
| --- | --- | --- |
| Styleguide | `cave-sty-001-communication` | The caveman voice: answer-first, exact payloads, kept negations, cliff-edge exceptions, user's words untouched. |
| Directive | `CAVE_001` (`cave-001-terse-output`) | Makes the voice an enforceable rule over the agent's **output prose** (never the user's text or any payload). |
| Mission type | `cave-dev` | The software-dev lifecycle re-voiced — same eight canonical steps and the same engineering rigour, caveman output prose. Governance profile selects the styleguide + directive. |

## Does activating this make `software-dev` caveman?

Two layers, kept separate on purpose:

- **Activate the styleguide and/or `CAVE_001`** → the agent *writes* caveman while you keep
  running `--type software-dev`. The built-in prompts are unchanged; only the output voice is.
- **Run `--type cave-dev`** → you select the re-voiced lifecycle. `software-dev` itself stays
  byte-identical. This pack deliberately does **not** override the built-in `software-dev`
  prompts, so activation never silently mutates the canonical type. Note the runtime caveat in the
  scope note above: `--type cave-dev` does not inherit software-dev's `next`-loop WP iteration or
  guards.

## Which path for a token A/B?

The pack exists to measure the caveman voice's token impact against a software-dev baseline. Use
the **voice-activation path** for that: run `--type software-dev` once as the baseline and once
with `CAVE_001` + the styleguide activated. The only variable that changes is the output voice —
same input prompts, same runtime, same WP machinery — so any token delta is attributable to the
voice.

Do **not** A/B `--type cave-dev` against `--type software-dev`: that confounds three variables at
once — the output voice, a smaller and lossy *input* prompt corpus, and (per the runtime caveat) a
structurally different `implement`/`review`. cave-dev's input-prompt shrinkage is a separate,
deliberate experiment, not the voice measurement.

## Adopt

```bash
# Voice only, applied where you choose:
spec-kitty charter activate styleguide cave-sty-001-communication

# Enforce the voice as a directive:
spec-kitty charter activate directive CAVE_001

# Or run the re-voiced lifecycle:
spec-kitty agent mission create --type cave-dev ...
```

## Validate

```bash
spec-kitty charter pack validate packs/cave-kitty
```
