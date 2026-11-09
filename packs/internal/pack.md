# spec-kitty-internal Charter Pack

Spec Kitty's own internal Charter Pack: the doctrine that governs the Spec Kitty project's
contributors, maintainers and core team. It is loaded as an org-tier pack (registered in
`.kittify/config.yaml` under `charter_packs.org.packs`), overlaying the public `built-in`
product doctrine.

It is never shipped to consumers: maintainer-only doctrine — how PRs are landed, the tracker
processed, main kept honest — must not be force-shipped on the wheel, so the packaging narrows
its `packs` include to `packs/built-in/` specifically to keep this tree in-repo.
