"""Build what each item SHOULD be, fetch what it IS, and diff the two.

    BOT_CONTACT=you@example.com python scripts/model-vs-reality.py [--refetch]

**Emma, 2026-08-24:** *"we are supposed to generate complete models of what the wikidata items
should be and compare with the reality for the quickstatements modelling stuff."*

The method it replaces was: emit statements, and find out what was wrong when she ran them. That
cost four corrective rounds in one afternoon — the married name as an alias instead of the primary
label, `mul` holding the wrong form, `ja` left stale against a label she had fixed by hand,
`P7452` *usual forename* on people with no middle name, and the married-name role on seven men.
Every one would have shown in a diff before anything was emitted.

## The three columns, and why the third is the point

* **missing** — the model has it, the item does not. This is the only column a batch should ever
  be projected from: a statement gets emitted because the diff says it is absent, and for no other
  reason.
* **extra** — the item has it, the model does not. Usually Emma's hand-work. **Never touched.**
  `CLAUDE.md`: *"the entire purpose of this is to add"*, and she edits continuously.
* **conflict** — both hold the property with different values. **A modelling mistake shows up here
  as a pattern.** Seven men conflicting on the same qualifier is one rule that is wrong, not seven
  separate errors, and that is exactly the signal the old method could only produce by Emma running
  a batch and reading the damage.

## What is modelled, and what is deliberately not

Modelled: `P31` *instance of*, `P21` *sex or gender*, `P2600` *Geni.com profile ID*, `P569`/`P570`
dates, the four relationships `P22`/`P25`/`P26`/`P40`, and the **full name model** through
`scripts/namemodel.py` — `P735` with `P1545`/`P7452`/`P3831`, `P5056` with `P144`, `P734` with its
role, `P1449`. The name model is where every one of the four corrective rounds happened, so it is
the part that most needs a diff.

**Labels are compared but never proposed as changes.** `Len`/`Lmul` *replace*, and `CLAUDE.md`
records `Q467497` labelled *Arne Garborg* on Wikidata against our derived *Aadne (Arne) Eivindson
Garborg* — emitting ours would overwrite a better label with a Geni display string. A label
difference is reported and nothing more.

**Freshness matters and is enforced.** `--refetch` pulls every ledger item again through
`genimerge.wikidata.full_entities`, the sanctioned batched client. Without it the cached
`out/model-vs-reality-items.json` is used and its age is printed, because
`CLAUDE.md` § *Emma edits the tree and the items BY HAND, continuously* means a stale snapshot
produces a diff that proposes undoing her work.

Writes `reports/model-vs-reality.tsv` and prints the pattern summary.
"""
from __future__ import annotations

import argparse
import collections
import csv
import json
import os
import re
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
csv.field_size_limit(1 << 30)
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "src"))
R = ROOT / "reports"
ITEMS = ROOT / "out" / "model-vs-reality-items.json"

HUMAN = "Q5"
#: `Q524158` *kami*: where the item already says so, the model says so too rather than
#: asserting `Q5` *human* at a divine descent. Emma, 2026-08-26.
KAMI = "Q524158"
SEX = {"M": "Q6581097", "F": "Q6581072"}
#: Relationship properties, and the column of ours each faces.
RELS = (("P22", "father"), ("P25", "mother"), ("P26", "spouses"), ("P40", "children"))


def split(cell):
    return [x.strip() for x in re.split(r"[,;|]", cell or "") if x.strip()]


def value_of(snak):
    """The comparable value of a mainsnak: a QID, a string, a text, or a time+precision.

    **Monolingual text is `{"language": ..., "text": ...}` and must be unwrapped.** Returning
    the JSON blob made every `P1449` *nickname* look like a conflict -- `Benedicta` against
    `{"language": "en", "text": ...}` -- five of them, which read exactly like the systematic
    modelling error this file exists to surface. It was the comparator.

    **A time carries its own precision and comparing the ISO string ignores it.** Wikidata
    writes `+0874-00-00` for a year and `+0874-07-01` for a day, and `+1568-01-01` is very often
    a year that was entered as a date. `CLAUDE.md` is emphatic that a date parser which quietly
    narrows is how this project loses data; a date COMPARATOR that quietly widens is the same
    error pointing the other way, so the precision travels with the value and
    `same_time` decides what "equal" means.
    """
    dv = snak.get("datavalue", {})
    v = dv.get("value")
    if isinstance(v, dict):
        if v.get("id"):
            return v["id"]
        if v.get("time"):
            return f'{v["time"].split("T")[0]}/{v.get("precision", 11)}'
        if "text" in v:
            return v["text"]
        return json.dumps(v, sort_keys=True)
    return v if isinstance(v, str) else json.dumps(v, sort_keys=True)


#: Wikidata precision: 9 = year, 10 = month, 11 = day.
def same_time(a, b):
    """Two `+YYYY-MM-DD/precision` values that agree as far as BOTH claim to know.

    A model saying `+0874-07-01` day-precision and an item saying `+0874-00-00`
    year-precision do not disagree -- the item simply knows less. Only the shared prefix is
    compared, so a real disagreement (1260-10-15 against 1260-10-05) still shows and a
    difference in what is known does not.
    """
    try:
        (ta, pa), (tb, pb) = a.rsplit("/", 1), b.rsplit("/", 1)
        p = min(int(pa), int(pb))
    except ValueError:
        return a == b
    ya, ma, da = ta[:5], ta[6:8], ta[9:11]
    yb, mb, db = tb[:5], tb[6:8], tb[9:11]
    try:
        na, nb = int(ya), int(yb)
    except ValueError:
        return a == b
    # **Precision below 9 is coarser than a year and must be compared as such.** 6 is a
    # millennium, 7 a CENTURY, 8 a decade. Comparing year strings against a century-precision
    # value manufactured two conflicts that were not: Rozala at `+0952/9` against `+1000/7`
    # and Svantepolk at `+1225/9` against `+1250/7` are each one century, agreeing.
    if p <= 6:
        return na // 1000 == nb // 1000
    if p == 7:
        return (na - 1) // 100 == (nb - 1) // 100
    if p == 8:
        return na // 10 == nb // 10
    if ya != yb:
        return False
    if p == 9:
        return True
    if ma != mb:
        return False
    return True if p <= 10 else da == db


def fetch(qids, dest=None):
    from genimerge.wikidata import WikidataClient
    if not os.environ.get("BOT_CONTACT", "").strip():
        sys.exit("BOT_CONTACT is not set; Wikimedia answers an empty User-Agent with a bare 403")
    client = WikidataClient(ROOT / "out" / "wikidata" / "livecache")
    out = {}
    ids = sorted(set(qids))
    for i in range(0, len(ids), 50):
        batch = ids[i:i + 50]
        # `full_entities` already returns the entities dict -- unwrapping "entities" a second
        # time silently yields {} and the diff then reports every person as ITEM NOT FETCHED,
        # which reads like a network problem rather than a bug two lines up.
        out.update(client.full_entities(batch))
        print(f"  fetched {min(i + 50, len(ids))}/{len(ids)}", flush=True)
    dest = Path(dest or ITEMS)
    dest.parent.mkdir(parents=True, exist_ok=True)
    json.dump(out, open(dest, "w", encoding="utf-8"), ensure_ascii=False)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--roster", default=str(R / "garborg-qids.tsv"), metavar="TSV",
                    help="the qid<->geni_id roster to diff. Defaults to the Garborg ledger. "
                         "Accepts either column naming: `qid`+`geni_id` as the ledger has it, "
                         "or `qid`+`geni_ids` as the Izumo and Tanba roster files do.")
    ap.add_argument("--items", default=str(ITEMS), metavar="JSON",
                    help="where the fetched items live. Give a different path per roster, so "
                         "one roster's snapshot is never read as another's.")
    ap.add_argument("--out", default=str(R / "model-vs-reality.tsv"), metavar="TSV",
                    help="where the diff goes.")
    ap.add_argument("--refetch", action="store_true",
                    help="pull every ledger item again. Without it the cached snapshot is used "
                         "and its age is printed -- a stale one produces a diff that proposes "
                         "undoing Emma's hand-work.")
    args = ap.parse_args()

    items_path = Path(args.items)
    ledger = {}
    with open(args.roster, encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            qid = (row.get("qid") or "").strip()
            if not qid.startswith("Q"):
                continue
            # `geni_id` on the Garborg ledger, `geni_ids` (semicolon-joined) on the roster
            # files. One item may carry several profiles; each gets its own diff row, because
            # `CLAUDE.md` says a second Geni id on one item is ordinary rather than a conflict
            # and both are equally the subject of the same statements.
            for g in re.split(r"[;,| ]+", row.get("geni_id") or row.get("geni_ids") or ""):
                if g.strip().isdigit():
                    ledger[g.strip()] = qid
    print(f"{len(ledger)} people in {Path(args.roster).name}")

    if args.refetch or not items_path.exists():
        print("fetching full items through genimerge.wikidata.full_entities ...")
        items = fetch(ledger.values(), items_path)
    else:
        items = json.load(open(items_path, encoding="utf-8"))
        age = (time.time() - items_path.stat().st_mtime) / 3600
        print(f"using the cached snapshot, {age:.1f} hours old -- pass --refetch to renew. "
              f"Emma edits by hand continuously, so an old one can propose undoing her work.")
    print(f"{len(items)} items held")

    facts, labels, fam, fields = {}, {}, {}, {}
    with open(R / "derived-facts.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["geni_id"] in ledger:
                facts[row["geni_id"]] = row
    with open(R / "derived-labels.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["geni_id"] in ledger:
                labels[row["geni_id"]] = row
    with open(R / "derived-family.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            fam[row["geni_id"]] = row
    with open(R / "display-names.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["geni_id"] in ledger and row["geni_id"] not in fields:
                fields[row["geni_id"]] = {k: row.get(k, "") for k in
                                          ("givn", "surn", "nick", "marnm")}

    from namemodel import load_plan, statements_for
    plan = load_plan()

    rows, patterns = [], collections.Counter()
    for geni, qid in sorted(ledger.items()):
        item = items.get(qid)
        if not item or "missing" in item:
            rows.append({"geni_id": geni, "qid": qid, "name": "", "property": "",
                         "verdict": "ITEM NOT FETCHED", "model": "", "reality": ""})
            continue
        f_ = facts.get(geni, {})
        claims = item.get("claims", {})
        live_p31 = {value_of(st.get("mainsnak", {})) for st in claims.get("P31", [])
                    if st.get("rank") != "deprecated"}

        # ---- the model ---------------------------------------------------------------
        model = collections.defaultdict(set)
        model["P31"].add(KAMI if KAMI in live_p31 else HUMAN)
        if f_.get("sex") in SEX:
            model["P21"].add(SEX[f_["sex"]])
        model["P2600"].add(geni)
        for prop, key, pkey in (("P569", "birth_date_iso", "birth_date_precision"),
                                ("P570", "death_date_iso", "death_date_precision")):
            if f_.get(key):
                model[prop].add(f'{f_[key].split("T")[0]}/{f_.get(pkey) or 11}')
        mine = fam.get(geni, {})
        for prop, col in RELS:
            for other in split(mine.get(col)):
                if other in ledger:
                    model[prop].add(ledger[other])
        # the name model, through the same code the emitter uses
        label = (labels.get(geni, {}).get("label_en")
                 or labels.get(geni, {}).get("label_mul") or "")
        dad = split(mine.get("father"))
        try:
            lines, _notes = statements_for(
                label, plan, geni,
                father_qid=ledger.get(dad[0]) if dad else None,
                fields=fields.get(geni), sex=f_.get("sex", ""))
            for prop, value, _quals in lines:
                model[prop].add(value)
        except Exception as exc:                                   # noqa: BLE001
            rows.append({"geni_id": geni, "qid": qid, "name": label, "property": "(name model)",
                         "verdict": "MODEL FAILED", "model": str(exc)[:80], "reality": ""})

        # ---- the reality -------------------------------------------------------------
        real = collections.defaultdict(set)
        for prop, sts in claims.items():
            for st in sts:
                if st.get("rank") == "deprecated":
                    continue
                v = value_of(st.get("mainsnak", {}))
                if v:
                    real[prop].add(v)

        # ---- the diff ----------------------------------------------------------------
        for prop in sorted(set(model) | set(real)):
            m, x = model.get(prop, set()), real.get(prop, set())
            if not m and not x:
                continue
            if m and not x:
                verdict = "missing"
            elif x and not m:
                verdict = "extra"
            elif m == x:
                continue
            elif m & x:
                verdict = "missing" if m - x else "extra"
            elif prop in ("P569", "P570") and any(
                    same_time(a, b) for a in m for b in x):
                # Agreeing as far as both claim to know is agreement, not conflict.
                continue
            else:
                verdict = "CONFLICT"
            patterns[(prop, verdict)] += 1
            rows.append({"geni_id": geni, "qid": qid, "name": label, "property": prop,
                         "verdict": verdict,
                         "model": ";".join(sorted(m - x)) or ";".join(sorted(m)),
                         "reality": ";".join(sorted(x - m)) or ";".join(sorted(x))})

    with open(args.out, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter="\t")
        w.writeheader()
        w.writerows(rows)

    tally = collections.Counter(r["verdict"] for r in rows)
    print(f"\n{len(rows):,} differences over {len(ledger)} people\n")
    for v, n in tally.most_common():
        print(f"   {n:>5,}  {v}")

    print("\nBY PROPERTY -- a CONFLICT repeated across people is ONE RULE that is wrong,\n"
          "not N separate errors. That is the whole reason for this file:\n")
    print(f"   {'property':<10}{'missing':>9}{'extra':>8}{'CONFLICT':>10}")
    props = sorted({p for p, _v in patterns}, key=lambda p: -sum(
        patterns[(p, v)] for v in ("missing", "extra", "CONFLICT")))
    for p in props:
        print(f"   {p:<10}{patterns[(p,'missing')]:>9,}{patterns[(p,'extra')]:>8,}"
              f"{patterns[(p,'CONFLICT')]:>10,}")
    print(f"\nwrote {Path(args.out).resolve().relative_to(ROOT)}")
    print("NOTHING IS EMITTED. A batch is a projection of the `missing` column and of "
          "nothing else.")


if __name__ == "__main__":
    main()
