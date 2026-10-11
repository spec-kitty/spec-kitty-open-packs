#!/usr/bin/env python3
"""Generate the DocKitty pack reference pages from the Charter Packs in this repo.

Content-from-code (ADR 2026-07-18-2, rendered by DocKitty per ADR 2026-10-10-5):
every pack directory under ``--packs-root`` (default ``packs/``) becomes one
Markdown page under ``--out`` (default ``docs/packs/reference/``), plus an
``index.md`` catalog table and a machine-readable ``checksums.json``
(ADR 2026-07-18-3). Pages carry the DocKitty frontmatter contract
(title/description/doc_status/updated/type/kind) and a ``generated: {by, at}``
stamp, and must never be edited by hand.

Untrusted input. Pack content is third-party text. Every pack-sourced value is
rendered either as escaped Markdown text (all ASCII punctuation backslash-escaped,
so it cannot form links, images, emphasis, autolinks, or raw HTML) or as a code
span with an adaptive backtick fence; link targets are percent-encoded paths the
generator computes itself. Malformed input (unparseable YAML, a non-mapping
where a mapping is required, wrongly typed ``pack.yaml`` fields, symlinks, a
path or id that would reach outside the pack) is a generator error: exit 2, never a silent "drift" exit 1.

Determinism. Output is a pure function of the pack files plus the committed
output: artifacts are sorted, YAML is parsed (never re-serialised), and no wall
clock leaks in. The only date on a page (``updated`` / ``generated.at``) is
*sticky*: when a page's rendered content is unchanged, the date already
committed on it is kept, so ``--check`` is stable across runs, machines, and
shallow CI clones. A page whose content changed gets a new date, taken from
``SOURCE_DATE_EPOCH`` when set (reproducible-builds convention) or today's UTC
date otherwise. (Git commit times were rejected: a pack change and its
regenerated page land in the same commit, so the commit time is unknowable at
generation time, and shallow CI checkouts report the wrong commit.)

Usage (from the repository root)::

    python3 scripts/docs/generate_pack_reference.py            # write docs/packs/reference/
    python3 scripts/docs/generate_pack_reference.py --check    # exit 1 on drift, 2 on bad input
    python3 scripts/docs/generate_pack_reference.py \\
        --packs-root tests/fixtures/valid --out tests/golden/pack-reference --check

Dependencies: Python 3.10+ standard library and PyYAML.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import difflib
import hashlib
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable
from urllib.parse import quote

import yaml

GENERATOR = "scripts/docs/generate_pack_reference.py"
CHECKSUM_RECIPE = "open-packs-sha256-v1"
REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PACKS_ROOT = "packs"
DEFAULT_OUT = "docs/packs/reference"
INDEX_SLUG = "packs/reference"
DESCRIPTION_MAX = 180  # DocKitty frontmatter contract
SUMMARY_MAX = 200

# File extensions / MIME types that mean "this asset is code a consumer may run".
EXECUTABLE_EXTS = {".py", ".sh", ".bash", ".zsh", ".js", ".mjs", ".cjs", ".ts", ".rb", ".pl", ".ps1", ".bat", ".cmd", ".exe", ".bin", ".jar", ".php", ".lua"}
EXECUTABLE_MIME = re.compile(r"(python|shellscript|x-sh\b|javascript|typescript|x-ruby|x-perl|powershell|executable|x-msdownload|java-archive|x-php|x-lua)", re.I)


class GeneratorError(Exception):
    pass


# --------------------------------------------------------------------------- #
# Safe rendering of untrusted pack text
# --------------------------------------------------------------------------- #

_PUNCT = re.compile(r"([!-/:-@\[-`{-~])")  # every ASCII punctuation character


def _scalar(value: Any) -> str:
    """A YAML scalar as text; non-scalars (mappings, lists) yield ''."""
    if value is None or isinstance(value, (dict, list)):
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def _clean(value: Any, limit: int = SUMMARY_MAX) -> str:
    text = " ".join(_scalar(value).split())
    if len(text) > limit:
        text = text[: limit - 1].rstrip() + "…"
    return text


# GFM autolink literals (URLs, www., e-mail) are found in *decoded* text by
# remark-gfm, so escaping cannot stop them; such tokens go into code spans.
_AUTOLINKISH = re.compile(
    r"(?i)(?:\b(?:https?|ftp|mailto|xmpp):\S*|\bwww\.\S*|[\w.+-]+@[\w-]+(?:\.[\w-]+)+)"
)


def _text(value: str) -> str:
    """Render untrusted text for Markdown (incl. a GFM table cell) literally.

    Backslash-escaping every ASCII punctuation character is valid CommonMark and
    neutralises links, images, emphasis, raw HTML, entities and table pipes in
    one rule. URL- and e-mail-like tokens, which GFM would autolink even when
    escaped, are emitted as code spans instead.
    """
    out, pos = [], 0
    for m in _AUTOLINKISH.finditer(value):
        out.append(_PUNCT.sub(r"\\\1", value[pos:m.start()]))
        out.append(_code(m.group(0)))
        pos = m.end()
    out.append(_PUNCT.sub(r"\\\1", value[pos:]))
    return "".join(out)


def _code(value: str) -> str:
    """Render ``value`` as an inline code span safe inside a GFM table cell.

    Code-span content is literal (no entity decoding, no escapes), so ``<`` stays
    ``<``. The fence is one backtick longer than the longest backtick run in the
    value, padded with spaces when the value starts or ends with a backtick. GFM
    tables split on ``|`` even inside code spans, so pipes are written ``\\|``
    (GFM removes that backslash inside table cells).
    """
    value = " ".join(value.split()).replace("|", "\\|")
    if not value:
        return ""
    longest = max((len(m) for m in re.findall(r"`+", value)), default=0)
    fence = "`" * (longest + 1)
    pad = " " if value.startswith("`") or value.endswith("`") or (value.startswith(" ") and value.endswith(" ")) else ""
    return f"{fence}{pad}{value}{pad}{fence}"


def _url(rel: str) -> str:
    """Percent-encode a computed relative path for use as a link target."""
    return quote(rel, safe="/.-_~")


# --------------------------------------------------------------------------- #
# YAML loading
# --------------------------------------------------------------------------- #


def _load_yaml(path: Path) -> Any:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, yaml.YAMLError) as exc:
        raise GeneratorError(f"{path}: cannot parse YAML: {exc}") from exc


def _load_mapping(path: Path, *, empty_ok: bool = False) -> dict[str, Any]:
    data = _load_yaml(path)
    if data is None and empty_ok:
        return {}
    if not isinstance(data, dict):
        raise GeneratorError(f"{path}: expected a YAML mapping, got {type(data).__name__}")
    return data


def _get(data: dict[str, Any], key: str) -> Any:
    """Look a key up in snake_case or kebab-case (agent profiles use ``profile-id``)."""
    if key in data:
        return data[key]
    return data.get(key.replace("_", "-"))


def _first(data: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        value = _get(data, key)
        if _scalar(value) != "":
            return value
    return None


def _count(value: Any) -> int:
    return len(value) if isinstance(value, (list, dict)) else 0


# --------------------------------------------------------------------------- #
# Artifact kinds (the Spec Kitty 4.x org Charter Pack layout)
# --------------------------------------------------------------------------- #


def _plural(n: int, word: str) -> str:
    return f"{n} {word}{'' if n == 1 else 's'}"


def _directive_detail(d: dict[str, Any]) -> str:
    return _code(_clean(d.get("enforcement")))


def _steps_detail(d: dict[str, Any]) -> str:
    n = _count(d.get("steps"))
    return _plural(n, "step") if n else ""


def _preset_detail(d: dict[str, Any]) -> str:
    parts = []
    for key in sorted(k for k in d if isinstance(k, str) and k.startswith("activated_")):
        n = _count(d[key])
        if n:
            noun = key[len("activated_"):].replace("_", " ")
            parts.append(f"{n} {noun[:-1] if n == 1 and noun.endswith('s') else noun}")
    return _text(", ".join(parts))


def _glossary_detail(d: dict[str, Any]) -> str:
    n = _count(d.get("terms"))
    return _plural(n, "term") if n else ""


def _contract_detail(d: dict[str, Any]) -> str:
    parts = []
    if _clean(d.get("mission")):
        parts.append(f"mission {_code(_clean(d.get('mission')))}")
    if _clean(d.get("action")):
        parts.append(f"action {_code(_clean(d.get('action')))}")
    n = _count(d.get("steps"))
    if n:
        parts.append(_plural(n, "step"))
    return ", ".join(parts)


def _profile_detail(d: dict[str, Any]) -> str:
    roles = d.get("roles")
    if isinstance(roles, list):
        return ", ".join(_code(_clean(r)) for r in roles if _clean(r))
    return ""


@dataclass(frozen=True)
class Kind:
    directory: str
    pattern: str
    singular: str
    plural: str
    detail: Callable[[dict[str, Any]], str] = lambda _d: ""
    detail_header: str = "Detail"


KINDS: tuple[Kind, ...] = (
    Kind("directives", "*.directive.yaml", "directive", "Directives", _directive_detail, "Enforcement"),
    Kind("tactics", "*.tactic.yaml", "tactic", "Tactics", _steps_detail, "Steps"),
    Kind("procedures", "*.procedure.yaml", "procedure", "Procedures", _steps_detail, "Steps"),
    Kind("styleguides", "*.styleguide.yaml", "styleguide", "Styleguides"),
    Kind("toolguides", "*.toolguide.yaml", "toolguide", "Toolguides"),
    Kind("paradigms", "*.paradigm.yaml", "paradigm", "Paradigms"),
    Kind("agent_profiles", "*.agent.yaml", "agent profile", "Agent profiles", _profile_detail, "Roles"),
    Kind("glossary_packs", "*.glossary-pack.yaml", "glossary pack", "Glossary packs", _glossary_detail, "Terms"),
    Kind("mission_step_contracts", "*.step-contract.yaml", "mission step contract", "Mission step contracts", _contract_detail, "Binds"),
    Kind("presets", "*.yaml", "preset", "Presets", _preset_detail, "Activates"),
    Kind("skills", "*.skill.yaml", "skill", "Skills"),
)


@dataclass
class Artifact:
    path: Path  # absolute
    ident: str
    title: str
    summary: str
    detail: str  # already-rendered Markdown


@dataclass
class Asset:
    path: Path  # the .asset.yaml descriptor
    ident: str
    title: str
    mime: str
    target: str  # the asset file the descriptor points at (relative to assets/)
    executable: bool


@dataclass
class MissionType:
    path: Path
    ident: str
    title: str
    summary: str
    actions: list[str]
    actions_source: Path | None


@dataclass
class MissionDir:
    path: Path  # missions/<id>/
    ident: str
    title: str
    steps: list[str]
    steps_source: Path | None
    command_templates: int
    templates: int


@dataclass
class MissionStep:
    path: Path  # mission-steps/<type>/<step>/step.yaml
    mission: str
    ident: str
    title: str
    agent_profile: str
    depends_on: list[str]


@dataclass
class Pack:
    name: str
    root: Path
    artifacts: dict[str, list[Artifact]] = field(default_factory=dict)
    assets: list[Asset] = field(default_factory=list)
    mission_types: list[MissionType] = field(default_factory=list)
    missions: list[MissionDir] = field(default_factory=list)
    mission_steps: list[MissionStep] = field(default_factory=list)
    purpose: str = ""
    depends_on: list[str] = field(default_factory=list)
    maturity: str = ""
    org_charter: dict[str, Any] | None = None
    drg: dict[str, int] | None = None
    checksum: str = ""
    file_count: int = 0
    file_set: str = ""


# --------------------------------------------------------------------------- #
# Checksum (recipe open-packs-sha256-v1)
# --------------------------------------------------------------------------- #


def _git_files(root: Path) -> list[str] | None:
    """Files git would ship for ``root``: tracked + untracked-but-not-ignored.

    Returns ``None`` when ``root`` is not inside a git work tree (or git is absent).
    Untracked, non-ignored files are included so that regenerating *before*
    ``git add`` yields the same checksum CI computes after the commit; ignored
    files (``__pycache__/``, editor droppings) never count.
    """
    try:
        inside = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "--is-inside-work-tree"],
            capture_output=True, text=True, check=False,
        )
        if inside.returncode != 0 or inside.stdout.strip() != "true":
            return None
        out = subprocess.run(
            ["git", "-C", str(root), "ls-files", "-z", "--cached", "--others", "--exclude-standard", "--", "."],
            capture_output=True, check=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError):
        return None
    names = sorted({n.decode("utf-8") for n in out.split(b"\0") if n})
    # A tracked file deleted in the work tree is not part of what we ship.
    return [n for n in names if (root / n).exists() or (root / n).is_symlink()]


def _walk_files(root: Path) -> list[str]:
    """Fallback outside git: every file, minus hidden paths and Python bytecode."""
    names = []
    for path in root.rglob("*"):
        rel = path.relative_to(root)
        if any(part.startswith(".") or part == "__pycache__" for part in rel.parts):
            continue
        if path.suffix in {".pyc", ".pyo"}:
            continue
        if path.is_file() or path.is_symlink():
            names.append(rel.as_posix())
    return names


def pack_checksum(root: Path) -> tuple[str, int, str]:
    """Recipe ``open-packs-sha256-v1``: sha256 of the ``sha256sum``-format manifest.

    The manifest has one ``<hex>  ./<path>`` line per file, sorted bytewise by
    path, over the pack's git-shipped files (tracked + untracked-not-ignored; a
    clean checkout or release tarball contains exactly these). Outside git the
    set falls back to every non-hidden, non-bytecode file. Symlinks and paths
    containing a backslash or newline are rejected, because ``sha256sum`` would
    follow/escape them differently from this implementation.

    Returns ``(hexdigest, file_count, file_set)`` where ``file_set`` is ``git``
    or ``filesystem``.
    """
    names = _git_files(root)
    file_set = "git"
    if names is None:
        names, file_set = _walk_files(root), "filesystem"
    lines = []
    for name in sorted(names, key=lambda s: s.encode("utf-8")):
        path = root / name
        if path.is_symlink():
            raise GeneratorError(f"{path}: symlinks are not allowed in a pack")
        if "\\" in name or "\n" in name:
            raise GeneratorError(f"{path}: file names may not contain a backslash or newline")
        if path.is_dir():  # a submodule / nested repo entry
            raise GeneratorError(f"{path}: nested repositories are not allowed in a pack")
        lines.append(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  ./{name}\n")
    digest = hashlib.sha256("".join(lines).encode("utf-8")).hexdigest()
    return digest, len(lines), file_set


# --------------------------------------------------------------------------- #
# Loading a pack
# --------------------------------------------------------------------------- #


def _ident(data: dict[str, Any], path: Path, *keys: str) -> str:
    return _clean(_first(data, *keys) or path.name.split(".")[0])


def _inside(base: Path, rel: str, where: str, *, root: Path) -> Path:
    """``base / rel``, refusing absolute paths and anything that resolves outside the pack ``root``."""
    if Path(rel).is_absolute() or "\\" in rel:
        raise GeneratorError(f"{where}: path {rel!r} must be relative, with forward slashes")
    target = base / rel
    if not target.resolve().is_relative_to(root.resolve()):
        raise GeneratorError(f"{where}: path {rel!r} points outside the pack")
    return target


def _segment(ident: str, where: str) -> str:
    """An id that is used as a single directory name."""
    if not ident or ident in {".", ".."} or "/" in ident or "\\" in ident:
        raise GeneratorError(f"{where}: id {ident!r} must be a single path segment")
    return ident


def _is_executable(target: Path, mime: str) -> bool:
    if target.suffix.lower() in EXECUTABLE_EXTS or EXECUTABLE_MIME.search(mime or ""):
        return True
    try:
        return target.is_file() and os.access(target, os.X_OK)
    except OSError:
        return False


def _str_list(value: Any, where: str) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list) or not all(isinstance(v, (str, int, float)) and not isinstance(v, bool) for v in value):
        raise GeneratorError(f"{where}: expected a list of strings")
    return [str(v) for v in value]


def _step_ids(steps: Any) -> list[str]:
    if not isinstance(steps, list):
        return []
    out = []
    for step in steps:
        if isinstance(step, dict):
            sid = _clean(_first(step, "id", "name", "key"))
            if sid:
                out.append(sid)
        elif _clean(step):
            out.append(_clean(step))
    return out


def _mission_actions(pack_root: Path, ident: str, data: dict[str, Any]) -> tuple[list[str], Path | None]:
    """Action sequence for a mission type: inline, else from missions/<id>/."""
    inline = _step_ids(_get(data, "action_sequence"))
    if inline:
        return inline, None
    for name in ("mission-runtime.yaml", "mission.yaml"):
        source = pack_root / "missions" / ident / name
        if source.is_file():
            runtime = _load_mapping(source, empty_ok=True)
            steps = _step_ids(runtime.get("steps")) or _step_ids(runtime.get("states"))
            if steps:
                return steps, source
    return [], None


def load_pack(root: Path) -> Pack:
    pack = Pack(name=root.name, root=root)
    for kind in KINDS:
        directory = root / kind.directory
        if not directory.is_dir():
            continue
        items: list[Artifact] = []
        for path in sorted(directory.glob(kind.pattern), key=lambda p: p.name):
            if not path.is_file():
                continue
            data = _load_mapping(path)
            ident = _ident(data, path, "id", "profile_id", "name")
            title = _clean(_first(data, "title", "name", "display_name") or ident)
            summary = _clean(_first(data, "intent", "purpose", "description", "summary"))
            items.append(Artifact(path, ident, title, summary, kind.detail(data)))
        if items:
            pack.artifacts[kind.directory] = items

    assets_dir = root / "assets"
    if assets_dir.is_dir():
        for path in sorted(assets_dir.glob("*.asset.yaml"), key=lambda p: p.name):
            data = _load_mapping(path)
            target = _clean(_first(data, "path", "file")) or path.name[: -len(".asset.yaml")]
            _inside(assets_dir, target, f"{path}: path", root=root)
            mime = _clean(_first(data, "mime", "media_type", "content_type"))
            pack.assets.append(Asset(
                path=path,
                ident=_ident(data, path, "id", "name"),
                title=_clean(_first(data, "title", "name")) or "",
                mime=mime,
                target=target,
                executable=_is_executable(assets_dir / target, mime),
            ))

    mt_dir = root / "mission_types"
    if mt_dir.is_dir():
        for path in sorted(mt_dir.glob("*.yaml"), key=lambda p: p.name):
            data = _load_mapping(path)
            ident = _segment(_ident(data, path, "id", "name"), str(path))
            actions, source = _mission_actions(root, ident, data)
            pack.mission_types.append(MissionType(
                path=path, ident=ident,
                title=_clean(_first(data, "display_name", "title", "name") or ident),
                summary=_clean(_first(data, "description", "purpose", "summary")),
                actions=actions, actions_source=source,
            ))

    missions_dir = root / "missions"
    if missions_dir.is_dir():
        for mdir in sorted((p for p in missions_dir.iterdir() if p.is_dir() and not p.name.startswith(".")), key=lambda p: p.name):
            steps: list[str] = []
            source: Path | None = None
            title = ""
            for name in ("mission-runtime.yaml", "mission.yaml"):
                candidate = mdir / name
                if candidate.is_file():
                    data = _load_mapping(candidate, empty_ok=True)
                    meta = data.get("mission")
                    if not title:
                        title = _clean(meta.get("name")) if isinstance(meta, dict) else _clean(_first(data, "display_name", "name", "title"))
                    if not steps:
                        steps = _step_ids(data.get("steps")) or _step_ids(data.get("states"))
                        source = candidate if steps else source
            pack.missions.append(MissionDir(
                path=mdir, ident=mdir.name, title=title or mdir.name, steps=steps, steps_source=source,
                command_templates=len([p for p in (mdir / "command-templates").glob("*") if p.is_file()]) if (mdir / "command-templates").is_dir() else 0,
                templates=len([p for p in (mdir / "templates").glob("*") if p.is_file()]) if (mdir / "templates").is_dir() else 0,
            ))

    ms_dir = root / "mission-steps"
    if ms_dir.is_dir():
        for path in sorted(ms_dir.glob("*/*/step.yaml"), key=lambda p: (p.parent.parent.name, p.parent.name)):
            data = _load_mapping(path)
            pack.mission_steps.append(MissionStep(
                path=path,
                mission=path.parent.parent.name,
                ident=_clean(_first(data, "id") or path.parent.name),
                title=_clean(_first(data, "display_name", "title", "name")),
                agent_profile=_clean(_first(data, "agent_profile")),
                depends_on=_str_list(_get(data, "depends_on"), f"{path}: depends_on"),
            ))

    manifest = root / "pack.yaml"
    if manifest.is_file():
        data = _load_mapping(manifest, empty_ok=True)
        purpose = data.get("purpose")
        if purpose is not None and not isinstance(purpose, str):
            raise GeneratorError(f"{manifest}: purpose must be a string")
        maturity = data.get("maturity")
        if maturity is not None and not isinstance(maturity, str):
            raise GeneratorError(f"{manifest}: maturity must be a string")
        pack.purpose = _clean(purpose)
        pack.maturity = _clean(maturity)
        pack.depends_on = _str_list(data.get("depends_on"), f"{manifest}: depends_on")

    charter = root / "org-charter.yaml"
    if charter.is_file():
        pack.org_charter = _load_mapping(charter, empty_ok=True)

    fragment = root / "drg" / "fragment.yaml"
    if fragment.is_file():
        data = _load_mapping(fragment, empty_ok=True)
        for key in ("nodes", "edges"):
            if data.get(key) is not None and not isinstance(data.get(key), list):
                raise GeneratorError(f"{fragment}: {key} must be a list")
        pack.drg = {"nodes": _count(data.get("nodes")), "edges": _count(data.get("edges"))}

    pack.checksum, pack.file_count, pack.file_set = pack_checksum(root)
    return pack


def discover(packs_root: Path) -> list[Pack]:
    if not packs_root.is_dir():
        raise GeneratorError(f"packs root not found: {packs_root}")
    dirs = sorted(
        (p for p in packs_root.iterdir() if p.is_dir() and not p.name.startswith(".")),
        key=lambda p: p.name,
    )
    return [load_pack(d) for d in dirs]


# --------------------------------------------------------------------------- #
# Rendering
# --------------------------------------------------------------------------- #


def _q(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def _frontmatter(*, title: str, description: str, kind: str, date: str, related: list[str], order: int | None = None) -> str:
    if len(description) > DESCRIPTION_MAX:
        description = description[: DESCRIPTION_MAX - 1].rstrip() + "…"
    lines = [
        "---",
        f"title: {json.dumps(title, ensure_ascii=False)}",
        f"description: {json.dumps(description, ensure_ascii=False)}",
        "doc_status: active",
        f"updated: {_q(date)}",
        "type: API",
        f"kind: {kind}",
        "tags:",
        "- pack-reference",
        "- generated",
        "generated:",
        f"  by: {GENERATOR}",
        f"  at: {_q(date)}",
    ]
    if order is not None:
        lines += ["sidebar:", f"  order: {order}"]
    if related:
        lines.append("related:")
        lines.extend(f"- {r}" for r in related)
    lines.append("---")
    return "\n".join(lines) + "\n"


def _banner(packs_root_rel: str) -> str:
    return (
        "> **Generated — do not edit.** This page is rendered from "
        f"{_code(packs_root_rel + '/')} by `scripts/docs/generate_pack_reference.py`; "
        "CI fails on drift. Change the pack, then re-run the generator.\n"
    )


def _counts(pack: Pack) -> list[str]:
    out = []
    for kind in KINDS:
        n = len(pack.artifacts.get(kind.directory, []))
        if n:
            out.append(_plural(n, kind.singular))
    if pack.assets:
        out.append(_plural(len(pack.assets), "asset"))
    if pack.mission_types:
        out.append(_plural(len(pack.mission_types), "mission type"))
    if pack.missions:
        out.append(_plural(len(pack.missions), "mission"))
    if pack.mission_steps:
        out.append(_plural(len(pack.mission_steps), "mission step"))
    return out


class Renderer:
    def __init__(self, packs_root: Path, out_dir: Path):
        self.packs_root = packs_root
        self.out_dir = out_dir  # the *intended* location (links are relative to it)
        try:
            self.packs_root_rel = packs_root.resolve().relative_to(REPO_ROOT).as_posix()
        except ValueError:
            self.packs_root_rel = packs_root.as_posix()

    def link(self, target: Path, *, folder: bool = False) -> str:
        rel = Path(os.path.relpath(target.resolve(), self.out_dir.resolve())).as_posix()
        return _url(rel + ("/" if folder else ""))

    def src(self, pack: Pack, path: Path, *, folder: bool = False) -> str:
        label = path.relative_to(pack.root).as_posix() + ("/" if folder else "")
        return f"[{_code(label)}]({self.link(path, folder=folder)})"

    @staticmethod
    def find_recipe(pack: Pack) -> str:
        """The ``find`` that lists the same files the checksum covers, in a plain copy."""
        if pack.file_set == "git":
            # Git-shipped files include tracked dotfiles; only git's own metadata is excluded.
            return "find . -type f ! -path './.git/*'"
        # Mirrors _walk_files: no hidden paths, no Python bytecode.
        return "find . -type f ! -path '*/.*' ! -path '*/__pycache__/*' ! -name '*.pyc' ! -name '*.pyo'"

    def pack_page(self, pack: Pack, date: str) -> str:
        counts = _counts(pack)
        description = (
            f"Generated reference for the {pack.name} Charter Pack: "
            + (", ".join(counts) if counts else "no artifacts")
            + "."
        )
        out = [
            _frontmatter(
                title=f"Pack: {pack.name}",
                description=description,
                kind="Reference",
                date=date,
                related=[INDEX_SLUG],
            ),
            f"# Pack: {_text(pack.name)}\n",
            _banner(self.packs_root_rel),
        ]
        executables = [a for a in pack.assets if a.executable]
        if executables:
            out += [
                "> **⚠ This pack ships executable code.** "
                f"{_plural(len(executables), 'asset')} in this pack "
                f"{'is' if len(executables) == 1 else 'are'} code a consumer may run: "
                + ", ".join(_code(f"assets/{a.target}") for a in executables)
                + ". Read them before you adopt the pack (see the repository's `SECURITY.md`); "
                "the checksum below only proves the files match this repository.\n",
            ]
        out += [
            "## Summary\n",
            "| Field | Value |",
            "| --- | --- |",
            f"| Source | [{_code(f'{self.packs_root_rel}/{pack.name}/')}]({self.link(pack.root, folder=True)}) |",
            f"| Purpose | {_text(pack.purpose) if pack.purpose else '— (no `pack.yaml`)'} |",
            f"| Depends on | {', '.join(_code(d) for d in pack.depends_on) or '—'} |",
        ]
        if pack.maturity:
            out.append(f"| Maturity | {_text(pack.maturity)} |")
        out.append(f"| Artifacts | {', '.join(counts) if counts else '—'} |")
        if pack.drg is not None:
            out.append(
                f"| DRG fragment | {pack.drg['nodes']} node(s), {pack.drg['edges']} edge(s) "
                f"({self.src(pack, pack.root / 'drg' / 'fragment.yaml')}) |"
            )
        if pack.org_charter is not None:
            keys = ", ".join(_code(str(k)) for k in sorted(pack.org_charter, key=str))
            org = _clean(pack.org_charter.get("org_name"))
            label = f"org {_code(org)}; " if org else ""
            out.append(f"| Org charter | {label}keys: {keys or '—'} ({self.src(pack, pack.root / 'org-charter.yaml')}) |")
        set_note = (
            "the git-shipped files (tracked, plus untracked files that are not ignored)"
            if pack.file_set == "git"
            else "every non-hidden, non-bytecode file (no git work tree found)"
        )
        out += [
            "",
            "## Provenance & integrity\n",
            f"- **Content checksum** (`{CHECKSUM_RECIPE}`, {pack.file_count} file(s)): `sha256:{pack.checksum}`",
            f"- **File set:** {set_note}. A clean checkout or release tarball of the pack contains exactly",
            "  these files. Symlinks and file names containing a backslash or newline are rejected.",
            "- **Verify** a fetched copy from inside the pack directory:\n",
            "  ```sh",
            "  # in a git checkout (matches what CI hashes):",
            "  git ls-files -z --cached --others --exclude-standard -- . | tr '\\0' '\\n' | LC_ALL=C sort \\",
            '    | while IFS= read -r f; do sha256sum "./$f"; done | sha256sum',
            "  # in a plain download of exactly those files:",
            f"  {self.find_recipe(pack)} | LC_ALL=C sort \\",
            '    | while IFS= read -r f; do sha256sum "$f"; done | sha256sum',
            "  ```\n",
            "  (`shasum -a 256` in place of `sha256sum` on macOS.) This is tamper-evidence for the published",
            "  content, not a signature: it tells you the copy matches this repository, not who to trust",
            "  (ADR 2026-07-18-3).",
            "",
        ]
        if not counts:
            out.append("This pack ships no recognised artifact files.\n")
        for kind in KINDS:
            items = pack.artifacts.get(kind.directory)
            if not items:
                continue
            show_detail = any(a.detail for a in items)
            out.append(f"## {kind.plural}\n")
            out.append("| ID | Title | Summary |" + (f" {kind.detail_header} |" if show_detail else "") + " Source |")
            out.append("| --- | --- | --- |" + (" --- |" if show_detail else "") + " --- |")
            for a in items:
                row = f"| {_code(a.ident)} | {_text(a.title)} | {_text(a.summary) or '—'} |"
                if show_detail:
                    row += f" {a.detail or '—'} |"
                row += f" {self.src(pack, a.path)} |"
                out.append(row)
            out.append("")
        if pack.assets:
            out.append("## Assets\n")
            out.append("| ID | Title | MIME | Path | Executable | Descriptor |")
            out.append("| --- | --- | --- | --- | --- | --- |")
            for a in pack.assets:
                target = pack.root / "assets" / a.target
                path_cell = self.src(pack, target) if target.is_file() else _code(f"assets/{a.target}")
                out.append(
                    f"| {_code(a.ident)} | {_text(a.title) or '—'} | {_code(a.mime) or '—'} | {path_cell} | "
                    f"{'**yes**' if a.executable else 'no'} | {self.src(pack, a.path)} |"
                )
            out.append("")
        if pack.mission_types:
            out.append("## Mission types\n")
            out.append("| ID | Title | Summary | Actions | Source |")
            out.append("| --- | --- | --- | --- | --- |")
            for m in pack.mission_types:
                actions = " → ".join(_code(s) for s in m.actions) or "—"
                if m.actions_source is not None:
                    actions += f" (from {self.src(pack, m.actions_source)})"
                out.append(f"| {_code(m.ident)} | {_text(m.title)} | {_text(m.summary) or '—'} | {actions} | {self.src(pack, m.path)} |")
            out.append("")
        if pack.missions:
            out.append("## Missions\n")
            out.append("| ID | Name | Steps | Command templates | Templates | Source |")
            out.append("| --- | --- | --- | --- | --- | --- |")
            for m in pack.missions:
                steps = " → ".join(_code(s) for s in m.steps) or "—"
                out.append(
                    f"| {_code(m.ident)} | {_text(m.title)} | {steps} | {m.command_templates} | {m.templates} | "
                    f"{self.src(pack, m.path, folder=True)} |"
                )
            out.append("")
        if pack.mission_steps:
            out.append("## Mission steps\n")
            out.append("| Mission | Step | Title | Agent profile | Depends on | Source |")
            out.append("| --- | --- | --- | --- | --- | --- |")
            for s in pack.mission_steps:
                out.append(
                    f"| {_code(s.mission)} | {_code(s.ident)} | {_text(s.title) or '—'} | {_code(s.agent_profile) or '—'} | "
                    f"{', '.join(_code(d) for d in s.depends_on) or '—'} | {self.src(pack, s.path)} |"
                )
            out.append("")
        return "\n".join(out).rstrip("\n") + "\n"

    def index_page(self, packs: list[Pack], date: str) -> str:
        out = [
            _frontmatter(
                title="Pack reference",
                description=(
                    "Generated reference for every Charter Pack in this repository: "
                    "artifacts per kind, dependencies, and content checksums."
                ),
                kind="Hub",
                date=date,
                related=["packs", "packs/catalog-proposal"],
                order=3,
            ),
            "# Pack reference\n",
            _banner(self.packs_root_rel),
        ]
        if not packs:
            out += [
                f"No packs are materialized under {_code(self.packs_root_rel + '/')} yet. The packs we intend to",
                f"ship are listed in the [catalog proposal]({self.link(REPO_ROOT / 'docs' / 'packs' / 'catalog-proposal.md')});",
                "each one gets a page here as soon as its directory lands.",
            ]
            return "\n".join(out).rstrip("\n") + "\n"
        out += [
            f"{len(packs)} pack(s) under {_code(self.packs_root_rel + '/')}. Checksums use recipe `{CHECKSUM_RECIPE}`;",
            "the machine-readable list is [`checksums.json`](checksums.json).\n",
            "| Pack | Purpose | Depends on | Artifacts | Executable assets | Checksum |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
        for p in packs:
            n_exec = len([a for a in p.assets if a.executable])
            out.append(
                f"| [{_text(p.name)}]({_url(p.name + '.md')}) | {_text(p.purpose) or '—'} | "
                f"{', '.join(_code(d) for d in p.depends_on) or '—'} | {', '.join(_counts(p)) or '—'} | "
                f"{f'**{n_exec}**' if n_exec else '0'} | `{p.checksum[:12]}…` |"
            )
        return "\n".join(out).rstrip("\n") + "\n"

    @staticmethod
    def checksums(packs: list[Pack]) -> str:
        data = {
            "recipe": CHECKSUM_RECIPE,
            "packs": {
                p.name: {"sha256": p.checksum, "files": p.file_count, "file_set": p.file_set}
                for p in packs
            },
        }
        return json.dumps(data, indent=2, sort_keys=True) + "\n"


# --------------------------------------------------------------------------- #
# Sticky dates + write / check
# --------------------------------------------------------------------------- #

_UPDATED_RE = re.compile(r"^updated: '(\d{4}-\d{2}-\d{2})'$", re.M)


def new_date() -> str:
    epoch = os.environ.get("SOURCE_DATE_EPOCH")
    if epoch:
        try:
            moment = _dt.datetime.fromtimestamp(int(epoch), tz=_dt.timezone.utc)
        except (ValueError, OverflowError, OSError) as exc:
            raise GeneratorError(f"SOURCE_DATE_EPOCH must be an integer Unix timestamp, got {epoch!r}") from exc
    else:
        moment = _dt.datetime.now(tz=_dt.timezone.utc)
    return moment.date().isoformat()


def sticky(render: Callable[[str], str], existing: str | None) -> str:
    """Keep the committed date when the content is otherwise unchanged."""
    if existing is not None:
        m = _UPDATED_RE.search(existing)
        if m:
            candidate = render(m.group(1))
            if candidate == existing:
                return candidate
    return render(new_date())


def build(packs_root: Path, out_dir: Path) -> dict[str, str]:
    """Return ``{filename: content}`` for the full generated output set."""
    packs = discover(packs_root)
    names = [p.name for p in packs]
    if "index" in names:
        raise GeneratorError("a pack may not be named 'index' (reserved for the catalog page)")
    renderer = Renderer(packs_root, out_dir)

    def existing(name: str) -> str | None:
        path = out_dir / name
        return path.read_text(encoding="utf-8") if path.is_file() else None

    files: dict[str, str] = {}
    for pack in packs:
        name = f"{pack.name}.md"
        files[name] = sticky(lambda d, p=pack: renderer.pack_page(p, d), existing(name))
    files["index.md"] = sticky(lambda d: renderer.index_page(packs, d), existing("index.md"))
    if packs:
        files["checksums.json"] = renderer.checksums(packs)
    return files


def _current(out_dir: Path) -> dict[str, str]:
    if not out_dir.is_dir():
        return {}
    return {
        p.name: p.read_text(encoding="utf-8")
        for p in sorted(out_dir.iterdir())
        if p.is_file() and p.suffix in {".md", ".json"}
    }


def write(files: dict[str, str], out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    for stale in set(_current(out_dir)) - set(files):
        (out_dir / stale).unlink()
    for name, content in files.items():
        path = out_dir / name
        if not path.is_file() or path.read_text(encoding="utf-8") != content:
            path.write_text(content, encoding="utf-8")


def check(files: dict[str, str], out_dir: Path) -> list[str]:
    """Diff the freshly rendered output set against ``out_dir``; return diff lines.

    Rendering already happened in memory (``build``), so nothing is written: a
    missing, changed, or stale (no longer generated) file is drift.
    """
    actual = _current(out_dir)
    diff: list[str] = []
    for name in sorted(set(files) | set(actual)):
        a = actual.get(name, "").splitlines(keepends=True)
        b = files.get(name, "").splitlines(keepends=True)
        if a != b or (name in files) != (name in actual):
            diff.extend(difflib.unified_diff(a, b, f"committed/{name}", f"generated/{name}"))
            if not a and not b:
                diff.append(f"{'missing' if name in files else 'stale'}: {name}\n")
    return diff


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--packs-root", default=DEFAULT_PACKS_ROOT, help="directory holding one subdirectory per pack (default: packs)")
    parser.add_argument("--out", default=DEFAULT_OUT, help="output directory (default: docs/packs/reference)")
    parser.add_argument("--check", action="store_true", help="do not write; exit 1 if the committed output drifts")
    args = parser.parse_args(argv)

    packs_root = Path(args.packs_root)
    out_dir = Path(args.out)
    if not packs_root.is_absolute():
        packs_root = REPO_ROOT / packs_root
    if not out_dir.is_absolute():
        out_dir = REPO_ROOT / out_dir
    try:
        files = build(packs_root, out_dir)
    except GeneratorError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.check:
        diff = check(files, out_dir)
        if diff:
            sys.stdout.writelines(diff)
            shown = out_dir.relative_to(REPO_ROOT) if out_dir.is_relative_to(REPO_ROOT) else out_dir
            print(
                f"\n✖ {shown} is out of date — run scripts/docs/generate_pack_reference.py and commit the result.",
                file=sys.stderr,
            )
            return 1
        print(f"✓ pack reference up to date ({len(files)} file(s)).")
        return 0

    write(files, out_dir)
    print(f"✓ wrote {len(files)} file(s) to {out_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
