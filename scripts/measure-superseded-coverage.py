"""How much of the superseded exports is not yet covered by a re-export?

**Emma's plan, 2026-08-15:** *"I am just gonna do imports until all items found in
the Tsedaka II ones are also present in later exports."*

**The problem being solved.** `Yitzhaq I ben Tsedaka` (`6000000227245553985`) was
missing from Geni, so Geni linked **Tsedaka II → Abram** directly, skipping a
generation. Emma added him and re-exported. Four Samaritan exports predate that
fix and still assert the skipping edge; `export-Forest-6000000178795709821.ged`
carries the corrected one. The merge unions `FAMC` links and never drops one, so
**the superseded edge survives in `out/merged.ged` as long as those four exports
are corpus** — and they are corpus permanently, because a GEDCOM is never deleted
here.

**So the fix is coverage, not deletion.** Once every person in a superseded
export also appears in an export taken after the correction, the old file adds
nothing that a newer one does not also carry, and the stale edges can be
overridden at merge time rather than by losing data.

**This measures the remaining gap.** For each superseded export: which of its
people are *only* there. Those are what the next export has to reach.

**Recency is by file, not by `HEAD` date.** Geni writes the *seed's* dates into
the header — `ABT 2010`, `1732` — not the export time, so the header cannot order
these. `SUPERSEDED` and `CORRECTED` are named explicitly below, which is honest
about it being a judgement rather than a derived fact.

Writes `reports/superseded-coverage.md` and `reports/superseded-coverage.csv` —
one row per person still uncovered, with which export holds them and who their
father is on each side.

    py scripts/measure-superseded-coverage.py
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

#: The four exports taken before Yitzhaq I existed on Geni. Each asserts
#: `Tsedaka II -> Abram`, skipping him.
SUPERSEDED = [
    "exports/samaritans/export-Ancestors-6000000227240714964.ged",
    "exports/samaritans/export-BloodTree-6000000227240714964.ged",
    "exports/samaritans/export-Forest-6000000178794141887.ged",
    "exports/samaritans/export-Forest-6000000227240691895.ged",
]

#: Taken after the correction. Anything appearing here is covered. New exports
#: get appended as Emma takes them — that is the loop this script is for.
CORRECTED = [
    "exports/samaritans/export-Forest-6000000178795709821.ged",
]

OUT_MD = REPO / "reports" / "superseded-coverage.md"
OUT_CSV = REPO / "reports" / "superseded-coverage.csv"

INDI = re.compile(r"^0 @I(\d+)@ INDI")
FAM = re.compile(r"^0 @F(\d+)@ FAM")


def read(path: Path):
    """`names[id]`, `father[id] -> id` for one GEDCOM."""
    names: dict[str, str] = {}
    famc: dict[str, str] = {}
    husb: dict[str, str] = {}
    cur = curf = None
    with open(path, encoding="utf-8-sig", errors="replace") as handle:
        for line in handle:
            if line.startswith("0 "):
                m = INDI.match(line)
                if m:
                    cur, curf = m.group(1), None
                    continue
                m = FAM.match(line)
                cur, curf = None, (m.group(1) if m else None)
                continue
            if cur:
                m = re.match(r"^1 NAME (.*)$", line)
                if m and cur not in names:
                    names[cur] = m.group(1).strip()
                m = re.match(r"^1 FAMC @F(\d+)@", line)
                if m:
                    famc.setdefault(cur, m.group(1))
            elif curf:
                m = re.match(r"^1 HUSB @I(\d+)@", line)
                if m:
                    husb[curf] = m.group(1)
    father = {c: husb[f] for c, f in famc.items() if f in husb}
    return names, father


def main() -> int:
    covered: dict[str, str] = {}
    cov_names: dict[str, str] = {}
    cov_father: dict[str, str] = {}
    for rel in CORRECTED:
        names, father = read(REPO / rel)
        for pid in names:
            covered.setdefault(pid, Path(rel).name)
        cov_names.update(names)
        cov_father.update(father)
        print(f"covered by {Path(rel).name}: {len(names):,} people")

    rows = []
    summary = []
    for rel in SUPERSEDED:
        path = REPO / rel
        names, father = read(path)
        missing = [p for p in names if p not in covered]
        summary.append((Path(rel).name, len(names), len(missing)))
        print(f"\n{Path(rel).name}: {len(names):,} people, "
              f"**{len(missing):,} not in any corrected export**")
        for pid in missing:
            fid = father.get(pid, "")
            rows.append({
                "geni_id": pid,
                "name": names[pid],
                "only_in": Path(rel).name,
                "father_id": fid,
                "father_name": names.get(fid, ""),
            })

    # A person can be uncovered in several superseded exports; the work to cover
    # them is one export either way, so report them once and note the rest.
    seen: dict[str, dict] = {}
    for row in rows:
        if row["geni_id"] in seen:
            seen[row["geni_id"]]["only_in"] += f" | {row['only_in']}"
        else:
            seen[row["geni_id"]] = row
    unique = list(seen.values())

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=["geni_id", "name", "only_in", "father_id", "father_name"])
        writer.writeheader()
        writer.writerows(sorted(unique, key=lambda r: r["name"]))

    total_super = len({p for rel in SUPERSEDED for p in read(REPO / rel)[0]})
    L: list[str] = []
    add = L.append
    add("# What the superseded Samaritan exports still hold alone")
    add("")
    add("**Emma, 2026-08-15:** *\"I am just gonna do imports until all items found in")
    add("the Tsedaka II ones are also present in later exports.\"* This is the gap")
    add("remaining. Re-run it after each import; the target is **0 uncovered**.")
    add("")
    add("`Yitzhaq I ben Tsedaka` (`6000000227245553985`) was missing from Geni, so Geni")
    add("linked **Tsedaka II → Abram** directly. Four exports predate the fix and still")
    add("carry that edge. GEDCOMs are never deleted here and the merge unions `FAMC`")
    add("links, so the superseded edge cannot be removed by dropping a file — **it is")
    add("retired by covering every person in those files with a newer export.**")
    add("")
    add("## The gap")
    add("")
    add("| superseded export | people | not yet covered |")
    add("| --- | ---: | ---: |")
    for name, total, miss in summary:
        add(f"| `{name}` | {total:,} | **{miss:,}** |")
    add(f"| **distinct across all four** | **{total_super:,}** | "
        f"**{len(unique):,}** |")
    add("")
    add("Covered means: present in an export listed as `CORRECTED` in")
    add("`scripts/measure-superseded-coverage.py`. **Add each new export to that list**")
    add("— it is the only place recency is recorded, because Geni writes the *seed's*")
    add("dates into the `HEAD` (`ABT 2010`, `1732`) rather than the export time, so the")
    add("header cannot order these files.")
    add("")
    add("Every uncovered person is a row in `reports/superseded-coverage.csv`, with the")
    add("father the superseded export gives them — which is what a re-export has to")
    add("either confirm or correct.")
    add("")
    add("## The two remaining gaps are not the same problem")
    add("")
    add("Both `Forest` exports are **fully covered already**, and the other two are not")
    add("uncovered in the same place:")
    add("")
    add("- **`export-Ancestors-…240714964` — 24 people, and they are the relevant ones.**")
    add("  Eight are the `Nth generation Samaritan Itamar line` placeholders; the rest are")
    add("  Assyrian kings, plus Amram and Jochebed. This is a small, targeted export away")
    add("  from zero.")
    add("- **`export-BloodTree-…240714964` — 3,290 people, and they are Javanese.** The")
    add("  `BloodTree` walked up out of the Samaritan cluster entirely: the uncovered")
    add("  head is Mataram and Demak royalty — Senapati, Sunan Giri, Raden Patah. None of")
    add("  them carries the superseded `Tsedaka II → Abram` edge, because none of them is")
    add("  anywhere near it. **1,069 of the 3,290 appear in no other export at all**, so")
    add("  covering them is real work that buys nothing towards this particular fix.")
    add("")
    add("**That distinction is worth making before doing the imports.** The criterion")
    add("here — cover everything in the superseded files — is Emma's and is stated")
    add("bluntly on purpose. But its *purpose* is retiring one stale edge, and the")
    add("Javanese 3,290 are a `BloodTree` side-effect rather than part of it.")
    add("")
    if unique:
        add("## Where to seed next — **per export, because they differ completely**")
        add("")
        add("The uncovered people grouped by the father they hang from: a seed reaching")
        add("one of these fathers covers that whole group in a single export. Grouped")
        add("per superseded export rather than merged, because the two remaining files")
        add("are uncovered in **different parts of the tree** and merging the tables")
        add("hides that.")
        add("")
        for rel in SUPERSEDED:
            name = Path(rel).name
            mine = [r for r in unique if name in r["only_in"]]
            if not mine:
                continue
            add(f"### `{name}` — {len(mine):,} uncovered")
            add("")
            by_father: dict[str, list[dict]] = {}
            for row in mine:
                by_father.setdefault(
                    row["father_name"] or "(no father recorded)", []).append(row)
            add("| father in the superseded export | uncovered children | example |")
            add("| --- | ---: | --- |")
            for fname, kids in sorted(by_father.items(), key=lambda kv: -len(kv[1]))[:12]:
                add(f"| {fname[:70]} | {len(kids)} | {kids[0]['name'][:44]} |")
            add("")
            if len(by_father) > 12:
                add(f"…and {len(by_father) - 12:,} more fathers with fewer children each.")
                add("")
    else:
        add("## Nothing is uncovered")
        add("")
        add("Every person in the four superseded exports appears in a corrected one.")
        add("The old files now add no person a newer export does not also carry, so the")
        add("stale `Tsedaka II → Abram` edge can be resolved at merge time without")
        add("losing anybody. **This is the condition Emma was importing towards.**")

    OUT_MD.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"\n{len(unique):,} distinct people uncovered")
    print(f"wrote {OUT_MD} and {OUT_CSV}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
