"""Size the Sinosphere label-override item from the pipeline's own copy of the live labels. No network.

The first version read every creation live from the API; on 2026-10-06 this machine's IP was rate-limited
(HTTP 429 on every call, shared with the other sessions), so it reads `reports/garborg-live-labels.tsv`
(live labels of our items, refreshed every pipeline run) instead, joined to the Geni record through
`garborg-qids.tsv`/`p2600-all.tsv`, `reports/derived-labels.csv` (CJK names) and `reports/derived-places.csv`.

A person counts as Sinosphere when any of: Han in their `mul`/`en` label; a `ja` label in Han with no kana;
the Geni CJK name in Han; a birth or death place in Japan, China, Korea or Taiwan; the particle `no` in the
Geni name. `created_range` marks items numbered from Q141223000 on, the range of the account's creations
(2026-08-30 on). Writes `reports/sinosphere-label-overrides-size-2026-10-06.csv` and prints the counts.
"""
import collections, csv, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LANGS = ["mul", "en", "ja", "zh", "ko", "fr", "es", "ru"]
HAN = re.compile("[㐀-䶿一-鿿豈-﫿]")
KANA = re.compile("[぀-ヿ]")
EAST_ASIA = re.compile(r"\b(Japan|China|Korea|Taiwan|Manchuria|Ryukyu)\b|日本|中国|中國|朝鮮|韓国|韓國|대한민국|台湾|臺灣")
csv.field_size_limit(1 << 30)


def main():
    labels = collections.defaultdict(dict)
    with open(ROOT / "reports/garborg-live-labels.tsv", encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            if r["lang"] in LANGS:
                labels[r["qid"]][r["lang"]] = r["label"]
    # `garborg-qids.tsv` (our items, kept current by the pipeline) first; the roster `p2600-all.tsv` was last
    # committed 2026-09-30 and misses everything created since (the Aido family among them).
    geni_of = collections.defaultdict(list)
    for r in csv.DictReader(open(ROOT / "reports/garborg-qids.tsv", encoding="utf-8"), delimiter="\t"):
        if r["qid"] in labels and r["geni_id"] not in geni_of[r["qid"]]:
            geni_of[r["qid"]].append(r["geni_id"])
    with open(ROOT / "out/wikidata/p2600-all.tsv", encoding="utf-8") as f:
        for line in f:
            q, _, g = line.rstrip("\n").partition("\t")
            if q in labels and g not in geni_of[q]:
                geni_of[q].append(g)
    wanted = {g for gs in geni_of.values() for g in gs}
    places, geni = {}, {}
    for r in csv.DictReader(open(ROOT / "reports/derived-places.csv", encoding="utf-8")):
        if r["geni_id"] in wanted:
            places[r["geni_id"]] = (r["birth_place"] + " / " + r["death_place"]).strip(" /")
    for r in csv.DictReader(open(ROOT / "reports/derived-labels.csv", encoding="utf-8")):
        if r["geni_id"] in wanted:
            geni[r["geni_id"]] = (r["label_mul"], r["cjk_names"])
    rows = []
    for q, lab in labels.items():
        gids = geni_of.get(q, [])
        gmul, gcjk = next((geni[g] for g in gids if g in geni), ("", ""))
        place = next((places[g] for g in gids if places.get(g)), "")
        why = []
        if any(HAN.search(lab.get(l, "")) for l in ("mul", "en")): why.append("han-mul/en")
        ja = lab.get("ja", "")
        if HAN.search(ja) and not KANA.search(ja): why.append("han-ja")
        if HAN.search(gcjk): why.append("geni-cjk")
        if EAST_ASIA.search(place): why.append("place")
        if "no" in gmul.split(): why.append("particle-no")
        if not why:
            continue
        # The shape of the problem: Latin `mul` and a katakana `ja` means the CJK labels are a reading of a
        # romanisation (the Aido shape); Han `mul` means the kanji universe.
        mul = lab.get("mul", "")
        shape = ("han" if HAN.search(mul) else
                 "latin+kana-ja" if KANA.search(ja) else
                 "latin+han-ja" if HAN.search(ja) else "latin, no ja")
        rows.append({"qid": q, "created_range": "yes" if int(q[1:]) >= 141223000 else "no",
                     "shape": shape, "why": "+".join(why), "geni_id": ";".join(gids), "geni_name": gmul,
                     "geni_cjk": gcjk, "place": place, **{l: lab.get(l, "") for l in LANGS}})
    rows.sort(key=lambda r: int(r["qid"][1:]))
    out = ROOT / "reports/sinosphere-label-overrides-size-2026-10-06.csv"
    with open(out, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)
    print(len(labels), "items in garborg-live-labels.tsv;", len(rows), "Sinosphere ->", out.name)
    print(collections.Counter((r["created_range"], r["shape"]) for r in rows).most_common())
    print(collections.Counter(r["why"] for r in rows).most_common(12))
    for l in LANGS:
        print(l, sum(1 for r in rows if r[l]), "have it")


if __name__ == "__main__":
    main()
