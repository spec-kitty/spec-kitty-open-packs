# Common Docs Structural Lint

## Overview

`docs_structural_lint.py` checks the shape of a docs tree against the common-docs standard. It
is the one mechanical gate the writing pack ships for DIRECTIVE_042 and the common-docs
styleguide. It only reads the tree. It never changes a file.

Use it before you hand off a documentation change, and in the documentation mission's
`validate` step. It needs Python 3 and the `ruamel.yaml` package.

## Resolve the script and its policy file

The script ships as the asset `common-docs-structural-lint`. Its default policy file,
`docs_structural_lint.config.yaml`, ships beside it as the asset
`common-docs-structural-lint-config`.

```bash
LINT="$(spec-kitty charter pack asset path common-docs-structural-lint)"
CONFIG="$(spec-kitty charter pack asset path common-docs-structural-lint-config)"
```

If your installation cannot resolve the config asset id, take the file that sits next to the
script:

```bash
CONFIG="$(dirname "$LINT")/docs_structural_lint.config.yaml"
```

You can also start from the pack root. `spec-kitty charter pack list` names the pack that
ships the asset, and `spec-kitty charter pack path <pack>` prints its root. The file is
`assets/docs_structural_lint.config.yaml` under that root.

Both `asset path` commands fail closed: an unknown id exits non-zero and names the id.

## Use your own policy

The lint reads its policy from the `structural_lint_config:` block of whatever file you pass.
The shipped file is a repository-agnostic default. If your project needs other sections,
other required frontmatter fields or other allowlists, copy the block into a file of your own
and point the lint at that file. Do not edit the shipped copy.

## Run it

```bash
python3 "$LINT" --styleguide "$CONFIG" docs
python3 "$LINT" --styleguide "$CONFIG" --extended docs
```

| Argument | Meaning |
|---|---|
| `DOCS_ROOT` | The docs tree to scan. Defaults to `docs`. |
| `--styleguide PATH` | The file that carries the `structural_lint_config:` block. Without it the lint reads the `SPEC_KITTY_STYLEGUIDE` environment variable. With neither, it stops with exit `2`. |
| `--extended` | Also runs `sanctioned_section_membership` and `one_index_per_dir`. Use it for a full check of the tree, such as the documentation mission's `validate` step. |
| `--json` | Prints `{"violations": [{"rule_id", "path", "message"}], "checked": N}` instead of the text summary. |
| `--repo-root PATH` | The base for the paths in the report. Defaults to the current directory. |

## Checks

Every violation names its check id.

| Check id | When it runs | What it flags |
|---|---|---|
| `index_completeness` | always | A page in a curated-complete section (`architecture/` by default) that the section's `index.md` does not link. Only runs when that `index.md` exists. |
| `point_in_time_placement` | always | A dated file, or one whose `doc_status` is `point_in_time` or `closeout`, outside the allowlist (`adr/**`, `plans/**` by default). |
| `shadow_tree_basename` | always | The same content file name in two different top-level sections. `index.md`, `README.md`, `toc.yml` and redirect stubs are exempt. |
| `frontmatter_contract` | always | An in-scope page that lacks a field in `frontmatter_required_fields` (`doc_status` and `updated` by default). `README.md` pages and `adr/**` are out of scope. |
| `sanctioned_section_membership` | `--extended` | A page whose top-level section is not in `sanctioned_content_sections` or `non_content_dirs`. |
| `one_index_per_dir` | `--extended` | A directory with both an `index.md` and a competing `README.md`. |

The lint does not check `description` length, `related:` or `audience:` values, kebab-case
names or the Divio `type:`. Those are review items.

## Exit codes

| Exit code | Meaning |
|---|---|
| `0` | No violations. |
| `1` | At least one violation. The report lists each one with its check id. |
| `2` | The policy file could not be found or loaded, or its `structural_lint_config:` block is missing or malformed. Nothing was checked. |

## Cautions

- A docs root that does not exist reports `checked 0 page(s)` and exits `0`. Read the page
  count before you trust a green run.
- The checks that need `--extended` do not run without it. A plain run can pass a tree with
  pages in the wrong section.
