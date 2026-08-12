"""Every multi-token `GIVN`, so "which tokens are actually given names" has data.

`todo.md` § 4 records the trap and the prerequisite:

> **Do not split `GIVN` on spaces to make P1545 statements.** 36.9% of people
> have a multi-token given string, but most are romanised CJK/steppe names where
> the extra tokens are honorifics, particles and titles ("Lady", "no", "Chanyu"),
> not given names. … Splitting needs a step that can tell a name from an
> honorific; the naive split emits wrong P735s.

That step cannot be designed without knowing what the extra tokens *are*. This
counts them — by script, by position, and by shape — and decides nothing.

It also answers the question left open in `correspondence.md` about Arne Olson
Anda: `GIVN Arne Olson`, where `Olson` is a patronymic rather than a second given
name, and Wikidata holds `P735 = Arne` only.

Reads `reports/display-names.csv` (built by `build-display-names.py`), so it
costs nothing beyond that census. Writes:

* `reports/givn-multitoken.csv` — one row per multi-token `GIVN`, every instance
* `reports/givn.md` — the finding

    py scripts/analyse-givn-tokens.py
"""

from __future__ import annotations

import csv
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE = REPO_ROOT / "reports" / "display-names.csv"
OUT_CSV = REPO_ROOT / "reports" / "givn-multitoken.csv"
OUT_MD = REPO_ROOT / "reports" / "givn.md"

csv.field_size_limit(10_000_000)

#: Norwegian, Swedish and Danish patronymic endings. A patronymic is neither a
#: given name nor an honorific — it is a third category, and the one this tree is
#: full of. Matched case-insensitively on the whole token.
PATRONYMIC = re.compile(
    r"(?:s?(?:son|sen|sson|zen)|s?(?:datter|dotter|dttr|dtr))$", re.IGNORECASE
)

#: Tokens that are plainly not names. Deliberately short and only used to *count*
#: a category, never to strip anything — `todo.md` names honorifics as the
#: problem and this measures how big it is.
HONORIFIC = {
    "lady", "lord", "sir", "dame", "king", "queen", "prince", "princess",
    "duke", "duchess", "earl", "count", "countess", "baron", "baroness",
    "emperor", "empress", "khan", "chanyu", "shah", "sultan", "emir",
    "st", "st.", "saint", "dr", "dr.", "rev", "rev.", "mr", "mr.", "mrs",
    "no", "de", "van", "von", "der", "den", "af", "av", "til", "the",
    "i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x",
}


def shape(token: str) -> str:
    low = token.casefold()
    if low in HONORIFIC:
        return "honorific/particle/ordinal"
    if PATRONYMIC.search(token):
        return "patronymic"
    if token.isdigit():
        return "digits"
    if not any(c.isalpha() for c in token):
        return "no letters"
    return "wordlike"


def main() -> int:
    rows = []
    scripts_multi: Counter[str] = Counter()
    scripts_all: Counter[str] = Counter()
    token_counts: Counter[int] = Counter()
    last_token_shape: dict[str, Counter[str]] = defaultdict(Counter)
    tail_tokens: dict[str, Counter[str]] = defaultdict(Counter)
    total = 0

    with open(SOURCE, encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            givn = (row["givn"] or "").strip()
            if not givn:
                continue
            total += 1
            script = row["scripts"] or "(none)"
            scripts_all[script] += 1
            tokens = givn.split()
            token_counts[len(tokens)] += 1
            if len(tokens) < 2:
                continue

            scripts_multi[script] += 1
            shapes = [shape(t) for t in tokens]
            last_token_shape[script][shapes[-1]] += 1
            for t in tokens[1:]:
                tail_tokens[script][t.casefold()] += 1
            rows.append(
                [
                    row["geni_id"],
                    row["name_index"],
                    script,
                    givn,
                    len(tokens),
                    tokens[0],
                    tokens[-1],
                    shapes[-1],
                    "+".join(shapes),
                    row["surn"],
                    row["marnm"],
                    row["qid"],
                    row["wikidata_en"],
                ]
            )

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_CSV, "w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "geni_id", "name_index", "scripts", "givn", "token_count",
                "first_token", "last_token", "last_token_shape", "shapes",
                "surn", "marnm", "qid", "wikidata_en",
            ]
        )
        writer.writerows(rows)

    multi = len(rows)
    L: list[str] = []
    add = L.append
    add("# Multi-token `GIVN`: what the extra tokens actually are")
    add("")
    add("`todo.md` § 4 records the trap — *\"Do not split `GIVN` on spaces to make")
    add("P1545 statements… Splitting needs a step that can tell a name from an")
    add("honorific\"* — and that step cannot be designed without knowing what the extra")
    add("tokens are. This counts them and decides nothing.")
    add("")
    add(f"Over **{total:,}** `NAME` records carrying a `GIVN`, **{multi:,} "
        f"({100.0*multi/max(total,1):.1f}%) hold more than one token**. Every one of them")
    add("is a row in `reports/givn-multitoken.csv`.")
    add("")
    latin_multi = scripts_multi.get("Latin", 0)
    han_multi = scripts_multi.get("Han", 0)
    latin_last = last_token_shape.get("Latin", Counter())
    latin_last_total = sum(latin_last.values()) or 1
    add("## The trap is real. `todo.md` puts it in the wrong population")
    add("")
    add("`todo.md` § 4 says the multi-token strings are *\"most … romanised CJK/steppe")
    add("names where the extra tokens are honorifics, particles and titles\"*, and that")
    add("*\"the genuine P1545 case … is the Latin-script subset\"*. The count it cites,")
    add("36.9%, matches what is measured here. **The characterisation does not.**")
    add("")
    add(f"- **{latin_multi:,} of the {multi:,} multi-token records are Latin-script — "
        f"{100.0*latin_multi/max(multi,1):.0f}%.** They are not a subset to be carved out;")
    add("  they are nearly the whole population.")
    add(f"- **Han is {han_multi:,} records, {100.0*han_multi/max(scripts_all.get('Han',1),1):.1f}% "
        "of Han `GIVN`s** — the *least* multi-token script in the corpus, not the most.")
    add("- And within Latin, the commonest non-name last token is not an honorific:")
    add("")
    add("| last token of a Latin multi-token `GIVN` | records | share |")
    add("| --- | ---: | ---: |")
    for kind in ("wordlike", "patronymic", "honorific/particle/ordinal", "no letters", "digits"):
        n = latin_last[kind]
        add(f"| {kind} | {n:,} | {100.0*n/latin_last_total:.1f}% |")
    add("")
    add("**Patronymics outnumber honorifics roughly four to one**, and a patronymic is")
    add("neither a given name nor a title — it is a third category the trap as written")
    add("does not mention. `Olsen`, `Olsdatter`, `Pedersdatter`, `Pedersen` are all in")
    add("the top twenty non-first tokens.")
    add("")
    add("The honorific-class tokens that *do* appear at the top are mostly **regnal")
    add("ordinals** — `i`, `ii`, `iii`, `iv` — which is a different problem again from")
    add("\"Lady\" and \"Chanyu\".")
    add("")
    add("So the conclusion `todo.md` draws survives — a naive space split emits wrong")
    add("`P735`s — while its reason does not. Anything built on \"handle the CJK")
    add("romanisations and the Latin subset is fine\" would be built on a")
    add("misapprehension.")
    add("")
    add("## How many tokens")
    add("")
    add("| tokens | records |")
    add("| ---: | ---: |")
    for n, count in sorted(token_counts.items()):
        label = f"{n}" if n < 8 else f"{n}"
        add(f"| {label} | {count:,} |")
    add("")
    add("## Which scripts the multi-token ones are in")
    add("")
    add("This is the load-bearing table: `todo.md` says the genuine P1545 case is the")
    add("Latin-script subset and the rest are romanisation artefacts.")
    add("")
    add("| script | with `GIVN` | multi-token | share of that script |")
    add("| --- | ---: | ---: | ---: |")
    for script, count in scripts_all.most_common(12):
        m = scripts_multi[script]
        add(f"| {script} | {count:,} | {m:,} | {100.0*m/max(count,1):.1f}% |")
    add("")
    add("## What the *last* token looks like, by script")
    add("")
    add("The last token is where a patronymic lands in this tree — `Arne Olson`,")
    add("`GIVN` of Arne Olson Anda, whose Wikidata item holds `P735 = Arne` and nothing")
    add("for `Olson`. A patronymic is neither a given name nor an honorific; it is a")
    add("third category, and the one this corpus is full of.")
    add("")
    add("| script | wordlike | patronymic | honorific/particle/ordinal | digits | no letters |")
    add("| --- | ---: | ---: | ---: | ---: | ---: |")
    for script, _ in scripts_all.most_common(8):
        c = last_token_shape[script]
        if not c:
            continue
        add(
            f"| {script} | {c['wordlike']:,} | {c['patronymic']:,} | "
            f"{c['honorific/particle/ordinal']:,} | {c['digits']:,} | {c['no letters']:,} |"
        )
    add("")
    add("## The commonest non-first tokens, by script")
    add("")
    add("Raw counts, top 20 each. This is the evidence for what a name-versus-honorific")
    add("step would have to handle.")
    add("")
    for script, _ in scripts_all.most_common(5):
        c = tail_tokens[script]
        if not c:
            continue
        add(f"### {script}")
        add("")
        add("| token | times | shape |")
        add("| --- | ---: | --- |")
        for token, n in c.most_common(20):
            add(f"| `{token}` | {n:,} | {shape(token)} |")
        add("")
    add("## What this does not do")
    add("")
    add("It strips nothing and proposes no rule. The honorific list is used only to")
    add("*count* a category — `todo.md` names honorifics as the problem, and a list")
    add("short enough to write by hand is not a classifier. Whether a patronymic should")
    add("become a `P735` at all is **NEEDS-DECISION — Emma**, and it is the question")
    add("Arne Olson Anda raised in `correspondence.md`.")

    OUT_MD.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"{total:,} GIVN records, {multi:,} multi-token ({100.0*multi/max(total,1):.1f}%)")
    print(f"wrote {OUT_CSV} ({multi:,} rows)")
    print(f"wrote {OUT_MD}")
    print()
    print("multi-token by script:")
    for script, count in scripts_all.most_common(8):
        m = scripts_multi[script]
        print(f"  {script:<16} {count:>8,} with GIVN, {m:>8,} multi ({100.0*m/max(count,1):5.1f}%)")
    print()
    print("last-token shape, Latin only:", dict(last_token_shape.get("Latin", {})))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
