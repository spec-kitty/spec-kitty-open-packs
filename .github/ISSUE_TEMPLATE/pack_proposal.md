---
name: 📦 Pack proposal
about: Propose a new Charter Pack (or a compound pack) for the open-packs catalog.
title: "pack: <pack-name>"
labels: ["pack", "doctrine"]
assignees: []
---

<!--
Before filing: check docs/packs/catalog-proposal.md and existing issues — the pack may
already be proposed or in progress. The contributor path is docs/guides/contribute-a-pack.md.
Agree the scope here before authoring: the pack contract still changes often (epic #287).
To change a pack that already exists, use the "Enhancement / idea" template instead.
-->

## Pack

- **Proposed name:** `<pack-name>`
- **Purpose (one line):**
- **Intended consumer:** who adopts this and why
- **Proposed `name` qualifier:** what other packs write as `<name>::<id>` (may differ from the directory)
- **Canonical home:** this repository, or another repository that will own the content

## Contents

Reference existing built-in artifacts by ID where possible; note anything net-new.

- **Directives:**
- **Tactics:**
- **Styleguides:**
- **Toolguides:**
- **Paradigms:**
- **Procedures:**
- **Agent profiles:**

## Composition

- **`depends_on`:** other packs this one requires (base packs it builds on)
- **Compound?** if this is a compound pack, list the base packs it bundles

## Cross-references

- **Core epic / issue:** e.g. spec-kitty/spec-kitty#2466
- **Related open-packs issues:**

## Notes

- Executable gate assets? (if yes, see SECURITY.md)
- Open questions / boundary decisions still to make
