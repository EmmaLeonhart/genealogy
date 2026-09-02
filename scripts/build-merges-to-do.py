"""Build reports/merges-to-do.md - the file Emma works from by hand.

Emma, 2026-08-31: "Just make a 'merges to do' file that records these merges and the
wikidata duplicates and all the other things we went over that's a file I'll use tomorrow
to do merges manually on my own with the quickstatements session".

Three populations, and they are not the same kind of work:

  * **Wikidata duplicates** - one Geni id carried by two Wikidata items. That is two items
    for one person and is a genuine merge. Note this is the *opposite* of the case
    CLAUDE.md section "A second Geni ID on one Wikidata item is NOT a conflict" rules out:
    two ids on one item is Geni's structure showing through, one id on two items is our own
    double-creation.
  * **Geni merges that cross a manager** - a real duplicate where the other profile belongs
    to somebody else, so merging is a request another editor sees.
  * **Items to audit** - three she flagged as wrong rather than duplicated. Not merges, but
    the same sitting.

Labels come from her ledger where she has one and from the merged tree otherwise; nothing
here is looked up over the network.
"""

import collections
import csv
import io
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
P2600 = ROOT / "out" / "wikidata" / "p2600-all.tsv"
LEDGER = ROOT / "reports" / "garborg-qids.tsv"
DERIVED = ROOT / "reports" / "derived-labels.csv"
OUT = ROOT / "reports" / "merges-to-do.md"

# Wikidata Help:Merge - merge the higher-numbered item into the lower-numbered one.
MERGE_URL = "https://www.wikidata.org/wiki/Special:MergeItems?from={frm}&to={to}"


def qnum(q):
    return int(q[1:])


def wikidata_duplicates():
    """Geni ids held by more than one Wikidata item."""
    by_geni = collections.defaultdict(set)
    with io.open(P2600, encoding="utf-8") as fh:
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            if len(parts) >= 2 and parts[0] and parts[1]:
                by_geni[parts[1]].add(parts[0])
    return {g: sorted(qs, key=qnum) for g, qs in by_geni.items() if len(qs) > 1}


def ledger():
    out = {}
    with io.open(LEDGER, encoding="utf-8") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            out[row["geni_id"]] = row
    return out


def tree_labels(wanted):
    """label_en / label_mul from the merged tree, for ids the ledger does not name."""
    found = {}
    if not DERIVED.exists() or not wanted:
        return found
    with io.open(DERIVED, encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            gid = row.get("geni_id")
            if gid in wanted:
                found[gid] = row.get("label_en") or row.get("label_mul") or ""
                if len(found) == len(wanted):
                    break
    return found


CORRESPONDENCE = ROOT / "reports" / "synoptic-correspondence.tsv"


def ledger_against_correspondence():
    """`[(geni_id, ours, {rival qid: sources})]` — an item we created beside an older one.

    **The shape section 1 cannot see.** That section needs BOTH items to carry a `P2600`, so it
    finds double-creations by our own batches and nothing else. The duplicates Emma actually hit
    on 2026-09-01 were the opposite: the **pre-existing item carries no Geni id at all**, so no
    `P2600` join reaches it and a `P2600` search afterwards returns only the one we made.
    `Q550343` *Welf I, Duke of Bavaria*, 27 sitelinks, was created again as `Q141249742` for
    exactly that reason, along with three others she merged by hand the same afternoon.

    `reports/synoptic-correspondence.tsv` does see them, through the zipper and the structural
    walk. Where the ledger says a Geni profile is one item and the correspondence says it is also
    an older one, that is a probable double-creation and a merge for her.

    **40 of them on 2026-09-01**, five spot-checked live that day: every one matched on sex, and
    on both dates wherever both sides carried them — `Johanna Catharina Burman` 1710–1778 against
    `Q100354376`, `Magdalena von Mentzer` 1726–1809 against `Q103771980`, plus `Maria Carlberg`,
    `Margareta Lejon` and `Ingrid Ekenbom` on sex and name.
    """
    tab = chr(9)
    led = collections.defaultdict(set)
    with io.open(LEDGER, encoding="utf-8") as fh:
        for r in csv.DictReader(fh, delimiter=tab):
            g, q = (r.get("geni_id") or "").strip(), (r.get("qid") or "").strip()
            if g and q:
                led[g].add(q)
    if not CORRESPONDENCE.exists():
        return []
    rival = collections.defaultdict(dict)
    with io.open(CORRESPONDENCE, encoding="utf-8") as fh:
        for r in csv.DictReader(fh, delimiter=tab):
            g, q = r.get("geni_id", ""), r.get("qid", "")
            if g in led and q and q not in led[g]:
                rival[g][q] = r.get("sources", "?")
    return [(g, sorted(led[g]), rival[g]) for g in sorted(rival)]


def pair_lines(geni_id, qids, label):
    """One bullet per duplicate, with the merge prefilled the way Help:Merge wants it."""
    keep = qids[0]  # lowest Q number survives
    bits = ["- **{}** - Geni `{}`".format(label or geni_id, geni_id)]
    for extra in qids[1:]:
        bits.append(
            "    - merge **{}** into **{}** - {}".format(
                extra, keep, MERGE_URL.format(frm=extra, to=keep)
            )
        )
    return "\n".join(bits)


def main():
    dupes = wikidata_duplicates()
    led = ledger()
    hers = {g: q for g, q in dupes.items() if g in led}
    theirs = {g: q for g, q in dupes.items() if g not in led}
    names = tree_labels(set(theirs))

    w = []
    w.append("# Merges to do - by hand\n")
    w.append(
        "**Emma's file, 2026-08-31**: *\"Just make a 'merges to do' file that records these "
        "merges and the wikidata duplicates and all the other things we went over that's a "
        "file I'll use tomorrow to do merges manually on my own with the quickstatements "
        'session"*.\n'
    )
    w.append(
        "Regenerate with `python scripts/build-merges-to-do.py`. Every link is prefilled; "
        "nothing here has been executed.\n"
    )
    w.append(
        "**Direction:** Wikidata's `Help:Merge` keeps the **lower** Q number, so each line "
        "below merges the higher into the lower. Where that is the wrong way round - the "
        "higher item is the better-populated one - merge the other way and let the redirect "
        "fall where it should.\n"
    )

    w.append("\n## 1. Wikidata duplicates in your own ledger - {}\n".format(len(hers)))
    w.append(
        "One Geni profile carrying two Wikidata items, where the ledger tracks that person. "
        "This is a double-creation, not the two-ids-on-one-item case CLAUDE.md says to leave "
        "alone. The ledger records people we track rather than only items you made, so a few "
        "of these pair one of ours against an item that already existed - `Garlande` below "
        "is that shape, and there the lower number is also the better-populated item.\n"
    )
    w.append(
        "**Spot-checked live against Wikidata on 2026-08-31**: 12 of the 16 were fetched with "
        "`wbgetentities`, none is already a redirect, and each pair carries the same `P2600`. "
        "They are live duplicates, not an artefact of a stale download.\n"
    )
    consecutive = [g for g, q in hers.items() if len(q) == 2 and qnum(q[1]) - qnum(q[0]) <= 3]
    if consecutive:
        w.append(
            "**{} of these are near-consecutive Q numbers**, which means one run created "
            "each person twice rather than two runs colliding months apart.\n".format(
                len(consecutive)
            )
        )
    for geni_id, qids in sorted(hers.items(), key=lambda kv: qnum(kv[1][0])):
        w.append(pair_lines(geni_id, qids, led[geni_id].get("label", "")))

    w.append("\n## 2. Wikidata duplicates outside your ledger - {}\n".format(len(theirs)))
    w.append(
        "Same shape, but these items are not ones the ledger records you making, so some "
        "will be somebody else's duplicates rather than ours. Lower priority, and worth a "
        "look at the item before merging.\n"
    )
    for geni_id, qids in sorted(theirs.items(), key=lambda kv: qnum(kv[1][0])):
        w.append(pair_lines(geni_id, qids, names.get(geni_id, "")))

    w.append("\n## 3. Geni merges that cross a manager\n")
    w.append(
        "Real duplicates where the other profile belongs to somebody else, so the merge is "
        "a request another editor sees. The Izumo pair that was entirely yours "
        "(`Munetoshi 71 Senge`) is already merged; `Okinaga no Sukune` was merged before we "
        "got there.\n"
    )
    w.append(
        "- **Shigeyasu Takaoka** - yours `6000000227331730906` (19 Aug placeholder, "
        "`Q135579463` in the About) against `6000000217687134824`, added by **Isao Takaoka** "
        "in April 2025 and managed by him: b.1437, d.1483, father of Joan Bingo-nyudo "
        "Takaoka. Same name, same father `Shigeyori Takaoka`.\n"
        "    - https://www.geni.com/people/x/6000000227331730906\n"
        "    - https://www.geni.com/people/x/6000000217687134824\n"
    )
    w.append(
        "- **The 40 largest CJK groups** are in `reports/geni-merge-worklist.md` and are not "
        "repeated here. The `坂上` groups under a `Tanba` parent are the real signal "
        "- eight of them, 3 to 6 profiles each. The bare one-token surname groups "
        "(`杨`, `黄`, `邱`) are an artefact of the name column and are **not** "
        "evidence of duplication.\n"
    )

    w.append("\n## 4. Items you flagged as wrong, to look at in the same sitting\n")
    w.append(
        "Not duplicates - three you called erroneous on 2026-08-30. None has been "
        "investigated, and each is still its own queue item.\n"
    )
    w.append(
        '- **`Q141223488`** and the item merged into it - *"both just completely '
        'erroneous"*. https://www.wikidata.org/wiki/Q141223488\n'
        '- **`Q6197518`** - the `mul` label was "corrected" to an English-only one and you '
        "did not understand why. https://www.wikidata.org/wiki/Q6197518\n"
        '- **"En dödfödd son Bielke"** - created as a label, which is a description '
        "of a stillborn child rather than a name.\n"
    )

    w.append("\n## 5. Name items that look like Wikidata duplicates\n")
    dupe_names = ROOT / "reports" / "duplicate-name-items.tsv"
    if dupe_names.exists():
        by_pair = {}
        with io.open(dupe_names, encoding="utf-8", newline="") as fh:
            for row in csv.DictReader(fh, delimiter="\t"):
                by_pair.setdefault(row["qids"], []).append(row)
        w.append(
            f"**{len(by_pair)} distinct item pairs**, across "
            f"{sum(len(v) for v in by_pair.values())} name strings. Two items for one name "
            "with **identical English descriptions** and nothing else to tell them apart — "
            "`Schloss` is `Q105540652` *family name* and `Q37300956` *family name*.\n"
        )
        w.append(
            "`reports/name-ambiguity-causes.md` found this bucket and its verdict was *\"worth "
            "reporting upstream rather than choosing between\"*. **An identical description is "
            "evidence, not proof** — the description may simply be too thin to distinguish two "
            "real names — so these are candidates to look at, not merges to run blind. They do "
            "not feed the name plan and nothing here depends on them.\n"
        )
        w.append(
            "Some pairs appear under more than one spelling, which is itself a hint: `Strauss` "
            "and `Strauß` resolve to the same two items, as do `FitzGerald` and `Fitzgerald`.\n"
        )
        for qids, rows in sorted(by_pair.items(),
                                 key=lambda kv: -sum(int(r["occurrences"] or 0)
                                                     for r in kv[1])):
            names = ", ".join(sorted({r["name"] for r in rows}))
            bearers = sum(int(r["occurrences"] or 0) for r in rows)
            parts = [q.strip() for q in qids.split("|")]
            keep = sorted(parts, key=qnum)[0]
            others = [q for q in sorted(parts, key=qnum)[1:]]
            w.append(f"- **{names}** — {rows[0]['kind']}, {bearers} bearer(s), both described "
                     f"*{rows[0]['description']}*")
            for extra in others:
                w.append(f"    - merge **{extra}** into **{keep}** — "
                         + MERGE_URL.format(frm=extra, to=keep))
    else:
        w.append("`reports/duplicate-name-items.tsv` is not built; run "
                 "`python scripts/find-duplicate-name-items.py`.\n")

    w.append("\n## 6. Created by a batch, and needing a merge afterwards\n")
    w.append(
        "**Emma flagged this one herself, 2026-08-31**, while running the batch: *\"we are gonna "
        "want to merge https://www.wikidata.org/wiki/Q130665779 with our recently created thing "
        "at some point\"*.\n"
    )
    w.append(
        "- **Ulrika von Düben** — `Q130665779` (sv *svensk friherrinna*, b. 1749-01-26, "
        "d. 1777-01-13) against the item `reports/wikidata-garborg-day.qs` creates for Geni "
        "`6000000009063273551`.\n"
        "    - merge the newly created item **into `Q130665779`** — it is the older and far "
        "better populated one, carrying `P22`, `P25`, `P26`, `P27`, `P40`×2, `P569`, `P570`, "
        "`P734` and `P735`.\n"
        "    - https://www.wikidata.org/wiki/Q130665779\n"
    )
    w.append(
        "**Why the duplicate guard did not stop it, which is the part worth knowing.** "
        "`build-garborg-day.py` blocks a creation when `out/wikidata/p2600-all.tsv` already "
        "links that Geni id — and **`Q130665779` carries no `P2600` at all**, so there was "
        "nothing to match on. The guard is a `P2600` join and is blind to an item that has "
        "never been linked to Geni.\n"
    )
    w.append(
        "**They are the same person on STRUCTURE, not on the name.** Our "
        "`6000000009063273551` has spouse `6000000007680468910`, which the ledger holds as "
        "`Q5626148` *Carl Wilhelm von Düben*; `Q130665779` carries `P26 Q5626148` — the same "
        "husband. That is a closed-slot match of the kind `CLAUDE.md` permits, not a name "
        "similarity.\n"
    )
    w.append(
        "**Creating then merging is not a defect here.** `CLAUDE.md` § *Her own duplicates are "
        "DELIBERATE* records that a creation followed by a merge leaves the edit trail she "
        "wants, and she raised this as something to do *at some point* rather than something "
        "to prevent.\n"
    )

    rivals = ledger_against_correspondence()
    rival_names = tree_labels({g for g, _, _ in rivals})
    w.append("\n## 8. An item you created beside an older one nobody joined by Geni id - {}\n"
             .format(len(rivals)))
    w.append(
        "**The shape section 1 cannot see.** That section needs BOTH items to carry a `P2600`. "
        "These are the opposite: the older item carries **no Geni id at all**, so no `P2600` join "
        "reaches it and a `P2600` search afterwards returns only the one we made. `Q550343` "
        "*Welf I, Duke of Bavaria* - 27 sitelinks - was created again as `Q141249742` for exactly "
        "this reason on 2026-09-01, along with three others you merged by hand.\n"
    )
    w.append(
        "`reports/synoptic-correspondence.tsv` does see them, through the zipper and the "
        "structural walk. **Five were spot-checked live on 2026-09-01** and every one matched on "
        "sex and on both dates where both sides carried them. The bracketed `sources` says what "
        "found each pair: a `zipper`-only row is the weakest, carrying a measured 2.8-4.8% error, "
        "so read both items before merging that one.\n"
    )
    # `older` rather than `theirs`: `theirs` is section 2's dict and shadowing it here made the
    # closing summary print `1 other` while the file itself correctly said 67. A summary line that
    # disagrees with the file it summarises is the exact failure this repo keeps recording.
    for g, ours, older in rivals:
        label = rival_names.get(g) or g
        w.append("- **{}** - Geni `{}` - you created {}".format(label, g, ", ".join(ours)))
        for q, src in sorted(older.items(), key=lambda kv: qnum(kv[0])):
            both = sorted(ours + [q], key=qnum)
            w.append("    - also **{}** _({})_ - merge **{}** into **{}** - {}".format(
                q, src, both[-1], both[0], MERGE_URL.format(frm=both[-1], to=both[0])))

    w.append("\n## 7. Name items merged away by other editors\n")
    w.append(
        "Your 2026-08-29 note: name items we created were merged into existing ones, and "
        '*"creating the name objects and having them merged by somebody else... is a thing '
        'that gets attention in a bad way"*. `Tunheim` is the one that already happened. '
        "The fix - invert the default so an existing name item is reused - is a queue item, "
        "not something for this sitting; it is here so the merges are in one place.\n"
    )

    OUT.write_text("\n".join(w) + "\n", encoding="utf-8")
    print("wrote {}".format(OUT))
    print("  wikidata duplicates: {} yours, {} other".format(len(hers), len(theirs)))
    print("  created beside an older item: {}".format(len(rivals)))

    # **The page is regenerated with the file, in the same step.** The queue item asks for this
    # explicitly so the page is never staler than the markdown it is built from. It is a
    # subprocess rather than an import because the generator has a hyphen in its name.
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / "build-merges-page.py")],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode:
        print("  merges page FAILED: " + ((r.stderr or r.stdout or "").strip()[-300:]))
    else:
        print("  " + (r.stdout or "").strip().splitlines()[-5].strip())


if __name__ == "__main__":
    main()
