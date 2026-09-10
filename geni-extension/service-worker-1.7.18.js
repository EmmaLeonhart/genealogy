/* ⛔⛔ **THE FILENAME CARRIES THE VERSION, AND IT MUST BE RENAMED ON EVERY EDIT TO THIS FILE.**
 *
 * `background.js` -> `service-worker.js` -> `service-worker-<version>.js`. The second rename was
 * a one-off to break a stale cache; this is the same lever made routine, because the staleness
 * is not a one-off and **bumping the manifest version does not touch it**.
 *
 * Measured 2026-09-10, which is what turned the one-off into a rule. `manifest.json` went
 * 1.6.9 -> 1.7.0 -> 1.7.1 and Chrome was fully restarted between each:
 *
 *     data-geni-collector          1.7.1   the CONTENT scripts reloaded off disk
 *     ping -> pong                 1.7.1   `getManifest().version`, so it reads the MANIFEST
 *     swBootedAt                   fresh   the worker really did boot
 *     status -> the new `exportWalk` key   ABSENT -- the worker was running the OLD BYTES
 *
 * So three of the four instruments agreed on 1.7.1 and all three were reading something other
 * than this file's contents. **A version number is never evidence about the script**: only a
 * behaviour that only the new code has -- here a new key in `status` -- distinguishes them.
 * `CLAUDE.md` § *CHECK before raising an alarm*, in the direction nobody expects: the reassuring
 * reading was the wrong one.
 *
 * The `ScriptCache` is keyed on the script URL and nothing reachable from the automation surface
 * invalidates it -- `chrome://extensions` is refused, deleting the cache is refused, and
 * `--load-extension` is ignored. Changing the URL is the only lever left, so the URL is where
 * the version goes.
 *
 * **The routine, and skipping either half means the edit did not happen:**
 *
 *     1. rename this file to the new version, and point `manifest.json` at the new name
 *     2. restart Chrome, then verify with a behaviour ONLY the new code has
 *
 * ---
 *
 * **THIS FILE WAS `background.js` AND WAS RENAMED TO BREAK A STALE SERVICE-WORKER CACHE.**
 *
 * 2026-09-09. The driver appeared dead for a whole afternoon: `sendMessage` from a content
 * script resolved `undefined`, with no rejection and no `lastError`, across four Chrome
 * restarts including one with `--load-extension`. Every hypothesis was wrong in turn -- a stale
 * extension, a dead worker, a throw before `sendResponse`, a hung `chrome.storage`.
 *
 * A boot beacon settled it: this file writes `swBootedAt` to `chrome.storage.local` at module
 * scope, and a content script can read that storage WITHOUT messaging. The beacon came back
 * empty, which means the file was never executing -- not that messages were being lost.
 *
 * The cause is on disk. `Default/Service Worker/ScriptCache` held a **7,132-byte** copy stamped
 * 15:12, against 12,190 bytes on disk: it contained `EXPORT_CONCURRENCY` but neither
 * `swBootedAt` nor the `walk` handler. Chrome had cached the worker and was still serving that
 * copy hours later.
 *
 * **Content scripts reload on a browser restart and the SERVICE WORKER DOES NOT** -- which is
 * why `data-geni-collector` went 1.6.4 -> 1.6.8 on cue while the worker stayed at 15:12, and why
 * restarting never helped. The cache is keyed on the SCRIPT URL, so bumping the manifest version
 * does not invalidate it either. Renaming the file changes the URL and forces a fresh
 * registration, which is the one lever reachable without `chrome://extensions`.
 *
 * If this ever recurs: read the beacon first. Absent means the file is not running, and the
 * ScriptCache is the next place to look, not the messaging.
 */
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

/* ⛔ **A BOOT BEACON, because "the worker never ran" and "the message never arrived" look
 * identical from a content script.** Both present as `sendMessage` resolving `undefined` with
 * no rejection and no `lastError`, and most of 2026-09-09 went on guessing between them.
 *
 * This writes to `chrome.storage.local` at module scope — the first thing the worker does, before
 * any listener is registered. A content script can read that storage directly, without sending
 * a message at all. So:
 *
 *     beacon present, ping unanswered  ->  the worker RUNS and messaging is broken
 *     beacon absent                    ->  the worker never executed this file
 *
 * It is two lines and it distinguishes the only two hypotheses left. */
try {
  chrome.storage.local.set({
    swBootedAt: new Date().toISOString(),
    swVersion: chrome.runtime.getManifest().version
  });
} catch (e) { /* nothing to do: if this throws, the beacon is absent and that is the signal */ }

const EXPORT_CONCURRENCY = 1;
const PUMP_ALARM = "geni-collector-pump";
/* How long the run holds off after Geni answers 429. Long enough to matter, short enough that
 * an overnight run recovers itself without anyone watching. */
const BLOCK_COOLDOWN_MS = 180000;

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
  endId: "",
  /* Set when Geni answers 429; `pump` opens nothing until it passes. */
  cooldownUntil: 0,
  /* Every id the extension has run on this run, whatever the outcome. See the result handler. */
  attempted: [],
  /* ⛔ THE WALK THE EXPORT AT THE END OF THE CLIMB TAKES. `forest` is the default and stays it
   * -- `docs/export-seed-rules.md` fixes a seed-driven export at Forest/5000 and that file is
   * still the authority for the ordinary loop. The descendants campaign is the other case:
   * `queue.md` § *DESCENDANTS EXPORTS ON THE 15 HINGE PEOPLE* and § *THE DISJOINTNESS CAMPAIGN*
   * both rule `Descendants`, NOT `Forest`, because Forest follows spouse links and spends the
   * 5,000 slots sideways when the ball is wanted going down.
   *
   * It lives in the STATE rather than on the seed job because a creation throws the seed queue
   * away: the export is enqueued by the `added` handler, which has the result and the state and
   * no longer has the job that started the climb. */
  exportWalk: "forest",
  /* ⛔⛔ **THE PRE-WRITE FLAG. A WALK MAY CREATE ONE PERSON AND THEN IT IS OVER.**
   *
   * `seed.js` sets this by message immediately BEFORE it clicks save, so it is set even when the
   * job that set it never reports — a closed tab, a timed-out confirmation, a torn-down worker.
   * On 2026-09-10 all three happened and every one of them left the background believing nothing
   * had been created, so the walk kept climbing and kept creating.
   *
   * Anything other than empty means *a person may now exist because of this run*, and that is
   * enough to stop. It is deliberately not a count and deliberately not clearable by a result:
   * only a new run clears it. */
  creating: ""
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
    /* ⛔ **A WRITE IS ABOUT TO HAPPEN. STOP THE RUN NOW, BEFORE IT DOES.**
     *
     * This arrives from `seed.js` ahead of the save click and it is the only creation signal that
     * does not depend on the job surviving. The run is halted here rather than in the `result`
     * handler, so a lost result cannot leave the walk climbing.
     *
     * The remaining seed jobs go too: they were the search for a slot and the slot has been
     * found. Any export the run has queued stays -- that is the point of the climb. */
    if (msg.type === "creating") {
      const s2 = await state();
      await put({
        creating: String(msg.geni_id || "unknown"),
        running: false,
        queue: (s2.queue || []).filter((q) => q.job !== "seed"),
        results: (s2.results || []).concat([{ at: new Date().toISOString(), job: "seed",
                                              geni_id: String(msg.geni_id || ""),
                                              state: "creating", which: msg.which || "",
                                              first: msg.first || "", last: msg.last || "" }])
      });
      sendResponse({ halted: true });
      return;
    }
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

      /* ⛔⛔ **THE EXTENSION RECORDS WHO IT RAN ON. NOT THE AGENT.**
       *
       * Ruled 2026-09-10: *"the extension should be scraping the page and adding and basically
       * just writing into the file automatically whether it has tried the page. It's not
       * agentic."*
       *
       * `attempt_ledger.py` exists as a script because **nothing downloads** -- the extension
       * cannot write into the repo, and that constraint is not negotiable. But the part that was
       * agentic is not the writing, it is the DECIDING: on 2026-09-10 fourteen rate-limited
       * people were stamped by typing their ids into a command line, which means a person chose
       * which attempts counted. That is the discretion the design removes everywhere else.
       *
       * So the extension keeps the list. Every result appends its id here, whatever the state --
       * a hit, a miss, a 429, an error. The harvest dumps this list wholesale into
       * `attempt_ledger.py`; nobody picks. `attempted` is append-only within a run and is reset
       * by `load`, exactly like `results`. */
      const attempted = (s.attempted || []).concat([{
        geni_id: String((msg.result && msg.result.geni_id) || ""),
        state: (msg.result && msg.result.state) || "",
        at: new Date().toISOString()
      }].filter((a) => a.geni_id));

      /* ⛔ A CAPTCHA STOPS THE RUN. `GC.blocked()` reports it and nothing acted on it -- which
       * did not matter while opening was pinned to the return rate, and matters a great deal now
       * that the loop opens continuously. Geni served an Incapsula challenge after roughly forty
       * rapid loads once already. A blocked page scrapes as a person with no family and reports
       * success, so carrying on would write empty captures over real people. */
      if (msg.result && msg.result.state === "blocked") {
        /* ⛔⛔ **A 429 BACKS THE RUN OFF. IT DOES NOT END IT, AND IT DOES NOT UN-ATTEMPT ANYBODY.**
         *
         * Ruled 2026-09-10: *"Every single individual that we ran this on gets added as being
         * run... You aren't trying to do some sort of exception where you decide, oh, we didn't
         * really do these people, and you don't list them as being attempted. They've been
         * attempted."* The request went out and Geni answered; that is the attempt, and
         * `attempt_ledger.py`'s own docstring already says so -- *"if we fail on an individual,
         * we've attempted it and we move on"*.
         *
         * So the result is KEPT, with its blocked state, for the harvest to stamp. What changes
         * is the rate: the stagger doubles, capped at a minute, and the next open waits out a
         * cooldown. That is the extension rate-limiting itself at the point Geni asks it to,
         * which is the whole of what a 429 means.
         *
         * Halting instead was the first version and it was wrong twice: it needed a human to
         * restart, and it invited exactly the un-attempting this ruling forbids. */
        const slower = Math.min(60000, Math.max(4000, (s.staggerMs || 4000) * 2));
        await put({ active, results, attempted, staggerMs: slower,
                    cooldownUntil: Date.now() + BLOCK_COOLDOWN_MS });
        try { await chrome.tabs.remove(tabId); } catch (e) {}
        chrome.alarms.create(PUMP_ALARM, { when: Date.now() + BLOCK_COOLDOWN_MS });
        sendResponse(true);
        return;
      }

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
          const w = s.exportWalk || "forest";
          queue = queue.concat([{ job: "export", geni_id: String(pid), kind: w,
                                  walk: w, label: "created by the parent walk" }]);
        }
        /* The `creating` flag has already stopped the run. The export is the whole point of the
         * climb, so it is let through -- and only it: `pump` will not open a seed while
         * `creating` is set, so `running` coming back on cannot restart the walk. With no `pid`
         * there is nothing to export from and the run simply stays stopped. */
        await put({ active, results, attempted, queue, endId: pid, running: !!pid });
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
        await put({ active, results, attempted, queue });
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
      await put({ active, results, attempted, queue });
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
        results: [], attempted: [], active: {}, endId: "", dryRun: false, creating: "",
        exportWalk: msg.exportWalk || "forest",
        running: true, startedAt: new Date().toISOString()
      });
      sendResponse({ started: id });
      pump();
      return;
    }
    /* ⛔ **`seedwalk` IS THE DESCENDANTS CAMPAIGN'S ENTRY POINT, and it is `walk` WITHOUT THE
     * PATH GATE.** `walk` starts on an `individual` job: scrape the family, ask Geni for the
     * Charlemagne path, and climb only if the path misses AND the statistics clear 300. That
     * gate is right for the isolate campaign, whose whole question is whether the person is
     * connected -- and it is wrong here, because the hinge people and the disjointness targets
     * are named in advance and an export is warranted on them by the naming, not by a census.
     * Running them through `walk` would ask Geni a path question nobody asked and then decline
     * the export on the answer.
     *
     * So this queues the CLIMB directly: `docs/parent-walk-algorithm.md`'s breadth-first walk,
     * mother then father, ending the moment one ancestor is created -- and then the export from
     * that created ancestor, in the walk this campaign rules.
     *
     * `queue.md`: *"Per person: create an ANCESTOR of them per `docs/export-seed-rules.md`, then
     * run a `Descendants` export on the created ancestor."* That sentence is these two lines.
     *
     * The agent's involvement is unchanged and is still the whole of it: open a page from the
     * repository's list, call this, stop. The queue stays here where it cannot be seen. */
    if (msg.type === "seedwalk") {
      const id = String(msg.geni_id || "");
      if (!id) { sendResponse({ error: "no geni_id" }); return; }
      await put({
        queue: [{ job: "seed", geni_id: id, kind: "seed", label: msg.label || "" }],
        results: [], attempted: [], active: {}, endId: "", dryRun: false, creating: "",
        exportWalk: msg.exportWalk || "forest",
        /* ⛔ AN HOUR, NOT THE TEN-MINUTE DEFAULT. `DEFAULTS.waitMs` is 600000 and it is the
         * PATH search's budget; `runExport` takes the same field and a 5,000-person ball
         * routinely builds for longer than ten minutes. A timeout here is not a retry either --
         * § *A SUBMITTED EXPORT CANNOT BE CANCELLED* means the build carries on regardless and
         * the only thing a short budget buys is losing track of it. */
        waitMs: msg.waitMs || 3600000,
        running: true, startedAt: new Date().toISOString()
      });
      sendResponse({ started: id, exportWalk: msg.exportWalk || "forest" });
      pump();
      return;
    }
    /* ⛔ **`enqueue` APPENDS. `load` REPLACES AND CLEARS.**
     *
     * `load` resets `results` and `attempted`, so queueing a new batch before the previous one
     * is written out DESTROYS it -- nine captures went that way on 2026-09-10, nine page loads
     * and their searches spent for nothing. The rule that followed was *harvest before loading*,
     * and the cost of that rule is that the collector sits idle for the whole harvest, which is
     * the slow half.
     *
     * This removes the tradeoff: top up the queue without touching results, so Geni keeps being
     * asked while the writing happens. Ruled 2026-09-10 -- *"I'd be legitimately cool with ...
     * consistently get 5 people a minute"*. Idle time is the thing to eliminate. */
    if (msg.type === "enqueue") {
      const add = (msg.queue || []).filter((j) => j && j.geni_id);
      const held = new Set((s.queue || []).map((q) => String(q.geni_id)));
      const fresh = add.filter((j) => !held.has(String(j.geni_id)));
      const patch = { queue: (s.queue || []).concat(fresh) };
      if (msg.staggerMs) patch.staggerMs = Math.max(1000, msg.staggerMs | 0);
      if (!s.running) { patch.running = true; patch.dryRun = false; }
      await put(patch);
      sendResponse({ added: fresh.length, queued: patch.queue.length });
      pump();
      return;
    }
    if (msg.type === "load") {
      /* ⛔ THE STAGGER IS THE ONLY THROTTLE, so the caller sets it. `DEFAULTS.staggerMs` is
       * 60000 -- the geni-scraping rate of one a minute -- and that was never the intended
       * ceiling for a run that holds its tabs: opening is serial, holding is unbounded, so the
       * gap between OPENS is the whole rate control. */
      const extra = {};
      if (msg.staggerMs) extra.staggerMs = Math.max(1000, msg.staggerMs | 0);
      await put(Object.assign({ queue: msg.queue, results: [], attempted: [], active: {} }, extra,
                              msg.start ? { running: true, dryRun: false, creating: "",
                                            startedAt: new Date().toISOString() } : {}));
      sendResponse(msg.queue.length);
      if (msg.start) pump();
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
      /* ⛔ **A CLIMB IS SEQUENTIAL, SO SEED JOBS RUN ONE AT A TIME.** `s.concurrency` is 12 and
       * it is the PATH search's number — *"how many searches can be in flight at once"* — where
       * twelve tabs each waiting ten minutes on Geni is the whole point. A seed job waits on a
       * page load, not on a search, and two things make twelve of them actively harmful:
       *
       *  - **The work is thrown away.** A creation ends the walk and drops the rest of the seed
       *    queue, so every seed running beside the one that finds a slot was spent on a queue
       *    about to be discarded.
       *  - **It broke the walk.** Twelve concurrent Geni loads on 2026-09-10 put 8 of 23 pages
       *    past `runSeed`'s load budget and closed 4 tabs outright; each of those took its two
       *    parents out of the frontier, and the walk stopped with nothing created.
       *
       * One at a time is also what `docs/parent-walk-algorithm.md`'s order actually describes:
       * the next person comes from this person's answer. */
      /* ⛔ **ONE CREATION PER RUN, ENFORCED WHERE THE TAB IS OPENED.** `creating` is set before
       * the write, never cleared by a result, and cleared only by starting a new run. So once a
       * person may exist, no further seed page is ever opened -- whatever the queue says, and
       * whatever happened to the job that set it. The export is still allowed through. */
      if (next.job === "seed" && s.creating) {
        await put({ queue: s.queue.filter((q) => q.job !== "seed") });
        continue;
      }
      /* `stats` joins them: a census read costs a real page load, Geni served an Incapsula
       * CAPTCHA after roughly forty rapid ones, and the campaign needs sixty. One at a time. */
      /* ⛔⛔ **THERE IS NO TAB CAP. THE LIMIT IS ON OPENING, NOT ON HOLDING.**
       *
       * Ruled 2026-09-10: *"You're supposed to open like 500 tabs in the process of this (not at
       * once though). No cap on tabs lol and the real thing is as soon as you request a path you
       * open a new tab, but never open multiple tabs simultaneously."*
       *
       * Two different quantities, and only one of them is bounded:
       *
       *   OPENING   strictly one at a time, paced by `staggerMs`. The loop opens a single tab
       *             and breaks, and that is the whole constraint.
       *   HOLDING   unbounded. A tab whose path search is running costs RAM and nothing else,
       *             and it MUST stay open -- closing it drops Geni's promise to notify.
       *
       * `s.concurrency` capped the HOLDING at 12, which is the wrong quantity entirely: the run
       * stalled until a ten-minute search finished before the next page could be opened, so
       * twelve searches ran and everything else waited. The searches are what is being
       * accumulated; the opens are what is being rationed.
       *
       * Exports stay at 1 because that is GENI's limit rather than ours, and seeds stay at 1
       * because a creation ends the walk and every parallel seed is work about to be discarded. */
      /* The 429 cooldown. Checked here, where tabs are opened, so it throttles the one thing
       * Geni is complaining about and nothing else. */
      if (s.cooldownUntil && Date.now() < s.cooldownUntil) {
        chrome.alarms.create(PUMP_ALARM, { when: s.cooldownUntil + 500 });
        break;
      }
      const serial = (next.job === "export" || next.job === "seed" || next.job === "stats");
      if (serial && inFlight >= 1) break;

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
      /* ⛔⛔ **THE OPEN LOOP MUST NOT WAIT FOR RESULTS, AND IT USED TO.**
       *
       * This opened ONE tab and broke out. `pump` was then re-entered only by a result arriving
       * or by the 60s alarm -- so the rate of OPENING was pinned to the rate of RETURNING, and
       * a run could never get ahead of its own searches. Measured 2026-09-10: 24 people took
       * eight minutes, which is the return rate and nothing to do with how fast Geni will accept
       * a page load.
       *
       * The design is the opposite: *"as soon as you request a path you open a new tab, but
       * never open multiple tabs simultaneously."* Serial opening, unbounded holding. So the
       * loop keeps opening, paced only by `staggerMs`, and the tabs pile up dormant.
       *
       * The alarm stays as the recovery path for a worker torn down mid-run; `pumping` and the
       * queue re-read make a double fire harmless. */
      chrome.alarms.create(PUMP_ALARM, { when: Date.now() + Math.max(1000, s.staggerMs) });
      await new Promise((res) => setTimeout(res, Math.max(250, s.staggerMs)));
      continue;
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
