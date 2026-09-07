"""Every (patronymic token, attesting given name) pair, with how many fathers attest it.

    python scripts/census-patronymic-sources.py

**Emma, 2026-09-07**, shown `Q141336969` and `Q141290188` carrying `P144` *based on*
`Q58785388` *Junna*: *"neither of these are based on Junna lol at least not the Junna you
linked. Not sure how you even got that one or how you're defining the patronymic sources."*
Her floor, given when asked: *"Uhh it needs to be attested lol. Really attested in our data
plus some degree of agentic inference or my manual approval."*

**How `Junna` got there.** `namemodel._skeleton` deletes every vowel, so `johan` and `junna`
both reduce to `jn` and `_same_name` calls them one name. One father in 1.45 M happens to be
recorded `Junna`, his child is a `Johansson`, and that single row became a `P144` source on a
token 4,512 people bear.

`build-patronymic-items.py` writes the *names* it accepted and not how many fathers attest
each, so nothing on disk could tell a 4,000-father source from a one-father one. This is that
number, one row per pair, per `CLAUDE.md` § *"Analyse this" means build a CSV*.

Writes `reports/patronymic-source-attestation.tsv`.
"""

import collections
import csv
import io
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "src"))

import namemodel as nm                                              # noqa: E402

LABELS = ROOT / "reports" / "derived-labels.csv"
FAMILY = ROOT / "reports" / "derived-family.csv"
OUT = ROOT / "reports" / "patronymic-source-attestation.tsv"

csv.field_size_limit(1 << 30)


def main():
    label, father = {}, {}
    with io.open(LABELS, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            label[r["geni_id"]] = r.get("label_en") or r.get("label_mul") or ""
    with io.open(FAMILY, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            f = (r.get("father") or "").strip()
            if f:
                father[r["geni_id"]] = f
    print(f"{len(label):,} labelled people, {len(father):,} with a father", file=sys.stderr)

    # The same walk `build-patronymic-items.py` makes, keeping the COUNT rather than the set,
    # and keeping one example bearer per pair so a row can be read as a person.
    sources = collections.defaultdict(collections.Counter)
    example = {}
    bearers = collections.Counter()
    for g, lab in label.items():
        dad = label.get(father.get(g, ""), "")
        if not dad:
            continue
        dad_given = dad.split()[0]
        for tok in lab.split():
            if not nm.PATRONYMIC.match(tok):
                src = nm.latin_patronymic_source(tok, dad_given)
                if src:
                    key = tok.casefold()
                    bearers[key] += 1
                    sources[key][src] += 1
                    example.setdefault((key, src), (g, lab, dad))
                continue
            if nm.patronymic_or_surname(tok, dad) != "patronymic":
                continue
            m = nm.PATRONYMIC_PARTS.match(tok)
            if not m:
                continue
            stem = m.group(1).casefold().rstrip("s")
            key = tok.casefold()
            bearers[key] += 1
            for w in dad.split():
                if nm.PATRONYMIC.match(w):
                    continue
                if nm._same_name(stem, w.casefold().rstrip("s")):
                    sources[key][w] += 1
                    example.setdefault((key, w), (g, lab, dad))
                    break

    rows = []
    for tok in sorted(sources):
        total = sum(sources[tok].values())
        for src, n in sorted(sources[tok].items(), key=lambda kv: (-kv[1], kv[0])):
            g, lab, dad = example.get((tok, src), ("", "", ""))
            rows.append({
                "token": tok,
                "source": src,
                "fathers": n,
                "share": "%.6f" % (n / total),
                "attested_total": total,
                "bearers": bearers[tok],
                "example_geni_id": g,
                "example_person": lab,
                "example_father": dad,
            })

    with io.open(OUT, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, delimiter="\t", fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {OUT.relative_to(ROOT)}: {len(rows):,} pairs over {len(sources):,} tokens")

    # The distribution, which is the thing to read: how many pairs each floor would drop.
    for floor in (1, 2, 3, 5, 10):
        kept = sum(1 for r in rows if int(r["fathers"]) >= floor)
        print(f"  fathers >= {floor:>2}: {kept:,} pairs kept, {len(rows)-kept:,} dropped")
    for floor in (0.01, 0.02, 0.05, 0.10):
        kept = sum(1 for r in rows if float(r["share"]) >= floor)
        print(f"  share  >= {floor:.0%}: {kept:,} pairs kept, {len(rows)-kept:,} dropped")


if __name__ == "__main__":
    main()
