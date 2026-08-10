"""Birth-century distribution, Wikidata against Geni — `todo.md` 8b, queue item 8b-i.

Scores a prediction Emma recorded on 2026-08-07, **before** the store existed:
the Geni-linked items on Wikidata *"skew heavily to the 20th and 21st centuries
much as the Geni profiles do, with the 19th ambiguous"*. Written down first so
it can be marked right or wrong rather than confirmed after the fact.

Both sides from primary data on disk, so they are comparable:

* **Wikidata** — P569 over the Geni-linked items in `wikidata/items/`, truthy
  ranks (preferred if any, else normal, never deprecated).
* **Geni** — birth dates in `out/merged.ged`.

**Compared as shares of the *dated* population on each side**, never as shares
of the whole. Date coverage differs sharply between the two, and mixing "how
many have a date" into "which century are they from" would make the better-
covered side look older or younger purely by having fewer blanks. The undated
counts are reported separately for exactly that reason.

Offline throughout: `todo.md` 8b's first line is that nothing here may be
answered by querying Wikidata.
"""

from __future__ import annotations

import io
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from genimerge import wikistore  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
STORE = ROOT / "wikidata" / "items"
MERGED = ROOT / "out" / "merged.ged"


def century_of(year: int) -> str:
    if year <= 0:
        return "BCE"
    return f"{(year - 1) // 100 + 1}00s"


def _truthy_times(entity: dict, prop: str) -> list[str]:
    statements = (entity.get("claims") or {}).get(prop) or []
    live = [s for s in statements if s.get("rank") != "deprecated"]
    chosen = [s for s in live if s.get("rank") == "preferred"] or live
    out = []
    for statement in chosen:
        snak = statement.get("mainsnak") or {}
        if snak.get("snaktype") != "value":
            continue
        value = (snak.get("datavalue") or {}).get("value")
        if isinstance(value, dict) and isinstance(value.get("time"), str):
            out.append(value["time"])
    return out


def _year_of_time(time: str) -> int | None:
    if len(time) < 5:
        return None
    try:
        year = int(time[1:5])
    except ValueError:
        return None
    return -year if time[0] == "-" else year


def wikidata_side() -> tuple[Counter, int, int]:
    """Birth centuries of the Geni-linked stored items."""
    counts: Counter = Counter()
    linked = undated = 0
    for shard in wikistore.shards(STORE):
        for entity in wikistore.read_shard(shard):
            if not wikistore.geni_ids_of(entity):
                continue
            linked += 1
            years = [y for y in (_year_of_time(t) for t in _truthy_times(entity, "P569")) if y is not None]
            if not years:
                undated += 1
                continue
            counts[century_of(years[0])] += 1
    return counts, linked, undated


#: GEDCOM years can carry qualifiers ("ABT 1420", "BET 1400 AND 1410"). The last
#: integer token is the year in every form this corpus uses; a range takes its
#: end, which is what `dates.py` does too.
def _gedcom_year(text: str) -> int | None:
    for token in reversed(text.replace(",", " ").split()):
        if token.isdigit():
            return int(token)
    return None


def geni_side() -> tuple[Counter, int, int]:
    """Birth centuries of the merged tree, straight from the GEDCOM."""
    counts: Counter = Counter()
    people = undated = 0
    in_birt = False
    pending: int | None = None
    with io.open(MERGED, encoding="utf-8") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if line.startswith("0 @I"):
                people += 1
                if pending is None and people > 1:
                    undated += 1
                if pending is not None:
                    counts[century_of(pending)] += 1
                pending, in_birt = None, False
            elif line.startswith("1 BIRT"):
                in_birt = True
            elif line.startswith("1 "):
                in_birt = False
            elif in_birt and line.startswith("2 DATE") and pending is None:
                pending = _gedcom_year(line[7:])
    if people:
        if pending is not None:
            counts[century_of(pending)] += 1
        else:
            undated += 1
    return counts, people, undated


def _sort_key(label: str) -> tuple[int, int]:
    if label == "BCE":
        return (0, 0)
    return (1, int(label[:-2]))


def main() -> int:
    for path in (STORE, MERGED):
        if not path.exists():
            print(f"{path} not found", file=sys.stderr)
            return 1

    print("reading the store...", flush=True)
    wd, wd_linked, wd_undated = wikidata_side()
    print("reading the merge...", flush=True)
    gd, gd_people, gd_undated = geni_side()

    wd_dated = sum(wd.values())
    gd_dated = sum(gd.values())
    labels = sorted(set(wd) | set(gd), key=_sort_key)

    lines = [
        "# Birth centuries — Wikidata against Geni",
        "",
        "Generated by `scripts/build-centuries.py`, offline. `todo.md` 8b.",
        "",
        "**Wikidata** is P569 over the Geni-linked items in the store; **Geni** is",
        "the birth dates in `out/merged.ged`. Shares are of the *dated* population",
        "on each side, never of the whole — date coverage differs sharply, and",
        "mixing that in would make the better-covered side look older or younger",
        "purely by having fewer blanks.",
        "",
        "| | Wikidata (Geni-linked) | Geni (merged tree) |",
        "| --- | ---: | ---: |",
        f"| people | {wd_linked:,} | {gd_people:,} |",
        f"| with a birth date | {wd_dated:,} ({100 * wd_dated / max(1, wd_linked):.1f}%) | "
        f"{gd_dated:,} ({100 * gd_dated / max(1, gd_people):.1f}%) |",
        f"| undated | {wd_undated:,} | {gd_undated:,} |",
        "",
        "## The distribution",
        "",
        "| century | Wikidata | share | Geni | share |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for label in labels:
        w, g = wd.get(label, 0), gd.get(label, 0)
        lines.append(
            f"| {label} | {w:,} | {100 * w / max(1, wd_dated):.1f}% | "
            f"{g:,} | {100 * g / max(1, gd_dated):.1f}% |"
        )

    out = ROOT / "reports" / "centuries.md"
    io.open(out, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")

    print()
    print(f"wikidata: {wd_linked:,} linked, {wd_dated:,} dated")
    print(f"geni    : {gd_people:,} people, {gd_dated:,} dated")
    modern = ("1900s", "2000s")
    print(f"  20th+21st  wikidata {100 * sum(wd[c] for c in modern) / max(1, wd_dated):.1f}%"
          f"   geni {100 * sum(gd[c] for c in modern) / max(1, gd_dated):.1f}%")
    print(f"  19th       wikidata {100 * wd['1800s'] / max(1, wd_dated):.1f}%"
          f"   geni {100 * gd['1800s'] / max(1, gd_dated):.1f}%")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
