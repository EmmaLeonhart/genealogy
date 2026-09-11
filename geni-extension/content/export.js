/* The export job: run a Forest export from a profile and take the zip.
 *
 * `docs/export-seed-rules.md` is the authority and this file implements it rather than
 * restating it. Four of its rules are load-bearing here and every one of them is a hard limit
 * of Geni's rather than a preference of ours:
 *
 *  - **Walk `Forest`, size 5000, everything else default.**
 *  - **STRICTLY ONE AT A TIME.** There is no way to run an export concurrently, and that is
 *    Geni's constraint rather than a choice made here. So there is no throughput dial. The
 *    background scheduler runs export jobs with a concurrency of exactly 1 and it is not
 *    configurable -- a second in flight is not slower, it is impossible.
 *  - **A SUBMITTED EXPORT CANNOT BE CANCELLED.** *"you think you can kill a geni export read
 *    the fucking docs you can't."* There is no abort here, and there must never be a control
 *    that pretends otherwise. A slow export is waited out or written off.
 *  - **POLL THE PAGE, NOT A CLOCK.** *"please don't use the ticks as a clock. Please use the
 *    web page changing as a clock."* The page flips to *Your GEDCOM File is Ready to Download*
 *    the moment the build finishes. Letting a clock notice instead dropped the measured rate
 *    from 7.1 exports/hour to about 1 overnight on 2026-08-18. `GC.until` is a
 *    MutationObserver, so the flip IS the trigger.
 *
 * The zips accumulate in ~/Downloads and are NOT integrated as they land -- *"I don't actually
 * want you to import or integrate the GEDCOM zip files because we're not doing it all at
 * once"*. Filing into `exports/` happens in bulk once every one of them is down, and it is
 * hers to direct: `CLAUDE.md` § *Never overwrite an existing `.ged`*.
 */

GC.runExport = async function (job) {
  const id = String(job.geni_id);
  const report = (extra) => Object.assign({ job: "export", geni_id: id, url: location.href }, extra);

  await GC.until(() => document.readyState === "complete", 30000);

  const bodyText = () => (document.body ? document.body.innerText : "");

  /* ⛔ THE SUBMIT NAVIGATES, AND THE TASK ID IS THE ONLY WAY BACK TO THE FILE.
   *
   * Clicking Export sends the tab to `/gedcom/download?task_id=<n>`, which tears down the content
   * script — so the `GC.until` further down waits on a dying document, exactly as the seed
   * confirmation did before `confirm_create`. The job then re-claims on the download page, and
   * before this it had nothing to say there: it reported `timeout` carrying the EXPORT url, so
   * the task id was lost.
   *
   * **Losing it means losing the export.** Geni mails the link and shows no list anywhere in the
   * UI — checked on `/gedcom` and on the profile's own export page, both of which render a blank
   * form — so an export whose task id was never captured cannot be collected at all. Two went
   * that way on 2026-09-10 before this.
   *
   * The URL is the whole answer, so this needs no stored state: landing here at all means the
   * submit succeeded, and the page says whether the file is built yet. */
  const task = (location.search.match(/task_id=(\d+)/) || [])[1];
  if (task) {
    const ready = GC.byText("a,button,input", /download my gedcom file/i).find(GC.visible);
    if (ready) {
      ready.click();
      return report({ state: "downloaded", task_id: task });
    }
    /* Still building. Not an error and not a retry: the build carries on without a tab held open,
     * and `task_id` is what fetches it later. */
    return report({ state: "building", task_id: task });
  }

  /* Geni refuses some profiles outright -- *"You are not allowed to export that profile."*
   * That is a real answer, not a failure to retry. Three spine steps were refused this way on
   * 2026-08-30 and the right move was to stop asking. */
  if (/not allowed to export that profile/i.test(bodyText())) {
    return report({ state: "refused" });
  }

  /* ALREADY BUILT. The page may come back ready if this profile was submitted earlier. */
  const readyLink = () =>
    GC.byText("a,button,input", /download my gedcom file/i).find(GC.visible);

  if (!readyLink()) {
    /* Set the walk and the size, then submit. The fields are found by value and by name rather
     * than by position: a form re-ordered upstream must fail loudly, not silently export a
     * different walk. `Forest` is what follows spouse links, which is why targeted exports
     * specify it -- an `Ancestors` or `BloodTree` walk goes straight past a partner step. */
    /* ⛔ THE WALK IS RADIO BUTTONS, not a select -- measured on the live form 2026-09-05, where
     * this code would have selected nothing and silently exported the DEFAULT walk, which is
     * `Blood Relatives`. A targeted export that quietly changes style is worse than one that
     * fails: `CLAUDE.md` § *When an export is meant to close a specific path, read the relation
     * column first and pick a style that follows those link types* -- an `Ancestors` or
     * `BloodTree` walk goes straight past a partner step that `Forest` follows.
     *
     * The five options render as their own labels: Blood Relatives, DNA Relatives, Ancestors,
     * Descendants, and *Forest including connected in-law trees*. */
    const radios = [...document.querySelectorAll("input[type=radio]")];
    const labelOf = (r) => {
      const byFor = r.id && document.querySelector("label[for='" + r.id + "']");
      const txt = (byFor && byFor.textContent) ||
                  (r.closest("label") && r.closest("label").textContent) ||
                  (r.parentElement && r.parentElement.textContent) || "";
      return txt.replace(/\s+/g, " ").trim();
    };
    /* The walk is the JOB'S, defaulting to Forest. It was hardcoded until 2026-09-05, when an
     * **Ancestors** export of a specific person was called for, to check that all of his
     * ancestors were present -- an ancestor export of Alfred Ingerman Hoknes, run afterwards.
     *
     * `docs/export-seed-rules.md` says `Forest`, size 5000, and that is still the default and
     * still what a seed-driven export takes. This is the other case: a named person, a named
     * walk, for a stated reason. The 2026-09-05 remark that ancestors and blood-relatives walks
     * are of questionable use right now was about what to spend an `addAncestor` result on, not
     * a ban -- and a later instruction naming one outranks it either way. */
    const want = new RegExp("^" + (job.walk || "forest"), "i");
    const walk = radios.find((r) => want.test(labelOf(r)));
    if (!walk) return report({ state: "no_such_walk", walk: job.walk || "forest" });
    if (!walk.checked) walk.click();

    const size = document.querySelector("input[name*='size' i], select[name*='size' i], input#size");
    if (size) {
      if (size.tagName === "SELECT") {
        const o = [...size.options].find((x) => (x.value || "").trim() === "5000");
        if (o) size.value = o.value;
      } else {
        size.value = "5000";
      }
      size.dispatchEvent(new Event("change", { bubbles: true }));
    }

    /* ⛔ THE SUBMIT IS AN ANCHOR, not a button or an input. Measured on the live form
     * 2026-09-05, after this returned `no_submit` on a real export:
     *
     *     <a class="super blue button gedcom-export-form-sub">Export GEDCOM</a>
     *
     * The old selector asked for `input[type=submit], button[type=submit], button` and found
     * nothing, so a correctly-filled form was simply never sent — the same shape as the walk
     * being a radio rather than a select, which this file already carries a comment about.
     * Both were selectors written from what the markup ought to be. The class is tried first
     * because it is the page's own name for the control; the text match is the fallback. */
    const findSubmit = () =>
      [...document.querySelectorAll("a.gedcom-export-form-sub")].find(GC.visible) ||
      [...document.querySelectorAll("a,button,input[type=submit],input[type=button]")]
        .find((b) => GC.visible(b) &&
                     /^export gedcom$/i.test(((b.textContent || b.value || "").trim())));
    if (!findSubmit()) return report({ state: "no_submit" });

    /* ⛔ **CLICKING THE ANCHOR IS NOT THE SAME AS SUBMITTING, AND THE DIFFERENCE WAS COSTING AN
     * HOUR A TIME.** This is the cause of *"the export submit does not fire unattended"*, which
     * stood unexplained from 2026-09-10 to 2026-09-11.
     *
     * The control is `<a class="super blue button gedcom-export-form-sub">Export GEDCOM</a>` --
     * an anchor with **no `href`**. Its only behaviour is a jQuery handler bound when Geni's
     * bundle runs, which is after `readyState === "complete"`, because Geni serves base HTML and
     * fills the page in afterwards. `element.click()` on an anchor with no href and no handler
     * yet bound does **nothing at all**: no navigation, no error, no exception to catch. The
     * script then fell into the wait below and sat there for `waitMs`.
     *
     * ⛔ **AND `waitMs` IS THE BUILD'S BUDGET, WHICH IS MEANINGLESS ON THIS PAGE.** An hour is
     * right for a 5,000-person ball being built -- and that build happens on
     * `/gedcom/download?task_id=<n>`, which the job reaches by re-claiming after the navigation.
     * On the export FORM there is nothing being built and nothing to wait for, so spending the
     * build budget here buys silence. Worse than silence: the job holds `active`, and `pump`'s
     * `if (serial && serialInFlight >= 1) break` gives the export slot to a tab doing nothing
     * for a full hour, so the NEXT target cannot start either. Observed on Elizabeth de Durfort
     * `6000000012808241290`, whose export tab was still parked with no result while the same
     * export was submitted by hand in another tab and finished.
     *
     * So: click, watch for the submit to take EFFECT, and re-click if it did not. The effect is
     * unambiguous -- the submit navigates to a URL carrying `task_id`, or the page is already
     * showing the download link. Three attempts at fifteen seconds is forty-five seconds to a
     * real answer instead of an hour to none.
     *
     * ⛔ The re-click cannot double-submit. It only fires while `location.href` is UNCHANGED
     * and no `task_id` has appeared -- and a click that worked navigates, which tears this
     * content script down before the loop can come round again. */
    const fired = () => /task_id=\d+/.test(location.search) || !!readyLink();
    const startedAt = location.href;
    let clicks = 0;
    while (clicks < 3 && !fired() && location.href === startedAt) {
      const el = findSubmit();
      if (!el) break;
      el.click();
      clicks += 1;
      if (await GC.until(() => fired() || location.href !== startedAt, 15000)) break;
    }
    if (!fired() && location.href === startedAt && findSubmit()) {
      /* A real, fast, diagnosable answer. The form was found and filled and the control would
       * not act, which is a different thing from `no_submit` (the control was never there) and
       * from `timeout` (the build ran long). */
      return report({ state: "no_submit_effect", clicks: clicks });
    }
  }

  /* WAIT FOR THE PAGE TO SAY SO. The budget is generous because the only alternative to waiting
   * is abandoning -- there is no cancel. */
  /* A short wait only. The submit normally navigates, and when it does the answer arrives on the
   * re-claim above rather than here; sitting on a dying document for an hour buys nothing. */
  const ok = await GC.until(() => !!readyLink(), job.waitMs || 3600000);
  if (!ok) {
    return report({ state: "timeout",
                    task_id: (location.search.match(/task_id=(\d+)/) || [])[1] || "" });
  }

  readyLink().click();
  return report({ state: "downloaded" });
};

/* Creating the placeholder individual is deliberately NOT automated here.
 *
 * `docs/export-seed-rules.md` is a five-tier preference order over what the person should be
 * called, resting on whether a patronymic names the father, whether a Nordic farm name is a
 * surname, and what to do when a tree is saturated -- and its § *Bail on anything weird* rule
 * exists because the wrong call creates a person on Geni who did not exist. That is an
 * outward-facing write to a live site with real other users on it, so it stays a decision the
 * seed rules drive with a person in the loop, and the extension does the part that is
 * mechanical: the export, the poll and the download.
 *
 * If that changes it is hers to change, and the tier logic belongs in a script that proposes a
 * name for review rather than in a content script that types it into Geni. */
