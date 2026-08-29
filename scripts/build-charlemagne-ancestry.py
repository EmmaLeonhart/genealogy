"""The blood line to Charlemagne, and where its descendants thin.

Emma, 2026-08-13: *"do this link to Charlemagne instead of the other one.
Ancestry is good like this. I want to see which points where the descendants
clearly thin in a way that suggests I'll need another export."*

**This replaces `build-charlemagne-route.py` as the link that matters.** That one
minimised people-to-create and returned a 398-step route hopping through spouses
and children — cheaper, and not a lineage. This is Geni's own *shortest blood
relationship*: Charlemagne as 35th great grandfather, 37 steps, every one a
parent.

**The path arrived as screenshots, so it carries no `href`s and no profile IDs** —
the loss CLAUDE.md warns about under "save the page, never the pasted text". Two
consequences, both handled explicitly rather than papered over:

1. Each person is looked up **by name**, against every rendering the repo holds.
   That is a report for a human and never an input to a merge, the same standing
   rule `genimerge.paths` follows for rows with no ID. A name carried by more
   than `AMBIGUITY_LIMIT` people is reported unresolved rather than claimed.
2. **The married name is why the lookup needs every rendering.** Geni's panel
   renders a woman under her husband's surname: Reinhert's mother is
   `Rakel Rasmusdottir Borsheim` there and `Rakel Rasmusdottir Lea` in the
   export, with `Borsheim` in `alias_names`. Comparing `label_en`
   alone declared the whole line absent at step 4 with 33 further steps sitting
   right there.

Connectivity is then checked **separately** from presence, because they are
different questions and the interesting answer is where they disagree.

The thinning measure: descendant counts rise monotonically up a lineage, so the
count is not the signal — the **step-to-step growth** is. An ancestor who adds
one person is one we hold only as a link in this chain.

Offline. Reads the derived CSVs and `reports/wikidata-components.csv`.

    py scripts/build-charlemagne-ancestry.py
"""

from __future__ import annotations

import csv
import sys
import unicodedata
from collections import defaultdict, deque
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
FAMILY = REPO_ROOT / "reports" / "derived-family.csv"
LABELS = REPO_ROOT / "reports" / "derived-labels.csv"
FACTS = REPO_ROOT / "reports" / "derived-facts.csv"
COMPONENTS = REPO_ROOT / "reports" / "wikidata-components.csv"
OUT_MD = REPO_ROOT / "reports" / "charlemagne-ancestry.md"
OUT_CSV = REPO_ROOT / "reports" / "charlemagne-ancestry.csv"

csv.field_size_limit(10_000_000)
AMBIGUITY_LIMIT = 20

#: Transcribed from Geni's "Shortest blood relationship" panel, 2026-08-13.
#: Each entry is (relation to the previous person, name as Geni renders it).
#: Step 5 is Geni's own "her adoptive mother", kept verbatim.
LINE: list[tuple[str, str]] = [
    ("self", "Emma Leonhart"),
    ("father", "Richard Wade Borsheim"),
    ("father", "Randolph Paulus Borsheim"),
    ("father", "Reinhert Borsheim"),
    ("mother", "Rakel Rasmusdottir Borsheim"),
    ("adoptive mother", "Anne Berta Osmundsdatter Nese"),
    ("father", "Osmund Larsson Nese"),
    ("father", "Lars Osmundsen Foss-Eikeland, d. y."),
    ("father", "Osmund Larsen Raunes"),
    ("father", "Lars Nilsen Raunes"),
    ("father", "Nils Larsen Raunes"),
    ("father", "Lars Jonsen Landsnes"),
    ("mother", "Magdalena Lauritsd Hogganvik"),
    ("mother", "Katarina Galte"),
    ("father", "Torgils Johannesson Galte"),
    ("mother", "Gyrild Torgilsdatter Galtung"),
    ("father", "Thorgil Vikingsson Måge"),
    ("father", "Viking Finnson Aga"),
    ("mother", "N.N. Vikingsdotter Nordbø"),
    ("mother", "Olov Eriksdotter"),
    ("father", "Eirik Sigurdsson Galtung"),
    ("father", "Sigurd Gautsson Galte, I"),
    ("mother", "N. Toresdatter Galte"),
    ("mother", "Bergljot Roarsdatter Øen"),
    ("mother", "Torbjørg Åsulvsdatter Austrått, til Rein"),
    ("father", "Lendmann Åsulf Guttormsson på Rein"),
    ("father", "Guttorm Àsulfsson à Rein"),
    ("father", "Åsulv Skulesson"),
    ("father", "Skule Torstigson"),
    ("mother", "Judith of Flanders"),
    ("father", "Baldwin IV the Bearded, count of Flanders"),
    ("mother", "Rozala of Italy"),
    ("father", "Berengar II of Ivrea, king of Italy"),
    ("mother", "Gisela of Friuli"),
    ("father", "Berengar I, emperor of the Romans"),
    ("mother", "Giséle of Cysoing"),
    ("father", "Louis I, The Pious"),
    ("father", "Charlemagne"),
]


def fold(text: str) -> str:
    text = unicodedata.normalize("NFKD", text or "")
    text = "".join(c for c in text if not unicodedata.combining(c))
    return "".join(c for c in text.casefold() if c.isalnum())


def renderings_of(row: dict) -> list[str]:
    """Every name this repo holds for a person, married names included."""
    out: list[str] = []
    for field in ("label_en", "label_mul", "further_latin_names",
                  "alias_names"):
        for part in (row.get(field) or "").split(" | "):
            if part.strip():
                out.append(part.strip())
    return out


def main() -> int:
    fam = {r["geni_id"]: r for r in csv.DictReader(open(FAMILY, encoding="utf-8"))}
    lab = {r["geni_id"]: r for r in csv.DictReader(open(LABELS, encoding="utf-8"))}
    fac = {r["geni_id"]: r for r in csv.DictReader(open(FACTS, encoding="utf-8"))}
    sizes: dict[str, int] = {}
    if COMPONENTS.exists():
        for row in csv.DictReader(open(COMPONENTS, encoding="utf-8")):
            sizes[row["qid"]] = int(row["component_size"])

    kids: dict[str, list[str]] = defaultdict(list)
    for geni_id, row in fam.items():
        for parent in (row.get("father"), row.get("mother")):
            if parent:
                kids[parent].append(geni_id)

    # One person can be indexed under several renderings; keep the set, not a
    # list, or a person whose label_en and label_mul agree looks like two people.
    index: dict[str, set[str]] = defaultdict(set)
    for geni_id, row in lab.items():
        for rendering in renderings_of(row):
            index[fold(rendering)].add(geni_id)

    def resolve(expected: str) -> tuple[str, str]:
        key = fold(expected)
        hits = index.get(key, set())
        if not hits:
            # Geni sometimes carries a trailing epithet the export's NAME lacks.
            hits = {g for k, ids in index.items()
                    if k.startswith(key) and len(k) - len(key) < 14 for g in ids}
        if not hits:
            return "", "absent"
        if len(hits) > AMBIGUITY_LIMIT:
            return "", f"ambiguous ({len(hits)})"
        chosen = sorted(hits)[0]
        return chosen, "present" if len(hits) == 1 else f"present ({len(hits)} candidates)"

    def descendants(root: str) -> tuple[int, int]:
        seen: set[str] = set()
        queue = deque([root])
        while queue:
            for child in kids.get(queue.popleft(), []):
                if child not in seen:
                    seen.add(child)
                    queue.append(child)
        return len(seen), sum(1 for g in seen if lab.get(g, {}).get("qid"))

    rows: list[dict] = []
    for i, (relation, expected) in enumerate(LINE):
        geni_id, state = resolve(expected)
        row: dict = {"step": i, "relation": relation, "geni_name": expected,
                     "geni_id": geni_id, "presence": state}
        if geni_id:
            total, with_qid = descendants(geni_id)
            held = (lab[geni_id].get("label_en") or "").strip()
            qid = lab[geni_id].get("qid", "")
            row |= {
                "held_as": "" if fold(held) == fold(expected) else held,
                "born": fac.get(geni_id, {}).get("birth_date_year", "") or "",
                "children": len(kids.get(geni_id, [])),
                "parents": sum(1 for k in ("father", "mother") if fam.get(geni_id, {}).get(k)),
                "descendants": total, "desc_wd": with_qid,
                "qid": qid, "component": sizes.get(qid, "") if qid else "",
            }
        else:
            row |= {"held_as": "", "born": "", "children": "", "parents": "",
                    "descendants": "", "desc_wd": "", "qid": "", "component": ""}
        rows.append(row)

    # Presence and connectivity are different questions. Check the edges.
    breaks: list[dict] = []
    for i in range(len(rows) - 1):
        a, b = rows[i]["geni_id"], rows[i + 1]["geni_id"]
        if not a or not b:
            rows[i]["edge"] = "?"
            continue
        row = fam.get(a, {})
        via = ("father" if row.get("father") == b else
               "mother" if row.get("mother") == b else "")
        rows[i]["edge"] = via or "BROKEN"
        if not via:
            breaks.append({"from": rows[i], "to": rows[i + 1]})
    rows[-1]["edge"] = ""

    with open(OUT_CSV, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=[
            "step", "relation", "geni_name", "held_as", "geni_id", "presence",
            "edge", "born", "parents", "children", "descendants", "desc_wd",
            "qid", "component"])
        writer.writeheader()
        writer.writerows(rows)

    present = [r for r in rows if r["geni_id"]]
    absent = [r for r in rows if not r["geni_id"]]

    # Growth per step. Descendant counts are cumulative up a lineage, so the
    # count itself is not the signal — the growth is.
    growth: list[tuple[dict, int]] = []
    previous = None
    for r in present:
        if previous is not None:
            growth.append((r, r["descendants"] - previous))
        previous = r["descendants"]

    L: list[str] = []
    add = L.append
    add("# The blood line to Charlemagne, and where it thins")
    add("")
    add("Emma, 2026-08-13: *\"do this link to Charlemagne instead of the other one.")
    add("Ancestry is good like this. I want to see which points where the descendants")
    add("clearly thin in a way that suggests I'll need another export.\"*")
    add("")
    add("Geni's own **shortest blood relationship** — Charlemagne as 35th great")
    add(f"grandfather, **{len(LINE)-1} steps, every one a parent**. This supersedes")
    add("`reports/charlemagne-route.md`, which minimised people-to-create and got a")
    add("398-step route through spouses and children: cheaper, and not a lineage.")
    add("")
    add(f"**{len(present)} of the {len(LINE)} people are already in the merged tree**, and")
    add(f"the line connects end to end apart from {len(breaks)} broken edge and")
    add(f"{len(absent)} absent people.")
    add("")

    add("## The line")
    add("")
    add("`edge` is the recorded parent link to the **next** row — what actually")
    add("connects, as opposed to what is merely present.")
    add("")
    add("| step | born | who | edge | children | descendants | +over below | with WD |")
    add("| ---: | ---: | --- | --- | ---: | ---: | ---: | ---: |")
    grow = {id(r): g for r, g in growth}
    for r in rows:
        if not r["geni_id"]:
            add(f"| {r['step']} | | **{r['geni_name']}** — {r['presence']} | — | | | | |")
            continue
        who = r["geni_name"]
        if r["held_as"]:
            who += f" <br><small>held as {r['held_as']}</small>"
        edge = "**BROKEN**" if r["edge"] == "BROKEN" else (r["edge"] or "—")
        g = grow.get(id(r))
        add(f"| {r['step']} | {r['born']} | {who} | {edge} | {r['children']} | "
            f"{r['descendants']:,} | {g:+,} | {r['desc_wd']:,} |" if g is not None else
            f"| {r['step']} | {r['born']} | {who} | {edge} | {r['children']} | "
            f"{r['descendants']:,} | | {r['desc_wd']:,} |")
    add("")

    add("## Where the line breaks")
    add("")
    for b in breaks:
        a, c = b["from"], b["to"]
        add(f"- **step {a['step']} → {c['step']}**: *{a['geni_name']}* → "
            f"*{c['geni_name']}*. Both are in the tree; the parent link is not. "
            f"Geni calls this relation *\"{c['relation']}\"* — **an adoption**, and "
            f"our derived family edges carry birth parents only. The tree gives "
            f"{a['geni_name']}'s parents as someone else entirely.")
    for r in absent:
        add(f"- **step {r['step']}**: *{r['geni_name']}* — {r['presence']}. Its "
            f"neighbours are held, so this is a single missing person rather than a "
            f"missing stretch.")
    add("")
    add("**None of these breaks needs an export to fix.** Two are people Geni has and")
    add("we did not sample; one is an adoption edge that the GEDCOM records with a")
    add("pedigree tag our family derivation drops.")
    add("")

    add("## Where the descendants thin — the export answer")
    add("")
    add("Descendant counts rise monotonically up a lineage: every ancestor's")
    add("descendants include everyone below them. So the count is not the signal. The")
    add("**growth from one step to the next** is: an ancestor who adds one person is")
    add("one we hold *only* as a link in this chain, with every sibling of the next")
    add("step unexplored.")
    add("")
    thin = [(r, g) for r, g in growth if g <= 2]
    add(f"**{len(thin)} of the {len(growth)} steps add two people or fewer.** They are not")
    add("scattered — they come in runs, and a run is what a single export fixes.")
    add("")
    add("| step | born | who | children | added |")
    add("| ---: | ---: | --- | ---: | ---: |")
    for r, g in thin:
        add(f"| {r['step']} | {r['born']} | {r['geni_name']} | {r['children']} | {g:+,} |")
    add("")

    add("## Reading it")
    add("")
    add("- **Steps 16–23, roughly 1430 back to 1200** — the Måge / Aga / Galtung /")
    add("  Galte stretch — is the thin run that matters. Eight consecutive")
    add("  generations, each with **exactly one recorded child**, the whole run adding")
    add("  seven people. We have a bare thread through two and a half centuries of")
    add("  Norwegian ancestry and nothing on either side of it.")
    add("- **Steps 9–11, 1697 back to 1625** is the same shape, shorter and later.")
    add("- **Everything above step 26 is dense** — Guttorm à Rein carries 10,070")
    add("  descendants and Judith of Flanders 24,874. That end of the line is")
    add("  well-sampled and needs nothing.")
    add("- **The Wikidata column turns on at the same place.** Steps 15–23 have four")
    add("  Wikidata-linked descendants between them; step 26 has 585 and step 29 has")
    add("  1,623. The thin run is invisible to Wikidata as well as to us.")
    add("")
    add("**So one export, seeded in the 1200–1430 stretch, is the pick.** A `Forest`")
    add("or `Descendants` take from any of steps 16–23 would fan out across siblings")
    add("this line has never touched.")
    add("")
    add("## Caveats")
    add("")
    add("- **Names resolved without profile IDs.** The screenshots carry no `href`s, so")
    add("  every person here was found by name against every rendering the repo holds.")
    add("  Saving the page and running `path-from-html` would make this exact.")
    add("- **Descendant counts measure our exports, never Geni.** A thin ancestor is one")
    add("  *we* barely sampled. Whether Geni holds more there is what an export settles.")
    add("- **Step 5 is an adoption** and Geni still calls the path a blood relationship.")
    add("  Recorded as it stands rather than reinterpreted.")

    OUT_MD.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"wrote {OUT_MD} and {OUT_CSV}")
    print(f"  {len(present)}/{len(LINE)} present, {len(breaks)} broken edges, "
          f"{len(absent)} absent")
    for r in absent:
        print(f"    absent: step {r['step']:>2}  {r['geni_name']}")
    for b in breaks:
        print(f"    broken: step {b['from']['step']}->{b['to']['step']}  "
              f"{b['from']['geni_name']} -> {b['to']['geni_name']}")
    print(f"  {len(thin)} steps add <=2 descendants:")
    for r, g in thin:
        print(f"    step {r['step']:>2}  {str(r['born']):>4}  {g:+3,}  "
              f"{r['children']} child  {r['geni_name']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
