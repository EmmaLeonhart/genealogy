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
 * ## ⛔ 202 AND 200 ARE DIFFERENT ANSWERS AND BOTH ARE SUCCESS
 *
 * This is the thing that made a healthy runner look dead, so it is written out in full.
 *
 *     202  ok / task 6000000227772636072      a real search was QUEUED on Geni's side
 *     200  data-result="not-found-blood"      answered at once: this person has NO blood path
 *     200  data-result="not-found-inlaw"      the same for the in-law search
 *
 * The old counter called both of them `ok`, so a climbing `ok` meant only *the endpoint
 * replied*. On 2026-09-15 that produced 253 cheerful successes against almost nothing new on
 * `/paths`, and the reasonable conclusion — that the requester was broken — was wrong.
 * **Most of this population genuinely has no path.** These are disconnected `P2600` holders;
 * that is what disconnected MEANS, and § *an isolate with no path is attempted and done*
 * already said so. A `/paths` row appears only when a path is actually FOUND, so `/paths` is
 * not the instrument for *is it running* and never was.
 *
 * So the counters are the outcomes themselves — `queued`, `notfound`, `fail` — and
 * `window.__pathrun.health()` is what a check reads. **A run where `notfound` climbs and
 * `queued` stays near zero is working correctly.** Only `fail` climbing, or nothing moving at
 * all, is a fault.
 *
 * Treating 202 as failure once brought an abort guard within one row of stopping a healthy run.
 *
 * ## ⛔ THE STALE `slug` IS NOT A BUG, AND IT WAS ACCUSED OF BEING ONE
 *
 * The derive swaps the page's numeric id and leaves its slug, so every request carries the slug
 * of whatever profile the template came from — `&slug=Johann-Bach` for hundreds of strangers.
 * Tested directly 2026-09-15 on two fresh ids, no-slug first and stale-slug first: **the
 * responses are byte-identical.** The id in the PATH governs and the slug is decoration. Do not
 * "fix" it, and do not re-derive on its account.
 *
 * ## ⛔ THE BATCH CANNOT BE FETCHED FROM THE REPO. IT HAS TO BE PASTED.
 *
 * Tried 2026-09-15 and refuted: a `fetch` from a geni.com page to
 * `raw.githubusercontent.com` dies on `TypeError: Failed to fetch` — geni.com's CSP forbids the
 * cross-origin connection, and it cannot be moved to a page that allows it, because the search
 * requests need geni.com's own cookies. So `build-pathrun-batch.py` output goes into the console
 * by hand, and a self-topping-up runner is not available however much the top-up rule wants one.
 * `reports/pathrun-batch.js` is committed anyway, because the ONE thing that must never happen
 * again is the target list existing only inside a tab.
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
 *     status   window.__pathrun.health()  ->  {alive, queued, notfound, fail, ...}
 *     drain    window.__pathrun.drain()   -> JSON for scripts/stamp-attempts.py
 *     stop     window.__pathrun.stop()
 *
 * ## ⛔ IT HAS TO RECORD WHAT IT ASKED, AND FOR ~9,500 REQUESTS IT DID NOT
 *
 * Emma, 2026-09-16: *"why the fuck are old qids being requested? Was it not saved what was
 * requested?"* It was not. Measured the same minute: `reports/unconnected-p2600.tsv` carried
 * **248 real attempt dates** against 221,448 rows still reading `SEED_NEVER`, and every one of
 * those 248 came from the extension. The path requester wrote `pathrun_cursor` to localStorage
 * and nothing else, so the ~8,000 requests before 2026-09-15 and the ~1,600 after left no trace
 * anywhere in the repo.
 *
 * **The consequence is that the campaign re-asks the same people every session.**
 * `build-pathrun-batch.py` differences out `reports/geni-paths-harvest.tsv` -- the people a path
 * was FOUND for -- and honours a 30-day cooldown on `last_attempted`. For this population the
 * answer is overwhelmingly *not found*, so the harvest never grows and the cooldown never
 * engages: an id answered *no path* is eligible again immediately, forever.
 *
 * The machinery to stop that already existed. `scripts/stamp-attempts.py` reads a JSON dump and
 * hands every id to `attempt_ledger.py`; the EXTENSION had been feeding it since 2026-09-10 and
 * the requester never did. So `R.done` accumulates one record per id -- **whatever the outcome**,
 * because § *a state this script refused to stamp would be a state somebody chose to un-attempt*
 * -- and `drain()` hands it over.
 *
 * ⛔ **THE ~9,500 ALREADY SPENT ARE NOT RECOVERABLE.** A found path is in the harvest and a
 * not-found answer was never written down. They will be re-asked once more, be recorded this
 * time, and then fall under the cooldown.
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
  R.queued = 0;                 // 202 -- a real search is now running on Geni's side
  R.notfound = 0;               // 200 not-found -- attempted, and the answer is no
  R.found = 0;                  // 200 that is neither -- something came back inline
  R.lastAt = null;              // ⛔ a TIMESTAMP, because no counter can say "stalled"
  /* One record per id, whatever Geni answered. This is the thing whose absence made the
   * campaign re-ask the same people every session -- see the header. */
  R.done = [];
  R.drain = function () {
    const out = JSON.stringify(R.done);
    R.done = [];
    try { localStorage.removeItem("pathrun_attempted"); } catch (e) {}
    return out;
  };
  R.stop = () => { R.running = false; };
  R.tpl = window.__tpl;

  /* What the hourly check reads. `alive` is the only field that matters and it is TIME-based:
   * a runner that stopped existing leaves `running:true` frozen behind it, so the question is
   * never "is the flag still set" but "did anything actually happen in the last two minutes". */
  R.health = function () {
    const age = R.lastAt ? (Date.now() - R.lastAt) / 1000 : null;
    return {
      alive: !!(R.running && age !== null && age < 120),
      secondsSinceLastRequest: age === null ? null : Math.round(age),
      i: R.i, of: R.ids.length,
      queued: R.queued, notfound: R.notfound, found: R.found, fail: R.fail,
      started: R.started, finished: R.finished || null,
    };
  };

  /* ⛔ **A RESTART MUST NOT LEAVE THE OLD LOOP RUNNING, AND ONCE IT DID.** Pasting this block
   * over a paused runner restarted it while the previous loop was still parked in its own
   * `await sleep()`; that loop then woke, saw `running` true again and carried on, so TWO loops
   * drove one cursor. `i` advanced 65 people in 14 seconds — a third of the proper pace, double
   * the request rate at Geni, and five failures where there had been none. The generation token
   * is the fix: a loop only continues while it is still the newest one. */
  R.gen = (R.gen || 0) + 1;

  R.go = async function () {
    const mine = R.gen;
    while (R.running && R.gen === mine && R.i < R.ids.length) {
      const id = R.ids[R.i];
      const outcome = [];
      for (const which of ["blood", "inlaw"]) {
        if (!R.running || R.gen !== mine) break;
        try {
          const res = await fetch(R.tpl[which].split("%ID%").join(id),
                                  { credentials: "include", redirect: "follow" });
          const body = await res.text();
          // ⛔ 202 and 200 are DIFFERENT ANSWERS AND BOTH ARE SUCCESS. See the header.
          if (res.status === 202) { R.queued++; R.ok++; outcome.push("queued"); }
          else if (res.status === 200 && /not-found/.test(body)) { R.notfound++; R.ok++; outcome.push("notfound"); }
          else if (res.status >= 200 && res.status < 300) { R.found++; R.ok++; outcome.push("found"); }
          else { R.fail++; outcome.push("http" + res.status); }
          R.lastAt = Date.now();
        } catch (e) { R.fail++; outcome.push("error"); }
        await new Promise(s => setTimeout(s, 1100 + Math.random() * 700));
      }
      R.i++;
      /* ⛔ ATTEMPTED IS ATTEMPTED. No filter on `state`: `stamp-attempts.py` is explicit that a
       * state the writer refuses to stamp is a state somebody chose to un-attempt. */
      R.done.push({ geni_id: id, state: outcome.join("/") });
      // Survives a reload: the cursor, and the attempts not yet stamped into the worklist.
      try {
        localStorage.setItem("pathrun_cursor", String(R.i));
        localStorage.setItem("pathrun_attempted", JSON.stringify(R.done));
      } catch (e) {}
    }
    if (R.gen === mine) {
      R.running = false;
      R.finished = new Date().toISOString();
    }
  };
  R.go();
})();
