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
    const walk = document.querySelector("select[name*='walk' i], select#walk");
    if (walk) {
      const opt = [...walk.options].find((o) => /^forest$/i.test((o.value || o.text || "").trim()));
      if (!opt) return report({ state: "no_forest_option" });
      walk.value = opt.value;
      walk.dispatchEvent(new Event("change", { bubbles: true }));
    }

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

    if (!walk && !size) return report({ state: "no_export_form" });

    const submit = [...document.querySelectorAll("input[type=submit],button[type=submit],button")]
      .find((b) => GC.visible(b) && /export|submit|create/i.test(b.textContent || b.value || ""));
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
