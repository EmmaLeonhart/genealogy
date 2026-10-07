"""Export the ancestors of a Wikidata person (via P22 father / P25 mother) as GEDCOM files.

One file per language. Each person's name is their label in that language (falling back to
the `mul` label, then the QID), used as a given name with no surname. Each person gets a
NOTE linking to their Wikidata page.

Usage: python wikidata_to_gedcom.py Q140568870 [--generations 10] [--langs en,zh,ja,ko] [--no-open]
"""
import argparse
import json
import os
import sys
import urllib.parse
import urllib.request

API = "https://www.wikidata.org/w/api.php"
USER_AGENT = "wikidata_to_gedcom/0.1 (https://github.com/; ancestor export script)"
FATHER, MOTHER, SEX = "P22", "P25", "P21"
MALE, FEMALE = {"Q6581097", "Q2449503"}, {"Q6581072", "Q1052281"}


def fetch_entities(qids, langs):
    """Fetch labels and claims for up to 50 QIDs at a time."""
    out = {}
    qids = list(qids)
    for i in range(0, len(qids), 50):
        params = {
            "action": "wbgetentities",
            "ids": "|".join(qids[i:i + 50]),
            "props": "labels|claims",
            "languages": "|".join(langs + ["mul"]),
            "format": "json",
        }
        req = urllib.request.Request(API + "?" + urllib.parse.urlencode(params),
                                     headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.load(resp)
        for qid, ent in data.get("entities", {}).items():
            if "missing" not in ent:
                out[ent.get("id", qid)] = ent
    return out


def claim_targets(ent, prop):
    targets = []
    for claim in ent.get("claims", {}).get(prop, []):
        if claim.get("rank") == "deprecated":
            continue
        value = claim["mainsnak"].get("datavalue", {}).get("value")
        if isinstance(value, dict) and "id" in value:
            targets.append(value["id"])
    return targets


def collect_ancestors(root, generations, langs):
    """Breadth-first walk up father/mother links. Returns {qid: entity}."""
    people, frontier = {}, [root]
    for gen in range(generations + 1):  # gen 0 is the root person
        frontier = [q for q in dict.fromkeys(frontier) if q not in people]
        if not frontier:
            break
        fetched = fetch_entities(frontier, langs)
        people.update(fetched)
        print(f"generation {gen}: {len(fetched)} people", file=sys.stderr)
        if gen == generations:
            break
        frontier = [p for ent in fetched.values()
                    for p in claim_targets(ent, FATHER)[:1] + claim_targets(ent, MOTHER)[:1]]
    return people


def label(ent, lang):
    labels = ent.get("labels", {})
    for code in (lang, "mul"):
        if code in labels:
            return labels[code]["value"]
    return ent["id"]


def to_gedcom(root, people, lang):
    """Build GEDCOM 5.5.1 text for one language."""
    xref = {qid: f"@I{n}@" for n, qid in enumerate(people, 1)}
    families = {}  # (father, mother) -> list of child qids
    for qid, ent in people.items():
        father = next((q for q in claim_targets(ent, FATHER) if q in people), None)
        mother = next((q for q in claim_targets(ent, MOTHER) if q in people), None)
        if father or mother:
            families.setdefault((father, mother), []).append(qid)
    fam_xref = {key: f"@F{n}@" for n, key in enumerate(families, 1)}
    fam_links = {}  # qid -> FAMC/FAMS lines, in family order
    for key, children in families.items():
        for qid in children:
            fam_links.setdefault(qid, []).append(f"1 FAMC {fam_xref[key]}")
        for qid in set(key) - {None}:
            fam_links.setdefault(qid, []).append(f"1 FAMS {fam_xref[key]}")

    lines = ["0 HEAD", "1 SOUR wikidata_to_gedcom", "1 GEDC", "2 VERS 5.5.1",
             "2 FORM LINEAGE-LINKED", "1 CHAR UTF-8", f"1 LANG {lang}",
             f"1 NOTE Ancestors of https://www.wikidata.org/wiki/{root}"]
    for qid, ent in people.items():
        name = label(ent, lang)
        lines += [f"0 {xref[qid]} INDI", f"1 NAME {name}", f"2 GIVN {name}"]
        sex = claim_targets(ent, SEX)
        if sex and sex[0] in MALE:
            lines.append("1 SEX M")
        elif sex and sex[0] in FEMALE:
            lines.append("1 SEX F")
        lines += fam_links.get(qid, [])
        lines.append(f"1 NOTE https://www.wikidata.org/wiki/{qid}")
    for key, children in families.items():
        lines.append(f"0 {fam_xref[key]} FAM")
        if key[0]:
            lines.append(f"1 HUSB {xref[key[0]]}")
        if key[1]:
            lines.append(f"1 WIFE {xref[key[1]]}")
        lines += [f"1 CHIL {xref[c]}" for c in children]
    lines.append("0 TRLR")
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("qid")
    ap.add_argument("--generations", type=int, default=15)
    ap.add_argument("--langs", default="en,zh,ja,ko")
    ap.add_argument("--out", default="output")
    ap.add_argument("--suffix", default="", help="appended to each file name, e.g. -2")
    ap.add_argument("--no-open", action="store_true")
    args = ap.parse_args()
    langs = args.langs.split(",")

    people = collect_ancestors(args.qid, args.generations, langs)
    os.makedirs(args.out, exist_ok=True)
    for lang in langs:
        path = os.path.abspath(os.path.join(args.out, f"{args.qid}_ancestors_{lang}{args.suffix}.ged"))
        with open(path, "w", encoding="utf-8", newline="\r\n") as f:
            f.write(to_gedcom(args.qid, people, lang))
        bare = sum(1 for ent in people.values() if label(ent, lang) == ent["id"])
        print(f"wrote {path} ({len(people)} people, {bare} named only by QID)", file=sys.stderr)
        if not args.no_open and hasattr(os, "startfile"):
            os.startfile(path)


if __name__ == "__main__":
    main()
