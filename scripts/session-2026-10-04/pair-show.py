# Prints zipper pairs (Geni person vs the Wikidata item the zipper called them) for the session to read.
import json, sys
o = json.load(open("reports/session-2026-10-04/zipper-pairs-behind-wikidata-links.json", encoding="utf-8"))
j = lambda l: "/".join(str(x)[:20] for x in l[:2])
for r in o[int(sys.argv[1]):int(sys.argv[2])]:
    G, W = r["G"], r["W"]
    print(f"{r['n']} {r['qid']}<-{r['geni']} links:{len(r['links'])}\n   GN {G['name'][:38]} [{G['b'][-4:]}-{G['d'][-4:]}] f:{j(G['f'])} m:{j(G['m'])} s:{j(G['s'])} c:{j(G['c'])}"
          f"\n   WD {W['name'][:38]} [{W['b']}-{W['d']}] {W['desc'][:40]} f:{j(W['f'])} m:{j(W['m'])} s:{j(W['s'])} c:{j(W['c'])}")
