import json, sys
o = json.load(open(f"reports/session-2026-10-04/id-review-{sys.argv[1]}.json", encoding="utf-8"))
j = lambda l: "/".join(str(x)[:22] for x in l[:2])
for r in o[int(sys.argv[2]):int(sys.argv[3])]:
    W, S = r["W"], r["S"]
    print(f"{r['n']}{'' if r['live'] else '(GONE)'}: {W['name'][:40]} [{W['b']}-{W['d']}] f:{j(W['f'])} s:{j(W['s'])} c:{j(W['c'])}"
          f"  ||  {S['name'][:40]} [{S['b'][-4:]}-{S['d'][-4:]}] f:{j(S['f'])} s:{j(S['s'])} c:{j(S['c'])}")
