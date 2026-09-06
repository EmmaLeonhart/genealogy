/* Shared state reading for every job.
 *
 * ONE RULE GOVERNS THIS FILE: the state must be read off the RENDERED page, never off the
 * DOM text. `geni-paths/README.md` records the cost of getting it wrong -- a hidden
 *
 *     <div id="path_search_response" style="...display:none;">Path search in progress. ...
 *
 * sits on EVERY profile before any search is requested, so `innerText` matching reported 22
 * untouched profiles as running when not one had been asked for. The same sentence baked into
 * `harvest-isolate-paths.pending()` as a substring test made every genuine miss leave the
 * reach-rate denominator, so the rate could only come out 100%.
 *
 * An extension is the right place for this precisely because it can ask the question the file
 * cannot answer: `offsetParent` and a non-zero box are real visibility, live, in the page.
 */

const GC = {};

GC.visible = function (el) {
  if (!el) return false;
  if (!el.offsetParent && getComputedStyle(el).position !== "fixed") return false;
  const r = el.getBoundingClientRect();
  return r.height > 0 && r.width > 0;
};

GC.byText = function (selector, re) {
  return [...document.querySelectorAll(selector)]
    .filter((e) => re.test(e.textContent || e.value || ""));
};

GC.sleep = (ms) => new Promise((r) => setTimeout(r, ms));

/* Wait until `test()` is true, or give up. Resolution is driven by a MutationObserver so the
 * moment Geni writes the answer in is the moment we act -- the whole reason this is an
 * extension. The interval is a backstop for changes that do not mutate the observed subtree. */
GC.until = function (test, timeoutMs) {
  return new Promise((resolve) => {
    if (test()) return resolve(true);
    let done = false;
    const finish = (v) => {
      if (done) return;
      done = true;
      obs.disconnect();
      clearInterval(iv);
      clearTimeout(to);
      resolve(v);
    };
    const check = () => { if (test()) finish(true); };
    const obs = new MutationObserver(check);
    obs.observe(document.documentElement,
      { childList: true, subtree: true, attributes: true, characterData: true });
    const iv = setInterval(check, 1000);
    const to = setTimeout(() => finish(false), timeoutMs);
  });
};

/* The four states `geni-paths/README.md` names, plus the one it calls an isolate.
 *
 * `no_panel` is NOT a miss: a profile carrying no relationship box at all is what an isolate
 * looks like, and the harvester's docstring is explicit that a blank chain is `chain_found=0`
 * and never *unrelated*. */
GC.pathState = function () {
  const ask = GC.byText("a,button,input", /how are (they|you) related/i).find(GC.visible);
  const running = GC.visible(document.getElementById("path_search_response"));
  const none = GC.byText("*", /no blood relationship was found|the relationship could not be found/i)
    .filter((e) => e.children.length === 0).some(GC.visible);
  const segs = document.querySelectorAll("span.segment > span.name a[data-profile-id]").length;
  const rd = document.querySelector("#relation_description, .relation_description");

  if (none) return { state: "resolved_none", segs };
  if (running) return { state: "running", segs };
  if (ask) return { state: "not_requested", segs, ask: true };
  if (segs > 0 && rd) return { state: "resolved_path", segs };
  if (!rd && segs === 0) return { state: "no_panel", segs };
  return { state: "unknown", segs };
};

/* Geni's own prose summary -- the residual `CLAUDE.md` insists is kept beside the steps,
 * because no step word ever says *half* and this does. Stored as-is, never parsed. */
GC.relationDescription = function () {
  const el = document.querySelector("#relation_description, .relation_description");
  return el ? (el.innerText || "").replace(/\s+/g, " ").trim() : "";
};

/* The statistics block, for `reports/isolates.csv`.
 *
 * A MISSING ROW MEANS ZERO and must be recorded as 0 -- Emma, on Dorothy Jeakins: *"ancestors
 * are not mentioned at all because she has no ancestors and geni is weird and gives zero as not
 * an option there"*. A blank later reads as *we failed to scrape it*, which is the
 * absent-versus-zero confusion that costs this repo real numbers elsewhere.
 *
 * 15,000 (or 5,000) is a CEILING, not a count. Her rule: any of these numbers at the cap means
 * the query exceeded its maximum, and is the STRONGEST evidence of world-tree connection there
 * is -- so a "no path found" sitting beside one is a database failure, not a negative result. */
GC.statistics = async function () {
  const want = ["family tree", "blood relatives", "ancestors", "descendants", "followers"];

  /* ⛔ WAIT FOR THE BLOCK, or every number is a fabricated zero.
   *
   * Found 2026-09-05 on the pilot's first target: this returned 0 for all five while the page
   * plainly read *Family Tree 1,896 / Blood Relatives 18 / Ancestors 2 / Descendants 7*. The
   * regexes were right -- run again by hand a moment later they matched every one. It was
   * called too early: the sidebar renders after the relationship box does.
   *
   * That is worse than an ordinary bug here, because of the rule it collides with. Emma, on
   * Dorothy Jeakins: *"ancestors are not mentioned at all because she has no ancestors and geni
   * is weird and gives zero as not an option there"* -- so a MISSING ROW MEANS ZERO and gets
   * recorded as 0. An extractor that returns zeros because it ran early is therefore
   * indistinguishable from a person who genuinely has none, and the zeros go into
   * `reports/isolates.csv` as measurements. `CLAUDE.md` § *check the separator before believing
   * a distribution* is the family; the absent-versus-zero confusion is the specific trap.
   *
   * So `read` says whether the block was there at all. A row missing from a block that IS
   * present is a real zero; a block that never appeared is not data. */
  /* ⛔ THE SENTINEL IS THE NUMBER, NOT THE LABEL. Waiting for the words *Family Tree* returned
   * true instantly and still read zeros: those words are also a NAVIGATION label on the same
   * page, so the wait was satisfied by the menu while the statistics block had not rendered.
   * Exactly the shape of the hidden `path_search_response` template -- a sentinel that is not
   * the thing it stands for, answering yes for the wrong element. Waiting for a digit after the
   * label waits for the datum itself. */
  const seen = () => /family[ ]tree[^0-9]{0,20}[0-9]/i.test(
    document.body ? document.body.innerText : "");
  await GC.until(seen, 20000);
  if (!seen()) return { read: false };

  const out = { read: true };
  const text = document.body.innerText;
  for (const k of want) {
    const key = k.replace(/ /g, "_");
    const re = new RegExp(k.replace(/ /g, "[ ]") + "[^0-9]{0,20}([0-9][0-9,]*)", "i");
    const m = text.match(re);
    /* Present block, absent row -> 0, which is her rule. Never blank: a blank later reads as
     * "we failed to scrape it", which is the confusion this whole comment exists against. */
    out[key] = m ? parseInt(m[1].replace(/,/g, ""), 10) : 0;
  }
  return out;
};

/* The proven save. `geni-paths/README.md` -- and the transcript it names -- do it exactly this
 * way: a Blob of `document.documentElement.outerHTML` clicked through an `<a download>`, landing
 * in ~/Downloads to be filed by `scripts/file-geni-downloads.py`.
 *
 * `<a download>` strips path separators, so the file cannot be written into a subfolder from
 * here. That is why filing is a separate step and not a nicety. */
GC.saveBlob = function (name, text, mime) {
  const b = new Blob([text], { type: mime || "text/html" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(b);
  a.download = name;
  document.body.appendChild(a);
  a.click();
  setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 10000);
};

/* ⛔ A MARKER THE PAGE CAN SEE, so "is the extension loaded?" is answerable in one line.
 *
 * A content script runs in an ISOLATED world: nothing it defines -- `GC` included -- is visible
 * to code running in the page, so there is no way to tell a loaded extension from an absent one
 * by looking at `window`. Chrome's own `Preferences` file does not record a `--load-extension`
 * extension either, and `chrome://extensions` is unreachable from the automation surface.
 *
 * That gap cost real time on 2026-09-05: the extension sat unloaded for a whole session while
 * work was done agentically around it, and the question was answered by asking Emma rather than
 * by checking. An attribute on the documentElement crosses the isolated-world boundary, because
 * the DOM is shared. `document.documentElement.dataset.geniCollector` is now the check. */
document.documentElement.setAttribute("data-geni-collector", "1.0.0");
