"""The `ja` step: a Japanese label for every individual, or `unknown`.

    py scripts/build-ja-labels.py

**Her order, `queue.md` § LABELS:** `en`, then `mul`, then **`ja`**, then `zh`, then the rest —
each one step over the whole population.

**Emma, 2026-09-02, on the objection this file removes:** *"Wtf lol that's why we have katakana
facepalm"*. The `ja` work had been held back because a generated Japanese label would come out
`Gerard Spencerの娘`, mixing scripts, and the `NN` batch excludes `ja` and `zh` for exactly that
reason. **Katakana is the answer and always was** — a European name has a Japanese form, and the
only question is where to get it.

## Where the katakana comes from, and it is NOT generated

**Wikidata's own name items**, the same source the romanisation reads in the other direction.
`out/wikidata/name-items-in-store.tsv` holds 801,475 name items, of which **37,659 carry a
katakana label**, giving **33,390 distinct Latin tokens with a sourced Japanese form** —
`Karolína` カロリーナ, `Włodzimierz` ヴウォジミェシュ, `Kevin` ケヴィン.

Nothing here transliterates. `CLAUDE.md` records why: established Japanese spellings of European
names are conventional rather than derivable, and syllabification and long vowels both have real
failure modes. A token with no sourced form is a token this step does not render.

## Coverage, measured over the 1,235,948 Latin-labelled people

    every token has a katakana form   144,400   11.7%   <- emitted
    some tokens have one              863,026   69.8%   <- NOT emitted
    no token has one                  228,522   18.5%

**A partly-rendered name is not emitted**, per § *partial is worse than absent*: half a label in
katakana and half in Latin is not a name anybody has. The one exception is a middle initial, which
`labels.transliterate_token` keeps as its Latin letter in every language — Emma's 2026-08-27
ruling, ジョン・F・スミス.

**The 863,026 partials are mostly a STORE-COVERAGE gap, not a language problem.** The commonest
unrendered tokens are `von` (44,703), `of`, `y`, `af` — particles rather than names — and then
ordinary given names like `Carl` (14,141), `Anders` (13,916) and `John` (10,916), which have
katakana on Wikidata but no name item inside this Geni-shaped slice of it. Fetching those is a
bounded follow-up, not a blocker.

**A Han-named person already has a `ja` label: the name as written.** Emma: *"If the name is
solely in kanji, then the Chinese and Japanese labels are both the same for it."*

Writes `reports/label-ja.tsv`.
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
NAME_ITEMS = ROOT / "out" / "wikidata" / "name-items-in-store.tsv"
FETCHED = ROOT / "reports" / "katakana-name-items.tsv"
OUT = ROOT / "reports" / "label-ja.tsv"

#: Katakana, the長音符 and the middle dot. A label made only of these is a Japanese rendering
#: of a foreign name. Written as escapes for the reason in `build-han-readings.py`.
KATAKANA = re.compile(r"[\u30A0-\u30FF\u31F0-\u31FF\u3005\u30FB]+$".replace("[", "^["))
HAN = re.compile(r"[\u3400-\u4DBF\u4E00-\u9FFF\uF900-\uFAFF]")
LATIN_TOKEN = re.compile(r"^[A-Za-zÀ-ɏ'.-]+$")

#: Japanese writes a foreign personal name with a middle dot between its parts.
NAKAGURO = "・"


def katakana_table():
    """`{latin token casefolded: katakana}` from Wikidata's name items."""
    table = {}
    if not NAME_ITEMS.exists():
        return table
    with io.open(NAME_ITEMS, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh, delimiter=TAB):
            labs = [x for x in (r.get("labels") or "").split("|") if x]
            kana = [x for x in labs if KATAKANA.match(x)]
            if not kana:
                continue
            for lat in labs:
                if LATIN_TOKEN.match(lat):
                    table.setdefault(lat.casefold(), kana[0])
                    break
    return table


def main() -> int:
    if not DERIVED.exists():
        print("no %s" % DERIVED.relative_to(ROOT), file=sys.stderr)
        return 1
    table = katakana_table()
    n_store = len(table)
    # **The fetched table, from `scripts/fetch-katakana-name-items.py`.** Our slice of Wikidata
    # was downloaded for a different purpose and simply lacks name items for ordinary given
    # names -- `Carl`, `John`, `Anders` -- so the commonest blockers were absent for no reason
    # of language. These come from the same place (Wikidata's own name items), by SPARQL rather
    # than from the local file. An ambiguous token is recorded there and NOT used, so anything
    # in the `katakana` column here is a single unambiguous form.
    if FETCHED.exists():
        with io.open(FETCHED, encoding="utf-8", newline="") as fh:
            for r in csv.DictReader(fh, delimiter=TAB):
                if r.get("state") == "single" and r.get("katakana"):
                    table.setdefault(r["token"].casefold(), r["katakana"])
    print("%s Latin tokens carry a sourced katakana form (%s from the store, %s fetched)"
          % (format(len(table), ","), format(n_store, ","), format(len(table) - n_store, ",")))
    if not table:
        print("no name-item table; nothing can be rendered", file=sys.stderr)
        return 1
    # `transliterate_token` takes a `{token: (ja, zh)}` table and handles the middle initial.
    pairs = {k: (v, "") for k, v in table.items()}

    rows, tally = [], collections.Counter()
    with io.open(DERIVED, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            g = r["geni_id"]
            cjk = (r.get("cjk_names") or "").strip()
            en = (r.get("label_en") or "").strip()

            if cjk and HAN.search(cjk):
                # Her rule: a name written solely in kanji IS the Japanese label.
                tally["from the Han name, written as it stands"] += 1
                rows.append([g, r.get("qid", ""), cjk, en, "from the Han name, as written"])
                continue
            if not en:
                tally["unknown: no English label to render"] += 1
                rows.append([g, r.get("qid", ""), "", en, "unknown: no English label to render"])
                continue

            toks = en.split()
            if not all(LATIN_TOKEN.match(t) for t in toks):
                tally["unknown: the label is not plain Latin"] += 1
                rows.append([g, r.get("qid", ""), "", en, "unknown: the label is not plain Latin"])
                continue

            out = []
            for t in toks:
                # **The RAW token first, casefolded only as a fallback.** `transliterate_token`
                # keeps a middle initial as its Latin letter and never changes case -- Emma's
                # 2026-08-27 ruling, ジョン・F・スミス. Casefolding before the call defeated that:
                # `Susannah H. Bates` came out `スザンナ・h・ベイツ`, a lowercase initial nobody
                # writes. The table is keyed casefolded, so the fallback still finds names.
                ja, _zh = L.transliterate_token(t, pairs)
                if ja is None:
                    ja, _zh = L.transliterate_token(t.casefold(), pairs)
                out.append(ja)
            if all(out):
                tally["rendered in katakana"] += 1
                rows.append([g, r.get("qid", ""), NAKAGURO.join(out), en, "rendered in katakana"])
            elif any(out):
                tally["unknown: only SOME tokens render, so none is emitted"] += 1
                rows.append([g, r.get("qid", ""), "", en,
                             "unknown: only some tokens render"])
            else:
                tally["unknown: no token has a katakana form"] += 1
                rows.append([g, r.get("qid", ""), "", en, "unknown: no token renders"])

    with io.open(OUT, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter=TAB, lineterminator="\n")
        w.writerow(["geni_id", "qid", "label_ja", "label_en", "state"])
        w.writerows(rows)

    print("\nwrote %s - %s people" % (OUT.relative_to(ROOT), format(len(rows), ",")))
    for k, v in tally.most_common():
        print("   %-52s %9s" % (k, format(v, ",")))
    got = sum(1 for r in rows if r[2])
    print("\n%s carry a ja label; %s are unknown and rostered"
          % (format(got, ","), format(len(rows) - got, ",")))
    print("%s of the labelled ones already have a Wikidata item"
          % format(sum(1 for r in rows if r[1] and r[2]), ","))
    print("\na sample of the katakana renderings:")
    n = 0
    for r in rows:
        if r[4] == "rendered in katakana":
            print("   %-34s -> %s" % (r[3][:34], r[2]))
            n += 1
            if n >= 10:
                break
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
