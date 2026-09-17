/* THE SIBLING SCRAPE'S PER-PAGE DRIVER. Paste the RUN block into the console of a profile page.
 *
 * ⛔ **THIS IS NOT `pathrun.js` AND MUST NOT BECOME IT.** The path requester is a loop that lives
 * in one page and does one `fetch` per person against a search endpoint, which is why it runs at
 * 1,040 an hour and carries a batch of 2,400. **This campaign needs a real page load per
 * person** -- `CLAUDE.md` § *a census read costs a real page load*, because `fetch` returns zeros
 * for the statistics block, which is rendered after load.
 *
 * So the loop is the AGENT's and it cannot live in a page at all: every person is a navigation,
 * and a navigation destroys whatever was running. `docs/collector-run-loop.md` § *WHY IT IS
 * AGENTIC AT ALL: the CAPTCHA, and nothing else* -- navigating to the page agentically and then
 * running the extension is what counts as proper traffic, and a background fetch loop is the
 * thing that gets blocked. Geni served an Incapsula CAPTCHA on 2026-09-12 and again on
 * 2026-09-15 after a few hundred back-to-back reads.
 *
 * ⛔ **COMMITTED BEFORE IT WAS RUN.** `CLAUDE.md` § *Anything driving the browser for hours
 * belongs in `scripts/`, committed, before it is run.* That rule was written after the path
 * requester was lost with ~8,000 requests of infrastructure in it, and broken again the next day
 * when the chain fetcher went the same way. This file is the third of the family and it is in
 * the repo first.
 *
 * ## What it does, per person
 *
 *     1  the AGENT navigates to /people/x/<id>        <- the agent's ONLY job
 *     2  RUN block: dispatch {job:"family"} and wait for the extension to answer
 *     3  append the answer to localStorage            <- survives the next navigation
 *     ... every ~25 people ...
 *     4  DUMP block: blob-download them as one JSON file
 *     5  python scripts/write-sibling-scrapes.py < the file
 *
 * ⛔ **`{job:"family"}` AND NOTHING ELSE.** `router.js` also takes `{job:"walk"}` and
 * `{job:"seedwalk"}`, which hand off to the background and run the FULL operation -- scrape,
 * path, gate, climb, create, **and the export**. Emma, 2026-09-16: *"exporting is not one of
 * them"*. `family` scrapes the immediate family and returns; it exports nothing.
 *
 * ⛔ **THE ANSWER GOES OUT AS A FILE, NOT THROUGH THE AGENT.** Returning the scrape from
 * `javascript_tool` does not even work -- the JSON carries the profile URL and comes back
 * `[BLOCKED: Cookie/query string data]` -- and it would cost the whole batch in context. Same
 * reason `pathchains.dump()` and `pathrun.dumpAttempts()` blob-download instead of returning
 * rows.
 *
 * ## The protocol, which is an attribute and an event
 *
 * `router.js`: a content script runs in an isolated world, so it shares the DOM and nothing
 * else. Everything crosses as a string on a data attribute, and **the attribute alone does
 * nothing** -- the event is what triggers the run. Setting the attribute and polling for a
 * result waits forever, which is exactly what it did the first time.
 *
 *     documentElement.dataset.geniCollectorJob = JSON.stringify({job:"family", geni_id:"..."})
 *     document.dispatchEvent(new Event("geni-collector-run"))
 *     documentElement.dataset.geniCollectorResult   <- the answer, as a string
 *
 * ## ⛔ DO NOT `await` `one()` FROM THE AGENT. FIRE IT AND POLL.
 *
 * `javascript_tool` is a CDP `Runtime.evaluate` and it gives up after **45000 ms**, which is the
 * same 45 s this file waits by default. Awaiting the call therefore fails on exactly the people
 * it is waiting for -- the slow ones -- and reports
 * *"The renderer may be frozen or unresponsive"* about a renderer that is working perfectly.
 *
 * **The work still lands**, because the promise keeps running in the page after the tool call
 * gives up, which is what makes the fix simple. The loop per person is:
 *
 *     navigate                                        <- the agent's only job
 *     window.__sibscrape.one(id, 60000)               <- NOT awaited; returns at once
 *     wait ~20 s
 *     read localStorage                               <- short call, always answers
 *
 * ⛔ **AND DO NOT SHORTEN THE WAIT TO MAKE IT FIT.** `GC.runFamily` allows the family
 * container 25 s by itself, and reads the statistics block after that. A 20 s wait passed here
 * records `timeout` on a page that was about to answer -- measured on `1434896`, where the only
 * thing the short wait produced was a wasted page load and a wrong state.
 *
 * ## What a state means
 *
 *     scraped            the family block was read. `tsv` is the file to write.
 *     private_profile    Geni declines to show the family. A FINAL answer for that person.
 *     no_family_block    nothing found on a page that should have had something. Look again.
 *     private_profile    Geni will not show this one. Detected from the URL before anything
 *                        else, because the redirect to `/people/private/<id>` has already
 *                        happened and waiting 60 s to discover it is a minute per person.
 *     timeout            the wait ran out on a page that is not private. An attempt either way.
 *     blocked            ⛔ A CAPTCHA. It scrapes as a person with no family and reports
 *                        success, which is why `GC.blocked()` is checked before anything else.
 *                        STOP THE RUN on this one; it does not get better by continuing.
 *
 * All four are RECORDED. § *a state this script refused to stamp would be a state somebody chose
 * to un-attempt* -- the attempt happened whatever the answer was.
 */

/* ---------- RUN: paste on each profile page, with the id it is for ---------- */

window.__sibscrape = window.__sibscrape || {};
window.__sibscrape.one = async function (id, waitMs) {
  const root = document.documentElement;
  const KEY = "sibling_scrapes";

  if (!root.getAttribute("data-geni-collector")) {
    return { geni_id: id, state: "no_extension" };
  }

  /* ⛔ **A PRIVATE PROFILE IS ANSWERED BY THE URL, FOR FREE, AND WAITING ON ONE COSTS A MINUTE.**
   * Geni redirects `/people/x/<id>` to `/people/private/<id>` when it will not show the profile,
   * and that page carries no family container at all -- so `GC.runFamily` sits out its own 25 s
   * wait, this file sits out the rest of its 60 s, and the answer that comes back is `timeout`,
   * which says "ask again later" about a person whose answer is final.
   *
   * Measured: three of the first twenty were private, and each one spent a minute of the sitting
   * to record the wrong state. The redirect has already happened by the time this runs. */
  if (/\/people\/private\//.test(location.pathname)) {
    const rec = { geni_id: String(id), state: "private_profile", at: new Date().toISOString() };
    let h = [];
    try { h = JSON.parse(localStorage.getItem(KEY) || "[]"); } catch (e) { h = []; }
    h.push(rec);
    try { localStorage.setItem(KEY, JSON.stringify(h)); } catch (e) {}
    return { geni_id: rec.geni_id, state: rec.state, parents: 0, siblings: 0, held: h.length };
  }

  delete root.dataset.geniCollectorResult;
  root.dataset.geniCollectorJob = JSON.stringify({ job: "family", geni_id: String(id) });
  document.dispatchEvent(new Event("geni-collector-run"));

  const t0 = Date.now();
  const limit = waitMs || 45000;
  while (!root.dataset.geniCollectorResult && Date.now() - t0 < limit) {
    await new Promise((s) => setTimeout(s, 400));
  }

  const raw = root.dataset.geniCollectorResult;
  let rec;
  if (!raw) {
    /* A timeout is an attempt too. Recorded rather than retried on the spot: a page that did not
     * answer in 45s answers no faster the second time, and the cooldown will bring them back. */
    rec = { geni_id: String(id), state: "timeout" };
  } else {
    try {
      rec = JSON.parse(raw);
    } catch (e) {
      rec = { geni_id: String(id), state: "bad_result_json" };
    }
  }
  rec.at = new Date().toISOString();

  let held = [];
  try { held = JSON.parse(localStorage.getItem(KEY) || "[]"); } catch (e) { held = []; }
  held.push(rec);
  try { localStorage.setItem(KEY, JSON.stringify(held)); } catch (e) {}

  /* ⛔ THE SUMMARY IS SAFE TO RETURN; THE RECORD IS NOT. `tsv` and `url` carry the profile URL
   * and come back redacted, so only counts and the state cross back. */
  return {
    geni_id: rec.geni_id || String(id), state: rec.state, name: rec.name,
    relatives: rec.relatives, parents: (rec.parents || []).length,
    siblings: (rec.siblings || []).length, held: held.length,
  };
};

/* ---------- DUMP: every ~25 people, write what is held out as a file ---------- */

window.__sibscrape.dump = function () {
  const KEY = "sibling_scrapes";
  let held = [];
  try { held = JSON.parse(localStorage.getItem(KEY) || "[]"); } catch (e) { held = []; }
  if (!held.length) return 0;

  const part = (parseInt(localStorage.getItem("sibling_scrapes_part") || "0", 10) || 0) + 1;
  const a = document.createElement("a");
  a.href = URL.createObjectURL(new Blob([JSON.stringify(held)], { type: "application/json" }));
  a.download = "sibling-scrapes-" + String(part).padStart(3, "0") + ".json";
  document.body.appendChild(a); a.click(); a.remove();

  /* Cleared only after the blob is handed over, so a failed download loses nothing. */
  try {
    localStorage.setItem(KEY, "[]");
    localStorage.setItem("sibling_scrapes_part", String(part));
  } catch (e) {}
  console.log("[sibscrape] wrote part " + part + ", " + held.length + " people");
  return held.length;
};

window.__sibscrape.held = function () {
  try { return JSON.parse(localStorage.getItem("sibling_scrapes") || "[]").length; }
  catch (e) { return -1; }
};
