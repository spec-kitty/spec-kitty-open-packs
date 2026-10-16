# Provenance

This pack is **not** a port of an existing pack. It was authored fresh in this repository,
inspired by the [`caveman`](https://github.com/JuliusBrussee/caveman) project by Julius Brussee —
a token-saving instruction set for AI coding agents (a skill plus a CLI proxy).

## What was taken, and what was not

What this pack takes from caveman is the **communication-voice idea**: answer-first telegraphic
output that keeps code, paths, numbers and negations exact, restores full sentences for
security/irreversible actions and confused readers, and never rewrites the user's prompts. That
idea is re-expressed here in Spec Kitty's own doctrine schema and wording.

What this pack does **not** take:

- No source text was copied. The styleguide, directive and prompts are written from scratch.
- caveman's **runtime mechanics** — the `/caveman` / `/ultracave` slash-command toggle, the
  `npx @caveman-ai/cli` proxy, and the v4 "rocks" (log/JSON/CSV input compression, model-effort
  routing, browser-page compression) — are **tooling, not doctrine**, and are out of scope for a
  Charter Pack. A Spec Kitty styleguide/directive is advisory context, not a transparent runtime
  interceptor.

## Licence

Authored for this repository and distributed under its MIT licence. The upstream `caveman`
project is referenced for attribution of the idea; no code or prose from it is included.

## Status

Complete for its stated scope (see README.md). The styleguide and directive are usable today.
The `cave-dev` mission type inherits the built-in `software-dev` step contract unchanged and
overrides only the output voice; its seven command templates follow the same structured shape
the canonical `qa` open pack uses — role + software-dev mapping, bound built-in profile,
directive & styleguide citation, artifact/template binding, and a per-step voice specialization.
They deliberately do not duplicate `software-dev`'s inherited governance into each file, which
would drift from the canonical source; they layer the caveman voice on top of it, exactly as `qa`
layers its QA doctrine.
