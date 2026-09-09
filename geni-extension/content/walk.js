/* ONE PERSON OF THE PARENT WALK. The queue is not here and must never be.
 *
 * **Emma, 2026-09-09, stating the design after watching it fail:** *"the extension's supposed
 * to do all of the work on its own. You should never be able to see the queue at all."* And:
 * *"There is nothing agentic in there at all. There's nothing agentic except for the fact that
 * it's your job to open up the page and call the extension."*
 *
 * Refined the same day: *"the extension opens up the tabs, but it saves the queue … The tab is
 * always actually open, and the extension navigates through the tabs all the time. There could
 * be parallel stuff, but the parallel stuff is just for waiting on the path exports."*
 *
 * ## ⛔ WHAT WENT WRONG, because this file exists to stop it recurring
 *
 * `runSeed` does ONE person. Meeting somebody with both parents recorded it returned
 * `both_present` with an `enqueue` list, and `individual.js` handed that list OUT of the
 * extension as `out.walk_queue` for the agent to walk. That put the walk state in the agent --
 * and on the first real run the agent took `enqueue[0]` at each step and threw the rest away,
 * which is not a queue walk but a single-line climb.
 *
 * Søren Hansen Hiuler `373218413260013352` is the case. His queue was `[mother Malene, father
 * Hans]`, and the FATHER had an open mother slot one step up. The agent took the mother,
 * discarded the father, and climbed eight generations up a Danish line recorded continuously to
 * 1561 without finding a slot. `871b3968` is where it entered: `runIndividual` had been
 * reporting `seed_failed` on the first `both_present`, and the fix stopped at handing the queue
 * to the agent instead of implementing the traversal.
 *
 * Her reading, and the history bears it out -- `runSeed` has no loop and nothing in
 * `content/` ever navigated: *"you tried to make this happen, then it failed, and then you
 * decided to make it somewhat agentic without telling me, and then created a point of failure."*
 *
 * ## The split, and it is the whole point of this file
 *
 *     background.js   owns the QUEUE, opens and navigates the TABS, paces with chrome.alarms
 *     this file       does ONE person on the page it is on, and returns a verdict
 *     the agent       opens a page from the repository's list and calls the extension. Nothing else.
 *
 * So there is no `location.href` here and no queue here. `stepHere()` is a pure verdict: who
 * are this person's parents, and can a parent be created on them?
 *
 * ## Why the queue lives in the BACKGROUND rather than in a content script
 *
 * Every navigation destroys the content script, so a queue held here would have to be
 * re-serialised on every step and would be lost the moment a page failed to load. The
 * background worker already opens tabs (`chrome.tabs.create({ active: false })`) and already
 * paces itself with `chrome.alarms` -- carrying a comment about the exact hazard Emma raised,
 * that the worker is torn down and *"a pending `setTimeout` dies with it"*. An inactive tab
 * throttles timers the same way, which is why the waiting is the background's job and not this
 * file's.
 *
 * ## The algorithm the background runs, dictated
 *
 *     queue = [subject]
 *     pop the front  ->  stepHere() on that person's page
 *       can_create        ->  create the parent, THROW THE QUEUE AWAY,
 *                             request the Forest export from the parent, clear the subject
 *       both_present      ->  push the MOTHER, then the FATHER, carry on
 *
 * Breadth-first, mother before father -- rule 4 of `docs/parent-walk-algorithm.md`.
 */

GC.walk = {
  /* The one thing a content script can answer: what is true of the person on THIS page.
   *
   * Returns `{ state, enqueue }` and nothing else that resembles a walk. `state` is `runSeed`'s
   * own verdict, so the decision stays in `seed.js` where it already lives and is not restated
   * here -- two copies of a rule is how `via` came to mean two different things.
   */
  async stepHere(geni_id) {
    const seed = await GC.runSeed({ geni_id: geni_id });
    return {
      job: "walk_step",
      geni_id: String(geni_id),
      state: seed.state,
      /* mother then father, already ordered by `runSeed` */
      enqueue: (seed.enqueue || []).map(String),
      created: seed.state === "added" ? seed.pid : null,
      name: seed.name || "",
      seed: seed,
    };
  },
};
