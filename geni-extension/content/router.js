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
           : await GC.runPath(job);
  } catch (e) {
    result = { job: job.job, geni_id: job.geni_id, state: "error", error: String(e && e.message || e) };
  }

  try {
    await chrome.runtime.sendMessage({ type: "result", jobId: job.jobId, result });
  } catch (e) { /* the background may have been torn down; the download, if any, still landed */ }
})();
