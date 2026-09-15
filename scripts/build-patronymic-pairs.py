"""Create the missing half of a patronymic pair, where it is safe to.

Ruled 2026-09-14: *"We really should be always creating patronymics in pairs. Feminine and
masculine version in a pair in the quickstatements ... Honestly I am not 100% sure about all of
this stuff. But I think the spelling equivalents are just regional and there is a clear
distinction there."*

The distinction is real and measurable. Lift over `reports/name-item-plan.csv` —
`P(female|male) / P(female)`, which strips out `-sdatter` merely being the commonest ending —
separates the registers cleanly: `-sen`↔`-sdatter` Dano-Norwegian ×1.13, `-sson`↔`-sdotter`
Swedish ×1.49, `-sson`↔`-sdóttir` Icelandic ×2.49.

## ⛔ And the uncertainty was warranted: pairing everything mints names nobody bore

1,882 patronymic tokens; 951 already have their counterpart, 671 do not. Pairing those 671
mechanically produces `Williamsdotter`, `Jacksdotter`, `Watsdotter` — Anglo surnames that
fossilised centuries ago — and `Sachsdatter`, because **`Sachsen` is Saxony**.

§ *PARSE PATRONYMICS BY FORM* cannot save this one. The form `-son` is identical in Bergen and in
Yorkshire; only the culture separates them, and the form does not carry culture.

## The two guards, and both are needed

    1. LOCALITY     the token is borne by somebody in the universe — `reports/garborg-qids.tsv`,
                    § *ONLY EVER EDIT THINGS IN THE UNIVERSE OR ONE STEP ADJACENT TO IT*
    2. THE FATHER   the stem, after the genitive `s`, is itself a GIVEN name borne in the
                    universe

Locality alone cuts 671 → 91 and **still passes `Hessen`, `Meissen` and `Nelson`**, because
people in our universe have German and English ancestry, so a German place name is genuinely
borne by somebody inside it. The father test is what rejects those: `Rasmus` is a given name here
and `Sach`, `Mei`, `Nel`, `Wil` and `Thomp` are not.

Together: **62 pairs**, every one a real Norwegian patronymic.

It also rejects `Tørresson`, `Estridsen` and `Brodersen`, whose stems are real names elsewhere
but are not borne as given names inside this universe. That is the conservative direction and it
is the right one — § *it's better to create no name object than a bad one*.

## The genitive `s` is shared, not doubled

`Rasmussen` is `Rasmus` + `sen`, so the counterpart is `Rasmusdatter`, never `Rasmussdatter`.
**32 of the candidates had this fault**, including `Johannessen`, `Andreassen`, `Torjussen`,
`Eliassen` and `Anderssen`. `namemodel.patronymic_counterpart` owns that rule, so this script and
any future caller cannot disagree about it.

    PYTHONPATH=src python scripts/build-patronymic-pairs.py

Writes `reports/wikidata-patronymic-pairs.qs`. Offline; reads committed files only.
"""

from __future__ import annotations

import collections
import csv
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

from namemodel import patronymic_counterpart  # noqa: E402

LEDGER = REPO / "reports" / "garborg-qids.tsv"
DISPLAY = REPO / "reports" / "display-names.csv"
PLAN = REPO / "reports" / "name-item-plan.csv"
OUT = REPO / "reports" / "wikidata-patronymic-pairs.qs"

PATRONYMIC_CLASS = "Q110874"
MATRONYMIC_CLASS = "Q110874"          # same class; the description is what separates them

#: Per run. The same reasoning as every other cap here: a name item is cheap to add and
#: expensive to argue about, and a hundred new ones in a day from an account that made none
#: yesterday is the shape that draws attention.
PAIRS_PER_RUN = 40


def universe_geni_ids():
    with LEDGER.open(encoding="utf-8", newline="") as fh:
        return {(r.get("geni_id") or "").strip()
                for r in csv.DictReader(fh, delimiter="\t") if (r.get("geni_id") or "").strip()}


def borne_in_universe(ours):
    """`(every token, given names only)` borne by somebody in the universe."""
    csv.field_size_limit(10 ** 7)
    every, givens = collections.Counter(), collections.Counter()
    with DISPLAY.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            if (row.get("geni_id") or "").strip() not in ours:
                continue
            for tok in (row.get("givn") or "").split():
                givens[tok.casefold()] += 1
            for field in ("givn", "surn", "marnm"):
                for tok in (row.get(field) or "").split():
                    every[tok.casefold()] += 1
    return every, givens


def main() -> int:
    ours = universe_geni_ids()
    every, givens = borne_in_universe(ours)

    with PLAN.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    existing = {(r["token"].casefold(), r["usage"]) for r in rows}

    pairs = []
    for row in rows:
        if row["usage"] != "patronymic":
            continue
        token = row["token"]
        want = patronymic_counterpart(token)
        if not want or (want.casefold(), "patronymic") in existing:
            continue
        # 1. locality
        if not every.get(token.casefold()):
            continue
        # 2. the father must be a given name borne here
        base = token
        for suf in ("sdatter", "sdotter", "sdóttir", "sson", "sen", "søn", "sønn", "son",
                    # **Finnish, ruled 2026-09-15.** Without these the stem stays the whole
                    # token, the father is never found and guard 2 rejects every Finnish pair.
                    # That fails CLOSED, which is safe, but it also means the 45,187-occurrence
                    # family would silently never pair. See `namemodel.FINNISH_PATRONYMIC`.
                    "npoika", "ntytär", "ntytar"):
            if token.casefold().endswith(suf):
                base = token[:len(token) - len(suf)]
                break
        # **The genitive comes off to find the father**, and for Finnish the suffix strip above
        # already took it: `npoika` carries the `n`, so `Juhonpoika` leaves `Juho` outright.
        # Only the Scandinavian forms need the extra `s` off, and the guard below tries `base`
        # as well, so `Rasmussen` is checked as both `Rasmu` and `Rasmus`.
        #
        # **Finnish consonant gradation is deliberately NOT modelled.** `Matti` takes the
        # genitive `Matin`, so the stem is not always the nominative -- but measured over the
        # corpus, **34,685 of 45,135 Finnish patronymic occurrences (77%) find the father
        # directly and only 127 (0%) would need gradation restored.** A Finnish morphology
        # module for 127 occurrences is exactly what § *A small component is IGNORED* refuses.
        father = base[:-1] if base.casefold().endswith("s") else base
        if not (givens.get(father.casefold()) or givens.get(base.casefold())):
            continue
        pairs.append((int(row.get("bearers") or 0), token, want))

    pairs.sort(key=lambda p: (-p[0], p[1]))
    batch = pairs[:PAIRS_PER_RUN]

    lines = [
        "# The missing half of a patronymic pair. Ruled 2026-09-14: patronymics are created in",
        "# pairs, feminine and masculine at the same time.",
        "#",
        "# Two guards, both needed: the token is borne inside the universe, AND its stem is a",
        "# given name borne inside the universe. Locality alone still passes Sachsen (Saxony),",
        "# Hessen and Meissen, because people here have German ancestry.",
        "#",
        "# The genitive s is shared: Rasmussen -> Rasmusdatter, never Rasmussdatter.",
        "",
    ]
    for bearers, have, want in batch:
        lines.append(f"# {want} -- the counterpart of {have} ({bearers} bearer(s))")
        lines.append("CREATE")
        lines.append(f'LAST\tLen\t"{want}"')
        lines.append(f'LAST\tLmul\t"{want}"')
        lines.append('LAST\tDen\t"patronymic"')
        lines.append(f"LAST\tP31\t{PATRONYMIC_CLASS}")
        lines.append("")

    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(f"{len(pairs)} safe pairs; {len(batch)} written to {OUT.name} "
          f"(PAIRS_PER_RUN {PAIRS_PER_RUN})")
    print(f"   {len(pairs) - len(batch)} held for later runs")
    for bearers, have, want in batch[:10]:
        print(f"   {have:<20} + {want}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
