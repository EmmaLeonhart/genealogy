"""Surnames that are places — the spread Emma asked to see before any rule.

Emma, 2026-08-11, on Aénor of Châtellerault, whose `SURN` is `of Châtellerault`,
whose birthplace field says Châtellerault, and whose Wikidata item carries no
`P734` at all: **"Show me more cases first."** Her chosen option was to pull the
cases where `SURN` looks toponymic and see the spread *before* any rule exists.

**No place-name list is used, because that would be the fuzzy matching this repo
refuses everywhere else.** The evidence comes from the record itself:

* **self-evidencing** — the surname, minus any leading particle, appears in one
  of *that person's own* `PLAC` / `CITY` / `STAE` / `CTRY` strings. That is the
  Aénor signature and it is objective: the record itself says the word is a
  place.
* **particle** — the surname begins `of` / `de` / `van` / `von` / `af` / `di` /
  `du` / `zu` and so on. A list of *particles*, not of places, and it only
  describes a row rather than deciding it.

The two are reported separately and neither is called a toponym detector.

Also carried, for the linked subset: whether Wikidata gives the person a `P734`
at all. Aénor's item does not, and whether that generalises is the question a
`P734` mapping depends on.

Writes `reports/toponym-surn.csv`, one row per `NAME` record carrying a `SURN`
that shows either signal. Offline throughout.

    py scripts/build-toponym-surn-census.py
"""

from __future__ import annotations

import csv
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from genimerge import doubles, wikistore  # noqa: E402

MERGED = REPO_ROOT / "out" / "merged.ged"
PAIRS = REPO_ROOT / "out" / "wikidata" / "p2600-all.tsv"
STORE = REPO_ROOT / "wikidata" / "items"
INDEX = REPO_ROOT / "out" / "wikidata" / "store-index.sqlite3"
OUTPUT = REPO_ROOT / "reports" / "toponym-surn.csv"

#: Territorial particles, several languages. A list of particles, never of
#: places — it labels a row, it does not classify a surname.
PARTICLES = {
    "of", "de", "del", "della", "di", "da", "das", "dos", "du", "des",
    "van", "von", "vom", "der", "den", "ter", "te", "ten",
    "af", "av", "à", "a", "al", "el", "la", "le", "les", "lo",
    "zu", "zur", "im", "auf", "y", "i",
}


def fold(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    return " ".join(text.casefold().replace(",", " ").replace(".", " ").split())


def strip_particle(surn: str) -> tuple[str, str]:
    """(leading particle or '', the rest)."""
    parts = surn.split()
    if len(parts) > 1 and parts[0].casefold() in PARTICLES:
        return parts[0], " ".join(parts[1:])
    return "", surn


def main() -> int:
    print(f"reading {MERGED}", flush=True)

    people: dict[str, dict] = {}
    current: str | None = None
    in_event = False

    with open(MERGED, encoding="utf-8", errors="replace") as handle:
        for line in handle:
            if line.startswith("0 "):
                current = None
                in_event = False
                parts = line.split()
                if len(parts) >= 3 and parts[2] == "INDI":
                    xref = parts[1]
                    if xref.startswith("@I") and xref.endswith("@"):
                        current = xref[2:-1]
                        people[current] = {"surns": [], "places": [], "name": ""}
                continue
            if current is None:
                continue
            record = people[current]
            if line.startswith("1 "):
                tag = line[2:].split(None, 1)[0].strip()
                in_event = tag in {"BIRT", "DEAT", "BURI", "BAPM", "CHR", "RESI"}
                if tag == "NAME" and not record["name"]:
                    record["name"] = line[6:].strip()
                continue
            parts = line.rstrip("\n").split(None, 2)
            if len(parts) < 2:
                continue
            level, tag = parts[0], parts[1]
            value = parts[2].strip() if len(parts) > 2 else ""
            if level == "2" and tag == "SURN" and value:
                record["surns"].append(value)
            elif in_event and value and tag in {"PLAC", "CITY", "STAE", "CTRY"}:
                record["places"].append(value)

    print(f"{len(people):,} people", flush=True)

    qids_for: dict[str, set[str]] = {}
    for qid, geni_id in doubles.load_pairs(PAIRS):
        if geni_id in people:
            qids_for.setdefault(geni_id, set()).add(qid)
    linked = {g: next(iter(q)) for g, q in qids_for.items() if len(q) == 1}
    print(f"{len(linked):,} linked people; reading their claims", flush=True)

    has_p734: dict[str, bool] = {}
    has_p735: dict[str, bool] = {}
    with wikistore.StoreReader(STORE, INDEX) as reader:
        for qid, entity in reader.entities(sorted(set(linked.values()))).items():
            claims = entity.get("claims") or {}
            has_p734[qid] = "P734" in claims
            has_p735[qid] = "P735" in claims

    rows = []
    signals: Counter[str] = Counter()
    particle_counts: Counter[str] = Counter()
    p734_by_signal: dict[str, Counter[str]] = defaultdict(Counter)

    for geni_id, record in people.items():
        if not record["surns"]:
            continue
        folded_places = [fold(p) for p in record["places"]]
        joined = " | ".join(folded_places)
        for surn in dict.fromkeys(record["surns"]):
            particle, rest = strip_particle(surn)
            folded = fold(rest)
            self_evident = bool(folded) and folded in joined
            if not (self_evident or particle):
                continue

            signal = (
                "self-evidencing + particle" if self_evident and particle
                else "self-evidencing" if self_evident
                else "particle only"
            )
            signals[signal] += 1
            if particle:
                particle_counts[particle.casefold()] += 1

            qid = linked.get(geni_id, "")
            if qid in has_p734:
                p734_by_signal[signal]["has P734" if has_p734[qid] else "no P734"] += 1

            rows.append(
                [
                    geni_id,
                    record["name"],
                    surn,
                    particle,
                    rest,
                    signal,
                    "; ".join(dict.fromkeys(record["places"]))[:200],
                    qid,
                    "" if qid not in has_p734 else ("yes" if has_p734[qid] else "no"),
                    "" if qid not in has_p735 else ("yes" if has_p735[qid] else "no"),
                ]
            )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "geni_id", "name", "surn", "particle", "surn_without_particle",
                "signal", "own_places", "qid", "wikidata_has_P734", "wikidata_has_P735",
            ]
        )
        writer.writerows(rows)

    print(f"wrote {OUTPUT} — {len(rows):,} rows")
    print()
    print("by signal:")
    for signal, n in signals.most_common():
        print(f"  {signal:<28} {n:>7,}")
    print()
    print("commonest particles:", dict(particle_counts.most_common(10)))
    print()
    # A rate is not a finding without the rate it is being compared against.
    # 77% carrying no P734 means nothing until we know what share of *all*
    # linked people carry none — the same discipline the QID-band enrichment
    # in reports/link-suspects.md needed.
    base_none = sum(1 for qid in set(linked.values()) if not has_p734.get(qid, False))
    base_total = len(set(linked.values()))
    base_rate = 100.0 * base_none / max(base_total, 1)
    print(f"BASE RATE: {base_none:,} of {base_total:,} linked people carry no P734 "
          f"({base_rate:.1f}%)")
    print()
    print("Wikidata P734, for the linked subset, by signal:")
    for signal in signals:
        c = p734_by_signal[signal]
        total = sum(c.values())
        if total:
            pct = 100.0 * c["no P734"] / total
            print(f"  {signal:<28} has {c['has P734']:>5,}  none {c['no P734']:>5,}  "
                  f"({pct:.0f}% carry no P734, base {base_rate:.0f}%, "
                  f"{pct - base_rate:+.0f} points)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
