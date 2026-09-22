"""Emit ancestor-closure GEDCOMs from the derived synoptic CSVs.

Source of truth: reports/derived-{family,facts,places}.csv + display-names.csv
(the indexed form of out/merged.ged / the Geni union). No Geni network contact.

Usage:
  python scripts/emit-ancestor-gedcoms.py
"""
from __future__ import annotations

import collections
import gzip
import csv
import hashlib
import os
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
OUT_DIR = ROOT / "research-exports"
SEP = " | "

TANG_SEEDS = (
    "362164304500001795",   # Alexios Komnenos
    "6000000008024207441",  # David IV of Georgia
    "6000000002187826932",  # Yuri Dolgorukiy
)
LEONHART_SEED = "6000000087535357291"  # Emma Leonhart

csv.field_size_limit(10**9)


def open_text(path: Path):
    """Open CSV path, preferring gzip when path ends with .gz or sibling .gz exists."""
    if path.suffix == '.gz' or str(path).endswith('.csv.gz'):
        return gzip.open(path, 'rt', encoding='utf-8', newline='')
    gz = Path(str(path) + '.gz')
    if not path.exists() and gz.exists():
        return gzip.open(gz, 'rt', encoding='utf-8', newline='')
    return path.open(encoding='utf-8', newline='')




def load_family(path: Path) -> dict[str, tuple[str | None, str | None]]:
    parents: dict[str, tuple[str | None, str | None]] = {}
    # child -> (father, mother) using singular columns; multi only if singular empty
    with open_text(path) as fh:
        for row in csv.DictReader(fh):
            g = (row.get("geni_id") or "").strip()
            if not g:
                continue
            father = (row.get("father") or "").strip() or None
            mother = (row.get("mother") or "").strip() or None
            if not father and not mother:
                fathers = [x.strip() for x in (row.get("fathers") or "").split(SEP) if x.strip()]
                mothers = [x.strip() for x in (row.get("mothers") or "").split(SEP) if x.strip()]
                # When both columns are polluted with both parents (seen on the owner row),
                # prefer the first of each only if disjoint; else leave empty rather than invent.
                if fathers and mothers and set(fathers) != set(mothers):
                    father = fathers[0]
                    mother = mothers[0]
                elif fathers and not mothers:
                    father = fathers[0]
                elif mothers and not fathers:
                    mother = mothers[0]
            parents[g] = (father, mother)
    return parents


def load_facts(path: Path) -> dict[str, dict]:
    out: dict[str, dict] = {}
    with open_text(path) as fh:
        for row in csv.DictReader(fh):
            g = (row.get("geni_id") or "").strip()
            if g:
                out[g] = row
    return out


def load_places(path: Path) -> dict[str, tuple[str, str]]:
    out: dict[str, tuple[str, str]] = {}
    gz = Path(str(path) + '.gz')
    if not path.exists() and not gz.exists():
        return out
    with open_text(path) as fh:
        for row in csv.DictReader(fh):
            g = (row.get("geni_id") or "").strip()
            if g:
                out[g] = (
                    (row.get("birth_place") or "").strip(),
                    (row.get("death_place") or "").strip(),
                )
    return out


def load_names(path: Path) -> dict[str, list[dict]]:
    """geni_id -> name rows sorted by name_index."""
    by: dict[str, list[dict]] = collections.defaultdict(list)
    with open_text(path) as fh:
        for row in csv.DictReader(fh):
            g = (row.get("geni_id") or "").strip()
            if g:
                by[g].append(row)
    for g, rows in by.items():
        rows.sort(key=lambda r: int(r.get("name_index") or 0))
    return by


def ancestor_closure(seeds: list[str], parents: dict[str, tuple[str | None, str | None]]) -> set[str]:
    seen: set[str] = set()
    q: collections.deque[str] = collections.deque()
    for s in seeds:
        if s not in seen:
            seen.add(s)
            q.append(s)
    while q:
        g = q.popleft()
        father, mother = parents.get(g, (None, None))
        for p in (father, mother):
            if p and p not in seen:
                seen.add(p)
                q.append(p)
    return seen


def fam_xref(father: str | None, mother: str | None) -> str:
    key = f"{father or ''}|{mother or ''}"
    dig = int(hashlib.sha1(key.encode()).hexdigest()[:15], 16)
    return f"@F{dig}@"


def escape_ged(s: str) -> str:
    # GEDCOM has no standard escapes beyond CONC/CONT; strip NULs only.
    return s.replace("\0", "")


def emit_name_lines(lines: list[str], nrow: dict) -> None:
    raw = (nrow.get("name_raw") or "").strip()
    if not raw:
        givn = (nrow.get("givn") or "").strip()
        surn = (nrow.get("surn") or "").strip()
        if givn or surn:
            raw = f"{givn} /{surn}/" if surn else f"{givn} //"
        else:
            disp = (nrow.get("display_name") or "").strip()
            raw = f"{disp} //" if disp else "NN //"
    lines.append(f"1 NAME {escape_ged(raw)}")
    for tag, key in (
        ("NPFX", "npfx"),
        ("GIVN", "givn"),
        ("NICK", "nick"),
        ("SPFX", "spfx"),
        ("SURN", "surn"),
        ("NSFX", "nsfx"),
    ):
        v = (nrow.get(key) or "").strip()
        if v:
            lines.append(f"2 {tag} {escape_ged(v)}")
    marnm = (nrow.get("marnm") or "").strip()
    if marnm:
        lines.append(f"2 _MARNM {escape_ged(marnm)}")


def emit_event(lines: list[str], tag: str, date_raw: str, place: str) -> None:
    date_raw = (date_raw or "").strip()
    place = (place or "").strip()
    if not date_raw and not place:
        return
    lines.append(f"1 {tag}")
    if date_raw:
        lines.append(f"2 DATE {escape_ged(date_raw)}")
    if place:
        lines.append(f"2 PLAC {escape_ged(place)}")


def write_ged(
    path: Path,
    *,
    title: str,
    seeds: list[str],
    people: set[str],
    parents: dict[str, tuple[str | None, str | None]],
    facts: dict[str, dict],
    places: dict[str, tuple[str, str]],
    names: dict[str, list[dict]],
) -> tuple[int, int]:
    # Families: one per unique parent pair among people who have a parent in the set.
    families: dict[tuple[str | None, str | None], list[str]] = collections.defaultdict(list)
    child_famc: dict[str, str] = {}
    for child in people:
        father, mother = parents.get(child, (None, None))
        # Keep only parents that are in the closure (or None).
        f = father if father in people else None
        m = mother if mother in people else None
        if f is None and m is None:
            continue
        key = (f, m)
        families[key].append(child)
        child_famc[child] = fam_xref(f, m)

    # FAMS for each parent: families where they are HUSB/WIFE
    fams_of: dict[str, list[str]] = collections.defaultdict(list)
    for (f, m), children in families.items():
        xref = fam_xref(f, m)
        if f:
            fams_of[f].append(xref)
        if m:
            fams_of[m].append(xref)

    today = date.today().strftime("%d %b %Y").upper()
    lines: list[str] = [
        "0 HEAD",
        "1 SOUR synoptic-derived",
        f"2 NAME {title}",
        "2 CORP Emma Leonhart",
        f"1 DATE {today}",
        "1 GEDC",
        "2 VERS 5.5.1",
        "2 FORM LINEAGE-LINKED",
        "1 CHAR UTF-8",
        "1 NOTE Ancestor closure extracted from the synoptic tree derived CSVs",
        "2 CONT (reports/derived-family.csv + facts + places + display-names).",
        "2 CONT Seeds: " + ", ".join(seeds),
        "2 CONT Geni IDs preserved as xref and RFN geni:<id>. Family xrefs are",
        "2 CONT synthetic digests of the parent pair (not Geni family IDs).",
        "2 CONT No Geni network contact.",
    ]

    # Individuals, deterministic order
    for gid in sorted(people, key=lambda x: (len(x), x)):
        lines.append(f"0 @I{gid}@ INDI")
        nrows = names.get(gid) or []
        if nrows:
            for nrow in nrows[:8]:  # Geni often carries several NAME records
                emit_name_lines(lines, nrow)
        else:
            emit_name_lines(lines, {"name_raw": "NN //", "display_name": "NN"})
        fact = facts.get(gid) or {}
        sex = (fact.get("sex") or "").strip().upper()
        if sex in ("M", "F", "U"):
            lines.append(f"1 SEX {sex}")
        bplac = (fact.get("birth_place") or "").strip()
        dplac = (fact.get("death_place") or "").strip()
        if gid in places:
            pb, pd = places[gid]
            bplac = bplac or pb
            dplac = dplac or pd
        emit_event(lines, "BIRT", fact.get("birth_date_raw") or "", bplac)
        emit_event(lines, "DEAT", fact.get("death_date_raw") or "", dplac)
        bur = (fact.get("burial_date_raw") or "").strip()
        bpl = (fact.get("burial_place") or "").strip()
        emit_event(lines, "BURI", bur, bpl)
        occ = (fact.get("occupations") or "").strip()
        if occ:
            # occupations may be multi-valued with SEP
            for part in occ.split(SEP):
                part = part.strip()
                if part:
                    lines.append(f"1 OCCU {escape_ged(part)}")
        if gid in child_famc:
            lines.append(f"1 FAMC {child_famc[gid]}")
        for fx in fams_of.get(gid, ()):
            lines.append(f"1 FAMS {fx}")
        lines.append(f"1 RFN geni:{gid}")

    # Families
    for (f, m) in sorted(families.keys(), key=lambda k: (k[0] or "", k[1] or "")):
        children = sorted(set(families[(f, m)]), key=lambda x: (len(x), x))
        xref = fam_xref(f, m)
        lines.append(f"0 {xref} FAM")
        if f:
            lines.append(f"1 HUSB @I{f}@")
        if m:
            lines.append(f"1 WIFE @I{m}@")
        for c in children:
            lines.append(f"1 CHIL @I{c}@")

    lines.append("0 TRLR")
    path.parent.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + "\n"
    tmp = path.with_suffix(path.suffix + ".partial")
    tmp.write_text(text, encoding="utf-8", newline="\n")
    os.replace(tmp, path)
    return len(people), len(families)


def main() -> int:
    print("loading derived CSVs...")
    parents = load_family(REPORTS / "derived-family.csv")
    facts = load_facts(REPORTS / "derived-facts.csv")
    places = load_places(REPORTS / "derived-places.csv")
    names = load_names(REPORTS / "display-names.csv")
    print(f"  family rows {len(parents):,}; facts {len(facts):,}; names {len(names):,}; places {len(places):,}")

    for label, seeds, out_name in (
        ("tang DFA seeds", list(TANG_SEEDS), "tang-ancestors.ged"),
        ("leonhart", [LEONHART_SEED], "leonhart-ancestors.ged"),
    ):
        missing = [s for s in seeds if s not in parents and s not in facts and s not in names]
        if missing:
            raise SystemExit(f"seeds missing from synoptic derived data: {missing}")
        people = ancestor_closure(seeds, parents)
        # ensure seeds always included even if orphaned
        people.update(seeds)
        n_indi, n_fam = write_ged(
            OUT_DIR / out_name,
            title=f"synoptic ancestor closure - {label}",
            seeds=seeds,
            people=people,
            parents=parents,
            facts=facts,
            places=places,
            names=names,
        )
        print(f"wrote {OUT_DIR / out_name}: {n_indi:,} INDI, {n_fam:,} FAM; seeds={seeds}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
