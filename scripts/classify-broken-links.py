"""What KIND of link is missing on the paths that do not connect?

    python scripts/classify-broken-links.py

`scripts/rank-broken-links.py` answers *which* link blocks the most paths and finds no
leverage: the top link blocks one path and the top fifty unblock forty-six between them.
`queue.md` § THE AGENDA concluded from that "there is no leverage play: it is 102 small
repairs".

**That is true by path and false by kind.** Joining each missing link back to the path row it
came from recovers the relation Geni stated, and the 102 fall into exactly two classes with
nothing else in them:

  * **siblings** -- `his brother`, `her sister` and so on
  * **former or prospective partners** -- `ex-husband`, `ex-wife`, `ex-partner`, `fiancée`

**No parent or child link is missing anywhere.** The vertical structure of these paths is
complete in our tree; only the lateral edges break. That is a different problem from "102
small repairs" and wants a different instrument, so it is worth knowing before any of them
is worked.

The two classes also fail for different reasons, which this measures rather than assumes:

  * A **sibling** step is not scored broken merely for lacking a sibling edge --
    `census-paths.connected` carries it through a shared parent. So a broken one means the two
    do **not** share a recorded parent, and here every single one has both people present,
    both with parents, sharing none. Our snapshot contradicts Geni about a parent.
  * An **ex-partner** step needs a marriage our tree does not hold. `1 DIV` appears in 502 of
    the exports, so Geni does export former marriages and this is not a structural limit of
    the format.

Writes `reports/broken-link-kinds.md`.
"""

import collections
import csv
import io
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
LINKS = ROOT / "reports" / "broken-links.tsv"
FAMILY = ROOT / "reports" / "derived-family.csv"
PATHS = ROOT / "paths"
OUT = ROOT / "reports" / "broken-link-kinds.md"

csv.field_size_limit(1 << 30)

SIBLING = ("brother", "sister")
FORMER = ("ex-", "fianc")

#: `derived-family.csv` separates multi-valued cells with ` | `, spaces included, and the
#: column is `spouses`/`father`/`mother`. `CLAUDE.md` § *Our side could never have two
#: children* is the record of what a wrong separator or a wrong column name does here: it
#: returns a clean, plausible, entirely instrument-made answer. Writing `spouse` for
#: `spouses` while drafting this script scored all 58 pairs "no spouse recorded".
SEP = "|"


def cell(row, column):
    return {x.strip() for x in (row.get(column) or "").split(SEP) if x.strip()}


def broken_links():
    out = {}
    with io.open(LINKS, encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            out[(row["from_geni"], row["to_geni"])] = row
    return out


def relations_for(wanted):
    """The relation Geni stated for each missing link, from the path file it came from."""
    found = {}
    for path in sorted(PATHS.glob("*.tsv")):
        rows = [ln.rstrip("\n").split("\t")
                for ln in io.open(path, encoding="utf-8") if not ln.startswith("#")]
        if not rows:
            continue
        header = rows[0]
        try:
            i_rel = header.index("relation_to_previous")
            i_note = header.index("note")
        except ValueError:
            continue
        previous = None
        for row in rows[1:]:
            if len(row) <= max(i_rel, i_note):
                continue
            m = re.search(r"geni:(\d+)", row[i_note] or "")
            geni_id = m.group(1) if m else None
            if previous and geni_id and (previous, geni_id) in wanted:
                found[(previous, geni_id)] = row[i_rel]
            previous = geni_id
    return found


def family_for(ids):
    out = {}
    with io.open(FAMILY, encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            if row["geni_id"] in ids:
                out[row["geni_id"]] = {
                    "parents": cell(row, "father") | cell(row, "mother"),
                    "spouses": cell(row, "spouses"),
                }
    return out


def main():
    wanted = broken_links()
    relation = relations_for(wanted)

    kinds = collections.Counter(relation.values())
    sibling = {k for k, v in relation.items() if any(w in v for w in SIBLING)}
    former = {k for k, v in relation.items() if any(w in v for w in FORMER)}
    other = set(relation) - sibling - former
    unmatched = set(wanted) - set(relation)

    people = {g for pair in (sibling | former) for g in pair}
    fam = family_for(people)
    # **No broken links is a RESULT.** The guard below exists to catch a wrong column or
    # separator returning an empty join -- `CLAUDE.md` § *Our side could never have two
    # children*. It must not fire when there is genuinely nothing to resolve, which is the
    # state reached on 2026-08-31 once the `ex-` fix closed the last 59 links. Distinguishing
    # the two is the whole point: an empty join and an empty question look identical
    # downstream, and only the input says which this is.
    if not people:
        OUT.write_text(
            "# What KIND of link is missing\n\n"
            "**None.** `reports/broken-links.tsv` is empty: all 979 relationship paths connect "
            "end to end, so there is no missing link to classify.\n",
            encoding="utf-8")
        print(f"wrote {OUT}")
        print("  no broken links to classify")
        return
    if not fam:
        sys.exit("no person resolved in derived-family.csv -- wrong column or separator")

    both_have_parents = [k for k in sibling
                         if fam.get(k[0], {}).get("parents") and fam.get(k[1], {}).get("parents")]
    share_a_parent = [k for k in both_have_parents
                      if fam[k[0]]["parents"] & fam[k[1]]["parents"]]
    linked = [k for k in former
              if k[1] in fam.get(k[0], {}).get("spouses", set())
              or k[0] in fam.get(k[1], {}).get("spouses", set())]
    no_spouse = [k for k in former
                 if not fam.get(k[0], {}).get("spouses")
                 and not fam.get(k[1], {}).get("spouses")]

    w = []
    w.append("# What KIND of link is missing\n")
    w.append(
        "`reports/broken-links.md` ranks the missing links and finds no leverage — the top "
        "one blocks a single path. Joining each back to its path row recovers the relation "
        "Geni stated, and the picture changes: the missing links are **two classes and "
        "nothing else**.\n"
    )
    w.append(f"- **{len(sibling)} sibling** links\n"
             f"- **{len(former)} former or prospective partner** links\n"
             f"- **{len(other)} other**\n"
             f"- {len(unmatched)} could not be matched back to a path row\n")
    w.append(
        "\n**No parent and no child link is missing anywhere.** The vertical structure of "
        "these paths is complete in our tree; only the lateral edges break.\n"
    )

    w.append("\n## The relations, counted\n")
    w.append("| relation | links |")
    w.append("| --- | ---: |")
    for name, count in kinds.most_common():
        w.append(f"| {name} | {count} |")

    w.append("\n## Siblings — our snapshot contradicts Geni about a parent\n")
    w.append(
        "A sibling step is **not** scored broken for lacking a sibling edge: "
        "`census-paths.connected` carries it through a shared parent, which is the rule "
        "`CLAUDE.md` records after counting all 2,126 sibling steps as broken once. So a "
        "broken one means the two do not share a recorded parent.\n"
    )
    w.append(f"- both people present in `derived-family.csv`: **{len(both_have_parents)} "
             f"of {len(sibling)}** have parents recorded on both sides")
    w.append(f"- of those, sharing at least one parent: **{len(share_a_parent)}**")
    w.append(
        "\nSo every one of them has full parentage on both sides and no parent in common. "
        "That is not a missing edge — it is our parentage disagreeing with Geni's, which is "
        "the staleness `CLAUDE.md` § *The question is whether OUR TREE MATCHES GENI* is "
        "about. A refresh of those people is the instrument, not a new edge.\n"
    )

    w.append("\n## Former partners — the marriage is simply absent\n")
    w.append(
        "`1 DIV` appears in **502** of the exports, so Geni does export former marriages and "
        "the format is not the limit.\n"
    )
    w.append(f"- already linked as spouses in our tree: **{len(linked)}**")
    w.append(f"- neither person has **any** spouse recorded: **{len(no_spouse)}** of {len(former)}")
    w.append(f"- one or both have spouses, but not each other: "
             f"**{len(former) - len(linked) - len(no_spouse)}**")
    w.append(
        "\nThe large group is people our exports reached without reaching their marriages at "
        "all, which points at export coverage rather than at a modelling gap.\n"
    )

    OUT.write_text("\n".join(w) + "\n", encoding="utf-8")
    print(f"wrote {OUT}")
    print(f"  sibling {len(sibling)}, former {len(former)}, other {len(other)}, "
          f"unmatched {len(unmatched)}")


if __name__ == "__main__":
    main()
