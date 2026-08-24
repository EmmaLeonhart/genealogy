"""One day's Garborg batch: everything that can run in a SINGLE QuickStatements run.

    python scripts/build-garborg-day.py

**Emma, 2026-08-24, after running yesterday's file:** *"I only ran some of the quick
statements because many of them required links that couldn't exist... The siblings all
being connected to each other: they should be connected to each other, but they
couldn't be connected to each other without things that required their QIDs, which we
had just created. This means this is going to be the practical limitation of what our
quick statements can do. With every day, we are kind of going through a full run of
what we can do on the frontier like this."*

So the rule is: **a statement goes in only if both ends already have a QID.** Nothing
deferred, nothing commented out, nothing that fails. What could not run today becomes
tomorrow's batch, because tomorrow those items exist.

`reports/garborg-qids.tsv` is the ledger of who has one. It is filled from **Emma's
Wikidata contributions**, not from a bulk download — her instruction: *"You should be
looking at my contributions to see the new ones I've created."* Her account is 日巫女.

Each day therefore does three things, all runnable:

1. **Close the links that yesterday's creations made possible** — the reciprocal `P40`
   from the parents, and `P3373` among siblings who all have QIDs now.
2. **Create the next ring**, everyone one edge away from someone who has a QID.
3. **Link the new people to anything that already exists** — parents, spouses,
   siblings — but never to each other, because they are being minted right now.

Labels come with `ja` and `zh` from `reports/garborg-name-transliterations.tsv`, per
Emma 2026-08-24: *"we should also be adding their names in languages that are not
English, or at least in Japanese... and Chinese."*

Writes `reports/wikidata-garborg-day.qs` and `reports/garborg-carry-forward.tsv`.
"""
from __future__ import annotations

import argparse
import collections
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
csv.field_size_limit(1 << 30)
sys.stdout.reconfigure(encoding="utf-8")

from namemodel import (  # noqa: E402
    NICKNAME, aliases_for, classify, classify_fields, load_plan,
    statements_for)


def _load_gaps():
    """`garborg-existing-gaps.py` has a hyphen, so `import` cannot reach it."""
    import importlib.util
    path = Path(__file__).resolve().parent / "garborg-existing-gaps.py"
    spec = importlib.util.spec_from_file_location("garborg_existing_gaps", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.existing_state


existing_state = _load_gaps()

ROOT = Path(__file__).resolve().parent.parent
SEX = {"M": "Q6581097", "F": "Q6581072"}
HUMAN = "Q5"


def qs(text):
    """QuickStatements V1 cannot escape a double quote inside a string."""
    return (text or "").replace('"', "").strip()


def ledger():
    out = {}
    with open(ROOT / "reports" / "garborg-qids.tsv", encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            out[row["geni_id"]] = row["qid"]
    return out


def translit():
    out = {}
    with open(ROOT / "reports" / "garborg-name-transliterations.tsv",
              encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            out[row["token"]] = (row["ja"], row["zh"])
    return out


def _words():
    """The per-language relationship table from `build-nn-label-batch.py`.

    Imported rather than restated: it carries decisions that were paid for, notably
    that Danish and Norwegian take a different preposition depending on which way the
    relation runs (`datter af` but `mor til`), and that Slavic and Welsh are left out
    because they inflect the name after the relationship word.
    """
    import importlib.util
    path = Path(__file__).resolve().parent / "build-nn-label-batch.py"
    spec = importlib.util.spec_from_file_location("build_nn_label_batch", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.WORDS


WORDS = _words()


def describe_all(geni_id, facts, father, mother, labels, table):
    """`{lang: "daughter of Arne Olaus Fjørtoft Garborg"}` for a redacted person.

    Built from the nearest named parent. `ja` and `zh` are included **here** where
    `build-nn-label-batch.py` excludes them, and the reason it excludes them is the
    reason this can: it warns the phrase would come out `Gerard Spencerの娘`, mixing
    scripts, *because the relative's name has not been transliterated*. In this family
    it has — `reports/garborg-name-transliterations.tsv` covers every token — so the
    Japanese and Chinese forms are whole rather than half Latin.
    """
    sex = (facts.get(geni_id, {}).get("sex") or "")
    for parent in (father.get(geni_id), mother.get(geni_id)):
        if not parent:
            continue
        name = (labels.get(parent) or "").strip()
        if not name or name.lower() in ("nn", "private", "unknown", "?"):
            continue
        out = {}
        for lang, words in WORDS.items():
            group = words["child_of"]
            word = group.get(sex) or group[""]
            joiner = words["of"]
            if isinstance(joiner, dict):
                joiner = joiner.get("child_of", joiner[""])
            out[lang] = f"{word} {joiner} {qs(name)}"
        ja, zh = label_in(name, table)
        if ja:
            out["ja"] = f"{ja}の{'息子' if sex == 'M' else '娘' if sex == 'F' else '子'}"
            out["zh"] = f"{zh}之{'子' if sex == 'M' else '女' if sex == 'F' else '子女'}"
        return out
    return {}


def live_state():
    """`{qid: (label languages, properties)}` from the 2026-08-24 live read.

    Ground truth, and it outranks the store: the store was downloaded before Emma made
    most of these items, and the fallback in `absent` assumes an item outside the store
    was made by our own batch and so carries no name statements. She edits by hand, so
    that assumption is wrong exactly where it matters most.

    A row marked `no` was **not** re-read and is deliberately omitted from the result,
    so it falls through to the store and then to the assumption rather than being
    reported as an item with no properties at all.
    """
    out = {}
    path = ROOT / "reports" / "garborg-live-state.tsv"
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.startswith("#") or line.startswith("qid\t"):
                continue
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 4 or parts[1] == "no":
                continue
            langs = {p.strip() for p in parts[2].replace(",", " ").split()
                     if p.strip().isalpha()}
            out[parts[0]] = (langs, set(parts[3].split()))
    return out


def read_tree():
    fam_p = collections.defaultdict(list)
    fam_c = collections.defaultdict(list)
    fams = collections.defaultdict(list)
    famc = collections.defaultdict(list)
    cur = kind = None
    with open(ROOT / "out" / "merged.ged", encoding="utf-8", errors="replace") as f:
        for line in f:
            if line.startswith("0 @"):
                p = line.split()
                cur, kind = p[1][2:-1], (p[2].strip() if len(p) > 2 else "")
            elif cur and line.startswith("1 "):
                tag, _, val = line[2:].strip().partition(" ")
                if kind == "FAM":
                    if tag in ("HUSB", "WIFE"):
                        fam_p[cur].append(val[2:-1])
                    elif tag == "CHIL":
                        fam_c[cur].append(val[2:-1])
                elif kind == "INDI":
                    if tag == "FAMS":
                        fams[cur].append(val[2:-1])
                    elif tag == "FAMC":
                        famc[cur].append(val[2:-1])
    return fam_p, fam_c, fams, famc


def label_in(label, table):
    """(ja, zh) for a whole name, or (None, None) if any token is unknown.

    Partial is worse than absent: half a name in katakana and half in Latin is not a
    Japanese label, it is a broken one.
    """
    ja, zh = [], []
    for token, _usage, _o in classify(label):
        pair = table.get(token)
        if not pair:
            return None, None
        ja.append(pair[0])
        zh.append(pair[1])
    return "・".join(ja), "·".join(zh)


def name_lines(label, plan, geni_id, father_qid, fields=None):
    """`P735`/`P734`/`P5056` lines for one person, and what could not be emitted.

    **Only tokens whose item already exists.** A name item this run is creating
    cannot be pointed at, same single-run rule as everybody else, so the rest waits
    for `reports/wikidata-garborg-name-items.qs` to have been run.

    QuickStatements takes qualifiers exactly like references, property then value on
    the same line: `LAST<TAB>P735<TAB>Q629347<TAB>P1545<TAB>"1"<TAB>P7452<TAB>Q3409033`.
    """
    out, notes = [], []
    lines, why = statements_for(label, plan, geni_id, father_qid=father_qid,
                                fields=fields)
    for prop, value, quals in lines:
        # `P1449` *nickname* is monolingual TEXT, so QuickStatements wants a language
        # tag and quotes rather than a bare item id.
        rendered = f'en:"{value}"' if prop == NICKNAME else value
        parts = [f"LAST	{prop}	{rendered}"]
        for qprop, qvalue in quals:
            # A series ordinal is a string; everything else here is an item.
            qv = f'"{qvalue}"' if qprop == "P1545" else qvalue
            parts.append(f"{qprop}	{qv}")
        out.append("	".join(parts))
    notes.extend(why)
    return out, notes


def main():
    # `--skip-nn` is a per-run choice, not a rule. Emma, 2026-08-24: *"for this
    # quickstatements run the NN people are not worth creating"* -- for THIS run. The
    # standing rule in `CLAUDE.md` is that redacted people go in, with the marker in
    # `mul` and a formulaic description elsewhere, so this must not become the default.
    ap = argparse.ArgumentParser()
    ap.add_argument("--skip-nn", action="store_true",
                    help="omit redacted/NN people from this batch (a per-run choice)")
    args = ap.parse_args()

    have = ledger()
    table = translit()
    plan = load_plan()
    fam_p, fam_c, fams, famc = read_tree()
    print(f"{len(have)} people already carry a QID; {len(table)} tokens transliterated")

    # Everyone one edge away from somebody who has a QID.
    frontier = {}
    for person in have:
        for fam in fams.get(person, []) + famc.get(person, []):
            for other in set(fam_p.get(fam, [])) | set(fam_c.get(fam, [])):
                if other not in have:
                    frontier.setdefault(other, fam)
    print(f"{len(frontier)} people one edge away and not yet on Wikidata")

    ids = set(frontier) | set(have)
    facts, labels = {}, {}
    with open(ROOT / "reports" / "derived-facts.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["geni_id"] in ids:
                facts[row["geni_id"]] = row
    with open(ROOT / "reports" / "derived-labels.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["geni_id"] in ids:
                labels[row["geni_id"]] = row["label_en"] or row["label_mul"]

    # **The GEDCOM name FIELDS, which is where name objects come from.** Emma,
    # 2026-08-24: *"I thought we were resolving name objects but now we're determining
    # which name field to use as a source of the label?"* -- catching that the name
    # model was re-parsing the rendered label. The first NAME record wins; later ones
    # are alternate forms and `derive-labels.py` already owns those.
    fields = {}
    with open(ROOT / "reports" / "display-names.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["geni_id"] in ids and row["geni_id"] not in fields:
                fields[row["geni_id"]] = {k: row.get(k, "") for k in
                                          ("givn", "surn", "nick", "marnm")}

    # Relationships, from the tree, in both directions.
    father, mother = {}, {}
    children = collections.defaultdict(set)
    spouses = collections.defaultdict(set)
    siblings = collections.defaultdict(set)
    for fam, parents in fam_p.items():
        kids = fam_c.get(fam, [])
        for p in parents:
            for k in kids:
                children[p].add(k)
                sex = (facts.get(p, {}).get("sex") or "")
                (father if sex == "M" else mother)[k] = p
        for a in parents:
            for b in parents:
                if a != b:
                    spouses[a].add(b)
        for a in kids:
            for b in kids:
                if a != b:
                    siblings[a].add(b)

    lines, carried = [], []

    def ref(g):
        return f'\tS2600\t"{g}"'

    # ---- 1. everything missing from people who ALREADY have QIDs ------------
    # Emma, 2026-08-24, asked whether to add properties to items that already exist:
    # yes. This section used to close *links* only, so an item that existed was never
    # asked whether it was missing a date, a name statement or a label -- which is a
    # large part of what "not remotely comprehensive" meant. `Q467497` Arne Garborg
    # had no `P22` father and no `P25` mother while both his parents had QIDs.
    state = existing_state(set(have.values()))
    # A live read beats both the store and the guess. `reports/garborg-live-state.tsv`
    # records what each item held on 2026-08-24; the store predates most of them and
    # the fallback below assumes our own batch made them, which is wrong wherever Emma
    # edited by hand. Eivind is the case: he carries P735/P734/P5056 she added herself.
    state.update(live_state())
    lines += [
        "# 1. Everything missing from people who already have items -- the links that",
        "#    yesterday's creations made possible, and the properties never emitted.",
        "#    Every subject and every value already has a QID.",
        "",
    ]
    seen = set()

    def add(q, prop, value, g):
        if (q, prop, value) in seen:
            return
        seen.add((q, prop, value))
        lines.append(f"{q}\t{prop}\t{value}{ref(g)}")

    def absent(q, prop):
        """True when the item demonstrably lacks `prop`, or our own batch made it.

        The store answers exactly for an item it holds. For one it does not hold --
        Emma's creations from the last two days -- what the item carries is what our
        `CREATE` block carried, and name statements were only added on 2026-08-24, so
        those are genuinely absent. Either way QuickStatements merges an identical
        statement rather than duplicating it, so a redundant line is a no-op.
        """
        known = state.get(q)
        return prop not in known[1] if known else True

    for g, q in sorted(have.items()):
        for prop, target in (("P22", father.get(g)), ("P25", mother.get(g))):
            if target and target in have and absent(q, prop):
                add(q, prop, have[target], g)
        for kid in sorted(children.get(g, ())):
            if kid in have:
                add(q, "P40", have[kid], g)
        for sib in sorted(siblings.get(g, ())):
            if sib in have:
                add(q, "P3373", have[sib], g)
        for sp in sorted(spouses.get(g, ())):
            if sp in have:
                add(q, "P26", have[sp], g)

        # Name statements, but never onto an item that already states one: `Q467497`
        # carries `P735` Arne, and our label reads the parenthesised `(Arne)` as a
        # middle name -- emitting it would contradict a curated statement rather than
        # add to it. `CLAUDE.md`: the purpose is to ADD, not to correct.
        if absent(q, "P735") and absent(q, "P734"):
            dad = father.get(g)
            for line in name_lines(labels.get(g, ""), plan, g,
                                   have.get(dad) if dad else None)[0]:
                lines.append(line.replace("LAST\t", f"{q}\t", 1))

        # A label ONLY in a language the item does not have. `Len`/`Lmul` REPLACE,
        # and `Q467497` is labelled `Arne Garborg` on Wikidata against our derived
        # `Aadne (Arne) Eivindson Garborg` -- emitting ours would overwrite a better
        # label with a Geni display string.
        langs = state.get(q, (set(), set()))[0]
        ja, zh = label_in(labels.get(g, ""), table)
        if ja:
            for code, value in (("ja", ja), ("zh", zh)):
                if code not in langs:
                    lines.append(f'{q}\tL{code}\t"{value}"')
    print(f"{len(seen)} statements added to existing items")
    lines.append("")

    # ---- 2. the next ring ---------------------------------------------------
    lines += ["# 2. The next ring. Each is linked only to items that already exist;",
              "#    links between two of these wait for tomorrow, when they have QIDs.",
              ""]
    created = 0
    for g in sorted(frontier, key=lambda x: labels.get(x, "")):
        f, label = facts.get(g), qs(labels.get(g, ""))
        if not f:
            carried.append((g, label, "no derived facts"))
            continue

        # A redacted profile is created and gets NO label. `CLAUDE.md`: *"Private is
        # a redaction marker, not a name, and an item labelled that asserts something
        # false while being impossible to find. The P2600 is what makes it
        # retrievable."* The person is real and none of the structure is redacted —
        # the Geni id, the sex, the parents, the dates all come through.
        low = label.lower()
        redacted = "<private>" in low or low.startswith("private")
        if redacted and args.skip_nn:
            carried.append((g, label, "redacted: skipped by --skip-nn for this run"))
            continue

        lines.append("CREATE")
        if redacted or not label:
            # **NOT unlabelled.** `CLAUDE.md` § *`NN` is PRESERVED in `mul`.
            # Descriptive labels are ADDED in other languages* -- the marker stays in
            # `mul` and every local language gets a formulaic description built from
            # the nearest named relative. Emma, 2026-08-16: *"NN and private are the
            # same thing here"*. The surname survives redaction and is real data, so
            # `mul` reads `NN Garborg`, not a bare `NN`.
            # The surname survives redaction and is real data -- CLAUDE.md measured
            # 3,605 such profiles. `<private> Garborg` -> `Garborg`.
            surname = " ".join(t for t in qs(labels.get(g, "")).split()
                               if not t.lower().startswith("<private")
                               and t.lower() not in ("private", "nn"))
            lines.append(f'LAST\tLmul\t"{("NN " + surname).strip()}"')
            described = describe_all(g, facts, father, mother, labels, table)
            for code, value in sorted(described.items()):
                lines.append(f'LAST\tL{code}\t"{value}"')
            if not described:
                carried.append((g, label, "redacted: no named relative to describe by"))
        else:
            # **The MARRIED name is the primary label; the BIRTH name is an alias.**
            # Emma, 2026-08-24, after running the first batch: *"the married name is
            # the primary label and the birth name is amul"*, then *"we move the lmul
            # to amul and the lja to aja and so on"*. The first version had it exactly
            # backwards -- birth name in `en` and `mul`, married name pushed out as an
            # `Aen` alias -- and cost her a corrective run over five items.
            f_ = fields.get(g, {})
            surn = " ".join((f_.get("surn") or "").split())
            marnm = " ".join((f_.get("marnm") or "").split())
            # `SURN` must be populated for `_MARNM` to mean *married*: `CLAUDE.md`
            # measured 43% of `_MARNM` values as the ONLY surname on the record, where
            # it is the family name rather than a married one.
            is_married = bool(marnm and surn and marnm.casefold() != surn.casefold())

            given = [t for t, u, _o in classify_fields(f_.get("givn", ""), "")
                     if u in ("given", "patronymic")]
            primary = " ".join(given + marnm.split()) if is_married else label
            birth = " ".join(given + surn.split()) if is_married else ""

            lines.append(f'LAST\tLen\t"{qs(primary)}"')
            lines.append(f'LAST\tLmul\t"{qs(primary)}"')
            if birth and qs(birth) != qs(primary):
                lines.append(f'LAST\tAen\t"{qs(birth)}"')
                lines.append(f'LAST\tAmul\t"{qs(birth)}"')

            ja, zh = label_in(primary, table)
            if ja:
                lines.append(f'LAST\tLja\t"{ja}"')
                lines.append(f'LAST\tLzh\t"{zh}"')
                bja, bzh = label_in(birth, table) if birth else (None, None)
                if bja and bja != ja:
                    lines.append(f'LAST\tAja\t"{bja}"')
                    lines.append(f'LAST\tAzh\t"{bzh}"')
            else:
                carried.append((g, label, "no transliteration for every token"))
        lines.append(f"LAST\tP31\t{HUMAN}")
        if f["sex"] in SEX:
            lines.append(f"LAST\tP21\t{SEX[f['sex']]}")
        lines.append(f'LAST\tP2600\t"{g}"')
        for prop, iso, prec in (("P569", f["birth_date_iso"], f["birth_date_precision"]),
                                ("P570", f["death_date_iso"], f["death_date_precision"])):
            if iso and prec:
                lines.append(f"LAST\t{prop}\t{iso}/{prec}{ref(g)}")
        for prop, target in (("P22", father.get(g)), ("P25", mother.get(g))):
            if target and target in have:
                lines.append(f"LAST\t{prop}\t{have[target]}{ref(g)}")
        for sp in sorted(spouses.get(g, ())):
            if sp in have:
                lines.append(f"LAST\tP26\t{have[sp]}{ref(g)}")
        for sib in sorted(siblings.get(g, ())):
            if sib in have:
                lines.append(f"LAST\tP3373\t{have[sib]}{ref(g)}")
        for kid in sorted(children.get(g, ())):
            if kid in have:
                lines.append(f"LAST\tP40\t{have[kid]}{ref(g)}")

        # The name model. Emma, 2026-08-24: *"we should be modelling the names
        # properly, which he didn't do."* Only tokens whose item ALREADY exists --
        # the ones still to be made are in reports/wikidata-garborg-name-items.qs and
        # join the batch the day after that runs, same single-run rule as everyone.
        # A redacted profile gets no name statements for the same reason it gets no
        # label: `<private>` is Geni withholding the name, not a name. Asking the plan
        # for a `<private>` given-name item produced three "name item missing" rows
        # that read as work to do, when the right answer is that there is nothing
        # underneath. The *surname* survives redaction and is real data -- but these
        # three are `<private> Garborg`, and `Garborg` is their father's family name,
        # which `P22` already says.
        if not redacted:
            dad = father.get(g)
            name_statements, unresolved = name_lines(
                labels[g], plan, g, have.get(dad) if dad else None,
                fields=fields.get(g))
            lines.extend(name_statements)
            # Aliases: the nickname, and the full name under a married surname. Emma
            # asked for these alongside the second `P734` *family name*.
            # An alias identical to the label is noise. Now that the married name is
            # the primary label, `aliases_for`'s married-full-name alias often
            # duplicates it exactly -- `Aen "Inger Kristoffersdatter"` sitting beside
            # `Len "Inger Kristoffersdatter"`. The birth-name alias is already emitted
            # with the labels above, so this carries only what those do not.
            emitted = {qs(primary), qs(birth)}
            for alias in aliases_for(fields.get(g, {})):
                if qs(alias) and qs(alias) not in emitted:
                    lines.append(f'LAST	Aen	"{qs(alias)}"')
                    emitted.add(qs(alias))
            for note in unresolved:
                carried.append((g, label, f"name item missing: {note}"))

        lines.append("")
        created += 1

    out = ROOT / "reports" / "wikidata-garborg-day.qs"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(f"wrote {out.relative_to(ROOT)}: {created} creations, {len(seen)} links")

    cf = ROOT / "reports" / "garborg-carry-forward.tsv"
    with open(cf, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["geni_id", "label", "why"])
        w.writerows(carried)
    print(f"wrote {cf.relative_to(ROOT)}: {len(carried)} carried to a later day")
    for g, label, why in carried[:10]:
        print(f"  {g}  {label[:40]:<40} {why}")


if __name__ == "__main__":
    main()
