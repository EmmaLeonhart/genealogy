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
 *     window.__forest.start([[id, name], ...])
 *     window.__forest.state()      // {left, done:[{id, nm, building, busy, notAllowed}]}
 */
(function () {
  const GAP_MS = 60000;
  const URL_FOR = (id) =>
    "/gedcom/request_export?id=" + id +
    "&walk=Forest&max_profiles=5000&destination=Ftb80&name_format=0&locale=en-US&include_bom=1";

  const R = (window.__forest = window.__forest || { todo: [], done: [], running: false, gen: 0 });

  async function submit(id, nm) {
    let rec = { id: id, nm: nm, at: new Date().toISOString() };
    try {
      const r = await fetch(URL_FOR(id), { credentials: "include" });
      const t = (await r.text()).replace(/\s+/g, " ");
      rec.status = r.status;
      /* The heading names the person, so a stale or misrouted page cannot pass as a
       * submit for THIS id -- the page text lies on this site throughout. */
      rec.building = new RegExp(nm.slice(0, 12).replace(/[.*+?^${}()|[\]\]/g, "\$&") +
                                "[^]{0,40}GEDCOM File is Being Created", "i").test(t) ||
                     /GEDCOM File is Being Created/i.test(t);
      rec.busy = /one at a time|already in progress|another export/i.test(t);
      rec.notAllowed = /not allowed to export/i.test(t);
    } catch (e) {
      rec.err = String((e && e.message) || e);
    }
    R.done.push(rec);
    return rec;
  }

  /* ⛔ `gen` IS THE RESTART GUARD, the same one `scripts/pathrun.js` carries: pasting
   * this twice would otherwise run two loops against one account. */
  async function pump(gen) {
    while (R.todo.length && gen === R.gen) {
      const next = R.todo.shift();
      const rec = await submit(next[0], next[1]);
      if (rec.busy) { R.stoppedOn = rec; break; }   /* serial limit: stop, do not hammer */
      if (R.todo.length && gen === R.gen) await new Promise((z) => setTimeout(z, GAP_MS));
    }
    if (gen === R.gen) { R.running = false; R.finished = new Date().toISOString(); }
  }

  R.start = function (roster) {
    R.todo = (roster || []).slice();
    R.gen += 1;
    R.running = true;
    R.finished = "";
    R.stoppedOn = null;
    pump(R.gen);
    return { queued: R.todo.length, gen: R.gen };
  };
  R.state = function () {
    return { running: R.running, left: R.todo.length, finished: R.finished,
             stoppedOn: R.stoppedOn, done: R.done };
  };
})();
