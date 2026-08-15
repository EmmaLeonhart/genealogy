"""The patronymic classifier, run against Wikidata instead of the Geni corpus.

**Queue item 11. Emma, 2026-08-15:** *"Of course we also should be running this
processing on both the geni stuff and the wiki data stuff... have at the end of
the queue a thing to run this same name analysis operation on the wiki data stuff
at the end of this."*

**Same method, different fields.** `scripts/classify-patronymics.py` decides a
patronymic from the **father's given name** — never from the token's shape — and
this reuses its form tables and its father test verbatim by importing them, so the
two sides cannot drift apart. What changes is where the data comes from:

| | Geni | Wikidata |
| --- | --- | --- |
| father | `FAMC` → `HUSB` | `P22` |
| name tokens | `GIVN`, `SURN` | the **label**, tokenised |
| sex | `SEX` | `P21` |

**The label is the only name string Wikidata gives us here.** It has no
`GIVN`/`SURN` split, so the tokens are the label's words. `P735`/`P734` name
*items* rather than strings, and resolving those to strings needs the name-item
download that is still running — so this works on the label, which is present now.
That is a real limitation and is reported rather than worked around.

**A father with no label yields no verdict**, exactly as an unnamed father does on
the Geni side. Absence of evidence is not a `no`.

Writes `reports/patronymic-classification-wikidata-N.csv` (several parts, because
one file is 194 MB and GitHub's limit is 100) and `reports/patronymic-classification-wikidata.md`.

    py scripts/classify-patronymics-wikidata.py
"""

from __future__ import annotations

import csv
import glob
import gzip
import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ITEMS = REPO / "wikidata" / "items"
#: **Written in parts, because one file would be 194 MB and GitHub rejects
#: anything over 100.** Emma's rule is that every instance is a row and repo size
#: is not a constraint — *"We're not trying to make the repo small... We care
#: about actually getting results"* — so the rows are all kept and the file is
#: split rather than sampled or filtered. Each part repeats the header.
OUT_CSV_STEM = REPO / "reports" / "patronymic-classification-wikidata"
PART_LIMIT = 60 * 1024 * 1024
OUT_MD = REPO / "reports" / "patronymic-classification-wikidata.md"

FATHER, SEX, INSTANCE_OF, HUMAN = "P22", "P21", "P31", "Q5"
SEX_LETTER = {"Q6581097": "M", "Q6581072": "F"}


def _geni_classifier():
    """Import the Geni-side classifier for its form tables and father test.

    Loaded by path because the script has hyphens in its name. **Importing it
    rather than copying it is the point** — a second copy of the suffix list is a
    second thing to get wrong, and `CLAUDE.md` records what happened the last time
    one question had six answers.
    """
    spec = importlib.util.spec_from_file_location(
        "classify_patronymics", REPO / "scripts" / "classify-patronymics.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    geni = _geni_classifier()
    print("reusing the Geni-side form tables and father test", flush=True)

    def targets(entity: dict, prop: str) -> list[str]:
        out = []
        for claim in (entity.get("claims") or {}).get(prop, []):
            snak = claim.get("mainsnak") or {}
            if snak.get("snaktype") != "value":
                continue
            value = (snak.get("datavalue") or {}).get("value")
            if isinstance(value, dict) and value.get("id"):
                out.append(value["id"])
        return out

    def label_of(entity: dict) -> str:
        labels = entity.get("labels") or {}
        for lang in ("en", "mul"):
            if lang in labels:
                return (labels[lang] or {}).get("value", "") or ""
        for value in labels.values():
            got = (value or {}).get("value", "")
            if got:
                return got
        return ""

    people: dict[str, dict] = {}
    shards = sorted(glob.glob(str(ITEMS / "*.jsonl.gz")))
    print(f"streaming {len(shards):,} shards", flush=True)
    for n, shard in enumerate(shards, 1):
        with gzip.open(shard, "rt", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                try:
                    entity = json.loads(line)
                except json.JSONDecodeError:
                    continue
                qid = entity.get("id")
                if not qid or HUMAN not in targets(entity, INSTANCE_OF):
                    continue
                fathers = targets(entity, FATHER)
                people[qid] = {
                    "label": label_of(entity),
                    "father": fathers[0] if fathers else "",
                    "sex": SEX_LETTER.get((targets(entity, SEX) or [""])[0], ""),
                }
        if n % 400 == 0:
            print(f"  {n:,}/{len(shards):,}, {len(people):,} humans", flush=True)
    print(f"{len(people):,} humans", flush=True)

    with_father = sum(1 for r in people.values() if r["father"])
    print(f"{with_father:,} state a P22 father", flush=True)

    rows = []
    tally: Counter[str] = Counter()
    for qid, rec in people.items():
        tokens = (rec["label"] or "").split()
        if len(tokens) < 2:
            continue
        fid = rec["father"]
        frec = people.get(fid) if fid else None
        fname = (frec or {}).get("label", "").split()
        fgiven = fname[0] if fname else ""
        fstems = geni.stems(fgiven) if fgiven else set()

        for i, token in enumerate(tokens[1:], start=1):
            if token.casefold() in geni.ABSENT or geni.ORDINAL.match(token):
                continue
            form = geni.has_patronymic_form(token)
            derived = (geni.derives_from_father(token, fgiven, fstems)
                       if fgiven else None)
            if derived:
                verdict, evidence = "patronymic", derived
            elif form and not fid:
                verdict = ("surname: patronymic form conflicts with recorded sex"
                           if geni.sex_conflict(form, rec["sex"])
                           else "patronymic (inferred, no father recorded)")
                evidence = form
            elif form and not fgiven:
                verdict, evidence = "AMBIGUOUS: form, father unnamed", form
            elif form:
                verdict, evidence = "AMBIGUOUS: form, father differs", form
            elif not fid:
                verdict, evidence = "no father recorded", ""
            elif not fgiven:
                verdict, evidence = "father has no label", ""
            else:
                verdict, evidence = "not patronymic", ""
            tally[verdict] += 1
            rows.append([qid, rec["label"], token, i, fid, fgiven,
                         rec["sex"], verdict, evidence, form or ""])

    header = ["qid", "label", "token", "position", "father_qid",
              "father_given", "sex", "verdict", "evidence", "form"]
    OUT_CSV_STEM.parent.mkdir(parents=True, exist_ok=True)
    for old in OUT_CSV_STEM.parent.glob(f"{OUT_CSV_STEM.name}-*.csv"):
        old.unlink()
    part, handle, writer = 1, None, None
    written = 0
    paths = []
    for row in rows:
        if handle is None:
            path = OUT_CSV_STEM.with_name(f"{OUT_CSV_STEM.name}-{part}.csv")
            handle = path.open("w", encoding="utf-8", newline="")
            writer = csv.writer(handle)
            writer.writerow(header)
            paths.append(path)
        writer.writerow(row)
        written += 1
        if written % 50000 == 0 and handle.tell() > PART_LIMIT:
            handle.close()
            handle, writer = None, None
            part += 1
    if handle is not None:
        handle.close()

    total = sum(tally.values())
    L: list[str] = []
    add = L.append
    add("# Patronymics on the Wikidata side")
    add("")
    add("**Queue item 11.** Emma, 2026-08-15: *\"we also should be running this")
    add("processing on both the geni stuff and the wiki data stuff.\"*")
    add("")
    add("Same method as `reports/patronymic-classification.md` — the **father's**")
    add("given name decides, never the token's shape — reusing that script's form")
    add("tables and father test by import, so the two cannot drift apart.")
    add("")
    add(f"**{len(people):,} humans in the store, {with_father:,} stating a `P22`")
    add(f"father, {total:,} name tokens classified.**")
    add("")
    add("| verdict | tokens | share |")
    add("| --- | ---: | ---: |")
    for key, n in tally.most_common():
        add(f"| {key} | {n:,} | {100.0*n/max(total,1):.1f}% |")
    add("")
    add("## The limitation, stated rather than worked around")
    add("")
    add("**Wikidata gives no `GIVN`/`SURN` split here, so the tokens are the")
    add("label's words.** `P735`/`P734` name *items* rather than strings, and")
    add("resolving those to strings needs the name-item download that is still")
    add("running. A label is a rendering of a name, not its parts, so a token's")
    add("position in it is weaker evidence than a GEDCOM field.")
    add("")
    add("**A father with no label yields no verdict**, exactly as an unnamed father")
    add("does on the Geni side. Absence of evidence is not a `no`.")
    OUT_MD.write_text("\n".join(L) + "\n", encoding="utf-8")

    print(f"\nwrote {OUT_CSV} ({len(rows):,} rows) and {OUT_MD}")
    for key, n in tally.most_common():
        print(f"  {key:<52} {n:>9,}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
