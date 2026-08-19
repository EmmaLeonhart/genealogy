"""Romanise Han-only names, from Wikidata's own name items.

Emma, 2026-08-18: *"I am convinced we can actually do the romanization of the CJK pretty
decently… if there's any listed place of birth, then you know which one it is. Chinese and
Korean readings are all very straightforward. Japanese readings are not straightforward,
but Chinese and Korean readings are very straightforward."*

**Both halves of that are built here, and the second half is why this works without a
transliteration library.** No `pypinyin`, no `hanja`, no `pykakasi` is installed, and her
standing instruction is against programmatic transliteration anyway — *"from CJK to English
do not remotely try to do any kind of programmatic transliteration because they all suck."*

So nothing is transliterated. **The romanisations are read out of Wikidata's own name
items**, which carry the Han form and the Latin form as labels on one item:

    Q4464775   zh 屠   en Tu       Chinese family name
    Q11983535  ja 李   ko 이  en Lee   Korean family name
    Q16884158  ja 橘   en Tachibana     Japanese family name

That is a *published* reading of that character as a name, not a guess, and it is
per-culture because the item is per-culture — 李 as a Korean family name is `Lee`, and the
Chinese item for the same character says `Li`.

## Culture first, in her order of evidence

1. **Birth place.** Her words: *"if there's any listed place of birth, then you know which
   one it is."* Strongest and checked first.
2. **Export provenance.** `reports/export-provenance.csv` plus the script mix of the
   exports a person appears in — a Han-only person inside a hangul-writing export is
   Korean. Built 2026-08-18 because the merge deliberately does not track it.
3. **Neighbours.** The scripts used by parents, children and spouses.

**Japanese is emitted separately and marked**, because she is right that its readings are
not straightforward: the same character takes different readings in different names, and a
name item only gives the reading for *that* name. A Chinese or Korean character reading is
effectively one-to-one; a Japanese one is not.

    py scripts/build-cjk-romanisation.py [--limit N]

Writes `reports/cjk-romanisation.csv` and `reports/cjk-romanisation.md`. Reads only.
"""

from __future__ import annotations

import collections
import csv
import io
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))

from genimerge import wikistore  # noqa: E402

LABELS = REPO / "reports" / "derived-labels.csv"
FACTS = REPO / "reports" / "derived-facts.csv"
FAMILY = REPO / "reports" / "derived-family.csv"
PROV = REPO / "reports" / "export-provenance.csv"
QIDS = REPO / "reports" / "name-item-qids.tsv"
STORE = REPO / "wikidata" / "items"
INDEX = REPO / "out" / "wikidata" / "store-index.sqlite3"
OUT_CSV = REPO / "reports" / "cjk-romanisation.csv"
OUT_MD = REPO / "reports" / "cjk-romanisation.md"

csv.field_size_limit(10_000_000)

HAN = re.compile(r"[㐀-鿿]")
KANA = re.compile(r"[぀-ヿ]")
HANGUL = re.compile(r"[가-힯]")
LATIN_NAME = re.compile(r"^[A-Z][A-Za-z\-']*$")

#: `P31` values that say what kind of name an item is, and for which culture.
CHINESE = {"Q1093580"}          # Chinese family name
JAPANESE = {"Q16919315", "Q17111581"}   # Japanese family name / given name
KOREAN = {"Q11420694", "Q17300640"}     # Korean family name / given name

#: Place words that settle the culture outright — her first rule.
PLACE = [
    ("zh", ("China", "Chinese", "Taiwan", "Hong Kong", "Beijing", "Shanghai", "Guangdong",
            "Fujian", "Zhejiang", "Jiangsu", "Shandong", "Sichuan", "Henan", "Hubei",
            "Hunan", "Anhui", "Shanxi", "Shaanxi", "Yunnan", "Guangxi", "Jiangxi")),
    ("ko", ("Korea", "Korean", "Seoul", "Busan", "Joseon", "Goryeo", "Silla", "Baekje",
            "Gyeongsang", "Jeolla", "Chungcheong", "Gyeonggi", "Hanyang", "Pyongyang")),
    ("ja", ("Japan", "Japanese", "Tokyo", "Kyoto", "Osaka", "Edo", "Yamato", "Musashi",
            "Owari", "Echizen", "Satsuma", "Hizen", "Kii", "Mutsu", "Shinano", "Nagano",
            "Hokkaido", "Kyushu", "Honshu", "Shikoku")),
]


def cjk_of(row: dict) -> str:
    """The first CJK name string on a record, or empty."""
    return (row.get("cjk_names") or "").split(" | ")[0].strip()


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    limit = None
    if "--limit" in sys.argv:
        limit = int(sys.argv[sys.argv.index("--limit") + 1])

    # ---- who needs romanising ------------------------------------------------
    need = {}
    scripts = {}
    with io.open(LABELS, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            cjk = cjk_of(r)
            if not cjk:
                continue
            scripts[r["geni_id"]] = cjk
            if not (r.get("label_en") or "").strip() and HAN.search(cjk):
                need[r["geni_id"]] = cjk
    print(f"people with a CJK name and no Latin label: {len(need):,}")

    # ---- culture evidence 1: birth place ------------------------------------
    culture = {}
    why = {}
    place_culture = {}
    with io.open(FACTS, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            g = r["geni_id"]
            place = f"{r.get('birth_place') or ''} {r.get('death_place') or ''}"
            if not place.strip():
                continue
            for code, words in PLACE:
                if any(w in place for w in words):
                    # kept for EVERYONE, not just the need-set: a Han-only person's
                    # culture is often settled by a relative's place rather than by
                    # their own, which is the whole point of the traversal below.
                    place_culture[g] = code
                    if g in need:
                        culture[g] = code
                        why[g] = f"place: {place.strip()[:40]}"
                    break
    print(f"  settled by a listed place: {len(culture):,}")

    # ---- culture evidence 2: export provenance ------------------------------
    prov = {}
    if PROV.exists():
        with io.open(PROV, encoding="utf-8", newline="") as fh:
            for r in csv.DictReader(fh):
                if r["geni_id"] in need:
                    prov[r["geni_id"]] = r["exports"].split(" | ")
    # what each export looks like, from the scripts its members write
    mix = collections.defaultdict(collections.Counter)
    if PROV.exists():
        with io.open(PROV, encoding="utf-8", newline="") as fh:
            for r in csv.DictReader(fh):
                s = scripts.get(r["geni_id"])
                if not s:
                    continue
                k = "ja" if KANA.search(s) else ("ko" if HANGUL.search(s) else None)
                if k:
                    for f in r["exports"].split(" | "):
                        mix[f][k] += 1
    export_culture = {}
    for f, c in mix.items():
        total = sum(c.values())
        if total >= 20:
            top, n = c.most_common(1)[0]
            if n / total >= 0.80:
                export_culture[f] = top
    settled_by_export = 0
    for g, files in prov.items():
        if g in culture:
            continue
        votes = {export_culture[f] for f in files if f in export_culture}
        if len(votes) == 1:
            culture[g] = votes.pop()
            why[g] = "export provenance"
            settled_by_export += 1
    print(f"  settled by export provenance: {settled_by_export:,}  "
          f"({len(export_culture)} export(s) characterised)")

    # ---- culture evidence 3: graph traversal ---------------------------------
    # Emma, 2026-08-18: *"graph traversal for people with unknown country there will
    # probably work for inferring nationality"*. Immediate kin is not enough -- a
    # Han-only person's parents are often Han-only too -- so this walks outward and
    # takes the NEAREST evidence, which is what makes it an inference rather than a
    # vote over the whole component.
    adj = collections.defaultdict(set)
    with io.open(FAMILY, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            me = r["geni_id"]
            for p in (r.get("father"), r.get("mother")):
                if p:
                    adj[me].add(p)
                    adj[p].add(me)
            for k in (r.get("children") or "").replace("|", " ").split():
                adj[me].add(k)
                adj[k].add(me)
            for sp in (r.get("spouses") or "").replace("|", " ").split():
                adj[me].add(sp)
                adj[sp].add(me)

    def evidence_at(g):
        """What this one person says about culture, if anything."""
        s = scripts.get(g)
        if s:
            if KANA.search(s):
                return "ja"
            if HANGUL.search(s):
                return "ko"
        return place_culture.get(g)

    settled_by_neighbour = 0
    MAX_HOPS = 6
    for g in list(need):
        if g in culture:
            continue
        seen = {g}
        frontier = [g]
        for hop in range(1, MAX_HOPS + 1):
            nxt = []
            votes = collections.Counter()
            for x in frontier:
                for y in adj[x]:
                    if y in seen:
                        continue
                    seen.add(y)
                    nxt.append(y)
                    e = evidence_at(y)
                    if e:
                        votes[e] += 1
            if votes:
                top, n = votes.most_common(1)[0]
                if n / sum(votes.values()) >= 0.7:
                    culture[g] = top
                    why[g] = f"graph traversal, {hop} hop(s)"
                    settled_by_neighbour += 1
                break
            frontier = nxt
            if not frontier:
                break
    print(f"  settled by graph traversal: {settled_by_neighbour:,}")
    print(f"  culture settled for {len(culture):,} of {len(need):,}")

    # ---- the reading table, out of Wikidata's own name items ----------------
    qids = []
    with io.open(QIDS, encoding="utf-8", newline="") as fh:
        rd = csv.reader(fh, delimiter="\t")
        next(rd, None)
        for row in rd:
            if row:
                qids.append(row[0])
    print(f"\nname items to read: {len(qids):,}")
    # **The table is built from the labels, not from P31.** A first version required the
    # item to carry a name-kind P31 and got 494 Chinese characters, 6 Korean and *zero*
    # Japanese -- the P31 vocabulary for name items is not consistent enough to filter on,
    # and filtering on it threw away most of the readings that are actually present.
    #
    # What is consistent is the label set: an item whose `zh` label is a single Han
    # character and whose `en` label is a Latin word is a published romanisation of that
    # character. The culture comes from WHICH language label carries the Han form and
    # whether a hangul or kana label sits beside it, which is the item's own statement
    # about itself rather than an inference from a property.
    table = {"zh": {}, "ja": {}, "ko": {}}
    seen_items = 0
    with wikistore.StoreReader(STORE, INDEX) as rd:
        for i in range(0, len(qids), 5000):
            for q, e in rd.entities(qids[i:i + 5000]).items():
                L = {k: v["value"] for k, v in (e.get("labels") or {}).items()}
                en = L.get("en") or L.get("mul")
                if not en or not LATIN_NAME.match(en):
                    continue
                seen_items += 1
                zh = L.get("zh") or L.get("zh-hant") or L.get("zh-hans")
                ja = L.get("ja")
                ko = L.get("ko")
                # Korean: a hangul label beside a Han one means the Han is hanja and the
                # Latin is its Korean reading.
                if ko and HANGUL.search(ko):
                    for han in (ja, zh):
                        if han and HAN.fullmatch(han):
                            table["ko"].setdefault(han, en)
                            break
                # Japanese: a kana label beside a Han one, same logic.
                if ja and KANA.search(ja):
                    for han in (L.get("ja_kanji"), zh):
                        if han and HAN.fullmatch(han):
                            table["ja"].setdefault(han, en)
                            break
                elif ja and HAN.fullmatch(ja) and not zh:
                    table["ja"].setdefault(ja, en)
                if zh and HAN.fullmatch(zh):
                    table["zh"].setdefault(zh, en)
            if i and i % 200000 == 0:
                print(f"  ...{i:,} read", flush=True)
    print(f"  {seen_items:,} item(s) had a Latin en label")
    for code in table:
        print(f"  {code}: {len(table[code]):,} character(s) with a published reading")

    # ---- romanise -----------------------------------------------------------
    rows = []
    done = collections.Counter()
    for g, cjk in need.items():
        code = culture.get(g)
        if not code:
            done["culture unknown"] += 1
            continue
        chars = [c for c in cjk if HAN.match(c)]
        parts = [table[code].get(c) for c in chars]
        if parts and all(parts):
            rows.append((g, cjk, code, " ".join(parts), why.get(g, "")))
            done[f"{code} romanised"] += 1
        else:
            done[f"{code} incomplete"] += 1
    print()
    for k, v in done.most_common():
        print(f"  {k:24} {v:,}")

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["geni_id", "cjk", "culture", "romanised", "culture_evidence"])
        for row in rows[:limit] if limit else rows:
            w.writerow(row)

    zh = sum(1 for r in rows if r[2] == "zh")
    ko = sum(1 for r in rows if r[2] == "ko")
    ja = sum(1 for r in rows if r[2] == "ja")
    md = ["# Romanising the Han-only names", "",
          "Built by `scripts/build-cjk-romanisation.py`. **Nothing is transliterated** — "
          "every reading is read off a Wikidata name item that carries both the Han form "
          "and the Latin form, so it is a published reading of that character *as a name*.",
          "",
          f"- people with a CJK name and no Latin label: **{len(need):,}**",
          f"- culture settled: **{len(culture):,}**",
          f"- romanised: **{len(rows):,}** — zh **{zh:,}**, ko **{ko:,}**, ja **{ja:,}**",
          "", "## How culture was settled, in Emma's order of evidence", "",
          "| evidence | people |", "| --- | ---: |",
          f"| a listed birth or death place | {sum(1 for g in culture if why.get(g,'').startswith('place')):,} |",
          f"| export provenance | {settled_by_export:,} |",
          f"| neighbours' script | {settled_by_neighbour:,} |",
          "", "## Japanese is separated on purpose", "",
          "Emma: *\"Chinese and Korean readings are all very straightforward. Japanese "
          "readings are not straightforward.\"* She is right, and it is structural: a "
          "Chinese or Korean character has effectively one reading as a name, while a "
          "Japanese one takes different readings in different names and the item only "
          "gives the reading for *that* name. **The `ja` rows are the ones to distrust.**"]
    OUT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"\nwrote {OUT_CSV} and {OUT_MD}")
    for row in rows[:15]:
        print("   %-22s %-8s %-3s %-22s %s" % row)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
