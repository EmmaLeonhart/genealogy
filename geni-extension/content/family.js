/* Step 1 of the per-individual loop: scrape the immediate family FROM THE PAGE, and save it.
 *
 * **Emma, 2026-09-06:** *"on each individual we always grab the html family members and save them
 * first, then try to get the Charlemagne path"*, and *"we also do the immediate family scrape on
 * sibling pairs in paths because parents are needed and this is the quickest way to get them."*
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

/* The relationship phrases Geni opens each line of the immediate-family block with. Anchors are
 * attributed to the nearest phrase ABOVE them, which is how the block is actually laid out:
 * "Son of A and B", "Husband of C", "Father of D; E", "Brother of F". */
GC.family.PHRASES = [
  [/^son of/i, "parent"], [/^daughter of/i, "parent"],
  [/^husband of/i, "spouse"], [/^wife of/i, "spouse"],
  [/^partner of/i, "partner"], [/^ex-husband of/i, "ex-spouse"], [/^ex-wife of/i, "ex-spouse"],
  [/^father of/i, "child"], [/^mother of/i, "child"],
  [/^brother of/i, "sibling"], [/^sister of/i, "sibling"],
  [/^half brother of/i, "half-sibling"], [/^half sister of/i, "half-sibling"],
  [/^stepson of/i, "step-parent"], [/^stepdaughter of/i, "step-parent"]
];

GC.family.classify = function (text) {
  const t = (text || "").trim();
  for (const pair of GC.family.PHRASES) {
    if (pair[0].test(t)) return { relation: pair[1], phrase: t.split(" of")[0].trim() };
  }
  return null;
};

/* Every relative on the page, with the relationship each was listed under.
 *
 * Walks the block in document order and attributes each `data-profile-id` anchor to the most
 * recent relationship phrase seen. A phrase with no anchors after it contributes nothing, and an
 * anchor before any phrase is recorded with an empty relation rather than guessed at. */
/* ⛔ "AND N OTHERS" IS NOT A COLLAPSED LIST. Those relatives have NO ANCHOR, and no click makes one.
 *
 * Geni renders a long line as `Hugo; Rosa; Elsa; Hermine; Margaretha and 1 other; and Laura`.
 * That reads like an expander, and a `GC.family.expand` was written on 2026-09-06 to click it.
 * **It was measured and it does nothing**, which is why it is not in this file:
 *
 *     Julius Hohenberger   6 anchors -> click "1 other"  -> 6 anchors, text unchanged
 *     Arne Garborg         8 anchors -> click "3 others" -> 8 anchors, text unchanged
 *
 * A real `MouseEvent` behaves the same, and **`« less` is already displayed on both** — the list
 * is expanded, and the missing people are named in the count while carrying no `href`. They are
 * relatives Geni will not link, which is what a redacted or private profile looks like in this
 * block.
 *
 * So the shortfall is a LIMIT OF THE SOURCE, not a defect to fix, and the honest thing is to make
 * it visible rather than to let a row count imply completeness. `toTsv` writes `# unlinked <n>`,
 * read out of the prose, so a consumer counting rows can see that `n` relatives exist and were
 * never linkable. `CLAUDE.md` § *Grab the RESIDUALS*: the prose keeps what the structured walk
 * drops, and here the prose is the only place the gap is stated at all.
 *
 * The clicking version is left out deliberately -- it clicked 18 toggles across the page on its
 * first run and gained not one anchor. § *a fix that changes nothing is evidence, not
 * reassurance.* */
GC.family.scrape = function () {
  const lead = [...document.querySelectorAll("*")].filter(
    (e) => e.children.length === 0 && GC.family.classify(e.textContent));
  if (!lead.length) return { found: false, relatives: [] };

  /* ⛔ THE CONTAINER IS THE COMMON ANCESTOR OF ALL THE LINES, not the parent of the first.
   *
   * Each line of the block has its own parent element, so `lead[0].parentElement` is one line.
   * Scoped that way the first run returned **parents only** on a man whose page also reads
   * "Husband of Nicoline Rebekka Svensdatter Ramsvig" and "Father of Andreas Petrus Eliassen
   * Hoknes" -- a scrape that looks like a complete answer and silently drops two thirds of the
   * family. Climbing to the ancestor that contains the LAST phrase as well is what makes the
   * walk cover every line. */
  let block = lead[0].parentElement;
  const last = lead[lead.length - 1];
  let guard = 0;
  while (block && !block.contains(last) && guard++ < 12) block = block.parentElement;
  if (!block) return { found: false, relatives: [] };

  const relatives = [];
  const seen = new Set();
  let current = null;

  const walk = document.createTreeWalker(block, NodeFilter.SHOW_ELEMENT | NodeFilter.SHOW_TEXT);
  for (let n = walk.nextNode(); n; n = walk.nextNode()) {
    if (n.nodeType === Node.TEXT_NODE) {
      const hit = GC.family.classify(n.textContent);
      if (hit) current = hit;
      continue;
    }
    if (n.tagName === "A" && n.hasAttribute("data-profile-id")) {
      const pid = n.getAttribute("data-profile-id");
      const key = (current ? current.relation : "") + "|" + pid;
      if (seen.has(key)) continue;
      seen.add(key);
      relatives.push({
        relation: current ? current.relation : "",
        phrase: current ? current.phrase : "",
        geni_id: pid,
        name: (n.textContent || "").trim()
      });
    }
  }
  return { found: true, relatives: relatives, prose: (block.innerText || "").replace(/\s+/g, " ").trim() };
};

/* How many relatives the prose NAMES but the block does not LINK -- the `and N others` counts,
 * summed. Zero for most people; 3 on Arne Garborg, 1 on Julius Hohenberger. */
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
   * Emma, 2026-09-06: *"you write stuff into files in the repo you dummy."* */
  const tsv = GC.family.toTsv(id, subjectName, scraped, stats);
  /* One download per page load, which is exactly one per profile. `saved` means the click was
   * awaited, not that the file is on disk -- `scripts/file-geni-downloads.py` is what confirms
   * that, by finding it. */
  let saved = false;
  if (!job.dryRun) {
    try { await GC.saveBlob(id + "-family.tsv", tsv, "text/tab-separated-values"); saved = true; }
    catch (e) { saved = false; }
  }

  const counts = {};
  for (const r of scraped.relatives) counts[r.relation || "?"] = (counts[r.relation || "?"] || 0) + 1;

  return {
    job: "family", geni_id: id, name: subjectName, state: "scraped",
    relatives: scraped.relatives.length, by_relation: counts,
    parents: scraped.relatives.filter((r) => r.relation === "parent").map((r) => r.geni_id),
    siblings: scraped.relatives.filter((r) => r.relation === "sibling").map((r) => r.geni_id),
    stats: stats, saved: saved, unlinked: GC.family.unlinked(scraped.prose), filename: id + "-family.tsv", tsv: tsv
  };
};
