/* Content-script entry point: ask the background what this tab is for, run it, report back.
 *
 * The tab announces itself rather than the background injecting on a timer, because Geni
 * navigates and redirects (`/people/x/<id>` lands on `/people/<Name>/<id>`) and a message sent
 * before the redirect is a message to a page that is about to be replaced.
 */

/* ⛔⛔ **ONE DISPATCH TABLE. THERE WERE TWO, AND ONLY ONE OF THEM GOT THE NEW JOB.**
 *
 * This file routes a job twice -- once for a job the BACKGROUND handed this tab (the `claim`
 * branch at the top) and once for the DOM trigger. They were two copies of the same ternary, and
 * on 2026-09-10 a `stats` job was added to the second one only. The first copy has no `stats`
 * case, so every background-driven census job fell through the whole ternary to its final
 * `else` -- `GC.runPath` -- and **asked Geni for a relationship path on each of sixty people**
 * instead of reading a number off the page. Four ran before it was stopped; Emma saw them as
 * *"We found the blood relationship path you requested to ..."* banners.
 *
 * A ternary chain ending in a bare fallback fails SILENTLY and fails LOUDLY at Geni: an
 * unrecognised job does not error, it runs the last branch. That is the same shape as
 * `CLAUDE.md` § *A GUARD IN ONE EMITTER IS NOT A GUARD* -- two copies of a rule is how the rule
 * comes to mean two different things -- so there is now one table, and adding a job means adding
 * it here, once.
 *
 * The fallback is gone with it: an unknown job returns `unknown_job` rather than quietly asking
 * Geni for a path. */
GC.dispatch = async function (job) {
  switch (job.job) {
    case "export":     return GC.runExport(job);
    case "seed":       return GC.runSeed(job);
    case "individual": return GC.runIndividual(job);
    case "family":     return GC.runFamily(job);
    case "path":       return GC.runPath(job);
    /* The census read. `GC.statistics()` costs a real page load and returns the numbers only. */
    case "stats":      return Object.assign({ job: "stats", geni_id: String(job.geni_id || "") },
                                            await GC.statistics());
    default:           return { job: String(job.job || ""), geni_id: String(job.geni_id || ""),
                                state: "unknown_job" };
  }
};

(async () => {
  if (!location.pathname.startsWith("/people/") &&
      !location.pathname.startsWith("/gedcom/")) return;

  let job;
  try {
    job = await chrome.runtime.sendMessage({ type: "claim", url: location.href });
  } catch (e) {
    return; /* no background listening: the extension is idle, and this is an ordinary visit */
  }
  if (!job || !job.job) return;

  let result;
  try {
    result = await GC.dispatch(job);
  } catch (e) {
    result = { job: job.job, geni_id: job.geni_id, state: "error", error: String(e && e.message || e) };
  }

  try {
    await chrome.runtime.sendMessage({ type: "result", jobId: job.jobId, result });
  } catch (e) { /* the background may have been torn down; the download, if any, still landed */ }
})();

/* ---------------------------------------------------------------- a DOM trigger
 *
 * The popup is the normal way to drive this, and it is unreachable from the automation surface:
 * the toolbar is browser chrome, and `chrome-extension://` URLs are refused the same way
 * `chrome://` ones are. So there is a second entry point that needs none of that.
 *
 * ⛔ EVERYTHING CROSSES AS A STRING, on a data attribute. A content script runs in an isolated
 * world, so it shares the DOM with the page and nothing else -- no globals, and `CustomEvent`
 * detail is cloned under rules that vary. An attribute is plain text both sides can read, which
 * is the same reason `data-geni-collector` is how "is it loaded?" got answered.
 *
 *     page:      documentElement.dataset.geniCollectorJob = JSON.stringify({job:"seed", ...})
 *                document.dispatchEvent(new Event("geni-collector-run"))
 *     extension: ... runs it ...
 *                documentElement.dataset.geniCollectorResult = JSON.stringify(result)
 *
 * `geniCollectorBusy` is set while a job runs, so a caller can wait rather than poll blindly.
 */
document.addEventListener("geni-collector-run", async () => {
  const root = document.documentElement;
  if (root.dataset.geniCollectorBusy === "1") return;
  let job;
  try {
    job = JSON.parse(root.dataset.geniCollectorJob || "{}");
  } catch (e) {
    root.dataset.geniCollectorResult = JSON.stringify({ state: "bad_job_json" });
    return;
  }
  root.dataset.geniCollectorBusy = "1";

  /* ⛔ **`{job:"walk"}` HANDS OFF TO THE BACKGROUND AND RETURNS.** It is the agent's whole
   * involvement: open a page from the repository's list, call this, stop. The background then
   * owns the queue, opens the tabs, paces itself and runs the full operation -- scrape, path,
   * gate, climb, create, export -- with nothing coming back out for anybody to manage.
   *
   * Emma, 2026-09-09: *"the extension's supposed to do all of the work on its own. You should
   * never be able to see the queue at all."* This returns a receipt, not a queue. */
  /* ⛔ **`{job:"bg"}` IS A PROBE OF THE BACKGROUND, and it exists because a silent
   * `sendMessage` resolving `undefined` is indistinguishable from a stale service worker, a
   * handler that never ran, and a handler that threw before `sendResponse`. All three look like
   * an empty receipt from here, and guessing between them cost a restart cycle. */
  /* ⛔ **`{job:"seedwalk"}` IS THE SAME HANDOFF FOR THE DESCENDANTS CAMPAIGN.** It differs from
   * `walk` in one thing and the background owns it: the climb starts immediately instead of
   * behind the path-and-statistics gate, and the export at the end of it takes `exportWalk`.
   * The campaigns rule `Descendants`; the ordinary loop's `Forest` stays the default. */
  if (job && (job.job === "walk" || job.job === "seedwalk" || job.job === "bg")) {
    const msg = job.job === "bg"
      ? Object.assign({ type: job.type || "ping" }, job.msg || {})
      : { type: job.job, geni_id: job.geni_id, label: job.label || "",
          exportWalk: job.exportWalk || "forest" };
    let reply = null, failed = null;
    try {
      reply = await chrome.runtime.sendMessage(msg);
    } catch (e) {
      failed = String(e && e.message || e);
    }
    const last = chrome.runtime.lastError ? String(chrome.runtime.lastError.message) : null;
    root.dataset.geniCollectorResult = JSON.stringify({
      job: job.job, geni_id: job.geni_id || "", sent: msg.type,
      reply: reply === undefined ? null : reply,
      replied: reply !== undefined && reply !== null,
      threw: failed, lastError: last,
      /* The manifest version of the CONTENT script. If the background reports a different one
       * the service worker is stale, which is the case this probe was written to name. */
      contentVersion: (chrome.runtime.getManifest && chrome.runtime.getManifest().version) || "?",
      /* The boot beacon, read straight out of storage rather than asked for. See background.js. */
      beacon: await new Promise((res) => {
        try { chrome.storage.local.get(["swBootedAt", "swVersion"], (o) => res(o || null)); }
        catch (e) { res({ error: String(e && e.message || e) }); }
      })
    });
    root.dataset.geniCollectorBusy = "0";
    return;
  }
  delete root.dataset.geniCollectorResult;
  let result;
  try {
    /* ⛔ `stats` IS THE CENSUS READ AND IT IS A JOB, not something the agent does by hand.
     * `GC.statistics()` has existed since the collector was written and nothing could call it on
     * its own -- only `runIndividual`, which also asks Geni for a path and applies the export
     * gate. The descendants campaign needs the number alone: *"randomly pick people in the graph
     * and find out if anybody has listed 5,000 descendants."* A census read costs a real page
     * load, so the agent opens the tab and this reads it. */
    result = await GC.dispatch(job);
  } catch (e) {
    result = { state: "error", error: String((e && e.message) || e) };
  }
  root.dataset.geniCollectorResult = JSON.stringify(result);
  root.dataset.geniCollectorBusy = "0";
});

/* ---------------------------------------------------------------- the SCHEDULER bridge
 *
 * ⛔ THE SCHEDULER HAD NO REACHABLE CONTROL, and that is why it has never run once.
 *
 * `background.js` already answers `status`, `start`, `stop` and `load` over
 * `chrome.runtime.sendMessage`, so it was always drivable — but only from an extension context,
 * and the only one that existed was the toolbar popup. The toolbar is browser chrome and
 * `chrome-extension://` URLs are refused the same way `chrome://` ones are, so driving it meant
 * asking for a click, every time. That is why the scheduler's viability was
 * still open weeks after the queue logic was written, and why `addAncestor`'s termination — which
 * lives in the background's `result` handler and nowhere else — had never executed.
 *
 * The DOM trigger above runs ONE job in THIS tab, deliberately: it calls `GC.runSeed` and friends
 * directly and never touches the queue. So it could not exercise the scheduler either. This is the
 * missing half — the same data-attribute channel, relaying to the background rather than running
 * anything itself.
 *
 *     page:      documentElement.dataset.geniCollectorScheduler =
 *                  JSON.stringify({type:"status"})            // or start / stop / load
 *                document.dispatchEvent(new Event("geni-collector-scheduler"))
 *     extension: ... relays to background ...
 *                documentElement.dataset.geniCollectorSchedulerResult = JSON.stringify(reply)
 *
 * It relays and does not interpret. Every rule about what the scheduler may do — exports one at a
 * time because that is Geni's limit, tabs held open while a search runs, the seed queue dropped
 * once one ancestor is added — stays in `background.js`, which is the only place that knows them.
 * A bridge that started making decisions would be a second scheduler. */
document.addEventListener("geni-collector-scheduler", async () => {
  const root = document.documentElement;
  let msg;
  try {
    msg = JSON.parse(root.dataset.geniCollectorScheduler || "{}");
  } catch (e) {
    root.dataset.geniCollectorSchedulerResult = JSON.stringify({ error: "bad json" });
    return;
  }
  delete root.dataset.geniCollectorSchedulerResult;
  let reply;
  try {
    reply = await chrome.runtime.sendMessage(msg);
  } catch (e) {
    reply = { error: String((e && e.message) || e) };
  }
  root.dataset.geniCollectorSchedulerResult = JSON.stringify(reply === undefined ? null : reply);
});
