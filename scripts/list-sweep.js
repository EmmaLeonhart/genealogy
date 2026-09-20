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
    queue: [], startedAt: new Date().toISOString(), lastAt: Date.now()
  };
  window.__listsweep = S;

  const STAGGER = 1800;      /* per page. Geni is hostile; 500 back-to-back reads have CAPTCHAd
                              * this account twice. */
  const BETWEEN = 4000;      /* between people, on top of the page stagger. */
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

  async function person(focus, base) {
    const out = [], seen = new Set();
    let pages = 1;
    S.who = focus; S.page = 0; S.pages = 0;
    for (let n = 1; S.running; n++) {
      S.page = n; S.lastAt = Date.now();
      const body = new URLSearchParams(Object.assign({}, base, {
        focus_id: focus, page: String(n), group: "descendants"
      }));
      let doc;
      try {
        const r = await fetch("/list/index", {
          method: "POST", credentials: "include", body: body,
          headers: { "Content-Type": "application/x-www-form-urlencoded" }
        });
        if (!r.ok) throw new Error("HTTP " + r.status);
        doc = new DOMParser().parseFromString(await r.text(), "text/html");
      } catch (e) {
        S.fail++; S.lastFail = focus + " p" + n + " " + String((e && e.message) || e);
        break;
      }
      if (n === 1) {
        const c = (doc.body.textContent.match(/of ([\d,]+) people/) || [, ""])[1];
        pages = c ? Math.ceil(parseInt(c.replace(/,/g, ""), 10) / 20) : 1;
        S.pages = pages;
      }
      parse(doc, focus, n, out, seen);
      S.rows = out.length;
      if (n >= pages) break;
      await new Promise(function (r) { setTimeout(r, STAGGER); });
    }
    /* A person with no descendants is a real answer, not a failure -- ruled 2026-09-19,
     * *"smaller exports leaking in are self healing and still give info"*. Written anyway,
     * so the sweep never re-asks. */
    if (!out.length) S.empty++;
    save(focus, out);
    S.done++;
  }

  S.health = function () {
    return { running: S.running, i: S.i, of: S.of, who: S.who, page: S.page, pages: S.pages,
             rows: S.rows, done: S.done, empty: S.empty, fail: S.fail, lastFail: S.lastFail,
             alive: S.running && (Date.now() - S.lastAt) < 120000 };
  };
  S.stop = function () { S.running = false; return "stopping after " + S.who; };

  S.start = async function (ids) {
    S.queue = ids.slice(); S.of = S.queue.length; S.running = true;
    const gen = S.gen;
    const base = baseFields();
    if (!base) { S.running = false; return "no paging form -- load a /list page first"; }
    for (let k = 0; k < S.queue.length && S.running && gen === S.gen; k++) {
      S.i = k + 1;
      try { await person(S.queue[k], base); }
      catch (e) { S.fail++; S.lastFail = S.queue[k] + " " + String((e && e.message) || e); }
      await new Promise(function (r) { setTimeout(r, BETWEEN); });
    }
    S.running = false;
    return "sweep finished: " + S.done + " people";
  };

  return "loaded; call __listsweep.start([...ids])";
})()
