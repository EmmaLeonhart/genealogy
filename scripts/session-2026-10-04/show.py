import json,sys
op=json.load(open("reports/session-2026-10-04/ancestor-deck-open-cards.json",encoding='utf-8'))
gf=[c for c in op if not (c['a']['id'].startswith('FS') and c['b']['id'].startswith('FS'))]
a,b=int(sys.argv[1]),int(sys.argv[2])
def side(p):
    r=p['r']; j=lambda l:'/'.join(l[:3])
    return f"{p['n']} [{p['b']}-{p['d']}] f:{j(r['f'])} m:{j(r['m'])} s:{j(r['s'])} c({r['nc']}):{j(r['c'])}"
print(len(gf),'Geni-FS open')
for i,c in enumerate(gf[a:b],a):
    print(f"#{i} {c['slot']} of {c['child']} gen{c['gen']} gap{c['gap']} old={c.get('old','')}\n  A {c['a']['id']}: {side(c['a'])}\n  B {c['b']['id']}: {side(c['b'])}")
