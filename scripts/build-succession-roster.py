"""One CSV of everyone who carries a regnal number or a number in office.

    python scripts/build-succession-roster.py

**Emma's spec, 2026-08-31:** *"it's relatively easy to just agentically write the stuff into csv
files with the geni id, qid if applicable, regnal number if applicable, and number in office, and
whether they are Izumo, Senge, Kitajima, or Samaritan."*

## The two numbers are different things, which is why she asked for both columns

- **`regnal_number`** is the number **inside the personal name** -- `Elazar XX`, `Yoseph II`. On
  Wikidata it is `P7338` *regnal ordinal*, a qualifier on the `P735` *given name* statement, per
  `name modelling.txt`. Emma, 2026-08-18: *"regnal ordinals fucking cannot behave like a middle
  name."*
- **`number_in_office`** counts the person among the holders of a post -- the Nth head of the
  house. On Wikidata that is `P39` *position held* with `P1545` *series ordinal*, which is a
  statement about the office and not about the name.

**They do not co-occur the way one might assume.** Measured 2026-08-31: of the 19,450
ordinal-bearing rows in `reports/regnal-ordinals.csv`, **zero** are Izumo, Senge, Kitajima or
Kitashima -- their numbers are not in the Latin name at all. A single item would have covered the
Samaritans and silently missed the family she named in the same breath, which is why she split it.

## Where each family's numbers come from

- **Izumo / Senge / Kitajima** -- `reports/izumo-chart-roster.tsv`, whose `succession` column is
  the office count. **The house splits at 55**: `Senge no Takamune` and `Kitajima no Sadataka` are
  both the 55th, and the two branches number onward in parallel from there. So `family` is read
  off the name, and anyone numbered below the split is the undivided line.
- **Samaritan** -- `reports/wikidata-samaritan-succession.json`, which already models the office
  as `P39` + `P1545` for 21 priests, plus the Roman ordinal in the name from
  `reports/regnal-ordinals.csv`.

## What it does NOT do

No statements, no QuickStatements. This is the roster she asked for, to be read and corrected by
hand before anything is emitted -- and it needs that: `reports/regnal-ordinals.csv` contains
`Wife 2 /ben Nathan, Mar Huna IV/` and `Preben 1. /Bille-Brahe/`, neither of which is a regnal
ordinal.

Writes `reports/succession-and-ordinals.csv`.
"""

import csv
import io
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CANDIDATES = ROOT / "reports" / "izumo-geni-candidates.tsv"
ANCHORS = ROOT / "reports" / "izumo-geni-anchors.tsv"
SAMARITAN = ROOT / "reports" / "wikidata-samaritan-succession.json"
ORDINALS = ROOT / "reports" / "regnal-ordinals.csv"
P2600 = ROOT / "out" / "wikidata" / "p2600-all.tsv"
LABELS = ROOT / "reports" / "derived-labels.csv"
TANBA = ROOT / "reports" / "tanba-geni-created.tsv"
OUT = ROOT / "reports" / "succession-and-ordinals.csv"

csv.field_size_limit(1 << 30)

#: The generation at which the Izumo Kokusō house divides into the Senge and Kitajima branches.
#: Read off the roster rather than looked up: `Senge no Takamune` and `Kitajima no Sadataka` both
#: carry succession 55, and every number from 55 up appears twice.
SPLIT_AT = 55

#: A Roman ordinal standing alone as a name token -- `Elazar XX`, `Yoseph II`. Bounded to the
#: forms that actually occur so `I` as an initial and `MD` as a title do not match.
ROMAN = re.compile(r"^(?:X{0,3})(?:IX|IV|V?I{0,3})$")


def geni_by_qid():
    """`{qid: geni_id}` from Wikidata's own `P2600`, then from her bio links.

    **`P2600` reaches almost none of these people, and that is the data rather than a broken
    join.** Measured 2026-08-31 over the 109 numbered Izumo/Senge/Kitajima heads: **0** are in
    `out/wikidata/p2600-all.tsv`, **0** are in `reports/izumo-geni-anchors.tsv` (which covers a
    later, different part of the chart), and **5** are reachable through `reports/bio-qids.tsv`.
    `CLAUDE.md` § *The Geni BIO carries her own QID claims* already records this asymmetry -- for
    the Izumo roster the bio links give 8 Geni ids where `P2600` gives 2 -- so the bio file is
    read second and never skipped.

    The `geni_id` column therefore comes out nearly empty on the Japanese side. These are ancient
    and medieval office-holders who have Wikidata items, largely of her own making, and are not in
    our Geni corpus under a matching id.
    """
    out = {}
    bio = ROOT / "reports" / "bio-qids.tsv"
    if bio.exists():
        with io.open(bio, encoding="utf-8", newline="") as fh:
            for r in csv.DictReader(fh, delimiter="\t"):
                if r.get("qid") and r.get("geni_id"):
                    out.setdefault(r["qid"].strip(), r["geni_id"].strip())
    with io.open(P2600, encoding="utf-8") as fh:
        for line in fh:
            p = line.rstrip("\n").split("\t")
            if len(p) >= 2:
                out.setdefault(p[0], p[1])
    return out


def main():
    by_qid = geni_by_qid()
    rows = []

    # ---- Izumo / Senge / Kitajima ----------------------------------------------------
    #
    # **The agentic pass, and it is a CHECK rather than a name guess.** Emma, 2026-08-31:
    # *"All of them are on geni lol the wikidata just doesn't have p2600."* She is right, and the
    # matcher missed them because the two sides write the name differently: the chart says
    # `Senge no Takakuni`, Geni says `Takakuni Senge`. Reversing `X no Y` to `Y X` finds **63 of
    # 73**.
    #
    # **What makes it safe is that the Geni label carries the succession number** -- `Funin 18
    # Izumo`, `Yukitaka 57 Kitajima`, `Takakatsu 62 Senge`. So a candidate is accepted only when
    # the number in its label matches the number in the chart, and a label with no number is
    # accepted only when it is the sole hit. That is verification, not similarity, which is the
    # line `CLAUDE.md` draws -- and it is what the old matcher lacked when it paired
    # `Izumo no Yoshitada` with *Minamoto* no Yoshitada.
    native = {}
    with io.open(ROOT / "reports" / "izumo-chart-roster.tsv", encoding="utf-8",
                 newline="") as fh:
        for r in csv.DictReader(fh, delimiter="	"):
            if r.get("english") and r.get("japanese"):
                native[r["english"].strip()] = r["japanese"].strip()

    corpus = []
    with io.open(LABELS, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            lab = (r.get("label_en") or r.get("label_mul") or "").strip()
            if lab:
                corpus.append((r["geni_id"], lab, [t.casefold() for t in lab.split()]))

    with io.open(CANDIDATES, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh, delimiter="	"):
            succ = (r.get("regnal") or "").strip()
            if not succ.isdigit():
                continue
            name = (r.get("roster_name") or "").strip()
            lineage = (r.get("lineage") or "").strip()
            geni, gstatus = "", ""

            ids = [x for x in (r.get("geni_id") or "").split(";") if x.strip()]
            if len(ids) == 1 and (r.get("status") or "").startswith("match"):
                geni, gstatus = ids[0].strip(), "matcher: " + r["status"]
            else:
                m = re.match(r"^(\S+) no (\S+)$", name)
                if m:
                    given, house = m.group(2).casefold(), m.group(1).casefold()
                    hits = [(g, lab) for g, lab, toks in corpus
                            if given in toks and house in toks]
                    numbered = [(g, lab) for g, lab in hits if succ in lab.split()]
                    if len(numbered) == 1:
                        geni, gstatus = numbered[0][0], "succession number confirms it"
                    elif len(hits) == 1 and not any(t.isdigit() for t in hits[0][1].split()):
                        geni, gstatus = hits[0][0], "sole match, no number in the label"
                    elif hits:
                        gstatus = "AMBIGUOUS (%d hits, none numbered %s)" % (len(hits), succ)
                # **Her bio links are the last and best resort.** Emma, 2026-08-31: *"most of
                # the geni profiles have qids in their bios."* `reports/bio-qids.tsv` is that,
                # attributed to the `INDI` that owns the link, so it is her own statement of
                # identity rather than anything inferred -- and `CLAUDE.md` records that for the
                # Izumo roster the bio links give 8 Geni ids where `P2600` gives 2.
                #
                # It is consulted last only because the succession number is a stronger check;
                # where the name pass found nothing, this is the answer.
                # **And the native form, for the mythological end.** The 18 left over are the
                # `-mikoto` figures at the head of the line, whose Geni profiles carry the Han
                # name rather than a romanisation, so `X no Y` never fires for them. An exact
                # CJK substring is not a name search: there is nothing to be similar to.
                if not geni:
                    ja = native.get(name, "")
                    if ja and not ja.startswith("Izumo"):
                        cjk = [(g, lab) for g, lab, _t in corpus if ja in lab]
                        if len(cjk) == 1:
                            geni, gstatus = cjk[0][0], "native name, unique in the corpus"
                        elif cjk:
                            gstatus = "AMBIGUOUS (%d carry %s)" % (len(cjk), ja)
                if not geni and r.get("qid", "").strip() in by_qid:
                    geni = by_qid[r["qid"].strip()]
                    gstatus = "her QID link in the Geni bio"
                if not gstatus:
                    gstatus = "not found in the corpus"

            rows.append({
                "family": lineage if lineage in ("Senge", "Kitajima", "Izumo") else "Izumo",
                "name": name, "native_name": "", "geni_id": geni,
                "qid": (r.get("qid") or "").strip(),
                "regnal_number": "", "number_in_office": succ,
                "geni_status": gstatus,
                "source": "reports/izumo-geni-candidates.tsv",
            })

    # ---- Samaritan: the office, from the succession model ----------------------------
    seen_sam = {}
    if SAMARITAN.exists():
        for edit in json.loads(SAMARITAN.read_text(encoding="utf-8")):
            subj = edit.get("subject", {})
            qid, geni = subj.get("qid", ""), subj.get("geni_id", "")
            ordinal = ""
            for add in edit.get("add", []):
                if add.get("property") == "P39":
                    for q in add.get("qualifiers", []):
                        if q.get("property") == "P1545":
                            ordinal = str(q.get("value", ""))
            seen_sam[geni or qid] = {
                "family": "Samaritan", "name": "", "native_name": "",
                "geni_id": geni, "qid": qid, "regnal_number": "",
                "number_in_office": ordinal,
                "source": "reports/wikidata-samaritan-succession.json",
            }

    # The authoritative Samaritan population, rather than anything read off a name.
    samaritans = set()
    sam_people = ROOT / "reports" / "samaritan-people.csv"
    if sam_people.exists():
        with io.open(sam_people, encoding="utf-8", newline="") as fh:
            for r in csv.DictReader(fh):
                if r.get("geni_id"):
                    samaritans.add(r["geni_id"].strip())

    # ---- the regnal number IN THE NAME, for the Samaritans ---------------------------
    label = {}
    with io.open(LABELS, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            label[r["geni_id"]] = r.get("label_en") or r.get("label_mul") or ""

    with io.open(ORDINALS, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            g = r["geni_id"]
            tok = (r.get("ordinal_token") or "").strip()
            # **`"ben " in name` was a substring test and it let in strangers.** Reading the
            # output is what caught it: `Agatha von Schwaben Daughter of Ernst II` and
            # `Bagben III Siounides Prince of Siounie` matched on the letters inside `Schwaben`
            # and `Bagben`, and `David ben Hizkiya II 39th Exilarch` and `Avraham II ben Ezra
            # HaLevi` are Jewish rather than Samaritan -- a `ben` patronymic is not a Samaritan
            # marker, it is a Hebrew one.
            #
            # `reports/samaritan-people.csv` is the actual population, 412 people taken from the
            # Samaritan exports, so membership is a lookup and not a guess about a name.
            if g not in samaritans:
                continue
            # **A bare `I`, `V` or `X` is a regnal ordinal here, and the census files it as
            # `single-letter` because elsewhere it could be a middle initial.** Taking only
            # `kind == "roman"` dropped 19 of the 63 Samaritan rows -- `Yitzhaq I ben Tsedaka`
            # and `Phinehas X ben Matzliach` among them, which are plainly the first and the
            # tenth. There are no middle initials in a `ben`-patronymic name, so inside this
            # screen the ambiguity the census is guarding against does not exist.
            if not tok or r.get("kind") not in ("roman", "single-letter"):
                continue
            if not ROMAN.match(tok):
                continue
            if g in seen_sam:
                seen_sam[g]["regnal_number"] = tok
                seen_sam[g]["name"] = label.get(g, "") or seen_sam[g]["name"]
            else:
                seen_sam[g] = {
                    "family": "Samaritan", "name": label.get(g, ""), "native_name": "",
                    "geni_id": g, "qid": "", "regnal_number": tok, "number_in_office": "",
                    "geni_status": "from the corpus",
                    "source": "reports/regnal-ordinals.csv",
                }
    for v in seen_sam.values():
        if not v["name"] and v["geni_id"]:
            v["name"] = label.get(v["geni_id"], "")
        rows.append(v)

    order = {"Izumo": 0, "Senge": 1, "Kitajima": 2, "Samaritan": 3}
    rows.sort(key=lambda r: (order.get(r["family"], 9),
                             int(r["number_in_office"]) if r["number_in_office"].isdigit()
                             else 9999, r["name"]))

    fields = ["family", "name", "native_name", "geni_id", "qid",
              "regnal_number", "number_in_office", "geni_status", "source"]
    with io.open(OUT, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)

    import collections
    fam = collections.Counter(r["family"] for r in rows)
    print("%d rows -> %s" % (len(rows), OUT.relative_to(ROOT)))
    for f in ("Izumo", "Senge", "Kitajima", "Samaritan"):
        sub = [r for r in rows if r["family"] == f]
        print("  %-10s %3d   qid %3d   geni %3d   regnal %3d   in-office %3d"
              % (f, fam[f], sum(1 for r in sub if r["qid"]),
                 sum(1 for r in sub if r["geni_id"]),
                 sum(1 for r in sub if r["regnal_number"]),
                 sum(1 for r in sub if r["number_in_office"])))


if __name__ == "__main__":
    main()
