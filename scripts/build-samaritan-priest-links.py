"""Link the Samaritan high priests Emma listed by QID to their Geni profiles.

**`samaritans/priests.txt` is the file this exists for, and it was missed.**
Emma, 2026-08-16: *"I literally gave you a list of the QIDs, a list of names of
High Priests and QIDs of them… It's in a text file called highpreests or
something! It's kind of an isolated thing that just has a bunch of names and
QIDs in it. You should have found it!"* Queue item 2 was reported as blocked on
finding these QIDs while the file sat in `samaritans/` at the repo root, which was
never searched. The blocker did not exist.

**Her instruction for what to do with them**, `samaritans/wikidata.txt`: *"they
both lack geni items and are kind of improperly linked. I want you to do manual
links to the geni in the same way that we did on the Empress Jingū item."*

**Matching by name here is correct, and is not the thing this repo forbids.**
`correspondence.md` bans *searching Wikidata* for a name — an open-ended query
over 100M items. This is the opposite: a **closed list of 21 people Emma wrote
down herself**, matched against the Samaritan exports, which she pointed at
directly — *"In the small original 33-person High Priest gedcom, all of these
individuals are present… You have the ability to look through the 33-person tree
pretty easily to find which QIDs appear to match, and then just match them up."*
The candidate set is bounded and hand-curated on both sides.

**The leading name must agree exactly.** A Samaritan name is
`<own name> ben <father> ben <grandfather>`, so the first token is the person and
the rest is their lineage. Requiring it to match stops `Levi ben Abisha` pairing
with `Levi V ben Abram`. Everything after it is scored by shared tokens, and the
match basis is recorded per row so a reviewer can see *why*.

**The differences are spelling and regnal numerals**, not identity: `Phinhas` vs
`Phinehas`, `Yittzhaq` vs `Yitzhaq`, `Ab-Chisda` vs `Ab-Hisda`, and Geni carrying
`Yoseph II` / `Levi VI` / `Elazar XX` / `Aharon IV` / `Aabed-El V` where Wikidata
has no numeral.

Writes `reports/samaritan-priest-links.csv` — every one of the 21, matched or not
— and `reports/wikidata-samaritan-links.json`, the `add_geni_id` edits.

    py scripts/build-samaritan-priest-links.py
"""

from __future__ import annotations

import csv
import glob
import json
import re
import sqlite3
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

LIST = REPO / "samaritans" / "priests.txt"
INDEX = REPO / "out" / "wikidata" / "store-index.sqlite3"
CSV_OUT = REPO / "reports" / "samaritan-priest-links.csv"
JSON_OUT = REPO / "reports" / "wikidata-samaritan-links.json"

INDI = re.compile(r"^0 @I(\d+)@ INDI")
NAME = re.compile(r"^1 NAME (.*)$")

#: Dropped before comparing: the patronymic connector, and the honorific suffix
#: that appears on some names and not their counterparts.
NOISE = {"ben", "bin", "the", "wikidata"}


def tokens(text: str) -> list[str]:
    text = re.sub(r"\bha'?[a-zåäöÀ-ɏ]+\b", " ", text.lower())
    text = re.sub(r"[^a-z0-9 ]", " ", text)
    return [t for t in text.split() if t not in NOISE]


def samaritan_people() -> dict[str, str]:
    people: dict[str, str] = {}
    for path in sorted(glob.glob(str(REPO / "exports" / "samaritans" / "*.ged"))):
        gid = ""
        with open(path, encoding="utf-8-sig", errors="replace") as fh:
            for line in fh:
                m = INDI.match(line)
                if m:
                    gid = m.group(1)
                    continue
                n = NAME.match(line)
                if n and gid and gid not in people:
                    people[gid] = n.group(1).strip().replace("/", "")
    return people


#: Links Emma gave directly, which no match over the exports could find.
#:
#: `Q137394557 Yitzhaq I ben Tsedaka` had no counterpart: the only Geni `Yitzhaq`
#: in the Samaritan exports has `Shalma II ben Tabia` for a father, and no
#: Yitzhaq with a Tsedaka father existed anywhere in them. Emma, 2026-08-16, with
#: the profile: *"this is the person for the qid to correspond to."* The profile
#: is **not in any of the 203 exports** — she created it on Geni after the last
#: Samaritan export ran — so the link is recorded here and the person arrives
#: with her next export. Hand-given identity, same standing as
#: `entity_resolution.md`.
GIVEN_BY_EMMA = {
    "Q137394557": ("6000000227245553985", "Yitzhaq I ben Tsedaka"),
}


def main() -> int:
    if not LIST.exists():
        print(f"no {LIST}", file=sys.stderr)
        return 1

    wanted = []
    for line in LIST.read_text(encoding="utf-8").splitlines():
        if "|" not in line:
            continue
        url, label = line.split("|", 1)
        qid = url.strip().rsplit("/", 1)[-1]
        name = label.replace(" - Wikidata", "").strip()
        if re.fullmatch(r"Q\d+", qid):
            wanted.append((qid, name))
    print(f"{len(wanted)} priests listed in {LIST.relative_to(REPO)}")

    people = samaritan_people()
    print(f"{len(people):,} distinct people in the Samaritan exports")

    linked = {}
    if INDEX.exists():
        conn = sqlite3.connect(INDEX)
        for qid, gid in conn.execute("select qid, geni_id from geni"):
            linked.setdefault(qid, set()).add(gid)
        conn.close()

    rows, edits = [], []
    matched = 0
    for qid, name in wanted:
        want = tokens(name)
        best = None
        for gid, geni_name in people.items():
            have = tokens(geni_name)
            if not have or not want or have[0] != want[0]:
                continue
            shared = len(set(want) & set(have))
            # Prefer the most lineage in common, then the shorter name: a longer
            # one carries extra generations and is a different person.
            key = (-shared, len(have))
            if best is None or key < best[0]:
                best = (key, gid, geni_name, shared)
        # **One shared token is the leading name and nothing else, which is not
        # a match.** `Q137394557 Yitzhaq I ben Tsedaka` scored 1 against a Geni
        # person called simply `Yitzhaq`, and the structure refuted it outright:
        # that Yitzhaq's father is `Shalma II ben Tabia`, not Tsedaka. No Geni
        # person in the Samaritan exports is a Yitzhaq with a Tsedaka father, so
        # this priest is genuinely absent rather than merely unmatched.
        if best is not None and best[3] < 2 and len(want) > 1:
            best = None
        if best is None and qid in GIVEN_BY_EMMA:
            gid, geni_name = GIVEN_BY_EMMA[qid]
            best = ((0, 0), gid, geni_name, -1)   # -1 marks "not matched, given"
        if best is None:
            rows.append({"qid": qid, "wikidata_name": name, "geni_id": "",
                         "geni_name": "", "shared_tokens": 0,
                         "verdict": "NO MATCH - lineage does not agree"})
            continue
        _key, gid, geni_name, shared = best
        matched += 1
        already = gid in linked.get(qid, set())
        given = shared == -1
        rows.append({"qid": qid, "wikidata_name": name, "geni_id": gid,
                     "geni_name": geni_name,
                     "shared_tokens": "" if given else shared,
                     "verdict": "already linked" if already
                     else ("add_geni_id (given by Emma, not in any export)"
                           if given else "add_geni_id")})
        if already:
            continue
        edits.append({
            "id": f"samaritan_priest_link:{qid}",
            "type": "add_geni_id",
            "source": "samaritans/priests.txt",
            "subject": {"qid": qid, "geni_id": gid},
            "requires": [],
            "statements": [{
                "property": "P2600",
                "value": gid,
                "references": [
                    {"property": "P854",
                     "value": f"https://www.geni.com/people/x/{gid}"},
                    {"property": "P813", "value": "+2026-08-16T00:00:00Z/11"},
                ],
            }],
            "wikidata_name": name,
            "geni_name": geni_name,
        })

    with CSV_OUT.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    JSON_OUT.write_text(json.dumps(edits, ensure_ascii=False, indent=1),
                        encoding="utf-8")

    print(f"\n{matched} of {len(wanted)} matched to a Geni profile")
    print(f"wrote {CSV_OUT} and {JSON_OUT} ({len(edits)} add_geni_id edits)\n")
    for r in rows:
        mark = "  " if r["verdict"] == "add_geni_id" else "! "
        print(f"{mark}{r['qid']:<12}{r['wikidata_name'][:40]:<42}"
              f"{r['geni_id'] or '-':<21}{r['verdict']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
