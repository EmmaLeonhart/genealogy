/* THE RUN LOOP. One job per individual, and every decision inside it.
 *
 * **THERE IS NO DISCRETION AT THE AGENT'S END AT ALL** -- said three times when this was
 * dictated. `docs/collector-run-loop.md` is that dictation. The agent lands on the profile;
 * everything after that is decided here, the same way every time.
 *
 *     scrape the family            -> tiny profile GEDCOM material, produced immediately
 *     request the Charlemagne path
 *     WAIT on a watcher            <- not a timer
 *     path found -> expand, grab the chain, hand back the path TSV
 *     no path    -> read the statistics; below the floor stop; at or above it walk the tree,
 *                   add the individual, run the Forest export, flag them as an export target
 *
 * **What this replaces is me.** Every step already existed as a job -- `runFamily`, `runPath`,
 * `runSeed`, `runExport` -- and I dispatched them one at a time and reasoned about the result
 * between calls. The gate lived in `scripts/export_gate.py` and I applied it in prose, per person.
 * That reasoning is the discretion that was removed; it is one rule here, applied identically.
 *
 * ⛔ **THE THRESHOLD IS 300, ON ANY FIGURE** -- the common threshold for whether the relatives
 * numbers make a person worth doing. It
 * replaced five per-figure numbers that were mine. Disjunctive: the figures measure different
 * things and a person can be evidently connected by any of them.
 *
 * ⛔ **AND THE AGENT'S NAVIGATION IS THE CAPTCHA MITIGATION, NOT OVERHEAD.** *"By agentically
 * going to the page and then running the extension, you are considered to be proper traffic."* So
 * this job never fetches a profile itself; it works on the page it is already on. Geni served an
 * Incapsula CAPTCHA earlier today after roughly forty rapid loads, which is what the alternative
 * costs.
 */

GC.individual = {};

/** The statistics floor, and the one rule that reads it. */
GC.individual.FLOOR = 300;

GC.individual.gate = function (stats) {
  const figures = ["family_tree", "blood_relatives", "ancestors", "descendants", "followers"];
  const read = {};
  const cleared = [];
  for (const f of figures) {
    read[f] = parseInt((stats || {})[f], 10) || 0;
    if (read[f] >= GC.individual.FLOOR) cleared.push(f);
  }
  return { export_worth_it: cleared.length > 0, cleared: cleared, read: read };
};

GC.runIndividual = async function (job) {
  const id = String(job.geni_id);
  const out = { job: "individual", geni_id: id, steps: [] };
  const step = (s) => { out.steps.push(s); document.documentElement.dataset.geniCollectorStep = s; };

  if (GC.blocked()) { out.state = "blocked"; return out; }

  /* 1. The family, always, and first. It is the cheap unconditional step: no search requested,
   *    no export spent, nothing created -- and the page load it needs has already happened. */
  step("family");
  const fam = await GC.runFamily({ geni_id: id, dryRun: true });
  out.name = fam.name;
  out.stats = fam.stats;
  out.relatives = fam.relatives;
  out.family_tsv = fam.tsv;
  out.family_filename = fam.filename;

  /* 2-4. The path: request it and WAIT on the page rather than on a clock. `runPath` already
   *      distinguishes not-requested, running, resolved-with-chain and resolved-with-nothing,
   *      and clicks "Show short path" itself, which is step 5a's expand. */
  step("path");
  /* ⛔ `waitMs` IS THE CALLER'S BUDGET AND WAS UNREACHABLE THROUGH THIS JOB.
   * `runPath` has documented it as the caller's budget since it was written, and this
   * function never passed one -- so every individual run takes the 600000 default whatever
   * the caller asks for. `CLAUDE.md` § *Code that is WRITTEN but never CALLED is not done*.
   *
   * ⛔ AND THE DEFAULT STAYS 600000, because the figure for a real search is ten minutes and
   * a capped wait turns a slow HIT into a deferral. This makes the knob reachable and moves
   * no behaviour: `job.waitMs` is undefined unless a caller sets it.
   *
   * ⛔ DO NOT CAP IT ON THE STRENGTH OF A SNAPSHOT. Five targets were read mid-run on
   * 2026-09-06 as having no relationship panel at all -- no `path_search_response`, no
   * button, no segments -- which reads exactly like a search that has died. All five then
   * resolved normally to a miss banner. The panel is simply absent between the request and
   * the answer, so a single observation of `no_panel` is not evidence of anything. */
  const path = await GC.runPath({ geni_id: id, kind: job.kind || "blood",
                                  waitMs: job.waitMs });
  out.path_state = path.state;
  out.path_steps = path.steps;
  out.path_has_target = path.hasTarget;
  out.path_tsv = path.tsv;
  out.path_filename = path.filename;
  out.description = path.description;

  /* ⛔ 5. BOTH TIES, ALWAYS. Not in-law-as-fallback.
   *
   * **BOTH SEARCHES, ALWAYS.** When a blood relationship is requested the non-blood other ways
   * are requested too, and where no blood relationship is found the other ways are still looked
   * at. And the reason, which is why this is not waste: *"The redundancy here is the
   * point ... the kind of 'ring' of the person to charlemange with the blood and non-blood gives
   * a maximum amount of relatives to go through for a minimal cost of just clicking the button
   * twice and waiting."*
   *
   * The goal for a person is a RING -- a blood chain to Charlemagne, a marriage chain to
   * Charlemagne, and the immediate family -- so the second search runs even when the first
   * succeeded. The first version of this ran in-law only after a blood miss, which is the
   * fallback reading that was corrected.
   *
   * ⛔ WHAT IS NOT DONE HERE IS THE BACKFILL. *"I do not care about non-blood relationships
   * among people already connected ... These first people covered just get worse coverage and
   * that is life."* That is about not RE-RUNNING the twelve who already resolved; it does not
   * make the second search optional on a person the loop is visiting now. */
  step("inlaw");
  const inlaw = await GC.runInLaw({ geni_id: id, label: job.label, waitMs: job.waitMs });
  out.inlaw_state = inlaw.state;
  out.inlaw_steps = inlaw.steps;
  out.inlaw_tsv = inlaw.tsv;
  out.inlaw_filename = inlaw.filename;
  out.inlaw_description = inlaw.description;

  const bloodHit = path.state === "resolved_path" && path.hasTarget;
  const inlawHit = inlaw.state === "resolved_path";
  /* ⛔ `neither` IS A VERDICT AND MUST BE WRITTEN. A blank `via` means *not asked*, and
   * `scripts/collector-worklist.py` re-queues on exactly that -- so a person who genuinely
   * misses BOTH searches would return to the pool forever unless the second miss is recorded.
   * The distinction is the same one `read` draws for the statistics block: unmeasured is not
   * the same fact as measured-and-empty. */
  const asked = inlaw.state === "resolved_path" || inlaw.state === "resolved_none";
  out.via = bloodHit && inlawHit ? "both"
          : bloodHit ? "blood"
          : inlawHit ? "inlaw"
          : (path.state === "resolved_none" && asked) ? "neither" : "";

  if (bloodHit || inlawHit) {
    out.state = bloodHit && inlawHit ? "path_found_both"
              : bloodHit ? "path_found" : "path_found_inlaw";
    out.export_decision = "not needed -- " + out.via + " resolved";
    return out;
  }

  if (path.state !== "resolved_none") {
    /* The BLOOD search never resolved -- still running, or never asked. NOT a miss: a requested
     * search decays back to unrequested, so this person is revisited rather than written off. */
    out.state = path.state;
    out.export_decision = "deferred -- the blood search has not resolved";
    return out;
  }

  /* 5b. A real miss on BOTH questions. The statistics decide, and they decide here rather
   *     than in a report. */
  step("gate");
  const gate = GC.individual.gate(fam.stats);
  out.gate = gate;
  if (!gate.export_worth_it) {
    out.state = "miss_below_floor";
    out.export_decision = "no export -- no figure reaches " + GC.individual.FLOOR;
    return out;
  }

  /* At or above the floor a miss is a database failure rather than a real negative -- the rule:
   * *"15,000 blood relatives or really any of these numbers being high on this scale indicates
   * that they are in the world tree but it was a database failure."* So walk up for an open slot,
   * create one ancestor, and export from it. */
  out.state = "miss_export_warranted";
  out.export_decision = "export -- cleared by " + gate.cleared.join(", ");
  if (!job.create) {
    /* The creation and the export are live-site writes. They run when the caller asks for them,
     * which is how a first run is observed before 2,527 of them are not. */
    out.export_decision += " (not run: job.create was not set)";
    return out;
  }

  /* ⛔ `both_present` IS THE WALK CONTINUING, NOT A FAILURE.
   *
   * `docs/parent-walk-algorithm.md` rule 4, as dictated: *"both present -> add neither;
   * enqueue the mother, THEN the father, and carry on up."* `runSeed` does ONE person and hands
   * back that queue; walking it needs a page load per step, and a page load is the agent's job
   * because agentic navigation is the CAPTCHA mitigation. So the job cannot finish the walk on
   * its own and must say so rather than reporting the first person as a dead end.
   *
   * Anna Hørlück `297536201290008921` is the case: two parents recorded, `enqueue` =
   * [mother, father], and the first version of this line called it `seed_failed` and returned --
   * which reads as *the export is impossible* when the walk had not started. */
  step("seed");
  const seed = await GC.runSeed({ geni_id: id });
  out.seed = seed;
  if (seed.state === "both_present" || seed.state === "enqueued") {
    /* ⛔ **THE QUEUE DOES NOT LEAVE THE EXTENSION.** Emma, 2026-09-09: *"the extension's
     * supposed to do all of the work on its own. You should never be able to see the queue at
     * all."*
     *
     * This used to set `out.walk_queue = seed.enqueue` and return, which handed the walk to the
     * agent -- and on the first real run the agent took `enqueue[0]` each step and discarded the
     * rest, climbing eight generations up one line while the open slot sat second in the very
     * first queue. `content/walk.js` has the full account.
     *
     * The walk is the BACKGROUND's job now: it owns the queue, opens the tabs and paces itself
     * with `chrome.alarms`, calling `GC.walk.stepHere` once per page. All this returns is the
     * fact that a walk is needed and where it starts -- one id, not a list to be managed. */
    out.state = "seed_walk";
    out.walk_from = id;
    out.export_decision += " -- walk needed, from " + id;
    return out;
  }
  if (seed.state !== "added") { out.state = "seed_failed"; return out; }

  step("export");
  out.export = await GC.runExport({ geni_id: seed.pid || id, walk: "forest" });
  out.state = "exported";
  return out;
};
