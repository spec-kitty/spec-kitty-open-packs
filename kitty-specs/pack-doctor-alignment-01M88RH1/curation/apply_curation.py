#!/usr/bin/env python3
"""Apply and check the anti-pattern curation ledgers of Mission pack-doctor-alignment-01M88RH1.

The contract is curation/README.md. In short:

* A ledger (``ledger-*.yaml`` beside this script) holds one row per inline ``anti_patterns``
  entry or file-less ``anti_pattern`` node. ``merge-map.yaml`` clusters the inline entries by
  meaning (decision Q1) and names each cluster's home pack.
* ``apply`` writes each ``anti_patterns/<id>.anti-pattern.yaml`` in its home pack, adds its
  graph node and a ``rejects`` edge from each former owner (pack-qualified across packs),
  applies the map's ``depends_on_added``, and deletes an inline block once every entry of it
  has been applied. It is deterministic and idempotent, and it refuses, writing nothing, on
  any fault it can see before writing.
* ``--check`` proves the data-model invariants over a tree.

Standard library plus PyYAML only. Mission tooling, not a product surface.
"""
from __future__ import annotations

import argparse
import copy
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
ID_RE = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$")
QUALIFIED_RE = re.compile(r"^(?P<pack>[a-z0-9][a-z0-9-]*)::anti_pattern:(?P<id>[a-z0-9-]+)$")
SOURCE_RE = re.compile(r"^(?P<path>[^#]+)#/(?P<block>anti_patterns|nodes)/(?P<index>\d+)$")
TOP_KEY_RE = re.compile(r"^[A-Za-z_][\w-]*\s*:")
SEVERITIES = ("smell", "severe", "breaking")
OWNER_KINDS = {"styleguides": "styleguide", "procedures": "procedure"}
FILE_KEYS = ("schema_version", "id", "title", "description", "severity", "bad_example", "good_example")
PERKIND_HEADER = "schema_version: '1.0'\ngenerated_at: STATIC\ngenerated_by: drg-migration-v1\n"


class Refusal(Exception):
    """A fault found before anything is written."""


# --------------------------------------------------------------------------- YAML text helpers


class _LiteralDumper(yaml.SafeDumper):
    pass


def _str_representer(dumper, value):
    style = "|" if "\n" in value else None
    return dumper.represent_scalar("tag:yaml.org,2002:str", value, style=style)


_LiteralDumper.add_representer(str, _str_representer)


def dump(data) -> str:
    return yaml.dump(data, Dumper=_LiteralDumper, sort_keys=False, allow_unicode=True, width=120,
                     default_flow_style=False)


def verbatim(text) -> str:
    """Source text as written, with only the block scalar's trailing line breaks removed."""
    return text.rstrip("\n") if isinstance(text, str) else text


def _block_span(lines: list[str], key: str) -> tuple[int, int] | None:
    """The [start, end) line span of top-level ``key`` and its block, keeping col-0 comments
    and blank lines that lead into the next top-level key."""
    start = next((i for i, l in enumerate(lines) if re.match(rf"^{re.escape(key)}\s*:", l)), None)
    if start is None:
        return None
    end = len(lines)
    for i in range(start + 1, len(lines)):
        if TOP_KEY_RE.match(lines[i]) or lines[i].startswith("---"):
            end = i
            break
    while end > start + 1 and (not lines[end - 1].strip() or lines[end - 1].startswith("#")):
        end -= 1
    return start, end


def remove_top_level_key(text: str, key: str) -> str:
    """Delete ``key`` and its block textually; prove the rest of the document unchanged."""
    before = yaml.safe_load(text)
    lines = text.splitlines(keepends=True)
    span = _block_span(lines, key)
    if span is None:
        return text
    start, end = span
    out = lines[:start] + lines[end:]
    # Collapse blank lines only at the seam the removal leaves; the rest of the file keeps its spacing.
    if start == len(out):
        while out and not out[-1].strip():
            out.pop()
    else:
        while 0 < start < len(out) and not out[start - 1].strip() and not out[start].strip():
            del out[start]
    result = "".join(out)
    expected = {k: v for k, v in before.items() if k != key}
    if yaml.safe_load(result) != expected:
        raise Refusal(f"removing '{key}' textually would change other keys")
    return result


def append_list_items(text: str, key: str, items: list) -> str:
    """Append ``items`` to the top-level block list ``key``, keeping its indentation and the
    rest of the text; create the key when it is absent or an empty flow list."""
    if not items:
        return text
    before = yaml.safe_load(text) if text.strip() else {}
    lines = text.splitlines(keepends=True)
    if lines and not lines[-1].endswith("\n"):
        lines[-1] += "\n"
    span = _block_span(lines, key)

    def render(indent: str) -> list[str]:
        rendered = dump(items).splitlines(keepends=True)
        return [indent + l if l.strip() else l for l in rendered]

    if span is None:
        new = lines + [f"{key}:\n"] + render("")
    else:
        start, end = span
        head = lines[start]
        if re.match(rf"^{re.escape(key)}\s*:\s*\[\s*\]\s*(#.*)?$", head.rstrip("\n")):
            new = lines[:start] + [f"{key}:\n"] + render("") + lines[start + 1:]
        else:
            body = lines[start + 1:end]
            dash = next((re.match(r"^(\s*)- ", l) for l in body if re.match(r"^\s*- ", l)), None)
            indent = dash.group(1) if dash else ""
            last = max((i for i, l in enumerate(body) if l.strip() and not l.lstrip().startswith("#")),
                       default=-1)
            at = start + 1 + last + 1
            new = lines[:at] + render(indent) + lines[at:]
    result = "".join(new)
    expected = copy.deepcopy(before) or {}
    expected[key] = list(expected.get(key) or []) + items
    if yaml.safe_load(result) != expected:
        raise Refusal(f"appending to '{key}' textually would change the document")
    return result


def replace_list_items(text: str, key: str, match, replace) -> tuple[str, int]:
    """Re-render each item of the top-level block list ``key`` for which ``match(item)`` holds as
    ``replace(item)``, keeping every other line; return the text and the number replaced."""
    before = yaml.safe_load(text) if text.strip() else {}
    lines = text.splitlines(keepends=True)
    span = _block_span(lines, key)
    if span is None:
        return text, 0
    start, end = span
    body = lines[start + 1:end]
    dash = next((re.match(r"^(\s*)- ", l) for l in body if re.match(r"^\s*- ", l)), None)
    if dash is None:
        return text, 0
    indent = dash.group(1)
    starts = [i for i, l in enumerate(body) if l.startswith(indent + "- ")] + [len(body)]
    out, count, expected = [], 0, []
    out.extend(body[:starts[0]])
    for a, b in zip(starts, starts[1:]):
        chunk = body[a:b]
        tail = []
        while chunk and (not chunk[-1].strip() or chunk[-1].lstrip().startswith("#")):
            tail.insert(0, chunk.pop())
        item = yaml.safe_load("".join(l[len(indent):] if l.startswith(indent) else l for l in chunk))[0]
        if match(item):
            item = replace(item)
            chunk = [indent + l if l.strip() else l for l in dump([item]).splitlines(keepends=True)]
            count += 1
        expected.append(item)
        out.extend(chunk + tail)
    result = "".join(lines[:start + 1] + out + lines[end:])
    want = copy.deepcopy(before)
    want[key] = expected
    if yaml.safe_load(result) != want:
        raise Refusal(f"rewriting items of '{key}' textually would change the document")
    return result, count


# --------------------------------------------------------------------------- the tree


@dataclass
class Pack:
    name: str
    path: Path
    pack_id: str
    depends_on: list[str]  # pack ids
    layout: str  # "fragment" or "perkind"


@dataclass
class Tree:
    root: Path
    texts: dict[Path, str] = field(default_factory=dict)  # pending writes
    deleted_blocks: set[Path] = field(default_factory=set)

    @property
    def packs_dir(self) -> Path:
        return self.root / "packs"

    def read(self, path: Path) -> str | None:
        if path in self.texts:
            return self.texts[path]
        return path.read_text(encoding="utf-8") if path.exists() else None

    def load(self, path: Path):
        text = self.read(path)
        return yaml.safe_load(text) if text is not None else None

    def write(self, path: Path, text: str) -> None:
        self.texts[path] = text

    def packs(self) -> dict[str, Pack]:
        out = {}
        for desc in sorted(self.packs_dir.glob("*/pack.yaml")):
            data = self.load(desc) or {}
            directory = desc.parent
            name = data.get("name") or directory.name
            deps = [d.get("pack_id") for d in (data.get("depends_on") or []) if isinstance(d, dict)]
            layout = "fragment" if (directory / "drg" / "fragment.yaml").exists() else "perkind"
            out[directory.name] = Pack(name, directory, data.get("pack_id"), deps, layout)
        return out

    def closure(self, packs: dict[str, Pack], start: str) -> set[str]:
        by_id = {p.pack_id: key for key, p in packs.items()}
        seen: set[str] = set()
        stack = [by_id.get(i) for i in packs[start].depends_on]
        while stack:
            key = stack.pop()
            if key is None or key in seen:
                continue
            seen.add(key)
            stack.extend(by_id.get(i) for i in packs[key].depends_on)
        return seen

    def cycle(self, packs: dict[str, Pack]) -> list[str] | None:
        by_id = {p.pack_id: key for key, p in packs.items()}
        state: dict[str, int] = {}
        path: list[str] = []

        def visit(key: str) -> list[str] | None:
            state[key] = 1
            path.append(key)
            for dep in packs[key].depends_on:
                nxt = by_id.get(dep)
                if nxt is None:
                    continue
                if state.get(nxt) == 1:
                    return path[path.index(nxt):] + [nxt]
                if nxt not in state and (found := visit(nxt)):
                    return found
            path.pop()
            state[key] = 2
            return None

        for key in sorted(packs):
            if key not in state and (found := visit(key)):
                return found
        return None

    # graph documents ------------------------------------------------------

    def graph_docs(self, pack: Pack) -> list[Path]:
        if pack.layout == "fragment":
            return [pack.path / "drg" / "fragment.yaml"]
        docs = set(pack.path.glob("*.graph.yaml")) | {p for p in self.texts if p.parent == pack.path
                                                     and p.name.endswith(".graph.yaml")}
        return sorted(docs)

    def anti_pattern_nodes(self, pack: Pack) -> dict[str, str]:
        """id -> graph doc for every anti-pattern node in the pack."""
        out = {}
        for doc in self.graph_docs(pack):
            for node in (self.load(doc) or {}).get("nodes") or []:
                if pack.layout == "fragment" and node.get("kind") == "anti_patterns":
                    out[node.get("id")] = doc
                elif pack.layout == "perkind" and node.get("kind") == "anti_pattern":
                    out[str(node.get("urn", "")).split(":", 1)[-1]] = doc
        return out

    def edges(self, pack: Pack) -> set[tuple[str, str, str]]:
        out = set()
        for doc in self.graph_docs(pack):
            for edge in (self.load(doc) or {}).get("edges") or []:
                out.add((edge.get("source"), edge.get("target"), edge.get("relation")))
        return out


# --------------------------------------------------------------------------- ledgers


@dataclass
class Row:
    ledger: Path
    data: dict

    def get(self, key, default=None):
        return self.data.get(key, default)

    @property
    def label(self) -> str:
        return f"{self.ledger.name}: {self.get('source')}"

    @property
    def merged(self) -> bool:
        return bool(self.get("merged_into"))

    @property
    def home_pack(self) -> str:
        return self.get("home_pack") or self.get("pack")

    @property
    def target(self) -> tuple[str, str]:
        """(home pack, id) of the file this row is, or merges into."""
        if self.merged:
            m = QUALIFIED_RE.match(str(self.get("merged_into")))
            if not m:
                raise Refusal(f"{self.label}: merged_into must be <pack>::anti_pattern:<id>")
            return m.group("pack"), m.group("id")
        return self.home_pack, self.get("id")

    @property
    def source_parts(self) -> tuple[str, str, int]:
        m = SOURCE_RE.match(str(self.get("source") or ""))
        if not m:
            raise Refusal(f"{self.label}: source must be <pack-relative path>#/anti_patterns/<i> or #/nodes/<i>")
        return m.group("path"), m.group("block"), int(m.group("index"))


def load_rows(ledgers: list[Path]) -> list[Row]:
    rows = []
    for ledger in ledgers:
        data = yaml.safe_load(ledger.read_text(encoding="utf-8")) or {}
        rows.extend(Row(ledger, entry) for entry in data.get("entries") or [])
    return rows


def default_ledgers() -> list[Path]:
    return sorted(HERE.glob("ledger-*.yaml"))


def load_map(path: Path | None) -> dict | None:
    if path is None or not path.exists():
        return None
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def anti_pattern_file(tree: Tree, pack: str, ident: str) -> Path:
    return tree.packs_dir / pack / "anti_patterns" / f"{ident}.anti-pattern.yaml"


def file_body(row: Row) -> dict:
    body = {"schema_version": "1.0", "id": row.get("id"), "title": verbatim(row.get("title")),
            "description": verbatim(row.get("description")), "severity": row.get("severity"),
            "bad_example": verbatim(row.get("bad_example"))}
    if row.get("good_example"):
        body["good_example"] = verbatim(row.get("good_example"))
    return body


def owner_urn(row: Row) -> str | None:
    owner = row.get("owner")
    return str(owner) if owner else None


def edge_target(row: Row) -> str:
    home, ident = row.target
    return f"anti_pattern:{ident}" if home == row.get("pack") else f"{home}::anti_pattern:{ident}"


def source_entry(tree: Tree, packs: dict[str, Pack], row: Row):
    """The source entry, or None when its inline block is already gone."""
    path, block, index = row.source_parts
    pack = packs.get(row.get("pack"))
    if pack is None:
        raise Refusal(f"{row.label}: unknown pack '{row.get('pack')}'")
    doc = tree.load(pack.path / path)
    if doc is None:
        raise Refusal(f"{row.label}: {path} does not exist in pack {pack.name}")
    items = doc.get(block)
    if items is None:
        return None
    if index >= len(items):
        raise Refusal(f"{row.label}: {block} has no index {index}")
    return items[index]


def says_default(value: str) -> bool:
    """True when the text itself (not a quote of the source inside it) rests on a default."""
    # A quote counts as source text only when it holds more than the bare word: a quoted
    # "default" on its own is still the call resting on a default.
    def keep_bare(m: re.Match) -> str:
        inner = m.group(1).strip(" .,:;!?()'")
        return m.group(0) if re.fullmatch(r"default(s|ed)?", inner, re.IGNORECASE) else ""
    unquoted = re.sub(r'"([^"]*)"', keep_bare, value)
    return re.search(r"\bdefault", unquoted, re.IGNORECASE) is not None


def validate_row(row: Row) -> list[str]:
    faults = []
    ident = row.get("id")
    if not row.merged:
        if not isinstance(ident, str) or not ID_RE.match(ident) or len(ident) > 64:
            faults.append(f"{row.label}: id '{ident}' is not kebab-case of at most 64 characters")
        for key in ("title", "description", "bad_example"):
            if not row.get(key):
                faults.append(f"{row.label}: {key} is empty")
        if row.get("severity") not in SEVERITIES:
            faults.append(f"{row.label}: severity must be one of {', '.join(SEVERITIES)}")
    # A merged row's file, severity and bad example are its home row's; it owes the merge's reason.
    for key in (("merge_reason",) if row.merged else ("severity_grounding", "bad_example_source")):
        value = str(row.get(key) or "")
        if not value.strip():
            faults.append(f"{row.label}: {key} is empty")
        elif says_default(value):
            faults.append(f"{row.label}: {key} says 'default'")
    if row.get("operator_question"):
        faults.append(f"{row.label}: open operator_question")
    for target in row.get("also_rejects") or []:
        if not QUALIFIED_RE.match(str(target)):
            faults.append(f"{row.label}: also_rejects '{target}' must be <pack>::anti_pattern:<id>")
    for extra in row.get("also_rejected_by") or []:
        if not (isinstance(extra, dict) and re.match(r"^[a-z_]+:[\w-]+$", str(extra.get("owner", "")))
                and extra.get("pack") and extra.get("reason")):
            faults.append(f"{row.label}: also_rejected_by entries need owner (<kind>:<id>), pack and reason")
    update = row.get("reason_update")
    if update is not None and (row.merged or not isinstance(update, dict) or not update.get("from") or not update.get("to")):
        faults.append(f"{row.label}: reason_update needs from and to, on a non-merged row")
    return faults


def qualified_target(owner_pack: str, home: str, ident: str) -> str:
    return f"anti_pattern:{ident}" if home == owner_pack else f"{home}::anti_pattern:{ident}"


def extra_edges(row: Row) -> list[tuple[str, str, dict]]:
    """(owner pack, owner kind, edge) for each also_rejects / also_rejected_by edge of the row."""
    out = []
    home, ident = row.target
    if row.source_parts[1] == "anti_patterns":
        kind, owner_id = owner_urn(row).split(":", 1)
        for target in row.get("also_rejects") or []:
            m = QUALIFIED_RE.match(str(target))
            out.append((row.get("pack"), kind, {
                "source": owner_urn(row), "target": qualified_target(row.get("pack"), m.group("pack"), m.group("id")),
                "relation": "rejects", "reason": f"the {kind} {owner_id} names this anti-pattern"}))
    for extra in row.get("also_rejected_by") or []:
        kind = str(extra["owner"]).split(":", 1)[0]
        out.append((extra["pack"], kind, {"source": extra["owner"], "target": qualified_target(extra["pack"], home, ident),
                                          "relation": "rejects", "reason": verbatim(extra["reason"])}))
    return out


def _norm(text) -> str:
    return " ".join(str(text or "").split())


# --------------------------------------------------------------------------- apply


def plan_apply(tree: Tree, rows: list[Row], catalog: list[Row], merge_map: dict | None) -> list[str]:
    """Compute every write into ``tree.texts``; return the log. Raise Refusal on any fault."""
    packs = tree.packs()
    log: list[str] = []
    faults = [f for row in rows for f in validate_row(row)]

    targets: dict[tuple[str, str], Row] = {}
    for row in rows:
        if row.merged:
            continue
        key = (row.home_pack, row.get("id"))
        if key in targets:
            faults.append(f"{row.label}: id clash with {targets[key].label} in pack {key[0]}")
        targets[key] = row
    for row in rows:
        try:
            home, ident = row.target
        except Refusal as exc:
            faults.append(str(exc))
            continue
        if home not in packs:
            faults.append(f"{row.label}: home pack '{home}' does not exist")
        elif row.merged and (home, ident) not in targets and not anti_pattern_file(tree, home, ident).exists():
            faults.append(f"{row.label}: merged_into {row.get('merged_into')} resolves to no row or file")
    if faults:
        raise Refusal("\n".join(faults))

    # depends_on the merge map adds for the clusters these rows belong to.
    for change in _depends_on_added(merge_map, rows):
        pack, on, rng = change.get("pack"), change.get("depends_on"), change.get("range")
        if pack not in packs or on not in packs or not rng:
            raise Refusal(f"merge map depends_on_added {change}: unknown pack or missing range")
        if packs[on].pack_id in packs[pack].depends_on:
            continue
        desc = packs[pack].path / "pack.yaml"
        tree.write(desc, append_list_items(tree.read(desc), "depends_on",
                                           [{"pack_id": packs[on].pack_id, "range": str(rng)}]))
        packs = tree.packs()
        log.append(f"depends_on: {pack} -> {on} ({rng})")
    if cyc := tree.cycle(packs):
        raise Refusal("depends_on cycle: " + " -> ".join(cyc))

    for row in rows:
        _apply_row(tree, packs, row, log)

    # Delete each inline block whose every entry has been applied (by any ledger).
    owners = sorted({(row.get("pack"), row.source_parts[0]) for row in rows
                     if row.source_parts[1] == "anti_patterns"})
    for pack_key, rel in owners:
        _delete_block_if_done(tree, packs, pack_key, rel, catalog, log)
    return log


def _depends_on_added(merge_map: dict | None, rows: list[Row]) -> list[dict]:
    if not merge_map:
        return []
    homes = {(row.target[0], row.target[1]) for row in rows}
    out = []
    for cluster in merge_map.get("clusters") or []:
        if (cluster.get("home_pack"), cluster.get("cluster")) in homes:
            out.extend(cluster.get("depends_on_added") or [])
    return out


def _apply_row(tree: Tree, packs: dict[str, Pack], row: Row, log: list[str]) -> None:
    path, block, _ = row.source_parts
    home, ident = row.target
    entry = source_entry(tree, packs, row)
    target_file = anti_pattern_file(tree, home, ident)
    if entry is None:
        # The block is gone: idempotent only when this row's effects are all present.
        if not _row_effects_present(tree, packs, row):
            raise Refusal(f"{row.label}: the source is gone and the row's file or edge is missing")
        _apply_extras(tree, packs, row, log)
        return
    title = entry.get("name") or entry.get("title") or entry.get("label")
    if verbatim(title) != verbatim(row.get("source_title")):
        raise Refusal(f"{row.label}: source title '{title}' differs from source_title '{row.get('source_title')}'")
    if block == "anti_patterns":
        owner_file_id = (tree.load(packs[row.get("pack")].path / path) or {}).get("id")
        kind = OWNER_KINDS.get(Path(path).parts[0])
        if owner_urn(row) != f"{kind}:{owner_file_id}":
            raise Refusal(f"{row.label}: owner '{row.get('owner')}' is not {kind}:{owner_file_id}")

    if not row.merged:
        text = dump(file_body(row))
        current = tree.read(target_file)
        if current is None:
            tree.write(target_file, text)
            log.append(f"write {target_file.relative_to(tree.root)}")
        elif yaml.safe_load(current) != file_body(row):
            raise Refusal(f"{row.label}: {target_file.relative_to(tree.root)} exists with other content")
        if block == "anti_patterns":
            _add_node(tree, packs[home], ident, verbatim(row.get("title")), log)

    if block == "anti_patterns":
        owner_pack = packs[row.get("pack")]
        if home != row.get("pack") and home not in tree.closure(packs, row.get("pack")):
            raise Refusal(f"{row.label}: {home} is not in {row.get('pack')}'s depends_on closure")
        kind, owner_id = owner_urn(row).split(":", 1)
        _add_edge(tree, owner_pack, kind, {
            "source": owner_urn(row), "target": edge_target(row), "relation": "rejects",
            "reason": f"the {kind} {owner_id} names this anti-pattern"}, log)
    _apply_extras(tree, packs, row, log)


def _apply_extras(tree: Tree, packs: dict[str, Pack], row: Row, log: list[str]) -> None:
    """also_rejects / also_rejected_by edges, and the reason_update of a non-merged row."""
    for pack_key, kind, edge in extra_edges(row):
        if pack_key not in packs:
            raise Refusal(f"{row.label}: unknown pack '{pack_key}' for an extra edge")
        m = QUALIFIED_RE.match(edge["target"])
        if m and m.group("pack") not in tree.closure(packs, pack_key):
            raise Refusal(f"{row.label}: {edge['target']} is not in {pack_key}'s depends_on closure")
        _add_edge(tree, packs[pack_key], kind, edge, log)
    update = row.get("reason_update")
    if update:
        home, ident = row.target
        for key, pack in sorted(packs.items()):
            target = qualified_target(key, home, ident)
            for doc in tree.graph_docs(pack):
                text = tree.read(doc)
                if text is None:
                    continue
                new, n = replace_list_items(
                    text, "edges",
                    lambda e: e.get("target") == target and e.get("relation") == "rejects"
                    and _norm(e.get("reason")) == _norm(update["from"]),
                    lambda e: {**e, "reason": verbatim(update["to"])})
                if n:
                    tree.write(doc, new)
                    log.append(f"reason {pack.name}: {n} rejects edge(s) to {target} follow the new text")


def _row_effects_present(tree: Tree, packs: dict[str, Pack], row: Row) -> bool:
    home, ident = row.target
    if not anti_pattern_file(tree, home, ident).exists() and anti_pattern_file(tree, home, ident) not in tree.texts:
        return False
    if row.source_parts[1] != "anti_patterns":
        return True
    return (owner_urn(row), edge_target(row), "rejects") in tree.edges(packs[row.get("pack")])


def _add_node(tree: Tree, pack: Pack, ident: str, title: str, log: list[str]) -> None:
    if ident in tree.anti_pattern_nodes(pack):
        return
    if pack.layout == "fragment":
        doc = pack.path / "drg" / "fragment.yaml"
        node = {"id": ident, "kind": "anti_patterns", "title": title}
    else:
        doc = pack.path / "anti_pattern.graph.yaml"
        if tree.read(doc) is None:
            tree.write(doc, PERKIND_HEADER + "nodes: []\nedges: []\n")
        node = {"urn": f"anti_pattern:{ident}", "kind": "anti_pattern", "label": title}
    tree.write(doc, append_list_items(tree.read(doc), "nodes", [node]))
    log.append(f"node {pack.name}: anti_pattern:{ident}")


def _add_edge(tree: Tree, pack: Pack, owner_kind: str, edge: dict, log: list[str]) -> None:
    if (edge["source"], edge["target"], edge["relation"]) in tree.edges(pack):
        return
    if pack.layout == "fragment":
        doc = pack.path / "drg" / "fragment.yaml"
    else:
        doc = pack.path / f"{owner_kind}.graph.yaml"
        if tree.read(doc) is None:
            raise Refusal(f"{pack.name}: {doc.name} does not exist for the owner's edge")
    tree.write(doc, append_list_items(tree.read(doc), "edges", [edge]))
    log.append(f"edge {pack.name}: {edge['source']} -rejects-> {edge['target']}")


def _delete_block_if_done(tree: Tree, packs: dict[str, Pack], pack_key: str, rel: str,
                          catalog: list[Row], log: list[str]) -> None:
    pack = packs[pack_key]
    path = pack.path / rel
    doc = tree.load(path) or {}
    entries = doc.get("anti_patterns")
    if entries is None:
        return
    by_index = {}
    for row in catalog:
        p, block, index = row.source_parts
        if row.get("pack") == pack_key and p == rel and block == "anti_patterns":
            by_index[index] = row
    for index in range(len(entries)):
        row = by_index.get(index)
        if row is None or not _row_effects_present(tree, packs, row):
            log.append(f"keep {path.relative_to(tree.root)} anti_patterns: index {index} not applied yet")
            return
    tree.write(path, remove_top_level_key(tree.read(path), "anti_patterns"))
    log.append(f"delete {path.relative_to(tree.root)} anti_patterns ({len(entries)} entries)")


def commit(tree: Tree) -> None:
    for path, text in sorted(tree.texts.items()):
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists() or path.read_text(encoding="utf-8") != text:
            path.write_text(text, encoding="utf-8")


# --------------------------------------------------------------------------- check


def check(root: Path, rows: list[Row], merge_map: dict | None) -> list[str]:
    tree = Tree(root)
    packs = tree.packs()
    faults = [f for row in rows for f in validate_row(row)]

    non_merged: dict[tuple[str, str], Row] = {}
    for row in rows:
        try:
            home, ident = row.target
        except Refusal as exc:
            faults.append(str(exc))
            continue
        if not row.merged:
            if (home, ident) in non_merged:
                faults.append(f"{row.label}: second non-merged row for {home}::anti_pattern:{ident}")
            non_merged[(home, ident)] = row

    for row in rows:
        try:
            home, ident = row.target
            path, block, _ = row.source_parts
        except Refusal as exc:
            faults.append(str(exc))
            continue
        if row.merged and (home, ident) not in non_merged:
            faults.append(f"{row.label}: merged_into {row.get('merged_into')} resolves to no non-merged row")
        if home not in packs:
            faults.append(f"{row.label}: home pack '{home}' does not exist")
            continue
        if not row.merged:
            target = anti_pattern_file(tree, home, ident)
            if not target.exists():
                faults.append(f"{row.label}: {target.relative_to(root)} is missing")
            elif yaml.safe_load(target.read_text(encoding="utf-8")) != file_body(row):
                faults.append(f"{row.label}: {target.relative_to(root)} differs from the row")
            if ident not in tree.anti_pattern_nodes(packs[home]):
                faults.append(f"{row.label}: no anti_pattern node for {ident} in {home}")
        if block == "anti_patterns" and row.get("pack") in packs:
            if (owner_urn(row), edge_target(row), "rejects") not in tree.edges(packs[row.get("pack")]):
                faults.append(f"{row.label}: no rejects edge {owner_urn(row)} -> {edge_target(row)}")
            if home != row.get("pack") and home not in tree.closure(packs, row.get("pack")):
                faults.append(f"{row.label}: {home} is not in {row.get('pack')}'s depends_on closure")

    for key, pack in sorted(packs.items()):
        for file in sorted((pack.path / "anti_patterns").glob("*.anti-pattern.yaml")):
            ident = file.name[: -len(".anti-pattern.yaml")]
            if (key, ident) not in non_merged:
                faults.append(f"{file.relative_to(root)}: no non-merged ledger row")
        for ident in sorted(tree.anti_pattern_nodes(pack)):
            if not anti_pattern_file(tree, key, ident).exists():
                faults.append(f"{key}: anti_pattern node {ident} has no file")
        for sub in ("styleguides", "procedures"):
            for file in sorted((pack.path / sub).rglob("*.yaml")):
                data = yaml.safe_load(file.read_text(encoding="utf-8")) or {}
                if isinstance(data, dict) and "anti_patterns" in data:
                    faults.append(f"{file.relative_to(root)}: still carries anti_patterns")

    for row in rows:
        try:
            edges = extra_edges(row)
        except (Refusal, KeyError, AttributeError):
            continue
        for pack_key, _, edge in edges:
            if pack_key not in packs:
                faults.append(f"{row.label}: unknown pack '{pack_key}' for an extra edge")
            elif (edge["source"], edge["target"], "rejects") not in tree.edges(packs[pack_key]):
                faults.append(f"{row.label}: no rejects edge {edge['source']} -> {edge['target']} in {pack_key}")
        update = row.get("reason_update")
        if update and not row.merged:
            home, ident = row.target
            for key, pack in sorted(packs.items()):
                target = qualified_target(key, home, ident)
                for doc in tree.graph_docs(pack):
                    for edge in (tree.load(doc) or {}).get("edges") or []:
                        if (edge.get("target") == target and edge.get("relation") == "rejects"
                                and _norm(edge.get("reason")) == _norm(update.get("from"))):
                            faults.append(f"{row.label}: {key} edge {edge.get('source')} -> {target} keeps the old reason")

    # Every cross-pack anti-pattern edge, ledger-made or hand-written, stays inside the owner's closure.
    for key, pack in sorted(packs.items()):
        for _, target, relation in sorted(tree.edges(pack), key=str):
            m = QUALIFIED_RE.match(str(target or ""))
            if m and m.group("pack") != key and m.group("pack") not in tree.closure(packs, key):
                faults.append(f"{key}: {relation} edge to {target} is outside {key}'s depends_on closure")

    if cyc := tree.cycle(packs):
        faults.append("depends_on cycle: " + " -> ".join(cyc))
    faults.extend(check_map(rows, merge_map))
    return faults


def check_map(rows: list[Row], merge_map: dict | None) -> list[str]:
    inline = [r for r in rows if SOURCE_RE.match(str(r.get("source") or ""))
              and SOURCE_RE.match(str(r.get("source"))).group("block") == "anti_patterns"]
    if not inline:
        return []
    if merge_map is None:
        return ["merge-map.yaml is missing, but ledgers hold inline-entry rows"]
    faults = []
    members: dict[tuple[str, str], dict] = {}
    for cluster in merge_map.get("clusters") or []:
        if cluster.get("operator_question"):
            faults.append(f"merge map cluster {cluster.get('cluster')}: open operator_question")
        for member in cluster.get("members") or []:
            key = (member.get("pack"), member.get("source"))
            if key in members:
                faults.append(f"merge map: {key[0]}/{key[1]} is in two clusters")
            members[key] = cluster
    row_keys = set()
    for row in inline:
        key = (row.get("pack"), row.get("source"))
        row_keys.add(key)
        cluster = members.get(key)
        if cluster is None:
            faults.append(f"{row.label}: not in the merge map")
            continue
        home, ident = row.target
        if (home, ident) != (cluster.get("home_pack"), cluster.get("cluster")):
            faults.append(f"{row.label}: row targets {home}::anti_pattern:{ident}, the map "
                          f"{cluster.get('home_pack')}::anti_pattern:{cluster.get('cluster')}")
    for key in sorted(set(members) - row_keys):
        faults.append(f"merge map: {key[0]}/{key[1]} has no ledger row")
    return faults


# --------------------------------------------------------------------------- CLI


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="repository (or scratch) root holding packs/")
    parser.add_argument("--ledger", type=Path, action="append", help="ledger to apply (default: every ledger-*.yaml)")
    parser.add_argument("--merge-map", type=Path, default=HERE / "merge-map.yaml")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="prove the invariants; exit 1 with one line per fault")
    mode.add_argument("--dry-run", action="store_true", help="print the planned writes; write nothing")
    args = parser.parse_args(argv)

    root = args.root.resolve()
    ledgers = [p.resolve() for p in (args.ledger or default_ledgers())]
    merge_map = load_map(args.merge_map)
    rows = load_rows(ledgers)
    if args.check:
        faults = check(root, rows, merge_map)
        for fault in faults:
            print(fault)
        return 1 if faults else 0
    # Every ledger beside the given ones decides whether an inline block is fully applied.
    siblings = {p for d in {l.parent for l in ledgers} for p in d.glob("ledger-*.yaml")}
    catalog = load_rows(sorted(siblings | set(ledgers)))
    tree = Tree(root)
    try:
        log = plan_apply(tree, rows, catalog, merge_map)
    except Refusal as exc:
        print(f"refused, nothing written:\n{exc}", file=sys.stderr)
        return 1
    for line in log:
        print(line)
    if not args.dry_run:
        commit(tree)
    return 0


if __name__ == "__main__":
    sys.exit(main())
