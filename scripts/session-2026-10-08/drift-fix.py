"""The fixes for the Geni-drift item, as Emma answered on 2026-10-08 (AskUserQuestion): for the 14 items created as the
walk's FamilySearch person under another person's Geni id, remove that Geni id and the alias and patronymic that came
with the Geni person ("Remove Geni id + residue"); for the 9 items carrying another person's statements from the walk,
remove those statements ("Yes, remove them"). Cases: `reports/geni-drift-cases-2026-10-08.md`.

Reads each item live and emits a removal only for a value that is there now:
  reports/geni-drift-fix-2026-10-08.qs        statement removals (QuickStatements, Run in a new tab)
  reports/geni-drift-fix-aliases-2026-10-08.json   mul aliases to remove (wbsetaliases from a logged-in tab)
and appends each removed statement to `reports/removed-statements.tsv`, which the batch builder never re-adds.

    python scripts/session-2026-10-08/drift-fix.py
"""
import csv, datetime, json, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
UA = {"User-Agent": "genealogy-review/1.0 (emma)"}
GENI = {r["qid"]: r["geni_id"] for r in csv.DictReader(open(ROOT / "reports" / "geni-drift-versions-2026-10-08.csv",
                                                            encoding="utf-8"))}
# qid: (remove that Geni id?, FamilySearch ids, patronymic items, mul aliases)
SPEC = {
    # created as the walk's FamilySearch person under another person's Geni id (14)
    "Q141562866": (True, [], ["Q141283709"], ["Mogens Olson Bjørgås", "Mogens Bjørgås"]),
    "Q141559631": (True, [], ["Q141440462"], ["Tormod Monsson Bjørgås"]),
    "Q141558357": (True, [], ["Q141436525"], ["Marita Larsdotter Bjørgås"]),
    "Q141562856": (True, [], ["Q141290425"], ["Lars Larsson"]),
    "Q141562358": (True, [], [], ["Kari Bjørgås"]),
    "Q141562826": (True, [], [], ["Hallvard Bjørgås", "Hallvard Gulleikson Bjørgås"]),
    "Q141565565": (True, [], ["Q141552172"], ["Knut Sjurson Bjørgo"]),
    "Q141565713": (True, [], ["Q51885688"], ["Elisabet Olsdatter Bjørgo"]),
    "Q141564600": (True, [], ["Q141419268"], ["Knut Knutsen Mestad", "Moestad"]),
    "Q141565147": (True, [], ["Q141283474"], ["Guri Knutsdatter Mestad"]),
    "Q141560557": (True, [], ["Q141352780"], ["Berge Brunborg", "Berge Toresen Brunborg"]),
    "Q141569620": (True, [], ["Q141381254"], ["Ambjørg Johannesdatter"]),
    "Q141571165": (True, [], ["Q141518427"], ["Knut Toresson Hærum"]),
    "Q141579565": (True, [], [], ["Karl Bååt"]),
    # another person's statements left by the walk (9)
    "Q141532596": (False, ["G2T9-19V"], ["Q141314143"], ["Elen Svensdatter Fosse"]),
    "Q141538482": (False, ["L63V-WW2"], ["Q141318548"], []),
    "Q141422290": (False, ["L6RL-W5T"], ["Q141318566"], []),
    "Q141217433": (False, ["LRP6-5H5"], [], ["Daniel Pehrsson"]),
    "Q141570661": (False, ["GXSB-Q57"], [], []),
    "Q141532548": (False, [], ["Q141250201"], ["Malin Olofsdotter"]),
    "Q141533731": (False, [], ["Q130233015"], []),
    "Q141549731": (False, [], ["Q130233015"], []),
    "Q141528244": (False, [], [], ["Anna Nilsdotter"]),
}


def main():
    ids = sorted(SPEC)
    u = ("https://www.wikidata.org/w/api.php?action=wbgetentities&format=json&props=claims|aliases&languages=mul&ids="
         + "|".join(ids))
    ents = json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60))["entities"]
    qs = ["# Geni drift fixes (Emma, 2026-10-08, by AskUserQuestion). reports/geni-drift-cases-2026-10-08.md. Run."]
    aliases, removed = {}, []
    today = datetime.date.today().isoformat()
    for q in ids:
        geni, fsids, pats, als = SPEC[q]
        e = ents[q]
        val = lambda p: [c["mainsnak"].get("datavalue", {}).get("value") for c in e["claims"].get(p, [])]
        live_geni, live_fs = val("P2600"), val("P2889")
        live_pat = [v["id"] for v in val("P5056") if v]
        live_al = [a["value"] for a in e.get("aliases", {}).get("mul", [])]
        if geni and GENI[q] in live_geni:
            qs.append(f'-{q}\tP2600\t"{GENI[q]}"'); removed.append((q, "P2600", GENI[q]))
        for f in fsids:
            if f in live_fs:
                qs.append(f'-{q}\tP2889\t"{f}"'); removed.append((q, "P2889", f))
        for p in pats:
            if p in live_pat:
                qs.append(f"-{q}\tP5056\t{p}"); removed.append((q, "P5056", p))
        gone = [a for a in als if a in live_al]
        if gone:
            aliases[q] = gone
            removed += [(q, "Amul", a) for a in gone]
        missing = [x for x in ([GENI[q]] if geni else []) + fsids if x not in live_geni + live_fs] + \
                  [p for p in pats if p not in live_pat] + [a for a in als if a not in live_al]
        if missing:
            print(q, "already absent:", missing)
    (ROOT / "reports" / "geni-drift-fix-2026-10-08.qs").write_text("\n".join(qs) + "\n", encoding="utf-8", newline="\n")
    (ROOT / "reports" / "geni-drift-fix-aliases-2026-10-08.json").write_text(
        json.dumps(aliases, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    with open(ROOT / "reports" / "removed-statements.tsv", "a", encoding="utf-8", newline="\n") as f:
        for q, p, v in removed:
            f.write(f"{q}\t{p}\t{v}\tEmma (Geni drift fix, positional walk)\t{today}\n")
    print(len(qs) - 1, "statement removals;", sum(map(len, aliases.values())), "aliases;", len(removed), "rows recorded")


if __name__ == "__main__":
    main()
