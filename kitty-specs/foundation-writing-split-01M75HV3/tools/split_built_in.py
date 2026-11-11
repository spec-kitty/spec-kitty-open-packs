#!/usr/bin/env python3
"""One-off migration for #73: split packs/built-in into foundation, writing and opt-in bundles.

Reads the approved per-node map (membership.json) and:
  1. maps every file under packs/built-in to the pack that owns it (refuses on any unmapped file);
  2. `git mv`s each file to the same relative path in its new pack;
  3. splits the *.graph.yaml shards: built-in-level packs keep root <kind>.graph.yaml shards, org
     packs get drg/fragment.yaml (qa and internal: appended); every edge is homed in its source's
     pack when the target is in that pack's depends_on closure, else in the target's pack with a
     qualified source; endpoints not owned by the home pack are written <pack-name>::<urn>;
  4. drops the two out-of-closure body references the operator ruled on (annie -> 047, daisy -> C4);
  5. qualifies cross-pack agent-profile references and drops any outside the closure (this also
     drops ivan's and renata's operating procedures; their graph edges are already relocated).

Not done by this tool (done by hand in WP01, see the commit): the pack descriptors, pack.md,
README, PROVENANCE and org-charter files, the Generic Giannis display name, moving policy.yaml to
foundation, the member pack-manifest.yaml lists and their restamp, and adapting the moved
directory READMEs. A partial re-run of steps 4-5 alone needs the moves to have happened already.

Run from the repository root:  python3 <this file> [--dry-run]
"""
import json, os, re, subprocess, sys, collections
import yaml

ROOT = os.getcwd()
ONLY_BODIES = '--only-bodies' in sys.argv
MISSION = 'kitty-specs/foundation-writing-split-01M75HV3'
BI = 'packs/built-in'
DRY = '--dry-run' in sys.argv
M = json.load(open(f'{MISSION}/membership.json'))
own = {u: p for p, us in M['membership'].items() for u in us}
DEPS = {k: set(v) for k, v in M['depends_on'].items()}
DIR = {'quality-assurance': 'qa', 'spec-kitty-internal': 'internal'}  # descriptor name -> directory
BUILTIN_LEVEL = {'foundation', 'writing'}
KEEP = {'pack.yaml', 'pack.md', 'policy.yaml', 'pack-manifest.yaml', 'presets/default.yaml', 'presets/minimal.yaml'}
PLURAL = {'directive': 'directives', 'tactic': 'tactics', 'styleguide': 'styleguides', 'toolguide': 'toolguides',
          'paradigm': 'paradigms', 'procedure': 'procedures', 'agent_profile': 'agent_profiles',
          'mission_step_contract': 'mission_step_contracts', 'glossary_pack': 'glossary_packs', 'skill': 'skills',
          'anti_pattern': 'anti_patterns', 'asset': 'assets', 'template': 'templates', 'mission_type': 'mission_types',
          'action': 'actions'}

def closure(p, seen=None):
    seen = set() if seen is None else seen
    if p in seen:
        return seen
    seen.add(p)
    for q in DEPS.get(p, ()):
        closure(q, seen)
    return seen

def pdir(p):
    return 'packs/' + DIR.get(p, p)

def git(*a):
    if DRY:
        return
    subprocess.run(['git', *a], check=True)

if ONLY_BODIES:
    own = {u: p for p, us in M['membership'].items() for u in us}
# ---------------------------------------------------------------- 1. file -> owner
files = sorted(os.path.relpath(os.path.join(d, f), BI) for d, _, fs in os.walk(BI) for f in fs)
manifest = yaml.safe_load(open(f'{BI}/pack-manifest.yaml'))['constituents']
body_path = {}          # urn -> path relative to pack root
file_owner = {}
for c in manifest:
    urn = f"{c['kind']}:{c['id']}"
    body_path[urn] = c['path']
    file_owner[c['path']] = own[urn]

# graph-declared nodes whose files the manifest misses (#182 drift) and the mission bundles
graph_nodes = {}
for g in sorted(f for f in files if f.endswith('.graph.yaml')):
    for n in yaml.safe_load(open(f'{BI}/{g}'))['nodes']:
        graph_nodes[n['urn']] = n
by_stem = collections.defaultdict(list)
for f in files:
    by_stem[os.path.basename(f).split('.')[0]].append(f)
SUFFIX = {'toolguide': '.toolguide.yaml', 'procedure': '.procedure.yaml', 'tactic': '.tactic.yaml',
          'directive': '.directive.yaml', 'styleguide': '.styleguide.yaml', 'paradigm': '.paradigm.yaml',
          'agent_profile': '.agent.yaml'}
for urn in graph_nodes:
    kind, ident = urn.split(':', 1)
    if urn in body_path or kind not in SUFFIX:
        continue
    hits = [f for f in files if f.endswith('/' + ident + SUFFIX[kind])]
    if len(hits) == 1:
        body_path[urn] = hits[0]
        file_owner[hits[0]] = own[urn]

for f in files:
    if f.startswith('missions/') and f.count('/') >= 2 and not f.startswith('missions/built_in_step_contracts/'):
        mtype = f.split('/')[1]
        file_owner[f] = own[f'mission_type:{mtype}']
        if f == f'missions/{mtype}/{mtype}.mission-type.yaml':
            body_path[f'mission_type:{mtype}'] = f
    elif f.startswith('missions/built_in_step_contracts/'):
        sc = yaml.safe_load(open(f'{BI}/{f}'))
        urn = f"mission_step_contract:{sc['mission']}/{sc['action']}"
        file_owner[f] = own[urn]
        body_path[urn] = f

# sidecars: toolguide guides, asset payloads and configs, by stem of an owned file
for f in files:
    if f in file_owner:
        continue
    if f.endswith('.guide.md'):
        tg = f[:-len('.guide.md')] + '.toolguide.yaml'
        if tg in file_owner:
            file_owner[f] = file_owner[tg]
    elif f.startswith('assets/'):
        side = f + '.asset.yaml'
        if side in file_owner:
            file_owner[f] = file_owner[side]
FIXED = {
    'assets/docs_structural_lint.config.yaml': 'writing',
    'assets/audiences/README.md': 'writing',
    'assets/README.md': 'writing',
    'styleguides/writing/README.md': 'writing',
    'templates/writing/meeting-minutes.md': 'writing',
    'templates/writing/meeting-discussion-notes.md': 'writing',
    'agent_profiles/README.md': 'foundation',
    'missions/README.md': 'foundation',
}
file_owner.update({k: v for k, v in FIXED.items() if k in files})
DROP = {'skills/.gitkeep'}

unmapped = [f for f in files if f not in file_owner and f not in KEEP and f not in DROP and not f.endswith('.graph.yaml')]
if unmapped:
    print('REFUSING: unmapped files under packs/built-in:', *unmapped, sep='\n  ')
    sys.exit(2)
missing_nodes = [u for u in graph_nodes if u not in own]
if missing_nodes:
    print('REFUSING: graph nodes absent from membership.json:', *missing_nodes, sep='\n  ')
    sys.exit(2)

counts = collections.Counter(file_owner.values())
print('files per pack:', dict(sorted(counts.items(), key=lambda x: -x[1])))

# ---------------------------------------------------------------- 2. moves
for f in files:
    if f in file_owner:
        dst = f'{pdir(file_owner[f])}/{f}'
        if not DRY:
            os.makedirs(os.path.dirname(dst), exist_ok=True)
        git('mv', f'{BI}/{f}', dst)
for f in DROP:
    if f in files:
        git('rm', '-q', f'{BI}/{f}')

# ---------------------------------------------------------------- 3. graph split
edges = []
for g in sorted(f for f in files if f.endswith('.graph.yaml')):
    edges += yaml.safe_load(open(f'{BI}/{g}')).get('edges') or []

home_nodes = collections.defaultdict(list)
for urn, n in graph_nodes.items():
    home_nodes[own[urn]].append(n)
home_edges = collections.defaultdict(list)
bad, relocated = [], 0
for e in edges:
    a, b = own.get(e['source']), own.get(e['target'])
    if a is None or b is None:
        bad.append(('unknown endpoint', e['source'], e['target']))
        continue
    if b in closure(a):
        home = a
    elif a in closure(b):
        home, relocated = b, relocated + 1
    else:
        bad.append(('no legal home', e['source'], a, e['target'], b))
        continue
    e = dict(e)
    if a != home:
        e['source'] = f'{a}::{e["source"]}'
    if b != home:
        e['target'] = f'{b}::{e["target"]}'
    home_edges[home].append(e)
if bad:
    print('REFUSING: edges without a legal home:', *bad, sep='\n  ')
    sys.exit(2)
print('edges relocated upward:', relocated)

def kind_of(urn):
    return urn.split('::')[-1].split(':', 1)[0]

def dump(obj):
    return yaml.safe_dump(obj, sort_keys=False, allow_unicode=True, width=120)

for pack in sorted(set(home_nodes) | set(home_edges)):
    nodes = sorted(home_nodes[pack], key=lambda n: n['urn'])
    pedges = home_edges[pack]
    if pack in BUILTIN_LEVEL:
        kinds = sorted({n['kind'] for n in nodes} | {kind_of(e['source']) for e in pedges})
        for k in kinds:
            doc = {'schema_version': '1.0', 'generated_at': 'STATIC', 'generated_by': 'drg-migration-v1',
                   'nodes': [n for n in nodes if n['kind'] == k],
                   'edges': [e for e in pedges if kind_of(e['source']) == k]}
            if not DRY:
                open(f'{pdir(pack)}/{k}.graph.yaml', 'w').write(dump(doc))
    else:
        onodes = []
        for n in nodes:
            kind, ident = n['urn'].split(':', 1)
            entry = {'id': ident, 'kind': PLURAL[kind], 'title': n.get('label') or ident}
            if n['urn'] in body_path:
                entry['body_path'] = body_path[n['urn']]
            onodes.append(entry)
        frag = f'{pdir(pack)}/drg/fragment.yaml'
        if os.path.exists(frag):           # qa / internal: append before edges:, and at the end
            text = open(frag).read()
            head, sep, tail = text.partition('\nedges:\n')
            pad = '  ' if '\n  - id:' in head else ''      # match the file's list indentation
            ind = lambda s: ''.join((pad + l if l.strip() else l) for l in s.splitlines(True))
            text = (head.rstrip('\n') + '\n' + ind(dump(onodes)) + sep + tail.rstrip('\n') + '\n'
                    + (ind(dump(pedges)) if pedges else ''))
            if not DRY:
                open(frag, 'w').write(text)
        else:
            header = ('# The pack\'s DRG fragment, the only DRG file an org Charter Pack may ship.\n'
                      '# Carved from packs/built-in by #73 (kitty-specs/foundation-writing-split-01M75HV3).\n'
                      '# Edge endpoints are URNs (<kind>:<id>); endpoints held by another pack are qualified\n'
                      '# <pack-name>::<urn> and must sit in this pack\'s depends_on closure.\n')
            if not DRY:
                os.makedirs(os.path.dirname(frag), exist_ok=True)
                open(frag, 'w').write(header + dump({'nodes': onodes, 'edges': pedges}))
for g in sorted(f for f in files if f.endswith('.graph.yaml')):
    git('rm', '-q', f'{BI}/{g}')

# ---------------------------------------------------------------- 5. body-reference qualification
REF_FIELDS = {'directive-references': ('directive', 'code'), 'tactic-references': ('tactic', 'id'),
              'styleguide-references': ('styleguide', 'id'), 'toolguide-references': ('toolguide', 'id')}

def qualify_bodies():
    """Profile references (charter ADR-0053 d7): bare inside the profile's own pack, `<pack>::<id>` for
    another pack in its closure; an entry outside the closure is dropped (its graph edge is relocated)."""
    def urn_of(kind, ref):
        if kind == 'directive' and re.fullmatch(r'\d+', ref):
            return f'directive:DIRECTIVE_{int(ref):03d}'
        return f'{kind}:{ref}'
    dropped = []
    for pack in sorted(M['membership']):
        for path in sorted(__import__('glob').glob(f'{pdir(pack)}/**/*.agent.yaml', recursive=True)):
            doc = yaml.safe_load(open(path))
            if f"agent_profile:{doc.get('profile-id')}" not in own:
                continue                                       # a pre-existing org-pack profile (WP02)
            lines = open(path).read().splitlines(True)
            section = None
            out = []
            skip_entry = False
            for line in lines:
                top = re.match(r'^([A-Za-z-]+):', line)
                if top:
                    section = top.group(1)
                if re.match(r'^  operating-procedures:', line):
                    section = 'operating-procedures'
                elif re.match(r'^  [a-z-]+:', line) and section == 'operating-procedures':
                    section = 'collaboration'
                m = None
                if section in REF_FIELDS:
                    kind, key = REF_FIELDS[section]
                    m = re.match(r'^(\s*- ' + key + r': )("?)([^"\n]+)("?)(\s*)$', line)
                elif section == 'operating-procedures':
                    kind = 'procedure'
                    m = re.match(r'^(\s+- )()([A-Za-z0-9_.-]+)()(\s*)$', line)
                if m:
                    skip_entry = False
                    ref = m.group(3)
                    if '::' not in ref:
                        tgt = own.get(urn_of(kind, ref))
                        if tgt is not None and tgt != pack:
                            if tgt in closure(pack):
                                line = f'{m.group(1)}{m.group(2)}{tgt}::{ref}{m.group(4)}{m.group(5)}'
                            else:
                                dropped.append((path, kind, ref, tgt))
                                skip_entry = True
                                continue
                elif skip_entry and re.match(r'^\s{4,}\S', line) and section in REF_FIELDS:
                    continue                                   # continuation lines of a dropped entry
                else:
                    skip_entry = False
                out.append(line)
            text = ''.join(out)
            text = re.sub(r'(?m)^(  operating-procedures|[a-z-]+-references):\n(?=\n*(?:[A-Za-z]|  [A-Za-z]|\Z))', '', text)
            if not DRY:
                open(path, 'w').write(text)
    for d in dropped:
        print('dropped out-of-closure body reference:', *d)

# ---------------------------------------------------------------- 4. body-reference drops
def drop_directive_ref(path, code_or_id):
    s = open(path).read()
    pat = re.compile(r'(?m)^- code: "?' + re.escape(code_or_id) + r'"?\n(?:  .*\n)*')
    s2, n = pat.subn('', s)
    if n != 1:
        print(f'WARNING: {path}: expected one directive-reference {code_or_id}, removed {n}')
    s2 = re.sub(r'(?m)^directive-references:\n(?=\n*(?:[A-Za-z]|\Z))', '', s2)  # drop an emptied list key
    if not DRY:
        open(path, 'w').write(s2)

drop_directive_ref('packs/foundation/agent_profiles/analyst-annie.agent.yaml', '047')
drop_directive_ref('packs/writing/agent_profiles/diagram-daisy.agent.yaml', 'USE_C4_MODEL_TECHNIQUES')
qualify_bodies()
print('done' + (' (dry run)' if DRY else ''))
