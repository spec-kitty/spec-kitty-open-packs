# Tracer: tooling-friction

One entry per finding: `YYYY-MM-DD · actor · <text>`.

---

2026-11-20 · claude-runner · spec-kitty resolves the project root of a T3 git worktree (.git file) to the main checkout, even with SPECIFY_REPO_ROOT set, so mission create would have written into the main checkout on main. Workaround: a standalone clone on the same branch in the session scratchpad, pushed to origin.
2026-11-20 · claude-implementer · Styleguide principle descriptions have a 256-char schema cap; seam-list rewrites in test-desiderata-and-boundaries and testing-principles were tightened to fit. Built-in digest needed no update.
