/* Forest exports on every profile this account created on a given day.
 *
 * Ruled 2026-09-18: *"do forest exports on all of the people that I created today"*.
 *
 * The roster comes from Geni's own built-in list, NOT from anything derived here:
 *
 *     https://www.geni.com/list?list_id=added_by_me
 *
 * which is newest-first and carries an `Added on` column reading `Today` / `Yesterday`.
 * Page until a page holds no `Today` and the set is complete rather than sampled.
 *
 * ⛔ **REFUTED SAME DAY: "A FOREST SHOWS NO ROW WHILE IT BUILDS" WAS AN INVENTION.**
 * This file first claimed that a Forest submit legitimately returns no task id and no
 * row on https://www.geni.com/gedcom until it completes. That was wrong, and the
 * disproof was already on the page it was written from: NN de Secadura Alvarado
 * appeared on the dashboard at 2:17 PM WHILE STILL BUILDING. **A row appears when a
 * request is ACCEPTED. No row means the request was refused.**
 *
 * Eleven submits between 15:56 and 16:17 produced no row between them -- NN Onarheim,
 * Turid Gissursdatter, Alvhild Tumesdatter, Ingemund Grimsson's Forest, Ancestors and
 * Descendants, NN NN, Ragnvald, Ole Motland, Helga Vestre Bore, Rasmus Kjosavik. Every
 * one rendered "<their own name>'s GEDCOM File is Being Created" and every one was void.
 *
 * ⛔ **SO THE HEADING IS NOT A CONFIRMATION, AND NEITHER IS THE PERSON'S NAME IN IT.**
 * queue.md said this already: *"Geni refuses a second export while one is generating and
 * the refusal appears as a banner on a page that ALSO still reads 'Being Created', so it
 * looks like success."* The banner is the pink
 * "Your previous request had an error which we are investigating", which was read here
 * as a stale site notice for an entire afternoon.
 *
 * **THE ONLY INSTRUMENT IS A NEW ROW ON /gedcom**, checked after the submit. One export
 * at a time is Geni's limit and this script cannot pace around it: a queue of submits
 * against a held slot is a queue of refusals.
 *
 * ⛔ AND THE STAGGER IS THE ONLY THROTTLE. § PACE IT -- 500+ back-to-back reads got the
 * account CAPTCHAd on 2026-09-12. One submit a minute.
 *
 * Paste into a geni.com tab, then read `window.__forest.state()`. It drives itself, so
 * the tool call does not sit inside the stagger -- a 60s sleep inside `Runtime.evaluate`
 * times out at 45s, which is how the first attempt died.
 *
 *     window.__forest.start([[id, name, walk], ...])
 *     window.__forest.state()      // {left, waiting, refused, done:[{id, nm, walk, accepted, count}]}
 */
(function () {
  const GAP_MS = 60000;
  /* ⛔ A HELD SLOT IS WAITED OUT, NOT QUEUED AGAINST. 2026-09-19: a dead task -- one whose
   * /gedcom/download errors on every reload -- held the single export slot for hours, and
   * every submit behind it rendered the lying "Being Created" heading and produced no row.
   * So a refusal re-queues the SAME id and waits SLOT_GAP_MS; it never advances the roster. */
  const SLOT_GAP_MS = 600000;
  /* A roster entry is [id, name] or [id, name, walk]; the walk defaults to Forest, which
   * is what this file was written for. Descendants and Ancestors ride the same submit. */
  const URL_FOR = (id, walk) =>
    "/gedcom/request_export?id=" + id + "&walk=" + (walk || "Forest") +
    "&max_profiles=5000&destination=Ftb80&name_format=0&locale=en-US&include_bom=1";

  const R = (window.__forest = window.__forest || { todo: [], done: [], running: false, gen: 0 });

  /* ⛔ THE INSTRUMENT IS THE YEAR COUNTER ON /gedcom -- "You have requested N GEDCOM
   * exports from Geni in the past year" -- because an accepted request increments it and a
   * refused one does not. **NOT the task rows**: they carry `data-doc-id` in the DOM but
   * are rendered after load, so a `fetch` of the same page returns none of them and every
   * submit reads as refused. That is the same shape as § *a census read costs a real page
   * load*, and it cost a restart here on 2026-09-19. The counter is in the served HTML. */
  async function requested() {
    try {
      const t = await fetch("/gedcom", { credentials: "include" }).then((r) => r.text());
      const m = t.match(/You have requested ([\d,]+) GEDCOM/);
      return m ? m[1].replace(/,/g, "") : "";
    } catch (e) { return ""; }
  }

  async function submit(id, nm, walk) {
    let rec = { id: id, nm: nm, walk: walk || "Forest", at: new Date().toISOString() };
    const before = await requested();
    try {
      const r = await fetch(URL_FOR(id, walk), { credentials: "include" });
      const t = (await r.text()).replace(/\s+/g, " ");
      rec.status = r.status;
      /* ⛔ THE HEADING IS GONE FROM HERE, AND SO IS ITS BUG. Matching the person's name
       * against "GEDCOM File is Being Created" read a refusal as a submit, and the regex
       * that did it was malformed -- an unclosed character class -- so this file threw on
       * paste and never ran at all. The year counter answers the question instead. */
      rec.notAllowed = /not allowed to export/i.test(t);
    } catch (e) {
      rec.err = String((e && e.message) || e);
    }
    const after = await requested();
    rec.accepted = !!before && !!after && Number(after) > Number(before);
    rec.count = after;
    R.done.push(rec);
    return rec;
  }

  /* ⛔ `gen` IS THE RESTART GUARD, the same one `scripts/pathrun.js` carries: pasting
   * this twice would otherwise run two loops against one account. */
  async function pump(gen) {
    while (R.todo.length && gen === R.gen) {
      const next = R.todo.shift();
      const rec = await submit(next[0], next[1], next[2]);
      /* A refusal that names the permission is final -- waiting cannot earn access to a
       * profile this account does not manage, so it leaves the roster rather than looping. */
      if (rec.notAllowed) { R.refused = (R.refused || []).concat([rec]); continue; }
      if (!rec.accepted) {
        /* Refused: the slot is held by whatever is ahead of us. Put it back and wait. */
        R.todo.unshift(next);
        R.waiting = rec;
        if (gen === R.gen) await new Promise((z) => setTimeout(z, SLOT_GAP_MS));
        continue;
      }
      R.waiting = null;
      if (R.todo.length && gen === R.gen) await new Promise((z) => setTimeout(z, GAP_MS));
    }
    if (gen === R.gen) { R.running = false; R.finished = new Date().toISOString(); }
  }

  R.start = function (roster) {
    R.todo = (roster || []).slice();
    R.gen += 1;
    R.running = true;
    R.finished = "";
    R.waiting = null;
    pump(R.gen);
    return { queued: R.todo.length, gen: R.gen };
  };
  R.state = function () {
    return { running: R.running, left: R.todo.length, finished: R.finished,
             waiting: R.waiting, refused: R.refused || [], done: R.done };
  };
})();
