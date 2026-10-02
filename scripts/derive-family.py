"""Plan item 5 — family links, and the parents that have to be invented.

Family links. A sibling relationship with no recorded parents gets two invented
parents, labelled *father of x and y* and *mother of x and y*, Geni-linked where
possible. Mother, father, spouse and child are the easy half.

Two halves, and they are very different in kind:

* **Derived links** — father, mother, spouse, child, read straight off the `FAM`
  records. Conversion, not invention.
* **Invented parents** — a sibling group with no parent recorded needs two
  placeholder people so the siblings hang off something. **This is the first
  step in the plan that creates data rather than converting it**, so the shapes
  are counted before anything is generated, and the generated rows are kept in
  their own file rather than mixed in with derived ones.

Matching is genealogical only — the governing rule — so nothing here uses a name
to decide anything. Names are used solely to *label* an invented parent.

Writes `reports/derived-family.csv` (one row per person),
`reports/invented-parents.csv` (one row per placeholder) and
`reports/derived-family-sources.csv` (which source gives a link, see `OUT_SOURCES`). Offline.

    py scripts/derive-family.py
"""

from __future__ import annotations

import csv
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from genimerge import doubles  # noqa: E402

MERGED = REPO_ROOT / "out" / "merged.ged"
PAIRS = REPO_ROOT / "out" / "wikidata" / "p2600-all.tsv"
LABELS = REPO_ROOT / "reports" / "derived-labels.csv"
OUT_PEOPLE = REPO_ROOT / "reports" / "derived-family.csv"
OUT_INVENTED = REPO_ROOT / "reports" / "invented-parents.csv"
#: ⛔ **WHICH SOURCE GIVES EACH LINK, SO A CITATION NAMES THE RIGHT ONE** (queue item, 2026-09-27).
#: The merged tree holds FamilySearch renders beside the Geni exports, with FamilySearch people
#: written on their Geni xrefs, so `derived-family.csv` alone cannot say whether FamilySearch,
#: Geni or both state a link, and everything was being cited to Geni. The family record says it:
#: every FamilySearch family is `@FFS…@` (`render-familysearch-gedcom.py`) and every Geni family
#: `@F<digits>@`. Rows: `geni_id, relation, relative, source`, with `relation` one of
#: `father`/`mother`/`spouse`/`child` and `source` `fs` or `both`. A link with no row is Geni's
#: alone, which keeps the file to the FamilySearch part. One more row per person carrying a
#: FamilySearch id: `relation` `fs_id`, `relative` the id (from `REFN fs:`), `source` `fs`.
OUT_SOURCES = REPO_ROOT / "reports" / "derived-family-sources.csv"
#: The family key drops the leading `@F`, so `@FFS…@` is keyed `FS…` and `@F<digits>@` digits.
FS_FAMILY_PREFIX = "FS"

csv.field_size_limit(10_000_000)


def join_names(names: list[str]) -> str:
    """`a and b`, `a and b and c`, then `a, b, c and d`.

    The label format is *father of x and y*, which fixes the two-child case and
    leaves the rest to follow. Extracted from ``main`` so the
    rule is testable: this string becomes the label of a **created** item, and a
    silent change to it changes data we are inventing.
    """
    if not names:
        return ""
    if len(names) <= 3:
        return " and ".join(names)
    return ", ".join(names[:-1]) + " and " + names[-1]


def parent_label(role: str, names: list[str]) -> str:
    return f"{role} of {join_names(names)}"


def main() -> int:
    qids: dict[str, str] = {}
    if PAIRS.exists():
        seen: dict[str, set[str]] = {}
        for qid, geni_id in doubles.load_pairs(PAIRS):
            seen.setdefault(geni_id, set()).add(qid)
        qids = {g: next(iter(q)) for g, q in seen.items() if len(q) == 1}

    # **This file is an INPUT, and for a long time the pipeline built it afterwards.**
    # `rebuild-everything.py` ran `derive-family.py` at step 3 and `derive-labels.py` at step 4,
    # so every rebuild read the previous generation's labels and a first run read none -- silently,
    # because the `if LABELS.exists()` below simply contributed nothing. The order is fixed there;
    # the warning here is so that running this script by hand, out of order, says so.
    labels: dict[str, str] = {}
    if LABELS.exists():
        with open(LABELS, encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                labels[row["geni_id"]] = row["label_en"] or row["cjk_names"].split(" | ")[0]
        if LABELS.stat().st_mtime < MERGED.stat().st_mtime:
            print(f"WARNING: {LABELS.name} is OLDER than {MERGED.name}. The names in "
                  f"invented-parents.csv will be from the previous merge. Run "
                  f"scripts/derive-labels.py first, or scripts/rebuild-everything.py.",
                  flush=True)
    else:
        print(f"WARNING: {LABELS} is absent, so no person will be named in "
              f"invented-parents.csv. Run scripts/derive-labels.py first.", flush=True)

    print(f"reading {MERGED}", flush=True)
    families: dict[str, dict] = {}
    people: set[str] = set()
    fs_ids: dict[str, str] = {}
    current: str | None = None
    kind = ""

    with open(MERGED, encoding="utf-8", errors="replace") as handle:
        for line in handle:
            if line.startswith("0 "):
                parts = line.split()
                current, kind = None, ""
                if len(parts) >= 3 and parts[1].startswith("@") and parts[1].endswith("@"):
                    xref = parts[1]
                    if parts[2] == "FAM" and xref.startswith("@F"):
                        current, kind = xref[2:-1], "FAM"
                        families[current] = {"husb": "", "wife": "", "chil": []}
                    elif parts[2] == "INDI" and xref.startswith("@I"):
                        current, kind = xref[2:-1], "INDI"
                        people.add(current)
                continue
            if kind == "INDI":
                if line.startswith("1 REFN fs:"):
                    fs_ids.setdefault(current, line[len("1 REFN fs:"):].strip())
                continue
            if kind != "FAM" or current is None:
                continue
            parts = line.rstrip("\n").split(None, 2)
            if len(parts) < 3 or parts[0] != "1":
                continue
            tag, value = parts[1], parts[2].strip()
            if not (value.startswith("@I") and value.endswith("@")):
                continue
            other = value[2:-1]
            if tag == "HUSB":
                families[current]["husb"] = other
            elif tag == "WIFE":
                families[current]["wife"] = other
            elif tag == "CHIL":
                families[current]["chil"].append(other)

    print(f"{len(people):,} people, {len(families):,} families", flush=True)

    # ⛔ **THE FATHER IS THE MAN AND THE MOTHER THE WOMAN, WHICHEVER SLOT A FILE PUT THEM IN.**
    # Found 2026-10-02 on the owner's own row: `exports/tiny-profiles/saved-6000000087535357291.ged`
    # writes Helen Frisk as `HUSB` and Richard Borsheim as `WIFE`, because `build-tiny-gedcoms.py`
    # filled the slots from a saved page's "son of X and Y" in page order. The saved pages were
    # deleted on 2026-09-14 and a `.ged` is never overwritten, so the slots are read by sex here.
    # Measured that day: 373 people had a woman as primary father, 358 a man as primary mother.
    # A family with one person in both slots keeps them in the slot their sex gives.
    sex_of: dict[str, str] = {}
    facts_for_sex = REPO_ROOT / "reports" / "derived-facts.csv"
    if facts_for_sex.exists():
        csv.field_size_limit(1 << 30)
        with open(facts_for_sex, encoding="utf-8", newline="") as fh:
            for row in csv.DictReader(fh):
                sex_of[row["geni_id"]] = (row.get("sex") or "").strip().upper()
    swapped = 0
    for fam in families.values():
        husb, wife = fam["husb"], fam["wife"]
        sh, sw = sex_of.get(husb, ""), sex_of.get(wife, "")
        if husb and husb == wife:
            if sh == "F":
                fam["husb"] = ""
            elif sh == "M":
                fam["wife"] = ""
            swapped += 1
        elif (sh == "F" and sw != "F") or (sw == "M" and sh != "M"):
            fam["husb"], fam["wife"] = wife, husb
            swapped += 1
    print(f"{swapped:,} families had their parents' slots corrected by sex", flush=True)

    # **A person can have more than one recorded father or mother, and 1,663 do.**
    # These were plain `dict[str, str]` and a second parent silently OVERWROTE the first,
    # so `derived-family.csv` could not represent the case at all -- it showed one parent,
    # chosen by family-iteration order, with nothing saying another existed. Measured over
    # `out/merged.ged` on 2026-08-25: 1,061 people with two or more fathers, 1,022 with two
    # or more mothers, 1,663 distinct people.
    #
    # `CLAUDE.md` documents exactly why this happens and that it is structural rather than
    # an error: the merge unions `FAMC`/`CHIL` and never drops one, so a parent link Geni
    # has since DELETED survives forever once any export carries it. The Samaritan case is
    # the worked example -- Geni rewrote a family in place and merging old with new gave
    # Abram two fathers, one of them the other's father. `exports/excluded/` exists because
    # nothing else can remove such a link.
    #
    # **`father`/`mother` keep their meaning** -- one id, the primary -- because 44 scripts
    # read them and a joined string would be a garbage id to every one of them. The full
    # set goes in NEW `fathers`/`mothers` columns, ` | `-separated like `children` and
    # `spouses` already are, so a consumer that cares can ask and the rest are untouched.
    father: dict[str, str] = {}
    mother: dict[str, str] = {}
    fathers: dict[str, list[str]] = defaultdict(list)
    mothers: dict[str, list[str]] = defaultdict(list)
    spouses: dict[str, list[str]] = defaultdict(list)
    children: dict[str, list[str]] = defaultdict(list)

    shapes: Counter[str] = Counter()
    needs_parents: list[tuple[str, list[str]]] = []
    link_sources: dict[tuple[str, str, str], set[str]] = defaultdict(set)

    for fam_id, fam in families.items():
        husb, wife, chil = fam["husb"], fam["wife"], fam["chil"]
        src = "fs" if fam_id.startswith(FS_FAMILY_PREFIX) else "geni"
        if husb and wife:
            link_sources[(husb, "spouse", wife)].add(src)
            link_sources[(wife, "spouse", husb)].add(src)
        for child in chil:
            for parent, role in ((husb, "father"), (wife, "mother")):
                if parent:
                    link_sources[(child, role, parent)].add(src)
                    link_sources[(parent, "child", child)].add(src)

        if husb and wife:
            if wife not in spouses[husb]:
                spouses[husb].append(wife)
            if husb not in spouses[wife]:
                spouses[wife].append(husb)

        for child in chil:
            if husb:
                father.setdefault(child, husb)
                if husb not in fathers[child]:
                    fathers[child].append(husb)
                if child not in children[husb]:
                    children[husb].append(child)
            if wife:
                mother.setdefault(child, wife)
                if wife not in mothers[child]:
                    mothers[child].append(wife)
                if child not in children[wife]:
                    children[wife].append(child)

        # The shape census. Counted before anything is invented.
        if chil and not husb and not wife:
            shapes["children, no parent recorded" if len(chil) > 1
                   else "one child, no parent recorded"] += 1
            if len(chil) > 1:
                needs_parents.append((fam_id, chil))
        elif chil and (husb and not wife):
            shapes["children, father only"] += 1
        elif chil and (wife and not husb):
            shapes["children, mother only"] += 1
        elif chil:
            shapes["children, both parents"] += 1
        elif husb and wife:
            shapes["couple, no children"] += 1
        elif husb or wife:
            shapes["one spouse alone"] += 1
        else:
            shapes["empty"] += 1

    # ⛔ **AN EXTRA PARENT BORN AT AN IMPOSSIBLE TIME IS DROPPED. Ruled 2026-10-02 (Emma, "fix
    # this").** The merge unions every `FAMC`, so a second father or mother survives from any
    # export that ever carried one, and some are impossible: Jelena of Hungary (born 1115) had
    # Immanuel Bang (born 1874) as a third father, Bogislaw II (born 1178) Ulla Celsing (born
    # 1854) as a second mother, and the path finder crossed them. A parent after the first
    # listed one is dropped, with the child's entry in its `children`, when both birth years are
    # known and the parent is born after the child, under 12 years before, or over 80 before;
    # with no birth year, by the parent's death year (below).
    # The first-listed parent is never dropped: that one is the Geni tree as Geni has it.
    facts_path = REPO_ROOT / "reports" / "derived-facts.csv"
    born: dict[str, int] = {}
    died: dict[str, int] = {}
    if facts_path.exists():
        csv.field_size_limit(1 << 30)
        with open(facts_path, encoding="utf-8", newline="") as fh:
            for row in csv.DictReader(fh):
                iso = (row.get("birth_date_iso") or "").strip()
                if len(iso) >= 5 and iso[1:5].isdigit():
                    born[row["geni_id"]] = int(iso[:5])
                iso = (row.get("death_date_iso") or "").strip()
                if len(iso) >= 5 and iso[1:5].isdigit():
                    died[row["geni_id"]] = int(iso[:5])
    else:
        print(f"WARNING: {facts_path.name} absent, so no impossible extra parent is dropped",
              flush=True)
    # A parent with no birth year in the tree takes Wikidata's, through the item its Geni id is
    # on (`out/wikidata/dates.tsv`): Immanuel Bang has no date in any export, and his item
    # `Q123437796` says 1874.
    wd_dates = REPO_ROOT / "out" / "wikidata" / "dates.tsv"
    if wd_dates.exists():
        by_qid = {}
        with open(wd_dates, encoding="utf-8", newline="") as fh:
            for row in csv.DictReader(fh, delimiter="\t"):
                y = (row.get("birth_year") or "").strip().lstrip("+")
                if y.lstrip("-").isdigit():
                    by_qid[row["qid"]] = int(y)
        for person in people:
            q = qids.get(person)
            if person not in born and q in by_qid:
                born[person] = by_qid[q]
    dropped_parents = []
    for plist, primary, role in ((fathers, father, "father"), (mothers, mother, "mother")):
        for child, parents in plist.items():
            if len(parents) < 2 or child not in born:
                continue
            keep = []
            for parent in parents:
                gap = born[child] - born[parent] if parent in born else None
                # No birth year for the parent: the death year decides instead. Dying over a year
                # before the child's birth, or over 120 years after it, is impossible too
                # (Immanuel Bang, Jelena's third father, has only a death year).
                late = (died[parent] - born[child]) if (gap is None and parent in died) else None
                if (parent != primary.get(child)
                        and ((gap is not None and (gap < 12 or gap > 80))
                             or (late is not None and (late < -1 or late > 120)))):
                    dropped_parents.append((child, role, parent, born[child],
                                            born.get(parent, ""), died.get(parent, "")))
                    if child in children.get(parent, []):
                        children[parent].remove(child)
                    continue
                keep.append(parent)
            plist[child] = keep
    with open(REPO_ROOT / "reports" / "dropped-impossible-parents.csv", "w", encoding="utf-8",
              newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["child", "slot", "parent", "child_born", "parent_born", "parent_died"])
        writer.writerows(sorted(dropped_parents))
    print(f"dropped {len(dropped_parents):,} impossible extra parent(s) "
          f"-> reports/dropped-impossible-parents.csv", flush=True)

    OUT_PEOPLE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_PEOPLE, "w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["geni_id", "qid", "father", "father_qid", "mother", "mother_qid",
                         "spouses", "spouse_qids", "children", "child_count",
                         "fathers", "mothers"])
        for person in sorted(people):
            f, m = father.get(person, ""), mother.get(person, "")
            sp = spouses.get(person, [])
            ch = children.get(person, [])
            writer.writerow([
                person, qids.get(person, ""),
                f, qids.get(f, "") if f else "",
                m, qids.get(m, "") if m else "",
                " | ".join(sp), " | ".join(qids.get(s, "") for s in sp),
                " | ".join(ch), len(ch),
                " | ".join(fathers.get(person, [])),
                " | ".join(mothers.get(person, [])),
            ])

    source_rows = sorted(
        [(p, rel, other, "both" if len(srcs) > 1 else "fs")
         for (p, rel, other), srcs in link_sources.items() if "fs" in srcs]
        + [(p, "fs_id", fs, "fs") for p, fs in fs_ids.items()])
    with open(OUT_SOURCES, "w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["geni_id", "relation", "relative", "source"])
        writer.writerows(source_rows)
    by_source = Counter(r[3] for r in source_rows if r[1] != "fs_id")
    print(f"wrote {OUT_SOURCES} ({len(source_rows):,} rows: {by_source['fs']:,} links FamilySearch "
          f"alone gives, {by_source['both']:,} both give, {len(fs_ids):,} FamilySearch ids)")

    def name_of(geni_id: str) -> str:
        return labels.get(geni_id) or geni_id

    with open(OUT_INVENTED, "w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["family", "role", "proposed_label", "children", "child_count",
                         "children_with_qid"])
        for fam_id, chil in needs_parents:
            names = [name_of(c) for c in chil]
            linked = sum(1 for c in chil if c in qids)
            for role in ("father", "mother"):
                writer.writerow([fam_id, role, parent_label(role, names),
                                 " | ".join(chil), len(chil), linked])

    with_father = sum(1 for p in people if p in father)
    with_mother = sum(1 for p in people if p in mother)
    with_spouse = sum(1 for p in people if spouses.get(p))
    with_child = sum(1 for p in people if children.get(p))

    print(f"wrote {OUT_PEOPLE} ({len(people):,} rows)")
    print(f"wrote {OUT_INVENTED} ({2*len(needs_parents):,} rows, "
          f"{len(needs_parents):,} families)")
    print()
    print(f"  father recorded  {with_father:>8,}")
    print(f"  mother recorded  {with_mother:>8,}")
    print(f"  spouse recorded  {with_spouse:>8,}")
    print(f"  children         {with_child:>8,}")
    print()
    print("family shapes:")
    for shape, n in shapes.most_common():
        print(f"  {n:>8,}  {shape}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
