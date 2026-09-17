"""Three people's Wikidata links, as GEDCOM notes.

    python scripts/build-qid-links-gedcom.py

**A bio Wikidata link is a specific entity-resolution strategy, not a property of the tree.**
Ruled 2026-08-29: bio Wikidata links are a specific entity-resolution strategy, not something
the tree carries wholesale. The technique already exists in the other direction — a Wikidata URL
is written into a Geni About Me by hand, Geni exports it as a `NOTE`, and
`scripts/build-geni-qid-links.py` reads the QID back out. This file applies that same technique
to **three hand-identified people where the link was never written**, so the correspondence has
somewhere to live besides a scratchpad.

**It is three records. Do not let it become an architecture.** An earlier version of this
docstring said the file existed so the synoptic tree *"ALWAYS"* carried QID links, which is the
tree-wide framing that was rejected — and the code under it emitted 83,988 people. Both were
generalisations of *"When the synoptic tree is merged we change all of their bios to links to
their qids"*, where *their* meant the people named below and nobody else.

## THREE people, not the whole correspondence

**Ruled 2026-08-29:** it was supposed to be three individuals. The first version of
this script emitted every pairing in `reports/synoptic-correspondence.tsv` that landed on somebody
in our tree -- **83,988 individuals**. That was a generalisation of a specific instruction and
nobody asked for it.

The three are the residue of a retired side file: hand-made identifications that took real
effort, whose Wikidata items carry **no `P2600`**, so the pairing exists
nowhere outside that scratchpad. Checked live 2026-08-29. The rest of the file's nine pairs are
already handled and are deliberately absent here -- `Q11443857` Futohime is in `CJK_CLAN_BLOCK`,
`Q19657284` and `Q12598947` already carry their `P2600`, the two Kitajima items are in
a ban list retired on 2026-09-09, and the ninth is the account owner.

**Widening this to the full correspondence is a decision, not a default.** It is one constant
below and the filtering already works, but 84,000 links is a different act from three and wants
a ruling first.

## `exports/post-merge/`, decided when asked

`sources._post_merge_last` sorts that directory to the **end** of merge order explicitly — the
requirement was a directory whose records *"overwrite earlier ones from other repos in the synoptic
tree"*, and alphabetical order would have put `post-merge` before `samaritans` and `tanba`. So
this applies last, which is what an overlay wants.

Being under `exports/` makes it corpus: `sources.find_exports` globs the directory, so the three
links reach the tree without anything having to be run afterwards. That is the right trade at
three records; it is the reason the count matters and the reason widening it is a decision rather
than a default.

## Why it merges rather than duplicating

Records are keyed on the xref, which is the Geni profile id — `CLAUDE.md`'s primary key. So
`0 @I6000000001846508982@ INDI` here is **the same record** as that person in every other export,
and its `NOTE` joins theirs. `merge.ALWAYS_REPEATABLE` holds `NOTE`, so nothing is overwritten:
repeatable paths with a value are matched on that value, an identical line collapses, a different
one is kept alongside. Re-generating and re-merging is therefore idempotent.

## The source is the hand identifications, and the first attempt got that wrong too

Reading `reports/synoptic-correspondence.tsv` and filtering it to the three returned **0 of 3** —
which is not a bug, it is the point restated. That report joins five places a pairing can live
and that side file was not one of them, so these three are invisible to it. They exist in
a hand scratchpad and nowhere else, which is exactly why writing them into the tree is worth
doing.

The pairs are inlined below, because the parser that read them and the file it read are both
file parses with zero unparsed entries.

## Every record must already exist in the tree

An `INDI` whose xref the merge has not seen is a **new person**, so an unfiltered emit would mint
people rather than annotate them. Checked against `reports/derived-labels.csv`, one row per person
in the merged tree, and an id that fails the check is printed as a finding rather than skipped
quietly.
"""
from __future__ import annotations

import collections
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


sys.stdout.reconfigure(encoding="utf-8")
csv.field_size_limit(1 << 30)

IN_TREE = ROOT / "reports" / "derived-labels.csv"
#: The adjudicated hand identifications. Every row is a positive verdict; see `main`.
HAND = ROOT / "reports" / "manual-identifications.csv"
OUT = ROOT / "exports" / "post-merge" / "wikidata-qid-links.ged"

#: The three, by Geni id. Named explicitly rather than derived: they are the ones whose Wikidata
#: item carries no `P2600`, and that is a live fact about Wikidata which will stop being true the
#: moment these links are acted on -- so a rule that recomputed it would empty this file and look
#: like success. An explicit list says what was decided and when.
#: **The pairs themselves, since the side file is gone.** It was deleted in `12f3134a`
#: and the deletion was right -- `CLAUDE.md` § *LEGACY CODE IS DELETED* -- but this script kept
#: reading it and had no guard, so it crashed with `FileNotFoundError` and stayed crashed through
#: four dead-item sweeps.
#:
#: **The correspondence is not a substitute: 0 of these 3 are in
#: `reports/synoptic-correspondence.tsv`.** Checked rather than assumed. They were made by hand,
#: from identifications that took real effort, and no
#: automated source reaches them -- which is exactly why they were in a hand-written file.
#:
#: So they live here as a constant, which is what `queue.md` already says: *"widening this beyond
#: the three is a decision and is one constant."*
PAIRS = {
    "6000000001835522164": "Q11596350",   # 稚武彦命 Wakatakehiko
    "6000000001844033355": "Q11078587",   # 播磨稲日大郎姫 Harima no Inabi, his daughter
    "6000000002039751362": "Q24890131",   # 物部伊莒弗 Mononobe no Ikofutsu

    # **Empress Jingū, added 2026-09-01 by instruction:** she goes in the identifications
    # GEDCOM so that Jingū is linked on Geni and Wikidata in future.
    #
    # `Q232803` is 神功皇后 — 38 sitelinks, no `P2600`, so nothing joins her by id and the
    # zipper cannot reach her either. **Geni holds two profiles for her**, which is the
    # ordinary unmergeable-duplicate case `CLAUDE.md` records, so both are linked to the one
    # item rather than one being picked.
    "6000000001846508982": "Q232803",   # 神功皇后 Jingū-kōgō (Okinagatarashi-hime)
    "6000000045545840003": "Q232803",   # the same person, Geni's second profile

    # **The eccentric clusters, added 2026-09-05 by instruction:** *"write these ones into
    # that identification gedcom thing that serves the dual purpose of entity resolution through
    # adding dummy bios with the wikidata links, which is scheduled to at Jan 1, 2027 become a
    # thing that turns every qid there into an entry point for editing"*.
    #
    # This is the widening the docstring above reserves for a ruling, and it is bounded: these
    # are the pairs that survived `reports/eccentric-cluster-candidates.tsv`, not a rule. Every
    # one was read by hand against the item's own label, description, `P31` and dates, which is
    # § *How this project works now* -- records, then a decision.
    #
    # **Not one of them carries a `P2600`**, which is why the pairing exists nowhere else: the
    # clusters they come from read `p2600_linked = 0` in `reports/eccentric-clusters.md`, and
    # that is what was corrected: pre-dynastic Egypt definitely does have items. It does;
    # nobody had linked them.

    # -- Cluster 3, PRE-DYNASTIC AND EARLY DYNASTIC EGYPT, 295 people at 100-129 hops.
    "6000000209058145828": "Q318613",   # Scorpion I -- predynastic Egypt pharaoh
    "6000000006743335611": "Q255585",   # Neithhotep -- Neithotep, ancient Egyptian queen consort
    "6000000004869093655": "Q152375",   # Djer -- ancient Egyptian pharaoh of the First Dynasty
    "6000000004869093676": "Q230548",   # Meryt-Neith -- Merneith, ancient Egyptian queen
    "6000000004869093649": "Q453789",   # Khenthap -- ancient Egyptian queen consort
    "6000000004869093727": "Q453508",   # Betrest -- ancient Egyptian queen consort
    "6000000004869093733": "Q151819",   # Qa'a -- Egyptian ruler
    "6000000005747697181": "Q151805",   # Semerkhet -- Egyptian pharaoh
    "6000000005747697123": "Q1962794",  # Nakhtneith -- ancient Egyptian queen of the 1st Dynasty
    "6000000006743369482": "Q453243",   # Herneith -- ancient Egyptian queen consort
    "6000000005747697154": "Q2342780",  # Serethor -- Queen of Egypt
    "6000000015211291801": "Q15639426", # Shesh I -- ancient Egyptian pharaoh
    "6000000004869093838": "Q464248",   # Neferkasokar -- seventh pharaoh of the second dynasty
    "6000000016659670347": "Q310878",   # Seth-Peribsen -- ancient Egyptian ruler
    # `Nebre` against `Nebra` is the one label mismatch kept: the description settles it, being
    # *"Horus name of the second early Egyptian king"*, which is this person's position exactly.
    "6000000005747697264": "Q152751",   # Nebre -- Nebra

    # -- Cluster 15, SIXTH DYNASTY, 10 people at 100-107 hops.
    "6000000004869097266": "Q320908",   # Merenre Nemtyemsaf II -- Egyptian pharaoh
    "6000000016328513720": "Q4766049",  # Ankhesenpepi III -- Egyptian queen, Sixth Dynasty
    "6000000016328494813": "Q489064",   # Ankhesenpepi IV -- Anchenespepi IV., Sixth Dynasty
    "6000000016662722475": "Q1052959",  # Nefer -- Egyptian pharaoh of the 6th Dynasty

    # -- Cluster 12, THIRD INTERMEDIATE PERIOD, 17 people at 100-107 hops. **These four agree on
    # the DEATH YEAR EXACTLY** -- Osorkon I -889, Takelot I -874, Shoshenq I -924 -- which is
    # the `date` step `reports/zipper-reliability.md` measures at 0.0% disagreement.
    "6000000042325392108": "Q311811",   # Scheschonq I -- Shoshenq I, Pharaoh of Egypt
    "6000000042325255325": "Q515574",   # Osorkon I -- Egyptian pharaoh, c. 925-890 BC
    "6000000042325032728": "Q548623",   # Takelot I -- Egyptian pharaoh
    "6000000042324946693": "Q459153",   # Osorkon II -- Egyptian pharaoh

    # -- Cluster 6, THE AXUMITE ROPE, 61 people at 100-153 hops. **Only one pair, and the
    # `instance of` filter would have thrown it away**: `Q159888` is `P31` `Q20643955` *human
    # biblical figure*, not `Q5` *human*, so `instance_of_human` reads `no` on a correct pair.
    # Recorded because it is a general hole -- a legendary or biblical person is routinely not
    # `Q5`, and every cluster out here is exactly that population. Our -1013 against the item's
    # -1000 is what actually settles her.
    "6000000210521076830": "Q159888",   # Makeda Queen of Sheba -- Queen of Sheba

    # -- THE SELJUQ PAIR, given by Emma 2026-09-09 with both links in her own message. They are
    # the two sons of `n n` `6000000035218690155`, the Seljuq matriarch whose line she has been
    # building westward -- *"this is the line from China to Europe that I wanted to get here and
    # was not sure if it was actually around"*.
    #
    # They belong here rather than in `reports/manual-identifications.csv`, which
    # `CLAUDE.md` § *"MANUAL ENTITY RESOLUTION" IS A MISLEADING NAME* says is the manual
    # PARENTAL ZIPPER MERGE correspondences and warns will be abused by *"a later agent [who]
    # will put anything hand-checked into it -- a Samaritan pair, a bio link, a spine anchor"*.
    # A pair of 11th-century sultans is precisely that abuse.
    #
    # And they fit this file's own category exactly: § *WHAT `wikidata-qid-links.ged` IS FOR*
    # is *"far off genealogical people who are too far away in the regular clusters to be ones
    # to start with"*, expanded to take people who already hold a proper QID. Both do.
    "6000000031527612551": "Q144565",   # Sultan Tughril I -- Tughril, first Seljuq sultan
    "6000000031528142916": "Q870223",   # Dawud Chaghri Bey, Lord of Khorasan -- Chaghri Beg
    # **Their FATHER, given by Emma 2026-09-16** with both links in her own message:
    # `Q6040326` *Mikail of Kinik tribe*, `P40` child = `Q870223` and `Q144565`, the two above.
    # No `P2600`, so the pairing lives nowhere else -- this file's own category exactly.
    "6000000031528058919": "Q6040326",   # Mika'il Seljuq -- Mikail of Kinik tribe

    # ⛔ **THE 39 HAND IDENTIFICATIONS, 2026-09-15 — AND THEY ARE NOT BLOCKED.** Ruled that day,
    # correcting the previous session exactly: *"The identification one goes into the gedcom it
    # isn't blocked but they are added to the entry ponys and universe and p2600 can be added
    # there at Jan 1 no blocking lol"*.
    #
    # The session before had read *"I do not want to draw more attention than I've been getting
    # from being non-local"* as a reason to DROP every line naming one of them, and added a
    # 39-QID tuple to `build-garborg-day.py` that filtered the finished batch. That inverted the
    # design. **Being far from the universe is what this file is for** — its own § *WHAT
    # `wikidata-qid-links.ged` IS FOR* is *"far off genealogical people who are too far away in
    # the regular clusters to be ones to start with"* — and the answer to non-locality here has
    # never been a ban, it is the DATE. `special-geni-gedcom-recognition` carries
    # `active_from 2027-01-01`, so a pair written here is inert until then and becomes an entry
    # point on the day, which is the mechanism Emma specified on 2026-09-05: *"write these ones
    # into that identification gedcom thing ... which is scheduled to at Jan 1, 2027 become a
    # thing that turns every qid there into an entry point for editing"*.
    #
    # So the identification is recorded, the tree knows who is who and `to_create` cannot mint a
    # duplicate, the QIDs join the universe on 2027-01-01, and **`P2600` can be added to them
    # then** — none of which a block permits. A blocked pairing is one that expires into nothing.
    #
    # 38 pairs, not 39: `Q236972` Fuxi was in that tuple with no Geni id recorded against it, and
    # it is already in the ledger (`reports/garborg-carry-forward.tsv` holds a `P3373` for it), so
    # it needs no row here and simply stops being excluded.
    "6000000001381114215": "Q10299225",   # Jing Kang 敬康 5
    "6000000001272831610": "Q10438384",   # Yu Gu Sou 瞽叟 8
    "6000000003474166572": "Q1045160",   # Qì 契 5
    "6000000007213183226": "Q10514592",   # Jiáo Jí 蟜極 3
    "6000000001381046535": "Q10752092",   # Qióng Chán 穷蝉 4
    "6000000008004418918": "Q10933357",   # Dà Yè 大业 5
    "6000000002481254239": "Q1147250",   # Xuán Xiāo 玄囂 Shǎo Hào 少昊 2
    "6000000008659107006": "Q128371",   # Caliph Marwan II bin Muhammad
    "6000000002048439278": "Q1441379",   # Léi Zǔ 嫘祖
    "6000000188494434823": "Q18028984",   # Reformatorin Ursula von Münsterberg
    "6000000001381123265": "Q198180",   # Zhuān Xū 顓頊 3世 DO NOT MERGE PARENTS
    "5152366561060066977": "Q2746812",   # Umayya bin Abd Shams
    "6000000002848066261": "Q28409803",   # Tóng Yú Shì Wife 3 彤魚氏
    "6000000001381274001": "Q29201",   # Yellow Emperor
    "6000000130192002822": "Q313336",   # Shén Nóng 神农 Yán Dì 炎帝 Yú Quān 榆圈 一任帝 2世
    "6000000195149451825": "Q313342",   # Emperor Shùn 帝舜 9 1G
    "6000000009562419205": "Q314809",   # Iry Hor Pharaoh of Egypt
    # ⛔ `Q318613` Scorpion I is NOT repeated here. He was already a Cluster 3 pair above, from
    # the 2026-09-05 eccentric-cluster reading, with this same Geni id -- and the 2026-09-15
    # identification block restated him, giving this dict a DUPLICATE KEY. Python keeps the last
    # silently: no error, no warning, and every count of this file was one too high. Found by
    # auditing for exactly the fault Emma named -- *"you did not figure out that the Chinese
    # tails were duplicates"*.
    "6000000028714712399": "Q334111",   # 조선 27대 순종 척
    "6000000008004518685": "Q4243879",   # Bó Yì 字 伯益 8
    "6000000020107122663": "Q4268330",   # Jī Nǚ Xīu姬女修 4
    "6000000026522778851": "Q4302144",   # GŌNGSŪN Shǎo Diǎn 少典 1世
    "6000000001272854603": "Q4499078",   # Gui Xiang 媯象 9
    "6000000028856413461": "Q484866",   # Yi Un Crown Prince of Korea
    "6000000028895625641": "Q496421",   # private
    "6000000001381063554": "Q6377648",   # Chāng Yì 昌意 2
    # **`Q70899` Adam carries a SECOND Geni id and that is DELIBERATE.** Ruled 2026-09-15, after
    # this was written up as a discrepancy: *"biblical figures have intentionally duplicated Geni
    # IDs because Geni ... just disconnects them. So people just had to periodically make new
    # ones."* The item holds `6000000003538706117`; this is a different profile for the same man,
    # added on purpose.
    #
    # So § *A second Geni ID on one item is NOT a conflict* applies here exactly as it does to
    # `Q9738` below, and the earlier reading of this as a MISMATCH was wrong. A biblical or
    # legendary figure accumulating profiles is the normal state of that corner of Geni, not a
    # defect to reconcile.
    "6000000201847373856": "Q70899",   # Adam the First Man
    "6000000028786845951": "Q7214248",   # 순헌황귀비 엄씨
    "6000000002481253260": "Q721756",   # Emperor Kù 帝嚳 4
    "6000000189960169823": "Q7480137",   # Nǚ Yīng 女英
    "6000000001380983518": "Q7664534",   # Jiao Niu 蟜牛 7
    "6000000001272026560": "Q7878975",   # Wò Dēng 握登
    "6000000189960074826": "Q7991612",   # É Huáng 娥皇
    "6000000003485847175": "Q819556",   # Emperor Yáo 帝堯 5
    "6000000023167303575": "Q8262857",   # Mó Mǔ Wife 4 嫫母
    "6000000195149174838": "Q9511624",   # Huaxu
    "6000000001380828716": "Q9569181",   # Ju Mang 句芒 6
    # **`Q9738` Wu Zetian also carries a different `P2600` on Wikidata -- `6000000074771352821`
    # -- and here OURS is the better one.** Checked 2026-09-15: this profile is in the merged
    # tree with a father, a mother, five children and three spouses, labelled 曌 武; Wikidata's
    # is in the corpus nowhere. Two Geni profiles for one person is the ordinary unmergeable
    # duplicate, and § *A second Geni ID on one item is NOT a conflict* applies squarely -- it
    # is self-healing and is not to be reported or fixed.
    "6000000002188099903": "Q9738",   # Wu Zhao 武曌 Zetian Emperor
}
ONLY = set(PAIRS)

LINK = "https://www.wikidata.org/wiki/{qid}"


def main():
    in_tree = set()
    with IN_TREE.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            if row.get("geni_id"):
                in_tree.add(row["geni_id"].strip())
    print(f"{len(in_tree):,} people in the merged tree")

    pairs = collections.defaultdict(set)
    for geni_id, qid in PAIRS.items():
        pairs[geni_id].add(qid)
    print(f"{len(pairs)} pairs, from the constant in this file")

    # ⛔ **THE HAND IDENTIFICATIONS BELONG HERE, AND THEY WERE LIVING SOMEWHERE ELSE.** Ruled
    # 2026-09-17: *"they are stored in a GEDCOM. If they are stored in some sort of other
    # format, that means that you were storing them in this separate location because they only
    # belong in a GEDCOM, which I'm pretty sure is significantly larger than 68 pairs. And that
    # GEDCOM primarily functions through adding the things into the universe as entry points."*
    #
    # That is the widening `queue.md` reserved as a decision -- *"widening this beyond the three
    # is a decision and is one constant"* -- and it has now been decided. It is not the 83,988
    # of the refuted first attempt and not the whole correspondence: it is
    # `reports/manual-identifications.csv`, the adjudicated file, every row of which is a
    # positive verdict somebody reached by hand.
    #
    # Measured the day it was ruled: **1,653 rows, 1,636 `SAME` and 17 `RIGHT`, and 0 of them
    # were in this file.** The store that is supposed to hold the correspondence held 65 records
    # and none of the 1,653. That is the whole complaint and this line is the whole fix.
    #
    # The CSV stays where it is, because `verdict`, `batch`, `date` and `note` are provenance
    # about how each pairing was reached and a GEDCOM `NOTE` cannot carry them. It is the
    # LEDGER of the adjudication; this is the STORE the tree reads. What it is emphatically not
    # any more is a source of `P2600` -- `wikidata-edit-run._refuse_hand_identifications` and
    # `build-garborg-day.manual_p2600_lines` both refuse that outright, and the entry points
    # arrive on 2027-01-01 through this file instead.
    hand = 0
    if HAND.exists():
        with HAND.open(encoding="utf-8", newline="") as fh:
            for row in csv.DictReader(fh):
                q = (row.get("qid") or "").strip()
                g = (row.get("geni_id") or "").strip()
                if q.startswith("Q") and g.isdigit():
                    pairs[g].add(q)
                    hand += 1
    print(f"{hand:,} hand identifications from {HAND.name}")
    print(f"{len(pairs):,} distinct people once both sources are joined")

    absent = sorted(g for g in pairs if g not in in_tree)
    if absent:
        # Never silently: emitting one of these would CREATE the person rather than annotate
        # them, which is the failure the tree filter exists to stop.
        print(f"REFUSING -- not in the merged tree, would be minted as new people: {absent}")
        for g in absent:
            pairs.pop(g)
    for g in sorted(ONLY - set(pairs)):
        print(f"not emitted: {g}")

    multi = sum(1 for qs in pairs.values() if len(qs) > 1)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8", newline="\n") as out:
        # A minimal but valid 5.5.1 header. `SOUR` names this script so the file is
        # traceable to what made it rather than looking like a Geni download.
        out.write("0 HEAD\n")
        out.write("1 SOUR genimerge\n")
        out.write("2 NAME scripts/build-qid-links-gedcom.py\n")
        out.write("1 GEDC\n")
        out.write("2 VERS 5.5.1\n")
        out.write("2 FORM LINEAGE-LINKED\n")
        out.write("1 CHAR UTF-8\n")
        written = 0
        for geni_id in sorted(pairs):
            out.write(f"0 @I{geni_id}@ INDI\n")
            for qid in sorted(pairs[geni_id]):
                out.write(f"1 NOTE {LINK.format(qid=qid)}\n")
                written += 1
        out.write("0 TRLR\n")

    print(f"{written:,} NOTE links over {len(pairs):,} individuals")
    print(f"{multi:,} people carry more than one QID; each gets one NOTE per QID")
    print(f"wrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
