"""Resolve a competing given-name item PER BEARER, using the person's sex.

    python scripts/resolve-names-by-sex.py

**Emma's ruling, on `Maria`:** *"everything appears to be diacritics or stuff that's not actually
it… there's a male and a female Maria"*, and *"That is settled by the person's sex."* So a token
carried by two items is not an ambiguity to resolve once for the string — it resolves differently
for each person who bears it.

**Two shapes, and the second is new.** `reports/name-ambiguity-buckets.tsv` separates them:

  * **sex split** — *male given name* against *female given name*. The original 95.
  * **generic vs sexed** — a bare `given name` against a sexed one, or two differently-sexed ones:
    `Abba` is *male* against *unisex*, `Salmon` is *given name* against *male given name*. This is
    the 33 that `reports/name-ambiguity-causes.md` left inside its *"231 · other. Mixed."* bucket,
    which was neither 231 nor mixed.

Extending her rule to the second shape is a decision taken rather than asked, per `CLAUDE.md`
§ *Working the queue: GUESS. Do not ask*: **take the sexed item matching the bearer's recorded
sex; where the bearer has no sex, take the generic item if one exists and resolve nothing
otherwise.** A generic `given name` item is never wrong for a person whose sex we do not know,
which is exactly why it is the fallback and not a guess.

**`reports/name-resolved-by-sex.csv` had no generator.** It carried 13,503 rows and nothing in the
repo could re-derive them — the § *LEGACY CODE IS DELETED* problem in its other form, a data file
whose provenance is gone. This is that generator.

**Bearers come from the NAME FIELDS, never the rendered label.** `namemodel.classify_fields` is
the authority on what is a given name, so a token that is really a patronymic or a nickname for
some person does not make them a bearer.
"""

import collections
import csv
import io
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from namemodel import classify_fields  # noqa: E402

BUCKETS = ROOT / "reports" / "name-ambiguity-buckets.tsv"
NAMES = ROOT / "reports" / "display-names.csv"
FACTS = ROOT / "reports" / "derived-facts.csv"
OUT = ROOT / "reports" / "name-resolved-by-sex.csv"

csv.field_size_limit(1 << 30)

#: The buckets whose competing items differ only in who may carry the name.
WANTED_BUCKETS = {"sex split", "other"}


def sex_class(description):
    """`M`, `F`, `U` (unisex) or `G` (generic) from an item's English description."""
    d = (description or "").lower()
    if not d.endswith("given name"):
        return None
    if "female" in d or "feminine" in d:
        return "F"
    if "male" in d or "masculine" in d:   # after female: "female" contains "male"
        return "M"
    if "unisex" in d:
        return "U"
    if d == "given name":
        return "G"
    return None


def candidates():
    """`{token: {class: qid}}` for every string this rule can settle."""
    out = {}
    with io.open(BUCKETS, encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            if row["bucket"] not in WANTED_BUCKETS or row["kind"] != "given":
                continue
            qids = [q.strip() for q in row["qids"].split("|") if q.strip()]
            descs = [d.strip() for d in row["descriptions"].split("|")]
            if len(qids) != len(descs):
                continue
            by_class = {}
            for qid, desc in zip(qids, descs):
                cls = sex_class(desc)
                if cls and cls not in by_class:
                    by_class[cls] = qid
            # Only useful if the classes actually differ; two items of the same class
            # are a duplicate, not something a bearer's sex can separate.
            if len(by_class) > 1:
                out[row["name"]] = by_class
    return out


def resolve(by_class, sex):
    """The item for a bearer of this token, and why."""
    if sex == "M" and "M" in by_class:
        return by_class["M"], "resolved by sex"
    if sex == "F" and "F" in by_class:
        return by_class["F"], "resolved by sex"
    # A unisex item fits a known sex only when no sexed item of that sex exists.
    if sex in ("M", "F") and "U" in by_class:
        return by_class["U"], "resolved by sex (unisex; no item for that sex)"
    if "G" in by_class:
        return by_class["G"], "no recorded sex; generic given-name item"
    if "U" in by_class:
        return by_class["U"], "no recorded sex; unisex item"
    return "", "unresolved: bearer has no recorded sex"


def main():
    wanted = candidates()
    if not wanted:
        sys.exit("no resolvable tokens -- has name-ambiguity-buckets.tsv been built?")

    # **This EXTENDS the file; it does not rebuild it.** The 95 tokens already in
    # `name-resolved-by-sex.csv` were resolved by an earlier analysis whose script is gone, and
    # they come from a different population -- every still-ambiguous string, not just the ones
    # this bucketing can settle. Regenerating from scratch replaced 13,503 rows with 801, a 94%
    # loss dressed up as a rebuild. Existing rows are kept verbatim and only genuinely new
    # tokens are added, which is what the queue item asked for: *extend*.
    existing_rows, existing_tokens = [], set()
    if OUT.exists():
        with io.open(OUT, encoding="utf-8", newline="") as fh:
            for row in csv.reader(fh):
                if row and row[0] != "geni_id":
                    existing_rows.append(row)
                    existing_tokens.add(row[1])
    wanted = {t: v for t, v in wanted.items() if t not in existing_tokens}
    sys.stderr.write(
        f"{len(existing_rows)} existing rows over {len(existing_tokens)} tokens kept; "
        f"{len(wanted)} new tokens to add\n")
    if not wanted:
        print("nothing new to add")
        return
    lowered = {t.casefold() for t in wanted}

    sex_of = {}
    with io.open(FACTS, encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            s = (row.get("sex") or "").strip().upper()
            if s in ("M", "F"):
                sex_of[row["geni_id"]] = s

    rows, seen = [], set()
    stats = collections.Counter()
    with io.open(NAMES, encoding="utf-8", newline="") as fh:
        for record in csv.DictReader(fh):
            givn = record.get("givn") or ""
            if not givn:
                continue
            # Cheap prefilter: only parse a record that could possibly bear one of them.
            if not any(t in lowered for t in re.split(r"\s+", givn.casefold()) if t):
                continue
            geni_id = record["geni_id"]
            for token, usage, _ordinal in classify_fields(
                    givn=givn, surn=record.get("surn", ""),
                    nick=record.get("nick", ""), marnm=record.get("marnm", "")):
                if usage != "given" or token not in wanted:
                    continue
                key = (geni_id, token)
                if key in seen:
                    continue
                seen.add(key)
                sex = sex_of.get(geni_id, "")
                qid, verdict = resolve(wanted[token], sex)
                stats[verdict] += 1
                rows.append([geni_id, token, sex, qid, verdict])

    added = len(rows)
    rows = existing_rows + rows
    rows.sort(key=lambda r: (r[1], r[0]))
    with io.open(OUT, "w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["geni_id", "token", "sex", "qid", "verdict"])
        writer.writerows(rows)

    print(f"wrote {OUT}")
    print(f"  {added} new bearer-token pairs over {len(wanted)} tokens")
    print(f"  {len(rows)} rows in total")
    for verdict, count in stats.most_common():
        print(f"  {count:6d}  {verdict}")


if __name__ == "__main__":
    main()
