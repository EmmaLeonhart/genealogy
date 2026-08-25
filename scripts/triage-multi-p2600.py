"""Order the remaining multi-`P2600` pairs by how much a human needs to look at them.

    python scripts/triage-multi-p2600.py

**This produces a QUEUE ORDER, never a verdict.** Nothing it writes may be emitted as an edit,
and `reports/multi-p2600-verdicts.tsv` is only ever written by hand after both Geni pages have
been opened. `CLAUDE.md` deleted a whole module for deciding identity by name similarity and that
stays deleted; what is different here is the *use*. Deciding a merge from a name is banned.
Deciding **which pair to open first** from a name costs nothing if it is wrong — the pair still
gets opened, just later.

**Why it is worth doing at all.** Fourteen pairs have been opened one at a time and the pattern
did not hold still: six were two real people, then four were one person twice. Opening the
remaining 56 blind is 115 page loads in an order that carries no information. `reports/
display-names.csv` already holds every `NAME` record from the merge plus the Wikidata English
label, so the cheap read is free and available now.

**What the signals are, and what each is worth.**

* `SAME-TOKENS` — the two display names share every meaningful token after folding case,
  whitespace and punctuation. `Владимир-Димитрий Всеволодович` against
  `Владимир-Дмитрий Всеволодович` differs by one letter inside a name.
* `SAME-CJK` — the Han characters match while the romanisation does not. `韋瑱 Wei Zhen` and
  `韋瑱 Wei Tian` are one man written twice; the reading is the transcriber's choice, the
  characters are the record.
* `DIFFERENT-PATRONYMIC` — both names carry a Slavic patronymic and the patronymics differ.
  *Vladimir Glebovich* and *Vladimir Rostislavich* are two men, and this is the one signal here
  that argues for **two people** rather than one.
* `PLACEHOLDER` — at least one side is a marker rather than a name: `NN`, `Private`, `?`, and
  the CJK forms `李氏` *the Li woman* and `某` *someone*, which were found in this very batch and
  which `CLAUDE.md`'s NN population does not yet list. **No name test means anything here** and
  the pair must be judged on structure and dates alone.
* `UNCLEAR` — everything else. These are the ones worth a human first.

**Diacritics are never folded.** `CLAUDE.md`: a diacritic makes a different name, and folding it
away invented ambiguity for 1,312 names. Only case, whitespace and punctuation fold.

Writes `reports/multi-p2600-triage.tsv`.
"""
from __future__ import annotations

import collections
import csv
import re
import sys
import unicodedata
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
csv.field_size_limit(1 << 30)
ROOT = Path(__file__).resolve().parent.parent

#: Markers, not names. The CJK pair was found on 2026-08-25 among Emperor Xuanzong's daughters,
#: all bulk-loaded from CBDB: `李氏` reads "the Li woman" and `某` reads "someone".
PLACEHOLDERS = {"nn", "n.n.", "n n", "private", "<private>", "ukjent", "?", "???", "unknown",
                "李氏", "某", "李某", "李公主"}

#: Slavic patronymic endings. Deliberately narrow: this signal argues that a pair is TWO people,
#: which is the direction that keeps a pair in the queue rather than dropping it.
PATRONYMIC = re.compile(r"\w+(?:ович|евич|овна|евна|ovich|evich|ovna|evna|owicz|ewicz)$",
                        re.IGNORECASE)

NOISE = {"of", "the", "de", "von", "van", "af", "af.", "и", "ii", "iii", "iv", "prince",
         "princess", "duke", "king", "queen", "count", "lord", "sir", "lady", "duchess"}


def han(s):
    return {c for c in s if "一" <= c <= "鿿"}


def tokens(s):
    """Case, whitespace and punctuation fold. Diacritics do NOT."""
    s = unicodedata.normalize("NFC", s or "")
    parts = re.split(r"[\s,./()\[\]\"'`【】]+", s.casefold())
    return {p.strip("-–—") for p in parts if p and p not in NOISE and len(p) > 1}


def main():
    targets = list(csv.DictReader(open(ROOT / "reports" / "multi-p2600-targets.tsv",
                                       encoding="utf-8"), delimiter="\t"))
    judged = {r["qid"] for r in csv.DictReader(
        open(ROOT / "reports" / "multi-p2600-verdicts.tsv", encoding="utf-8"), delimiter="\t")}
    todo = [r for r in targets if r["qid"] not in judged]
    print(f"{len(targets)} targets, {len(judged)} already opened, {len(todo)} to triage")

    want = {g for r in todo for g in r["geni_ids"].split(";")}
    names = collections.defaultdict(list)
    wd_label = {}
    with open(ROOT / "reports" / "display-names.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["geni_id"] in want:
                d = (row.get("display_name") or "").strip()
                if d:
                    names[row["geni_id"]].append(d)
                if row.get("wikidata_en"):
                    wd_label.setdefault(row["qid"], row["wikidata_en"])

    rows = []
    for r in todo:
        gs = r["geni_ids"].split(";")
        joined = [" / ".join(dict.fromkeys(names.get(g, []))) for g in gs]
        toks = [tokens(j) for j in joined]
        hans = [han(j) for j in joined]

        flat = " ".join(joined).casefold()
        if any(p in flat for p in PLACEHOLDERS) or any(not t for t in toks):
            signal, why = "PLACEHOLDER", "a marker, not a name - judge on structure and dates"
        elif all(hans) and len(set(map(frozenset, hans))) == 1:
            signal, why = "SAME-CJK", "identical Han characters, different romanisation"
        elif len(toks) == 2 and toks[0] and toks[0] == toks[1]:
            signal, why = "SAME-TOKENS", "every meaningful token matches"
        elif len(toks) == 2 and toks[0] & toks[1] and (
                len(toks[0] ^ toks[1]) <= 2 and min(len(toks[0]), len(toks[1])) >= 2):
            signal, why = "NEAR-TOKENS", "shares tokens, differs by one or two"
        else:
            pats = [{t for t in tk if PATRONYMIC.match(t)} for tk in toks]
            if all(pats) and not (pats[0] & pats[1]):
                signal, why = "DIFFERENT-PATRONYMIC", "different fathers named in the names"
            else:
                signal, why = "UNCLEAR", "no cheap read - open this one first"

        rows.append({
            "look_first": "yes" if signal in ("UNCLEAR", "PLACEHOLDER",
                                              "DIFFERENT-PATRONYMIC") else "no",
            "signal": signal, "provisional_reading": why,
            "qid": r["qid"], "wikidata_label": wd_label.get(r["qid"], ""),
            "shares_father": r["shares_father"],
            "geni_a": gs[0], "name_a": joined[0][:80],
            "geni_b": gs[1] if len(gs) > 1 else "", "name_b": joined[1][:80] if len(gs) > 1 else "",
        })

    order = {"UNCLEAR": 0, "PLACEHOLDER": 1, "DIFFERENT-PATRONYMIC": 2,
             "NEAR-TOKENS": 3, "SAME-TOKENS": 4, "SAME-CJK": 5}
    rows.sort(key=lambda r: (order[r["signal"]], r["qid"]))

    dest = ROOT / "reports" / "multi-p2600-triage.tsv"
    with open(dest, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter="\t")
        w.writeheader()
        w.writerows(rows)

    print(f"\nwrote {dest.relative_to(ROOT)}  -- A QUEUE ORDER, NOT A VERDICT\n")
    tally = collections.Counter(r["signal"] for r in rows)
    for k in order:
        if tally[k]:
            print(f"   {tally[k]:>3}  {k}")
    first = sum(1 for r in rows if r["look_first"] == "yes")
    print(f"\n{first} need a human eye before anything else; {len(rows) - first} have a cheap "
          f"read that still has to be confirmed on the pages")


if __name__ == "__main__":
    main()
