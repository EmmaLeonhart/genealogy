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
