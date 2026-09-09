/* The scheduler. Holds the queue, opens tabs, paces them, keeps the results.
 *
 * Two pacing rules, and they are different in kind:
 *
 *  - **Exports run one at a time and that is GENI's limit**, not a setting: there is no way to
 *    run an export concurrently, and that is Geni's constraint rather than a choice made here.
 *    `EXPORT_CONCURRENCY` is 1 and is deliberately not exposed in the popup, because a
 *    control implies a choice that does not exist.
 *  - **Path collection is bounded by RAM and by politeness**, both of which are ours. A tab
 *    must STAY OPEN while its search runs -- *"If you do not leave the tabs open then it
 *    actually messes a bit with the data that is given"*, and closing them *"drops its promise
 *    to notify you"* -- so concurrency is how many searches can be in flight at once, and the
 *    stagger is how fast new ones are asked for. `geni-scraping/` sets the rate at one a
 *    minute; that is the default here and the popup can change it.
 */

const EXPORT_CONCURRENCY = 1;
const PUMP_ALARM = "geni-collector-pump";

const DEFAULTS = {
  running: false,
  concurrency: 12,
  staggerMs: 60000,
  waitMs: 600000,
  dryRun: true,
  queue: [],
  active: {},
  results: [],
  startedAt: null,
  //: The id `addAncestor` returned: what the export runs from.
  endId: ""
};

async function state() {
  const s = await chrome.storage.local.get(Object.keys(DEFAULTS));
  return Object.assign({}, DEFAULTS, s);
}
async function put(patch) { await chrome.storage.local.set(patch); }

/* `active` maps tabId -> job. It is stored rather than held in a variable because an MV3
 * service worker is torn down whenever it is idle, which is most of the time while a ten-minute
 * search runs. Anything kept only in memory is gone by the time the answer arrives. */

/* ⛔ **A HANDLER THAT THROWS BEFORE `sendResponse` IS INVISIBLE, and that cost a restart cycle.**
 *
 * The listener returns `true` to keep the channel open, so the caller's promise stays pending
 * until the channel closes and then resolves `undefined` -- with no rejection and no
 * `lastError`. From the content script that is indistinguishable from a dead service worker, a
 * stale one, and a handler that simply has no case for the message. On 2026-09-09 all four were
 * guessed at in turn while the real fault was a throw somewhere above the reply.
 *
 * So every path answers. An error comes back AS the answer rather than as silence. */
chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  /* ⛔ **`ping` ANSWERS BEFORE ANY `await`, ON PURPOSE.** Everything below opens with
   * `await state()`, i.e. `chrome.storage.local.get`. If that ever hangs or rejects, the async
   * body never reaches `sendResponse`, the channel closes, and the caller's promise resolves
   * `undefined` with no rejection and no `lastError` -- which is indistinguishable from a dead
   * service worker and was read as one for most of an afternoon.
   *
   * A probe whose purpose is *is the worker alive* must therefore not depend on storage. This
   * one touches nothing. If `ping` answers and the others do not, the fault is storage, and
   * that is a diagnosis rather than another guess. */
  if (msg && msg.type === "ping") {
    sendResponse({ pong: chrome.runtime.getManifest().version, sync: true });
    return true;
  }
  (async () => {
    const s = await state();
    if (msg.type === "claim") {
      const job = s.active[String(sender.tab && sender.tab.id)];
      sendResponse(job || null);
      return;
    }
    if (msg.type === "result") {
      const tabId = sender.tab && sender.tab.id;
      const active = Object.assign({}, s.active);
      delete active[String(tabId)];
      const results = s.results.concat([Object.assign({ at: new Date().toISOString() }, msg.result)]);

      /* ⛔ THE ALGORITHM'S QUEUE, not ours. `docs/parent-walk-algorithm.md`: when both parents
       * already exist the walk adds neither and enqueues the MOTHER, then the FATHER, in that
       * order, and carries on up. The content script returns them already ordered; appending
       * keeps the walk breadth-first, which is what "going up going up" describes.
       *
       * Already-seen ids are dropped: pedigree collapse is dense in this tree, so the same
       * ancestor is reached down several lines and would otherwise be walked repeatedly. */
      let queue = s.queue;

      /* ⛔ `addAncestor(start_id)` ADDS ONE ANCESTOR AND RETURNS ITS ID. It is not an unbound
       * method: it runs as `addAncestor(start_id)`, adds an ancestor of `start_id`, and returns
       * that new id as `end_id`, which a subsequent method uses -- generally a Forest or a
       * Descendants export.
       *
       * So a creation ENDS the walk. Climbing exists only to find an open slot; once one person
       * is created there is an `end_id` and the next step is an export from it, not more
       * ancestors. Left running, every created `NN` has no parents of its own and becomes a
       * candidate for its own `NN` mother -- an unbounded chain of invented people on a live
       * site. That was the shape of it before that ruling.
       *
       * The remaining seed jobs are dropped rather than kept: they were the search for a slot,
       * and the slot has been found. */
      if (msg.result && msg.result.state === "added") {
        /* ⛔ **AND THE EXPORT IS REQUESTED FROM THE PARENT.** Emma, 2026-09-09: *"Once it has
         * created the parent, then the queue gets thrown out, and the export is requested from
         * the parent."* Both halves of that sentence, and only the first was here: `endId` was
         * SET and then read by nothing, so a walk that found its slot created the person and
         * stopped. The whole point of the climb is the export at the end of it. */
        const pid = msg.result.pid || "";
        queue = s.queue.filter((q) => q.job !== "seed");
        if (pid) {
          queue = queue.concat([{ job: "export", geni_id: String(pid), kind: "forest",
                                  walk: "forest", label: "created by the parent walk" }]);
        }
        await put({ active, results, queue, endId: pid });
        try { await chrome.tabs.remove(tabId); } catch (e) {}
        sendResponse(true);
        pump();
        return;
      }

      /* ⛔ **`seed_walk` IS WHERE THE CLIMB BEGINS.** `runIndividual` no longer hands out a
       * queue -- it returns `walk_from`, one id -- so the background turns that into the first
       * seed job and owns every step after it. Before this the individual job reported that a
       * walk was needed and nothing started one. */
      if (msg.result && msg.result.state === "seed_walk" && msg.result.walk_from) {
        const from = String(msg.result.walk_from);
        const held = new Set(s.queue.map((q) => String(q.geni_id)));
        if (!held.has(from)) {
          queue = s.queue.concat([{ job: "seed", geni_id: from, kind: "seed", label: "" }]);
        }
        await put({ active, results, queue });
        try { await chrome.tabs.remove(tabId); } catch (e) {}
        sendResponse(true);
        pump();
        return;
      }

      const add = (msg.result && msg.result.enqueue) || [];
      if (add.length) {
        const seen = new Set(s.results.map((r) => String(r.geni_id))
          .concat(s.queue.map((q) => String(q.geni_id)))
          .concat([String(msg.result.geni_id)]));
        const fresh = add.filter((p) => p && !seen.has(String(p)))
                         .map((p) => ({ job: "seed", geni_id: String(p), kind: "seed", label: "" }));
        queue = s.queue.concat(fresh);
      }
      await put({ active, results, queue });
      /* A resolved tab is closed. It is held open only WHILE the search runs, which is the
       * thing the rule protects; once the answer is on the page the tab costs RAM and buys
       * nothing. A still-running or never-asked target is closed too and goes to the next
       * pass -- that is what makes this a two-pass campaign rather than an unbounded wait. */
      try { await chrome.tabs.remove(tabId); } catch (e) {}
      sendResponse(true);
      pump();
      return;
    }
    /* A probe with no purpose but to answer. If `ping` comes back null the running service
     * worker predates this line, whatever the content scripts report -- they reload on a browser
     * restart and the worker does not, which is the distinction that cost a day. */
    /* ⛔ **REPORT THE MANIFEST VERSION, NOT A LITERAL.** This answered `"1.4.2"` -- a hardcoded
     * string, like the one in `common.js` that claimed 1.6.4 for four releases and was believed.
     * A probe whose job is to reveal a stale worker must not itself be a stale literal. */
    if (msg.type === "ping") {
      sendResponse({ pong: chrome.runtime.getManifest().version, keys: Object.keys(s).length });
      return;
    }
    if (msg.type === "status") { sendResponse(s); return; }
    if (msg.type === "start") {
      await put({ running: true, startedAt: new Date().toISOString() });
      sendResponse(true);
      pump();
      return;
    }
    if (msg.type === "stop") {
      /* Stops opening NEW tabs. It does not and cannot cancel an export already submitted --
       * Geni has no such operation, and offering one would be fiction. */
      await put({ running: false });
      sendResponse(true);
      return;
    }
    /* ⛔ **THE ENTRY POINT THE AGENT CAN REACH.** The popup is browser chrome and
     * `chrome-extension://` URLs are refused the same way `chrome://` ones are, so the popup's
     * load/start pair cannot be driven from the automation surface. Without this the whole
     * background driver -- queue, tabs, pacing, the walk -- was unreachable, and every run went
     * down the DOM-trigger path instead, which has no queue at all. That is why the walk looked
     * unimplemented when it was merely unreachable.
     *
     * One individual in, the full operation out: scrape, path, gate, climb, create, export.
     * Emma, 2026-09-09: *"it's your job to open up the page and call the extension"*, and
     * nothing else. */
    if (msg.type === "walk") {
      const id = String(msg.geni_id || "");
      if (!id) { sendResponse({ error: "no geni_id" }); return; }
      await put({
        queue: [{ job: "individual", geni_id: id, kind: "individual",
                  create: true, label: msg.label || "" }],
        results: [], active: {}, endId: "", dryRun: false,
        running: true, startedAt: new Date().toISOString()
      });
      sendResponse({ started: id });
      pump();
      return;
    }
    if (msg.type === "load") {
      await put({ queue: msg.queue, results: [], active: {} });
      sendResponse(msg.queue.length);
      return;
    }
    sendResponse(null);
  })().catch((e) => {
    try {
      sendResponse({ error: String((e && e.stack) || (e && e.message) || e),
                     failedOn: msg && msg.type });
    } catch (_) { /* the channel is already gone; nothing left to say */ }
  });
  return true;
});

let pumping = false;

async function pump() {
  if (pumping) return;
  pumping = true;
  try {
    for (;;) {
      const s = await state();
      if (!s.running) break;
      const active = Object.assign({}, s.active);
      const inFlight = Object.keys(active).length;
      const next = (s.queue || [])[0];
      if (!next) {
        if (inFlight === 0) await put({ running: false });
        break;
      }
      const limit = next.job === "export" ? EXPORT_CONCURRENCY : s.concurrency;
      if (inFlight >= limit) break;

      const queue = s.queue.slice(1);
      const job = Object.assign({ jobId: next.geni_id + ":" + (next.kind || next.job),
                                  waitMs: s.waitMs, dryRun: s.dryRun }, next);
      const url = next.job === "export"
        ? "https://www.geni.com/gedcom/export/" + next.geni_id
        : "https://www.geni.com/people/x/" + next.geni_id;
      const tab = await chrome.tabs.create({ url, active: false });
      active[String(tab.id)] = job;
      await put({ queue, active });

      /* The stagger is the rate. It is between OPENS, so a slow search does not make the next
       * request come sooner -- politeness is about how often we ask, not how fast we finish.
       *
       * ⛔ IT IS SCHEDULED, NOT SLEPT. An MV3 service worker is torn down when it goes idle,
       * and a pending `setTimeout` dies with it -- so a plain sleep here stops a 100-target run
       * dead somewhere in the middle and looks exactly like a run that finished. `chrome.alarms`
       * survives the teardown; the `setTimeout` stays as the precise path for the case where the
       * worker happens to still be alive, because Chrome clamps alarms to 30s. Whichever fires
       * first wins, and a double fire is harmless: `pumping` and the re-read of the queue mean
       * the second one finds the work already taken. */
      chrome.alarms.create(PUMP_ALARM, { when: Date.now() + Math.max(1000, s.staggerMs) });
      setTimeout(pump, s.staggerMs);
      break;
    }
  } finally {
    pumping = false;
  }
}

chrome.alarms.onAlarm.addListener((a) => { if (a.name === PUMP_ALARM) pump(); });

/* A run interrupted by a browser restart resumes rather than stalling silently. */
chrome.runtime.onStartup.addListener(() => pump());

/* A tab the user closes by hand releases its slot rather than wedging the queue. */
chrome.tabs.onRemoved.addListener(async (tabId) => {
  const s = await state();
  if (!s.active[String(tabId)]) return;
  const active = Object.assign({}, s.active);
  const job = active[String(tabId)];
  delete active[String(tabId)];
  await put({
    active,
    results: s.results.concat([{ at: new Date().toISOString(), job: job.job,
                                 geni_id: job.geni_id, kind: job.kind, state: "tab_closed" }])
  });
  pump();
});
