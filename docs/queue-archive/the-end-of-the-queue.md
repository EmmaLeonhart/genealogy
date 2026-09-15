## THE END OF THE QUEUE

- **⛔ AN ANALYSIS OF THE FIVE ARTEFACTS SENT 2026-09-10.** *"Things to think about. But put at the
  end of the queue an analysis of these"* — so this is the roster and **nothing here is
  investigated, measured, fetched or queried.** `CLAUDE.md` § *"Add it to the end of the queue"
  means WRITE IT DOWN AND STOP*. When it is reached, § *"Analyse this" means: build a CSV of every
  instance* governs the shape of the answer.

  **1. The `daughters` paste** — <https://pastebin.com/wP2dbrVf>, guest paste, **11.13 KB**,
  posted **2026-09-10**, **365-day retention** so it expires 2027-09-10. One Wikidata item URL per
  line. The fifteen legible on screen:

      Q108655747  Q106472244  Q106535162  Q106472816  Q106683636
      Q106540429  Q109927895  Q108779632  Q108655970  Q108891795
      Q22694450   Q106240452  Q107239466  Q110573431  Q106240606

  and two more partly visible below the fold, `Q106713074` and `Q75381643`. At ~46 bytes a line
  the file is on the order of **240 items**; that is arithmetic off the byte count, not a count.

  **2. `Q106583062` — "Daughter of Ito Nyudo"**, `mul` / `en` / `en-ca` / `en-us` / `fr` all
  carrying that same string, no description in any language, `instance of` human,
  `sex or gender` female with 1 reference.

  **3. `Q116054588` — "NN ferch Iorwerth ab Owain Brogyntyn"**, the same string in all five
  language slots, no description, human, female.

  **4. `Q76006546` — "unknown son (?)"**, and this one disagrees with itself:

      mul      NN                    en-ca   unknown son (?)
      en       unknown son (?)       en-us   NN
                                     fr      NN

  Its **English description is `Peerage person ID=462780`** — an identifier used as a description.

  **5. `Q141381269` — label `..`**, in every language slot, `instance of` **family name**, English
  description `family name`. **Created by `日巫女` via QuickStatements**, revision 04:27
  2026-09-09, edit summary `#quickstatements; #temporary_batch_1788927746966`.

  **What connects them is not stated and is not to be assumed here.** Four of the five are
  unnamed or relationally-named people — *Daughter of X*, *NN ferch Y*, *unknown son (?)* — and
  the fifth is a name item whose label is two full stops. Whether the paste is a list of the same
  shape is exactly the thing the analysis has to establish rather than take as read.

- **⛔ WELSH PATRONYMIC CHAINS TAKE `P1545` (series ordinal).** Ruled 2026-09-10: *"For people
  like this (mostly welsh on wikidata) we use series ordinal for patronymics."*

  **The instance sent** is `Q116812067` **Margred ferch Llywelyn Gôch ab Ieuan ap Dafydd of
  Rhydlafar** — one label carrying a chain of three generations, `ferch Llywelyn` / `ab Ieuan` /
  `ap Dafydd`. No description in any language; `instance of` human, 0 references. The other tabs
  open beside it were `Lewys ap Robert Raglan, of Vorc…`, `John Games, of Penfathrin`, so the
  shape is a population rather than one person.

  **Why the ordinal is the answer and not a second property:** a Welsh name names the father, the
  grandfather and the great-grandfather in one string, so `P5056` (patronymic) has **several
  values on one person** and nothing about the statement says which generation each belongs to.
  `P1545` (series ordinal) is the qualifier that orders them.

  `name modelling.txt` is the authority on how a name is modelled and beats `CLAUDE.md`, so this
  rule belongs there once it is worked — `CLAUDE.md` § *`name modelling.txt` is the authority*.
  It is recorded here first because that is where it was sent.

  **Nothing is investigated, measured or queried**: not how many Welsh-chain labels exist, not
  which already carry `P5056` (patronymic), not whether `P144` (based on) points anywhere.
  `CLAUDE.md` § *"Add it to the end of the queue" means WRITE IT DOWN AND STOP*.

- **⛔ ANALYSE THE NINE SCREENSHOTS SENT 2026-09-11 AND THE ISSUES IN THEM.**
  `docs/queued-analysis/wikidata-reverts-2026-09-11/` — nine images, saved as sent:

      01-pastebin-contributions.jpg          pastebin.com/uXm3P4yA, a contributions listing
      02-Q3656094-Sempronia.jpg
      03-Q176912-Philip.jpg
      04-Q359687-Antigonus-II-Mattathias.jpg
      05-Q313883-Alexandros-II-of-Macedon.jpg
      06-Q1427539-Flavius-Hannibalianus.jpg
      07-Q125542470-Joel-von-Brehmer.jpg
      08-Q113006331-Johan-Leijel.jpg
      09-Q64802-Engelbert-II-of-Berg.jpg

  **The task emerges from the images; read them and work it out there.** Emma: *"add to the very
  end of the queue a task to analyze these images and issues I have with them, just save into a
  directory for this the task emerges from the images when you look at them do not ask questions
  or think about them carry on with your work"*.

  **⛔ NOT INVESTIGATED, NOT DIAGNOSED, NOT ACTED ON — and deliberately not summarised here
  either.** The instruction was to save them and carry on, so no reading of what they show has
  been written down: no account of who reverted what, no cause, no count, and above all **no
  change to any batch or emitter on the strength of them.** `CLAUDE.md` § *"Add it to the end of
  the queue" means WRITE IT DOWN AND STOP* and § *A LONG-HORIZON INSTRUCTION IS NOT ANSWERED FROM
  THE FIRST SLICE*.

  When this is worked: the answer is a CSV of every instance, committed, and then the analysis of
  that CSV — `CLAUDE.md` § *"Analyse this" means: build a CSV of every instance, commit it, then
  analyse that* — not a reading of nine screenshots. The screenshots are where the question comes
  from, not the evidence base.

- **⛔ FIX THE GENI-ID APPLICATION: IT IS SUPPOSED TO FIRE ONLY ON THE BORDER, AND IT FIRES
  EVERYWHERE.** Emma, 2026-09-11: *"fix our geni id application stuff, because it is only
  supposed to add geni ids to people bordering the universe when a relationship is added to them,
  right now it kinda just does it everywhere not in accordance with the algorithm"*.

  So the rule it is meant to obey has two conditions and it is honouring neither:

      the person is BORDERING THE UNIVERSE
      a RELATIONSHIP IS BEING ADDED to them

  **Nothing is investigated, measured, grepped or diagnosed.** Which emitter does it, whether
  `docs/algorithms.md` states the border condition, how many statements went out that should not
  have — none of that is looked at here, and no batch or emitter is touched on the strength of
  it. `CLAUDE.md` § *"Add it to the end of the queue" means WRITE IT DOWN AND STOP*.

- **⛔ WHY ARE `|` NAME CORRECTIONS LANDING ON NON-ADJACENT ITEMS?** Emma, 2026-09-11: *"look
  over why name corrections with the | appear to be being done to non-adjacent items"*.

  **Not investigated, not diagnosed, not traced to an emitter.** Which script writes the `|`
  form, what "adjacent" is measured against, and how many such corrections went out are all
  unexamined here. `CLAUDE.md` § *"Add it to the end of the queue" means WRITE IT DOWN AND STOP*.

- **⛔ ONLY EVER EDIT THINGS IN THE UNIVERSE OR ONE STEP ADJACENT TO IT.** Emma, 2026-09-11:
  *"making it so that we only ever edit things in the universe or one adjacent to it. We are
  being way too non-local and it is drawing attention"*.

  So the edit surface is bounded to two rings and nothing further:

      in the universe
      one step adjacent to it

  **And the reason is OPSEC, not correctness** — *"it is drawing attention"* — which is the same
  concern behind the caps in § *Caps* and behind the QuickStatements batching generally.

  **⛔ AND THE FUXI CASE IS THIS RULE'S FIRST MEASURED COST, 2026-09-14.** A Chinese
  mythological figure, `Q236972`, nowhere near the universe, got a phonetic katakana label
  written over its correct 伏羲 — because a batch reached him at all. Emma: *"the core of this
  really is based upon something later in the queue related to how the quickstatements that are
  generated are supposed to be local, but they're not local... the Scandinavian areas are places
  where we really have a good idea of what good data looks like and what the edge cases are, but
  stuff that leaks out of the universe into just random areas is an intrinsic risk."*

  That is the diagnosis and it outranks the symptom. The transliteration bug is real — the guard
  for it went in the same day — but **a correct transliterator pointed at Chinese mythology is
  still the wrong pipeline aimed at the wrong people.** Locality is what would have prevented it,
  and it is a stronger fix than any amount of per-script special-casing.

  **Nothing is investigated, measured or changed.** No emitter is audited, no locality test is
  written, and no batch is altered on the strength of this. It is written down where it was sent.

- **⛔ `Q1934051` — THE ONE OTHER IDENTIFICATION SHAPED LIKE THE WRONG ONE.**
  `NN Sverkerska Kungaätten` `6000000031940461725` identified with **Helena of Sweden**.

  `Q22678387` `NN de Courtenay` -> `Hodierne of Courtenay` was ruled wrong by Emma on 2026-09-11
  and is retracted. `reports/nn-manual-identifications.csv` holds all 11 identifications with
  `NN` on our side; nine are `NN` ↔ `NN` matched on family, and this is the **only** other one
  where an unnamed person on our side was matched to a **named** individual on Wikidata.

  **It is hers to rule on and is NOT retracted on a resemblance.** Written down, not acted on.
