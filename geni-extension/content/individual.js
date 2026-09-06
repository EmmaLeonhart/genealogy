/* THE RUN LOOP. One job per individual, and every decision inside it.
 *
 * **Emma, 2026-09-06, dictating it and saying this three times: "There's no discretion on your
 * part at all."** `docs/collector-run-loop.md` is the dictation. The agent lands on the profile;
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
 * That reasoning is the discretion she removed; it is one rule here, applied identically.
 *
 * ⛔ **THE THRESHOLD IS 300, ON ANY FIGURE.** Emma: *"if the relatives numbers indicate that it
 * would be worthwhile based off of our common threshold there, I believe three hundred"*. It
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
  const path = await GC.runPath({ geni_id: id, kind: job.kind || "blood" });
  out.path_state = path.state;
  out.path_steps = path.steps;
  out.path_has_target = path.hasTarget;
  out.path_tsv = path.tsv;
  out.path_filename = path.filename;
  out.description = path.description;

  if (path.state === "resolved_path" && path.hasTarget) {
    /* 5a. Found. Both artifacts are in hand and nothing further is spent on this person. */
    out.state = "path_found";
    out.export_decision = "not needed -- the path resolved";
    return out;
  }

  if (path.state !== "resolved_none") {
    /* Still running, or never asked. NOT a miss -- a requested search decays back to
     * unrequested, so this person is revisited rather than being written off. */
    out.state = path.state;
    out.export_decision = "deferred -- the search has not resolved";
    return out;
  }

  /* 5b. A real miss. The statistics decide, and they decide here rather than in a report. */
  step("gate");
  const gate = GC.individual.gate(fam.stats);
  out.gate = gate;
  if (!gate.export_worth_it) {
    out.state = "miss_below_floor";
    out.export_decision = "no export -- no figure reaches " + GC.individual.FLOOR;
    return out;
  }

  /* At or above the floor a miss is a database failure rather than a real negative -- her rule:
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

  step("seed");
  const seed = await GC.runSeed({ geni_id: id });
  out.seed = seed;
  if (seed.state !== "added") { out.state = "seed_failed"; return out; }

  step("export");
  out.export = await GC.runExport({ geni_id: seed.pid || id, walk: "forest" });
  out.state = "exported";
  return out;
};
