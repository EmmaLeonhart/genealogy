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
 * ## ⛔ THERE IS A THIRD RESPONSE SHAPE, AND IT WAS BEING THROWN AWAY
 *
 * The two answers above are not the whole set. Measured 2026-09-19, live, by recording the
 * bodies the loop was already receiving:
 *
 *     200  <div class="relationship_card">  20-44 KB   GENI ALREADY HAS THE PATH
 *
 * It is not a queued search and not a refusal -- it is the finished chain, rendered, arriving
 * in the same response. One sample carried **53 profile ids across 106 segments** and the line
 * *"Arend Rothuizen is your 25th cousin once removed"*. Roughly a QUARTER of this population
 * answers this way: 312 of the first 1,274 replies on the 2026-09-19 batch.
 *
 * The classifier counted it -- `R.found++` -- read `body` once for the not-found regex, and let
 * it go. So the campaign was asking Geni for paths, being given them, and keeping a tally.
 *
 * ⛔ **AND `found` CLIMBING IS NOT VISIBLE ANYWHERE ELSE, WHICH IS HOW IT SURVIVED.** These
 * produce NO row on `/paths`: that page lists *Recently Requested* relationships, and nothing
 * was requested -- Geni already knew. So the one external instrument the campaign has says
 * nothing about the outcome that carries the most data, and `/paths` looking empty while
 * `found` climbed was read as the requester being broken rather than as a harvest being
 * dropped. § *`/paths` IS NOT THE INSTRUMENT FOR *IS IT RUNNING** understates it: it is not
 * the instrument for *is anything being collected* either.
 *
 * `R.parseChain` now reads these into `reports/path-chains.tsv` rows and `R.dumpChains()`
 * writes them out, which is the same loop `scripts/pathchains.js` runs -- except that this half
 * pays nothing for them, because the fetch has already happened.
 *
 * ## ⛔ THE STALE `slug` IS NOT A BUG, AND IT WAS ACCUSED OF BEING ONE
 *
 * The derive swaps the page's numeric id and leaves its slug, so every request carries the slug
 * of whatever profile the template came from — `&slug=Johann-Bach` for hundreds of strangers.
 * Tested directly 2026-09-15 on two fresh ids, no-slug first and stale-slug first: **the
 * responses are byte-identical.** The id in the PATH governs and the slug is decoration. Do not
 * "fix" it, and do not re-derive on its account.
 *
 * ## ⛔ THE BATCH GOES IN AS A FILE, NOT AS A PASTE
 *
 * Superseding the section below, which stands as the record of what was refuted and why.
 * Pasting 800 ids is ~17KB of console input and 1,600 is ~32KB, spent again at every top-up --
 * and the batch drains in about 45 minutes, so it is spent roughly hourly. The same channel the
 * chain fetcher already uses in the other direction works here: a `<input type=file>` on the
 * page, and the agent hands it the file.
 *
 *     python scripts/build-pathrun-batch.py --count 1600 --order qid   -> ids as JSON
 *     create <input type=file id=batchinput> on the geni.com tab
 *     upload the JSON to it; the change handler parses it into window.__batchLoaded
 *     R.ids = window.__batchLoaded, then the RUN block
 *
 * `reports/pathrun-batch.js` is still committed, and for the same reason as ever: the ONE thing
 * that must never happen again is the target list existing only inside a tab.
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
 *     chains   window.__pathrun.dumpChains()    -> pathrun-chains-NNN.tsv in Downloads,
 *              straight into `python scripts/merge-path-chains.py <file>`
 *     drain    window.__pathrun.dumpAttempts()  -> pathrun-attempted-NNN.json in Downloads,
 *              which goes straight into `python scripts/stamp-attempts.py < <file>`
 *     stop     window.__pathrun.stop()
 *
 * ## ⛔ RESTARTING A LOOP THAT STALLED MID-BATCH: RESUME, DO NOT RE-PASTE
 *
 * The RUN block sets `R.i = 0`. Re-pasting it over a batch that is half done therefore re-asks
 * everyone already done in it -- 2,420 people, on the run this was written for. The cursor is in
 * `localStorage.pathrun_cursor` and survives, so a mid-batch restart is:
 *
 *     R.gen = (R.gen || 0) + 1;                                  // the old loop stands down
 *     R.i = parseInt(localStorage.getItem("pathrun_cursor"), 10);
 *     R.running = true; R.lastAt = Date.now(); R.finished = null;
 *     R.go();
 *
 * `R.gen` is what makes this safe: the stalled loop is parked inside an `await`, and when that
 * finally settles it sees the generation has moved and stops instead of driving the cursor
 * alongside the new one.
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
  /* Harvested chain rows, in `reports/path-chains.tsv` column order. */
  R.rows = [];
  R.chainPart = 0;

  /* ⛔ **THE SAME PARSER AS `scripts/pathchains.js` § `C.one`, DELIBERATELY.** The markup is
   * Geni's and both halves read it the same way, so a change to the site breaks them together
   * rather than one of them silently. The parentheses around a relation are NESTED SPANS and
   * not text -- a regex for the bracketed form matches nothing and reports every page as having
   * zero relations, which is what it did the first time it was tried. `DOMParser` sidesteps it.
   *
   * `span.subtext.clipboard-hide` is the viewer's own blank subtext, so step 0 is the viewer,
   * with a name and no profile id. That row is KEPT: a chain that does not say where it starts
   * is not a chain, and `split-path-chains.py` fills the id from `from=`.
   *
   * ⛔ **STEP -2 CARRIES THE KINSHIP DEGREE, AND IT IS WHY THIS IS NOT JUST `pathchains.js`.**
   * The inline answer renders `#relation_description` -- *"Arend Rothuizen is your 25th cousin
   * once removed"* -- which the six columns have no room for. `merge-path-chains.py` truncates
   * every row to `HEADER`, so a seventh column would be accepted and silently dropped, and a
   * companion file would need a second merger for one fact per path. The file already solved
   * this shape once: `step -1` / `EMPTY` bounds a chain that rendered nothing. So the degree
   * rides in as `step -2`, unique under the `(to_id, kind, step)` dedupe key and ignored by
   * anything reading steps from 0. Nothing new is added anywhere to carry it.
   */
  R.parseChain = function (html, to_id, which) {
    const kind = which === "inlaw" ? "in-law" : "blood";
    const doc = new DOMParser().parseFromString(html, "text/html");
    const out = [];

    const descEl = doc.querySelector("#relation_description");
    if (descEl) {
      const desc = (descEl.textContent || "").replace(/\s+/g, " ")
                     .replace(/Generate Diagram\s*$/, "").trim();
      if (desc) out.push([to_id, kind, "-2", "", "", desc]);
    }

    let step = 0;
    for (const seg of doc.querySelectorAll("span.segment")) {
      const nameEl = seg.querySelector("span.name");
      if (!nameEl) continue;
      const name = (nameEl.textContent || "").replace(/\s+/g, " ").trim();
      if (!name) continue;
      const a = seg.querySelector("[data-profile-id]");
      const sub = seg.querySelector("span.subtext:not(.clipboard-hide)");
      const rel = sub
        ? (sub.textContent || "").replace(/\s+/g, " ").trim().replace(/^\(/, "").replace(/\)$/, "").trim()
        : "";
      out.push([to_id, kind, String(step), a ? a.getAttribute("data-profile-id") : "", name, rel]);
      step++;
    }

    // A 200 that rendered no segments is RECORDED, not dropped -- the same bound pathchains.js
    // puts on an empty permalink, and merge-path-chains.py keeps those rows.
    if (!step) out.push([to_id, kind, "-1", "", "", "EMPTY"]);
    return out;
  };

  /* Written as `pathrun-chains-NNN.tsv`, NOT `path-chains-NNN.tsv`: the chain fetcher numbers
   * its own parts, and two loops writing one series into Downloads would overwrite each other.
   * `merge-path-chains.py` takes explicit paths, so the distinct name costs nothing. */
  R.dumpChains = function () {
    if (!R.rows.length) return 0;
    const n = R.rows.length;
    const head = ["to_id", "kind", "step", "profile_id", "name", "relation"].join("\t") + "\n";
    const body = R.rows.map(r => r.join("\t")).join("\n") + "\n";
    const a = document.createElement("a");
    a.href = URL.createObjectURL(new Blob([head + body], { type: "text/tab-separated-values" }));
    R.chainPart++;
    a.download = "pathrun-chains-" + String(R.chainPart).padStart(3, "0") + ".tsv";
    document.body.appendChild(a); a.click(); a.remove();
    R.rows = [];
    console.log("[pathrun] wrote chains part " + R.chainPart + ", " + n + " rows");
    return n;
  };

  R.drain = function () {
    const out = JSON.stringify(R.done);
    R.done = [];
    try { localStorage.removeItem("pathrun_attempted"); } catch (e) {}
    return out;
  };

  /* ⛔ **THE DRAIN GOES OUT AS A FILE, NOT THROUGH THE AGENT.** Returning the JSON from
   * `javascript_tool` works and costs the whole batch in context every hour, which is the same
   * reason `pathchains.dump()` blob-downloads instead of returning rows. `stamp-attempts.py`
   * already reads a dump from stdin, so the loop is: dump here, pipe the file there. Nothing
   * about which ids counted is decided on the way. */
  R.dumpAttempts = function () {
    if (!R.done.length) return 0;
    const n = R.done.length;
    const a = document.createElement("a");
    a.href = URL.createObjectURL(new Blob([R.drain()], { type: "application/json" }));
    R.part = (R.part || 0) + 1;
    a.download = "pathrun-attempted-" + String(R.part).padStart(3, "0") + ".json";
    document.body.appendChild(a); a.click(); a.remove();
    console.log("[pathrun] wrote attempts part " + R.part + ", " + n + " ids");
    return n;
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
      chainRows: R.rows.length, chainPart: R.chainPart,
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
          /* ⛔ **A FETCH WITH NO TIMEOUT HANGS THE WHOLE CAMPAIGN, SILENTLY.** Measured
           * 2026-09-17: one request never settled, and because the loop was parked inside its
           * `await` the flags kept saying the run was healthy -- `running` true, `finished`
           * null, `i` frozen -- for 13 minutes until the next check. `health()` caught it only
           * because `alive` is time-based; no counter could have.
           *
           * The record before the hang was `queued/error`, so the endpoint was already refusing
           * one of the pair. A browser `fetch` has no default timeout at all: without an
           * AbortController the promise can stay pending indefinitely.
           *
           * 20s is well past a normal reply (these answer in well under a second) and well
           * under the 120s `alive` allows, so a timeout is recorded and the loop moves on
           * rather than the run dying between two checks. */
          const ctl = new AbortController();
          const timer = setTimeout(() => ctl.abort(), 20000);
          let res, body;
          try {
            res = await fetch(R.tpl[which].split("%ID%").join(id),
                              { credentials: "include", redirect: "follow", signal: ctl.signal });
            body = await res.text();
          } finally { clearTimeout(timer); }
          // ⛔ 202 and 200 are DIFFERENT ANSWERS AND BOTH ARE SUCCESS. See the header.
          if (res.status === 202) { R.queued++; R.ok++; outcome.push("queued"); }
          else if (res.status === 200 && /not-found/.test(body)) { R.notfound++; R.ok++; outcome.push("notfound"); }
          /* ⛔ **A 200 THAT IS NEITHER OF THOSE IS A WHOLE PATH, AND IT WAS THROWN AWAY.**
           * See the header § THE THIRD RESPONSE SHAPE. `body` is already in hand, so parsing
           * it costs no request: this is the one outcome that arrives with the answer in it. */
          else if (res.status >= 200 && res.status < 300) {
            R.found++; R.ok++; outcome.push("found");
            try { R.rows.push.apply(R.rows, R.parseChain(body, id, which)); }
            catch (e) { R.parseErr = String(e); }
            if (R.rows.length >= 5000) R.dumpChains();
          }
          else { R.fail++; outcome.push("http" + res.status); }
          R.lastAt = Date.now();
        } catch (e) {
          R.fail++;
          /* `timeout` and `error` are kept apart: a timeout is this guard firing, an error is
           * the request failing on its own. Collapsing them would hide whether the guard is
           * doing anything. */
          outcome.push(e && e.name === "AbortError" ? "timeout" : "error");
          /* ⛔ STAMP IT HERE TOO. `lastAt` was only touched on the success path, so a run
           * failing every request looked STALLED rather than failing -- `alive:false` with
           * `fail` climbing, which reads as "the tab died" and sends the next check off to
           * restart something that is actually running. */
          R.lastAt = Date.now();
        }
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
