# Generating CJK names from the name items on the PARTS of a `mul` label

Emma's plan, recorded 2026-09-14 and investigated 2026-09-15 under `queue.md` § *Generate CJK
names from the CJK labels on PARTS of the `mul` label*: *"I had a plan to generate cjk names from
cjk labels on parts of the mul label."* It is the second half of a ruling whose first half is
already built — *"Given names and surnames should have our standardized cjk-izations attached to
them. **imo they should even be the source of it in the logic.**"*

**The first half is done.** `build-garborg-name-items.py` gives every newly created name item
`Lja`/`Lzh`/`Lko`, and `build-name-item-cjk.py` backfills the ones that existed first.

**The second half — making those items the SOURCE a person's CJK label is composed from — is not
built, and this page is the investigation the queue item asks for.**

## How it would work

A person's `mul` label is `Anna Olsdatter Atletveit`. Its parts are `Anna`, `Olsdatter`,
`Atletveit`; each part is a name item (`P735` given, `P734` family, `P5056` patronymic) and each
item carries `ja`/`zh`/`ko`. Compose the person's CJK label from the parts' readings instead of
transliterating the whole string token by token, which is what `label_in` does today.

The gain is consistency: every `Anna` in the tree gets one decided reading rather than whatever
the token table happened to produce, and a correction to the item propagates to everyone bearing
the name.

## Coverage today — measured, and the answer is that the plan is EARLY, not blocked

Over the 3,526 ledger people who carry a `mul` label, by token occurrence:

| share | state | examples |
| ---: | --- | --- |
| **8%** | item exists **with all three readings** — composable now | `Samuel`, `Karl`, `Fredrik`, `Andreas` |
| **55%** | **item exists, readings MISSING** | `Anna`, `Gustaf`, `Ingegerd`, `Fleming` |
| **32%** | **no name item at all** | `Passionei`, `Svantepolksdotter`, `baroness`, `(Rollo),` |
| **4%** | particle — never a name item | `de`, `von`, `af`, `van` |

**Only 9 of 3,526 people could have their whole label composed today.** But **55% of the gap is
readings missing from items that already exist**, and `build-name-item-cjk.py` is the script that
adds exactly those — 8,006 items in its scope, 7,516 missing at least one reading. Coverage rises
on its own as that runs. The plan is waiting on a pipeline that is already wired, not on a
decision.

## ⛔ THE COST OF A MISSING NAME OBJECT, MEASURED AT LAST

`queue.md` records that this plan is *the* reason not creating a name object could be costly, and
that the reason had to be understood rather than felt. It is the **32%**: a part with no name item
generates no reading, and since **partial is worse than absent** — `label_in` returns
`(None, None, None)` if any token is unknown — one missing part costs the whole person's CJK
label, not a third of it.

That is the specific cost, and it does not reopen anything. The 32% is mostly junk that should
never have an item (`baroness`, `(Rollo),`, `of`) plus genuinely rare surnames. *"There's
effectively zero cost for not creating a name object"* stays true of the junk; the cost lands on
the real names among them.

## ⛔ THE BLOCKER, AND IT IS NOT COVERAGE: A NAME ITEM'S READING IS NOT NECESSARILY OURS

Wikidata holds 823,907 name items written by everyone. Over the 889 token occurrences that
**do** have a full name-item reading today, against what `label_in` produces:

    agree                              684
    DISAGREE                           200
    our transliterator has nothing       5

**And on the disagreements ours is usually the better one**, which is the opposite of what
*"they should even be the source"* assumes:

| token | name item says | we say | |
| --- | --- | --- | --- |
| `Øystein` | パスクアーレ | オイスタイン | **the item says *Pasquale*** — a different name entirely |
| `Ingrid` | インフリット | イングリッド | the item's is garbled; its `ko` 잉리 is truncated too |
| `Fredrik` | フリエドリック | フレドリク | `Q4926491`; **`Q83349948` is a second `Fredrik` item reading フレドリック** |
| `Ingeborg` | インゲボルク | インゲボルグ | final voicing; ours is standard |

`Q317315` is the clearest: its `mul` and `en` are `Øystein`, its `zh` 奥伊斯坦 and `ko` 외위스테인
are correct, and its `ja` is the Italian name *Pasquale*. Composing from that item would put
somebody else's error into every Norwegian `Øystein` in the tree at once — the blast radius is the
whole point of composing from shared parts, and it runs both ways.

**`Fredrik` having two items is the second failure**: which reading you get depends on which item
the join lands on, and nothing about the token decides that.

## The proposal

**Trust a name item's reading only where WE emitted it.** That is not a new rule — it is exactly
what `build-garborg-day.cjk_slots_we_have_emitted()` already does for a person's own label, where
*"the CJK overwrite is allowed only where the label being overwritten is one this pipeline
emitted"*. The same test, one level down:

    for each token in the mul label:
        1. a name item we created or backfilled  -> its ja/zh/ko IS the reading
        2. a particle                            -> the fixed particle table (von -> フォン)
        3. anything else                         -> transliterate_token, as today
        if any token yields nothing              -> emit no CJK label at all

Step 1 reads `reports/created-name-items.tsv` and whatever `build-name-item-cjk.py` records, not
`reports/name-item-languages.csv` wholesale — the difference between the two is `Øystein`.

**It does not change a single label until step 1 has members**, which makes it safe to wire before
it is useful: today it would fall through to step 3 for almost everything and emit what it emits
now. That is the right order — the composition path lands first and inert, and coverage arrives as
`build-name-item-cjk.py` fills our own items.

**Particles need their own table and will never have name items** — `namemodel.PARTICLES` is
consulted before the refusal lists precisely because a particle is not a name, so `von`, `de`,
`af` and `van` must be rendered from a small fixed map or the composition fails on 4% of tokens
for a reason that has nothing to do with names.

## What is NOT proposed

**Backfilling readings onto name items we did not make.** 699,287 of the 823,907 carry no CJK at
all, and writing into them is the non-locality failure `build-name-item-cjk.py`'s own docstring
refuses: *"having stuff that leaks out from the universe and into just random areas ... is an
intrinsic risk."*

**Correcting `Q317315`.** It is a real error on a real item, and it is outside the universe. It is
recorded here and nowhere else.
