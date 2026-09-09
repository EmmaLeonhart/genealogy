"""Resolve a same-romanisation name collision using the bearer's own Han name.

`reports/name-ambiguity-causes.md` put 210 strings in a bucket called *different
characters, same romanisation* — `Tu` is 涂 **and** 屠, `Tachibana` is 橘 **and** 立花 — and
concluded: *"unresolvable from a Latin string — the information needed was destroyed before
the data reached us."*

**That is true of the Latin string and false of the record.** A Geni profile often carries
the Han name beside the romanised one, and `reports/derived-labels.csv` has held it in
`cjk_names` all along. Where the two competing items carry different Han forms and the
bearer's own name contains one of them, the collision is settled for that person.

**Per bearer, not per string** — which is Emma's own ruling on `Maria`, *"there's a male and
a female Maria… That is settled by the person's sex"*, applied to a different signal.
`Tachibana no Moroe` is 橘 and `Q16884158`; a Tachibana written 立花 is `Q26216117`. The
string stays ambiguous; the people do not.

WHAT IT DOES NOT DO

**It is small, and the reason is worth stating.** 254 ambiguous strings have competing items
with different Han forms, but most are not CJK collisions at all: `Landau` is 朗道 and 蘭道,
`Cohen` is 科恩, `FitzGerald` is 費茲傑羅 — **Chinese transcriptions of European names**, the
same population that makes the multi-character `zh` name items unusable elsewhere in this
repo. Their bearers are European and carry no Han name, so nothing resolves and nothing
should. What is left is the genuine CJK collisions, and there are **119** of them.

**It proposes no Wikidata edit and resolves no string.** It records, per person, which of
the competing items their own name points at.

    py scripts/build-name-resolved-by-han.py

Offline: `reports/name-ambiguity-resolved.csv`, `reports/derived-labels.csv`, the store.
Writes `reports/name-resolved-by-han.csv`.
"""

from __future__ import annotations

import csv
import io
import re
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))
from genimerge import wikistore  # noqa: E402

AMBIG = REPO / "reports" / "name-ambiguity-resolved.csv"
LABELS = REPO / "reports" / "derived-labels.csv"
STORE = REPO / "wikidata" / "items"
INDEX = REPO / "out" / "wikidata" / "store-index.sqlite3"
OUT = REPO / "reports" / "name-resolved-by-han.csv"

csv.field_size_limit(10 ** 7)
HAN_TOKEN = re.compile(r"[\u3400-\u9fff]+")


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    amb = [r for r in csv.DictReader(io.open(AMBIG, encoding="utf-8", newline=""))
           if r["verdict"] == "still ambiguous"]
    qids = sorted({q.strip() for r in amb for q in r["qid"].split("|")})
    print(f"ambiguous strings: {len(amb):,}; competing items: {len(qids):,}")

    han: dict[str, set[str]] = {}
    with wikistore.StoreReader(STORE, INDEX) as rd:
        for i in range(0, len(qids), 5000):
            for q, e in rd.entities(qids[i:i + 5000]).items():
                L = {k: v["value"] for k, v in (e.get("labels") or {}).items()}
                forms = {v for k, v in L.items()
                         if k in ("zh", "zh-hant", "zh-hans", "ja") and HAN_TOKEN.fullmatch(v)}
                if forms:
                    han[q] = forms

    # A collision is a candidate only when every competing item has a Han form and those
    # forms are distinct -- otherwise the bearer's name cannot choose between them.
    form_of: dict[str, dict[str, set[str]]] = {}
    for r in amb:
        qs = [q.strip() for q in r["qid"].split("|")]
        hs = {q: han.get(q) for q in qs}
        if all(hs.values()) and len({frozenset(v) for v in hs.values()}) == len(hs):
            form_of[r["name"]] = hs
    print(f"  strings whose competing items carry different Han forms: {len(form_of):,}")

    rows, unresolved = [], 0
    for r in csv.DictReader(io.open(LABELS, encoding="utf-8", newline="")):
        lab = (r.get("label_en") or "").strip()
        cjk = r.get("cjk_names") or ""
        if not lab or not cjk:
            continue
        for tok in lab.replace(",", " ").split():
            if tok not in form_of:
                continue
            got = [q for q, forms in form_of[tok].items() if any(f in cjk for f in forms)]
            if len(got) == 1:
                rows.append((r["geni_id"], tok, sorted(form_of[tok][got[0]])[0], got[0],
                             "resolved by the bearer's Han name"))
            else:
                unresolved += 1
            break

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["geni_id", "token", "han", "qid", "verdict"])
        w.writerows(sorted(rows))
    by = Counter(t for _, t, _, _, _ in rows)
    print(f"  bearers resolved: {len(rows):,}; bearers a Han form could not settle: {unresolved:,}")
    print("  by token: " + ", ".join(f"{k} {v}" for k, v in by.most_common(12)))
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
