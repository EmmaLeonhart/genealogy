"""Every run: look each super entry point up on Wikidata by its id and, once found, make it a regular entry point.

Emma, 2026-10-06: a super entry point is created in one run, and "the next run, through doing a search, picks it
up and adds it into the regular entry points list". That pick-up was never built: the 7 that had items sat on
Wikidata with no links, in no roster, for days.

    reports/super-entry-points.tsv   key (Geni id, or FS + the FamilySearch id without its dash), label, note, qid
    reports/entry-points-now.tsv     qid, geni_id (blank for a FamilySearch-keyed one; see ledgers._read)

For each row: search `haswbstatement:P2600=<id>` or `P2889=<id>`, write the QID found into `qid`, and append
`qid<TAB>geni_id` to entry-points-now.tsv if the QID is not there yet. Nothing found leaves the row alone, and a
failed request changes nothing.
"""
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUPER = ROOT / "reports" / "super-entry-points.tsv"
NOW = ROOT / "reports" / "entry-points-now.tsv"
UA = {"User-Agent": "genealogy-super-entry-points/1.0 (emma@topazcomputing.com)"}


def find(key):
    prop, value = ("P2889", f"{key[2:6]}-{key[6:]}") if key.startswith("FS") else ("P2600", key)
    url = ("https://www.wikidata.org/w/api.php?format=json&action=query&list=search&srsearch="
           + urllib.parse.quote(f"haswbstatement:{prop}={value}"))
    for attempt in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
                hits = [h["title"] for h in json.load(r)["query"]["search"]]
            return sorted(hits, key=lambda q: int(q[1:]))[0] if hits else ""
        except Exception as exc:  # noqa: BLE001
            print(f"{key}: lookup failed ({exc}), attempt {attempt + 1}")
            time.sleep(5)
    return None


def main():
    lines = SUPER.read_text(encoding="utf-8").splitlines()
    header = lines[0].split("\t")
    if "qid" not in header:
        header.append("qid")
    rows = [dict(zip(header, l.split("\t"))) for l in lines[1:] if l.strip()]
    now_text = NOW.read_text(encoding="utf-8")
    in_now = {l.split("\t")[0] for l in now_text.splitlines()[1:]}
    added = []
    for row in rows:
        q = find(row["key"])
        time.sleep(0.5)
        if q is None:
            continue
        if q:
            row["qid"] = q
        q = row.get("qid", "")
        if q and q not in in_now:
            added.append(f"{q}\t{row['key'] if row['key'].isdigit() else ''}")
            in_now.add(q)
        print(f"{row['key']}\t{row.get('label', '')}\t{q or 'not on Wikidata yet'}")
    SUPER.write_bytes(("\n".join(["\t".join(header)] + ["\t".join(r.get(h, "") for h in header) for r in rows])
                       + "\n").encode("utf-8"))
    if added:
        NOW.write_bytes((now_text.rstrip("\n") + "\n" + "\n".join(added) + "\n").encode("utf-8"))
    print(f"{sum(1 for r in rows if r.get('qid'))} of {len(rows)} super entry points have an item; "
          f"{len(added)} added to entry-points-now.tsv")


if __name__ == "__main__":
    main()
