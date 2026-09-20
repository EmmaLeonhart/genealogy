"""The three identification ledgers. One place to ask which bucket a pair is in.

⛔ **THREE FLAT TSVs, TWO COLUMNS EACH, NO PROVENANCE. Ruled 2026-09-17.**

    reports/entry-points-now.tsv    an entry point TODAY
    reports/entry-points-jan1.tsv   an entry point on 2027-01-01
    reports/identifications.tsv     passive: a QID identification and nothing more

Every row is `qid` and `geni_id`. **That is the whole schema.** No label, no date, no note, no
batch, no verdict, no source file — *"there is no reason why you, the agent, should have any
knowledge of where it is that any of these IDs came from ... These IDs are accepted as gospel by
you. You do not question them. I add to them."*

This module exists because the thing it replaces was spread over four files with two different
`active_from` mechanisms, and answering *is this person an entry point* meant holding all of them
together. It could not be held: *"you were always consistently breaking it because it was not
transparent enough to you what it was."* Now there is one import and three functions.

## ⛔ A PAIR MAY BE IN ALL THREE, AND NOTHING HERE DEDUPES ACROSS THEM

*"something can be in every single one of these buckets. If there's any kind of check that somehow
blocks anything from happening in the January 1st one, it's wrong."*

The passive identification is **contained within** the other two: an entry point is also an
identification. So `identifications()` returns the union of all three rather than only the passive
file, and no function here treats membership of two buckets as a conflict.

## ⛔ THE DATE GOVERNS ENTRY-POINT STATUS ONLY, NEVER EDITABILITY

*"If any one of the January 1st one is eligible to be edited, it can have the Geni ID added to it
before it's an entry point."* So `identifications()` ignores the date entirely, and only
`entry_points()` consults it. A caller asking *may I write a statement about this pair* must use
`identifications()`; a caller asking *does this pair seed the universe* uses `entry_points()`.
"""

from __future__ import annotations

import csv
import datetime
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

NOW = ROOT / "reports" / "entry-points-now.tsv"
JAN1 = ROOT / "reports" / "entry-points-jan1.tsv"
PASSIVE = ROOT / "reports" / "identifications.tsv"


#: ⛔ **THE BLOC IS BACK, AND A BLOC IS A ROSTER REFERENCE.** Restored 2026-09-20 after being
#: deleted on 2026-09-17 by the commit that flattened everything to two-column files.
#:
#: `CLAUDE.md` § *A BLOC IS A ROSTER REFERENCE, never pasted ids. Entry points drip in on a date
#: column, not a cron; the roster stays at about 250.* That rule survived the deletion and spent
#: three days describing machinery that no longer existed. **Two columns cannot express a bloc**:
#: a bloc names a SOURCE FILE and a date, so when the roster grows the entry points grow with it.
#: Flattened to `qid, geni_id`, it becomes a snapshot that silently stops tracking.
GROUPS = ROOT / "reports" / "entry-point-groups.tsv"

#: One row per PERSON with the date they switch on -- the trickle, as against the blocs above.
DATED = ROOT / "reports" / "entry-points.tsv"


def _pairs_from_source(spec: str) -> list[tuple[str, str]]:
    """Every `(qid, geni_id)` a bloc's source file names.

    Two shapes, because the rosters have two. A delimited table is read on its own header; the
    identifications GEDCOM is read as `0 @I<geni>@ INDI` followed by `1 NOTE <wikidata url>`,
    which is the shape `build-qid-links-gedcom.py` writes.
    """
    out: list[tuple[str, str]] = []
    for part in (spec or "").split(","):
        path = ROOT / part.strip()
        if not part.strip() or not path.exists():
            continue
        if path.suffix.lower() == ".ged":
            gid = ""
            for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
                m = re.match(r"^0 @I(\d+)@ INDI", line)
                if m:
                    gid = m.group(1)
                    continue
                q = re.search(r"\b(Q\d+)\b", line)
                if q and gid and line.lstrip().startswith("1 NOTE"):
                    out.append((q.group(1), gid))
            continue
        delim = "\t" if path.suffix.lower() == ".tsv" else ","
        with path.open(encoding="utf-8") as fh:
            for row in csv.DictReader(fh, delimiter=delim):
                q = (row.get("qid") or "").strip()
                g = (row.get("geni_ids") or row.get("geni_id") or "").strip()
                # A roster may carry several ids in one cell; each is its own pair.
                for one in re.split(r"[ ,;|]+", g):
                    if q.startswith("Q") and one.isdigit():
                        out.append((q, one))
    return out


def bloc_pairs(today: datetime.date | None = None) -> list[tuple[str, str]]:
    """Every pair from every bloc whose `active_from` has arrived."""
    today = today or datetime.date.today()
    if not GROUPS.exists():
        return []
    out: list[tuple[str, str]] = []
    with GROUPS.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            try:
                live = datetime.date.fromisoformat((row.get("active_from") or "").strip()) <= today
            except ValueError:
                live = False
            if live:
                out.extend(_pairs_from_source(row.get("source") or ""))
    return out


def dated_pairs(today: datetime.date | None = None) -> list[tuple[str, str]]:
    """The per-person trickle, for rows whose own date has arrived."""
    today = today or datetime.date.today()
    if not DATED.exists():
        return []
    out = []
    with DATED.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            qid = (row.get("qid") or "").strip()
            gid = (row.get("geni_id") or "").strip()
            try:
                live = datetime.date.fromisoformat((row.get("active_from") or "").strip()) <= today
            except ValueError:
                live = False
            if live and qid.startswith("Q") and gid.isdigit():
                out.append((qid, gid))
    return out

#: The one date in the system. The January bucket becomes entry points on it and not before.
JAN1_DATE = datetime.date(2027, 1, 1)


def _read(path: Path) -> list[tuple[str, str]]:
    """`(qid, geni_id)` pairs, in file order, skipping anything malformed.

    A malformed row is skipped rather than repaired. This module renders a decision somebody else
    made; it does not adjudicate one.
    """
    if not path.exists():
        return []
    out = []
    with path.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            qid = (row.get("qid") or "").strip()
            gid = (row.get("geni_id") or "").strip()
            if qid.startswith("Q") and gid.isdigit():
                out.append((qid, gid))
    return out


def now_pairs() -> list[tuple[str, str]]:
    """Entry points effective immediately."""
    return _read(NOW)


def jan1_pairs() -> list[tuple[str, str]]:
    """Entry points effective 2027-01-01. Editable before then like anything else."""
    return _read(JAN1)


def passive_pairs() -> list[tuple[str, str]]:
    """Identifications that confer no entry-point status of their own."""
    return _read(PASSIVE)


def entry_points(today: datetime.date | None = None) -> list[tuple[str, str]]:
    """The pairs that are entry points as of `today`, deduped, sorted.

    ⛔ The January bucket joins on `JAN1_DATE` and not one day earlier. That is the only thing the
    date does.
    """
    today = today or datetime.date.today()
    pairs = list(now_pairs())
    # ⛔ The blocs and the per-person trickle each carry their OWN date and are checked
    # against it; only the January bucket uses JAN1_DATE. Restored 2026-09-20.
    pairs += bloc_pairs(today)
    pairs += dated_pairs(today)
    if today >= JAN1_DATE:
        pairs += jan1_pairs()
    return sorted(dict.fromkeys(pairs))


def identifications() -> list[tuple[str, str]]:
    """Every QID-to-Geni identification this repo holds, from all three ledgers, deduped.

    ⛔ **ALL THREE, ALWAYS, AND NO DATE.** An entry point is an identification too, so the passive
    file is not the whole answer and the January date is irrelevant here: a pair may have its Geni
    id written to Wikidata whenever the item is otherwise eligible, entry point or not.
    """
    far = datetime.date.max
    return sorted(dict.fromkeys(now_pairs() + jan1_pairs() + passive_pairs()
                                + bloc_pairs(far) + dated_pairs(far)))


def qid_for_geni() -> dict[str, list[str]]:
    """`{geni_id: [qid, ...]}` over every ledger. A Geni id may carry more than one QID."""
    out: dict[str, list[str]] = {}
    for qid, gid in identifications():
        if qid not in out.setdefault(gid, []):
            out[gid].append(qid)
    return out


def geni_for_qid() -> dict[str, list[str]]:
    """`{qid: [geni_id, ...]}` over every ledger.

    A QID with two Geni ids is the ordinary unmergeable-duplicate case — `CLAUDE.md` § *A second
    Geni ID on one item is NOT a conflict* — so this returns a list and never picks one.
    """
    out: dict[str, list[str]] = {}
    for qid, gid in identifications():
        if gid not in out.setdefault(qid, []):
            out[qid].append(gid)
    return out
