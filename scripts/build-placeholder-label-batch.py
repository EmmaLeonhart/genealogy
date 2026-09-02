"""Labels for every placeholder-named person, as JSON edit objects.

Queue items 7 and 8, which are one job: the `mul` label is the normalisation and
the per-language label is the generated relationship. Both were settled by Emma
on 2026-08-15 after she read the preview, so this generates rather than asks.

**`mul` — the normalisation.** Every placeholder given-name form collapses to
`NN`, or `NN <surname>` where a real surname exists. A surname that is *itself*
placeholder vocabulary — `NN ???`, `NN N.N.`, `NN Unknown` — collapses to bare
`NN`; her call, 351 people.

**`en` — the relationship label.** Precedence parent, spouse, child, giving
`daughter of Olof Larsson`, `wife of Rostaing Arbald`. Her rulings, both applied:

* **Everyone with a placeholder given name gets one**, including the 3,934 who
  already carry a surname, and including the 331 whose surname also appears
  inside the generated label. Shown the rows, she chose to generate: the label
  still carries a given name the `mul` label does not.
* **A redacted or placeholder relative is skipped** and the precedence falls
  through to the next one, trying every spouse and child. This is why no label
  reads *"husband of `<private>` Gaya Pereira"* — there were 2,730 of those.

**The surname is kept, and the reason is the measurement.** A relative has a real
name for 69% of bare-`NN` people but only 36% of `NN <surname>` ones. Emma read
that correctly where I had it backwards: *"the surname ones being badly connected
is kind of evidence in favour of the fact that we need to keep the surname."* For
that population the relationship label usually cannot be built at all, so the
surname is the only informative thing they have.

**No `ja` or `zh` is emitted here and that is queue item 9, not an oversight.**
Emma requires English, Japanese, Chinese and `mul` on everything. `en` comes free
because the relative's own label is English; `ja` and `zh` have to be
*constructed*, since Japanese is not in Wikidata's top 18 languages by coverage
and cannot be copied from a relative. Every edit records which languages it is
missing so item 9 can find them.

**Unknown sex takes the neutral form** — `child of`, `spouse of`. No gender is
inferred to make a label read better.

Writes `reports/wikidata-placeholder-labels.json`.

    py scripts/build-placeholder-label-batch.py
"""

from __future__ import annotations

import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PREVIEW = REPO / "reports" / "relationship-label-preview.csv"
PAIRS = REPO / "reports" / "geni-wikidata-pairs.csv"
OUT = REPO / "reports" / "wikidata-placeholder-labels.json"

csv.field_size_limit(10 ** 7)

#: Emma, 2026-08-15: English, Japanese and Chinese on everything, plus `mul`.
REQUIRED = ("en", "ja", "zh")



#: **The relationship word in Japanese and Chinese**, built the native way rather than by
#: borrowing English grammar. `CLAUDE.md` § *The NN/Private label algorithm* gives the shape:
#:
#:     ja   アルネ・オーラウス・フョルトフト・ガルボルグの息子
#:     zh   阿尔内·奥劳斯·夫约托夫特·加尔博格之子
#:
#: There is no `の`-for-`of` borrowing here beyond what Japanese itself uses: `<name>の息子` IS
#: the Japanese construction, and `<name>之子` the Chinese one.
#: **Every relation the preview can generate, not just the nine it started with.**
#: `build-relationship-label-preview.py` has emitted grandparent, grandchild, sibling, nibling
#: and pibling labels for a long time and this table covered none of them, so those people got an
#: `en` label and no CJK at all -- the pattern `CLAUDE.md` keeps recording, where two halves of
#: one job drift apart because nothing forces them to agree.
#:
#: The in-law pair is new on 2026-09-01, her ruling. It is the largest single population:
#: **8,129 people whose only named relative is a spouse's father**, because their own spouse is
#: unnamed too.
CJK_RELATION = {
    "son": ("の息子", "之子", "의 아들"),
    "daughter": ("の娘", "之女", "의 딸"),
    "child": ("の子", "之子", "의 자녀"),
    "father": ("の父", "之父", "의 아버지"),
    "mother": ("の母", "之母", "의 어머니"),
    "parent": ("の親", "之親", "의 부모"),
    "husband": ("の夫", "之夫", "의 남편"),
    "wife": ("の妻", "之妻", "의 아내"),
    "spouse": ("の配偶者", "之配偶", "의 배우자"),
    "grandson": ("の孫", "之孫", "의 손자"),
    "granddaughter": ("の孫娘", "之孫女", "의 손녀"),
    "grandchild": ("の孫", "之孫", "의 손주"),
    "grandfather": ("の祖父", "之祖父", "의 할아버지"),
    "grandmother": ("の祖母", "之祖母", "의 할머니"),
    "grandparent": ("の祖父母", "之祖父母", "의 조부모"),
    "brother": ("の兄弟", "之兄弟", "의 형제"),
    "sister": ("の姉妹", "之姐妹", "의 자매"),
    "sibling": ("の兄弟姉妹", "之同胞", "의 형제자매"),
    "nephew": ("の甥", "之侄", "의 조카"),
    "niece": ("の姪", "之侄女", "의 조카딸"),
    "nephew or niece": ("の甥姪", "之侄", "의 조카"),
    # **Side-dependent: the Korean comes from `KO_BY_SIDE`, not from here.** Emma, 2026-09-01:
    # *"you realize we can do logic for the NN stuff right? It's easy lol."* A nibling is reached
    # through a NAMED sibling who is that nibling's father or mother, so paternal against maternal
    # is which list the candidate came out of rather than an inference. 삼촌/외삼촌, 고모/이모.
    "uncle": ("の叔父", "之叔父", None),
    "aunt": ("の叔母", "之姑母", None),
    "uncle or aunt": ("の叔父叔母", "之叔伯", None),
    "son-in-law": ("の婿", "之婿", "의 사위"),
    "daughter-in-law": ("の嫁", "之媳", "의 며느리"),
    "child-in-law": ("の子の配偶者", "之子媳", "의 자녀의 배우자"),
    # **These stay unrendered and the reason is different from uncle/aunt.** Korean in-law sibling
    # terms split by the speaker's sex AND relative age -- 처남 against 매형, 시숙 against 시동생 --
    # and age is not what the side logic gives us. 482 people; they keep `ja` and `zh`.
    "brother-in-law": ("の義兄弟", "之姐夫", None),
    "sister-in-law": ("の義姉妹", "之嫂", None),
    "brother-in-law or sister-in-law": ("の義兄弟姉妹", "之姻親", None),
}

#: **Built from the table rather than typed beside it.** The two were separate literals and the
#: regex listed nine relations while the preview emitted seventeen; deriving it means a relation
#: added above cannot be missing here. Longest first, so `son-in-law` is not eaten by `son`.
RELATION_RE = re.compile(
    r"^(" + "|".join(re.escape(k) for k in
                     sorted(CJK_RELATION, key=len, reverse=True)) + r") of (.+)$", re.I)


#: The Korean the side decides. `nibling` means the unnamed person IS the uncle or aunt of the
#: named one, so the term describes them from the nephew's side of the family.
KO_BY_INLAW = {
    # Korean names a sibling-in-law by both sexes and, in three of the four cases, by whether the
    # linking sibling is senior. The speaker is the NAMED relative -- the label reads
    # `<relative>의 <term>` -- and the seniority compared is that relative against their sibling,
    # who is the unnamed person's spouse. `build-relationship-label-preview._inlaw_key` derives it.
    "F-F": "의 올케",              # her brother's wife; no date needed, and 112 of the 121
    "F-M-older": "의 형수",        # his older brother's wife
    "F-M-younger": "의 제수",      # his younger brother's wife
    "M-F-older": "의 형부",        # her older sister's husband
    "M-F-younger": "의 제부",      # her younger sister's husband
    "M-M-older": "의 매형",        # his older sister's husband
    "M-M-younger": "의 매제",      # his younger sister's husband
}

KO_BY_SIDE = {
    ("uncle", "paternal"): "의 삼촌",
    ("uncle", "maternal"): "의 외삼촌",
    ("aunt", "paternal"): "의 고모",
    ("aunt", "maternal"): "의 이모",
}


def cjk_labels(en_label, table, side="", inlaw=""):
    """`(ja, zh)` for a generated `X of Y` label, or `(None, None)`.

    **This was deferred, and the reason it was deferred is now gone.** `CLAUDE.md` records that
    `ja`/`zh` were excluded *"only because the relative's name is usually not transliterated --
    where it is, as in the Garborg family, they are emitted."* The token funnel wired into
    `build-daily-batch.py` on 2026-08-31 fills the table on every run, so the relative's name is
    transliterable far more often than it was.

    **Partial is still worse than absent.** If any token of the relative's name is unknown, both
    labels are withheld -- half a name in katakana and half in Latin is not a Japanese label. The
    middle-initial exception in `labels.transliterate_token` is the only one and it applies here
    through the same table.
    """
    m = RELATION_RE.match((en_label or "").strip())
    if not m:
        return None, None, None
    kind = m.group(1).lower()
    words = CJK_RELATION.get(kind)
    if not words:
        return None, None, None
    ko_word = words[2] or KO_BY_INLAW.get(inlaw) or KO_BY_SIDE.get((kind, side))
    ja_parts, zh_parts, ko_parts = [], [], []
    for token in m.group(2).split():
        trio = table.get(token)
        if not trio or not trio[0] or not trio[1]:
            return None, None, None
        ja_parts.append(trio[0])
        zh_parts.append(trio[1])
        ko_parts.append(trio[2] if len(trio) > 2 else "")
    ja = "・".join(ja_parts) + words[0]
    zh = "·".join(zh_parts) + words[1]
    # **Korean needs the relative's name in Hangul and a relation word that does not assert a
    # side.** Either missing means no `ko` rather than a half-Hangul label -- *partial is worse
    # than absent*, which is why `ja`/`zh` are gated on every token too.
    ko = (" ".join(ko_parts) + ko_word) if (ko_word and all(ko_parts)) else None
    return ja, zh, ko


def main() -> int:
    if not PREVIEW.exists():
        print(f"no {PREVIEW}; run scripts/build-relationship-label-preview.py first",
              file=sys.stderr)
        return 1

    translit = {}
    tpath = REPO / "reports" / "garborg-name-transliterations.tsv"
    if tpath.exists():
        with tpath.open(encoding="utf-8", newline="") as fh:
            for t in csv.DictReader(fh, delimiter="	"):
                translit[t["token"]] = (t["ja"], t["zh"], t.get("ko", ""))
    print(f"{len(translit):,} tokens in the transliteration table")

    rows = list(csv.DictReader(PREVIEW.open(encoding="utf-8", newline="")))
    print(f"{len(rows):,} people carry a placeholder given name")

    edits, counts = [], Counter()
    for r in rows:
        gid = r["geni_id"]
        labels = {"mul": r["mul_label"]}
        if r.get("generated_en"):
            labels["en"] = r["generated_en"]
            ja, zh, ko = cjk_labels(r["generated_en"], translit,
                                    (r.get("relation_side") or ""),
                                    (r.get("inlaw_key") or ""))
            if ja:
                labels["ja"], labels["zh"] = ja, zh
                counts["ja and zh built from the relative's name"] += 1
            if ko:
                labels["ko"] = ko
                counts["ko built from the relative's name"] += 1
        missing = [l for l in REQUIRED if l not in labels]
        counts["with an en label" if "en" in labels else "mul only"] += 1
        counts[r["population"]] += 1
        edits.append({
            "id": f"placeholder_label:{gid}",
            "type": "set_labels",
            "source": "geni placeholder normalisation",
            # No QID: these people are overwhelmingly not on Wikidata yet, so the
            # labels attach to whatever creates them. An edit runner resolves it
            # by Geni ID, the same key everything else in this repo joins on.
            "subject": {"qid": None, "geni_id": gid},
            "requires": [],
            "labels": labels,
            "missing_languages": missing,
            "relation_used": r.get("relation_used") or None,
            "via_geni_id": r.get("via_geni_id") or None,
            "skipped_a_relative": r.get("skipped_a_relative") or None,
        })

    OUT.write_text(json.dumps(edits, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {OUT} ({len(edits):,} set_labels edits)\n")
    for k, v in counts.most_common():
        print(f"  {v:>7,}  {k}")
    print(f"\n  {sum(1 for e in edits if 'ja' in e['missing_languages']):>7,}  "
          "still need a ja label - queue item 9")
    print(f"  {sum(1 for e in edits if 'zh' in e['missing_languages']):>7,}  "
          "still need a zh label - queue item 9")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
