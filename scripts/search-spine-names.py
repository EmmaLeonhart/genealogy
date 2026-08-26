"""Candidates for the spine people we call absent — by name, for a human to judge.

    python scripts/search-spine-names.py

**Emma, 2026-08-25:** *"we didn't actually establish in any meaningful sense that the people are
absent in that chain... I want you to actually at least make some effort in trying to do text
searches on the names or variants of the names on Wikidata... We might basically find that that one
single daughter is the only person absent in the line in Wikidata, but it's just that the Wikidata
ones are not genealogically linked."*

She is right that nothing established the absences. They were called absent because no `P2600`
*Geni.com profile ID* carries their Geni ids — the same reasoning that called `Q2183430` *Benedicta
Ebbesdotter of Hvide* absent while she sat in the store with thirty properties.

**The structural half already ran** and found **4 of 22** — Rozala of Italy `Q466257`, Knut
Valdemarsson → `Q3743799` *Canute, Duke of Estonia*, Berengar I → `Q274606`, Gisele of Cysoing →
`Q284400`. This is the text half, over the remaining 18.

## Candidates, never matches

`CLAUDE.md` deleted a module for using names to decide identity and it stays deleted. **Nothing
here resolves anything.** Every row is a candidate for Emma to look at, ranked by how much
*besides* the name agrees.

Ranking signals, all offline:

* **shared identifying words** between our name and any label or alias in
  `en`/`mul`/`no`/`nb`/`sv`/`da` — the more, the better, and a rarer word counts for more.
* **era** — a birth or death year within a working lifetime of ours, where both are known.
* **external genealogy identifiers** — `P1819` Genealogics, `P1185` Rodovid, `P7929` Geneanet,
  `P8172` Roglo, `P4159` WeRelate, `P4638` The Peerage and the rest. Emma: *"I think Wikidata does
  the best at entity resolution across different genealogical databases... if those things have
  cross-references with Geni, we could potentially go down that chain."* An item carrying one of
  those for a person this chain names is the same kind of evidence a `P2600` would be, arriving by
  another route.

**Diacritics are kept.** `CLAUDE.md` is explicit that folding them invents ambiguity — 525
genuinely ambiguous names became 1,312 when a previous pass folded them.

**Cross-language variants are generated**, because her twenty hand verdicts in
`reports/emma-judgments.tsv` show that is exactly where the real variation lives: she accepted
`Lars`/`Laurens`, `Margareta`/`Marjatta`, `Gustafsson`/`Kustaanpoika`, `Nilsdotter`/`Niilontytär`.
A search that only matches the Swedish spelling would have missed every one of them.

Writes `reports/spine-name-candidates.tsv` and `reports/spine-name-candidates.md`.
"""
from __future__ import annotations

import collections
import csv
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
csv.field_size_limit(1 << 30)
ROOT = Path(__file__).resolve().parent.parent
R = ROOT / "reports"

SPINE = ROOT / "paths" / "charlemagne-to-arne-garborg.tsv"

#: Words that identify nobody. Titles, particles, offices, and the redaction markers.
NOISE = {
    "of", "de", "von", "van", "der", "den", "di", "da", "du", "la", "le", "el", "af",
    "och", "the", "til", "till", "zu", "zur", "sir", "lord", "lady", "count", "countess",
    "graf", "gräfin", "duke", "duchess", "king", "queen", "baron", "baroness", "earl",
    "prince", "princess", "herr", "fru", "nn", "unknown", "private", "ukjent", "kong",
    "konge", "jarl", "herre", "frue", "knight", "lagmann", "emperor", "empress",
    "i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x",
}

#: Cross-language equivalences her own verdicts accepted. NOT a normalisation -- both forms
#: are kept and either may match, because folding them would be the diacritic mistake again.
VARIANTS = {
    "lars": {"laurens", "laurentius", "lauritz", "lauridsen", "laurens"},
    "jon": {"jonas", "johannes", "johan", "john"},
    "peder": {"peter", "petrus", "per", "pehr"},
    "knut": {"canute", "cnut", "knud", "canutus"},
    "tore": {"thore", "thor", "tor"},
    "gunnbjørn": {"gunbjorn", "gunbjørn", "gunnbjorn"},
    "bergitte": {"birgitte", "birgitta", "brigitta", "birgit"},
    "ingrid": {"ingerid", "ingride"},
    "helena": {"helene", "helen", "elin"},
    "margareta": {"margrete", "margaret", "marjatta", "margareth"},
    "ramborg": {"ramborg"},
    "algot": {"algotsson", "algoth"},
    "svantepolk": {"svantepolk", "zwantepolk"},
    "ingegerd": {"ingeborg", "ingegärd"},
    "berit": {"birgitte", "berete"},
    "marta": {"marthe", "martha", "marit"},
    "asulv": {"åsulv", "aasulv", "asulf"},
    "guttorm": {"gudthorm", "guthorm"},
}


def words(name):
    out = set()
    for w in re.split(r"[^0-9A-Za-zÀ-ÿĀ-ſ]+", (name or "").lower()):
        if len(w) > 2 and w not in NOISE and not re.fullmatch(r"\d+(st|nd|rd|th)?", w):
            out.add(w)
    return out


def expand(ws):
    """Every word plus its cross-language equivalents. Originals are always kept."""
    out = set(ws)
    for w in ws:
        out |= VARIANTS.get(w, set())
        for base, forms in VARIANTS.items():
            if w in forms:
                out.add(base)
                out |= forms
    return out


def main():
    # ---- the spine, and who is still called absent -----------------------------------
    rows = [l.rstrip("\n").split("\t") for l in open(SPINE, encoding="utf-8")
            if not l.startswith("#") and l.strip()]
    header, chain = rows[0], []
    for r in rows[1:]:
        d = dict(zip(header, r))
        gid = re.sub(r"\D", "", d.get("note", ""))
        if gid:
            chain.append((int(d["step"]), gid, d["name"]))

    held = set()
    with open(ROOT / "out" / "wikidata" / "p2600-all.tsv", encoding="utf-8") as f:
        for row in csv.reader(f, delimiter="\t"):
            if len(row) >= 2:
                held.add(row[1].strip())
    for path, col in ((R / "garborg-qids.tsv", "geni_id"),):
        if path.exists():
            with open(path, encoding="utf-8") as f:
                for row in csv.DictReader(f, delimiter="\t"):
                    held.add(row[col])
    found = {}
    p = R / "spine-already-on-wikidata.tsv"
    if p.exists():
        with open(p, encoding="utf-8") as f:
            for row in csv.DictReader(f, delimiter="\t"):
                found[row["geni_id"]] = row["candidate_qid"]

    absent = [(s, g, n) for s, g, n in chain if g not in held and g not in found]
    print(f"{len(chain)} chain steps; {len(absent)} still called absent "
          f"({len(found)} settled structurally, {len(chain) - len(absent) - len(found)} hold a "
          f"P2600)")

    years = {}
    with open(R / "derived-facts.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["geni_id"] in {g for _s, g, _n in absent}:
                years[row["geni_id"]] = (row["birth_date_year"], row["death_date_year"])

    # ---- index the store's labels by word --------------------------------------------
    wanted = {}
    for _s, g, n in absent:
        wanted[g] = expand(words(n))
    every = set().union(*wanted.values()) if wanted else set()
    print(f"{len(every)} distinct search words after cross-language expansion")

    by_word = collections.defaultdict(list)
    scanned = 0
    with open(ROOT / "out" / "wikidata" / "labels.tsv", encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            scanned += 1
            text = " ".join(filter(None, (row["en"], row["mul"], row["no"], row["nb"],
                                          row["sv"], row["da"], row["aliases"])))
            hit = words(text) & every
            if not hit:
                continue
            for w in hit:
                by_word[w].append((row["qid"], row["en"] or row["mul"] or row["sv"]
                                   or row["no"] or row["nb"] or row["da"], row["ids"]))
    print(f"{scanned:,} items scanned; {sum(len(v) for v in by_word.values()):,} word hits")

    ty = {}
    with open(ROOT / "out" / "wikidata" / "dates.tsv", encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            ty[row["qid"]] = row["birth_year"]

    #: A word matching thousands of items identifies nobody; one matching a handful is real
    #: evidence. This is the rarity weight, not a cutoff -- nothing is discarded for it.
    rarity = {w: len(v) for w, v in by_word.items()}

    out = []
    for step, g, name in absent:
        by_qid = collections.defaultdict(set)
        meta = {}
        for w in wanted[g]:
            for qid, label, ids in by_word.get(w, ()):
                by_qid[qid].add(w)
                meta[qid] = (label, ids)
        ours_birth = years.get(g, ("", ""))[0]
        scored = []
        for qid, hits in by_qid.items():
            label, ids = meta[qid]
            score = sum(1.0 / max(rarity.get(w, 1), 1) ** 0.5 for w in hits) * len(hits)
            era = ""
            if ours_birth and ty.get(qid):
                try:
                    d = abs(int(ours_birth) - int(ty[qid]))
                    era = str(d)
                    if d <= 40:
                        score *= 3
                    elif d <= 100:
                        score *= 1.5
                    else:
                        score *= 0.3
                except ValueError:
                    pass
            ext = [i for i in (ids or "").split(";") if i and not i.startswith("P2600")]
            if ext:
                score *= 1.4
            scored.append((score, qid, label, sorted(hits), era, ";".join(ext[:4])))
        scored.sort(reverse=True)
        for rank, (score, qid, label, hits, era, ext) in enumerate(scored[:8], 1):
            out.append({"step": step, "geni_id": g, "our_name": name,
                        "our_birth": ours_birth, "rank": rank,
                        "candidate_qid": qid, "candidate_label": label,
                        "candidate_birth": ty.get(qid, ""),
                        "years_apart": era, "shared_words": ",".join(hits),
                        "external_ids": ext, "score": f"{score:.3f}"})
        print(f"  step {step:>2} {name[:46]:<46} {len(scored):>5} candidates")

    with open(R / "spine-name-candidates.tsv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]), delimiter="\t")
        w.writeheader()
        w.writerows(out)

    with open(R / "spine-name-candidates.md", "w", encoding="utf-8", newline="\n") as f:
        f.write("# Spine people called absent — name candidates for a human to judge\n\n")
        f.write("Generated by `scripts/search-spine-names.py`. **Nothing here is a match.** "
                "Emma: *\"we didn't actually establish in any meaningful sense that the people "
                "are absent in that chain.\"* The structural search already settled 4 of 22; "
                f"this is the text search over the remaining {len(absent)}.\n\n")
        f.write("Ranked by how much *besides* the name agrees — era, external genealogy "
                "identifiers, and how rare the shared word is. Diacritics kept; cross-language "
                "variants generated, because her own verdicts accepted `Lars`/`Laurens` and "
                "`Margareta`/`Marjatta`.\n\n")
        cur = None
        for row in out:
            if row["step"] != cur:
                cur = row["step"]
                f.write(f"\n## Step {row['step']} — {row['our_name']}"
                        + (f" (b. {row['our_birth']})" if row["our_birth"] else "") + "\n\n")
                f.write("| # | candidate | born | apart | shared | external ids |\n")
                f.write("| ---: | --- | ---: | ---: | --- | --- |\n")
            f.write(f"| {row['rank']} | [{row['candidate_label']}]"
                    f"(https://www.wikidata.org/wiki/{row['candidate_qid']}) "
                    f"`{row['candidate_qid']}` | {row['candidate_birth']} | "
                    f"{row['years_apart']} | {row['shared_words']} | "
                    f"{row['external_ids']} |\n")
    print(f"\nwrote reports/spine-name-candidates.tsv and .md")


if __name__ == "__main__":
    main()
