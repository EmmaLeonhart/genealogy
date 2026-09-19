/* Scrape a Geni relatives list -- every row of all its pages -- with no export and no profile
 * creation.
 *
 * `https://www.geni.com/list?focus_id=<ID>&group=descendants` shows up to **15,000** people,
 * 20 to a page, 750 pages. It is the cheapest source of a person's descent that Geni has: it
 * creates nothing, it does not touch the one-at-a-time export slot, and it works on ANY profile
 * regardless of who manages it -- `request_export` is the thing that cares about management, and
 * this is not that.
 *
 * ⛔ **THE PAGER HAS NO URL AND SYNTHETIC CLICKS DO NOT DRIVE IT.** Every pager anchor is
 * `href="#"`; `&page=N` on the GET does nothing. `.click()` does nothing and a hand-built
 * `MouseEvent` with bubbles, coordinates and button does nothing either -- the handler wants a
 * trusted event. Measured 2026-09-19, all three.
 *
 * ⛔ **BUT IT IS A FORM POST, AND A FORM POST IS ADDRESSABLE.** A real click navigates rather
 * than firing XHR, which is why hooking `fetch` and `XMLHttpRequest` captured NOTHING while the
 * counter advanced. The page carries a form holding the whole paging state:
 *
 *     POST /list/index
 *       authenticity_token  id  list_type=ProfileList  list_id
 *       focus_id  page_profiles  page_objects
 *       mode=view  page=<N>  order=relationship  order_type=asc
 *       export_format  process_list=false  group=descendants
 *
 * Setting `page` to any value and posting it returns that page. Verified by jumping straight to
 * `page=750`, which came back `14981-15000 of 15000`. So the 750 pages cost 750 posts and no
 * mouse events at all.
 *
 * ⛔ **SAVE THE WHOLE ROW.** Ruled 2026-09-19: *"We save every single row with all of its
 * information, the link and the text."* Every cell, plus the profile href. Do not filter by
 * manager, do not keep only the id, and do not try to parse the Immediate Family prose into
 * edges -- it carries **names only, zero anchors in all 20 cells**, and this very list holds two
 * different people called `NN Western Turkic Khaganate` one generation apart. Joining on that is
 * the fuzzy name match `CLAUDE.md` § *The primary key* forbids.
 *
 * The edges come from the path requester afterwards, not from here. This file only gets the SET.
 *
 *     window.__listscrape.health()    {running, page, of, rows, fail, alive}
 *     window.__listscrape.save()      write the TSV to Downloads
 *     window.__listscrape.stop()
 */
(function () {
  if (window.__listscrape && window.__listscrape.running) {
    console.log("[listscrape] already running -- stop() first"); return;
  }

  /* ⛔ The form is read off the LIVE page, never reconstructed. `authenticity_token` is a CSRF
   * token tied to this session and `page_profiles`/`page_objects` are the server's own cursor
   * state; inventing any of them is how a scrape starts posting nonsense that returns 200. */
  const form = [...document.querySelectorAll("form")]
    .find((f) => [...f.querySelectorAll("input")].some((i) => i.name === "page"));
  if (!form) { console.log("[listscrape] no paging form -- is this a /list page?"); return; }

  const base = {};
  for (const [k, v] of new FormData(form).entries()) base[k] = String(v);

  const R = {
    running: true, page: 0, of: 0, rows: 0, fail: 0, lastFail: "", gen: Date.now(),
    out: [], seen: new Set(), startedAt: new Date().toISOString(), lastAt: Date.now()
  };
  window.__listscrape = R;

  const STAGGER = 1800;   /* Geni is hostile and 500 back-to-back reads have CAPTCHAd this
                           * account twice. This is one request per page, not per person. */

  function parse(doc, page) {
    /* A data row has exactly SEVEN direct `td`. The page also emits a one-cell alternate-layout
     * copy of every row whose text is prefixed `Name: ... Relationship: ...`; counting those
     * doubles everything. */
    const rows = [...doc.querySelectorAll("tr")]
      .filter((t) => t.querySelectorAll(":scope > td").length === 7);
    let added = 0;
    for (const t of rows) {
      const cells = [...t.querySelectorAll(":scope > td")]
        .map((td) => td.textContent.replace(/\s+/g, " ").trim());
      const a = t.querySelector('a[href*="/people/"]');
      const href = a ? a.getAttribute("href") || "" : "";
      const m = href.match(/\/(\d{10,})/);
      const id = m ? m[1] : "";
      if (!id || R.seen.has(id)) continue;
      R.seen.add(id);
      R.out.push([id, String(page), cells[2] || "", cells[3] || "", cells[4] || "",
                  cells[5] || "", href]);
      added++;
    }
    return added;
  }

  async function fetchPage(n) {
    const body = new URLSearchParams(Object.assign({}, base, { page: String(n) }));
    const r = await fetch("/list/index", {
      method: "POST", credentials: "include", body,
      headers: { "Content-Type": "application/x-www-form-urlencoded" }
    });
    if (!r.ok) throw new Error("HTTP " + r.status);
    const doc = new DOMParser().parseFromString(await r.text(), "text/html");
    const c = (doc.body.textContent.match(/of ([\d,]+) people/) || [, ""])[1];
    if (c) R.of = Math.ceil(parseInt(c.replace(/,/g, ""), 10) / 20);
    return parse(doc, n);
  }

  R.health = function () {
    return { running: R.running, page: R.page, of: R.of, rows: R.out.length, fail: R.fail,
             lastFail: R.lastFail,
             /* time-based, because a loop that stopped existing leaves running:true behind it */
             alive: R.running && (Date.now() - R.lastAt) < 60000 };
  };
  R.stop = function () { R.running = false; return "stopped at page " + R.page; };
  R.save = function () {
    const head = ["geni_id", "page", "name", "relationship", "managed_by",
                  "immediate_family", "href"].join("\t");
    const tsv = head + "\n" + R.out.map((r) => r.join("\t")).join("\n") + "\n";
    const a = document.createElement("a");
    a.href = URL.createObjectURL(new Blob([tsv], { type: "text/tab-separated-values" }));
    a.download = "list-" + (base.group || "list") + "-" + (base.focus_id || "x") + ".tsv";
    document.body.appendChild(a); a.click(); a.remove();
    return R.out.length + " rows";
  };

  (async function pump(gen) {
    for (let n = 1; R.running && gen === R.gen; n++) {
      R.page = n; R.lastAt = Date.now();
      try { await fetchPage(n); }
      catch (e) { R.fail++; R.lastFail = "p" + n + " " + String((e && e.message) || e); }
      if (R.of && n >= R.of) break;
      await new Promise((r) => setTimeout(r, STAGGER));
    }
    R.running = false;
    console.log("[listscrape] done: " + R.out.length + " rows, " + R.fail + " failures");
  })(R.gen);

  console.log("[listscrape] started; health() / save() / stop()");
})();
