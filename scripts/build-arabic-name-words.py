"""
Write reports/arabic-name-words.tsv: the usual Latin spelling of each unvocalised Arabic word in the names of the given
GEDCOMs, from Wikidata's name items, for romanize_scripts.py. Arabic written without vowel marks loses its short
vowels when read letter by letter ("Mjd", "Shms", "Hnri"); a name item whose Arabic label is exactly the word carries
the spelling people use (Henry, Malik, Bakr).

Wikidata's Arabic labels on name items are noisy (ويليام is on Guillaume and on Hale, أوتو on Isak), so a candidate
counts only when its consonants are the ones the Arabic letters spell, and the English label most of the matching
items share wins; a tie, or no candidate, leaves the word to the letter-by-letter reading.
Name items are the given-name and family-name items of out/wikidata/name-items-in-store.tsv.gz.

    python scripts/build-arabic-name-words.py <gaiad.ged> [more.ged ...]
"""
import collections
import gzip
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import romanize_scripts as R

R.arab_names = lambda: {}   # the letter-by-letter reading is what each candidate is checked against, not this table

ROOT = Path(__file__).resolve().parent.parent
ITEMS = ROOT / "out" / "wikidata" / "name-items-in-store.tsv.gz"
OUT = ROOT / "reports" / "arabic-name-words.tsv"
UA = {"User-Agent": "genealogy arabic name words (emma@topazcomputing.com)"}
AR = re.compile("[؀-ۿ]")
API = "https://www.wikidata.org/w/api.php?format=json&"


def get(query):
    for attempt in range(4):
        try:
            req = urllib.request.Request(API + query, headers=UA)
            return json.load(urllib.request.urlopen(req, timeout=60))
        except OSError:
            time.sleep(5 * (attempt + 1))
    return {}


def skeleton(latin):
    """The consonants of a Latin spelling, the near ones merged: Henry and Hnri are both n r."""
    s = latin.lower()
    for a, b in (("ph", "f"), ("th", "t"), ("kh", "k"), ("sh", "s"), ("gh", "g"), ("dh", "d"), ("ch", "k"),
                 ("q", "k"), ("c", "k"), ("x", "ks"), ("v", "b"), ("p", "b"), ("j", "g"), ("z", "s")):
        s = s.replace(a, b)
    s = "".join(ch for ch in s if ch in "bdfgklmnrst")
    return re.sub(r"(.)\1+", r"\1", s)


def plain(latin):
    """Without the Arabic transcription marks (ʻAbdūn is Abdun), which the CJK label composer cannot read: the ʻayn and
    hamza signs, macrons and dots below. A European name keeps its accents (André)."""
    import unicodedata
    s = "".join(c for c in unicodedata.normalize("NFD", latin) if c not in "̣̱̄")
    return unicodedata.normalize("NFC", s).replace("ʻ", "").replace("ʾ", "").replace("ʿ", "").replace("ʼ", "")


def words_of(paths):
    out = collections.Counter()
    for p in paths:
        for line in open(p, encoding="utf-8-sig"):
            if not line.startswith(("1 NAME ", "2 TRAN ")) or R.reader_for(line[7:]) is not R._arab:
                continue
            for w in re.split(r"[\s/\-()_،]+", line[7:].strip()):
                w = w.strip("\"'.,؛")
                if w and AR.search(w) and not any(c in R.ARAB_VOW for c in w):
                    if w.startswith("ال") and len(w) > 3:
                        w = w[2:]
                    if w not in R.ARAB_WORDS:
                        out[w] += 1
    return out


def spell(words):
    """[(arabic, latin, letter reading, agreeing items, candidates)] and how many words had a name item."""
    kinds = {}
    for i, line in enumerate(gzip.open(ITEMS, "rt", encoding="utf-8")):
        if i:
            q, kind = line.split("\t")[:2]
            kinds[q] = kind
    hits = {}
    for n, w in enumerate(sorted(words)):
        s = get("action=wbsearchentities&language=ar&strictlanguage=1&type=item&limit=50&search=" + urllib.parse.quote(w))
        hits[w] = [h["id"] for h in s.get("search", []) if h["id"] in kinds
                   and h.get("match", {}).get("type") == "label" and h["match"].get("text") == w]
        time.sleep(0.1)
        if n % 200 == 0:
            print(f"  {n}/{len(words)}", flush=True)
    ids = sorted({q for qs in hits.values() for q in qs})
    en = {}
    for i in range(0, len(ids), 50):
        for q, e in get("action=wbgetentities&props=labels&languages=en|mul&ids=" + "|".join(ids[i:i + 50])).get(
                "entities", {}).items():
            lb = (e.get("labels", {}).get("en") or e.get("labels", {}).get("mul") or {}).get("value", "")
            if lb and " " not in lb and not AR.search(lb):
                en[q] = lb
    rows = []
    for w, qs in sorted(hits.items()):
        reading = R._arab(w) or ""
        votes = collections.Counter(en[q] for q in qs if q in en and skeleton(en[q]) == skeleton(reading))
        best = votes.most_common(2)
        # One consonant tells little apart (ليو is Liu on some items, Leo on others; يوهان was Yohn on its one item):
        # such a word needs two items or more, all on the one spelling (علي Ali).
        short = len(skeleton(reading)) < 2
        if short and not (len(best) == 1 and best[0][1] >= 2 and best[0][1] == sum(1 for q in qs if q in en)):
            continue
        if best and (len(best) == 1 or best[0][1] > best[1][1]):
            lb = best[0][0]
            rows.append((w, plain(lb), reading, ",".join(q for q in qs if en.get(q) == lb), sum(votes.values())))
    return rows, sum(1 for v in hits.values() if v)


def main():
    words = words_of(sys.argv[1:])
    rows, found = spell(words)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8", newline="\n") as f:
        f.write("arabic\tlatin\tletter_reading\tagreeing_items\tcandidates\n")
        for r in rows:
            f.write("\t".join(map(str, r)) + "\n")
    print(f"{len(words)} words, {found} with a name item, {len(rows)} spelled -> {OUT}")


if __name__ == "__main__":
    main()
