"""Her per-person patronymic resolution, run as a measurement: who clears both gates today.

    python scripts/resolve-patronymics.py

**Emma's design, 2026-08-31.** The half this script covers is the one that runs *after* the
patronymic name items exist:

    the parent carries a given name OBJECT              (P735 -> an item)
    that item is among the patronymic item's P144 values
    -> emit  P5056 patronym, with P144 based on pointing at THAT PARENT as a person

Both gates are hard skips in her words -- *"if the father doesn't have a given name object, then
it just doesn't go"*, and *"if the patronymic in question does not have a reference to the certain
given name presence, that's also skipped."* Nothing here falls back to a string.

**This writes no QuickStatements.** It reports who would resolve and what stops the rest, which is
the number that says whether the design reaches anybody yet. She has not asked for a batch.

## Why it is cheap

Of 235,113 people carrying an attested patronymic, **8,277** have a father who has a Wikidata item
at all -- everyone else fails gate one before any lookup. Those 8,277 share **2,666** distinct
father items, so the whole question is ~54 batched `wbgetentities` requests. The 226,836 without a
linked father are not a failure of the design; they are the people the pipeline has not reached.

Writes `reports/patronymic-resolution.tsv`.
"""

import collections
import csv
import io
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "src"))

import namemodel as nm                                              # noqa: E402
from genimerge.wikidata import _http_fetch, require_agent           # noqa: E402

LABELS = ROOT / "reports" / "derived-labels.csv"
FAMILY = ROOT / "reports" / "derived-family.csv"
PLAN = ROOT / "reports" / "patronymic-items-to-create.tsv"
P2600 = ROOT / "out" / "wikidata" / "p2600-all.tsv"
LEDGER = ROOT / "reports" / "garborg-qids.tsv"
CACHE = ROOT / "out" / "wikidata" / "cache" / "father-given-names.json"
OUT = ROOT / "reports" / "patronymic-resolution.tsv"

csv.field_size_limit(1 << 30)


def qid_index():
    out = {}
    with io.open(P2600, encoding="utf-8") as fh:
        for line in fh:
            p = line.rstrip("\n").split("\t")
            if len(p) >= 2:
                out.setdefault(p[1], p[0])
    with io.open(LEDGER, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            if r.get("geni_id") and r.get("qid"):
                out.setdefault(r["geni_id"], r["qid"])
    return out


def given_names(qids):
    """`{qid: [given-name item, ...]}` — cached, because these change slowly and the fetch is
    the only network in the script."""
    cache = {}
    if CACHE.exists():
        cache = json.loads(CACHE.read_text(encoding="utf-8"))
    todo = sorted(q for q in qids if q not in cache)
    if todo:
        ua = {"User-Agent": require_agent()}
        for k in range(0, len(todo), 50):
            chunk = todo[k:k + 50]
            url = ("https://www.wikidata.org/w/api.php?action=wbgetentities&format=json"
                   "&props=claims&ids=" + "|".join(chunk))
            ent = json.loads(_http_fetch(url, headers=ua)).get("entities", {})
            for q, v in ent.items():
                vals = []
                for st in (v.get("claims", {}) or {}).get("P735", []):
                    dv = st["mainsnak"].get("datavalue", {}).get("value", {})
                    if isinstance(dv, dict) and dv.get("id"):
                        vals.append(dv["id"])
                cache[q] = vals
            for q in chunk:
                cache.setdefault(q, [])
            sys.stderr.write(f"\r  fetched {min(k + 50, len(todo)):,}/{len(todo):,}")
        sys.stderr.write("\n")
        CACHE.parent.mkdir(parents=True, exist_ok=True)
        CACHE.write_text(json.dumps(cache), encoding="utf-8")
    return cache


def main():
    label, father = {}, {}
    with io.open(LABELS, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            label[r["geni_id"]] = r.get("label_en") or r.get("label_mul") or ""
    with io.open(FAMILY, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            f = (r.get("father") or "").strip()
            if f:
                father[r["geni_id"]] = f

    # the patronymic items' P144 values, from the plan
    p144 = {}
    with io.open(PLAN, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            p144[r["token"]] = [q for q in (r["p144_targets"] or "").split() if q]

    qid = qid_index()

    # gate one: the father must have an item, then that item must carry P735
    cases = []
    for g, lab in label.items():
        f = father.get(g, "")
        dad = label.get(f, "")
        if not dad or f not in qid:
            continue
        for tok in lab.split():
            if not nm.PATRONYMIC.match(tok):
                continue
            if nm.patronymic_or_surname(tok, dad) != "patronymic":
                continue
            cases.append((g, tok.casefold(), f, qid[f]))
            break
    print(f"{len(cases):,} people whose father has an item -- gate one")

    names = given_names({q for _, _, _, q in cases})

    rows, tally = [], collections.Counter()
    for g, tok, f, fq in cases:
        fathers_given = names.get(fq, [])
        targets = p144.get(tok, [])
        if not fathers_given:
            status = "father has no P735 given name object"
        elif not targets:
            status = "patronymic item has no P144 derivation"
        elif set(fathers_given) & set(targets):
            status = "RESOLVES"
        else:
            status = "P735 not among the patronymic's P144 values"
        tally[status] += 1
        rows.append({"geni_id": g, "person": label.get(g, ""), "token": tok,
                     "father_geni": f, "father_qid": fq,
                     "father_p735": " ".join(fathers_given),
                     "p144_targets": " ".join(targets),
                     "status": status, "person_qid": qid.get(g, "")})

    with io.open(OUT, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, delimiter="\t", fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)

    for status, n in tally.most_common():
        print(f"  {n:>6,}  {status}")
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
