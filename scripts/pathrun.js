/* THE PATH REQUESTER. Paste into the console of any geni.com profile page.
 *
 * ⛔ **THIS FILE EXISTS BECAUSE THE RUNNER WAS SAVED NOWHERE AND DIED.** On 2026-09-14 the
 * requester and the chain fetcher lived only as ad-hoc JavaScript typed into a browser tab.
 * The tab was lost at 20:33 while Geni exports were being driven in neighbouring tabs, and
 * with it went the only copy — infrastructure that had made roughly 8,000 requests, with no
 * source of truth in the repo, the extension, or anywhere else. Emma, on being told:
 * *"Wait what the fuck the runner was not saved anywhere?"* Quite.
 *
 * Nothing about the outage was detectable from inside: it does not crash, it simply stops
 * existing, and the only evidence is that `path-chains-NNN.tsv` stops appearing in Downloads.
 *
 * ## What it does
 *
 * For each Geni id it requests BOTH relationship searches — blood and in-law. `CLAUDE.md`
 * § *BOTH TIES, ALWAYS*: the redundancy is the point, and a blood miss with no path is not
 * done.
 *
 * ## The URL is derived, never hardcoded
 *
 * `window.pathSearcher` carries `path_blood_search_url` and `path_inlaw_search_url`, but ONLY
 * on a profile with no known path — a profile that already has one renders no searcher. So
 * open an unconnected person (`reports/unconnected-p2600.tsv` is full of them), and the
 * template is built by swapping that page's own id for a placeholder. Hardcoding the URL here
 * would rot the first time Geni changed it, and it would put a session-scoped URL in a public
 * repo.
 *
 * ## 202 IS SUCCESS
 *
 * The search endpoints answer **202 Accepted**, not 200 — the search is queued, not completed.
 * Treating 202 as failure once brought an abort guard within one row of stopping a healthy run.
 * The test is `2xx`.
 *
 * ## Pace
 *
 * 1.1–1.8s jittered between requests, inside the runner. § *the stagger is the extension's,
 * never a sleep in the agent* — the agent must not sit in a loop babysitting this. Geni served
 * an Incapsula CAPTCHA on 2026-09-12 after roughly 500 back-to-back reads.
 *
 *     step 1   open an UNCONNECTED profile
 *     step 2   paste the DERIVE block, check it reports derived:true
 *     step 3   paste the RUN block with an id list from scripts/build-pathrun-batch.py
 *     status   window.__pathrun  ->  {running, i, ok, fail}
 *     stop     window.__pathrun.stop()
 */

/* ---------- DERIVE: run this first, on a profile that has NO known path ---------- */

(function derive() {
  const ps = window.pathSearcher;
  if (typeof ps === "undefined") {
    console.log("pathSearcher absent — this profile already has a path. Open an unconnected one.");
    return;
  }
  const here = (location.pathname.match(/\/(\d{10,})/) || [])[1];
  const b = String(ps.path_blood_search_url || "");
  const i = String(ps.path_inlaw_search_url || "");
  if (!here || b.indexOf(here) < 0 || i.indexOf(here) < 0) {
    console.log("could not find this page's id inside the search URLs; template not built");
    return;
  }
  window.__tpl = { blood: b.split(here).join("%ID%"), inlaw: i.split(here).join("%ID%") };
  console.log("derived:true — both templates carry %ID%");
})();

/* ---------- RUN: paste with R.ids filled in from build-pathrun-batch.py ---------- */

window.__pathrun = window.__pathrun || {};
(function run() {
  const R = window.__pathrun;
  if (!window.__tpl) { console.log("no template — run the DERIVE block first"); return; }
  R.ids = R.ids || [];                    // replaced by the generated batch
  R.i = 0; R.ok = 0; R.fail = 0;
  R.running = true;
  R.started = new Date().toISOString();
  R.stop = () => { R.running = false; };
  R.tpl = window.__tpl;

  R.go = async function () {
    while (R.running && R.i < R.ids.length) {
      const id = R.ids[R.i];
      for (const which of ["blood", "inlaw"]) {
        if (!R.running) break;
        try {
          const res = await fetch(R.tpl[which].split("%ID%").join(id),
                                  { credentials: "include", redirect: "follow" });
          // 202 Accepted is the success status here, not 200.
          if (res.status >= 200 && res.status < 300) R.ok++; else R.fail++;
        } catch (e) { R.fail++; }
        await new Promise(s => setTimeout(s, 1100 + Math.random() * 700));
      }
      R.i++;
      // Survives a reload: the cursor is the only state worth keeping.
      try { localStorage.setItem("pathrun_cursor", String(R.i)); } catch (e) {}
    }
    R.running = false;
    R.finished = new Date().toISOString();
  };
  R.go();
})();
