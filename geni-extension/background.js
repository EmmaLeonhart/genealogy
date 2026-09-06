/* The scheduler. Holds the queue, opens tabs, paces them, keeps the results.
 *
 * Two pacing rules, and they are different in kind:
 *
 *  - **Exports run one at a time and that is GENI's limit**, not a setting. Emma, 2026-08-18:
 *    *"There's no way that you can do an export concurrently. That isn't my decision thats
 *    geni."* `EXPORT_CONCURRENCY` is 1 and is deliberately not exposed in the popup, because a
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
  concurrency: 6,
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

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
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

      /* ⛔ `addAncestor(start_id)` ADDS ONE ANCESTOR AND RETURNS ITS ID. Emma, 2026-09-05:
       * *"this is not an unbound method... it runs like addAncestor(start_id); and then it adds
       * an ancestor of start_id and returns the id of it as end_id and then a subsequent method
       * will use end_id, generally doing a forest export, or descendants export."*
       *
       * So a creation ENDS the walk. Climbing exists only to find an open slot; once one person
       * is created there is an `end_id` and the next step is an export from it, not more
       * ancestors. Left running, every created `NN` has no parents of its own and becomes a
       * candidate for its own `NN` mother -- an unbounded chain of invented people on a live
       * site. That was the shape of it before she ruled.
       *
       * The remaining seed jobs are dropped rather than kept: they were the search for a slot,
       * and the slot has been found. */
      if (msg.result && msg.result.state === "added") {
        queue = s.queue.filter((q) => q.job !== "seed");
        await put({ active, results, queue, endId: msg.result.pid || "" });
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
       * thing her rule protects; once the answer is on the page the tab costs RAM and buys
       * nothing. A still-running or never-asked target is closed too and goes to the next
       * pass -- that is what makes this a two-pass campaign rather than an unbounded wait. */
      try { await chrome.tabs.remove(tabId); } catch (e) {}
      sendResponse(true);
      pump();
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
    if (msg.type === "load") {
      await put({ queue: msg.queue, results: [], active: {} });
      sendResponse(msg.queue.length);
      return;
    }
    sendResponse(null);
  })();
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
