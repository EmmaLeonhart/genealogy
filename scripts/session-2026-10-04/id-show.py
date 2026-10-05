import json, sys
o = json.load(open(f"reports/session-2026-10-04/id-review-{sys.argv[1]}.json", encoding="utf-8"))
j = lambda l: "/".join(str(x) for x in l[:3])
for r in o[int(sys.argv[2]):int(sys.argv[3])]:
    W, S = r["W"], r["S"]
    print(f"#{r['n']} {r['qid']} <- {r['value']}{'' if r['live'] else ' (GONE)'}\n  WD {W['name']} | {W['desc']} [{W['b']}-{W['d']}] f:{j(W['f'])} m:{j(W['m'])} s:{j(W['s'])} c:{j(W['c'])} geni:{len(W['geni'])}\n  GN {S['name']} [{S['b']}-{S['d']}] f:{j(S['f'])} m:{j(S['m'])} s:{j(S['s'])} c:{j(S['c'])}")
