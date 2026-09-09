"""Every (patronymic token, attesting given name) pair, with how many fathers attest it.

    python scripts/census-patronymic-sources.py

**`Q141336969` and `Q141290188` carried `P144` *based on* `Q58785388` *Junna*, and neither is
based on that name.** That raised the question of how a patronymic source is being defined at
all. The floor: it has to be genuinely attested in our own data, plus some degree of agentic
inference or hand approval.

**How `Junna` got there.** `namemodel._skeleton` deletes every vowel, so `johan` and `junna`
both reduce to `jn` and `_same_name` calls them one name. One father in 1.45 M happens to be
recorded `Junna`, his child is a `Johansson`, and that single row became a `P144` source on a
token 4,512 people bear.

`build-patronymic-items.py` writes the *names* it accepted and not how many fathers attest
each, so nothing on disk could tell a 4,000-father source from a one-father one. This is that
number, one row per pair, per `CLAUDE.md` § *"Analyse this" means build a CSV*.

## The MOTHER is walked too, and that is where the matronymics actually are

The second ruling the same day was **reclassify as matronymic**, put over the 53
`P144` values whose given-name item is `Q11879590` *female given name*. **Those are the wrong
population and reading them says so**: `adriansdatter ← Adrian`, `jonesdatter ← Jone`,
`brynildsen ← Brynild`, `herlaugson ← Herlaug` — Norwegian and Old Norse **male** names carrying
a wrong or unisex `P31` on Wikidata. A source in the father walk *is* the father's name, so it
cannot make a matronymic however it is classed.

**A matronymic derives from the MOTHER, and nothing had walked the mothers.** Measured here:
**476 tokens
are attested by a mother and 110 by a mother ALONE**, over 214 people — `Mariasson`,
`Mariasdotter`, `Annasson`, `Evasdotter`, `Britasson`, `Bodilsen`, `Ulrikasdotter`,
`Johannasdotter`. Those are unambiguous, and they answer the question in
`build-garborg-name-items`'s own comment, that matronymic currently fires for nothing — it
fired for nothing because nobody had looked at the mothers.

Writes `reports/patronymic-source-attestation.tsv`, one row per (token, parent role, source).
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
    label, father, mother = {}, {}, {}
    with io.open(LABELS, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            label[r["geni_id"]] = r.get("label_en") or r.get("label_mul") or ""
    with io.open(FAMILY, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            f = (r.get("father") or "").strip()
            if f:
                father[r["geni_id"]] = f
            m = (r.get("mother") or "").strip()
            if m:
                mother[r["geni_id"]] = m
    print(f"{len(label):,} labelled people, {len(father):,} with a father, "
          f"{len(mother):,} with a mother", file=sys.stderr)

    # The same walk `build-patronymic-items.py` makes, keeping the COUNT rather than the set,
    # and keeping one example bearer per pair so a row can be read as a person. Run twice: once
    # against the father, which is what the plan uses, and once against the mother, which
    # nothing had ever walked and which is where the matronymics are.
    sources = {"father": collections.defaultdict(collections.Counter),
               "mother": collections.defaultdict(collections.Counter)}
    example = {}
    bearers = collections.Counter()
    for role, parent_of in (("father", father), ("mother", mother)):
        sink = sources[role]
        for g, lab in label.items():
            par = label.get(parent_of.get(g, ""), "")
            if not par:
                continue
            par_given = par.split()[0]
            for tok in lab.split():
                if not nm.PATRONYMIC.match(tok):
                    # The Latin genitive confirms against the parent's own given name; see
                    # `namemodel.latin_patronymic`. Only the father branch feeds the plan.
                    if role != "father":
                        continue
                    src = nm.latin_patronymic_source(tok, par_given)
                    if src:
                        key = tok.casefold()
                        bearers[key] += 1
                        sink[key][src] += 1
                        example.setdefault((role, key, src), (g, lab, par))
                    continue
                # `patronymic_or_surname` is the father's test by construction -- it asks
                # whether the father carries the same token -- so it is applied on the father
                # walk only. On the mother walk the token shape and the mother's given name are the
                # whole evidence, which is what makes `Mariasson` legible.
                if role == "father" and nm.patronymic_or_surname(tok, par) != "patronymic":
                    continue
                m = nm.PATRONYMIC_PARTS.match(tok)
                if not m:
                    continue
                stem = m.group(1).casefold().rstrip("s")
                key = tok.casefold()
                if role == "father":
                    bearers[key] += 1
                # The same scoping the plan builder applies, so the census measures what ships.
                for w in nm.given_name_run(par.split()):
                    if nm.PATRONYMIC.match(w):
                        continue
                    if nm._same_name(stem, w.casefold().rstrip("s")):
                        sink[key][w] += 1
                        example.setdefault((role, key, w), (g, lab, par))
                        break

    rows = []
    for role in ("father", "mother"):
        for tok in sorted(sources[role]):
            total = sum(sources[role][tok].values())
            for src, n in sorted(sources[role][tok].items(), key=lambda kv: (-kv[1], kv[0])):
                g, lab, par = example.get((role, tok, src), ("", "", ""))
                rows.append({
                    "token": tok,
                    "parent": role,
                    "source": src,
                    "parents": n,
                    "share": "%.6f" % (n / total),
                    "attested_total": total,
                    "bearers": bearers[tok],
                    "example_geni_id": g,
                    "example_person": lab,
                    "example_parent": par,
                })

    with io.open(OUT, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, delimiter="\t", fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {OUT.relative_to(ROOT)}: {len(rows):,} pairs")
    for role in ("father", "mother"):
        n = sum(1 for r in rows if r["parent"] == role)
        print(f"  {role}: {n:,} pairs over {len(sources[role]):,} tokens")

    # **The matronymics.** A token attested by a mother and by no father is a matronymic, and
    # this is the first thing in the repo that could say so.
    only = [t for t in sources["mother"] if t not in sources["father"]]
    people = sum(sum(sources["mother"][t].values()) for t in only)
    print(f"  {len(only):,} token(s) attested ONLY by a mother -- {people:,} people. "
          f"These are the matronymics.")
    for tok in sorted(only, key=lambda t: -sum(sources["mother"][t].values()))[:10]:
        c = sources["mother"][tok]
        print(f"    {tok:<22} {sum(c.values()):>4}  "
              + " ".join(f"{s}({c[s]})" for s in sorted(c, key=lambda s: -c[s])[:3]))

    # The distribution, which is what refuted both floors; see the module docstring.
    fa = [r for r in rows if r["parent"] == "father"]
    for floor in (2, 3, 5):
        kept = sum(1 for r in fa if int(r["parents"]) >= floor)
        print(f"  father pairs with >= {floor} attesting fathers: {kept:,} of {len(fa):,}")


if __name__ == "__main__":
    main()
