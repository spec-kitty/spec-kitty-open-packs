# Missions

A **mission type** defines the ordered steps of a Mission, the role each step asks for, the
artifacts each step expects, and the guidance it references. Each mission-type directory holds
one mission-type file, its step prompts and guidelines, and its content templates.

## Available mission types

| Mission type         | Directory        | Steps                                                                       |
|----------------------|------------------|-----------------------------------------------------------------------------|
| Software Development | `software-dev/`  | discovery → specify → plan → tasks → analyze → implement → review → accept |
| Documentation        | `documentation/` | discover → audit → design → generate → validate → publish → accept        |
| Plan                 | `plan/`          | specify → research → plan → review                                          |
| Research             | `research/`      | scoping → methodology → gathering → synthesis → output → accept             |

## Structure Convention

Each mission-type directory `<type>/` contains:

- `<type>.mission-type.yaml` — The mission type: its title and description, its `steps` in run
  order, its `on_demand_steps`, and per step the `role`, the `expected_input_artifacts` and
  `expected_output_artifacts`, and the `references` to guidance
- `steps/<step>.prompt.md` — The step prompt, named by the step's `prompt_path`
- `steps/<step>.guidelines.md` — The step's working notes, named by the step's `guidelines_path`
- `templates/` — Content scaffolds for output artifacts (spec, plan, tasks, etc.), named by an
  expected output's `template_path`

A step names a role, never a profile; the activation preset decides which profiles are active.
The layout is set by charter ADR-0044.

## Python Utilities

The mission **logic modules** are **not** in this directory — this pack ships mission
**data** only (mission-type files, prompts, templates, step contracts). The Python modules
(`primitives.py` with `PrimitiveExecutionContext`, `glossary_hook.py` with
`execute_with_glossary()`, `repository.py`, and the other 8 logic modules) live in the
`charter.offering` package at `src/charter/offering/missions/` and read this data at
runtime; a pack tree cannot host a Python package.

## Glossary Reference

See the [glossary](../../../docs/glossary/index.md) and
[Charter artefacts](../../../docs/artefacts/index.md).
