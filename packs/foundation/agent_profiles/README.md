# Shipped Agent Profiles

The base agent profiles of the `foundation` pack, a member of the built-in distribution. These
define the core roles with their specialization, collaboration contracts, directive references,
and initialization declarations. The comms and documentation profiles live in the `writing` pack;
specialist and stack profiles (for example `architect-alphonso`, `java-jenny`) ship in opt-in
bundles that build on this pack (#73). A role no installed profile fills falls back to
`generic-agent`.

| File | Profile ID | Primary Role |
|------|------------|------|
| `generic-agent.agent.yaml` | `generic-agent` (Generic Giannis) | generic (fallback) |
| `implementer-ivan.agent.yaml` | `implementer-ivan` | implementer |
| `reviewer-renata.agent.yaml` | `reviewer-renata` | reviewer |
| `analyst-annie.agent.yaml` | `analyst-annie` | analyst |
| `human-in-charge.agent.yaml` | `human-in-charge` | human-in-charge |

Shipped profiles are read-only at the package level. Project-level overrides in
`.kittify/charter/agents/` can customize any profile by matching `profile-id`.
