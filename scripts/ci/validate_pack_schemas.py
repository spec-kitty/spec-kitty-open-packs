#!/usr/bin/env python3
"""Validate Charter Pack files against the JSON Schemas of spec-kitty-charter.

The charter repository owns the pack shapes (``contracts/packs/schemas/*.schema.json``)
and says which file gets which schema (``contracts/packs/file-kinds.yaml``). This script
mirrors that mapping: it classifies every file of a pack by the ``files``, ``exclusions``,
``retired`` and ``payloads`` rules, then a root case variant of a ruled file (refused under that rule,
FR-022) and last the ``ignored`` fallback (Markdown nothing models, left out, not held), validates
YAML files against their schema, and reads
Markdown files (the pack document ``README.md``, guides, mission-step prompts, guidelines and prompt fragments) into the
charter's Markdown model ``{frontmatter?, title?, preamble, sections}`` before validating
that model against the rule's structure schema.

It fails closed. Exit status:

* 0  every pack is valid (its ``pack-manifest.yaml``, when it has one, carries the hashes of the
     files it lists: ``--regenerate-manifest PACK`` restamps them) and every ``--expect-invalid`` pack has schema violations;
     ``--regenerate-manifest`` without a pack to validate only restamps, it validates nothing;
* 1  a schema violation, a retired-layout file, a file no rule models (``unmodelled``, as the charter
     refuses it at registration) or a file the charter would not hold outside ``NOT_HELD_ALLOWANCES``
     (``not_held``) in a pack, an ``--expect-invalid``
     pack that came out clean, or a ``--regenerate-manifest`` pack whose manifest lists a missing file
     (that manifest is left as it was, like the charter's refused write);
* 2  the gate cannot judge: unloadable contract or schema, a file of a known kind with no
     schema mapping, a pack with zero files checked, or an unreadable file.

Needs ``pyyaml`` and ``jsonschema`` (Draft 2020-12). The contract is fetched from the
pinned charter commit (``charter.lock.yaml``) unless ``--contract DIR`` (a directory holding
``file-kinds.yaml`` and ``schemas/``) or ``$CHARTER_CONTRACT_DIR`` is given.
"""

from __future__ import annotations

import argparse
import functools
import hashlib
import json
import os
import re
import sys
import tempfile
import unicodedata
import urllib.request
from collections.abc import Callable, Iterator
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

sys.path.insert(0, str(Path(__file__).resolve().parent))
import charter_lock  # noqa: E402

CHARTER_REPOSITORY = "spec-kitty/spec-kitty-charter"
# The commit of spec-kitty-charter whose contracts/packs/ this repository validates against is the
# `commit` of charter.lock.yaml at the repository root, the one pin of every charter check (the
# charter service job reads the same file). Read by `charter_commit()`, which fails closed unless it is
# 40 lowercase hex characters; never a branch.
CONTRACT_PATH = "contracts/packs"
SCHEMA_NAME_PATTERN = re.compile(r"[a-z0-9][a-z0-9-]*")

#: File-name tokens (``<id>.<token>.yaml``) of kinds the contract must map to a schema.
KNOWN_KIND_TOKENS = frozenset(
    {
        "directive", "tactic", "styleguide", "toolguide", "paradigm", "procedure",
        "agent", "step-contract", "asset", "glossary-pack", "skill", "mission-type",
        "step-enhancement", "graph",
    }
)  # fmt: skip

EXIT_OK, EXIT_INVALID, EXIT_GATE = 0, 1, 2
#: The schemas of file-backed doctrine artifacts a pack's manifest lists (#182). Every file one of
#: these rules classifies must be a manifest constituent, or the manifest under-reports the pack:
#: the git-flow and execution-lanes files shipped unlisted that way. Graph-only kinds (actions,
#: anti-patterns) have no file. Mission types, step contracts and templates are not listed in this
#: repository's manifests (the charter schema would admit them), so they are exempt here.
MANIFEST_CONSTITUENT_SCHEMAS = frozenset({
    "agent-profile", "asset", "directive", "glossary-pack", "guard", "lifecycle", "paradigm", "procedure",
    "skill", "styleguide", "tactic", "toolguide",
})
#: Graph-node kinds a manifest does not list (#182 residual, #194). ``action`` and ``anti_pattern``
#: are graph-only: no file backs them. Mission types, step contracts and templates are deliberately
#: not manifest constituents in this repository (see above). Any other declared node must be a
#: constituent; a new kind fails closed until it is listed here.
MANIFEST_EXEMPT_NODE_KINDS = frozenset({"action", "anti_pattern", "template", "mission_type", "mission_step_contract"})
REGENERATE_COMMAND = "python3 scripts/ci/validate_pack_schemas.py --regenerate-manifest"


class GateError(Exception):
    """The validator cannot judge; the run must fail (exit 2)."""


def charter_commit() -> str:
    """The pinned charter commit, read from ``charter.lock.yaml``; a missing or malformed pin is a GateError."""
    try:
        return charter_lock.read()["commit"]
    except charter_lock.LockError as exc:
        raise GateError(f"charter.lock.yaml: {exc}") from exc


# --------------------------------------------------------------------------- contract


@dataclass(frozen=True)
class Rule:
    regex: re.Pattern[str]
    match: str
    schema: str | None = None
    content_form: str = "yaml"
    reason: str = ""


@dataclass
class Contract:
    files: list[Rule]
    exclusions: list[Rule]
    retired: list[Rule]
    payloads: list[Rule]
    #: The last-resort ``ignored`` rules (#451), matched case-insensitively; ``regex`` is the folded glob.
    ignored: list[Rule] = field(default_factory=list)
    validators: dict[str, Draft202012Validator] = field(default_factory=dict)


def glob_to_regex(glob: str) -> re.Pattern[str]:
    """``*`` within one segment, ``**/`` zero or more whole segments, the rest literal."""
    out, i = [], 0
    while i < len(glob):
        if glob.startswith("**/", i):
            out.append("(?:.*/)?")
            i += 3
        elif glob[i] == "*":
            out.append("[^/]*")
            i += 1
        else:
            out.append(re.escape(glob[i]))
            i += 1
    return re.compile("".join(out) + r"\Z")


def _rules(table: dict[str, Any], section: str, *, folded: bool = False) -> list[Rule]:
    rules = []
    for entry in table.get(section) or []:
        rules.append(
            Rule(
                regex=glob_to_regex(entry["match"].lower() if folded else entry["match"]),
                match=entry["match"],
                schema=entry.get("schema"),
                content_form=entry.get("content_form", "yaml"),
                reason=str(entry.get("reason", "")).strip(),
            )
        )
    return rules


def load_contract(contract_dir: Path) -> Contract:
    """Read ``file-kinds.yaml`` and load every schema it names; fail closed on any gap."""
    table_path = contract_dir / "file-kinds.yaml"
    try:
        table = yaml.safe_load(table_path.read_text(encoding="utf-8"))
        contract = Contract(
            files=_rules(table, "files"),
            exclusions=_rules(table, "exclusions"),
            retired=_rules(table, "retired"),
            payloads=_rules(table, "payloads"),
            ignored=_rules(table, "ignored", folded=True),
        )
    except (OSError, yaml.YAMLError, KeyError, TypeError, AttributeError) as exc:
        raise GateError(f"cannot read {table_path}: {exc!r}") from exc
    if not contract.files:
        raise GateError(f"{table_path} has no `files` rules")
    for rule in contract.files:
        name = rule.schema
        if not name:
            raise GateError(f"files rule {rule.match!r} names no schema")
        if name in contract.validators:
            continue
        if not SCHEMA_NAME_PATTERN.fullmatch(name):
            raise GateError(f"files rule {rule.match!r} names an invalid schema {name!r}")
        schemas_dir = (contract_dir / "schemas").resolve()
        schema_path = (schemas_dir / f"{name}.schema.json").resolve()
        if schema_path.parent != schemas_dir:
            raise GateError(f"schema {name!r} resolves outside {schemas_dir}")
        try:
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
            Draft202012Validator.check_schema(schema)
        except Exception as exc:  # noqa: BLE001 - any failure to load a schema is a gate failure
            raise GateError(f"cannot load schema {schema_path}: {exc!r}") from exc
        contract.validators[name] = Draft202012Validator(schema)
    return contract


def fetch_contract(dest: Path) -> Path:
    """Download file-kinds.yaml and the schemas it names from the pinned charter commit."""
    base = f"https://raw.githubusercontent.com/{CHARTER_REPOSITORY}/{charter_commit()}/{CONTRACT_PATH}"
    headers = {}
    if token := os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = f"Bearer {token}"

    def get(relative: str) -> bytes:
        request = urllib.request.Request(f"{base}/{relative}", headers=headers)
        try:
            with urllib.request.urlopen(request, timeout=30) as response:  # noqa: S310 - fixed https URL
                return response.read()
        except OSError as exc:
            raise GateError(f"cannot fetch {base}/{relative}: {exc!r}") from exc

    (dest / "schemas").mkdir(parents=True, exist_ok=True)
    table_bytes = get("file-kinds.yaml")
    (dest / "file-kinds.yaml").write_bytes(table_bytes)
    try:
        names = {rule["schema"] for rule in yaml.safe_load(table_bytes)["files"]}
    except (yaml.YAMLError, KeyError, TypeError) as exc:
        raise GateError(f"fetched file-kinds.yaml is unreadable: {exc!r}") from exc
    for name in sorted(names):
        (dest / "schemas" / f"{name}.schema.json").write_bytes(get(f"schemas/{name}.schema.json"))
    return dest


_CONTRACT_CACHE: dict[str, Contract] = {}


def contract_for(contract_dir: Path | None) -> Contract:
    """The contract at ``contract_dir`` (or ``$CHARTER_CONTRACT_DIR``, else the pinned fetch)."""
    chosen = contract_dir or (Path(os.environ["CHARTER_CONTRACT_DIR"]) if os.environ.get("CHARTER_CONTRACT_DIR") else None)
    key = str(chosen or f"pinned:{charter_commit()}")
    if key not in _CONTRACT_CACHE:
        if chosen is None:
            with tempfile.TemporaryDirectory(prefix="charter-contract-") as scratch:
                _CONTRACT_CACHE[key] = load_contract(fetch_contract(Path(scratch)))
        else:
            _CONTRACT_CACHE[key] = load_contract(chosen)
    return _CONTRACT_CACHE[key]


# --------------------------------------------------------------------------- YAML


class YamlRefused(yaml.YAMLError):
    """A document the charter's reader (ParsedYaml) refuses for a guard, not for a syntax error."""


class _Loader(yaml.SafeLoader):
    """Safe loader that keeps timestamps as strings, as JSON Schema sees them, and refuses duplicate keys.

    The charter loads with ``setAllowDuplicateKeys(false)`` (Yaml.java); PyYAML keeps the last value.
    """

    def construct_mapping(self, node: yaml.MappingNode, deep: bool = False) -> dict[Any, Any]:
        self.flatten_mapping(node)
        seen: set[Any] = set()
        for key_node, _ in node.value:
            key = self.construct_object(key_node, deep=True)
            try:
                duplicate = key in seen
                seen.add(key)
            except TypeError:  # unhashable key: the base class reports it
                break
            if duplicate:
                raise yaml.constructor.ConstructorError(
                    "while constructing a mapping", node.start_mark, f"found duplicate key {key!r}", key_node.start_mark
                )
        return super().construct_mapping(node, deep=deep)


_Loader.yaml_implicit_resolvers = {
    key: [(tag, regexp) for tag, regexp in resolvers if tag != "tag:yaml.org,2002:timestamp"]
    for key, resolvers in yaml.SafeLoader.yaml_implicit_resolvers.items()
}

#: The guards of the charter's ParsedYaml: collections nested at most this deep, and a document that
#: expands (a shared, aliased node counted each time it is reached) to at most this many nodes.
MAX_DEPTH = 200
MAX_NODES = 100_000


def _nested_too_deeply(text: str) -> bool:
    """Whether the parser's events nest collections deeper than MAX_DEPTH; the event stream is not recursive."""
    depth = 0
    try:
        for event in yaml.parse(text, Loader=_Loader):
            if isinstance(event, yaml.CollectionStartEvent):
                depth += 1
                if depth > MAX_DEPTH:
                    return True
            elif isinstance(event, yaml.CollectionEndEvent):
                depth -= 1
    except yaml.YAMLError:
        return False  # the loader reports a syntax error in the parser's own words
    return False


def _problem(value: Any, depth: int, path: set[int], nodes: list[int]) -> str | None:
    """The first reason a loaded document cannot be validated (ParsedYaml.problem), or ``None``."""
    nodes[0] += 1
    if nodes[0] > MAX_NODES:
        return "the document is too large"
    if not isinstance(value, (dict, list)):
        plain = value is None or isinstance(value, (str, int, float, bool))
        return None if plain else "a value is not a string, a number, a boolean or null"
    if depth >= MAX_DEPTH:
        return "the document is nested too deeply"
    if id(value) in path:
        return "the document contains itself"
    path.add(id(value))
    try:
        if isinstance(value, dict):
            if not all(isinstance(key, str) for key in value):
                return "a mapping key is not a string"
            children: Any = value.values()
        else:
            children = value
        for child in children:
            if (problem := _problem(child, depth + 1, path, nodes)) is not None:
                return problem
        return None
    finally:
        path.discard(id(value))


def load_yaml(text: str) -> Any:
    """Load one YAML document through the charter's guards; raises ``yaml.YAMLError`` when it is refused."""
    if _nested_too_deeply(text):
        raise YamlRefused("the document is nested too deeply")
    document = yaml.load(text, Loader=_Loader)  # noqa: S506 - SafeLoader subclass
    if (problem := _problem(document, 0, set(), [0])) is not None:
        raise YamlRefused(problem)
    return document


# --------------------------------------------------------------------------- manifest

MANIFEST_NAME = "pack-manifest.yaml"
#: The ``pack-manifest.yaml`` entry lists that carry a ``content_hash``.
MANIFEST_LISTS = ("constituents", "presets")


def content_hash(data: bytes) -> str:
    """SHA-256 (lowercase hex) of a file's bytes after every CRLF, then every lone CR, becomes LF."""
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")).hexdigest()


def manifest_hash(manifest: dict[str, Any]) -> str:
    """SHA-256 of the RFC 8785 canonical JSON of the manifest without ``manifest_hash``.

    Narrow like the charter's recipe (PackManifests.canonicalJson): every value is a string, a list
    or an object of the manifest's fixed keys, so no number output is needed, and the keys are
    ASCII, so sorting them by code point equals sorting them by UTF-16 code unit. ``presets`` is
    left out when the manifest lists none.
    """
    body: dict[str, Any] = {"schema_version": manifest["schema_version"]}
    for name in MANIFEST_LISTS:
        if name == "constituents" or manifest.get(name):
            body[name] = [
                {key: entry[key] for key in ("content_hash", "id", "kind", "path") if key in entry}
                for entry in manifest.get(name, [])
            ]
    canonical = json.dumps(body, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _bytes_reader(pack_dir: Path) -> Callable[[str], bytes | None]:
    """The bytes of a pack-relative path; ``None`` for a missing file, a symlink or a path leaving the pack."""

    def read(relative: str) -> bytes | None:
        target = pack_dir / relative
        try:
            inside = target.resolve().is_relative_to(pack_dir.resolve())
            return target.read_bytes() if inside and not target.is_symlink() and target.is_file() else None
        except OSError:
            return None

    return read


def stale_manifest_fields(manifest: dict[str, Any], read: Callable[[str], bytes | None]) -> list[str]:
    """The derived fields of ``manifest`` that do not verify, as the charter names them (PackManifests.stale)."""
    stale, missing = [], []
    for name in MANIFEST_LISTS:
        for entry in manifest.get(name) or []:
            data = read(entry["path"])
            if data is None:
                missing.append(entry["path"])
            elif entry["content_hash"] != content_hash(data):
                stale.append(f"{name}{{{entry['path']}}}.content_hash")
    if manifest["manifest_hash"] != manifest_hash(manifest):
        stale.append("manifest_hash")
    return [*stale, *(f"missing: {path}" for path in missing)]


def unlisted_constituents(manifest: dict[str, Any], files: set[str]) -> list[str]:
    """The file-backed doctrine files of a pack its manifest does not list (#182), sorted. A listed
    file that is missing is ``stale_manifest_fields``'s to report."""
    listed = {entry.get("path") for entry in manifest.get("constituents") or [] if isinstance(entry, dict)}
    return sorted(files - listed)


def unlisted_nodes(manifest: dict[str, Any], nodes: set[tuple[str, str]]) -> list[str]:
    """The declared graph nodes of a pack its manifest does not list as constituents (#182 residual),
    sorted ``kind:id``; nodes of an exempt kind (``MANIFEST_EXEMPT_NODE_KINDS``) are not held to it."""
    listed = {
        (entry.get("kind"), entry.get("id"))
        for entry in manifest.get("constituents") or []
        if isinstance(entry, dict)
    }
    return sorted(f"{kind}:{node_id}" for kind, node_id in nodes if kind not in MANIFEST_EXEMPT_NODE_KINDS and (kind, node_id) not in listed)


def regenerate_manifest(pack_dir: Path) -> list[str]:
    """Restamp every derived field of ``pack_dir``/pack-manifest.yaml from the files; membership is kept.

    Returns the listed paths that have no regular file inside the pack; when there are any, nothing is
    written (the charter refuses such a write with ``pack_unreadable`` before it reaches the target).
    """
    path = pack_dir / MANIFEST_NAME
    try:
        manifest = load_yaml(path.read_bytes().decode("utf-8"))
        read = _bytes_reader(pack_dir)
        missing = []
        for name in MANIFEST_LISTS:
            for entry in manifest.get(name) or []:
                data = read(entry["path"])
                if data is None:
                    missing.append(entry["path"])
                else:
                    entry["content_hash"] = content_hash(data)
        if missing:
            return missing
        manifest["manifest_hash"] = manifest_hash(manifest)
        path.write_text(yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True), encoding="utf-8", newline="\n")
    except (OSError, UnicodeDecodeError, yaml.YAMLError, KeyError, TypeError, AttributeError) as exc:
        raise GateError(f"{path}: cannot regenerate the manifest: {exc!r}") from exc
    return missing


# --------------------------------------------------------------------------- Markdown model

# The scanner's patterns are matched whole (Java Matcher.matches). Java's `.` stops at \n, \r, U+0085,
# U+2028 and U+2029, Python's only at \n, so the class spells Java's out.
_SETEXT = re.compile(r" {0,3}(?:=+|-+)[ \t]*")
_CLOSING = re.compile(r"(?:#+|[^\n\r\x85\u2028\u2029]*[ \t]#+)")
_NOT_WHITESPACE = frozenset("\u00a0\u2007\u202f")  # no-break spaces: Zs, but not Java whitespace


def _java_whitespace(char: str) -> bool:
    """Java's Character.isWhitespace, which String.isBlank and strip use (not Python's str.isspace)."""
    if char in "\t\n\x0b\x0c\r\x1c\x1d\x1e\x1f":
        return True
    return char not in _NOT_WHITESPACE and unicodedata.category(char) in {"Zs", "Zl", "Zp"}


def _blank(text: str) -> bool:
    return all(map(_java_whitespace, text))


def _strip(text: str) -> str:
    start, end = 0, len(text)
    while start < end and _java_whitespace(text[start]):
        start += 1
    while end > start and _java_whitespace(text[end - 1]):
        end -= 1
    return text[start:end]


class MarkdownRefused(Exception):
    def __init__(self, line: int, reason: str) -> None:
        super().__init__(f"line {line}: {reason}")


def _spaces(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def _run(text: str, char: str) -> int:
    return len(text) - len(text.lstrip(char)) if text.startswith(char) else 0


def _fence_opener(line: str) -> tuple[str, int] | None:
    rest = line[_spaces(line):]
    if not rest or rest[0] not in "`~":
        return None
    marker, length = rest[0], _run(rest, rest[0])
    if length < 3 or (marker == "`" and "`" in rest[length:]):
        return None
    return marker, length


def _heading(text: str, number: int) -> tuple[int, str] | None:
    indent = _spaces(text)
    if indent > 3:
        return None
    rest = text[indent:]
    level = _run(rest, "#")
    if level == 0 or level > 6:
        return None
    after = rest[level:]
    if after and after[0] not in " \t":
        return None
    if level > 2:
        return None
    name = "an H1" if level == 1 else "an H2"
    if indent:
        raise MarkdownRefused(number, f"{name} indented by {indent} spaces is ambiguous; start it at column 0")
    if _blank(after):
        raise MarkdownRefused(number, "an empty heading is ambiguous")
    if after[0] == "\t":
        raise MarkdownRefused(number, f"{name} separated from its text by a tab is ambiguous")
    title = _strip(after)
    if _CLOSING.fullmatch(title):
        raise MarkdownRefused(number, f"{name} with a closing # sequence is ambiguous")
    return level, title


def _thematic_break(text: str) -> bool:
    indent = _spaces(text)
    if indent > 3 or indent == len(text) or text[indent] not in "-*_":
        return False
    marker, count = text[indent], 0
    for char in text[indent:]:
        if char == marker:
            count += 1
        elif char not in " \t":
            return False
    return count >= 3


def _deeper_heading(text: str) -> bool:
    if _spaces(text) > 3:
        return False
    rest = text[_spaces(text):]
    level = _run(rest, "#")
    return 2 < level <= 6 and (len(rest) == level or rest[level] in " \t")


def _trimmed(lines: list[str]) -> str:
    start, end = 0, len(lines)
    while start < end and _blank(lines[start]):
        start += 1
    while end > start and _blank(lines[end - 1]):
        end -= 1
    return "\n".join(lines[start:end])


def parse_markdown(text: str) -> dict[str, Any]:
    """Read Markdown into the charter's model (MarkdownCodec): refuses what the codec refuses."""
    if not text:
        return {"preamble": "", "sections": []}
    if text[0] == "﻿":
        raise MarkdownRefused(1, "a byte order mark is not admitted")
    if "\r" in text:
        raise MarkdownRefused(text[: text.index("\r")].count("\n") + 1, "a carriage return is not admitted")
    lines = text.split("\n")
    if text.endswith("\n"):
        lines.pop()
    model: dict[str, Any] = {}
    start = 0
    if lines[0] == "---":
        try:
            end = lines.index("---", 1)
        except ValueError:
            raise MarkdownRefused(1, "unterminated frontmatter: no closing --- line") from None
        raw = "\n".join(lines[1:end])
        try:
            front = {} if _blank(raw) else load_yaml(raw + "\n")
        except yaml.YAMLError as exc:
            raise MarkdownRefused(1, f"frontmatter is not valid YAML: {exc}") from exc
        if not isinstance(front, dict) or not all(isinstance(key, str) for key in front):
            raise MarkdownRefused(1, "frontmatter must be a YAML mapping with string keys")
        model["frontmatter"] = front
        start = end + 1

    preamble: list[str] = []
    current = preamble
    titles: list[str] = []
    bodies: list[list[str]] = []
    title_line, any_block = 0, False
    fence: tuple[str, int, int] | None = None
    under_paragraph = False
    for offset, line in enumerate(lines[start:]):
        number = start + offset + 1
        if fence:
            stripped = line[_spaces(line):]
            if _run(stripped, fence[0]) >= fence[1] and not stripped[_run(stripped, fence[0]):].strip(" "):
                fence = None
            current.append(line)
            under_paragraph = False
            continue
        opened = _fence_opener(line)
        if opened:
            fence = (*opened, number)
            current.append(line)
            any_block = True
            under_paragraph = False
            continue
        if _blank(line):
            current.append(line)
            under_paragraph = False
            continue
        heading = _heading(line, number)
        if heading:
            level, title = heading
            under_paragraph = False
            if level == 1:
                if "title" in model:
                    raise MarkdownRefused(number, f"a second H1 (the first is at line {title_line})")
                if any_block:
                    raise MarkdownRefused(number, "an H1 that is not the first block")
                model["title"], title_line = title, number
            else:
                current = []
                titles.append(title)
                bodies.append(current)
            any_block = True
            continue
        if under_paragraph and _SETEXT.fullmatch(line):
            raise MarkdownRefused(number, "a setext heading underline is ambiguous; use an ATX heading or a blank line")
        current.append(line)
        any_block = True
        under_paragraph = not _thematic_break(line) and not _deeper_heading(line)
    if fence:
        raise MarkdownRefused(fence[2], f"unclosed fence opened at line {fence[2]}")
    model["preamble"] = _trimmed(preamble)
    model["sections"] = [{"title": t, "content": _trimmed(b)} for t, b in zip(titles, bodies, strict=True)]
    return model


# --------------------------------------------------------------------------- prompt slots and fragments (ADR-0066)

SLOT_ID = re.compile(r"[a-z][a-z0-9-]*:[a-z][a-z0-9-]*")
_HTML_COMMENT = re.compile(r"<!--(.*?)-->", re.DOTALL)
_SLOT_COMMENT = re.compile(r"\s*(\S+):(start|end)\s*")
_SLOT_LIKE = re.compile(r":(?:start|end)\b")


def _prompt_slot_problem(line: int, detail: str, code: str = "prompt_slot_malformed") -> str:
    return f"{code} at line {line}: {detail}"


def prompt_slot_violations(text: str, *, require_empty: bool) -> list[str]:
    """The declaration checks of ADR-0066 decisions 2 and 8 for one base prompt.

    All prompts get the well-formedness checks. Only a descriptor at schema_version 1.0
    switches on ``prompt_slot_not_empty``; an unversioned descriptor keeps the legacy
    gate-marker behavior without a shim.
    """
    problems: list[str] = []
    declared: set[str] = set()
    open_slots: list[tuple[str, int, int]] = []
    for comment in _HTML_COMMENT.finditer(text):
        body = comment.group(1)
        match = _SLOT_COMMENT.fullmatch(body)
        line = text.count("\n", 0, comment.start()) + 1
        if match is None:
            if _SLOT_LIKE.search(body):
                problems.append(_prompt_slot_problem(line, f"malformed slot marker {comment.group(0)!r}"))
            continue
        slot_id, marker = match.groups()
        if SLOT_ID.fullmatch(slot_id) is None:
            problems.append(_prompt_slot_problem(line, f"invalid slot id {slot_id!r}"))
            continue
        if marker == "start":
            if slot_id in declared:
                problems.append(_prompt_slot_problem(line, f"slot {slot_id!r} is declared more than once"))
            declared.add(slot_id)
            if open_slots:
                problems.append(_prompt_slot_problem(line, f"slot {slot_id!r} nests inside {open_slots[-1][0]!r}"))
            open_slots.append((slot_id, line, comment.end()))
            continue
        if not open_slots:
            problems.append(_prompt_slot_problem(line, f"slot {slot_id!r} ends before it starts"))
            continue
        open_id, start_line, content_start = open_slots.pop()
        if open_id != slot_id:
            problems.append(_prompt_slot_problem(line, f"slot {slot_id!r} closes open slot {open_id!r} from line {start_line}"))
            continue
        if require_empty and text[content_start:comment.start()].strip():
            problems.append(_prompt_slot_problem(start_line, f"slot {slot_id!r} must contain only whitespace", "prompt_slot_not_empty"))
    for slot_id, line, _ in open_slots:
        problems.append(_prompt_slot_problem(line, f"slot {slot_id!r} has no end marker"))
    return problems


def declared_prompt_slots(text: str) -> set[str]:
    """Ids whose well-formed start marker occurs in a base prompt (compose-time use)."""
    slots = set()
    for comment in _HTML_COMMENT.finditer(text):
        match = _SLOT_COMMENT.fullmatch(comment.group(1))
        if match is not None and match.group(2) == "start" and SLOT_ID.fullmatch(match.group(1)):
            slots.add(match.group(1))
    return slots


def prompt_fragment_violations(text: str) -> list[str]:
    """Refuse slot markers in raw fragment Markdown, which its structure schema cannot see."""
    problems = []
    for comment in _HTML_COMMENT.finditer(text):
        if _SLOT_LIKE.search(comment.group(1)):
            line = text.count("\n", 0, comment.start()) + 1
            problems.append(f"prompt_fragment_invalid at line {line}: a fragment cannot declare or fill a slot")
    return problems


# --------------------------------------------------------------------------- validation


@dataclass
class PackReport:
    pack: str
    checked: int = 0
    skipped: int = 0
    violations: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.violations


def _short(message: str, limit: int = 300) -> str:
    return message if len(message) <= limit else message[: limit - 3] + "..."


@functools.lru_cache(maxsize=None)
def _folded_regex(glob: str) -> re.Pattern[str]:
    """``glob`` in lower case, compiled once: matched against a path folded the same way."""
    return glob_to_regex(glob.lower())


def _exact(contract: Contract, relative: str, *, folded: bool = False) -> tuple[str, Rule | None]:
    """``files``, ``exclusions``, ``retired``, then ``payloads``: the first rule that matches, as written or folded."""
    path = relative.lower() if folded else relative
    for kind, rules in (("file", contract.files), ("excluded", contract.exclusions), ("retired", contract.retired),
                        ("payload", contract.payloads)):
        for rule in rules:
            regex = _folded_regex(rule.match) if folded else rule.regex
            if regex.match(path):
                return kind, rule
    return "unmodelled", None


ROOT_FILE = re.compile(r"\*/([^*/]+)")


def classify(contract: Contract, relative: str) -> tuple[str, Rule | None]:
    """The charter's classification of a path relative to the directory holding the packs.

    As ``PackFileKind.classify`` does at the pin: the exact rules first; then a root file that differs only in
    letter case from a root-anchored ``files`` or ``retired`` rule's file (``Readme.md``, ``PROVENANCE.MD``),
    refused as ``retired`` under that rule (FR-022); then the first ``ignored`` rule, matched case-insensitively,
    unless a ``files``, ``retired`` or ``payloads`` rule takes the path in another letter case (``a.guide.MD``).
    What is left is ``unmodelled``: the charter refuses it at registration."""
    kind, rule = _exact(contract, relative)
    if kind != "unmodelled":
        return kind, rule
    folded = relative.lower()
    for candidate in (*contract.files, *contract.retired):
        root = ROOT_FILE.fullmatch(candidate.match)
        if root and _folded_regex(candidate.match).match(folded):
            return "retired", Rule(candidate.regex, candidate.match, reason=f"differs only in letter case from '{root.group(1)}'")
    if _exact(contract, relative, folded=True)[0] in ("unmodelled", "excluded"):
        for candidate in contract.ignored:
            if candidate.regex.match(folded):
                return "ignored", candidate
    return "unmodelled", None


#: Files the charter leaves out of a pack (``file_not_held``) that this repository lets a pack carry: the
#: orientation notes (a ``README.md`` at any depth; the root one is the pack document and is held) and a
#: skill's ``*.skill.md`` body (held as its skill's companion when it sits beside the skill; the charter
#: service check sees one that does not). Any other file only the ``ignored`` rule takes is a misplaced guide,
#: prompt or note, and fails as ``not_held``. ``scripts/ci/charter_service_check.py`` holds the same list for
#: what a registration reports. Globs match like the contract's, case-sensitively.
NOT_HELD_ALLOWANCES = tuple(glob_to_regex(glob) for glob in ("**/README.md", "**/*.skill.md"))
#: A fixture's own file, never pack content (``tests/fixtures/invalid/*/expected-code``).
FIXTURE_FILES = frozenset({"expected-code"})


def _step_enhancement_violations(path: Path, document: dict[str, Any]) -> list[str]:
    """Fragment addressing rules that JSON Schema cannot express over companion files."""
    problems = []
    expected_id = path.name.removesuffix(".step-enhancement.yaml")
    if document.get("id") != expected_id:
        problems.append(f"prompt_fragment_invalid: enhancement id {document.get('id')!r} is not its file stem {expected_id!r}")
    entries = document.get("prompt_fragments")
    seen: set[str] = set()
    for index, entry in enumerate(entries if isinstance(entries, list) else []):
        if not isinstance(entry, dict):
            continue
        slot = entry.get("slot")
        if isinstance(slot, str):
            if slot in seen:
                problems.append(f"prompt_fragment_invalid: enhancement names slot {slot!r} more than once")
            seen.add(slot)
        companion = entry.get("path")
        if isinstance(companion, str) and not (path.parent / companion).is_file():
            problems.append(f"prompt_fragment_invalid at /prompt_fragments/{index}/path: companion {companion!r} does not exist beside the enhancement")
    return problems


def validate_pack(pack_dir: Path, contract: Contract) -> PackReport:
    """Validate every file of one pack directory; violations are sorted and path-relative."""
    if not pack_dir.is_dir():
        raise GateError(f"{pack_dir} is not a directory")
    report = PackReport(pack=pack_dir.name)
    descriptor = _load_or_none(pack_dir / "pack.yaml")
    require_empty_slots = isinstance(descriptor, dict) and descriptor.get("schema_version") == "1.0"
    manifest: dict[str, Any] | None = None
    payloads: set[str] = set()
    sidecars: list[tuple[str, str]] = []
    constituent_files: set[str] = set()
    for path in sorted(pack_dir.rglob("*")):
        inside = path.relative_to(pack_dir).as_posix()
        relative = f"{pack_dir.name}/{inside}"
        if path.is_symlink():  # a file or a directory; not followed, so a link cannot smuggle files in or out
            report.violations.append(f"{relative}: symlink: a pack holds regular files and directories only")
            continue
        if not path.is_file():
            if not path.is_dir():
                report.violations.append(f"{relative}: not a regular file or directory")
            continue
        kind, rule = classify(contract, relative)
        if kind == "retired" and rule is not None:
            report.violations.append(f"{relative}: retired layout: {rule.reason}")
            continue
        if kind == "payload" and inside.startswith("assets/"):
            payloads.add(inside.removeprefix("assets/"))
        if kind != "file" or rule is None:
            tokens = path.name.rsplit(".", 2)
            if kind == "unmodelled" and path.suffix == ".yaml" and len(tokens) == 3 and tokens[1] in KNOWN_KIND_TOKENS:
                raise GateError(f"{relative}: a `{tokens[1]}` file has no schema mapping in file-kinds.yaml")
            if kind == "unmodelled" and inside not in FIXTURE_FILES:
                report.violations.append(f"{relative}: unmodelled: no file-kinds.yaml rule models this file; "
                                         "the charter refuses it at registration")
                continue
            if kind == "ignored" and rule is not None and not any(allowed.match(relative) for allowed in NOT_HELD_ALLOWANCES):
                report.violations.append(
                    f"{relative}: not_held: the charter leaves this file out ({rule.match}: {rule.reason}); "
                    "only README.md notes and *.skill.md bodies may be carried unheld"
                )
                continue
            report.skipped += 1
            continue
        validator = contract.validators.get(rule.schema or "")
        if validator is None:
            raise GateError(f"{relative}: rule {rule.match!r} names schema {rule.schema!r}, which is not loaded")
        try:
            # Bytes, not read_text: universal newlines would turn a CR into LF before the Markdown
            # reader could refuse it, as the charter does.
            text = path.read_bytes().decode("utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            raise GateError(f"{relative}: unreadable: {exc!r}") from exc
        report.checked += 1
        try:
            document = parse_markdown(text) if rule.content_form == "markdown" else load_yaml(text)
        except (yaml.YAMLError, MarkdownRefused) as exc:
            report.violations.append(f"{relative}: not readable as {rule.content_form}: {_short(str(exc))}")
            continue
        errors = sorted(validator.iter_errors(document), key=lambda e: (list(map(str, e.absolute_path)), e.message))
        for error in errors:
            where = "/" + "/".join(str(part) for part in error.absolute_path)
            report.violations.append(f"{relative}: {rule.schema} schema at {where}: {_short(error.message)}")
        if rule.schema == "mission-step-prompt":
            for problem in prompt_slot_violations(text, require_empty=True):
                if problem.startswith("prompt_slot_not_empty") and not require_empty_slots:
                    report.warnings.append(f"{relative}: {problem}; an unversioned descriptor keeps this legacy block, descriptor 1.0 refuses it")
                else:
                    report.violations.append(f"{relative}: {problem}")
        elif rule.schema == "prompt-fragment":
            report.violations += [f"{relative}: {problem}" for problem in prompt_fragment_violations(text)]
        elif rule.schema == "step-enhancement" and isinstance(document, dict):
            report.violations += [f"{relative}: {problem}" for problem in _step_enhancement_violations(path, document)]
        if inside == MANIFEST_NAME and rule.schema == "pack-manifest" and not errors:
            manifest = document
        if rule.schema in MANIFEST_CONSTITUENT_SCHEMAS:
            constituent_files.add(inside)
        if rule.schema == "asset" and isinstance(document, dict) and isinstance(document.get("path"), str):
            sidecars.append((relative, document["path"]))
        # The charter's rule (spec pack-level-files FR-003): a preset's id is its file stem.
        if rule.schema == "preset" and isinstance(document, dict) and "id" in document and document["id"] != path.stem:
            report.violations.append(f"{relative}: preset id {document['id']!r} is not its file stem {path.stem!r}")
    # A pack with pack-level files (its README.md document, a manifest) needs its descriptor even when
    # judged alone. A pack with no descriptor at all is refused when the packs are checked together.
    if not (pack_dir / "pack.yaml").is_file() and any((pack_dir / n).is_file() for n in ("README.md", MANIFEST_NAME)):
        report.violations.append(
            f"{pack_dir.name}/pack.yaml: missing: a pack with a README.md or a {MANIFEST_NAME} needs its descriptor"
        )
    # The charter's SidecarPayloads rule: a sidecar names, exactly, an asset payload the pack holds.
    report.violations += [f"{file}: payload assets/{named} does not exist" for file, named in sidecars if named not in payloads]
    if manifest is not None:
        for stale in stale_manifest_fields(manifest, _bytes_reader(pack_dir)):
            remedy = (
                "restore the file or remove its entry" if stale.startswith("missing: ")
                else f"run `{REGENERATE_COMMAND} {pack_dir}`"
            )
            report.violations.append(f"{pack_dir.name}/{MANIFEST_NAME}: stale manifest: {stale}; {remedy}")
        report.violations += [
            f"{pack_dir.name}/{MANIFEST_NAME}: incomplete manifest: {unlisted} is not a constituent; "
            f"add its entry, then run `{REGENERATE_COMMAND} {pack_dir}`"
            for unlisted in unlisted_constituents(manifest, constituent_files)
        ]
        report.violations += [
            f"{pack_dir.name}/{MANIFEST_NAME}: incomplete manifest: graph node {node} is not a constituent; "
            f"add its entry, then run `{REGENERATE_COMMAND} {pack_dir}`"
            for node in unlisted_nodes(manifest, declared_nodes(pack_dir))
        ]
    if report.checked == 0:
        raise GateError(f"{pack_dir}: no pack file was checked; the gate would prove nothing")
    return report


# --------------------------------------------------------------------------- cross-pack checks


def _singular(kind: str) -> str:
    """``directives`` -> ``directive``: fragments name kinds in the plural, URNs in the singular."""
    return kind.removesuffix("s")


def _load_or_none(path: Path) -> Any:
    try:
        return load_yaml(path.read_bytes().decode("utf-8"))
    except (OSError, UnicodeDecodeError, yaml.YAMLError):
        return None  # the per-pack validation already reports an unreadable file


#: Schemas of the artifact files whose ``id`` is a declaration of a node kind (the schema name with
#: ``-`` for ``_`` is the kind): ``qa-plan.step-contract.yaml`` declares ``mission_step_contract:qa-plan``.
ARTIFACT_SCHEMAS = frozenset(
    {
        "directive", "tactic", "styleguide", "toolguide", "paradigm", "procedure",
        "agent-profile", "mission-step-contract", "asset", "glossary-pack", "skill",
        "step-enhancement",
    }
)  # fmt: skip


def declared_nodes(pack_dir: Path, contract: Contract | None = None) -> set[tuple[str, str]]:
    """The ``(kind, id)`` pairs a pack declares: the nodes of its ``drg/fragment.yaml`` (``kind``
    plural, ``id``), of its root ``*.graph.yaml`` files (``urn``) and, given the contract, the
    ``id`` of each artifact file it classifies (kind from the file's schema). A file and a node of
    the same pack for one id are one declaration."""
    found: set[tuple[str, str]] = set()
    if contract is not None:
        for path in sorted(pack_dir.rglob("*.yaml")):
            if path.is_symlink() or not path.is_file():
                continue
            _, rule = classify(contract, f"{pack_dir.name}/{path.relative_to(pack_dir).as_posix()}")
            if rule is None or rule.schema not in ARTIFACT_SCHEMAS:
                continue
            document = _load_or_none(path)
            if isinstance(document, dict) and isinstance(document.get("id"), str):
                found.add((rule.schema.replace("-", "_"), document["id"]))
    fragment = _load_or_none(pack_dir / "drg" / "fragment.yaml")
    for node in (fragment.get("nodes") or []) if isinstance(fragment, dict) else []:
        if isinstance(node, dict) and isinstance(node.get("id"), str) and isinstance(node.get("kind"), str):
            found.add((_singular(node["kind"]), node["id"]))
    for graph_file in sorted(pack_dir.glob("*.graph.yaml")):
        graph = _load_or_none(graph_file)
        for node in (graph.get("nodes") or []) if isinstance(graph, dict) else []:
            urn = node.get("urn") if isinstance(node, dict) else None
            if isinstance(urn, str) and ":" in urn:
                kind, _, node_id = urn.partition(":")
                found.add((kind, node_id))
    return found


#: A template's id is its path: ``templates/<path>``, or ``<type>/<path>`` under a mission type.
TEMPLATE_PATH = re.compile(r"(?:missions/([^/]+)/)?templates/(.+)")


def held_artifacts(pack_dir: Path, contract: Contract | None) -> set[tuple[str, str]]:
    """The ``(kind, id)`` pairs a pack holds, in the charter's sense (``compositionFacts``): its
    artifact files and its ``anti_pattern`` nodes. Any other node without a file is held by nobody."""
    held = {key for key in declared_nodes(pack_dir) if key[0] == "anti_pattern"}
    for path in sorted(pack_dir.rglob("*")) if contract is not None else []:
        if path.is_symlink() or not path.is_file():
            continue
        relative = path.relative_to(pack_dir).as_posix()
        category, rule = classify(contract, f"{pack_dir.name}/{relative}")
        template = TEMPLATE_PATH.fullmatch(relative) if category == "payload" else None
        if template:
            held.add(("template", "/".join(part for part in template.groups() if part)))
        elif rule is not None and rule.schema in ARTIFACT_SCHEMAS | {"mission-type"}:
            document = _load_or_none(path)
            artifact_id = document.get("profile-id", document.get("id")) if isinstance(document, dict) else None
            if isinstance(artifact_id, str):
                held.add((rule.schema.replace("-", "_"), artifact_id))
    return held


def split_qualifier(reference: str) -> tuple[str | None, str]:
    """``<pack>::<rest>`` as ``(pack, rest)``; a bare reference as ``(None, reference)``."""
    qualifier, separator, rest = reference.partition("::")
    return (qualifier, rest) if separator else (None, reference)


def graph_edges(pack_dir: Path) -> Iterator[tuple[Path, dict[str, Any]]]:
    """Every edge dictionary in a pack's DRG fragment and root graph documents, in stable order."""
    for graph in [pack_dir / "drg" / "fragment.yaml", *sorted(pack_dir.glob("*.graph.yaml"))]:
        document = _load_or_none(graph)
        for edge in (document.get("edges") or []) if isinstance(document, dict) else []:
            if isinstance(edge, dict):
                yield graph, edge


#: The agent-profile reference fields, the kind each names and the key an entry is keyed by:
#: ``directive-references`` entries carry a ``code`` (``QA_001``), the others an ``id``.
#: Together with ``collaboration.operating-procedures`` (plain strings naming procedures) these
#: are the selection data ADR-0064 keeps out of the graph; charter ADR-0053 decision 7 writes a
#: reference to another pack's artifact as ``<pack>::<id>`` in them.
PROFILE_REFERENCE_FIELDS = frozenset(
    {
        ("directive-references", "directive", "code"),
        ("tactic-references", "tactic", "id"),
        ("styleguide-references", "styleguide", "id"),
        ("toolguide-references", "toolguide", "id"),
    }
)


def _reference_keys(kind: str, reference: str) -> tuple[tuple[str, str], ...]:
    """The ``held`` keys a profile reference of ``kind`` names. A directive's code is its id
    (``QA_001``) or — built-in's convention — the number after ``DIRECTIVE_`` in its id: the
    code ``010`` names ``DIRECTIVE_010``."""
    return ((kind, reference), (kind, f"DIRECTIVE_{reference}")) if kind == "directive" else ((kind, reference),)


def profile_references(pack_dir: Path, contract: Contract | None) -> Iterator[tuple[str, str, str]]:
    """``(file, kind, reference)`` for every artifact an agent profile of ``pack_dir`` names
    in its directive-, tactic-, styleguide- and toolguide-references (a directive by its
    ``code``, the others by their ``id``) and in its collaboration operating-procedures. A
    reference is bare when it names the profile's own pack and ``<pack>::<id>`` when it names
    another pack's (charter ADR-0053 decision 7). Only files the contract classifies as agent
    profiles are read; without a contract none are."""
    for path in sorted(pack_dir.rglob("*.agent.yaml")) if contract is not None else []:
        if path.is_symlink() or not path.is_file():
            continue
        relative = path.relative_to(pack_dir).as_posix()
        _, rule = classify(contract, f"{pack_dir.name}/{relative}")
        if rule is None or rule.schema != "agent-profile":
            continue
        document = _load_or_none(path)
        if not isinstance(document, dict):
            continue
        file = f"{pack_dir.name}/{relative}"
        for field, kind, key in sorted(PROFILE_REFERENCE_FIELDS):
            for entry in document.get(field) or []:
                if isinstance(entry, dict) and isinstance(entry.get(key), str):
                    yield file, kind, entry[key]
        collaboration = document.get("collaboration")
        procedures = collaboration.get("operating-procedures") if isinstance(collaboration, dict) else None
        for procedure in procedures if isinstance(procedures, list) else []:
            if isinstance(procedure, str):
                yield file, "procedure", procedure


def _depends_on(pack: Path, descriptors: dict[Path, dict[str, Any]], by_id: dict[str, Path]) -> list[Path]:
    """The packs ``pack``'s ``depends_on`` names that resolve to a configured pack, in the order
    written; an unknown id names none."""
    entries = descriptors[pack].get("depends_on")
    targets = []
    for entry in entries if isinstance(entries, list) else []:
        pack_id = entry.get("pack_id") if isinstance(entry, dict) else None
        target = by_id.get(pack_id) if isinstance(pack_id, str) else None
        if target is not None:
            targets.append(target)
    return targets


def _depends_on_closure(pack: Path, descriptors: dict[Path, dict[str, Any]], by_id: dict[str, Path]) -> set[Path]:
    """The pack and every pack it reaches through ``depends_on``, which names packs by ``pack_id``."""
    reached, pending = {pack}, [pack]
    while pending:
        for target in _depends_on(pending.pop(), descriptors, by_id):
            if target not in reached:
                reached.add(target)
                pending.append(target)
    return reached


def _descriptors(pack_dirs: list[Path]) -> dict[Path, dict[str, Any]]:
    loaded = {pack: _load_or_none(pack / "pack.yaml") for pack in pack_dirs}
    return {pack: document if isinstance(document, dict) else {} for pack, document in loaded.items()}


def profile_reference_violations(
    pack_dirs: list[Path], held: dict[Path, set[tuple[str, str]]], contract: Contract | None = None
) -> list[str]:
    """Agent-profile references, judged like edge ends (charter ADR-0053 decision 7): a bare id held
    only by another pack, or by no pack at all (which resolves to no artifact), is refused; a reference
    qualified with the profile's own pack is refused, because references inside one pack stay bare; a
    qualified one must name a pack of the closure that holds it.

    Kept because the charter service does not make these checks: a scratch pack with each of these
    defects composes (``GET /offering``) and registers (``PUT /packs/{packId}``) without a refusal
    (``docs/guides/validate-a-pack.md``, "What the service owns and what stays here"). The composition
    rules the service does make (descriptors, ``depends_on``, edge ends) are not repeated here."""
    descriptors = _descriptors(pack_dirs)
    by_id = {d["pack_id"]: pack for pack, d in descriptors.items() if isinstance(d.get("pack_id"), str)}
    by_name = {d["name"]: pack for pack, d in descriptors.items() if isinstance(d.get("name"), str)}
    violations: list[str] = []
    for pack in pack_dirs:
        closure = _depends_on_closure(pack, descriptors, by_id)
        for file, kind, reference in profile_references(pack, contract):
            qualifier, ref_id = split_qualifier(reference)
            keys = _reference_keys(kind, ref_id)
            if qualifier is None:
                holder = next((other.name for other, nodes in held.items() if any(key in nodes for key in keys)), None)
                if holder is None:
                    violations.append(f"{file}: bare {kind} reference {ref_id!r} resolves to no artifact of any pack")
                elif not any(key in held[pack] for key in keys):
                    violations.append(
                        f"{file}: bare {kind} reference {ref_id!r} is held only by {holder}; qualify it with that pack's name"
                    )
            else:
                named = by_name.get(qualifier)
                # the own pack, named by its descriptor name or by its directory (the natural way
                # a pack qualifies itself, `qa::x` in the pack of packs/qa): references inside
                # one pack stay bare, so no qualifier may name it
                if named is pack or (named is None and qualifier == pack.name):
                    violations.append(
                        f"{file}: reference '{qualifier}::{ref_id}' names this profile's own pack; "
                        "references inside one pack stay bare"
                    )
                elif named not in closure:
                    violations.append(f"{file}: reference '{qualifier}::{ref_id}' names a pack outside this pack's depends_on closure")
                elif not any(key in held[named] for key in keys):
                    violations.append(f"{file}: reference '{qualifier}::{ref_id}': {qualifier} does not hold {kind} {ref_id!r}")
    return violations


def prompt_fragment_composition_violations(pack_dirs: list[Path]) -> list[str]:
    """Resolve every fragment's target step and slot, independently of activation (ADR-0066 d8).

    Kept because the charter service resolves neither: an enhancement whose ``enhances`` target names
    a step the mission does not have, or whose fragment names a slot the step's prompt does not
    declare, composes and registers without a refusal. What the service does refuse is not repeated:
    an enhancement without exactly one ``enhances`` edge, and a target that is not ``action:<type>/<step>``
    (both ``pack_unreadable`` at composition, ``validation_failed`` at registration).

    Sibling enhancements are deliberately not a conflict. The graph's ``enhances`` edge
    is the only target field; no target or activation key is read from the enhancement.

    This checkout has no mission-step integrity metadata, so it cannot refuse enhancement of a
    locked step. It also reads the target pack's declared prompt directly: prompt overrides that
    drop a slot are a charter-service check, not reproduced here (no pack overrides these prompts).
    """
    descriptors = _descriptors(pack_dirs)
    by_id = {d["pack_id"]: pack for pack, d in descriptors.items() if isinstance(d.get("pack_id"), str)}
    by_name = {document.get("name"): pack for pack, document in descriptors.items() if isinstance(document.get("name"), str)}
    problems: list[str] = []
    for pack in pack_dirs:
        pack_name = descriptors[pack].get("name")
        closure = _depends_on_closure(pack, descriptors, by_id)
        edges = list(graph_edges(pack))
        for enhancement in sorted(pack.glob("missions/*/enhancements/*.step-enhancement.yaml")):
            document = _load_or_none(enhancement)
            fragments = document.get("prompt_fragments") if isinstance(document, dict) else None
            if not isinstance(fragments, list) or not fragments:
                continue
            enhancement_id = document.get("id")
            source = f"step_enhancement:{enhancement_id}"
            targets = []
            for graph, edge in edges:
                qualifier, urn = split_qualifier(edge.get("source", ""))
                if edge.get("relation") == "enhances" and urn == source and (qualifier in (None, pack_name)):
                    targets.append((graph, edge.get("target")))
            file = f"{pack.name}/{enhancement.relative_to(pack).as_posix()}"
            if len(targets) != 1 or not isinstance(targets[0][1], str):
                continue  # the service refuses an enhancement without exactly one enhances edge
            target = targets[0][1]
            qualifier, urn = split_qualifier(target)
            target_pack = pack if qualifier is None else by_name.get(qualifier)
            if qualifier is not None and (target_pack is None or target_pack not in closure):
                continue  # the service refuses a qualifier outside the closure
            kind, _, action = urn.partition(":")
            if kind != "action" or action.count("/") != 1:
                continue  # the service refuses a target that is not action:<type>/<step>
            mission_id, step_id = action.split("/")
            mission_path = target_pack / "missions" / mission_id / f"{mission_id}.mission-type.yaml"
            mission = _load_or_none(mission_path)
            steps = []
            if isinstance(mission, dict):
                steps = [*(mission.get("steps") or []), *(mission.get("on_demand_steps") or [])]
            step = next((item for item in steps if isinstance(item, dict) and item.get("id") == step_id), None)
            if step is None:
                problems.append(f"{file}: pack_reference_artifact_missing: target {target!r} does not resolve to a step")
                continue
            prompt_path = step.get("prompt_path", f"steps/{step_id}.prompt.md")
            prompt = target_pack / "missions" / mission_id / prompt_path
            try:
                slots = declared_prompt_slots(prompt.read_text(encoding="utf-8"))
            except OSError:
                problems.append(f"{file}: pack_reference_artifact_missing: target {target!r} has no readable prompt at {prompt_path}")
                continue
            for index, fragment in enumerate(fragments):
                slot = fragment.get("slot") if isinstance(fragment, dict) else None
                if isinstance(slot, str) and slot not in slots:
                    problems.append(f"{file}: prompt_slot_missing at /prompt_fragments/{index}/slot: target {target!r} declares no slot {slot!r}")
    return problems


def cross_pack_violations(pack_dirs: list[Path], contract: Contract | None = None) -> list[str]:
    """The checks across all packs together that the charter service does not make. The service is
    the authority on composition (descriptors, ``depends_on``, edge ends, sibling conflicts) and runs
    in its own job (``scripts/ci/charter_service_check.py``); what is left here is what a scratch pack
    run through it showed it accepts:

    * an id declared by two packs of different levels: the service takes it as a layer override, this
      repository does not allow an org pack to re-declare a built-in id (the same id in two packs of
      one level is the service's ``pack_sibling_conflict``);
    * a preset ``activated_<kinds>`` entry naming an id no pack declares (checked against the
      declared ``(kind, id)`` pairs of all packs, so an id of another kind does not satisfy it);
      a ``must_have: true`` entry must be declared within the preset pack's ``depends_on`` closure
      (the charter's ``requiredNotHeld``), not merely by some pack;
    * a DRG edge endpoint written bare (``<kind>:<id>``) in a pack's fragment that resolves to no node
      of any pack (a qualified endpoint is the service's ``pack_reference_*``);
    * the agent-profile references of ``profile_reference_violations``;
    * the prompt-fragment resolution of ``prompt_fragment_composition_violations``.

    With ``contract``, artifact files count as declarations too (``declared_nodes``).

    Fails closed (GateError) when no pack declares any node.
    """
    held = {pack: held_artifacts(pack, contract) for pack in pack_dirs}
    levels = {pack: descriptor.get("pack_level") for pack, descriptor in _descriptors(pack_dirs).items()}
    owners: dict[tuple[str, str], list[Path]] = {}
    for pack in pack_dirs:
        for key in declared_nodes(pack, contract):
            owners.setdefault(key, []).append(pack)
    if not owners:
        raise GateError("cross-pack checks: no pack declares any DRG node; the id index is empty and would prove nothing")
    violations = [
        f"{kind}:{node_id}: declared by packs of different levels "
        f"({', '.join(sorted(f'{pack.name} [{levels[pack]}]' for pack in packs))}); a pack re-declaring another level's id is not allowed here"
        for (kind, node_id), packs in sorted(owners.items())
        if len({levels[pack] for pack in packs}) > 1
    ]
    descriptors = _descriptors(pack_dirs)
    by_id = {d["pack_id"]: pack for pack, d in descriptors.items() if isinstance(d.get("pack_id"), str)}
    for pack in pack_dirs:
        closure = _depends_on_closure(pack, descriptors, by_id)
        for preset in sorted((pack / "presets").glob("*.yaml")):
            document = _load_or_none(preset)
            if not isinstance(document, dict):
                continue
            for key, entries in sorted(document.items()):
                if not key.startswith("activated_") or not isinstance(entries, list):
                    continue
                kind = _singular(key.removeprefix("activated_"))
                for entry in entries:
                    entry_id = entry.get("id") if isinstance(entry, dict) else None
                    if not isinstance(entry_id, str):
                        continue
                    if (kind, entry_id) not in owners:
                        violations.append(
                            f"{pack.name}/presets/{preset.name}: {key} names {entry_id!r}, which no pack declares as a {kind}"
                        )
                    elif entry.get("must_have") is True and not closure.intersection(owners[(kind, entry_id)]):
                        reached = ", ".join([pack.name, *sorted(p.name for p in closure if p != pack)])
                        violations.append(
                            f"{pack.name}/presets/{preset.name}: {key} names {entry_id!r} as must_have, but no pack in its "
                            f"depends_on closure ({reached}) declares it as a {kind}"
                        )
        fragment = _load_or_none(pack / "drg" / "fragment.yaml")
        for edge in (fragment.get("edges") or []) if isinstance(fragment, dict) else []:
            if not isinstance(edge, dict):
                continue
            for end in ("source", "target"):
                urn = edge.get(end)
                if not isinstance(urn, str):
                    continue
                qualifier, rest = split_qualifier(urn)
                kind, _, node_id = rest.partition(":")
                if qualifier is None and (kind, node_id) not in owners and not any((kind, node_id) in nodes for nodes in held.values()):
                    violations.append(
                        f"{pack.name}/drg/fragment.yaml: edge {end} {urn!r} resolves to no node of any pack"
                    )
    return (
        violations
        + profile_reference_violations(pack_dirs, held, contract)
        + prompt_fragment_composition_violations(pack_dirs)
    )


# --------------------------------------------------------------------------- CLI


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("packs", nargs="*", type=Path, help="pack directories that must validate")
    parser.add_argument("--expect-invalid", action="append", default=[], type=Path, metavar="PACK",
                        help="a pack directory that must produce schema violations (non-vacuity)")
    parser.add_argument("--regenerate-manifest", action="append", default=[], type=Path, metavar="PACK",
                        help="restamp the content_hash and manifest_hash fields of PACK/pack-manifest.yaml "
                             "(membership is kept); refused, exit 1, if a listed file is missing. Validates only the "
                             "packs also given as positional arguments")
    parser.add_argument("--cross-pack", action="store_true",
                        help="also check the given packs together, for what the charter service does not "
                             "(scripts/ci/charter_service_check.py): preset ids, bare DRG edge endpoints, an id re-declared "
                             "at another level, agent-profile references and prompt-fragment targets and slots")
    parser.add_argument("--contract", type=Path, help="directory holding file-kinds.yaml and schemas/")
    args = parser.parse_args(argv)
    if not args.packs and not args.expect_invalid and not args.regenerate_manifest:
        parser.error("give at least one pack directory")
    try:
        status = EXIT_OK
        for pack in args.regenerate_manifest:
            missing = regenerate_manifest(pack)
            for path in missing:
                print(f"::error file={pack}::{path} is listed in {MANIFEST_NAME} but is missing, not a regular file "
                      "or outside the pack; restore it or remove its entry")
            if missing:
                print(f"not regenerated: {pack / MANIFEST_NAME} ({len(missing)} listed files missing)")
                status = EXIT_INVALID
            else:
                print(f"regenerated: {pack / MANIFEST_NAME}")
        if not args.packs and not args.expect_invalid:
            return status
        contract = contract_for(args.contract)
        print(f"charter contract: {args.contract or os.environ.get('CHARTER_CONTRACT_DIR') or charter_commit()}; "
              f"{len(contract.validators)} schemas loaded")
        for pack in args.packs:
            report = validate_pack(pack, contract)
            for line in report.warnings:
                print(f"::warning file={pack}::{line}")
            for line in report.violations:
                print(f"::error file={pack}::{line}")
            print(f"{'ok' if report.ok else 'FAIL'}: {pack} ({report.checked} files checked, "
                  f"{report.skipped} excluded or payload, {len(report.violations)} violations)")
            status = status or (EXIT_OK if report.ok else EXIT_INVALID)
        if args.cross_pack:
            found = cross_pack_violations(args.packs, contract)
            for line in found:
                print(f"::error::cross-pack: {line}")
            print(f"{'ok' if not found else 'FAIL'}: cross-pack checks over {len(args.packs)} packs ({len(found)} violations)")
            status = status or (EXIT_OK if not found else EXIT_INVALID)
        for pack in args.expect_invalid:
            report = validate_pack(pack, contract)
            if report.ok:
                print(f"::error file={pack}::{pack} is an invalid fixture but passed schema validation; the gate is vacuous")
                status = EXIT_INVALID
            else:
                print(f"ok: {pack} fails validation as expected ({len(report.violations)} violations)")
    except GateError as exc:
        print(f"::error::cannot judge, failing closed: {exc}")
        return EXIT_GATE
    return status


if __name__ == "__main__":
    sys.exit(main())
