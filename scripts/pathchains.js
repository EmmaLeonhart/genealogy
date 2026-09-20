/* THE CHAIN FETCHER. Paste into the console of any geni.com page.
 *
 * ⛔ **THIS FILE EXISTS BECAUSE THE FETCHER WAS SAVED NOWHERE AND DIED — THE SECOND HALF OF THE
 * SAME FAILURE.** On 2026-09-14 the requester and the fetcher both lived only as ad-hoc
 * JavaScript in a browser tab; the tab was lost at 20:33 and `scripts/pathrun.js` was written so
 * the REQUESTER could never go that way again. **Only half the lesson was applied.** On
 * 2026-09-15 the requester was restarted and ran correctly — `queued` and `notfound` both
 * climbing, `fail` at 0 — and not one new `path-chains-NNN.tsv` appeared, because the half that
 * WRITES them did not exist anywhere in the repo. Emma: *"what the fuck did you just not request
 * paths"*. Paths were being requested. Nothing was collecting the answers.
 *
 * `CLAUDE.md` § *Anything driving the browser for hours belongs in `scripts/`, committed, before
 * it is run.* That rule was written for this exact file. It was committed before it was run.
 *
 * ## The two halves, and how to tell which one is dead
 *
 *     scripts/pathrun.js      ASKS Geni for a path.   window.__pathrun.health()
 *     scripts/pathchains.js   COLLECTS the answers.   path-chains-NNN.tsv appears in Downloads
 *
 * **A healthy requester says nothing whatever about this half.** The only external evidence that
 * the loop is closed is the FILE timestamps in Downloads — § *Read a sweep's results off the FILE
 * a drain wrote*, and the same rule that caught the 2026-09-14 outage.
 *
 * ## ⛔ THE PERMALINK IS NOT A CONSTRUCTED `/path/` URL
 *
 * `scripts/build-isolate-path-targets.py` carries the refutation: a constructed `/path/` URL
 * redirects to Charlemagne and renders HIS chain, so a harvest scoring on step count reads 100%
 * reach made of one path repeated. The permalinks are read off `/paths` — Geni's own list of
 * *Recently Requested Relationships*, 30 to a page — where each row is a saved object.
 *
 * ## The markup, and the one thing that is easy to get wrong
 *
 *     <span class="segment">
 *       <span class="name"><a data-profile-id="6000000019395171839">Olof Ericsson</a></span>
 *       <span class="subtext"><span class="clipboard-only">(</span>his son<span ...>)</span></span>
 *     </span>
 *
 * ⛔ **THE PARENTHESES ARE NESTED SPANS, NOT TEXT.** `scripts/extract-saved-path-pages.py` carries
 * the same warning, because a regex for `>\(...\)</span>` matches nothing and reports every page
 * as having zero relations — which is exactly what it did on its first attempt. Here the response
 * goes through `DOMParser` and is read with `querySelector`, so the question does not arise.
 *
 * `span.subtext.clipboard-hide` is the viewer's own blank subtext and is skipped, so **step 0 is
 * the viewer, with a name and no profile id.** That row is KEPT: a chain that does not say where
 * it starts is not a chain, and `scripts/split-path-chains.py` fills the id from `from=`.
 *
 * ## ⛔ IT RUNS IN THE FOREGROUND TAB, AND IN A BACKGROUND TAB IT LOOKS FINE AND DOES NOTHING
 *
 * Measured 2026-09-15. The fetcher was started in its own `/paths` tab while the requester held
 * the foreground, and it managed **10 chains in 7 minutes** -- against the 1.5s a chain that
 * `path-chains-090..094` were written at on 2026-09-14, five minutes apart to the file. Nothing
 * was wrong with it: `alive` was true, `fail` was 0, every counter moved. **Chrome throttles
 * `setTimeout` in a background tab**, so the 1.1-1.8s stagger became tens of seconds and a 3.5
 * hour pass became 35 hours.
 *
 * This is the worst shape a fault can take here -- every instrument green, the work not getting
 * done -- and it is the same shape as `ok` climbing while nothing was requested. So: **both
 * halves live in ONE tab, the foreground one.** `queue.md` says so in the singular, *"the
 * requester and the chain fetcher live in the geni.com tab"*, and this is why.
 *
 * `save()` and `load()` are what make moving tabs cheap. The url list costs 28 minutes of
 * `/paths` walking to rebuild and both tabs are geni.com, so it goes through `localStorage`
 * rather than being collected again.
 *
 * ## Pace
 *
 * 1.1–1.8s jittered, the same as the requester and for the same reason: Geni served an Incapsula
 * CAPTCHA on 2026-09-12 after roughly 500 back-to-back reads, and another on 2026-09-15. The
 * stagger is in here, never a sleep in the agent.
 *
 *     step 1   paste this file into the console of the FOREGROUND geni.com tab
 *     step 2   window.__chains.seed([...])      -- a batch from build-chain-batch.py
 *              or await window.__chains.collect() -- walk /paths, gather permalinks
 *              or window.__chains.load()          -- take them off localStorage instead
 *     step 3   window.__chains.go()              -- fetch each, dump every 200 chains
 *     move it  window.__chains.save() in the old tab, load() in the new one
 *     status   window.__chains.health()  ->  {alive, ok, fail, i, of, part}
 *     stop     window.__chains.stop()
 */

window.__chains = window.__chains || {};
(function () {
  const C = window.__chains;
  C.urls = C.urls || [];
  C.rows = C.rows || [];
  /* ⛔ **A FAILED PERMALINK WAS COUNTED AND THEN LOST.** `C.fail++` and `C.i++` both ran, so a
   * chain that timed out was stepped over and never fetched again -- and the only trace was a
   * number going up. Measured 2026-09-20: 72 of the first 8,823 timed out, which is ~1% and
   * would be ~470 chains quietly missing from a 47,692 run. `health()` reporting `fail` is not
   * the same as the work being recoverable. These are kept so `reseedFailed()` can put them
   * back on the end of the list once the latency spike has passed. */
  C.failed = C.failed || [];
  C.i = C.i || 0;
  C.ok = C.ok || 0;
  C.fail = C.fail || 0;
  C.part = C.part || 0;
  C.every = C.every || 200;                 // chains per downloaded file
  C.lastAt = null;
  C.running = false;
  C.stop = () => { C.running = false; };

  /* ⛔ The same generation guard as the requester, and for the same reason: pasting this over a
   * paused fetcher woke the old loop as well, and two loops drove one cursor at double the
   * request rate — the way to get CAPTCHAd. A loop runs only while it is still the newest. */
  C.gen = (C.gen || 0) + 1;

  /* ⛔ **THE PACE BACKS OFF NOW, BECAUSE A FIXED ONE WALKED INTO A RATE LIMIT.** Measured
   * 2026-09-20 over 9,229 chains: the failure rate climbed **monotonically the longer the loop
   * ran** -- 0%, then 9%, then 17.5% -- and throughput fell 1,134 -> 304 -> 214 an hour with it.
   * Every failure was the 25 s timeout; every completed response was HTTP 200 with a real page.
   * And a single probe taken seconds after each stop came back in **1.7-2.0 s every time**, on
   * urls nothing had touched.
   *
   * Fast when idle, progressively slower under a sustained stream, recovering after a pause:
   * that is a rate limiter, not random latency, and a fixed 1.1-1.8 s stagger cannot see one.
   * Backing off is also § *PACE IT* -- 500 back-to-back reads is what got the account CAPTCHAd
   * on 2026-09-12 -- so the response to being throttled is never to push harder.
   *
   * Additive-increase on success, multiplicative-decrease on failure: every failure doubles the
   * gap toward `PACE_MAX`, every `PACE_DECAY` consecutive successes takes 10% back off toward
   * `PACE_MIN`. The agent still never sleeps -- `CLAUDE.md` § *the stagger is the extension's,
   * never a sleep in the agent*. */
  const PACE_MIN = 1100, PACE_MAX = 20000, PACE_DECAY = 10;
  C.pace = C.pace || PACE_MIN;
  C.paceRun = 0;
  C.paceUp = function () {
    C.pace = Math.min(PACE_MAX, Math.max(PACE_MIN, C.pace * 2));
    C.paceRun = 0;
  };
  C.paceDown = function () {
    if (++C.paceRun >= PACE_DECAY) { C.pace = Math.max(PACE_MIN, C.pace * 0.9); C.paceRun = 0; }
  };
  const sleep = () => new Promise(s => setTimeout(s, C.pace + Math.random() * 700));
  const qp = (u, k) => {
    try { return new URL(u, location.origin).searchParams.get(k) || ""; } catch (e) { return ""; }
  };

  /* Time-based, exactly as `pathrun.health()`: a fetcher that stopped existing leaves
   * `running:true` frozen behind it, and no counter can say "stalled". */
  C.health = function () {
    const age = C.lastAt ? (Date.now() - C.lastAt) / 1000 : null;
    return {
      /* ⛔ `alive` HAS TO COVER THE COLLECT PHASE, and in its first form it did not: `running` is
       * set by `go()` alone, so a fetcher ten minutes into its `/paths` walk reported
       * `alive:false` -- the same false negative `health()` was written to abolish. The collect
       * phase is derived, not a fourth flag: a page counter that has started and not finished. */
      alive: !!((C.running || (C.collectPage && !C.collectDone)) && age !== null && age < 120),
      secondsSinceLastRequest: age === null ? null : Math.round(age),
      i: C.i, of: C.urls.length,
      /* Caught up and waiting for `collect()` to add more, rather than dead. `alive` stays true
       * because the loop is stamping `lastAt` -- this says WHY nothing is moving. */
      idling: !!C.idle, ok: C.ok, fail: C.fail,
      part: C.part, pending: C.rows.length, pace: Math.round(C.pace),
      collectPage: C.collectPage || 0, collectDone: !!C.collectDone,
      finished: C.finished || null,
    };
  };

  /* ⛔ **A `fetch` WITH NO TIMEOUT HANGS THIS LOOP, AND IT HANGS IT SILENTLY.** Measured on
   * the requester the same evening -- `scripts/pathrun.js` had the identical defect and one
   * request that never settled stopped the campaign for 13 minutes with every flag still saying
   * it was running. This half is worse, because `collect()` stamps `lastAt` as it walks: a
   * fetcher parked inside `one()` while a walk is in progress reports `alive:true` and fetches
   * nothing, which is exactly what it did for 45 minutes on 2026-09-17.
   *
   * A browser `fetch` has NO default timeout at all. Without an AbortController the promise can
   * stay pending for ever.
   *
   * 25s is past a slow `/paths` render and well under the 120s `alive` allows, so a stuck
   * request is recorded and stepped over rather than ending the run between two checks. */
  const TIMEOUT_MS = 25000;
  //: How long to wait when the list is exhausted, and how many of those waits before the held
  //: rows are written out. 15s x 4 = one minute of nothing arriving before a file is cut.
  const IDLE_MS = 15000;
  const IDLE_FLUSH = 4;
  async function fetchPage(url) {
    const ctl = new AbortController();
    const timer = setTimeout(() => ctl.abort(), TIMEOUT_MS);
    try {
      const r = await fetch(url, { credentials: "include", redirect: "follow",
                                   signal: ctl.signal });
      /* ⛔ **`r.url` IS THE WHOLE POINT OF THIS FUNCTION AND `r.text()` ALONE THREW IT AWAY.**
       * A `/c/<hash>` permalink carries no `to=` and no `path_type=`; it REDIRECTS to the
       * `/path/` url that does. `redirect: "follow"` was already here, so the parameters were
       * arriving and being discarded one line later. See `C.one`. */
      return { text: await r.text(), url: r.url || url };
    } finally { clearTimeout(timer); }
  }

  const fetchText = async (url) => (await fetchPage(url)).text;

  /* ---------- carry the state between tabs; both tabs are geni.com ---------- */
  /* ⛔ **SEEDING FROM THE FILE IS NOT `collect()` AND MUST NOT CLEAR THE LIST.** `collect()`
   * walks `/paths` newest-first and costs 28 minutes for 30 a page; this takes a batch printed
   * by `scripts/build-chain-batch.py` off `reports/path-permalinks.tsv`, which cost one mbox
   * parse. Both may be in play at once, so this ADDS and de-duplicates rather than assigning --
   * assigning would drop whatever `collect()` had already gathered, and the loop reads `C.i`
   * against a list that had just got shorter. */
  C.seed = function (urls) {
    const seen = new Set(C.urls);
    let added = 0;
    for (const u of urls || []) {
      if (!seen.has(u)) { seen.add(u); C.urls.push(u); added++; }
    }
    console.log("[chains] seeded +" + added + ", " + C.urls.length + " total, at " + C.i);
    return added;
  };

  /* Put the timed-out permalinks back on the end of the list. Returns how many went back.
   * Deliberately manual rather than automatic: a retry inside the loop would re-request during
   * whatever is causing the timeouts, which is the opposite of what the pace rules want. */
  C.reseedFailed = function () {
    const again = C.failed.splice(0, C.failed.length);
    const n = C.seed(again);
    console.log("[chains] reseeded " + n + " previously failed permalinks");
    return n;
  };

  C.save = function () {
    try {
      localStorage.setItem("chains_urls", JSON.stringify(C.urls));
      localStorage.setItem("chains_rows", JSON.stringify(C.rows));
      localStorage.setItem("chains_i", String(C.i));
      localStorage.setItem("chains_part", String(C.part));
      return C.urls.length;
    } catch (e) { console.log("[chains] save failed: " + e); return -1; }
  };
  C.load = function () {
    try {
      const u = localStorage.getItem("chains_urls");
      if (u) C.urls = JSON.parse(u);
      const r = localStorage.getItem("chains_rows");
      if (r) C.rows = JSON.parse(r);
      const i = localStorage.getItem("chains_i");
      if (i) C.i = parseInt(i, 10) || 0;
      const p = localStorage.getItem("chains_part");
      if (p) C.part = parseInt(p, 10) || 0;
      /* The collect phase is over by definition if a url list came back, and `alive` reads
       * collectPage/collectDone -- so say so, or a loaded fetcher reports collectPage 0. */
      if (C.urls.length) { C.collectPage = C.collectPage || 1; C.collectDone = true; }
      return { urls: C.urls.length, rows: C.rows.length, i: C.i, part: C.part };
    } catch (e) { console.log("[chains] load failed: " + e); return null; }
  };

  /* ---------- collect the permalinks off /paths, 30 to a page ---------- */
  /* ⛔ **A SECOND `collect()` RUNS A SECOND WALK, AND ON 2026-09-17 ONE DID.** The 45-minute
   * check re-collects whenever the fetcher has caught up, and it read `idling` to decide --
   * but `idling` is about the FETCH cursor, not about the walk. A collect already 565 pages in
   * left `idling` true, so the check started another, and two loops walked `/paths` at once
   * against the same `C.urls`, both stamping `C.collectPage` (it went 565 -> 5 mid-tick, which
   * is what gave it away). Nothing was lost -- they share the dedupe set -- but it is a doubled
   * request rate at Geni, which is § *RESTARTING IT TWICE RUNS IT TWICE* on the other loop.
   *
   * Same fix as `R.gen`: a generation token, taken at entry and rechecked every page, so only
   * the newest walk continues. And the honest test for *is a walk running* is `collectDone`,
   * never `idling`. */
  C.collect = async function (maxPages) {
    const mine = (C.collectGen = (C.collectGen || 0) + 1);
    /* ⛔ THE CAP HAS TO CLEAR THE LIST, AND ON 2026-09-16 IT STOPPED CLEARING IT. `/paths` is
     * 30 to a page, so 400 pages is 12,000 permalinks -- and the list passed 11,532 that
     * evening, with `collectPage` coming back as exactly 400. The walk is newest-first, so a
     * truncated one still finds every NEW permalink and only clips an already-collected tail;
     * that is why this was harmless rather than a silent loss. It will not stay harmless. */
    maxPages = maxPages || 900;
    const seen = new Set(C.urls);
    let added = 0;
    for (let p = 1; p <= maxPages; p++) {
      let doc;
      try {
        const html = await fetchText("/paths?page=" + p);
        doc = new DOMParser().parseFromString(html, "text/html");
      } catch (e) {
        /* ⛔ A TIMEOUT IS NOT THE END OF THE LIST. `break` here treats one stuck page as
         * "past the last page", which silently truncates the walk and loses every permalink
         * after it. Only an EMPTY page means the end; a failure skips to the next one. */
        if (e && e.name === "AbortError") { C.lastAt = Date.now(); continue; }
        break;
      }
      const hrefs = [...doc.querySelectorAll('a[href*="/path/"]')]
        .map(a => a.getAttribute("href"))
        .filter(h => h && /[?&]to=/.test(h));
      if (!hrefs.length) break;             // past the last page
      for (const h of hrefs) {
        const abs = new URL(h, location.origin).href;
        if (!seen.has(abs)) { seen.add(abs); C.urls.push(abs); added++; }
      }
      /* ⛔ **`collect()` HAS TO BE INSTRUMENTED TOO.** It is a ten-minute walk and it runs
       * unawaited, so without these three fields the fetcher spends its first ten minutes
       * indistinguishable from a fetcher that never started -- the exact ambiguity `health()`
       * exists to remove. `lastAt` is stamped here, and `alive` reads the pair. */
      if (C.collectGen !== mine) {
        console.log("[chains] collect gen " + mine + " superseded at page " + p);
        return added;
      }
      C.collectPage = p;
      C.lastAt = Date.now();
      if (p % 10 === 0) console.log("[chains] page " + p + ", " + C.urls.length + " permalinks");
      await sleep();
    }
    console.log("[chains] collect done: +" + added + ", " + C.urls.length + " total");
    C.collectDone = true;
    return added;
  };

  /* ---------- one permalink -> rows ---------- */
  /* ⛔ **TWO URL SHAPES REACH HERE AND ONLY ONE CARRIES THE PARAMETERS.**
   *
   *     /path/index?from=..&to=..&path_type=..   collected off `/paths`
   *     /c/<64 hex>                              the permalink Geni EMAILS
   *
   * The second is 47,692 of them -- `reports/path-permalinks.tsv`, harvested out of the Takeout
   * mbox -- and it has no `to=` at all. Reading `to` off the REQUEST url gives every one of them
   * a blank `to_id`, and `split-path-chains.py` keys chains on `(to_id, kind)` and names the
   * GEDCOM `harvested-path-geni-<to_id>-<kind>`, so a blank one does not fail: it silently
   * collapses every chain into one bucket. The redirect target is where the parameters live.
   *
   * Three sources, in falling order of authority: the request url, the FINAL url after the
   * redirect, and -- if Geni ever stops putting them in the query string -- the last segment of
   * the rendered chain, which is the target by construction. */
  C.one = async function (url) {
    const res = await fetchPage(url);
    const final = res.url || url;
    let to_id = qp(url, "to") || qp(final, "to");
    const kind = (qp(url, "path_type") || qp(final, "path_type") || "blood")
                   .replace("inlaw", "in-law");
    const doc = new DOMParser().parseFromString(res.text, "text/html");
    if (!to_id) {
      const ids = [...doc.querySelectorAll("span.segment [data-profile-id]")];
      to_id = ids.length ? (ids[ids.length - 1].getAttribute("data-profile-id") || "") : "";
    }
    const out = [];
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
    // A permalink that rendered no segments is RECORDED, not dropped: `step -1` / `EMPTY` bounds
    // the absence instead of leaving it silent, and merge-path-chains.py keeps those rows.
    if (!out.length) out.push([to_id, kind, "-1", "", "", "EMPTY"]);
    return out;
  };

  /* ---------- dump what has accumulated ---------- */
  C.dump = function () {
    if (!C.rows.length) return 0;
    const head = "to_id\tkind\tstep\tprofile_id\tname\trelation\n";
    const body = C.rows.map(r => r.join("\t")).join("\n") + "\n";
    const a = document.createElement("a");
    a.href = URL.createObjectURL(new Blob([head + body], { type: "text/tab-separated-values" }));
    C.part++;
    a.download = "path-chains-" + String(C.part).padStart(3, "0") + ".tsv";
    document.body.appendChild(a); a.click(); a.remove();
    const n = C.rows.length;
    C.rows = [];
    console.log("[chains] wrote part " + C.part + ", " + n + " rows");
    return n;
  };

  C.go = async function () {
    if (!C.urls.length) { console.log("[chains] no urls -- await window.__chains.collect() first"); return; }
    const mine = C.gen;
    C.running = true;
    C.finished = null;
    let since = 0;
    while (C.running && C.gen === mine) {
      /* ⛔ **CATCHING UP IS NOT FINISHING, AND EXITING HERE COSTS A RESTART EVERY TICK.**
       * The requester queues searches far faster than Geni resolves them, so this loop reaches
       * the end of the list routinely -- it drained on three consecutive 45-minute checks on
       * 2026-09-17, each time setting `finished` and reporting `alive:false`, which reads as a
       * dead fetcher and cost a manual restart every time.
       *
       * The list is not a fixed job. It GROWS underneath this loop whenever `collect()` walks
       * `/paths` again, so the honest behaviour at the end is to WAIT, not to stop. `lastAt` is
       * stamped while waiting so `alive` keeps telling the truth: the loop is up, there is
       * simply nothing to fetch this second.
       *
       * The tail is flushed before waiting, so a pause never leaves rows sitting in the page --
       * the same reason the old exit called `dump()`. */
      if (C.i >= C.urls.length) {
        C.idle = (C.idle || 0) + 1;
        /* ⛔ **FLUSH ONCE THE PAUSE LOOKS REAL, NOT THE MOMENT IT CATCHES UP.** Flushing on
         * every catch-up wrote a file per handful: parts 196-207 came out at 2-15 KB against
         * the 500 KB a full part is, because the loop was fetching three or four chains, running
         * out, and dumping again fifteen seconds later.
         *
         * `IDLE_FLUSH` ticks of nothing to do means the trickle has genuinely stopped, and
         * `since` is zeroed after, so a long wait produces exactly one file rather than one per
         * tick. Work arriving before then simply carries on accumulating. */
        if (since && C.idle >= IDLE_FLUSH) { C.dump(); since = 0; }
        C.lastAt = Date.now();
        await new Promise((r) => setTimeout(r, IDLE_MS));
        continue;
      }
      C.idle = 0;
      try {
        C.rows.push(...await C.one(C.urls[C.i]));
        C.ok++;
        C.paceDown();
      } catch (e) {
        C.fail++;
        C.lastErr = String(e).slice(0, 80);
        C.failed.push(C.urls[C.i]);
        C.paceUp();
      }
      C.lastAt = Date.now();
      C.i++;
      since++;
      try { localStorage.setItem("chains_cursor", String(C.i)); } catch (e) {}
      if (since >= C.every) { C.dump(); since = 0; }
      await sleep();
    }
    if (C.gen === mine) {
      C.dump();                              // never leave the tail sitting in the page
      C.running = false;
      C.finished = new Date().toISOString();
      console.log("[chains] stopped at " + C.i + "/" + C.urls.length);
    }
  };
})();
"pathchains loaded -- await window.__chains.collect() then window.__chains.go()";
