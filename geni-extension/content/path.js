/* The relationship-path job: request the search, wait for it, capture, parse.
 *
 * This is the pilot's instrument and, if the hit rate justifies it, the 185,327-target
 * campaign's. What it replaces is an agent taking one sampled snapshot per tool call at 10-20
 * seconds each -- `geni-paths/README.md` says the design must MINIMISE observations because
 * that channel is the one that lies. Here there is no sampling: a MutationObserver fires on the
 * mutation that resolves the search.
 *
 * THE PUSHPIN IS NEVER TOUCHED. It is pinned to Charlemagne exactly once, by hand, out of band.
 * Toggling it mid-run re-anchors every later search to "You".
 * Nothing in this file calls `toggleRelationshipAnchor`, and the check that the anchor is right
 * is that the description names Charlemagne on one end.
 */

GC.parsePath = function () {
  /* Mirrors `genimerge.genipage.parse_relationship_path`: the steps are the anchors carrying
   * `data-profile-id` INSIDE `span.segment > span.name`, and nothing else. A Geni profile page
   * carries several hundred `data-profile-id` anchors -- immediate family, managers, followers
   * -- so matching them directly yields a plausible-looking list that is not a path. That
   * scoping IS the parser. */
  const links = [];
  for (const seg of document.querySelectorAll("span.segment")) {
    const a = seg.querySelector("span.name a[data-profile-id]");
    if (!a) continue;
    links.push({
      geni_id: a.getAttribute("data-profile-id"),
      name: (a.textContent || "").trim(),
      relation: ""
    });
    const sub = seg.querySelector("span.subtext");
    if (sub && links.length) {
      let t = (sub.textContent || "").replace(/\u00a0/g, " ");
      t = t.split(/\s+/).join(" ").trim();
      if (t.startsWith("(") && t.endsWith(")")) t = t.slice(1, -1).trim();
      /* The first step's subtext is a non-breaking space: Geni prints "You" with nothing to
       * relate it to, so an empty relation is left empty rather than invented. */
      if (t) links[links.length - 1].relation = t;
    }
  }
  return links;
};

GC.toTsv = function (links, header) {
  /* Byte-compatible with `genipage.to_tsv`, so a file written here is one `genimerge.paths`
   * reads. The `geni:<id>` note column is what makes the later check an exact join rather than
   * a name match. */
  const out = header ? header.split("\n") : [];
  out.push(["step", "name", "relation_to_previous", "note"].join("\t"));
  links.forEach((l, i) => {
    out.push([i + 1, l.name, l.relation || "-", "geni:" + l.geni_id].join("\t"));
  });
  return out.join("\n") + "\n";
};

/* ⛔ THE IN-LAW SEARCH. A BLOOD MISS IS NOT AN ANSWER TO THE QUESTION.
 *
 * In-law connections are just as valid; blood is not required. This search was never being run
 * at all, so in-law relationships were simply not being saved.
 *
 * `runPath` asks Geni for the BLOOD path. When that misses, Geni offers a second search under
 * *"They might be connected in other ways"* with a **Show Me** button, and nothing ever clicked
 * it. So every `resolved_none` this collector has ever recorded means *no blood path*, which is
 * a narrower statement than the one the ledger's `path_found` column is read as making.
 *
 * `docs/anchor-protocol.md` already said as much about one person — Rudolf Beck, *"a blood miss
 * with in-law unchecked"* — and that sentence sat there while the same gap applied to every
 * miss in the file.
 *
 * **It is a SECOND REQUEST, with the same asynchrony as the first.** The button fires a search
 * that resolves later, so this waits the same way `runPath` does rather than reading the page
 * once and calling it empty.
 *
 * Returns `resolved_path` with the chain, `resolved_none` when Geni says
 * *"No in-law relationship was found."*, or `not_offered` when there is neither a stated answer
 * nor a button to press -- which is a real state and is not a miss. */
GC.runInLaw = async function (job) {
  const id = String(job.geni_id);

  /* ⛔ THE ANSWER IS READ BEFORE THE BUTTON IS LOOKED FOR, and getting that order wrong threw
   * away the verdict on EVERY person this loop finished.
   *
   * Geni states the in-law miss in words -- *"No in-law relationship was found."* -- and once it
   * has, the **Show Me** button is gone, because there is nothing left to press. This function
   * looked for the button first and returned `not_offered` the instant it was absent, so a
   * stated verdict read as *never asked*.
   *
   * That is not an edge case: measured 2026-09-08 on the first three targets of the run --
   * Constans Wilhelm Wenström `1605703`, Raymond Impanis `2205409`, Karl Olofsson `2398881` --
   * **3 of 3** had the sentence on the page, no button, and came back `not_offered`.
   *
   * And it is silent, cumulative and self-perpetuating. `individual.js` computes
   * `asked = resolved_path || resolved_none`, so `not_offered` leaves `via` blank;
   * `scripts/collector-worklist.py` re-queues on exactly a blank `via` -- *"If blood did not hit
   * and there is no path then redo it."* So every person the loop completed returned to the pool
   * forever, and re-running them would produce the same blank again. The campaign could scrape
   * indefinitely and never mark anybody done.
   *
   * `common.js` already lists this sentence in its miss regex, and `write-family-scrape.py`'s
   * `path_state()` already reads the blood miss off the page the same way. This is the same rule
   * in the one place that was refusing to apply it.
   *
   * ⛔ ONLY A MISS. A HIT STILL CANNOT BE READ OFF THE PAGE -- `write-family-scrape.py`'s
   * asymmetry rule -- so nothing here infers `resolved_path` from prose. A miss is stated; a hit
   * needs the parsed chain below. */
  const stated = () => /no in-law relationship was found/i.test(
    document.body ? document.body.innerText : "");
  if (stated()) return { state: "resolved_none" };

  const btn = GC.byText("a,button,input", /^\s*show me\s*$/i).find(GC.visible);
  if (!btn) return { state: "not_offered" };

  const before = document.querySelectorAll("span.segment > span.name a[data-profile-id]").length;
  btn.click();

  const settled = () => {
    const t = document.body ? document.body.innerText : "";
    if (/no in-law relationship was found/i.test(t)) return true;
    return document.querySelectorAll("span.segment > span.name a[data-profile-id]").length > before;
  };
  await GC.until(settled, job.waitMs || 600000);

  const t = document.body ? document.body.innerText : "";
  if (/no in-law relationship was found/i.test(t)) return { state: "resolved_none" };

  const show = GC.byText("a", /show short path/i).find(GC.visible);
  if (show) {
    show.click();
    await GC.until(
      () => document.querySelectorAll("span.segment > span.name a[data-profile-id]").length > 0,
      20000);
  }

  const links = GC.parsePath();
  const ids = links.map((l) => l.geni_id);
  const hasTarget = ids.includes(id);
  const description = GC.relationDescription();
  if (!hasTarget || links.length < 3) return { state: "unresolved", steps: links.length };

  const header = [
    "# Geni relationship path to " + (job.label || id) + " (IN-LAW)",
    "#",
    "# GENERATED by the geni collector extension from " + location.href + ".",
    "# Do not hand-edit: re-run the collector instead.",
    "#",
    "# AN IN-LAW PATH COUNTS. In-law connections are just as valid,",
    "# blood is not required. Geni was asked for the blood path first, said no, and this",
    "# is the answer to the second question. The step words carry `her husband` and",
    "# `his wife` but nothing marks the path as a whole; Geni prose below is the only",
    "# place that is stated, which is CLAUDE.md section Grab the RESIDUALS.",
    "#",
    "# Geni own prose summary, kept because the per-step relation words drop what it",
    "# keeps --- half-siblings above all, which no step word states:",
    "# " + description
  ].join("\n");

  return {
    state: "resolved_path", steps: links.length, hasTarget: true, description: description,
    filename: id + "-inlaw.tsv", tsv: GC.toTsv(links, header)
  };
};

/* One target, start to finish. Resolves with a verdict the background stores; it never decides
 * what the hit RATE is, which stays with `harvest-isolate-paths.py` over the saved files. */
GC.runPath = async function (job) {
  if (GC.blocked()) return { job: "path", geni_id: String(job.geni_id), state: "blocked" };
  const id = String(job.geni_id);
  const kind = job.kind || "blood";
  const report = (extra) => Object.assign({
    job: "path", geni_id: id, kind: kind, url: location.href
  }, extra);

  /* Wait for the page to actually be a profile. A capture taken before the relationship box
   * exists saves a page with no path on it, which reads as a miss rather than as an error. */
  await GC.until(() => GC.pathState().state !== "unknown", 25000);

  let st = GC.pathState();
  const stats = await GC.statistics();

  /* NOT REQUESTED -> ask. This is the click the whole two-pass campaign turns on, and the
   * button vanishing is the confirmation that it took. */
  let requested = false;
  if (st.state === "not_requested") {
    const btn = GC.byText("a,button,input", /how are (they|you) related/i).find(GC.visible);
    if (btn) {
      btn.click();
      requested = true;
      await GC.until(() => {
        const s = GC.pathState();
        return s.state !== "not_requested";
      }, 15000);
      st = GC.pathState();
    }
  }

  /* RUNNING -> wait it out in place. It might take ten minutes, and the tab must stay open:
   * closing it drops Geni's promise to notify. `waitMs` is the caller's budget. */
  if (st.state === "running") {
    await GC.until(() => {
      const s = GC.pathState();
      return s.state === "resolved_path" || s.state === "resolved_none";
    }, job.waitMs || 600000);
    st = GC.pathState();
  }

  if (st.state === "resolved_none") {
    return report({ state: "resolved_none", steps: 0, hasTarget: false,
                    requested, stats, description: GC.relationDescription() });
  }

  /* ⛔ A STATED MISS BEATS A RENDERED CHAIN, because the chain may belong to the OTHER search.
   *
   * Geni answers the blood question and the other-ways question into the SAME panel, and they do
   * not land together. `pathState` tests the miss sentence first, so the order it happens to
   * sample in decides the answer: if the in-law chain renders before the blood-miss sentence
   * does, `segs > 0 && rd` matches and the in-law chain is returned as the BLOOD result.
   *
   * Measured 2026-09-08 on Ellen Christensdatter Thrane `309763264470008240`. Her page states
   * *"No blood relationship was found."* in words, and the run produced `resolved_path` with a
   * 29-step chain -- so `runInLaw` then found the same chain again and `individual.js` scored her
   * `via = "both"`, one chain counted twice. Her `path_tsv` and `inlaw_tsv` came back
   * byte-identical, which is what made it visible. Written out she would have carried
   * `path_found=yes, via=both` and a "blood" path file that is not a blood path.
   *
   * The repo's asymmetry rule is what settles it: a MISS is stated on the page in words and is
   * readable; a HIT is an inference from what happens to be displayed. So when Geni has said no
   * to *this* question, that sentence wins, whatever is on screen. Only the blood-miss sentences
   * count here -- the in-law one answers a different question and is `runInLaw`'s to read. */
  const deniedHere = GC.byText(
    "*", /no blood relationship was found|the relationship could not be found|no path found to/i)
    .filter((e) => e.children.length === 0).some(GC.visible);
  if (deniedHere) {
    return report({ state: "resolved_none", steps: 0, hasTarget: false,
                    requested, stats, description: GC.relationDescription() });
  }
  if (st.state !== "resolved_path") {
    /* Still running, or never had a panel. Both are "come back later", never a miss -- the
     * distinction the harvester's `pending()` and `not_requested()` now keep apart. */
    return report({ state: st.state, steps: st.segs, hasTarget: false, requested, stats,
                    description: GC.relationDescription() });
  }

  /* RESOLVED WITH A CHAIN. "Show short path" is clicked because the chain can be collapsed;
   * where it is already expanded the click is harmless. */
  const show = GC.byText("a", /show short path/i).find(GC.visible);
  if (show) {
    show.click();
    await GC.until(
      () => document.querySelectorAll("span.segment > span.name a[data-profile-id]").length > 0,
      20000);
  }

  const links = GC.parsePath();
  const ids = links.map((l) => l.geni_id);
  const description = GC.relationDescription();

  /* THE GUARD THAT MATTERS. A miss page renders a full chain -- the VIEWER's own -- so the step
   * count alone scores every miss as a hit. The target's own id must be ON the chain. */
  const hasTarget = ids.includes(id);

  /* ⛔ THE PAGE IS NOT SAVED. Pages are not saved by the collector.
   * The chain is parsed here, in the page, where the markup is -- so what leaves this tab is the
   * finished path TSV, and the agent writes it into `paths/`. `geni-paths/*.html` is the earlier
   * page-saving form and stays as the six captures it already holds, not as a destination. */
  let tsv = "";
  if (hasTarget && links.length >= 3) {
    const header = [
      "# Geni relationship path to " + (job.label || id) + " (" + kind + ")",
      "#",
      "# GENERATED by the geni collector extension from " + location.href + ".",
      "# Do not hand-edit: re-run the collector instead.",
      "#",
      "# Geni's own prose summary, kept because the per-step relation words drop what it",
      "# keeps --- half-siblings above all, which no step word states:",
      "# " + description
    ].join("\n");
    tsv = GC.toTsv(links, header);
  }

  return report({
    state: "resolved_path", steps: links.length, hasTarget, requested, stats, description,
    first: ids[0] || "", last: ids[ids.length - 1] || "",
    filename: id + "-" + kind + ".tsv", tsv: tsv
  });
};
