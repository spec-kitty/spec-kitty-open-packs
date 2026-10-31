#!/usr/bin/env python3
"""Generate per-pack reference pages for the open-packs docsite.

This is the *content-from-code* generator described in
``docs/architecture/docsite-design.md``. For every doctrine pack it emits a
``docs/packs/<pack>.md`` page carrying only facts derivable from the source:

* doc-kitty-valid frontmatter (so the Astro site keeps building);
* a "generated — do not edit" banner plus a deterministic content checksum
  (sha256 over the pack's sorted artifact contents);
* the pack purpose from ``pack.yaml`` *if present* (never fabricated);
* an artifact inventory with per-kind counts;
* validation status from the charter pack schemas, checked by
  ``scripts/ci/validate_pack_schemas.py``.

The output is **deterministic**: re-running on an unchanged tree yields a
byte-identical file. WP05 adds a CI drift gate that re-runs this generator and
fails on any diff, so nothing here may depend on wall-clock time, dict
iteration order, or filesystem ordering.

Run it from the repository root::

    python3 scripts/docs/gen_pack_reference.py            # write pages
    python3 scripts/docs/gen_pack_reference.py --check    # fail on any drift

``pack.yaml`` is read with a tiny local reader. The validation status needs
``pyyaml`` and ``jsonschema`` (the validator's dependencies) and the pinned
charter schemas, which it fetches unless ``$CHARTER_CONTRACT_DIR`` names a local
copy of ``contracts/packs``.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "scripts" / "ci"))
DOCS_PACKS_DIR = REPO_ROOT / "docs" / "packs"
GENERATOR_REL = "scripts/docs/gen_pack_reference.py"

#: Exact opening of the do-not-edit banner every generated page carries. Used
#: both to render the banner and to recognise generated pages on disk (orphan
#: detection), so the two can never drift apart.
GENERATED_BANNER_PREFIX = "> **Generated page — do not edit by hand.**"

#: Hand-authored pages that live beside the generated ones in docs/packs/. A
#: pack slugged like one of these would overwrite it, so it is rejected.
RESERVED_SLUGS = frozenset({"index", "catalog-proposal"})

#: Fixed generation-baseline date stamped into every generated page's `updated`
#: and `generated.at`. Deliberately NOT git-derived: a git date is ref-dependent
#: (it changes when main moves under the branch and differs on a PR merge ref),
#: which makes a drift-gated generated page fail spuriously. The on-page content
#: checksum is the real per-change freshness signal. Bump only on a deliberate
#: generator change.
GENERATED_PAGE_DATE = "2026-10-17"

#: Artifact-kind subdirectories understood by the doctrine model, in the order
#: the design document lists them. Any *other* subdirectory a pack contains is
#: still reported (appended, sorted) so the inventory never silently hides
#: content — it is just ordered after the canonical kinds.
CANONICAL_KINDS: tuple[str, ...] = (
    "directives",
    "tactics",
    "styleguides",
    "toolguides",
    "paradigms",
    "procedures",
    "agent_profiles",
    "assets",
    "glossary_packs",
    "drg",
)


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class PackDescriptor:
    """The authored ``pack.yaml`` fields the reference page surfaces."""

    name: str | None = None
    purpose: str | None = None
    pack_version: str | None = None
    depends_on: tuple[str, ...] = ()


@dataclass(frozen=True)
class ValidationResult:
    """Outcome of validating a pack against the charter pack schemas."""

    available: bool
    ok: bool | None = None
    errors: tuple[str, ...] = ()
    note: str | None = None


@dataclass
class PackReference:
    """Everything needed to render one pack's reference page."""

    slug: str
    directory: Path
    rel_directory: str
    checksum: str
    descriptor: PackDescriptor
    counts: list[tuple[str, int]] = field(default_factory=list)
    inventory: list[tuple[str, list[str]]] = field(default_factory=list)
    file_count: int = 0
    validation: ValidationResult = field(
        default_factory=lambda: ValidationResult(available=False)
    )


# ---------------------------------------------------------------------------
# Pack discovery
# ---------------------------------------------------------------------------


def discover_packs(repo_root: Path) -> list[tuple[str, Path]]:
    """Return ``(slug, directory)`` for built-in plus every ``packs/*`` dir.

    built-in (``packs/built-in``) is always first; the rest follow sorted by
    slug so the catalog order is stable.
    """

    packs: list[tuple[str, Path]] = []
    packs_root = repo_root / "packs"
    built_in = packs_root / "built-in"
    if built_in.is_dir():
        packs.append(("built-in", built_in))

    if packs_root.is_dir():
        for child in sorted(packs_root.iterdir(), key=lambda p: p.name):
            if child.is_dir() and child != built_in:
                packs.append((child.name, child))
    return packs


# ---------------------------------------------------------------------------
# Light pack.yaml reader (stdlib only)
# ---------------------------------------------------------------------------


def read_pack_descriptor(directory: Path) -> PackDescriptor:
    """Parse the flat ``pack.yaml`` if present; otherwise return empties.

    Packs without a ``pack.yaml`` (e.g. ``packs/qa``) degrade gracefully: the
    page omits the purpose rather than inventing one.

    Only the small, flat ``pack.yaml`` shape is supported — ``key: value``
    scalars plus a ``depends_on`` list (inline ``[a, b]`` or a block of
    ``- item`` lines). That is all the authored descriptor carries, so no
    third-party YAML dependency is needed.
    """

    path = directory / "pack.yaml"
    if not path.is_file():
        return PackDescriptor()

    scalars: dict[str, str] = {}
    depends_on: list[str] = []
    collecting_depends = False

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        if collecting_depends:
            if stripped.startswith("- "):
                depends_on.append(_clean_scalar(stripped[2:]))
                continue
            collecting_depends = False  # fall through to normal key handling

        if ":" not in stripped:
            continue
        key, _, value = stripped.partition(":")
        key = key.strip()
        value = value.strip()

        if key == "depends_on":
            if value in ("", "[]"):
                collecting_depends = value == ""
                if value == "[]":
                    pass  # empty inline list
                continue
            if value.startswith("[") and value.endswith("]"):
                inner = value[1:-1].strip()
                if inner:
                    depends_on.extend(
                        _clean_scalar(item) for item in inner.split(",")
                    )
                continue
            # A scalar on the same line (unusual) — treat as single dependency.
            depends_on.append(_clean_scalar(value))
            continue

        scalars[key] = _clean_scalar(value)

    def _none_if_null(value: str | None) -> str | None:
        if value is None or value.lower() in ("null", "~", ""):
            return None
        return value

    return PackDescriptor(
        name=_none_if_null(scalars.get("name")),
        purpose=_none_if_null(scalars.get("purpose")),
        pack_version=_none_if_null(scalars.get("pack_version")),
        depends_on=tuple(dep for dep in depends_on if dep),
    )


def _clean_scalar(value: str) -> str:
    """Strip surrounding quotes and inline comments from a scalar token."""

    value = value.strip()
    if value and value[0] in ("'", '"') and value[-1] == value[0]:
        return value[1:-1]
    # Drop a trailing inline comment that is not inside quotes.
    hash_index = value.find(" #")
    if hash_index != -1:
        value = value[:hash_index].rstrip()
    return value.strip().strip("'\"")


# ---------------------------------------------------------------------------
# Inventory, checksum, dates
# ---------------------------------------------------------------------------


def _pack_files(directory: Path) -> list[Path]:
    """All regular files under ``directory``, sorted by POSIX relative path."""

    files = [p for p in directory.rglob("*") if p.is_file()]
    return sorted(files, key=lambda p: p.relative_to(directory).as_posix())


def compute_checksum(directory: Path) -> str:
    """sha256 over the sorted ``(relative-path, bytes)`` of every pack file.

    The relative path is folded into the hash so that moving a file changes
    the checksum even when its bytes are unchanged. Published verbatim in the
    page so a consumer can re-hash a downloaded pack and compare.
    """

    digest = hashlib.sha256()
    for file_path in _pack_files(directory):
        rel = file_path.relative_to(directory).as_posix()
        digest.update(rel.encode("utf-8"))
        digest.update(b"\0")
        digest.update(file_path.read_bytes())
        digest.update(b"\n")
    return digest.hexdigest()


def build_inventory(
    directory: Path,
) -> tuple[list[tuple[str, int]], list[tuple[str, list[str]]], int]:
    """Return per-kind counts, per-kind file listings, and total file count.

    Kinds are the immediate subdirectories of the pack; canonical kinds come
    first in doctrine order, any extra subdirectories follow sorted. Counts are
    recursive so nested artifact assets are included.
    """

    subdirs = {
        child.name: child for child in directory.iterdir() if child.is_dir()
    }
    ordered = [k for k in CANONICAL_KINDS if k in subdirs]
    ordered += sorted(name for name in subdirs if name not in CANONICAL_KINDS)

    counts: list[tuple[str, int]] = []
    inventory: list[tuple[str, list[str]]] = []
    for kind in ordered:
        kind_dir = subdirs[kind]
        members = sorted(
            p.relative_to(kind_dir).as_posix()
            for p in kind_dir.rglob("*")
            if p.is_file()
        )
        counts.append((kind, len(members)))
        inventory.append((kind, members))

    total = sum(1 for p in directory.rglob("*") if p.is_file())
    return counts, inventory, total


# ---------------------------------------------------------------------------
# Validation (charter pack schemas)
# ---------------------------------------------------------------------------


def validate_pack(directory: Path) -> ValidationResult:
    """Validate ``directory`` against the charter pack schemas.

    If the schemas cannot be loaded (offline, missing dependency) the result is
    marked unavailable rather than failing generation: the page then says so
    instead of asserting a validation status it could not obtain.
    """

    try:
        import validate_pack_schemas as validator
    except ImportError as exc:
        return ValidationResult(available=False, note=f"the validator's dependencies are missing ({exc.name}).")
    try:
        report = validator.validate_pack(directory, validator.contract_for(None))
    except validator.GateError as exc:
        return ValidationResult(
            available=False,
            note=f"the charter pack schemas could not be used ({exc}).",
        )
    # Violations are path-relative to the pack directory's parent, so the page is
    # identical on every machine.
    return ValidationResult(
        available=True,
        ok=report.ok,
        errors=tuple(sorted(report.violations)),
    )


# ---------------------------------------------------------------------------
# Assembly
# ---------------------------------------------------------------------------


def build_reference(repo_root: Path, slug: str, directory: Path) -> PackReference:
    counts, inventory, file_count = build_inventory(directory)
    try:
        rel_directory = directory.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        rel_directory = directory.name
    return PackReference(
        slug=slug,
        directory=directory,
        rel_directory=rel_directory,
        checksum=compute_checksum(directory),
        descriptor=read_pack_descriptor(directory),
        counts=counts,
        inventory=inventory,
        file_count=file_count,
        validation=validate_pack(directory),
    )


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------


def _yaml_quote(value: str) -> str:
    """Quote a frontmatter scalar when needed (colon, leading symbol)."""

    needs_quote = any(ch in value for ch in ":#") or value.strip() != value
    if needs_quote:
        escaped = value.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'
    return value


def render_frontmatter(ref: PackReference) -> list[str]:
    title = f"{ref.slug} pack reference"
    description = (
        f"Generated reference for the {ref.slug} Charter Pack: artifact "
        f"inventory, per-kind counts, content checksum, and validation status."
    )
    lines = [
        "---",
        f"title: {_yaml_quote(title)}",
        f"description: {_yaml_quote(description)}",
        "doc_status: active",
        f"updated: '{GENERATED_PAGE_DATE}'",
        "kind: Reference",
        "related:",
        "- packs",
        "- architecture/docsite-design",
        "- packs/catalog-proposal",
        "generated:",
        f"  by: {GENERATOR_REL}",
        f"  at: '{GENERATED_PAGE_DATE}'",
        "---",
    ]
    # NOTE: `updated`/`generated.at` use a fixed generation-baseline constant,
    # not a git-derived date. A git date is ref-dependent (changes when main
    # moves under the branch, differs on a PR merge ref), which would make this
    # drift-gated page fail spuriously. The on-page content checksum is the real
    # per-change freshness signal.
    return lines


def render_validation(validation: ValidationResult) -> list[str]:
    lines = ["## Validation", ""]
    if not validation.available:
        note = validation.note or "Validation status was not available."
        lines.append(
            f"Validation status unavailable — {note} "
            "Run `python3 scripts/ci/validate_pack_schemas.py <dir>` locally."
        )
        lines.append("")
        return lines

    status = "passing" if validation.ok else "failing"
    lines.append(
        f"Reported by the charter pack schemas (`scripts/ci/validate_pack_schemas.py`): **{status}**."
    )
    lines.append("")
    lines.append(f"- Errors: {len(validation.errors)}")
    lines.append("")
    if validation.errors:
        lines.append("### Errors")
        lines.append("")
        lines.extend(f"- {error}" for error in validation.errors)
        lines.append("")
    return lines


def render_inventory(ref: PackReference) -> list[str]:
    lines = ["## Artifact inventory", ""]
    if not ref.counts:
        lines.append("This pack contains no artifact-kind subdirectories.")
        lines.append("")
        return lines

    lines.append("| Kind | Count |")
    lines.append("| --- | --- |")
    for kind, count in ref.counts:
        lines.append(f"| `{kind}` | {count} |")
    lines.append(f"| **Total files** | **{ref.file_count}** |")
    lines.append("")

    lines.append("### Full listing")
    lines.append("")
    for kind, members in ref.inventory:
        lines.append(f"<details>")
        lines.append(f"<summary><code>{kind}</code> ({len(members)})</summary>")
        lines.append("")
        if members:
            lines.extend(f"- `{member}`" for member in members)
        else:
            lines.append("- _(empty)_")
        lines.append("")
        lines.append("</details>")
        lines.append("")
    return lines


def render_page(ref: PackReference) -> str:
    lines: list[str] = []
    lines.extend(render_frontmatter(ref))
    lines.append("")
    lines.append(f"# {ref.slug} pack reference")
    lines.append("")
    lines.append(
        f"{GENERATED_BANNER_PREFIX} This file is produced by "
        f"`{GENERATOR_REL}` from the pack source. Hand edits are overwritten on "
        "regeneration, and the CI drift gate fails on any difference."
    )
    lines.append("")

    # Provenance & integrity.
    lines.append("## Provenance & integrity")
    lines.append("")
    lines.append(f"- **Pack directory:** `{ref.rel_directory}`")
    if ref.descriptor.pack_version:
        lines.append(f"- **Declared version:** `{ref.descriptor.pack_version}`")
    lines.append(f"- **Content checksum (sha256):** `{ref.checksum}`")
    lines.append(
        "- **Checksum recipe:** sha256 over the sorted "
        "`(relative-path + NUL + bytes)` of every file in the pack directory. "
        "Re-hash a downloaded pack with the same recipe to verify integrity."
    )
    lines.append("")

    # Purpose — only when authored in pack.yaml; never fabricated.
    lines.append("## Purpose")
    lines.append("")
    if ref.descriptor.purpose:
        lines.append(ref.descriptor.purpose)
    else:
        lines.append(
            "_No `purpose` is declared in this pack's `pack.yaml`, so none is "
            "shown here (the generator never fabricates one). See the pack's "
            "`README.md` and the [Packs hub](index.md) for authored context._"
        )
    lines.append("")

    if ref.descriptor.depends_on:
        deps = ", ".join(f"`{dep}`" for dep in ref.descriptor.depends_on)
        lines.append(f"**Depends on:** {deps}")
        lines.append("")

    lines.extend(render_inventory(ref))
    lines.extend(render_validation(ref.validation))

    return "\n".join(lines).rstrip("\n") + "\n"


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def generate(
    repo_root: Path,
    docs_packs_dir: Path,
    *,
    check: bool,
) -> int:
    packs = discover_packs(repo_root)
    if not packs:
        print("No packs discovered — nothing to generate.", file=sys.stderr)
        return 1

    clashes = sorted(slug for slug, _ in packs if slug in RESERVED_SLUGS)
    if clashes:
        raise ValueError(
            "Pack slug(s) collide with hand-authored docs/packs pages: "
            + ", ".join(clashes)
        )

    docs_packs_dir.mkdir(parents=True, exist_ok=True)
    drifted: list[str] = []
    written: list[str] = []

    for slug, directory in packs:
        ref = build_reference(repo_root, slug, directory)
        content = render_page(ref)
        target = docs_packs_dir / f"{slug}.md"

        existing = target.read_text(encoding="utf-8") if target.is_file() else None
        if check:
            if existing != content:
                drifted.append(slug)
            continue

        if existing != content:
            target.write_text(content, encoding="utf-8")
            written.append(slug)

    if check:
        known = {slug for slug, _ in packs}
        orphaned = sorted(
            page.name
            for page in docs_packs_dir.glob("*.md")
            if page.stem not in known
            and page.stem not in RESERVED_SLUGS
            and GENERATED_BANNER_PREFIX in page.read_text(encoding="utf-8")
        )
        if drifted or orphaned:
            if drifted:
                print(
                    "Drift detected in generated pack pages: "
                    + ", ".join(sorted(drifted)),
                    file=sys.stderr,
                )
            if orphaned:
                print(
                    "Orphaned generated pack pages (pack no longer exists): "
                    + ", ".join(f"docs/packs/{name}" for name in orphaned),
                    file=sys.stderr,
                )
            return 1
        print(f"No drift: {len(packs)} pack page(s) up to date.")
        return 0

    for slug in written:
        print(f"wrote docs/packs/{slug}.md")
    unchanged = len(packs) - len(written)
    print(
        f"Generated {len(packs)} pack page(s) "
        f"({len(written)} written, {unchanged} unchanged)."
    )
    return 0


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Verify generated pages are up to date; exit 1 on any drift.",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=REPO_ROOT,
        help="Repository root (defaults to the generator's own repo).",
    )
    parser.add_argument(
        "--docs-packs-dir",
        type=Path,
        default=None,
        help="Output directory for generated pages (defaults to docs/packs).",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    repo_root = args.repo_root.resolve()
    docs_packs_dir = (
        args.docs_packs_dir.resolve()
        if args.docs_packs_dir is not None
        else repo_root / "docs" / "packs"
    )
    return generate(repo_root, docs_packs_dir, check=args.check)


if __name__ == "__main__":
    raise SystemExit(main())
