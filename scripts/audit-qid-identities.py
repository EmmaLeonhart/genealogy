"""Do the About Me QID links name the right person?

    python scripts/audit-qid-identities.py

**Emma, 2026-08-24:** *"do an audit of the qid identities"* — after one entry turned out
to name the wrong person.

`reports/geni-qid-links.tsv` maps Geni profiles to a QID taken from the Wikidata link she
wrote into each profile's About Me. It is the join the whole programme rests on, and it is
hand-entered, so an entry can be wrong. The known case: `6000000227334350078` *Naokiyo
Hiraoka* carries a link to `Q135579476` *Senge no Naokatsu* — **his son**. The father's
page holds the son's QID.

Two checks, both offline:

* **Shared QID.** Where several Geni profiles carry the same QID, are they one person or
  relatives? Relatives are the dangerous case, because the join silently attributes one
  person's facts to another. The tree is asked for the relationship rather than guessed at.
* **Label mismatch.** Where a profile's name and the item's label share no token at all,
  flag it. This is deliberately crude — a *report* for a human, never an automated
  rejection — because transliteration and regnal numbers make Geni and Wikidata names
  differ constantly and legitimately.

**Nothing is rewritten.** These are Emma's own About Me entries; which of two links is
wrong is hers to say. `CLAUDE.md`: the purpose is to add, and her scratchpad data is not
ours to edit.

Writes `reports/qid-identity-audit.tsv`.
"""
from __future__ import annotations

import collections
import csv
import json
import re
import sys
import unicodedata
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
csv.field_size_limit(1 << 30)

ROOT = Path(__file__).resolve().parent.parent


def fold(text):
    """Lowercase, strip accents and punctuation, drop regnal digits."""
    text = unicodedata.normalize("NFKD", text or "")
    text = "".join(c for c in text if not unicodedata.combining(c))
    return re.sub(r"[^a-z　-鿿 ]+", " ", text.lower())


def tokens(text):
    return {t for t in fold(text).split() if len(t) > 2}


def main():
    links = []
    with open(ROOT / "reports" / "geni-qid-links.tsv", encoding="utf-8") as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) >= 2 and parts[0].isdigit():
                links.append((parts[0], parts[1], parts[2] if len(parts) > 2 else ""))
    print(f"{len(links)} About Me QID links")

    items = {}
    for name in ("clan-full-items.json", "izumo-full-items.json",
                 "garborg-full-items.json", "garborg-new-items.json"):
        path = ROOT / "out" / name
        if path.exists():
            items.update(json.loads(path.read_text(encoding="utf-8")))
    print(f"{len(items)} items downloaded in full")

    geni_ids = {g for g, _q, _n in links}
    labels, family = {}, {}
    with open(ROOT / "reports" / "derived-labels.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["geni_id"] in geni_ids:
                labels[row["geni_id"]] = (row["label_en"] or row["label_mul"] or "")
    with open(ROOT / "reports" / "derived-family.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["geni_id"] in geni_ids:
                family[row["geni_id"]] = row

    by_qid = collections.defaultdict(list)
    for geni_id, qid, _name in links:
        by_qid[qid].append(geni_id)

    def relationship(a, b):
        """How `a` relates to `b` in our tree, or ''. Structural, never by name."""
        fa, fb = family.get(a, {}), family.get(b, {})
        if (fa.get("father") or "").strip() == b:
            return "b is a's father"
        if (fa.get("mother") or "").strip() == b:
            return "b is a's mother"
        if (fb.get("father") or "").strip() == a:
            return "a is b's father"
        if (fb.get("mother") or "").strip() == a:
            return "a is b's mother"
        if b in (fa.get("spouses") or "").split():
            return "spouses"
        pa = {(fa.get("father") or "").strip(), (fa.get("mother") or "").strip()} - {""}
        pb = {(fb.get("father") or "").strip(), (fb.get("mother") or "").strip()} - {""}
        if pa & pb:
            return "siblings"
        return ""

    rows = []
    for qid, ids in sorted(by_qid.items()):
        if len(ids) < 2:
            continue
        for i, a in enumerate(sorted(ids)):
            for b in sorted(ids)[i + 1:]:
                rel = relationship(a, b)
                rows.append({
                    "issue": "relatives share a QID" if rel else "several profiles share a QID",
                    "qid": qid,
                    "item_label": (items.get(qid, {}).get("labels", {})
                                   .get("en", {}).get("value", "")),
                    "geni_a": a, "name_a": labels.get(a, ""),
                    "geni_b": b, "name_b": labels.get(b, ""),
                    "relationship": rel or "none recorded in the tree",
                })

    shared = len(rows)
    for geni_id, qid, _n in links:
        item = items.get(qid)
        if not item:
            continue
        label = item.get("labels", {}).get("en", {}).get("value", "")
        name = labels.get(geni_id, "")
        if not label or not name:
            continue
        if tokens(label) and tokens(name) and not (tokens(label) & tokens(name)):
            rows.append({
                "issue": "name and item label share no token",
                "qid": qid, "item_label": label,
                "geni_a": geni_id, "name_a": name,
                "geni_b": "", "name_b": "", "relationship": "",
            })

    dest = ROOT / "reports" / "qid-identity-audit.tsv"
    with open(dest, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter="\t")
        w.writeheader()
        w.writerows(rows)

    print(f"\nwrote {dest.relative_to(ROOT)}: {len(rows)} findings")
    print(f"  {shared} from shared QIDs, {len(rows) - shared} from label mismatch\n")
    for row in rows[:12]:
        if row["geni_b"]:
            print(f"  [{row['issue']}] {row['qid']} {row['item_label'][:24]}")
            print(f"       {row['name_a'][:28]:<28} {row['geni_a']}")
            print(f"       {row['name_b'][:28]:<28} {row['geni_b']}   -> {row['relationship']}")
        else:
            print(f"  [label] {row['qid']} item={row['item_label'][:26]!r} "
                  f"geni={row['name_a'][:26]!r}")


if __name__ == "__main__":
    main()
