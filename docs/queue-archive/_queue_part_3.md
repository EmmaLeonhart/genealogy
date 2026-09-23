 test
  pins them to agree.
- `test_p2600_batches.py::test_the_daily_batch_never_restates_what_the_item_already_holds` — 97
  statements the item already holds

Some are stale committed artifacts that `pipeline.yml` fixes on recompose; the quote one and the
description one are generator defects. § *the exception is a defect: fix the generator, push, and
let the pipeline run it.*

### ⛔ WOMEN GO UNDER THEIR MAIDEN NAMES. MEN STAY UNDER THEIR MARRIED NAMES

Ruled 2026-09-21: *"we are going to switch so that women are made under their maiden names, not
under their married names, because women under their married names was a source of confusion.
Men are still under their married names."*

**This REVERSES § *The MARRIED name is the real name* for women only.** That rule said `mul`
carries the married name with the birth name as `Amul`; for a woman the two now swap — `mul` is
the maiden name, the married name becomes the alias. **Never an `Aen`**, which is unchanged.

Men are untouched, and Emma's own note on why: *"married names for men are like a bit of a weird
ass thing where whenever they have them, it usually means a name change occurred"* — so a man's
married name is evidence of an event, not a naming convention, and it stays where it is.

⛔ § *A GUARD IN ONE EMITTER IS NOT A GUARD* — there are two emitters and this belongs in
`namemodel`. And `name modelling.txt` is the authority over both this file and `CLAUDE.md`.

### ⛔ A RELATIONAL LABEL ON A PERSON WHOSE GIVEN NAME IS KNOWN — THE BIGGEST DEFECT OF THE CAMPAIGN

Ruled 2026-09-21: *"You still are producing wrong things where a person's first name is known,
but their labels that they're given are relational. That is not supposed to be happening. And
you're doing that as the biggest issue of this entire fucking campaign."* And: *"you actually
fix this critical issue that's been destroying so many items or making them useless."*

**The trigger is a person who HAS a given name.** The emitter still reaches for the relational
phrase and ships `mother of Brita Danielsdotter Berg` where it holds `Tora` and could have
written `Tora, mother of Brita Danielsdotter Berg`. § *A NAME FIELD THAT NAMES A RELATIVE IS NOT
A NAME* — a label that is only a relation names somebody else, so the item is not merely
untidy, it is **useless**: it cannot be found, and it cannot be told apart from every other
item labelled the same way.

**It is already visible in three places and they are one fault:**

- `tests/test_no_descriptions_or_summaries.py::test_no_batch_carries_a_description` fails on
  `Den` values that are relational rather than life descriptions — `"wife of Thure Johansson
  Stålarm"`, `"son of Gunnar Gunnarson Ænes"`, `"mother of Brita Danielsdotter Berg"`,
  `"daughter of Margareta Lithman"`, `"husband of Sissel Jonsdatter"`, `"born Foss"`.
- the `Tora NN` item above — `mul` missing, descriptive labels dropping the given name.
- **the corpus itself carries the same shape from Geni**, so it is arriving as well as being
  generated: 9 people in one 506-person ancestor walk are labelled `Jön abu Eric`,
  `Matt abu Anders`, `Nils abu Kierstin`, `Olof abu Malin`, `Erik abu Olof`,
  `Pärs abu Ingerborg`, `Lars abu Hanna`, `Olof abu Maria`, `Anders abu Elin` — `abu` is
  *father of*. Those have a given name in hand too.

**The fix is the branch, not a pass over the emitted items.** ⛔ § *A GUARD IN ONE EMITTER IS NOT
A GUARD* — it belongs in `namemodel`, and it needs the two tests named in the `Tora NN` item:
`mul` is `Given NN` when there is a given name and no surname, and **every descriptive label
opens with the given name**. Then fix what already went out.

#### Done 2026-09-21 — the fix, and the one thing it does NOT settle

`namemodel.own_given_name` and `namemodel.lead_with_given_name` are the model's copy of the
rule, and `describe_all` in `build-garborg-day.py` now threads `fields` and calls them. Five
tests in `tests/test_namemodel.py` pin it.

**The rule already existed in the other emitter.** `build-nn-label-batch` has emitted
`Andreas father of Malin` since 2026-09-09 and `tests/test_nn_label_batch.py` pins it;
`describe_all` never got it. That is § *A GUARD IN ONE EMITTER IS NOT A GUARD* exactly, which
is why the model holds it now.

- **⛔ SETTLED 2026-09-21: A COMMA.** `Tora, mother of Brita`. Two forms were attested and
  both were Emma's -- the bare space of 2026-09-09, pinned by `tests/test_nn_label_batch.py`,
  and the comma of the `Tora NN` item. The comma wins, the test moved with it rather than
  being left to fail, and `build-nn-label-batch` now calls the model function instead of
  formatting the prefix itself, so the two emitters cannot drift apart again.

- **⛔ SETTLED 2026-09-21: CJK TAKES THE NATIVE ORDER, NAME LAST.** `マリンの父アンドレアス`
  is *Malin's father Andreas*, which is where an apposition goes in Japanese -- the reverse of
  the European form, not a copy of it. Japanese and Chinese take no joiner, Korean takes a
  space. `namemodel._DESCRIBE_TRAILS` holds it. The name is transliterated by `describe_all`
  before it is placed, and **all three CJK labels drop when it will not transliterate**,
  because a Latin token spliced into a katakana phrase is the 2026-09-03 `ソン・オフ・`
  failure -- § *Partial is worse than absent*.

- **Still owed: fix what already went out.** The rule now stops new ones; the items already
  carrying a bare relational label are a separate pass and are not done.

---

---

## AT THE VERY END — INVESTIGATE ON FAMILYSEARCH, NOT GENI. Queued 2026-09-21

*"people I particularly want to investigate now … long story short [FamilySearch] is much better
documented than anything on geni I think. I am inclined to think that geni is really bad at
covering this area. So I will investigate on family search more … and then barrel through the
queue (that thing is at the end lol)."*

**Her own words place this last, and she is doing the investigating.** The agent's job is to
hold the two identifiers and whatever the tree already says, not to start a research campaign.

- **`Q660913` Kruto the Wend** — Prince of Wagria, `P2600` `6000000007690981645`, 13 sitelinks.
  Wagria is eastern Holstein: Wendish / Obotrite, which is the **Pomeranian side of the
  Dutch-Pomeranian cluster** § *Why the cluster campaign exists* is about.
- **FamilySearch `MBW7-P7H`** — <https://www.familysearch.org/en/tree/pedigree/portrait/MBW7-P7H>.

⛔ **AND FAMILYSEARCH DATA GOES INTO THE SYNOPTIC TREE. Ruled 2026-09-21:** *"I never ruled
that ... and yes the familysearch data is specifically meant for the synoptic tree"*, against
this file having claimed the opposite. **The claim was invented here**: the 2026-09-10 ruling
that the WIKIDATA tree never enters the synoptic tree was stretched to cover FamilySearch,
which she had never ruled on at all. § *Incomplete earlier work is not the thing being
described* — and a ruling about one source is not a ruling about another.

### The exporter: `getmyancestors`, and there is no API key

**There is no FamilySearch exporter in this repo and there never was.** Checked 2026-09-21:
`geni-extension` is `host_permissions` `*://www.geni.com/*` and `file:///*`, its eight content
scripts are Geni-specific, and FamilySearch appears in exactly two docs — as an order.life
external-id property and as a suggestion in `docs/cbdb.md`. A previous session said the
extension existed; it does not.

**`getmyancestors` 1.2.0 is the tool** — a Python CLI, `pip install getmyancestors`, installed
2026-09-21. It authenticates with the ordinary FamilySearch **account username and password**
and has a client ID compiled in, so `--client_id` only overrides it. **Run with no `-u`/`-p` it
prompts**, which is the only acceptable form: § the agent never handles a password, and
`--save-settings` / `--show-password` are never passed.

    getmyancestors -i MBW7-P7H -a 12 -d 2 -m -v       -o gedcom/familysearch/MBW7-P7H-a12-d2.ged       -l gedcom/familysearch/MBW7-P7H.log --concurrency 4 --delay 0.3

`--concurrency 4 --delay 0.3` against defaults of 10 and 0.1, deliberately: concurrency 24 is
what got Geni's WAF to answer 403 to everything.

⛔ **It pins `requests==2.32.3`** and the install downgraded the environment from 2.34.2. Other
scripts here import `requests`.

### ⛔ THE PRIMARY KEY IS THE WORK, AND THE PRECEDENT ALREADY EXISTS

`identity.GENI_ID_RE` is `^@[IFNS](\d+)@$` — **digits only** — and a FamilySearch id is
`MBW7-P7H`, alphanumeric with a hyphen. So a FamilySearch GEDCOM cannot join on the Geni
profile id, and dropping one straight into `exports/` would put an unparseable file into the
daily rebuild. It stages in `gedcom/familysearch/` until the merge can read it.

**`scripts/build-wikidata-gedcom.py` is the shape to copy.** It renders a *mergeable* GEDCOM
for a second identifier namespace already:

    a P2600 holder   @I<geni id>@    1 RFN geni:<id>     FUSES with the corpus, exact join
    everyone else    @IQ<digits>@    1 REFN Q<digits>    no Geni profile
    families         @FW<n>@                             `@F9<n>@` parsed as Geni family 91

**The `Q` and the `W` are load-bearing** — they are what stops a foreign xref parsing as a Geni
id, which is the `@NI04461@` trap that once pointed at a stranger's profile. FamilySearch needs
the same treatment and the letter must not be `Q`, `F`, `I`, `N` or `S`.

### DONE 2026-09-21 — the first export is in the corpus

    gedcom/familysearch/MBW7-P7H-a12-d2.ged                      ORIGINAL, never rewritten
    exports/familysearch/MBW7-P7H-ancestors12-descendants2.ged   the render, in the corpus

**`MBW7-P7H` is Inger Axelsdatter Güntersberg** — `Q141493478`, Geni `6000000000757999620`,
the FIRST of the two `PRIORITY_ANCESTOR_SEEDS`. So the export is the ring seed's own tree:
**3,103 individuals, 1,456 families, 1,315 sources, 6,490 notes**, with dates, places and
coordinates. 3,637 requests at 200, 84 at 429 absorbed by the retry loop, 9 at 403.

**What it emits, measured rather than guessed:** sequential integers on OUR four prefixes —
`@I1@`, `@F1@`, `@N1@`, `@S1@` — so `@I1@` parses as Geni profile 1. The identifier lives in
`_FSFTID` on 3,103 of 3,103 individuals and 1,339 of 1,456 families, and there is **no `RFN`
at all**. `scripts/render-familysearch-gedcom.py` renumbers to `@IFS/FFS/NFS/SFS<n>@`, adds
`REFN fs:<id>`, and REFUSES to write if any xref still parses as a Geni id.
`tests/test_familysearch_gedcom.py` pins it, including that the raw file *would* have leaked.

**The original is preserved untouched** — 101,511 lines against the render's 105,953, which is
exactly the 4,442 added `REFN` lines and nothing else.

⛔ **THE BRIDGE WORKS AND IS NEARLY EMPTY. 11 OF 3,103.** `scripts/bridge-familysearch-qids.py`
asked Wikidata for all 4,442 ids in batches of 250: **11 resolve through `P2889`**, and with the
ledger folded in all 11 reach a Geni id — `reports/familysearch-qid-bridge.tsv`. That is
**0.35% coverage**, so the FamilySearch tree enters the synoptic tree as a 3,103-person
component attached at eleven points. The mechanism is exact and proven end to end; the data on
Wikidata's side is simply not there. Inger herself is one of the eleven, which is the
attachment that matters most.

⛔ **AND `p2600-all.tsv` ALONE REPORTED 4, NOT 11.** The first version of the bridge read only
the master correspondence and said Inger — the person the export is rooted on — reached no Geni
id, while `garborg-qids.tsv` pairs her perfectly well. `ledger()` folds both for exactly this
reason. A join that silently under-reports by 2.75x is the shape of failure this repo keeps
being bitten by.

**SETTLED 2026-09-21, and the first reading is the one taken**: we emit `P2889` ourselves and
become the bridge. `scripts/build-familysearch-day.py` writes
`reports/wikidata-familysearch-day.txt`, a separate batch that creates every FamilySearch
person as their own item carrying `P2889`, so the next `bridge-familysearch-qids.py` run
resolves against ids we published. The duplicate against a Geni item is intended and a human
merges it. The third reading -- measure coverage across all of Wikidata first -- was refused by
§ *DO NOT MEASURE THE VOLUME BEFORE DOING A SMALL THING*.

### ⛔ OUR TREE IS ALREADY RICHER THAN WIKIDATA HERE, AND THAT IS THE POINT

Wikidata holds **no parents and no children** for `Q660913` — one spouse, an occupation, and two
CONFLICTING death dates (`1093` and `1105`, both live). Our corpus holds a whole household,
under the label **`Crito von Rügen`** rather than `Kruto the Wend`:

    father    6000000012966007622  Grimus von von Rügen        no QID
    mother    6000000059830466964  Slavina von Rügen           no QID
    spouse    6000000007705157654  Slawina von Rügen           Q111239463   already on Wikidata
    spouse    6000000175893574822  Slavka Swantiborides        no QID
    child     6000000007690998267  Littog auf Rügen            no QID
    child     6000000007705759288  Ratibor auf Rügen           no QID
    child     6000000007705521210  Burislav auf Rügen          no QID

So **six of the seven are creations, not statements** — § *A statement goes in only if BOTH ends
already have a QID*, and the batch is a SEQUENCE. Nothing here is emittable today beyond what is
already there, and that is the ordinary shape rather than a blocker.

**Two things to look at when this is worked, neither of them asserted now:**

- **`Grimus von von Rügen` carries a doubled `von`.** A label defect in our own data, not Geni's
  rendering of a name.
- **The mother is `Slavina von Rügen` and the spouse is `Slawina von Rügen`** — one letter apart.
  That is either two real women who shared a name or a confusion, and § *The question is whether
  OUR TREE MATCHES GENI* decides it is checked against Geni rather than reasoned about. ⛔ Under
  the moratorium it cannot be checked at all, so it waits. § *DO NOT PANIC ABOUT ITEMS WE GOT
  WRONG*.

---

## Follow-up (not first)

- FS ids on entry points should generate people too — implement seeding from P2889 / FS columns where Geni is empty.
