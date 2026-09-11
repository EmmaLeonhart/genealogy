/* A random walk DOWN the tree, so the extension chooses the person and the agent does not.
 *
 * Ruled 2026-09-10: *"we are supposed to be doing this algorithmically with the Chrome extension
 * selecting a person ... a random descendant of the person and then just going there."*
 *
 * ⛔ **THIS EXISTS BECAUSE THE SELECTION WAS BEING DONE BY HAND.** The Monte Carlo round earlier
 * today drew ids out of a GEDCOM in Python and navigated to each one by typing the URL. That is
 * the discretion `docs/collector-run-loop.md` removes in its first line — *"the agent navigates
 * and nothing else"* — and it also drew from a ball on disk rather than from Geni, so it could
 * only ever sample people some earlier export already held.
 *
 * **One step per page load, and the background owns the sequence.** The job reads the card grid,
 * picks ONE child uniformly at random, and returns its id; the background enqueues that as the
 * next `descend` job and the walk continues on the next page. A person with no children ends the
 * walk and is the person landed on.
 *
 * ⛔ **NO GENERATION TARGET, AND THE DEPTH IS NOT A MEASURE OF ANYTHING.** Ruled the same day:
 * *"generation counts shouldn't actually matter in this algorithm because they do not necessarily
 * indicate that somebody's on the frontier because of the ball shape."* `steps` exists only to
 * stop an unbounded walk on a cyclic or very deep line; it is a safety limit, not a parameter of
 * the method, and nothing downstream reads it as depth.
 */

GC.descend = {};

/* The children on this page, from the card grid `GC.family.scrape` already reads. Using the same
 * reader is the point: one place knows what a relation label means, so the walk cannot disagree
 * with the scrape about who somebody's child is. */
GC.descend.children = async function () {
  const scraped = await GC.family.scrape();
  return (scraped.relatives || []).filter((r) => r.relation === "child");
};

GC.runDescend = async function (job) {
  const id = String(job.geni_id || "");
  /* ⛔ WAIT, like everything else that reads this site. Geni serves base HTML and fills the page
   * in afterwards; `GC.family.scrape` carries the wait and the reasoning. */
  if (GC.blocked()) return { job: "descend", geni_id: id, state: "blocked" };

  const kids = await GC.descend.children();
  const step = (job.step | 0) + 1;
  const limit = job.steps ? (job.steps | 0) : 40;

  if (!kids.length || step >= limit) {
    /* The walk has landed. The census read is what decides whether this person is worth an
     * export, and it is the only measure the campaign accepts -- `descendants` against the
     * threshold, read off the real profile rather than inferred from a merged GEDCOM. */
    const stats = await GC.statistics();
    return {
      job: "descend", geni_id: id, state: "landed", step: step,
      why: kids.length ? "step_limit" : "no_children",
      name: ((document.querySelector("h1") || {}).textContent || "").trim(),
      stats: stats, url: location.href
    };
  }

  const pick = kids[Math.floor(Math.random() * kids.length)];
  return {
    job: "descend", geni_id: id, state: "descend_next", step: step,
    next_id: String(pick.geni_id), next_name: pick.name || "",
    children_seen: kids.length, url: location.href
  };
};
