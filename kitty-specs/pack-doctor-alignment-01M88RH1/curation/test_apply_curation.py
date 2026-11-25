"""Tests for apply_curation.py: a two-pack fixture, one graph layout each."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import apply_curation as ac  # noqa: E402

ALPHA_GUIDE = """\
# A styleguide with an inline block between two keys.
id: alpha-guide
title: Alpha guide
anti_patterns:
  - name: Float Money
    description: "Holding money in a float, so totals drift."
    bad_example: |
      total: float
    good_example: |
      total: Money

  - name: Silent Retry
    description: "Retrying without a log line."
    bad_example: retry()

  - name: Float money again
    description: "Holding money in a float, so totals drift."
    bad_example: price = 0.1

# A comment that belongs to the next key.
principles:
  - keep it boring
"""

BETA_PROC = """\
id: beta-proc
title: Beta procedure
steps:
  - do the thing
anti_patterns:
- title: Floating totals
  content: |
    Money held in floating point drifts.
- title: Skipping the claim
  content: |
    Starting before the issue is claimed.
"""

FRAGMENT = """\
# The fragment.
nodes:
- id: alpha-guide
  kind: styleguides
  title: Alpha guide
- id: orphan
  kind: anti_patterns
  title: Orphan Practice
edges:
- source: tactic:keep-it-small
  target: anti_pattern:orphan
  relation: rejects
  reason: An orphan practice that keeps nothing small.
"""

PROC_GRAPH = """\
schema_version: '1.0'
generated_at: STATIC
generated_by: drg-migration-v1
nodes:
- urn: procedure:beta-proc
  kind: procedure
  label: Beta procedure
edges: []
"""


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def row(**kw) -> dict:
    base = {"severity": "smell", "severity_grounding": '"drift" -> a style cost',
            "bad_example_source": "bad_example", "operator_question": None}
    base.update(kw)
    return base


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    packs = tmp_path / "packs"
    write(packs / "alpha/pack.yaml", "name: alpha\npack_id: A1\ndepends_on: []\n")
    write(packs / "alpha/drg/fragment.yaml", FRAGMENT)
    write(packs / "alpha/styleguides/alpha-guide.styleguide.yaml", ALPHA_GUIDE)
    write(packs / "beta/pack.yaml", "name: beta\npack_id: B1\ndepends_on:\n  - pack_id: A1  # alpha\n    range: \">=1\"\n")
    write(packs / "beta/procedure.graph.yaml", PROC_GRAPH)
    write(packs / "beta/procedures/beta-proc.procedure.yaml", BETA_PROC)
    return tmp_path


def ledgers(root: Path, overrides: dict | None = None) -> tuple[list[Path], Path]:
    cur = root / "curation"
    rows_00 = [row(source="drg/fragment.yaml#/nodes/1", source_title="Orphan Practice", pack="alpha",
                   owner=None, id="orphan", title="Orphan Practice",
                   description="An orphan practice that keeps nothing small.", bad_example="a 40-step tactic",
                   bad_example_source="tactic keep-it-small step 1")]
    guide = "styleguides/alpha-guide.styleguide.yaml"
    proc = "procedures/beta-proc.procedure.yaml"
    rows_a = [
        row(source=f"{guide}#/anti_patterns/0", source_title="Float Money", pack="alpha",
            owner="styleguide:alpha-guide", id="float-money", title="Float Money",
            description="Holding money in a float, so totals drift.", bad_example="total: float\n",
            good_example="total: Money\n", severity="breaking"),
        row(source=f"{guide}#/anti_patterns/1", source_title="Silent Retry", pack="alpha",
            owner="styleguide:alpha-guide", id="silent-retry", title="Silent Retry",
            description="Retrying without a log line.", bad_example="retry()"),
        row(source=f"{guide}#/anti_patterns/2", source_title="Float money again", pack="alpha",
            owner="styleguide:alpha-guide", id="float-money", merged_into="alpha::anti_pattern:float-money",
            merge_reason="both: money in a float drifts"),
        row(source=f"{proc}#/anti_patterns/0", source_title="Floating totals", pack="beta",
            owner="procedure:beta-proc", id="float-money", merged_into="alpha::anti_pattern:float-money",
            merge_reason="both: money in a float drifts", bad_example_source="authored, grounded in 'drifts'"),
    ]
    rows_b = [
        row(source=f"{proc}#/anti_patterns/1", source_title="Skipping the claim", pack="beta",
            owner="procedure:beta-proc", id="skipping-the-claim", title="Skipping the claim",
            description="Starting before the issue is claimed.", bad_example="open a branch on an unclaimed issue",
            bad_example_source="authored, grounded in 'before the issue is claimed'"),
    ]
    for name, rows in (overrides or {}).items():
        {"00": rows_00, "a": rows_a, "b": rows_b}[name][:] = rows
    paths = []
    for name, rows in (("ledger-00-nodes.yaml", rows_00), ("ledger-a-alpha.yaml", rows_a),
                       ("ledger-b-beta.yaml", rows_b)):
        write(cur / name, yaml.safe_dump({"batch": name, "entries": rows}, sort_keys=False))
        paths.append(cur / name)
    merge_map = {"clusters": [
        {"cluster": "float-money", "home_pack": "alpha", "merge_reason": "money in a float drifts",
         "members": [{"pack": "alpha", "source": f"{guide}#/anti_patterns/0"},
                     {"pack": "alpha", "source": f"{guide}#/anti_patterns/2"},
                     {"pack": "beta", "source": f"{proc}#/anti_patterns/0"}]},
        {"cluster": "silent-retry", "home_pack": "alpha",
         "members": [{"pack": "alpha", "source": f"{guide}#/anti_patterns/1"}]},
        {"cluster": "skipping-the-claim", "home_pack": "beta",
         "members": [{"pack": "beta", "source": f"{proc}#/anti_patterns/1"}]},
    ]}
    write(cur / "merge-map.yaml", yaml.safe_dump(merge_map, sort_keys=False))
    return paths, cur / "merge-map.yaml"


def run(root: Path, paths: list[Path], mm: Path, *extra: str) -> int:
    args = ["--root", str(root), "--merge-map", str(mm)] + [a for p in paths for a in ("--ledger", str(p))]
    return ac.main(args + list(extra))


def snapshot(root: Path) -> dict:
    return {p: p.read_text() for p in sorted((root / "packs").rglob("*")) if p.is_file()}


# --------------------------------------------------------------------------- apply


def test_apply_then_check_is_clean_and_second_apply_writes_nothing(repo):
    paths, mm = ledgers(repo)
    assert run(repo, paths, mm) == 0
    first = snapshot(repo)
    assert run(repo, paths, mm, "--check") == 0
    assert run(repo, paths, mm) == 0
    assert snapshot(repo) == first


def test_files_nodes_and_edges_in_both_layouts(repo):
    paths, mm = ledgers(repo)
    run(repo, paths, mm)
    packs = repo / "packs"
    money = yaml.safe_load((packs / "alpha/anti_patterns/float-money.anti-pattern.yaml").read_text())
    assert list(money) == ["schema_version", "id", "title", "description", "severity", "bad_example", "good_example"]
    assert money["bad_example"] == "total: float" and money["severity"] == "breaking"
    assert (packs / "alpha/anti_patterns/orphan.anti-pattern.yaml").exists()
    fragment = yaml.safe_load((packs / "alpha/drg/fragment.yaml").read_text())
    assert {"id": "float-money", "kind": "anti_patterns", "title": "Float Money"} in fragment["nodes"]
    targets = {(e["source"], e["target"]) for e in fragment["edges"] if e["relation"] == "rejects"}
    assert ("styleguide:alpha-guide", "anti_pattern:float-money") in targets
    assert ("styleguide:alpha-guide", "anti_pattern:silent-retry") in targets
    ap_graph = yaml.safe_load((packs / "beta/anti_pattern.graph.yaml").read_text())
    assert ap_graph["nodes"] == [{"urn": "anti_pattern:skipping-the-claim", "kind": "anti_pattern",
                                  "label": "Skipping the claim"}]
    proc_edges = yaml.safe_load((packs / "beta/procedure.graph.yaml").read_text())["edges"]
    assert {"source": "procedure:beta-proc", "target": "alpha::anti_pattern:float-money", "relation": "rejects",
            "reason": "the procedure beta-proc names this anti-pattern"} in proc_edges
    assert not (packs / "beta/anti_patterns/float-money.anti-pattern.yaml").exists()


def test_block_deletion_keeps_neighbouring_comments_and_keys(repo):
    paths, mm = ledgers(repo)
    run(repo, paths, mm)
    text = (repo / "packs/alpha/styleguides/alpha-guide.styleguide.yaml").read_text()
    assert "anti_patterns" not in text
    assert "# A styleguide with an inline block between two keys." in text
    assert "# A comment that belongs to the next key.\nprinciples:" in text
    assert yaml.safe_load(text) == {"id": "alpha-guide", "title": "Alpha guide", "principles": ["keep it boring"]}


def test_a_block_stays_until_every_entry_is_applied(repo):
    paths, mm = ledgers(repo)
    assert run(repo, paths[:2], mm) == 0  # ledger 00 and A only
    proc = yaml.safe_load((repo / "packs/beta/procedures/beta-proc.procedure.yaml").read_text())
    assert len(proc["anti_patterns"]) == 2
    assert run(repo, paths[2:], mm) == 0  # ledger B alone completes the block
    proc = yaml.safe_load((repo / "packs/beta/procedures/beta-proc.procedure.yaml").read_text())
    assert "anti_patterns" not in proc
    assert run(repo, paths, mm, "--check") == 0


def test_dry_run_writes_nothing(repo, capsys):
    paths, mm = ledgers(repo)
    before = snapshot(repo)
    assert run(repo, paths, mm, "--dry-run") == 0
    assert snapshot(repo) == before
    assert "write packs/alpha/anti_patterns/float-money.anti-pattern.yaml" in capsys.readouterr().out


def test_depends_on_added_from_the_merge_map(repo):
    paths, mm = ledgers(repo)
    write(repo / "packs/gamma/pack.yaml", "name: gamma\npack_id: G1\ndepends_on: []\n")
    write(repo / "packs/gamma/drg/fragment.yaml", "nodes: []\nedges: []\n")
    write(repo / "packs/gamma/styleguides/g.styleguide.yaml",
          "id: g\nanti_patterns:\n  - name: Silent Retry\n    description: d\n    bad_example: b\n")
    extra = row(source="styleguides/g.styleguide.yaml#/anti_patterns/0", source_title="Silent Retry",
                pack="gamma", owner="styleguide:g", id="silent-retry",
                merged_into="alpha::anti_pattern:silent-retry", merge_reason="same claim")
    data = yaml.safe_load(paths[1].read_text())
    data["entries"].append(extra)
    write(paths[1], yaml.safe_dump(data, sort_keys=False))
    mmd = yaml.safe_load(mm.read_text())
    mmd["clusters"][1]["members"].append({"pack": "gamma", "source": extra["source"]})
    mmd["clusters"][1]["depends_on_added"] = [{"pack": "gamma", "depends_on": "alpha", "range": ">=1"}]
    write(mm, yaml.safe_dump(mmd, sort_keys=False))
    assert run(repo, paths, mm) == 0
    gamma = yaml.safe_load((repo / "packs/gamma/pack.yaml").read_text())
    assert gamma["depends_on"] == [{"pack_id": "A1", "range": ">=1"}]
    assert run(repo, paths, mm, "--check") == 0


# --------------------------------------------------------------------------- refusals


def refused(repo, paths, mm, capsys, needle: str) -> None:
    before = snapshot(repo)
    assert run(repo, paths, mm) == 1
    assert needle in capsys.readouterr().err
    assert snapshot(repo) == before


def _edit_row(path: Path, index: int, **changes) -> None:
    data = yaml.safe_load(path.read_text())
    data["entries"][index].update(changes)
    write(path, yaml.safe_dump(data, sort_keys=False))


def test_refuses_an_open_operator_question(repo, capsys):
    paths, mm = ledgers(repo)
    _edit_row(paths[1], 1, operator_question="smell or severe?")
    refused(repo, paths, mm, capsys, "open operator_question")


def test_refuses_an_id_clash(repo, capsys):
    paths, mm = ledgers(repo)
    _edit_row(paths[1], 1, id="float-money")
    refused(repo, paths, mm, capsys, "id clash")


@pytest.mark.parametrize("bad", ["Float_Money", "a" * 65, "-lead"])
def test_refuses_a_bad_id(repo, capsys, bad):
    paths, mm = ledgers(repo)
    _edit_row(paths[1], 1, id=bad)
    refused(repo, paths, mm, capsys, "kebab-case")


def test_refuses_a_source_that_does_not_resolve(repo, capsys):
    paths, mm = ledgers(repo)
    _edit_row(paths[1], 1, source="styleguides/alpha-guide.styleguide.yaml#/anti_patterns/9")
    refused(repo, paths, mm, capsys, "no index 9")


def test_refuses_title_drift(repo, capsys):
    paths, mm = ledgers(repo)
    _edit_row(paths[1], 1, source_title="Loud Retry")
    refused(repo, paths, mm, capsys, "differs from source_title")


def test_refuses_a_wrong_owner(repo, capsys):
    paths, mm = ledgers(repo)
    _edit_row(paths[1], 1, owner="procedure:alpha-guide")
    refused(repo, paths, mm, capsys, "is not styleguide:alpha-guide")


def test_refuses_an_unresolved_merge(repo, capsys):
    paths, mm = ledgers(repo)
    _edit_row(paths[1], 2, merged_into="alpha::anti_pattern:nowhere")
    refused(repo, paths, mm, capsys, "resolves to no row or file")


def test_refuses_a_cross_pack_target_outside_the_closure(repo, capsys):
    paths, mm = ledgers(repo)
    write(repo / "packs/beta/pack.yaml", "name: beta\npack_id: B1\ndepends_on: []\n")
    refused(repo, paths, mm, capsys, "not in beta's depends_on closure")


def test_refuses_a_depends_on_cycle(repo, capsys):
    paths, mm = ledgers(repo)
    write(repo / "packs/alpha/pack.yaml", "name: alpha\npack_id: A1\ndepends_on:\n  - pack_id: B1\n    range: '>=1'\n")
    refused(repo, paths, mm, capsys, "depends_on cycle")


def test_refuses_a_merge_without_its_reason(repo, capsys):
    paths, mm = ledgers(repo)
    _edit_row(paths[1], 2, merge_reason="")
    refused(repo, paths, mm, capsys, "merge_reason is empty")


def test_refuses_a_default_grounding(repo, capsys):
    paths, mm = ledgers(repo)
    _edit_row(paths[1], 1, severity_grounding="default")
    refused(repo, paths, mm, capsys, "says 'default'")


# --------------------------------------------------------------------------- check faults


def check_faults(repo, paths, mm, capsys) -> str:
    assert run(repo, paths, mm, "--check") == 1
    return capsys.readouterr().out


def test_check_reports_remaining_inline_blocks_before_apply(repo, capsys):
    paths, mm = ledgers(repo)
    out = check_faults(repo, paths, mm, capsys)
    assert "still carries anti_patterns" in out and "is missing" in out


def test_check_reports_a_file_that_differs(repo, capsys):
    paths, mm = ledgers(repo)
    run(repo, paths, mm)
    f = repo / "packs/alpha/anti_patterns/silent-retry.anti-pattern.yaml"
    f.write_text(f.read_text().replace("severity: smell", "severity: severe"))
    assert "differs from the row" in check_faults(repo, paths, mm, capsys)


def test_check_reports_a_file_without_a_row_and_a_node_without_a_file(repo, capsys):
    paths, mm = ledgers(repo)
    run(repo, paths, mm)
    write(repo / "packs/alpha/anti_patterns/stray.anti-pattern.yaml", "id: stray\n")
    (repo / "packs/alpha/anti_patterns/silent-retry.anti-pattern.yaml").unlink()
    out = check_faults(repo, paths, mm, capsys)
    assert "stray.anti-pattern.yaml: no non-merged ledger row" in out
    assert "anti_pattern node silent-retry has no file" in out


def test_check_reports_a_missing_edge_and_node(repo, capsys):
    paths, mm = ledgers(repo)
    run(repo, paths, mm)
    graph = repo / "packs/beta/procedure.graph.yaml"
    data = yaml.safe_load(graph.read_text())
    data["edges"] = []
    graph.write_text(yaml.safe_dump(data, sort_keys=False))
    (repo / "packs/beta/anti_pattern.graph.yaml").write_text(ac.PERKIND_HEADER + "nodes: []\nedges: []\n")
    out = check_faults(repo, paths, mm, capsys)
    assert "no rejects edge procedure:beta-proc -> alpha::anti_pattern:float-money" in out
    assert "no anti_pattern node for skipping-the-claim in beta" in out


def test_check_reports_row_faults(repo, capsys):
    paths, mm = ledgers(repo)
    run(repo, paths, mm)
    _edit_row(paths[2], 0, bad_example_source="", operator_question="which?")
    out = check_faults(repo, paths, mm, capsys)
    assert "bad_example_source is empty" in out and "open operator_question" in out


def test_check_reports_merge_map_faults(repo, capsys):
    paths, mm = ledgers(repo)
    run(repo, paths, mm)
    mmd = yaml.safe_load(mm.read_text())
    mmd["clusters"][2]["home_pack"] = "alpha"
    mmd["clusters"][1]["members"].append({"pack": "alpha", "source": "x.yaml#/anti_patterns/0"})
    write(mm, yaml.safe_dump(mmd, sort_keys=False))
    out = check_faults(repo, paths, mm, capsys)
    assert "the map alpha::anti_pattern:skipping-the-claim" in out
    assert "x.yaml#/anti_patterns/0 has no ledger row" in out
    mm.unlink()
    assert "merge-map.yaml is missing" in check_faults(repo, paths, mm, capsys)


def test_check_reports_an_unresolved_merge(repo, capsys):
    paths, mm = ledgers(repo)
    run(repo, paths, mm)
    _edit_row(paths[1], 2, merged_into="alpha::anti_pattern:nowhere")
    assert "resolves to no non-merged row" in check_faults(repo, paths, mm, capsys)


# --------------------------------------------------------------------------- extra edges and reason updates


def _with_extras(paths):
    _edit_row(paths[1], 1, also_rejected_by=[
        {"owner": "tactic:keep-it-small", "pack": "alpha", "reason": "Keeping retries visible keeps them small."},
        {"owner": "procedure:beta-proc", "pack": "beta", "reason": "A silent retry hides the claim's failure."}])
    _edit_row(paths[2], 0, also_rejects=["alpha::anti_pattern:silent-retry"])
    _edit_row(paths[0], 0, description="An orphan practice that keeps nothing small, enhanced.",
              description_source="authored by merge",
              reason_update={"from": "An orphan practice that keeps nothing small.",
                             "to": "An orphan practice that keeps nothing small, enhanced."})


def test_extra_edges_and_reason_update_apply_idempotently(repo):
    paths, mm = ledgers(repo)
    _with_extras(paths)
    assert run(repo, paths, mm) == 0
    fragment = yaml.safe_load((repo / "packs/alpha/drg/fragment.yaml").read_text())
    assert {"source": "tactic:keep-it-small", "target": "anti_pattern:silent-retry", "relation": "rejects",
            "reason": "Keeping retries visible keeps them small."} in fragment["edges"]
    orphan_edge = next(e for e in fragment["edges"] if e["target"] == "anti_pattern:orphan")
    assert orphan_edge["reason"] == "An orphan practice that keeps nothing small, enhanced."
    proc = yaml.safe_load((repo / "packs/beta/procedure.graph.yaml").read_text())["edges"]
    targets = {(e["source"], e["target"], e["reason"]) for e in proc}
    assert ("procedure:beta-proc", "alpha::anti_pattern:silent-retry", "A silent retry hides the claim's failure.") in targets
    assert ("procedure:beta-proc", "alpha::anti_pattern:silent-retry", "the procedure beta-proc names this anti-pattern") not in targets
    first = snapshot(repo)
    assert run(repo, paths, mm, "--check") == 0
    assert run(repo, paths, mm) == 0
    assert snapshot(repo) == first


def test_refuses_an_extra_edge_outside_the_closure(repo, capsys):
    paths, mm = ledgers(repo)
    _edit_row(paths[2], 0, also_rejected_by=[{"owner": "tactic:keep-it-small", "pack": "alpha", "reason": "r"}])
    refused(repo, paths, mm, capsys, "beta::anti_pattern:skipping-the-claim is not in alpha's depends_on closure")


def test_refuses_a_malformed_extra(repo, capsys):
    paths, mm = ledgers(repo)
    _edit_row(paths[1], 1, also_rejects=["silent-retry"])
    refused(repo, paths, mm, capsys, "must be <pack>::anti_pattern:<id>")


def test_check_reports_a_missing_extra_edge_and_a_stale_reason(repo, capsys):
    paths, mm = ledgers(repo)
    _with_extras(paths)
    run(repo, paths, mm)
    frag = repo / "packs/alpha/drg/fragment.yaml"
    data = yaml.safe_load(frag.read_text())
    data["edges"] = [e for e in data["edges"] if e["source"] != "tactic:keep-it-small" or e["target"] != "anti_pattern:silent-retry"]
    for e in data["edges"]:
        if e["target"] == "anti_pattern:orphan":
            e["reason"] = "An orphan practice that keeps nothing small."
    frag.write_text(yaml.safe_dump(data, sort_keys=False))
    out = check_faults(repo, paths, mm, capsys)
    assert "no rejects edge tactic:keep-it-small -> anti_pattern:silent-retry in alpha" in out
    assert "keeps the old reason" in out


def test_replace_list_items_rewrites_only_the_matching_item():
    text = "# head\nedges:\n- source: a\n  reason: old\n# between\n- source: b\n  reason: old\nnodes: []\n"
    out, n = ac.replace_list_items(text, "edges", lambda e: e["source"] == "b", lambda e: {**e, "reason": "new"})
    assert n == 1 and "# head" in out and "# between" in out
    assert yaml.safe_load(out)["edges"] == [{"source": "a", "reason": "old"}, {"source": "b", "reason": "new"}]


# --------------------------------------------------------------------------- text helpers


def test_append_to_an_empty_flow_list_and_to_an_indented_list():
    text = "a: 1\nedges: []\nb: 2\n"
    out = ac.append_list_items(text, "edges", [{"x": 1}])
    assert yaml.safe_load(out) == {"a": 1, "edges": [{"x": 1}], "b": 2}
    text = "depends_on:\n  - pack_id: A  # alpha\n    range: '>=1'\nname: z\n"
    out = ac.append_list_items(text, "depends_on", [{"pack_id": "B", "range": ">=2"}])
    assert "# alpha" in out and "  - pack_id: B\n" in out
    assert yaml.safe_load(out)["depends_on"][1] == {"pack_id": "B", "range": ">=2"}


def test_append_creates_a_missing_key():
    out = ac.append_list_items("a: 1", "nodes", [{"id": "n"}])
    assert yaml.safe_load(out) == {"a": 1, "nodes": [{"id": "n"}]}


def test_remove_collapses_blank_lines_only_at_the_seam():
    text = "a: 1\n\n\nb: 2\n\nanti_patterns:\n- x\n\nc: 3\n"
    out = ac.remove_top_level_key(text, "anti_patterns")
    assert out == "a: 1\n\n\nb: 2\n\nc: 3\n"


def test_check_reports_a_hand_written_cross_pack_edge_outside_the_closure(repo, capsys):
    paths, mm = ledgers(repo)
    run(repo, paths, mm)
    graph = repo / "packs/alpha/drg/fragment.yaml"
    graph.write_text(ac.append_list_items(graph.read_text(), "edges", [
        {"source": "styleguide:alpha-guide", "target": "beta::anti_pattern:skipping-the-claim", "relation": "rejects"}]))
    assert "edge to beta::anti_pattern:skipping-the-claim is outside alpha's depends_on closure" in check_faults(repo, paths, mm, capsys)


def test_remove_the_last_key_of_a_document():
    out = ac.remove_top_level_key("id: x\nanti_patterns:\n- title: t\n  content: |\n    c\n", "anti_patterns")
    assert out == "id: x\n"
