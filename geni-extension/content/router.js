/* Content-script entry point: ask the background what this tab is for, run it, report back.
 *
 * The tab announces itself rather than the background injecting on a timer, because Geni
 * navigates and redirects (`/people/x/<id>` lands on `/people/<Name>/<id>`) and a message sent
 * before the redirect is a message to a page that is about to be replaced.
 */

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
    result = job.job === "export" ? await GC.runExport(job)
           : job.job === "seed" ? await GC.runSeed(job)
           : job.job === "family" ? await GC.runFamily(job)
           : await GC.runPath(job);
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
  delete root.dataset.geniCollectorResult;
  let result;
  try {
    result = job.job === "export" ? await GC.runExport(job)
           : job.job === "seed" ? await GC.runSeed(job)
           : job.job === "family" ? await GC.runFamily(job)
           : await GC.runPath(job);
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
 * asking Emma to click, every time. That is why *"the scheduler I don't know if it can work"* was
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
