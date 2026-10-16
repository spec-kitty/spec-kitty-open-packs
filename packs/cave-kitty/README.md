# `cave-kitty` — Caveman Communication Charter Pack

An open Spec Kitty Charter Pack that makes an agent answer in a **compressed, token-saving
"caveman" voice** — outcome-first, filler cut — while keeping every payload and every negation
exact and restoring full sentences at a cliff edge.

> **🚧 v0 skeleton.** The styleguide and directive are complete and usable today. The
> `cave-dev` mission type is a **proof-of-concept**: all seven steps are wired and every step's
> command template is re-voiced, but the templates are deliberately thin. They re-voice the
> *shape* of the software-dev lifecycle, not its full governance text. Treat `cave-dev` as a
> demonstration of the mechanism, not a drop-in replacement for the built-in `software-dev`
> mission type yet.

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
| Mission type | `cave-dev` | The software-dev lifecycle re-voiced — same seven canonical steps and the same engineering rigour, caveman output prose. Governance profile selects the styleguide + directive. |

## Does activating this make `software-dev` caveman?

Two layers, kept separate on purpose:

- **Activate the styleguide and/or `CAVE_001`** → the agent *writes* caveman while you keep
  running `--type software-dev`. The built-in prompts are unchanged; only the output voice is.
- **Run `--type cave-dev`** → you select the re-voiced lifecycle. `software-dev` itself stays
  byte-identical. This pack deliberately does **not** override the built-in `software-dev`
  prompts, so activation never silently mutates the canonical type.

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
