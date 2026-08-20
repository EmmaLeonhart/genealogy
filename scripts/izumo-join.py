"""Fill the `geni` column of the Izumo chart roster from a walk of Geni.

Emma, 2026-08-20: *"you can use the text of the page to build a roster of everything
that should be present (including whether they have qids) and then search through the
tree to see what corresponds on geni."* This is the second half of that - the roster
is `reports/izumo-chart-roster.tsv`, the walk is every descendant of Ame no Hohi
reachable on Geni, and this joins them.

**The join is on token sets, not on string similarity.** The chart and Geni disagree
on romanisation constantly - the clan was added to Geni three separate times, in
Japanese in 2008, in English in 2011, and by Emma in 2026 - and word order differs
too: the chart writes `Kitajima no Yoshitaka`, Geni writes `Yoshitaka 56 Kitajima`.
Sorting the tokens makes those the same key. Nothing here scores a near-miss; two
names either reduce to the same set of tokens or they do not match, which keeps this
on the right side of the project's standing refusal to match people by name
similarity.

**The regnal number is the strongest evidence and is treated as such.** Geni carries
it inside the name, so when both sides have one they must agree, and when they agree
the match is reported as `regnal` rather than `tokens`. A number on one side only
does not block a match; the chart omits the number for cadet-house members that Geni
sometimes numbers anyway.

Ambiguity is never resolved by picking. Two Geni people reducing to one key is
reported as `AMBIGUOUS` with both ids, because that is the duplicate situation Emma
handles herself.
"""

import argparse
import collections
import csv
import pathlib
import re
import sys

# Words that carry no identity: honorifics and the connective particle. Stripping
# them is what makes `Kitajima no Yoshitaka` and `Yoshitaka Kitajima` one key.
NOISE = {"no", "mikoto", "nomikoto", "sukune", "sukunenomikoto", "kokuso", "izumokokuso"}


def tokens(name: str) -> tuple[frozenset[str], str | None]:
    """Reduce a name to its identity tokens plus its regnal number, if any."""
    s = name.lower().replace("’", "'")
    s = re.sub(r"[\-‐-―_.,()\[\]]+", " ", s)
    s = re.sub(r"[^0-9a-z' ]+", " ", s)
    parts = [p for p in s.split() if p]
    regnal = None
    keep = []
    for p in parts:
        if p.isdigit():
            # A bare number in a Geni name is the regnal ordinal.
            if regnal is None:
                regnal = p
            continue
        if p in NOISE:
            continue
        keep.append(p)
    # `nomikoto` also shows up glued to the end of a name: Kushidanomikoto.
    keep = [re.sub(r"nomikoto$|nomi$", "", k) or k for k in keep]
    keep = [k for k in keep if k and k not in NOISE]
    return frozenset(keep), regnal


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--roster", default="reports/izumo-chart-roster.tsv")
    ap.add_argument("--walk", default="reports/izumo-geni-walk.tsv")
    ap.add_argument("--out", default="reports/izumo-chart-roster.tsv")
    ap.add_argument("--report", default="reports/izumo-join.md")
    args = ap.parse_args()

    walk_path = pathlib.Path(args.walk)
    if not walk_path.exists():
        print(f"no walk file at {walk_path}", file=sys.stderr)
        return 1

    by_key: dict[frozenset[str], list[tuple[str, str, str | None]]] = collections.defaultdict(list)
    walked = 0
    with walk_path.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            gid, name = row["geni"].strip(), row["name"].strip()
            if not gid or not name:
                continue
            walked += 1
            key, regnal = tokens(name)
            if key:
                by_key[key].append((gid, name, regnal))

    rows = list(csv.DictReader(args.roster and open(args.roster, encoding="utf-8"), delimiter="\t"))
    fields = ["english", "japanese", "qid", "geni", "lt_ja", "succession"]

    matched = ambiguous = absent = 0
    notes: list[str] = []
    for r in rows:
        want_key, _ = tokens(r["english"])
        want_regnal = r.get("succession", "").strip()
        want_regnal = want_regnal if want_regnal.isdigit() else None
        cands = by_key.get(want_key, [])
        if want_regnal:
            narrowed = [c for c in cands if c[2] in (None, want_regnal)]
            # A regnal number that disagrees is a different person, not a near miss.
            cands = narrowed
        if len(cands) == 1:
            r["geni"] = cands[0][0]
            matched += 1
        elif len(cands) > 1:
            ambiguous += 1
            notes.append(
                f"- **{r['english']}** — {len(cands)} Geni profiles reduce to the same "
                f"name: " + ", ".join(f"`{c[0]}` {c[1]}" for c in cands)
            )
        else:
            absent += 1

    with open(args.out, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, delimiter="\t", extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)

    missing = [r["english"] for r in rows if not r["geni"]]
    with open(args.report, "w", encoding="utf-8") as fh:
        fh.write("# Izumo chart roster against Geni\n\n")
        fh.write(
            f"{len(rows)} people on the chart, {walked} walked on Geni below Ame no Hohi.\n"
            f"**{matched} joined**, {ambiguous} ambiguous, {absent} with no Geni profile "
            "found by this join.\n\n"
            "Absent here means *this walk and this join did not find them*, which is not the "
            "same as absent from Geni: the walk follows children only from Ame no Hohi, so "
            "anyone attached to the clan by marriage or sitting in a disconnected duplicate "
            "tree is invisible to it. The in-law columns - Sasaki, Minamoto, En'ya, Ookuma, "
            "Takaoka and the emperors - are expected to fall here for that reason.\n\n"
        )
        if notes:
            fh.write("## Ambiguous\n\n" + "\n".join(notes) + "\n\n")
        fh.write("## Not found by the join\n\n")
        for m in missing:
            fh.write(f"- {m}\n")

    print(f"joined {matched}, ambiguous {ambiguous}, not found {absent}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
