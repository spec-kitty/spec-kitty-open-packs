import json,collections,re,sys
R='research/'
E=json.load(open(R+'edges.json')); D=json.load(open(R+'delegates.json')); P=json.load(open(R+'profrefs.json'))
S=json.load(open(R+'strict-membership.json')); B=json.load(open('bundles/B-bundles.json'))
own={}
for n in S['foundation']: own[n]='foundation'
for n in S['writing']: own[n]='writing'
for n in S['internal']: own[n]='spec-kitty-internal'
for n in S['qa']: own[n]='quality-assurance'
for b,v in B['bundles'].items():
    for n in v: own[n]=b
for n in B['_proposed_from_qa']['testing']: own[n]='testing'
# operator rulings
for n in list(own):
    if own[n] in('core-engineering','->foundation','git-delivery'): own[n]='foundation'
    elif own[n]=='->writing': own[n]='writing'
own['agent_profile:retrospective-facilitator']='planning-analysis'
own['directive:DISCIPLINED_REFACTORING']='foundation'
own['directive:DIRECTIVE_039']='foundation'; own['procedure:small-explicit-code-shaping']='foundation'
own['paradigm:brownfield-onboarding']='planning-analysis'
# directive-required how-tos and step delegates -> foundation (fixpoint over foundation directives' requires)
dirnum={re.match(r'directive:DIRECTIVE_0*(\d+)$',n).group(1):n for n in own if re.match(r'directive:DIRECTIVE_0*\d+$',n)}
def res(t):
    m=re.match(r'directive:0*(\d+)$',t); return dirnum.get(m.group(1),t) if m else t
changed=True
pulled=[]
while changed:
    changed=False
    for s,r,t,*_ in E:
        if own.get(s)=='foundation' and s.startswith('directive:') and r=='requires' and own.get(t) not in('foundation',None) and own.get(t)!='writing':
            pulled.append((t,own[t],s)); own[t]='foundation'; changed=True
    for s,r,t in D:
        if own.get(s)=='foundation' and own.get(t) not in('foundation','writing',None):
            pulled.append((t,own[t],s)); own[t]='foundation'; changed=True
print('pulled into foundation by rule:',len(pulled)); [print('  ',p) for p in pulled]
deps={'foundation':set(),'writing':{'foundation'},'built-in':{'foundation','writing'}}
DEP=B['_depends_on']
for k,v in DEP.items():
    if k in('foundation','writing','cut','core-engineering','git-delivery'): continue
    name={'qa':'quality-assurance','internal':'spec-kitty-internal'}.get(k,k)
    deps[name]=set({'qa':'quality-assurance','internal':'spec-kitty-internal'}.get(x,x) for x in v if x not in('core-engineering','git-delivery'))|{'foundation'}
deps.setdefault('event-driven',{'foundation'});deps.setdefault('spdd',{'foundation'});deps.setdefault('cave-kitty',{'foundation'})
def clo(p,seen=None):
    seen=seen or set()
    if p in seen: return seen
    seen.add(p)
    for q in deps.get(p,()): clo(q,seen)
    return seen
# body refs
bodyviol=[]
for s,r,t in D:
    if own.get(t) and own[t] not in clo(own[s]): bodyviol.append(('delegates',s,own[s],t,own[t]))
for s,r,t in P:
    if r in('directive-references','tactic-references'):
        t=res(t)
        if own.get(t) and own.get(s) and own[t] not in clo(own[s]): bodyviol.append((r,s,own[s],t,own[t]))
print('body-ref violations:',len(bodyviol)); [print('  ',v) for v in bodyviol]
# graph edges needing relocation & impossible edges
reloc=0; imp=[]; needdep=collections.Counter()
for s,r,t,*_ in E:
    a,b=own.get(s),own.get(t)
    if not a or not b or a==b: continue
    if b in clo(a): continue
    if a in clo(b): reloc+=1; continue
    imp.append((s,a,r,t,b)); needdep[(a,b)]+=1
print('relocated edges:',reloc,' impossible edges:',len(imp))
for k,c in needdep.most_common(): print('  ',k,c)
cnt=collections.Counter(own.values()); print(dict(sorted(cnt.items(),key=lambda x:-x[1])))
json.dump({'membership':{p:sorted(n for n in own if own[n]==p) for p in cnt},'depends_on':{k:sorted(v) for k,v in deps.items()},'impossible_edges':imp,'body_violations':bodyviol},open('bundles/F-final.json','w'),indent=1)
