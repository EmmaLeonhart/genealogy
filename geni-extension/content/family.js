/* Step 1 of the per-individual loop: scrape the immediate family FROM THE PAGE, and save it.
 *
 * **On each individual the HTML family members are grabbed and saved FIRST, and only then is the
 * Charlemagne path requested.** The immediate-family scrape also runs on the sibling pairs in
 * paths, because the parents are needed and this is the quickest way to get them.
 *
 * `docs/per-individual-loop.md` is the order. This job is the cheap, unconditional one: no search
 * is requested, no export is spent, nothing is created. It runs on everybody, first, and the page
 * load it needs is the same one steps 2 and 3 were going to make anyway — so the family members
 * cost nothing extra, and a person who later fails to yield a path has still yielded these.
 *
 * ⛔ WHY IT MATTERS MOST FOR SIBLINGS. Geni records **no sibling edge** — two siblings are joined
 * only through a shared parent — so a path that steps sideways between them names a parent that
 * may be in nothing we hold. `CLAUDE.md` § *A sibling step is the worked example* measured it:
 * **2,125 sibling steps of 30,329, across 662 of 696 path files.** Scraping both members' family
 * is one page load each and yields exactly the parent the step needs.
 *
 * **The prose block is the source, not the labelled one.** That is not a style choice: on
 * 2026-09-05 the labelled block reported `father` alone for a woman with two parents, and
 * `nothing at all` for another, while the prose named both. Reading the labels put a spurious
 * third parent on a live profile. § *The labelled block is not the parent list*.
 */

GC.family = {};

/* ⛔ THE RELATION IS READ OFF THE CARD, NOT INFERRED FROM PROSE. Ruled 2026-09-10.
 *
 * Geni renders the immediate family TWICE on the same page and this file used to read the harder
 * of the two. Emma: *"There's the easy immediate family section and the hard one ... I didn't
 * catch that you were doing the hard one."*
 *
 *     HARD  the prose cell -- "Son of Nikulás Rögnvaldsson and Herborg Bárðardóttir Husband of
 *           ... and 1 other". The relation is an OPENER governing a run of anchors after it, so
 *           reading it needs a table of every phrase Geni writes, a guard for phrases not in the
 *           table, and a scope that stops the run at the right place.
 *     EASY  the card grid, already in the DOM with no click and no toggle: each relative is a
 *           card carrying `div.quiet` with the relation word and an `a[data-profile-id]`.
 *
 * **Every defect this scraper had came from the prose and none of them can occur here.** The
 * 24-opener table that drifted out of step with `scraped_pages.py`; `Ex-partner of` matching
 * `partner of` mid-string and turning two ex-partners into spouses; an unrecognised opener
 * silently extending the previous relation; and the worst of them, a profile literally named
 * `Daughter Of Gaon The` whose NAME parsed as an opener and made ten people into R' Chaim
 * Volozhiner's parents. A relation that is an attribute of a card cannot be any of those.
 *
 * ⛔ **AND IT ANSWERS WHAT THE PROSE CANNOT: WHICH PARENT IS THE FATHER.** The prose says
 * "Son of A and B" and never says which is which -- `seed.js` carries a whole `skipped` state for
 * it and `docs/export-seed-rules.md` tier 3 turns on knowing. The card says `father` and `mother`.
 *
 * The relation word describes the RELATIVE's role, which is the same convention the old phrase
 * table produced: `Son of A` recorded A as `parent`, and a card labelled `father` records that
 * person as `parent` too. Nothing downstream changes. */
GC.family.RELATION = {
  "father": "parent", "mother": "parent",
  "son": "child", "daughter": "child",
  "husband": "spouse", "wife": "spouse",
  "ex-husband": "ex-spouse", "ex-wife": "ex-spouse",
  "partner": "partner", "ex-partner": "ex-spouse",
  "fiancé": "fiance", "fiancée": "fiance", "fiance": "fiance", "fiancee": "fiance",
  "brother": "sibling", "sister": "sibling", "sibling": "sibling",
  "half brother": "half-sibling", "half sister": "half-sibling",
  "stepfather": "step-parent", "stepmother": "step-parent",
  "stepson": "step-child", "stepdaughter": "step-child",
  "stepbrother": "step-sibling", "stepsister": "step-sibling",
  "adoptive father": "adoptive-parent", "adoptive mother": "adoptive-parent",
  "adopted son": "adopted-child", "adopted daughter": "adopted-child",
  "foster father": "foster-parent", "foster mother": "foster-parent",
  "foster son": "foster-child", "foster daughter": "foster-child"
};

/* The prose cell is still READ, and only read. `CLAUDE.md` § *Grab the RESIDUALS*: it carries the
 * "and N others" count for relatives Geni names but will not link, which the card grid does not
 * state and which `toTsv` reports as `# unlinked`. It is a record, never a source of structure. */
GC.family.proseText = function () {
  const th = [...document.querySelectorAll("th")]
    .find((e) => /^immediate family/i.test((e.textContent || "").trim()));
  const cell = th && th.parentElement ? th.parentElement.querySelector("td") : null;
  return cell ? (cell.innerText || "").replace(/\s+/g, " ").trim() : "";
};

GC.family.scrape = function () {
  const relatives = [];
  const seen = new Set();
  /* A label node is a leaf `div.quiet` whose whole text is one relation word. Scoping to the
   * label and climbing to the card it belongs to is exact: the card is the nearest ancestor that
   * also holds a profile anchor, and there is one anchor per card. */
  const labels = [...document.querySelectorAll("div.quiet")]
    .filter((e) => e.children.length === 0
                && GC.family.RELATION[(e.textContent || "").trim().toLowerCase()]);
  for (const label of labels) {
    const word = (label.textContent || "").trim().toLowerCase();
    let n = label, a = null;
    for (let i = 0; i < 5 && n && !a; i++) {
      n = n.parentElement;
      if (n) a = n.querySelector("a[data-profile-id]");
    }
    if (!a) continue;
    const pid = a.getAttribute("data-profile-id");
    const key = word + "|" + pid;
    if (seen.has(key)) continue;
    seen.add(key);
    relatives.push({
      relation: GC.family.RELATION[word],
      phrase: word,
      geni_id: pid,
      name: (a.textContent || "").trim()
    });
  }
  /* ⛔ NO FALLBACK TO THE PROSE. Ruled 2026-09-10, "structured only, delete the prose parser". A
   * page with no card grid reports `found: false` and is a person to look at, not a person to
   * guess at from a weaker source. */
  return { found: relatives.length > 0, relatives: relatives, prose: GC.family.proseText() };
};

/* How many relatives the prose NAMES but does not LINK -- the `and N others` counts, summed.
 *
 * ⛔ KEPT WHEN THE PROSE PARSER WENT. The structured card grid does not state this shortfall at
 * all, so the prose is the only place it is visible -- `CLAUDE.md` § *Grab the RESIDUALS*. Those
 * relatives carry no `href` and no click reveals one (measured on Julius Hohenberger and Arne
 * Garborg, 2026-09-06), so `# unlinked <n>` is what stops a row count implying completeness.
 * Reading a COUNT out of the prose is not parsing structure out of it. */
GC.family.unlinked = function (prose) {
  let n = 0;
  const re = /and (\d+) others?/gi;
  let m;
  while ((m = re.exec(prose || ""))) n += parseInt(m[1], 10);
  return n;
};

GC.family.toTsv = function (subject, subjectName, scraped, stats) {
  const head = [
    "# Immediate family scraped from the Geni profile page. Step 1 of the per-individual loop.",
    "# subject\t" + subject + "\t" + subjectName,
    "# prose\t" + (scraped.prose || "").slice(0, 400),
    "# unlinked\t" + GC.family.unlinked(scraped.prose) +
      "\trelatives the prose names that carry no link, and that no click reveals",
    "# statistics\tfamily_tree=" + (stats.family_tree === undefined ? "" : stats.family_tree) +
      "\tblood_relatives=" + (stats.blood_relatives === undefined ? "" : stats.blood_relatives) +
      "\tancestors=" + (stats.ancestors === undefined ? "" : stats.ancestors) +
      "\tdescendants=" + (stats.descendants === undefined ? "" : stats.descendants) +
      "\tfollowers=" + (stats.followers === undefined ? "" : stats.followers) +
      "\tread=" + (stats.read ? "1" : "0"),
    ["subject_geni_id", "relation", "phrase", "relative_geni_id", "relative_name"].join("\t")
  ];
  for (const r of scraped.relatives) {
    head.push([subject, r.relation, r.phrase, r.geni_id, r.name].join("\t"));
  }
  return head.join("\n") + "\n";
};

GC.runFamily = async function (job) {
  const id = String(job.geni_id);
  /* Before anything: is this Geni, or the block page? A CAPTCHA scrapes as a person with no
   * family and no statistics, and reports success. */
  if (GC.blocked()) return { job: "family", geni_id: id, state: "blocked" };
  await GC.until(
    () => !!document.querySelector("#family_profile_module, .immediate-family"), 25000);

  const subjectName = ((document.querySelector("h1") || {}).textContent || "").trim();
  const scraped = GC.family.scrape();
  /* The statistics come from the same page load and are read here rather than inferred later:
   * a saturated Blood Relatives figure is what tells a genuine isolate from a query that
   * overflowed, and step 3 turns on that distinction. */
  const stats = await GC.statistics();

  if (!scraped.found) {
    return { job: "family", geni_id: id, name: subjectName, state: "no_family_block",
             relatives: 0, stats: stats };
  }

  /* RETURNED, never downloaded -- `common.js` § *THE COLLECTOR DOES NOT DOWNLOAD FILES*.
   * The caller writes it into a file in the repo; nothing here downloads. */
  const tsv = GC.family.toTsv(id, subjectName, scraped, stats);


  const counts = {};
  for (const r of scraped.relatives) counts[r.relation || "?"] = (counts[r.relation || "?"] || 0) + 1;

  return {
    job: "family", geni_id: id, name: subjectName, state: "scraped",
    relatives: scraped.relatives.length, by_relation: counts,
    parents: scraped.relatives.filter((r) => r.relation === "parent").map((r) => r.geni_id),
    siblings: scraped.relatives.filter((r) => r.relation === "sibling").map((r) => r.geni_id),
    stats: stats, unlinked: GC.family.unlinked(scraped.prose), filename: id + "-family.tsv", tsv: tsv
  };
};
