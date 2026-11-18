#!/usr/bin/env python3
"""Render the ledger's foundation and internal rows as glossary terms (mission tool, not shipped).

Usage: render_terms.py [--write | --flag]

Paths are fixed (build_ledger.REPO and CORE_CONTEXT, and this mission's directory); only the mode is read from
the command line.

Definitions come from the source table; a foundation definition is cleaned of Markdown links and of
parentheticals that cite core's code, tests, ADRs or issues. research/rewrites.yaml overrides any
field of a term by id (name, definition, status, aliases, see_also) and supplies hand-authored terms
(rows whose source has no table). --flag lists foundation definitions that still lean on core
internals; --write appends the terms to the two contexts (existing terms are never rewritten, except
for adding aliases from `alias` rows).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).parent))
from build_ledger import CORE_CONTEXT, REPO, STATUS, parse, slug  # noqa: E402

MISSION = Path(__file__).resolve().parents[1]

CONTEXTS = {
    "foundation": ("packs/foundation/glossaries/spec-kitty-core.glossary.yaml", "spec-kitty-core"),
    "internal": ("packs/internal/glossaries/spk-internal-glossary.glossary.yaml", "spk-internal-glossary"),
}
INTERNAL_HINT = re.compile(
    r"src/|tests/|\.py\b|ADR|#\d{3,}|\b[a-z]+_[a-z_]+\(|`[A-Z][a-z]+[A-Z]\w*`|this repository|this codebase|in this repo",
)


def unlink(text: str) -> str:
    return re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)


CORE_MARKER = re.compile(r"src/|tests/|\.py|ADR|#\d{3,}")


def drop_core_parentheticals(text: str) -> str:
    """Remove each top-level parenthetical (with the whitespace before it) that cites core code, tests, ADRs or issues."""
    out, depth, start = [], 0, 0
    for i, ch in enumerate(text):
        if ch == "(":
            if depth == 0:
                out.append(text[start:i])
                start = i
            depth += 1
        elif ch == ")" and depth:
            depth -= 1
            if depth == 0:
                group = text[start:i + 1]
                if CORE_MARKER.search(group):
                    out[-1] = out[-1].rstrip()
                else:
                    out.append(group)
                start = i + 1
    out.append(text[start:])
    return "".join(out)


def clean(text: str) -> str:
    text = unlink(text).replace("\\|", "|").replace("<br>", " ").replace("**", "")
    text = drop_core_parentheticals(text)
    return re.sub(r"\s{2,}", " ", text).strip()


OPERATOR = [  # #139: the accountable human is "the operator"
    (re.compile(r"Human[- ]in[- ]Charge \(HiC\)"), "operator"),
    (re.compile(r"Human[- ]in[- ](?:Charge|Command)|[Hh]uman-in-command"), "operator"),  # never the profile id human-in-charge
    (re.compile(r"\bHiC\b"), "operator"),
]


def operatorize(text: str) -> str:
    for pattern, word in OPERATOR:
        text = pattern.sub(word, text)
    text = re.sub(r"(^|[.!?]\s+)operator", lambda m: m.group(1) + "Operator", text)  # sentence start
    return re.sub(r"\b([Aa]) operator", r"\1n operator", text)


def drop_suffix(text: str, suffix: str) -> str:
    """`text` without a trailing `suffix` and the whitespace before it."""
    return text[: -len(suffix)].rstrip() if text.endswith(suffix) else text


def anchors(text: str) -> list[str]:
    return [m.split("#")[-1] for m in re.findall(r"\]\(([^)#]*#[^)]+)\)", text)]


def main() -> None:
    src, mission, repo = CORE_CONTEXT, MISSION, REPO
    mode = "--write" if "--write" in sys.argv[1:] else "--flag"
    ledger = yaml.safe_load((mission / "research/ledger.yaml").read_text(encoding="utf-8"))["rows"]
    rewrites = yaml.safe_load((mission / "research/rewrites.yaml").read_text(encoding="utf-8")) or {}
    source = {(t["page"], t["heading"]): t for t in parse(src)}
    docs = {c: yaml.safe_load((repo / p).read_text(encoding="utf-8")) for c, (p, _) in CONTEXTS.items()}
    ids = {c: {t["id"] for t in d["terms"]} for c, d in docs.items()}
    # anchor (heading slug as GitHub renders it, and our slug) -> (context, id)
    where: dict[str, tuple[str, str]] = {}
    for row in ledger:
        ctx = row.get("context") or row["verdict"]
        if ctx in CONTEXTS:
            gh = re.sub(r"[^a-z0-9 _-]", "", row["heading"].lower()).replace(" ", "-")
            where[gh] = where[slug(row["heading"])] = (ctx, row["id"])
    new: dict[str, list[dict]] = {"foundation": [], "internal": []}
    alias_rows = {}
    for row in ledger:
        if row["verdict"] == "alias":
            alias_rows.setdefault(row["id"], []).append(drop_suffix(row["heading"], "(Alias)"))
    for row in ledger:
        verdict, tid = row["verdict"], row["id"]
        if verdict not in CONTEXTS:
            continue
        src_term = source.get((row["page"], row["heading"]))
        term: dict = {"id": tid, "name": row.get("name") or drop_suffix(drop_suffix(row["heading"], "(Candidate)"), "(Alias)").replace("`", "")}
        if src_term:
            raw = src_term["rows"]["Definition"]
            term["definition"] = clean(raw) if verdict == "foundation" else unlink(raw).replace("\\|", "|")
            term["status"] = STATUS.get(row["source_status"], "active")
            related = " ".join(src_term["rows"].get(k, "") for k in ("Related terms", "Definition"))
            see = []
            for anchor in anchors(related):
                hit = where.get(anchor)
                if hit and hit[0] == verdict and hit[1] != tid:
                    ref = f"term:{CONTEXTS[verdict][1]}/{hit[1]}"
                    if ref not in see:
                        see.append(ref)
            if see:
                term["see_also"] = see
        if "definition" in term:
            term["definition"] = operatorize(term["definition"])
        term.update(rewrites.get(tid) or {})
        if tid in alias_rows:
            term["aliases"] = [*term.get("aliases", []), *alias_rows.pop(tid)]
        missing = [k for k in ("definition", "status") if k not in term]
        if missing:
            sys.exit(f"{tid}: no {missing} (add it to research/rewrites.yaml)")
        new[verdict].append(term)
    if mode == "--flag":
        for term in new["foundation"]:
            if INTERNAL_HINT.search(term["definition"]) and term["id"] not in rewrites:
                print(f"- {term['id']}: {term['definition'][:400]}\n")
        print(f"foundation +{len(new['foundation'])}, internal +{len(new['internal'])}", file=sys.stderr)
        return
    class Dumper(yaml.SafeDumper):  # the contexts indent their sequences
        def increase_indent(self, flow=False, indentless=False):
            return super().increase_indent(flow, False)

    for ctx, terms in new.items():
        known = ids[ctx] | {t["id"] for t in terms}
        if len(known) != len(ids[ctx]) + len(terms):
            sys.exit(f"{ctx}: a new id collides")
        for term in terms:  # keep only see_also that resolves in the context
            if "see_also" in term:
                term["see_also"] = [s for s in term["see_also"] if s.split("/")[-1] in known]
                if not term["see_also"]:
                    del term["see_also"]
        path = repo / CONTEXTS[ctx][0]
        text = yaml.dump({"terms": terms}, Dumper=Dumper, sort_keys=False, width=120, allow_unicode=True)
        current = path.read_text(encoding="utf-8")
        path.write_text(current.rstrip("\n") + "\n" + text.split("\n", 1)[1], encoding="utf-8")
        print(f"{ctx}: +{len(terms)} terms", file=sys.stderr)
    for tid, aliases in alias_rows.items():
        print(f"alias of an existing term, add by hand: {aliases} -> {tid}", file=sys.stderr)

if __name__ == "__main__":
    main()
