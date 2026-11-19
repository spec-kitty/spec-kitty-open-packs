# Documentation Plan: {DOCUMENTATION_PROJECT}

**Mission**: `{MISSION_SLUG}` | **Date**: {YYYY-MM-DD} | **Spec**: [spec.md](spec.md) | **Gap analysis**: [gap-analysis.md](gap-analysis.md)
**Input**: `kitty-specs/{MISSION_SLUG}/spec.md` (discover) and `kitty-specs/{MISSION_SLUG}/gap-analysis.md` (audit)

**Note**: The mission's `design` step fills in this plan, and the `generate` step implements it. See the mission's step prompts for the workflow.

## Summary

{SUMMARY: documentation goals, Divio types selected, target audience and generators needed, from spec.md and gap-analysis.md}

## Technical Context

**Documentation Framework**: {FRAMEWORK: Sphinx | MkDocs | Docusaurus | Jekyll | Hugo | none yet}
**Languages Detected**: {LANGUAGES: Python, JavaScript, Rust, etc., from codebase analysis}
**Generator Tools**:

- JSDoc for JavaScript/TypeScript API reference
- Sphinx for Python API reference (autodoc + napoleon extensions)
- rustdoc for Rust API reference

**Output Format**: {OUTPUT_FORMAT: HTML | Markdown | PDF}
**Hosting Platform**: {HOSTING_PLATFORM: Read the Docs | GitHub Pages | GitBook | custom}
**Build Commands**:

- `sphinx-build -b html docs/ docs/_build/html/` (Python)
- `npx jsdoc -c jsdoc.json` (JavaScript)
- `cargo doc --no-deps` (Rust)

**Theme**: {THEME: sphinx_rtd_theme | docdash | custom}
**Accessibility Requirements**: WCAG 2.1 AA compliance (proper headings, alt text, contrast)

## Project Structure

### Mission Artifacts

Each step of the documentation mission writes one artifact:

```
kitty-specs/{MISSION_SLUG}/
├── spec.md              # discover: needs, audience, iteration mode, goals
├── gap-analysis.md      # audit: coverage matrix, drift findings, prioritized gaps
├── plan.md              # design: this file
├── audit-report.md      # validate: gate results, risks and verdict
└── release.md           # publish: publication handoff
```

The `generate` step writes the documentation pages themselves, under `docs/`.

### Documentation Files (repository root)

Pages follow the common-docs sections. Each Divio type has one home section:

| Divio type | Section | Template |
|------------|---------|----------|
| Tutorial | `docs/guides/` | `divio/tutorial-template.md` |
| How-to | `docs/guides/` | `divio/howto-template.md` |
| Reference | `docs/api/` | `divio/reference-template.md` |
| Explanation | `docs/architecture/` | `divio/explanation-template.md` |

```
docs/
├── index.md                    # Landing page with navigation
├── guides/
│   ├── index.md                # Section landing page
│   ├── getting-started.md      # Tutorial: step-by-step for beginners
│   ├── {TASK_NAME}.md          # How-to: one task per page
│   └── ...
├── api/
│   ├── index.md                # Section landing page
│   ├── {GENERATOR_OUTPUT}/     # Generated API reference (Sphinx, JSDoc, rustdoc)
│   ├── cli.md                  # CLI reference (manual)
│   └── config.md               # Configuration reference (manual)
└── architecture/
    ├── index.md                # Lists every page in architecture/
    ├── concepts.md             # Explanation: core concepts
    └── ...
```

`architecture/` is curated-complete: its `index.md` links every page in it. Keep file
names unique across sections. Generator configuration files (`conf.py`, `jsdoc.json`,
`Cargo.toml`) live where the generator expects them.

## Documentation Design

### Divio Allocation

| Area (from spec.md) | Tutorial | How-to | Reference | Explanation | Deferral reason |
|---------------------|----------|--------|-----------|-------------|-----------------|
| {AREA} | {required / deferred} | {required / deferred} | {required / deferred} | {required / deferred} | {REASON, or none} |

### Navigation Strategy

- Landing page links to the guides, api and architecture sections
- Each section index has a clear purpose statement
- Cross-links between types (tutorials → reference, how-tos → explanation), declared in each page's `related:` list
- Search functionality (if framework supports it)

### Generator Configurations

**Sphinx Configuration** (Python):

```python
# docs/conf.py
project = '{PROJECT_NAME}'
extensions = [
    'sphinx.ext.autodoc',      # Generate docs from docstrings
    'sphinx.ext.napoleon',     # Support Google/NumPy docstring styles
    'sphinx.ext.viewcode',     # Add source code links
    'sphinx.ext.intersphinx',  # Link to other projects' docs
]
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
```

**JSDoc Configuration** (JavaScript):

```json
{
  "source": {
    "include": ["src/"],
    "includePattern": ".+\\.js$",
    "excludePattern": "(node_modules/|test/)"
  },
  "opts": {
    "destination": "docs/api/javascript",
    "template": "node_modules/docdash",
    "recurse": true
  },
  "plugins": ["plugins/markdown"]
}
```

**rustdoc Configuration** (Rust):

```toml
# Cargo.toml
[package.metadata.docs.rs]
all-features = true
rustdoc-args = ["--document-private-items"]
```

### Content Outline

**Tutorials** (`docs/guides/`):

- Getting Started (installation, first use, basic concepts)
- {ADDITIONAL_TUTORIALS: based on key user journeys}

**How-To Guides** (`docs/guides/`):

- How to {TASK_1}
- How to {TASK_2}
- {ADDITIONAL_GUIDES: based on common tasks}

**Reference** (`docs/api/`):

- API Reference (generated from code)
- CLI Reference (manual)
- Configuration Reference (manual)

**Explanation** (`docs/architecture/`):

- Architecture Overview (design decisions, system structure)
- Core Concepts (domain concepts explained)
- {ADDITIONAL_EXPLANATIONS: as needed}

### Design Decisions

Record each major choice (generator, hierarchy shape, cross-link strategy) as an
ADR-shaped decision: context, options, choice, consequences.

| Decision | Options considered | Choice | Consequences |
|----------|--------------------|--------|--------------|
| {DECISION} | {OPTIONS} | {CHOICE} | {CONSEQUENCES} |

## Mission Flow

The rest of the mission implements and checks this plan:

1. **generate** — writes each required page from its Divio template into its section, and runs the selected generators.
2. **validate** — runs the structural lint with `--extended` and the styleguide checks, and writes `audit-report.md` with a verdict.
3. **publish** — publishes what `audit-report.md` cleared, and writes `release.md`.
4. **accept** — accepts the publication handoff as the mission baseline.

## Success Criteria Validation

Validating against spec.md success criteria:

- **SC-001** (findability): Structured navigation and search enable quick information access
- **SC-002** (accessibility): Templates enforce proper headings, alt text, clear language
- **SC-003** (API completeness): Generators ensure comprehensive API coverage
- **SC-004** (task completion): Tutorials and how-tos enable users to succeed independently
- **SC-005** (build quality): Documentation builds without errors or warnings

## Charter Check

*GATE: Documentation mission requires adherence to Write the Docs best practices and Divio principles.*

**Write the Docs Principles**:

- Documentation as code (version controlled, reviewed, tested)
- Accessible language (clear, plain, bias-free)
- User-focused (written for audience, not developers)
- Maintained (updated with code changes)

**Divio Documentation System**:

- Four distinct types with clear purposes
- Learning-oriented tutorials
- Goal-oriented how-tos
- Information-oriented reference
- Understanding-oriented explanations

**Accessibility Standards**:

- WCAG 2.1 AA compliance
- Proper heading hierarchy
- Alt text for all images
- Sufficient color contrast
- Keyboard navigation support

## Risks & Dependencies

**Risks**:

- Documentation becomes outdated as code evolves
- Generated documentation quality depends on code comment quality
- Accessibility requirements may require manual auditing
- Framework limitations may restrict functionality

**Dependencies**:

- Generator tools must be installed in development environment
- Code must have comments/docstrings for reference generation
- Hosting platform must be available and accessible
- Build pipeline must support documentation generation
