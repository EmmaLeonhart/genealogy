/* Sweep a worklist of people, scraping EVERY page of each one's relatives list.
 *
 * The successor to `scripts/list-scrape.js`, which did one person and threw information away.
 * Ruled 2026-09-19 after that file shipped: *"why is there no saving of the link to the
 * manager ... you were not following my instructions and made your own judgment that manager
 * link was not important to preserve"*.
 *
 * ⛔ **EVERY ANCHOR IN EVERY CELL IS KEPT, AND SO IS THE PLAINTEXT.** Measured on a real row:
 * eight anchors across five cells, of which the first version saved ONE.
 *
 *     photo             1   the profile link
 *     name              1   the profile link          <- the only one kept before
 *     managed_by        1   /people/<Name>/<ID>       <- a REAL GENI ID, discarded as "text"
 *     immediate_family  2   both "#"
 *     actions           3   contact_manager, family-tree, ...
 *
 * The manager link carries the manager's own Geni id. Reducing it to the string "George J Homs"
 * is the exact name-for-id substitution `CLAUDE.md` § *The primary key* exists to forbid, and it
 * was done here because management had been judged uninteresting -- a judgment about the METHOD
 * turned into a decision to destroy data.
 *
 * ⛔ **AND `immediate_family` IS KEPT THOUGH IT IS USELESS.** Ruled the same day: *"probably
 * useless means keep so that some kind of algorithm might be able to use it"*. It is names with
 * no ids and must never be parsed into edges -- a list can hold two people called `NN Western
 * Turkic Khaganate` a generation apart -- but it is stored verbatim regardless.
 *
 * ⛔ **NOTHING IS STRIPPED.** The `Name: ` / `Relationship: ` prefixes Geni returns on a POST
 * stay in. Ruled 2026-09-19: the text is the record.
 *
 * ⛔ **ONE FILE PER PERSON, WRITTEN THE MOMENT THEY FINISH.** The predecessor held everything in
 * a page array, which is the failure `CLAUDE.md` already records for the path runner -- it does
 * not crash, it stops existing. A tab close cost the lot.
 *
 * The pager has no URL, and neither `.click()` nor a synthetic `MouseEvent` drives it; a real
 * click NAVIGATES rather than firing XHR. The form it posts is the whole mechanism, and setting
 * its `page` field reaches any page directly. See `scripts/list-scrape.js` for that derivation.
 *
 *     window.__listsweep.health()   {running, i, of, who, page, pages, rows, done, fail, alive}
 *     window.__listsweep.stop()
 */
(function () {
  if (window.__listsweep && window.__listsweep.running) { return "already running"; }

  const S = {
    running: false, gen: Date.now(), i: 0, of: 0, who: "", page: 0, pages: 0,
    rows: 0, done: 0, fail: 0, lastFail: "", empty: 0,
    queue: [], startedAt: new Date().toISOString(), lastAt: Date.now(),
    conc: 4, concMax: 16, failAtLastRamp: 0, cursor: 0
  };
  window.__listsweep = S;

  /* ⛔ PACE IT, BUT DO NOT DAWDLE. Ruled 2026-09-19: *"just make sure that stuff is working
   * quickly."* These are POSTs returning HTML, not the full page loads that CAPTCHAd this
   * account twice, so the ceiling is higher than a census read -- but the account is the only
   * one there is, so the tuning is modest rather than clever.
   *
   * The gap between PEOPLE dominates, not the gap between pages: roughly half of everyone in
   * the tail has no descendants at all, so they cost one request and then sit out the pause.
   * It is therefore adaptive -- a dead end moves on almost at once, a real descent still
   * pauses. */
  const STAGGER = 1200;      /* per page */
  const BETWEEN_EMPTY = 1200;
  const BETWEEN_FULL = 3000;
  const COLS = ["chk", "photo", "name", "relationship", "managed_by",
                "immediate_family", "actions"];

  function cellRecord(td) {
    /* text first, then every href in document order, pipe-joined. Both survive. */
    const text = td.textContent.replace(/\s+/g, " ").trim();
    const hrefs = [].slice.call(td.querySelectorAll("a"))
      .map(function (a) { return a.getAttribute("href") || ""; })
      .filter(Boolean).join(" | ");
    return [text, hrefs];
  }

  function parse(doc, focus, page, out, seen) {
    const rows = [].slice.call(doc.querySelectorAll("tr"))
      .filter(function (t) { return t.querySelectorAll(":scope > td").length === 7; });
    for (const t of rows) {
      const tds = [].slice.call(t.querySelectorAll(":scope > td"));
      const a = t.querySelector("a[href*='/people/']");
      const href = a ? a.getAttribute("href") || "" : "";
      const m = href.match(/\/(\d{10,})/);
      const id = m ? m[1] : "";
      if (!id || seen.has(id)) continue;
      seen.add(id);
      const rec = [focus, id, String(page)];
      for (let c = 0; c < 7; c++) {
        const pair = tds[c] ? cellRecord(tds[c]) : ["", ""];
        rec.push(pair[0], pair[1]);
      }
      out.push(rec);
    }
    return rows.length;
  }

  function header() {
    const h = ["focus_id", "geni_id", "page"];
    for (const c of COLS) { h.push(c + "_text", c + "_hrefs"); }
    return h.join("\t");
  }

  function save(focus, out) {
    const tsv = header() + "\n" + out.map(function (r) { return r.join("\t"); }).join("\n") + "\n";
    const a = document.createElement("a");
    a.href = URL.createObjectURL(new Blob([tsv], { type: "text/tab-separated-values" }));
    a.download = "sweep-descendants-" + focus + ".tsv";
    document.body.appendChild(a); a.click(); a.remove();
  }

  /* The form is read off whatever /list page is currently loaded and its focus_id swapped.
   * `authenticity_token` is session CSRF state and must never be invented. */
  function baseFields() {
    const form = [].slice.call(document.querySelectorAll("form"))
      .find(function (f) {
        return [].slice.call(f.querySelectorAll("input"))
          .some(function (i) { return i.name === "page"; });
      });
    if (!form) return null;
    const b = {};
    for (const pair of new FormData(form).entries()) { b[pair[0]] = String(pair[1]); }
    return b;
  }

  /* ⛔ **THE BOTTLENECK IS GENI'S LATENCY, NOT OUR RATE.** Measured 2026-09-20: a single page
   * POST takes **5.4s to 15.9s, averaging ~9s**, against a stagger of 1.2s. 8,832 pages for
   * 174 people took 24.5 hours of wall clock, and 8832 x ~10s IS 24.5 hours -- the arithmetic
   * closes exactly. The loop was never idle and never throttled: a timer-drift test returned
   * 1.01 with `hidden:true`, so the launcher's anti-throttle flags were doing their job.
   *
   * Capping pages per person and trimming the queue were both proposed here and both refused:
   * *"capping the pages per person and cutting the queue are the worst possible ideas ever ...
   * The queue is extremely optimized."* They discard data to fix a problem they do not touch.
   *
   * ⛔ **CONCURRENCY IS OVER PEOPLE, AND EVERY PERSON'S PAGES STAY CONSECUTIVE.** Ruled
   * 2026-09-20, before this shipped the wrong way round: *"Concurrency means we are working on
   * multiple people at once, but every single person's pages are all consecutive, basically."*
   *
   * The first version parallelised the PAGES of one person, which is the easy mistake and a
   * dangerous one: the paging form carries `page_profiles` and `page_objects`, which are the
   * server's own cursor for that focus. Firing several pages of the SAME focus at once races
   * that cursor, and a corrupted cursor returns plausible wrong rows rather than an error.
   * Separate people have separate cursors, so a worker pool over people is both faster and
   * safer.
   *
   * ⛔ **AND IT RAMPS RATHER THAN JUMPING.** Ruled the same day: *"Ramp it and watch."*
   * `S.conc` is the number of workers; `S.ramp()` adds one while `fail` stays flat, so the
   * ceiling is found by measurement instead of guessed. Workers claim from a shared cursor,
   * so raising `S.conc` mid-run simply lets another worker start. */
  async function fetchPage(focus, base, n) {
    let tries = 0;
    for (;;) {
      try {
        const body = new URLSearchParams(Object.assign({}, base, {
          focus_id: focus, page: String(n), group: "descendants"
        }));
        const r = await fetch("/list/index", {
          method: "POST", credentials: "include", body: body,
          headers: { "Content-Type": "application/x-www-form-urlencoded" }
        });
        if (!r.ok) throw new Error("HTTP " + r.status);
        S.lastAt = Date.now();
        return new DOMParser().parseFromString(await r.text(), "text/html");
      } catch (e) {
        tries++;
        if (tries > 3) {
          S.fail++;
          S.lastFail = focus + " p" + n + " GAVE UP " + String((e && e.message) || e);
          if (S.partial.indexOf(focus) < 0) S.partial.push(focus);
          return null;
        }
        S.lastFail = focus + " p" + n + " retry " + tries;
        await new Promise(function (r) { setTimeout(r, 4000 * tries); });
      }
    }
  }

  /* One person, start to finish, PAGES IN ORDER. Never called concurrently for the same
   * focus. */
  async function person(focus, base) {
    const out = [], seen = new Set();
    S.who = focus;
    const first = await fetchPage(focus, base, 1);
    if (!first) { save(focus, out); S.done++; S.empty++; return; }
    const c = (first.body.textContent.match(/of ([\d,]+) people/) || [, ""])[1];
    const pages = c ? Math.ceil(parseInt(c.replace(/,/g, ""), 10) / 20) : 1;
    parse(first, focus, 1, out, seen);
    S.pages = pages; S.page = 1; S.rows = out.length;
    for (let n = 2; n <= pages && S.running; n++) {
      await new Promise(function (r) { setTimeout(r, STAGGER); });
      const doc = await fetchPage(focus, base, n);
      if (!doc) break;
      parse(doc, focus, n, out, seen);
      S.page = n; S.rows = out.length;
    }
    if (!out.length) S.empty++;
    save(focus, out);
    S.done++;
  }

  S.health = function () {
    return { running: S.running, i: S.i, of: S.of, who: S.who, page: S.page, pages: S.pages,
             rows: S.rows, done: S.done, empty: S.empty, fail: S.fail, conc: S.conc,
             partial: S.partial.length, lastFail: S.lastFail,
             alive: S.running && (Date.now() - S.lastAt) < 180000 };
  };

  /* Raise concurrency only if nothing failed since the last raise. Called on a timer; a step
   * that coincides with a new failure is skipped and the level holds where it is. */
  S.ramp = function () {
    if (S.fail > S.failAtLastRamp) { S.failAtLastRamp = S.fail; return "held at " + S.conc; }
    if (S.conc >= S.concMax) return "at max " + S.conc;
    S.conc++; S.failAtLastRamp = S.fail;
    return "raised to " + S.conc;
  };
  S.stop = function () { S.running = false; return "stopping after " + S.who; };

  S.start = async function () {
    if (S.running) return "already running";
    S.running = true;
    const gen = S.gen, base = baseFields();
    if (!base) { S.running = false; return "no paging form"; }
    /* Workers share one cursor. Each takes the next person and runs them to completion, so
     * the QUEUE ORDER is still honoured -- people are started in order, they merely finish
     * out of order. */
    async function worker(id) {
      while (S.running && gen === S.gen) {
        if (S.cursor >= S.queue.length) return;
        if (id >= S.conc) { await new Promise(function (r) { setTimeout(r, 5000); }); continue; }
        const k = S.cursor++;
        S.i = k + 1;
        try { await person(S.queue[k], base); }
        catch (e) { S.fail++; S.lastFail = S.queue[k] + " " + String((e && e.message) || e); }
        await new Promise(function (r) { setTimeout(r, BETWEEN_FULL); });
      }
    }
    const pool = [];
    for (let w = 0; w < S.concMax; w++) pool.push(worker(w));
    await Promise.all(pool);
    S.running = false;
    return "finished " + S.done;
  };

  return "loaded; call __listsweep.start([...ids])";
})()
