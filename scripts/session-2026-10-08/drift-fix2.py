"""Second round of Geni-drift fixes, 2026-10-08, after Emma's "do more analysis ... and fix these things".
Cases and reasons: `reports/geni-drift-cases-2026-10-08.md` § Round 2. Reads each item live and emits a removal only for
a value present now; appends every removal to `reports/removed-statements.tsv`.
  reports/geni-drift-fix2-2026-10-08.qs, reports/geni-drift-fix2-aliases-2026-10-08.json

    python scripts/session-2026-10-08/drift-fix2.py
"""
import datetime, json, sys, urllib.request
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
UA = {"User-Agent": "genealogy-review/1.0 (emma)"}
# qid: ([(property, value)], [mul aliases])
SPEC = {
    "Q141562977": ([("P734", "Q24353049")], []),                      # Siri Madland: her husband's given name as surname
    "Q141515038": ([("P735", "Q1457563")], []),                       # Hallgrim Oxehode: the walk's Aslak
    "Q141382445": ([("P734", "Q2817217")], []),                       # Niklas Olsson: his brother's family's Andersson
    "Q141382447": ([("P734", "Q2817217")], []),                       # Stina Larsdotter: the same
    "Q141564600": ([("P22", "Q141570110")], []),                      # Andres Ottarsen: the Geni person's father
    "Q141570110": ([("P40", "Q141564600")], []),                      # Knut Mestad: the reverse link
    "Q141499675": ([("P2889", "G6HP-V83")], ["Jakob von Güntersberg"]),
    "Q141502702": ([("P2889", "GBYR-856")], ["Henning von Güntersberg"]),
    "Q141510091": ([("P2889", "GDBR-PKV")], ["Voltekin Walter von Güntersberg"]),
    "Q141511190": ([("P2889", "GBYR-F31")], []),
    "Q141515084": ([("P2889", "GBYR-FQH")], ["Jakub Kaszuba von Güntersberg"]),
    "Q141517168": ([("P2889", "LVGN-3RW")], []),                      # Eickstedt: one generation off
    "Q141523508": ([("P2889", "LVGN-3YS")], []),
}


def main():
    u = ("https://www.wikidata.org/w/api.php?action=wbgetentities&format=json&props=claims|aliases&languages=mul&ids="
         + "|".join(SPEC))
    ents = json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60))["entities"]
    qs, aliases, rec = ["# Geni drift fixes, round 2 (Emma, 2026-10-08). Run."], {}, []
    for q, (stmts, als) in SPEC.items():
        e = ents[q]
        for p, v in stmts:
            live = [c["mainsnak"].get("datavalue", {}).get("value") for c in e["claims"].get(p, [])]
            live = [x["id"] if isinstance(x, dict) else x for x in live]
            if v in live:
                qs.append(f"-{q}\t{p}\t{v}" if v.startswith("Q") else f'-{q}\t{p}\t"{v}"'); rec.append((q, p, v))
            else:
                print(q, p, v, "already absent")
        live_al = [a["value"] for a in e.get("aliases", {}).get("mul", [])]
        gone = [a for a in als if a in live_al]
        for a in als:
            if a not in live_al:
                print(q, "alias", a, "already absent")
        if gone:
            aliases[q] = gone; rec += [(q, "Amul", a) for a in gone]
    (ROOT / "reports" / "geni-drift-fix2-2026-10-08.qs").write_text("\n".join(qs) + "\n", encoding="utf-8", newline="\n")
    (ROOT / "reports" / "geni-drift-fix2-aliases-2026-10-08.json").write_text(
        json.dumps(aliases, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    with open(ROOT / "reports" / "removed-statements.tsv", "a", encoding="utf-8", newline="\n") as f:
        for q, p, v in rec:
            f.write(f"{q}\t{p}\t{v}\tEmma (Geni drift fix round 2, positional walk)\t{datetime.date.today()}\n")
    print(len(qs) - 1, "statement removals;", sum(map(len, aliases.values())), "aliases")


if __name__ == "__main__":
    main()
