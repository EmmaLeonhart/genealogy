"""Strip a marker wedged INSIDE a real name. The mechanical third of the marker work.

    py scripts/build-marker-normalisation.py

**Her instruction, in `queue.md` § LABELS, IN HER ORDER**, on the second of three marker
populations: *"A real name with a marker wedged inside it — strip the marker, keep the rest.
`Catherine unknown` → `Catherine`, `Nechama (?) Heller` → `Nechama Heller`, `Hadaburg N.N. Gräfin
im Saalgau` → `Hadaburg Gräfin im Saalgau`. Mechanical, no judgement."*

**This is the one of the three that needs no ruling from her**, which is why it goes first. The
other two do:

* a marker *leading* a real surname keeps the surname and puts the marker in `mul` —
  `unknown Bloomfield` → `mul: NN Bloomfield`;
* a *description* in the name slot gets `NN` in `mul` and the description as the local label.

Both of those decide what a person is CALLED. This one only removes a word that says the name is
unknown from a name that is otherwise present, so the result is the name that was already there.

## What it will not do

**A label that is nothing but a marker is not touched.** `position` `whole` means there is no name
underneath, and that is the other populations' business. Only `inside` and `tail` qualify, and only
when a remainder survives.

**A remainder that is no longer a name is dropped.** Stripping has to leave something with a
letter in it; `(?)` → `""` is not a normalisation, it is a deletion.

**`NOT_A_NAME` is untouched.** `CLAUDE.md`: detection and suppression are different questions.
Widening what counts as a *marker* never widens what `label_for()` empties.

Writes `reports/marker-label-normalisation.tsv` — one row per distinct label, both stores.
"""
from __future__ import annotations

import collections
import csv
import io
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
csv.field_size_limit(1 << 30)

TAB = chr(9)
CENSUS = ROOT / "reports" / "marker-labels.csv"
OUT = ROOT / "reports" / "marker-label-normalisation.tsv"

#: A remainder has to still look like a name: at least one letter in some script. A remainder of
#: punctuation or digits means the marker WAS the label, which is the `whole` population.
HAS_LETTER = re.compile(r"[^\W\d_]", re.UNICODE)


def strip_marker(label, marker):
    """Remove `marker` from `label`, dropping a whole bracketed phrase if it held the marker.

    **A dangling bracket is a broken name, and the census's own `remainder` produces them.**
    `Dr. Aaron (surname Unknown)` came back as `Dr. Aaron (surname`, `Hans Magnus (Ukendt
    tvilling)` as `Hans Magnus tvilling)`, `Banyak Ngampar [Versi 2 Unknown] Ditinggalkan` as
    `Banyak Ngampar [Versi 2 Ditinggalkan` — 41 of 1,594.

    A bracketed phrase carrying the marker is a *comment about the name being unknown*, not part
    of it, so the whole phrase goes: `Dr. Aaron`, `Hans Magnus`, `Banyak Ngampar Ditinggalkan`.
    Removing only the marker word is what left the bracket behind.
    """
    if not marker:
        return ""
    esc = re.escape(marker)
    # A bracketed phrase containing the marker, brackets and all.
    out = re.sub(r"[（(\[][^）)\]]*" + esc + r"[^）)\]]*[）)\]]", " ", label, flags=re.I)
    if out == label:
        # Not bracketed: remove the marker as a whole token.
        out = re.sub(r"(?<![^\W\d_])" + esc + r"(?![^\W\d_])", " ", label, flags=re.I)
    return out


def tidy(s):
    """Collapse the whitespace and stray brackets a removal leaves behind."""
    s = re.sub(r"\s+", " ", s or "").strip()
    # `Nechama (?) Heller` loses the marker and leaves `Nechama () Heller`.
    s = re.sub(r"[（(\[]\s*[）)\]]", " ", s)
    s = re.sub(r"\s+([,、.])", r"\1", s)
    return re.sub(r"\s+", " ", s).strip(" ,-–—")


def main() -> int:
    if not CENSUS.exists():
        print("no %s; run scripts/build-marker-label-census.py first" % CENSUS.relative_to(ROOT),
              file=sys.stderr)
        return 1
    with io.open(CENSUS, encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    print("%s census rows" % format(len(rows), ","))

    seen, out, dropped = set(), [], collections.Counter()
    for r in rows:
        if r.get("kind") != "marker" or r.get("position") not in ("inside", "tail"):
            continue
        label = (r.get("label") or "").strip()
        rest = tidy(strip_marker(label, (r.get("marker") or "").strip()))
        if not rest:
            dropped["nothing left after the strip"] += 1
            continue
        if not HAS_LETTER.search(rest):
            dropped["remainder has no letter"] += 1
            continue
        if rest == label:
            dropped["no change"] += 1
            continue
        # A name with a dangling bracket is a broken name. If the phrase-drop above did not
        # balance it, this row is not mechanical and is left for a human.
        for a, b in (("(", ")"), ("[", "]"), ("（", "）")):
            if rest.count(a) != rest.count(b):
                dropped["unbalanced brackets, refused"] += 1
                rest = ""
                break
        if not rest:
            continue
        key = (r.get("store"), r.get("geni_id") or "", r.get("qid") or "",
               r.get("language") or "", label)
        if key in seen:
            dropped["duplicate row"] += 1
            continue
        seen.add(key)
        out.append([r.get("store", ""), r.get("geni_id", ""), r.get("qid", ""),
                    r.get("language", ""), label, rest, r.get("marker", ""),
                    r.get("position", ""), r.get("vocabulary", "")])

    with io.open(OUT, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter=TAB, lineterminator="\n")
        w.writerow(["store", "geni_id", "qid", "language", "label", "normalised",
                    "marker", "position", "vocabulary"])
        w.writerows(sorted(out, key=lambda x: (x[0], x[4])))

    print("wrote %s - %s normalisations" % (OUT.relative_to(ROOT), format(len(out), ",")))
    by = collections.Counter(r[0] for r in out)
    for k, v in by.most_common():
        print("   %-10s %5d" % (k, v))
    print()
    for k, v in dropped.most_common():
        print("   skipped: %-30s %5d" % (k, v))
    print("\na sample:")
    for r in out[:12]:
        print("   %-34s -> %s" % (r[4][:34], r[5][:40]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
