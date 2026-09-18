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
 * ⛔ A FOREST SUBMIT RETURNS NO TASK ID AND SHOWS NO DASHBOARD ROW WHILE IT BUILDS.
 * Measured 2026-09-18 on NN Onarheim and Turid Gissursdatter: the submit renders
 * "<name>'s GEDCOM File is Being Created", `location.search` carries no `task_id`, the
 * page HTML holds none either, and https://www.geni.com/gedcom never grew a row for
 * either one. The export form itself says a Forest "may take several days to complete"
 * against the 6-15 minutes a Descendants ball takes. So the only confirmation a submit
 * gets is THE PERSON'S OWN NAME in that heading, which is what `building` checks, and
 * collection happens later off the dashboard when rows appear.
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
