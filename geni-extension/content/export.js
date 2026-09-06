/* The export job: run a Forest export from a profile and take the zip.
 *
 * `docs/export-seed-rules.md` is the authority and this file implements it rather than
 * restating it. Four of its rules are load-bearing here and every one of them is a hard limit
 * of Geni's rather than a preference of ours:
 *
 *  - **Walk `Forest`, size 5000, everything else default.**
 *  - **STRICTLY ONE AT A TIME.** Emma, 2026-08-18: *"There's no way that you can do an export
 *    concurrently. That isn't my decision thats geni."* So there is no throughput dial. The
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
    /* The walk is the JOB'S, defaulting to Forest. It was hardcoded until 2026-09-05, when she
     * asked for an **Ancestors** export of a specific person to check his ancestors were all
     * present -- *"Make sure all of his ancestors are present by doing an ancestor export of
     * [Alfred Ingerman Hoknes] after and this is the proper thing."*
     *
     * `docs/export-seed-rules.md` says `Forest`, size 5000, and that is still the default and
     * still what a seed-driven export takes. This is the other case: a named person, a named
     * walk, for a stated reason. Her 2026-09-05 remark that ancestors and blood-relatives walks
     * are *"of questionable use for this time"* was about what to spend an `addAncestor` result
     * on, not a ban -- and a later instruction naming one outranks it either way. */
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
    const submit =
      [...document.querySelectorAll("a.gedcom-export-form-sub")].find(GC.visible) ||
      [...document.querySelectorAll("a,button,input[type=submit],input[type=button]")]
        .find((b) => GC.visible(b) &&
                     /^export gedcom$/i.test(((b.textContent || b.value || "").trim())));
    if (!submit) return report({ state: "no_submit" });
    submit.click();
  }

  /* WAIT FOR THE PAGE TO SAY SO. The budget is generous because the only alternative to waiting
   * is abandoning -- there is no cancel. */
  const ok = await GC.until(() => !!readyLink(), job.waitMs || 3600000);
  if (!ok) return report({ state: "timeout" });

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
