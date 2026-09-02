"""The `mul` step: a language-neutral label for every individual, derived from `en`.

    py scripts/build-mul-labels.py

**Her order, `queue.md` § LABELS:** *"then mul gets made for every individual (almost always
derived from en)"* — one step over the whole population, after the `en` step and before `ja`.

**`mul` IS `en` for almost everybody, and that is measured rather than assumed.** Over
`reports/derived-labels.csv`: 1,295,226 people carry both, and **1,292,928 of them are already
identical**. Wikidata's `Help:Default values for labels and aliases` makes the default label the
native full name in Latin script, which is exactly what `en` holds here. So this step is not a
transformation; it is *carrying `en` across* and then naming the exceptions.

## The exceptions, which are the actual content of this step

* **An unnamed person keeps the MARKER in `mul`.** `CLAUDE.md` § *`NN` is PRESERVED in `mul`* —
  Emma: *"NN is always preserved in the multi-language label. It just has more descriptive labels
  added in some languages for the relationships."* So `mul` is `NN Garborg` while `en` is
  `son of Arne Olaus Fjørtoft Garborg`. These are the 2,298 rows where the two already differ,
  plus 548 with no label yet.
* **A redacted person gets NO label, in either.** § *Redacted people go in* — the person is
  created and the marker never becomes a label. 94,845 of them, and their emptiness is correct
  rather than missing.
* **The `en` step's new romanisations now supply `mul`** for 5,353 people who had no label in any
  language before it ran.

## What stays unlabelled, and why that is a roster rather than a failure

22,010 people have no `NAME` record at all, and 33,982 have a name nothing has derived a label
from — overwhelmingly CJK and Hangul forms outside the `en` step's reach (`光安正室 /斎藤/`,
`씨 /이/`). Emma, 2026-09-02: *"just list these as unknowns if they are unclear"*. They are listed.

Writes `reports/label-mul.tsv`.
"""
from __future__ import annotations

import collections
import csv
import io
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
csv.field_size_limit(1 << 30)

import labels as L  # noqa: E402

TAB = chr(9)
DERIVED = ROOT / "reports" / "derived-labels.csv"
DISPLAY = ROOT / "reports" / "display-names.csv"
EN_STEP = ROOT / "reports" / "label-en.tsv"
OUT = ROOT / "reports" / "label-mul.tsv"

#: Any character that is a letter or a digit in ANY script. A label with none of these is
#: punctuation and cannot be somebody's name.
WORD = re.compile(r"[^\W_]", re.UNICODE)


def main() -> int:
    for p in (DERIVED, DISPLAY):
        if not p.exists():
            print("no %s" % p.relative_to(ROOT), file=sys.stderr)
            return 1

    en_step = {}
    if EN_STEP.exists():
        with io.open(EN_STEP, encoding="utf-8", newline="") as fh:
            for r in csv.DictReader(fh, delimiter=TAB):
                if r["label_en"]:
                    en_step[r["geni_id"]] = r["label_en"]
    print("%s labels from the en step" % format(len(en_step), ","))

    # **`name_records` in derived-labels.csv is a COUNT, not the records.** Reading it as a name
    # made `is_redacted("1")` the question and produced a categorisation of the whole unlabelled
    # population that meant nothing. The raw GEDCOM name lives here instead.
    raw = {}
    with io.open(DISPLAY, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            raw.setdefault(r["geni_id"], r.get("name_raw", ""))
    print("%s raw names" % format(len(raw), ","))

    rows, tally = [], collections.Counter()
    with io.open(DERIVED, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            g = r["geni_id"]
            en = (r.get("label_en") or "").strip()
            mul = (r.get("label_mul") or "").strip()
            name = raw.get(g, "")

            if mul and en and mul != en:
                state, value = "kept: mul differs from en on purpose (a marker)", mul
            elif mul:
                state, value = "kept: mul already equals en", mul
            elif g in en_step:
                state, value = "NEW: derived from the en step", en_step[g]
            elif en:
                state, value = "NEW: carried across from en", en
            elif name and L.is_redacted(name):
                state, value = "none: redacted, correctly has no label", ""
            elif name and L.is_unnamed(name):
                # **The marker is preserved -- but punctuation is not a marker.** `CLAUDE.md`
                # § *An obvious unknown-word marker goes straight in* draws the line in her
                # words: **words yes, punctuation no**. `label_for` empties only `Private` and
                # `<private>`, so without this a bare `?` (228 people), `???` (148), `*` (29),
                # `.` (8) and `--` (1) go out as labels -- an item asserting a person is called
                # "?". A word that MEANS unknown is different and is kept as written: 未知 (23)
                # and `Без име` (18) are real statements that the name is not known, and
                # § *`NN` is PRESERVED in `mul`* says a marker is never removed.
                got = L.label_for(name)
                if got and not WORD.search(got):
                    state, value = "NEW: unnamed, punctuation replaced by the NN marker", "NN"
                else:
                    state, value = "NEW: unnamed, marker preserved in mul", got or "NN"
            elif not name:
                state, value = "none: no NAME record at all", ""
            else:
                state, value = "unknown: has a name, nothing derived a label", ""
            # **A final guard, applied to EVERY branch rather than only the unnamed one.**
            # 34 labels reached this point carrying no word character at all, and they did not
            # come from the branch above -- they were already in `derived-labels.csv`:
            #
            #  * **27 are invisible.** `‏‏‎ ‎ /姜姓/` is U+200F RIGHT-TO-LEFT MARK and U+200E
            #    LEFT-TO-RIGHT MARK with spaces, which render as nothing. An item labelled with
            #    those asserts a name a reader cannot see, and the SURNAME beside it (姜姓, 姬姓)
            #    is real data that was being dropped.
            #  * **7 are `???` / `??` / `??!!`**, from records like `(incognita) /???/` and
            #    `(Unknown) /???/` -- both of which `CLAUDE.md` names as unknown-name markers.
            #
            # None of the 34 carries a QID, so nothing wrong is live on Wikidata; this stops it
            # ever being emitted. § *`NN` is PRESERVED in `mul`* gives the replacement, and
            # § *a marker leading a real surname* gives the form: `unknown Bloomfield` becomes
            # `NN Bloomfield`, so a surname is kept wherever the record has one.
            if value and not WORD.search(value):
                surname = L.surname_of(name) if name else ""
                if surname and WORD.search(surname):
                    state, value = "FIXED: unreadable label, surname kept", "NN " + surname
                else:
                    state, value = "FIXED: unreadable label, no surname to keep", "NN"

            tally[state] += 1
            rows.append([g, r.get("qid", ""), value, en, name[:60], state])

    with io.open(OUT, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter=TAB, lineterminator="\n")
        w.writerow(["geni_id", "qid", "label_mul", "label_en", "name_raw", "state"])
        w.writerows(rows)

    print("\nwrote %s - %s people" % (OUT.relative_to(ROOT), format(len(rows), ",")))
    for k, v in tally.most_common():
        print("   %-46s %9s" % (k, format(v, ",")))
    new = sum(v for k, v in tally.items() if k.startswith("NEW"))
    have = sum(1 for r in rows if r[2])
    print("\n%s people gain a mul label they did not have; %s carry one in total"
          % (format(new, ","), format(have, ",")))
    with_qid = sum(1 for r in rows if r[1] and r[2] and r[5].startswith("NEW"))
    print("%s of the new ones already have a Wikidata item" % format(with_qid, ","))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
