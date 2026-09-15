## ALWAYS LAST — the tail

- **⛔ RUN THE EXTENSION'S EXPORTS ON EVERY PENDING PERSON. THIS IS TAIL WORK, AFTER EVERYTHING
  ELSE.** Emma, 2026-09-09: *"you run browser extension exports on all the pending people you
  cunt at the end after other tasks are completed, this is an actual tail thing."*

  The extension already decides this itself: a person who misses both searches and clears the
  **250** floor on any statistic gets `state: miss_export_warranted`, and with `job.create` set
  it walks up, creates one ancestor and runs a `Forest` export from them. `individual.js` owns
  every part of that; there is no discretion here and none is wanted.

  ⛔ **AND THE POINT OF ALL OF IT IS THE WIKIDATA ISOLATES.** Emma, same message: *"The wikidata
  isolates the entire point of the extension with its workflow."* So the collector over
  `collector-worklist.tsv` is the WORK and these exports are what falls out of it — never the
  other way round. An export campaign that crowds out the isolate captures has inverted the
  thing.

  **Scale, so nobody starts it lightly:** 2,587 outstanding on the worklist today. Geni runs one
  export at a time and that is its limit, not a setting.

- **⛔ EXPORT FROM THESE SIX FIRST — found in Abul Hamza's ball, 2026-09-10.** They cleared the
  descendants threshold on a random pick and each one is an individual export to run **before**
  the general descendants-of-Abul-Hamza process below.

      6000000008384075400  Sayaluna ata                15,000   (Geni's display ceiling)
      6000000000746523797  Hélène de Corday            15,000   (ceiling)
      6000000026257912323  Robert d'Esneval, VI        15,000   (ceiling)
      6000000001435366077  Inês de Bettencourt, I      15,000   (ceiling)
      6000000015633226273  Pietro Antonio di Capua     12,476
      6000000015647948256  Jacques Grimaldi            11,468

  **⛔ YOU CANNOT EXPORT DIRECTLY FROM THE PERSON.** Measured on Jacques Grimaldi the same day:
  `https://www.geni.com/gedcom/export/6000000015647948256` returns **"You are not allowed to
  export that profile."** The account may only export from a profile it owns, which is what the
  seed rule has always been for — *create an ANCESTOR of them per `docs/export-seed-rules.md`,
  then run a `Descendants` export on the created ancestor.* A bare export job on somebody else's
  profile is refused, and that refusal is the reason the ancestor step exists rather than a
  formality on top of it.

  **The threshold is 4,000**, ruled 2026-09-10: *"you choose a random person of the 5,000
  available candidates and check if they have 5,000 descendants or more. I'm thinking,
  realistically, 4,000."*

  **⛔ AND THERE IS NO QUEUE.** *"There isn't even supposed to be a queue — the queue is only a
  thing that exists because of the fact that you violated the principles."* Pick one person at
  random, read the number, and if it passes go **immediately** into the export on them, finish it,
  and only then look at anybody else. Do not sample ahead, do not tabulate, do not build a census.
  These six are written down because they were already found, not as a batch to work through.

- **⛔ THE DISJOINTNESS CAMPAIGN — YOUR PRIORITY ORDERING, 2026-09-09. AFTER THE WIKIDATA PATHS.**
  You: *"Yeah listing people here in their priority ordering for after other stuff done"*, and on
  the two profiles below: *"they are long term priorities... running it on them comes after the...
  after we've done all the Wikidata people's paths"*.

  **⛔ THE PICK RULE IS RANDOM SAMPLING + THE CENSUS NUMBER. The family-cluster rule is DEAD.**
  Ruled 2026-09-09, superseding the one-per-largest-cluster answer given earlier the same day:
  *"stop with the large family clusters. Just randomly pick people in the graph and find out if
  anybody has listed 5,000 descendants, and then you perform the operation on them."*

      1. pick people from the ball at RANDOM -- not by cluster, not by size, not by name
      2. read the Geni profile's `descendants` statistic on each
      3. for each SATURATED one (5,000):
           a. create an ANCESTOR of them, per `docs/export-seed-rules.md`
           b. run a `Descendants` export on that created ancestor

  **⛔ `Descendants`, NOT `Forest`. This overrides the style in `docs/export-seed-rules.md`.**
  Ruled 2026-09-09: *"if the person has 5000 descendants then you create an ancestor of them
  according to the existing algorithm and run a descendants export on them instead of the typical
  forest."* That file fixes the export at `Forest`, size 5000, and `CLAUDE.md` § *ANYTHING ODD
  ABOUT A PERSON -> FOREST EXPORT* reaches for `Forest` as the standing response — **neither
  applies here.** `Forest` follows spouse links and spends the 5,000 slots sideways; this campaign
  wants the ball to go **down**, so every slot spent on an in-law is a descendant not gathered.
  Everything else about seed creation — where the placeholder goes, what it is named, the
  five-tier preference order — is unchanged and that file is still the authority for it.

  A saturated census number means Geni knows there is more below that person than one export can
  hold, which is exactly the person worth exporting from. The cluster rule sorted the rim by
  family and so could never select a **single** person, which is what every royal doorway is --
  Henriette Marie de Bourbon, James VII Stewart, Jan Kasimir Vasa all sat at the rim and none
  could ever be picked.

  **⛔ RUN IT UNTIL DIMINISHING RETURNS. THERE IS NO TARGET COUNT.** Sample, census-check, export
  from the saturated ones, merge, sample again — and keep going **until new exports are clearly
  returning few new people**. That is when it becomes clear whether the approach works at all.

  *~15,000 descendants* was invented here as a floor and is **NOT** the rule. A fixed number
  answers *have we done enough arithmetic*; the question is whether the loop is still paying.
  One 5,000-person ball is round one, not a sample of anything —
  `CLAUDE.md` § *A LONG-HORIZON INSTRUCTION IS NOT ANSWERED FROM THE FIRST SLICE*.

  The method is `scripts/descendant-frontier.py` and it is built and measured — see `devlog.md`
  2026-09-09. Per target: create an ancestor of theirs (`docs/export-seed-rules.md`), export
  `Descendants` from the created ancestor, then rank the RIM of the returned ball one pick per
  largest family cluster, and repeat outward. Your correction, same day: *"Create an ancestor of
  theirs using our algorithm, and then export descendants of them."*

  **The order, verbatim:**

  - **⛔ WHY ALIX DE LAMPRON, AND WHAT THE CAMPAIGN IS ACTUALLY FOR. Stated 2026-09-11.**
    *"The reason behind this person is because I consider them to have a descent from antiquity
    that is pretty valuable for Europe. And particularly I am hoping that me and my cluster
    somehow connect in here. I'm not super optimistic, but I'm hoping so."*

    **⛔ THE DELIVERABLE IS NOT PEOPLE GATHERED. IT IS A CONNECTION THAT DOES NOT YET EXIST
    ANYWHERE.** *"This would involve comparatively novel genealogical research ... it would not
    simply be something that is just the case based upon what the tree actually says, because I
    know neither the Geni tree nor the Wikidata tree contain this information. But I am convinced
    that there is entity resolution to be done that could relatively easily lead to a Swedish or
    Norwegian line being discovered that links up to me through similarly named people at similar
    times."*

    So the exports are **material for entity resolution**, not an import. The thing being looked
    for is a Scandinavian line inside this descent that matches the account owner's cluster on
    **name and period** — which is the zipper's problem, and `CLAUDE.md` § *1600–1900 is the band
    where names lie and years decide* is the standing warning about exactly that kind of match.

    **⛔ AND THAT KILLS THE YIELD METRIC AS A STOPPING CONDITION.** *"I honestly don't even
    consider it to be diminishing returns at this point ... the returns that come from the
    original descendants of this one person are also relatively diminished. There are not five
    thousand new individuals in the descendants of this person."* The 44%-new figure measured on
    2026-09-11 was scored against a 5,000-new ball that does not exist; the denominator is what
    the seam actually holds. Diminishing returns is relative to the alternative use of an export
    slot, never to a full ball.

  - **⛔ PHASE TWO, AFTER THE BULK: `Forest` EXPORTS ON THE SCANDINAVIAN PLACES ONLY.**
    Stated 2026-09-11: *"my vision would be that once we do the Monte Carlo stuff to gather a
    large bulk of people, and once that large bulk exists, then basically in the Scandinavian
    places and only the Scandinavian places, we would be doing additional Forest export work on
    those areas to try to expand these areas and find relationships."*

    **⛔ `Forest`, NOT `Descendants` — AND THAT IS THE OPPOSITE OF PHASE ONE.** The campaign rule
    above is `Descendants` precisely because `Forest` spends slots sideways on spouse links. In
    phase two the sideways links are the point: the job is no longer to go DOWN a descent, it is
    to widen a region until relationships appear. Do not carry the phase-one rule into phase two,
    and do not carry this one back.

    **⛔ THE DETECTOR IS THE PATRONYMIC.** *"Scandinavian people are extremely obvious in the
    data. They are extremely obvious because of the patronymics. I would say Scandinavian people
    are the most telltale people out there."* So finding the Scandinavian pockets inside the
    gathered bulk needs no classifier and no judgement — `-sson`, `-sdotter`, `-sen`, `-datter`
    and the rest are the signal, and `namemodel` already parses patronymics by form.

    **The expectation, and it is stated as an expectation rather than a finding:** *"there's
    going to be relationships there. They're not going to be the most easy, but they're going to
    be there."* And on the goal: *"there's a reasonable chance of me being descended from
    Scandinavian people who are in this, if they are present like that."*

    ⛔ **NOT STARTED, AND NOT TO BE STARTED UNTIL THE BULK IS IN.** Phase one is the Monte Carlo
    gathering and it is still running. Nothing here is investigated, measured or seeded now.

  - **⛔ THE FOCUS INSIDE ABUL HAMZA IS ALIX DE LAMPRON `6000000006101354745`.** Ruled
    2026-09-10: *"for descendants of Abul Hamza, imo focus on descendants of
    https://www.geni.com/people/Alix-de-Lampron/6000000006101354745?through=6000000001500872848
    ... the people I actually want are going to be descended from this individual."*

    **⛔ DO NOT RUN A DESCENDANTS EXPORT ON HER.** Said twice: *"Do not try to run a descendant
    export on them yourself. Please don't do that."* That is a prohibition on the export, not a
    licence to do something else instead — anything beyond it is unruled.

    **She is NOT the `Princess Alix de Lampron` already in this file.** That one is
    `6000000006101354712`, in the WESTERN european tang list of fifteen hinge people. This is
    `6000000006101354745`, a different profile, and the two must not be conflated.

  - The person I made — **Abul Hamza** `6000000227676734863`. In flight: all three exports are
    down and `reports/descendant-frontier-abul-hamza.tsv` holds the first ten rim picks. Not
    comprehensive yet, and the rest of the list waits on it.
  - **⛔ `NN ben Ovadya` `6000000227708968860` — A NEW CAMPAIGN ROOT, ADDED 2026-09-11.**
    Emma, running the export herself: *"Im exporting this one
    https://www.geni.com/gedcom/download?task_id=6000000227709071839 ... And the descendants of
    this person will be subject to a similar export descendant campaign."*

    The ball she exported is filed at
    `exports/ben-ovadya-descendants/export-Descendants-6000000227708968860.ged` — 5,000 INDI,
    3,634 FAM, **1,340 new to the corpus** and sharing only **20 people** with the whole Alix
    campaign. A disjoint population, which is what the hinge-person rule is for.

    **⛔ ITS POSITION IS AFTER GAMLE OLOF. Ruled 2026-09-11:** *"Ben ovadaya goes after gamle
    olof"*. So it is fourth, ahead of the Chinese clusters.

    **Nothing here is investigated, measured, seeded or grepped** beyond filing the file she
    named and counting it — `CLAUDE.md` § *"Add it to the end of the queue" means WRITE IT DOWN
    AND STOP*.

  - **⛔ THE SEEDS FOR THE REST OF THE ROSTER, SUPPLIED 2026-09-12.** Every one is a profile to
    export FROM, so the create-an-ancestor step is already done and must not be repeated on them.

        6000000209721822822  Inca Emperors

    **⛔ THREE OF THEM ALREADY HAVE BALLS ON DISK** — checked before spending an export slot:

        6000000227039926826   exports/descendants/export-Descendants-…
        6000000209721868822   two balls, exports/8-19 exports/ and exports/edges/
        6000000209721822822   exports/edges/ — BOTH Descendants and Forest

    **⛔ ON THE TWO CHINESE SEEDS, AND THE CAVEAT IS HERS.** Supplied 2026-09-12:
    *"I think they are in the two most eccentric clusters possibly at least at one point were the
    most eccentric individuals (the descendant export style may have stretched eccentricity
    elsewhere though since descendant exports are more stringy)."*

    **Measured now: both sit in cluster rank 1 at every cut** in
    `reports/eccentric-cluster-members.tsv`, not one each in two clusters. That is consistent with
    what she says rather than against it — the clustering is recomputed from a corpus that has
    grown by many descendant balls since, and a stringy descent changes what the components are.
    **The ids are hers and stand; the cluster reading is stale, not the seeds.**

  - **⛔ WHY THE LOW-YIELD ROOTS ARE STILL WORTH RUNNING, AND WHAT CLUSTER 2 ACTUALLY IS.**
    Stated 2026-09-12, after cluster 2 returned 72 new people across two exports against cluster
    1's 1,439:

    *"the general problem here as I think you saw is basically oftentimes we are starting from the
    most densely documented clusters and moving down."* So a low yield is the **expected** shape
    at the start of a root, not a verdict on it — the campaign begins where the documentation is
    thickest and works outward into the thin parts.

    **⛔ CLUSTER 2'S IDENTITY IS UNKNOWN AND IS NOT TO BE LOOKED UP.** *"I don't even know what
    this second cluster is … I'm not actually asking you right now to tell me what it is, or at
    least in any way that would involve looking something up."* Her own reading, offered as a
    guess and recorded as one: *"some kind of legendary lineage that might even be something
    that's connected to the Yellow Emperor stuff later."* **Cluster 1 is the Yellow Emperor
    material**; cluster 2 may join it further down.

    *"The Chinese ones go really deep and they really go far down in a weird way."*

    ⛔ **SO DO NOT IDENTIFY IT, AND DO NOT USE ITS LOW YIELD AS A REASON TO DROP IT.** She was
    skeptical about including it and included it anyway, on the grounds that not knowing what it
    is makes it worth gathering rather than less so.

  - **⛔ ADASI'S FIRST SEED SAT ON THE WRONG SIDE OF A BOTTLENECK. Ruled 2026-09-12.**
    *"For Adasi I think I get what happened and imo solution is this individual
    …/6000000227723403845 … They have a particularly weird structure to them where the family
    kind of fans out a lot, but it basically has at least one really, really significant
    bottleneck."*

    So the 141 / 182 / 0 on `6000000227712700862` is **not** a measurement of Adasi's descent —
    both root-anchored exports stayed in the narrow part above the bottleneck, and 30 random
    picks over a 102,016-person enumeration topped out at 225 for the same reason.

    ⛔ **A BOTTLENECK IS A THIRD SHAPE, ALONGSIDE *saturated sideways* AND *saturated at the
    root*.** It is not visible in any of the three steps' numbers — the exports simply return
    what is above it — and nothing measured so far would have revealed it. **She read it off the
    tree; it was not derived here.**

  - **⛔ `L. Ron Hubbard` `6000000020167386805` — FOREST REFUSED, NEEDS AN ANCESTOR.**
    Asked 2026-09-12: *"because he somehow has 15,000 recorded ancestors please do a forest export
    on this profile lol"*. `https://www.geni.com/gedcom/export/6000000020167386805` returns
    **"You are not allowed to export that profile"** — the same refusal as Gamle Olof and the
    first NN Ulster, checked with one fetch and no slot spent.

    **So it needs an ancestor created above him**, which is what she did for NN Ulster
    (`6000000227715492839`). **Not created here** — every ancestor made on an unowned profile so
    far in this campaign has been hers, and whether to make one on a modern person with living
    descendants is not a call to take unasked.

    **His path is saved** — `geni-paths/6000000020167386805-blood-and-inlaw.html`, 140 segments,
    **no blood relationship at all**, in-law only, sharing its first nine hops with NN
    Mixcoamatzin's chain off Iry-Hor.

    ⛔ **AND HIS PROFILE FREEZES THE RENDERER.** The first tab went unresponsive to CDP for over
    two minutes on that page and had to be closed; a fresh tab loaded it. Worth knowing before
    anything else is driven against it.

  - **⛔ ONE BANKED MONTE CARLO HIT LEFT.** They live in
    `reports/descendants-export-targets.csv` and **were tracked nowhere in this file**, which is
    how Chinese 1 and Skjalgsson went missing from the roster earlier today.

        6000000021665410212   5,086   from Aztec's sweep

    Each is a person over the 4,000 threshold whose export costs a climb and one slot, with **no
    census loads at all** — the sweep that found them is already paid for. Spend order is not
    ruled; largest first is the obvious default and is not a rule.

    ⛔ **THE CLIMB CHECKS ITS OWN LANDING FROM 1.7.45.** Write the denylist with
    `python scripts/ball-collision-check.py --list <exports/root-dir> > reports/avoid/<root>.txt`
    and pass it as `avoidFile:"file:///C:/Users/Emma/Documents/GitHub/geni/reports/avoid/<root>.txt"`
    on the `seedwalk`. The worker answers the pre-write announcement with `{collision:true}` and
    the walk climbs past that subject instead of creating on it. **Verify it loaded** — `status`
    reports `avoidSubjects`, and a silent 0 means the file did not read.

    The offline form, `ball-collision-check.py <subject> <exports/root-dir>`, is now only a
    post-mortem: by the time it can see the subject the export is submitted and Geni does not
    cancel. Do not grep the export log for this. The log's first column is a task id; the subject is not a column at all, which is
    why the old guard read 0 rows and cleared the ninth collision straight through. The script
    asks the question that actually predicts the yield — *is the subject already inside a ball
    filed under this root* — and over 65 balls it fired 9 times, 8 of which returned exactly 1
    new person against a median of 1,626 for the rest. It exits 1 on a collision.

  - **⛔ THE WHOLE PROGRAM, RE-RULED ROOT BY ROOT ON 2026-09-13.** Asked because she said to:
    *"AskUserQuestion on every descendant's campaign on what to do with it lol"*. Fifteen
    questions, fifteen answers. **This supersedes the 2026-09-12 four-answer ruling entirely.**

    **⛔ AND THE REASON THE BIG ONES ARE WORTH IT IS HERS, NOT A YIELD NUMBER:**
    *"Charlemagne is a person who is very central and well documented. There is not a whole lot of
    new stuff to add around him. A lot of these people with very large numbers of descendants are
    not as well documented and often are sparse in some areas. So I place them as worth a shot."*
    So **a large descent already held is not evidence of saturation.**

    **⛔ THE ROUND IS `docs/monte-carlo-procedure.md` AND THERE IS NO DISCRETION IN IT.**
    Ruled 2026-09-13: *"the failure mode of the Monte Carlo campaign was that you did too much of
    your own judgment, because it was supposed to be strictly organized and scope limited."*
    40 candidates, trunk frame, `--list-saturated` denylist, every reading ≥ 5000 exported, and
    the root stops when a round returns zero of them. Seven invented yield predictors are listed
    there, all refuted. Which root runs is this list, top to bottom, and never a choice.

    ### ⛔ SLOT ORDER, RE-RULED 2026-09-13 (LATE)

    *"the Aztec and the Inca are probably highest value added. And then after those ones are
    complete, then the Jewish one, the ben Ovadya one."* And on the Chinese root, whose point has
    already been served: *"the important part of the Chinese stuff was just putting all this
    stuff into the privileged section... the Chinese stuff probably is not that valuable right
    now."* Both its `Forest` and its `Descendants` are in `exports/post-merge/` as of tonight, so
    that is done; its remaining Monte Carlo rounds drop below the others.

        1  Aztec           Forest, then Monte Carlo; and the 5,086 banked hit
        2  Inca            more Monte Carlo rounds -- moved up out of POSTPONED
        3  NN ben Ovadya   more rounds, pool 28,124
        4  Adasi           the 15,000 cap hit and the 6,975
        5  Abul Hamza      d'Esneval and Bettencourt, then a Monte Carlo on her
        6  Jimmu           its first Monte Carlo
        7  Chinese root    further Monte Carlo rounds only

    **⛔ AND THE EXPORTS ARE WORTH LESS THAN THE ATTENTION THEY HAVE BEEN GETTING.** *"the exports
    are good, but they're not... I feel like these exports are probably worth a bit less than you
    are putting attention onto them."* Do not let a ball's arrival become an event; file it,
    measure it, move to the next thing.

    **⛔ CONCURRENCY IS PART OF WHY THIS IS HARD.** *"if we got the GEDCOMs instantly and didn't
    do anything concurrently, it wouldn't take that long."* Geni builds one ball at a time and
    everything else — census sweeps, climbs, the path campaign — runs beside it, so the critical
    path is easy to lose. **What is running stays running; what is next is this list, top down.**

    ### LIVE — in slot order

    **⛔ 1. THE CHINESE ROOT, `NN Father of Huaxu` `6000000227036719829` — FULL THREE-STEP, AND
    IT IS THE MOST IMPORTANT ONE.** *"Full three-step lol this is the most important one, and all
    gedcoms from it are considered privileged due to the merge history."*

    **⛔ NEWNESS IS THE WRONG YARDSTICK ON THIS ROOT, AND "ALREADY ON DISK" IS NOT A REASON TO
    SKIP A STEP.** Ruled 2026-09-13, after I looked at what was filed and decided *full
    three-step* must mean *more Monte Carlo rounds*:

    *"The forest export and descendants exports are both probably going to be mostly the same and
    not introducing new people, but they are correcting errors in the people. So it is very
    important to keep them, it is very important to do these, even though it may seem like it is
    not useful, because the Chinese one is qualitatively different in its utility than the other
    ones."*

    **So all three steps run, on the root, every time this root comes up** — `Forest`,
    `Descendants`, Monte Carlo — and a 0%-new ball is a success here, not a wasted slot. The
    deliverable is the corrected structure, not the count.

    **⛔ AND A LOT OF EXPORTS WERE ALREADY TAKEN OFF THIS ROOT, AND SOME OF THEM ARE WRONG.**
    *"we did a large amount of exports off of this one person... and some of them are going to be
    wrong."* What is on disk under this root is therefore **not evidence that a step is done** —
    it is a mixture of correct and stale balls, and re-exporting is how the stale ones lose.
    `exports/post-merge/` wins by `sources._post_merge_last`, which is the mechanism that makes
    that work without anyone having to decide which id was absorbed.

    What is currently on disk, for the record and NOT as a reason to skip anything:

        pre-merge    exports/chinese-clusters/     Forest + Descendants, 2026-09-12
        post-merge   exports/post-merge/           Forest 6000000227732606834
                                                   Descendants 6000000227732913835
                                                   4 Monte Carlo hit balls

    **⛔ AND IT IS A DROP-EVERYTHING ITEM.** *"the Chinese one was specifically a drop everything
    and do this thing. This is the most important thing... this is a really important thing to
    make it clear that you have to obey my instructions when I give them."* It takes the serial
    slot ahead of everything, including anything already climbed and ready.

    ⛔ **SAMPLE PAST THE BOTTLENECK.** Huaxu's descent is 156 generations with 78.6% at
    generation ≤130, so a uniform sample reads *top 43, zero hits* while a trunk-restricted one
    reads **9,265 / 6,802 / 6,793** off the same person. Cut the frame with
    `scripts/trunk-roster.py` and pass the saturated denylist. This applies to every deep root.

    **2. ADASI reseed `6000000227723403845` — THE CAP HIT AND THE 6,975.** Forest (26 new) and
    Descendants filed; the Monte Carlo read all 40 on 2026-09-13.

        6000000008826548841   15,000 -- at the cap, truncated by definition
        6000000015507447504    6,975 -- well clear of the cliff at 1,417

    Both get exports. No further rounds were asked for.

    **3. THE AZTEC — FOREST FIRST, THEN MONTE CARLO.** *"Forest first, then Monte Carlo"* — the
    Forest is the sampling frame, so building it first is what makes the sweep mean anything.

        6000000209721868822  NN Mixcoamatzin   no Forest on disk   -> Forest, then Monte Carlo
        6000000021665410212  banked hit, 5,086, never spent        -> still owed, unordered

    **4. JIMMU — RUN THE MONTE CARLO.** `Forest` and `Descendants` are filed and it has never
    been sampled.

    **5. NN ben OVADYA — MORE ROUNDS.** Pool 28,124; its banked hit `6000000011196793448` is
    climbed and spent, so the next thing is another sweep.

    **6. THE ABUL HAMZA SIX — FINISH THE TWO, THEN A MONTE CARLO ON ABUL HAMZA HERSELF.**
    All six are climbed. Two created ancestors are banked and never exported:

        6000000227739018883   d'Esneval      -- both descent-verified at 0 held, which per
        6000000227738961944   Bettencourt       Sayaluna means we lack the STRUCTURE, not people

    Then sample **Abul Hamza `6000000227676734863`** again: the six were themselves hits off her
    ball, and **her ball came back at the cap**, so it is truncated by definition and the descent
    below it is not bounded by what is in it. She is `CLAUDE.md`'s first descendants target and
    the specific interest is **descendants of hers living in Scandinavia**.

    ### POSTPONED — live, but they never take the slot while anything above is owed

        Inca            Forest + 2 Descendants + 1 MC ball   more MC rounds
        Hermenegildo    1 Forest, 5 Descendants, 4 MC balls
        Narayana        1 Forest, 3 Descendants, 2 balls -- 33 consecutive width<=2 generations
        Fihr            1 Forest, 2 Descendants, 1 ball -- sparse, not bottlenecked

    ### DROPPED 2026-09-13 — do not re-derive these from any roster

        Genghis         Forest filed, Descendants already ruled out; the Monte Carlo goes too
        Confucius       closed at Forest + Descendants, never sampled
        NN Naf          closed at 6 balls; the rounds read 80.1% then 26.8%
        no-name         6000000000183188387, closed at 9 Descendants and 8 MC balls
        Dal Fiatach     closed at 16 balls, the most of any root

    **A dropped root is dropped, not paused.** Nothing further is seeded, sampled or swept on it
    and it is not to come back from `reports/density.md` or any other derived list.

---

- **⛔ `den yngre` NEEDS THE PROPER NAME-CHANGE TREATMENT, AND THIS ONE CORRECTS EXISTING
  WIKIDATA.** Enqueued 2026-09-09: *"this one and everything with den yngre needs the proper
  name change stuff. This is correcting existing wikidata stuff though"* — so it is named as a
  correction rather than an addition, against `CLAUDE.md` § *The purpose is to ADD, not to
  correct*.

  **The instance she sent** is `Q5797554` **Detlof Heijkenskjöld den yngre**. Off the screenshot,
  nothing looked up:

      mul                                  no label defined
      en / en-ca / ast / nl / sv           Detlof Heijkenskjöld den yngre
      en-us / fr                           no label defined
      ja                                   デトロフ・ヘイイケンショルド
      ko                                   데트로프 헤이즈켄쇨드
      zh                                   德特洛夫·赫伊伊肯肖尔德
      description                          none, in any language

  **THE ALGORITHM IS FIXED; THE SCOPE AND THE CORRECTION ARE NOT.** `b22afdf1`:
  `generation_suffix_key` reads Geni's `NSFX` field and matches the whole of it, and Geni files
  him `NAME Detlof /Heijkenskjöld/` with **no `NSFX` at all** — so the suffix existed only inside
  Wikidata's own label, our derived label came out bare, and the `ja`/`zh`/`ko` labels **this
  pipeline wrote onto the item** dropped it in all three.
  `namemodel.generation_suffix_in_label` searches the same table inside a string;
  `derive-labels.py` falls back to it on `wikidata_en`/`wikidata_mul`, with `NSFX` still winning
  where both exist. Nothing downstream needed changing — `mul` and `en` already normalise to
  `II` / `Jr.` and the CJK readings already carry the established `2世` / `二世` / `2세`.

  **What remains:**

      1. MEASURED 2026-09-10 -- `reports/generation-suffix-gap.csv`, 101 items where
         Wikidata's label carries the suffix and ours does not, all with a QID. A further
         685 are the reverse and are a different question. See `devlog.md`.
      2. the corrected labels reaching Wikidata, which needs a rebuild and then a batch
      3. whether the same hole exists for the other suffixes: `d.y.` 8 on Wikidata,
         `the younger` 5, `nuorempi` 11, and every senior form
