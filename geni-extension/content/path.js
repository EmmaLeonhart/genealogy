/* The relationship-path job: request the search, wait for it, capture, parse.
 *
 * This is the pilot's instrument and, if the hit rate justifies it, the 185,327-target
 * campaign's. What it replaces is an agent taking one sampled snapshot per tool call at 10-20
 * seconds each -- `geni-paths/README.md` says the design must MINIMISE observations because
 * that channel is the one that lies. Here there is no sampling: a MutationObserver fires on the
 * mutation that resolves the search.
 *
 * THE PUSHPIN IS NEVER TOUCHED. Emma, 2026-09-03: *"You do not pin Charlemagne, it needs to be
 * done exactly once and I did it."* Toggling it mid-run re-anchors every later search to "You".
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

  /* RUNNING -> wait it out in place. Emma: it *"might take 10 minutes"*, and the tab must stay
   * open -- closing it *"drops its promise to notify you"*. `waitMs` is the caller's budget. */
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

  /* ⛔ THE PAGE IS NOT SAVED. Emma, 2026-09-06: *"we are not supposed to be saving pages lol"*.
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
