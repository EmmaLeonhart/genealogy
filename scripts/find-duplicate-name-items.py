"""Which competing name items look like Wikidata DUPLICATES rather than real distinctions?

    python scripts/find-duplicate-name-items.py

`reports/name-ambiguity-causes.md` sorted the 769 still-ambiguous name strings into four
buckets and found **57 where the two items carry identical descriptions** — `Schloss` is
`Q105540652` *family name* and `Q37300956` *family name*, with nothing between them. Its
verdict: *"These look like Wikidata duplicates. Worth reporting upstream rather than choosing
between."*

That report named four examples and no list, so this recomputes the bucket in full and writes
it where Emma can act on it. She asked on 2026-08-31 for one file holding *"these merges and
the wikidata duplicates and all the other things we went over"*, to work through by hand.

**Identical description is evidence, not proof.** Two family-name items both described
`family name` may still be two names — the description is simply too thin to tell. So this
writes merge *candidates* to look at, and says so; it does not resolve the ambiguity and does
not feed the name plan.

**A pair with no description on either side is NOT counted.** Two empty strings are trivially
equal and say nothing at all, which would have been the largest and emptiest bucket.

Reads `reports/name-ambiguity-resolved.csv`. Writes `reports/duplicate-name-items.tsv`.
"""

import csv
import io
import json
import pathlib
import sys
import time
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "reports" / "name-ambiguity-resolved.csv"
OUT = ROOT / "reports" / "duplicate-name-items.tsv"

API = "https://www.wikidata.org/w/api.php"
UA = "geni-name-dupes/1.0 (emma@topazcomputing.com)"
BATCH = 50          # wbgetentities takes 50 ids; do not fan out one request per item
PAUSE = 0.4         # be polite about the rate, per CLAUDE.md


def ambiguous_pairs():
    """`(kind, name, occurrences, [qids])` for every row with more than one candidate."""
    out = []
    with io.open(SRC, encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            qids = [q.strip() for q in (row.get("qid") or "").split("|") if q.strip()]
            if len(qids) > 1:
                out.append((row["kind"], row["name"], row["occurrences"], qids))
    return out


def descriptions(qids):
    """`{qid: english description}` for every id, batched."""
    out = {}
    ids = sorted(set(qids))
    for i in range(0, len(ids), BATCH):
        chunk = ids[i:i + BATCH]
        url = (f"{API}?action=wbgetentities&ids={'|'.join(chunk)}"
               "&props=descriptions|labels&languages=en&format=json")
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=60) as fh:
            data = json.load(fh)
        for qid, entity in (data.get("entities") or {}).items():
            if "missing" in entity:
                continue
            desc = (entity.get("descriptions", {}).get("en") or {}).get("value", "")
            label = (entity.get("labels", {}).get("en") or {}).get("value", "")
            out[qid] = (desc, label)
        sys.stderr.write(f"  {min(i + BATCH, len(ids))}/{len(ids)}\n")
        time.sleep(PAUSE)
    return out


def main():
    pairs = ambiguous_pairs()
    every = [q for _k, _n, _o, qids in pairs for q in qids]
    sys.stderr.write(f"{len(pairs)} ambiguous strings, {len(set(every))} distinct items\n")
    info = descriptions(every)

    rows = []
    for kind, name, occurrences, qids in pairs:
        described = [(q, info.get(q, ("", ""))[0]) for q in qids]
        # Every candidate must HAVE a description and they must all agree. Two blanks are
        # equal and mean nothing, which is why the empty case is excluded rather than
        # counted -- it would be the biggest bucket and the least informative.
        texts = {d for _q, d in described}
        if len(texts) == 1 and all(d for _q, d in described):
            rows.append({
                "kind": kind,
                "name": name,
                "occurrences": occurrences,
                "description": described[0][1],
                "qids": " | ".join(qids),
            })

    rows.sort(key=lambda r: -int(r["occurrences"] or 0))
    with io.open(OUT, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(
            fh, delimiter="\t",
            fieldnames=["kind", "name", "occurrences", "description", "qids"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {OUT}")
    print(f"  {len(rows)} name strings whose candidate items share one description")


if __name__ == "__main__":
    main()
