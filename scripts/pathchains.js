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
 *     step 2   await window.__chains.collect()   -- walk /paths, gather permalinks
 *              or window.__chains.load()         -- take them off localStorage instead
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

  const sleep = () => new Promise(s => setTimeout(s, 1100 + Math.random() * 700));
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
      i: C.i, of: C.urls.length, ok: C.ok, fail: C.fail,
      part: C.part, pending: C.rows.length,
      collectPage: C.collectPage || 0, collectDone: !!C.collectDone,
      finished: C.finished || null,
    };
  };

  /* ---------- carry the state between tabs; both tabs are geni.com ---------- */
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
  C.collect = async function (maxPages) {
    maxPages = maxPages || 400;
    const seen = new Set(C.urls);
    let added = 0;
    for (let p = 1; p <= maxPages; p++) {
      let doc;
      try {
        const html = await fetch("/paths?page=" + p, { credentials: "include" }).then(r => r.text());
        doc = new DOMParser().parseFromString(html, "text/html");
      } catch (e) { break; }
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
  C.one = async function (url) {
    const to_id = qp(url, "to");
    const kind = (qp(url, "path_type") || "blood").replace("inlaw", "in-law");
    const html = await fetch(url, { credentials: "include", redirect: "follow" }).then(r => r.text());
    const doc = new DOMParser().parseFromString(html, "text/html");
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
    while (C.running && C.gen === mine && C.i < C.urls.length) {
      try {
        C.rows.push(...await C.one(C.urls[C.i]));
        C.ok++;
      } catch (e) { C.fail++; C.lastErr = String(e).slice(0, 80); }
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
      console.log("[chains] done at " + C.i + "/" + C.urls.length);
    }
  };
})();
"pathchains loaded -- await window.__chains.collect() then window.__chains.go()";
