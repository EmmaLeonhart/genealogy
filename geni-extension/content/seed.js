/* The parent walk: go up the ancestry adding whichever parent is missing.
 *
 * `docs/parent-walk-algorithm.md` is the dictation and the authority on the ORDER. This file
 * implements it; `docs/export-seed-rules.md` decides what a created person is CALLED.
 *
 * ⛔ THE ORDER IS THE SPECIFICATION, and it was given as a very specific ordering.
 * Per person:
 *
 *   1. patronymic present -> check the FATHER first; absent -> add him, named from the patronymic
 *   2. otherwise          -> check the MOTHER first, then the father
 *   3. no mother -> add the mother; no father -> add the father
 *   4. both present -> add neither; enqueue the mother, THEN the father, and carry on up
 *   5. an add that fails for any reason -> take the next person off the queue
 *
 * Rule 5 IS the master-profile handling. *"If it fails to add somebody for some reason... it just
 * moves on to the next member of the queue. And that's how we resolve master profiles."* So there
 * is no error taxonomy here and nothing is held: a person skipped is not excluded, which is
 * `docs/export-seed-rules.md` § *A BAIL IS PER-ATTEMPT, NEVER PER-PERSON*.
 *
 * IT NEEDS NO CANVAS AND NO EYES. Everything below is ordinary DOM on `/people/<id>`: the
 * immediate-family block says which parents exist, and the page's own **Add Family** link opens
 * the add dialog. The tree view's `+` affordances are canvas draw calls with no scene graph
 * (measured: `stage.current.find('Group')` returns 0), which is what made that route need
 * pixels. This one does not.
 */

GC.seed = {};

/* ---------------------------------------------------------------- reading the person */

/* Which parents exist. ⛔ THE LABELLED BLOCK IS NOT THE SOURCE OF TRUTH -- measured the hard
 * way on 2026-09-05, by creating somebody who should never have been created.
 *
 * Ane Oline Jonsdatter Raugstad's labelled block reports **`father` only**. Her prose block
 * reads *"Daughter of Jon Samuelsen Raustad; Inger Kristoffersdatter and NN"* -- she had a
 * mother, `Inger Kristoffersdatter`, the whole time. Reading the labels said "no mother", the
 * walk added one, and a live profile acquired a spurious third parent.
 *
 * That is `CLAUDE.md` § *check the separator before believing a distribution* in its most
 * expensive form: an instrument reading a partial source and returning a confident wrong answer,
 * where the cost is a write to somebody else's tree rather than a number in a report.
 *
 * So: the PROSE block is authoritative for how many parents exist, and the labelled block is
 * used only to say WHICH one a lone parent is. Two or more parents listed means the slot is
 * full, whatever any label says.
 */
/* ⛔⛔ **`found` MEANS THE PROSE WAS READ. IT USED TO MEAN A CONTAINER EXISTED, AND THAT CREATED
 * REAL PEOPLE ON A LIVE SITE.**
 *
 * 2026-09-10. `out.found = true` was set by `#family_profile_module` being present in the DOM.
 * That element renders before the family data lands in it, so a page caught mid-load gave:
 *
 *     prose block   absent   ->  out.parents === []
 *     the module    present  ->  out.found === true
 *
 * and `runSeed` reads that pair as *this person has no parents at all*, which is tier 4/5 and a
 * creation. The walk then invented a father — and a mother beside him, because Geni's add-parent
 * flow makes the couple — on page after page of the Черкасский / Идаров tree.
 *
 * The file already says the right thing one comment up: *the PROSE block is authoritative for
 * how many parents exist, and the labelled block is used only to say WHICH one a lone parent
 * is.* `found` was the one place that did not obey it. The labelled block can no longer make a
 * page look read.
 *
 * **Absent prose is NOT zero parents. It is no answer**, and no answer must never reach a write.
 */
GC.seed.family = function () {
  const out = { parents: [], father: null, mother: null, found: false, read: false, module: false };

  /* ⛔⛔ **THE PROSE IS `<th>Immediate Family:</th><td><p>Son of <a>…</a> and <a>…</a></p>…</td>`,
   * AND THE OLD READER COULD NOT SEE IT.**
   *
   * It looked for a LEAF element whose text starts with "son of" — `e.children.length === 0`.
   * Every relation line is a `<p>` containing `<a>` elements, so `children.length` is 2 or more
   * and the filter matched nothing. Measured on the live DOM 2026-09-10.
   *
   * That is the other half of the creations. With no prose match `out.parents` stayed empty
   * while `out.found` was set true by the module merely existing, so `runSeed` read *no parents
   * at all* on people who plainly had two, and created a father.
   *
   * And where the old filter DID match something, it then took **every** `a[data-profile-id]` in
   * the matched element's PARENT — which is this `<td>`, holding the spouse and children lines
   * too. So parents were over-counted from the wrong lines, which is a walk that climbs into
   * somebody's wife and calls her a parent.
   *
   * Both faults come from guessing at the markup instead of reading it. This reads it:
   *
   *   - the `Immediate Family:` header cell finds the block, and its row's `<td>` is the block
   *   - each `<p>` in it is ONE relation, and only the `Son of` / `Daughter of` one holds parents
   *   - `read` is *this block has rendered at least one relation*, which is true for a
   *     parentless person too — they still have a `Husband of` or `Father of` line
   *
   * **`read` is what a write is allowed to depend on, and `found` is not**: a person with no
   * parents has no `Son of` line at all, so requiring `found` before creating would make the walk
   * unable to ever create anybody — which is the entire point of it. */
  const th = [...document.querySelectorAll("th")]
    .find((e) => /^immediate family/i.test((e.textContent || "").trim()));
  const td = th && th.parentElement ? th.parentElement.querySelector("td") : null;
  if (td) {
    /* ⛔⛔ **THE RELATION LINES ARE SEPARATED BY `<br>`, NOT BY ELEMENTS.** Measured on
     * Constantine, lord of Barbaron `6000000006101354662`, 2026-09-10:
     *
     *     <td><p>Son of <a>Vasak Pahlavuni</a><br>
     *            Husband of <a>Alix de Lampron</a>; <a>Beatrice</a><br>
     *            Father of <a>…</a>, <a>…</a>, …</p></td>
     *
     * ONE `<p>`, fourteen anchors, and only the first is a parent. Taking a whole element's
     * anchors -- any element, `<p>` or `<td>` -- reads his wives and his children as his parents.
     * That is not a mis-count that makes the walk cautious: `enqueue` is what the walk climbs
     * into next, so it walked into spouses and CHILDREN and spread sideways and downwards
     * through the family instead of going up. Reading it as `parents: 14` also makes every such
     * person `both_present`, which is why an entire run came back that way.
     *
     * So the split is on `<br>`, and a parent is an anchor inside the `Son of` / `Daughter of`
     * segment and nowhere else. Both markups are handled: several `<p>`s, or one `<p>` full of
     * `<br>`s. */
    /* ⛔⛔ **PARSE BY THE RELATION WORDS, NOT BY THE MARKUP.** Third attempt, and the first two
     * both failed the same way: they assumed a separator.
     *
     *   - splitting on the ELEMENT took a whole `<p>`/`<td>`, which holds every relation
     *   - splitting on `<br>` worked on a fully rendered page and failed on a half-rendered one,
     *     where the relations arrive as one unseparated text run. Constantine, lord of Barbaron
     *     then read as `both_present` with FOURTEEN parents -- one father, three wives, nine
     *     children -- on a page whose own text says `Son of Vasak Pahlavuni` and nothing else.
     *
     * The separator that is always there is the SENTENCE: `Son of`, `Husband of`, `Father of`.
     * So the block is flattened into document order and each anchor is assigned to whichever
     * relation word was most recently seen in the text before it. That is true of every markup
     * Geni has produced here, rendered or half-rendered, because it reads what the page SAYS
     * rather than how it is wrapped. */
    const REL = /(son|daughter|husband|wife|father|mother|brother|sister|partner|widow|widower)\s+of\b/ig;
    const buckets = {};
    let current = "";
    const walk = (node) => {
      for (const n of node.childNodes) {
        if (n.nodeType === 3) {
          const txt = n.textContent || "";
          let m, last = null;
          REL.lastIndex = 0;
          while ((m = REL.exec(txt)) !== null) last = m[1].toLowerCase();
          if (last) current = last;
        } else if (n.nodeType === 1) {
          if (n.matches && n.matches("a[data-profile-id]")) {
            if (current) (buckets[current] = buckets[current] || []).push(n);
          } else {
            walk(n);
          }
        }
      }
    };
    walk(td);

    /* Rendered at least one relation. An empty block is one that has not filled in yet, and it
     * must never look like a person without parents. */
    out.read = Object.keys(buckets).length > 0 ||
               REL.test((td.textContent || "").replace(/\s+/g, " "));
    out.lines = Object.keys(buckets).map((k) => k + ":" + buckets[k].length);

    /* ⛔ A PARENT IS `son of` / `daughter of` AND NOTHING ELSE. Not `husband of`, not `father
     * of` -- those are the spouse and the children, and enqueueing them is what made the walk
     * spread sideways and downwards through the family instead of climbing it. */
    const parentAnchors = (buckets.son || []).concat(buckets.daughter || []);
    if (parentAnchors.length) {
      out.found = true;
      const seen = new Set();
      for (const a of parentAnchors) {
        const pid = a.getAttribute("data-profile-id");
        if (seen.has(pid)) continue;
        seen.add(pid);
        out.parents.push({ pid: pid, name: (a.textContent || "").trim() });
      }
    }
  }

  /* The labels, for which-one-is-it when exactly one parent exists. */
  const fam = document.querySelector("#family_profile_module, .immediate-family, #immediate_family");
  if (fam) {
    /* NOT `found`. This block says which of a lone parent is the father, and nothing about how
     * many there are -- see the comment above the function. */
    out.module = true;
    for (const lbl of fam.querySelectorAll("*")) {
      if (lbl.children.length !== 0) continue;
      const t = (lbl.textContent || "").trim().toLowerCase();
      if (t !== "father" && t !== "mother") continue;
      let n = lbl.parentElement, hop = 0, a = null;
      while (n && hop < 4 && !a) { a = n.querySelector("a[data-profile-id]"); n = n.parentElement; hop++; }
      if (a) out[t] = { pid: a.getAttribute("data-profile-id"), name: (a.textContent || "").trim() };
    }
  }
  return out;
};

/* The person's own name, off the page.
 *
 * The GIVEN name is the first token and the SURNAME is the last, unless the last IS the
 * patronymic. That is what makes `Ole Larsen Tjåland` a tier 1 -- given `Ole`, patronymic
 * `Larsen`, surname `Tjåland`, so the father is `Lars /Tjåland/` -- while `Anders Olsen` has no
 * surname left and falls to tier 2. **A Nordic farm name IS a surname** (ruled 2026-08-18), and
 * the standing warning applies: do not reason a surname out of existence. That ruling was made
 * twice, on farm names and on `-ez`. */
GC.seed.name = function () {
  const h = document.querySelector("h1, #profile_name, .profile-name");
  let raw = h ? (h.textContent || "").trim() : "";
  if (!raw) raw = (document.title || "").replace(/^Geni\s*-\s*/, "").replace(/\s*\(.*$/, "").trim();
  raw = raw.replace(/\s*\([^)]*\)\s*$/, "").replace(/\s+/g, " ").trim();
  const tokens = raw.split(" ").filter(Boolean);
  return { display: raw, tokens: tokens, given: tokens[0] || "" };
};

/* ---------------------------------------------------------------- the patronymic */

/* Names that genuinely END IN S. This set is the whole difference between
 * `Andersdotter -> Anders` (right) and `Andersdotter -> Ander` (a man who never existed). */
GC.seed.ENDS_IN_S = new Set(["anders", "lars", "hans", "nils", "jens", "mads", "rasmus", "thomas",
  "tobias", "mathias", "matthias", "andreas", "elias", "klaus", "claus", "nicolas", "niklas",
  "markus", "marcus", "magnus", "jonas", "silas", "moses", "johannes", "julius", "cornelius"]);

/* Where stripping leaves a stem that is not itself a name. Decision 2: *"Where the ending admits
 * several nominatives, take the commonest and do not agonise."* `Ols-` is Ole, Ola or Olav; it is
 * written `Ole`. */
GC.seed.STEM = { ol: "Ole", oll: "Ole", ola: "Ola", olav: "Olav", tor: "Tor", tore: "Tore",
  torkel: "Torkel", torger: "Torger", ivar: "Ivar", eivind: "Eivind", osmund: "Osmund",
  sivert: "Sivert", syvert: "Syvert", gunder: "Gunder", torstein: "Torstein" };

/* An Iberian patronymic is a lookup, not a stem plus an ending: `Rodríguez` is son of *Rodrigo*,
 * not of *Rodrígu*. Ruled 2026-08-18: `-ez` is a real patronymic in some cases and is treated
 * as one in historical contexts. The reading that `-ez` had fossilised into an inherited
 * surname is a true linguistic fact and explicitly NOT how this project reads them. */
GC.seed.IBERIAN = { rodriguez: "Rodrigo", fernandez: "Fernando", sanchez: "Sancho", nunez: "Nuño",
  jimenez: "Jimeno", ximenez: "Jimeno", gimenez: "Jimeno", gonzalez: "Gonzalo", martinez: "Martín",
  perez: "Pedro", lopez: "Lope", alvarez: "Álvaro", diaz: "Diego", ruiz: "Ruy",
  gutierrez: "Gutierre", ramirez: "Ramiro", velazquez: "Velasco", vasquez: "Vasco",
  vazquez: "Vasco", ordonez: "Ordoño", munoz: "Munio", enriquez: "Enrique", benitez: "Benito",
  suarez: "Suero", tellez: "Tello", bermudez: "Bermudo", garcez: "García", ibanez: "Iván" };

GC.seed.SLAVIC = { petrovich: "Pyotr", petrovna: "Pyotr", ivanovich: "Ivan", ivanovna: "Ivan",
  petrovic: "Petar", nikolaevich: "Nikolai", nikolaevna: "Nikolai", alexandrovich: "Alexander",
  alexandrovna: "Alexander", mikhailovich: "Mikhail", vasilievich: "Vasily", wojslawic: "Wojsław" };

/* A particle names the father in the tokens after it, UP TO THE NEXT PARTICLE -- ruled
 * 2026-09-04: `bin Haji Muhammad` is one patronymic naming *Haji Muhammad*, while
 * `ben Phinhas ben Yittzhaq` is two. */
GC.seed.PARTICLES = new Set(["ap", "ab", "ferch", "verch", "fitz", "ben", "bat", "bin", "ibn", "bar"]);

/* The genitive `s` is deliberately not part of these endings -- it is handled afterwards by the
 * known-name check, which is what keeps `Andersdotter` from losing its `s`. */
GC.seed.NORSE = [["dottir", 6], ["dóttir", 6], ["datter", 6], ["dotter", 6], ["dattr", 5],
  ["dtr", 3], ["sønn", 3], ["søn", 2], ["son", 3], ["sen", 2]];

GC.seed.fold = (s) => (s || "").toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "");
GC.seed.cap = (s) => (s ? s.charAt(0).toUpperCase() + s.slice(1) : s);

/* Given one token: is it a patronymic, and whom does it name? */
GC.seed.fatherFrom = function (token) {
  const t = (token || "").replace(/[.,]+$/, "");
  if (!t) return null;
  const f = GC.seed.fold(t);
  if (GC.seed.IBERIAN[f]) return { father: GC.seed.IBERIAN[f], system: "iberian" };
  if (GC.seed.SLAVIC[f]) return { father: GC.seed.SLAVIC[f], system: "slavic" };

  for (const pair of GC.seed.NORSE) {
    const suf = pair[0], cut = pair[1];
    if (f.length > suf.length + 1 && f.endsWith(suf)) {
      let stem = t.slice(0, t.length - cut);
      let sf = GC.seed.fold(stem);
      if (!GC.seed.ENDS_IN_S.has(sf) && !GC.seed.STEM[sf] && sf.endsWith("s") && sf.length > 2) {
        stem = stem.slice(0, -1);
        sf = GC.seed.fold(stem);
      }
      return { father: GC.seed.STEM[sf] || GC.seed.cap(stem), system: "norse" };
    }
  }
  /* An unmapped Iberian ending is REPORTED, never guessed at: inventing a nominative from `-ez`
   * alone would name a man on the strength of a suffix. */
  if (/(?:ez|iz|oz|az)$/.test(f) && f.length > 4) return { father: null, system: "iberian-unknown" };
  return null;
};

/* Scan the whole name. The first token is the person's own given name and is never read as their
 * patronymic; which field the patronymic sits in decides nothing, which is why this walks tokens
 * rather than fields -- `Ane Oline Jonsdatter Raugstad` keeps hers in the middle name. */
GC.seed.patronymic = function (nm) {
  const toks = nm.tokens;
  for (let i = 1; i < toks.length; i++) {
    if (GC.seed.PARTICLES.has(GC.seed.fold(toks[i]))) {
      const parts = [];
      for (let j = i + 1; j < toks.length && !GC.seed.PARTICLES.has(GC.seed.fold(toks[j])); j++) {
        /* Stop at a territorial opener. `CLAUDE.md`: over 16,165 labelled people a non-initial
         * bare English `of` is followed by a place without exception -- `of Egypt`, `of Armenia`,
         * `of that Ilk`. Without this, `Owain ap Cadwgan of Powys` names the father
         * *Cadwgan of Powys*, which is a man plus a kingdom. */
        if (GC.seed.fold(toks[j]) === "of") break;
        parts.push(toks[j]);
      }
      if (parts.length) {
        return { token: toks[i] + " " + parts.join(" "), father: parts.join(" "),
                 system: "particle", index: i, consumed: parts.length + 1 };
      }
    }
  }
  for (let i = 1; i < toks.length; i++) {
    const hit = GC.seed.fatherFrom(toks[i]);
    if (hit) return { token: toks[i], father: hit.father, system: hit.system, index: i, consumed: 1 };
  }
  return null;
};

/* The surname the created parent takes: the last token, unless that token IS the patronymic. */
GC.seed.surname = function (nm, pat) {
  const toks = nm.tokens;
  if (toks.length < 2) return "";
  const last = toks[toks.length - 1];
  if (pat && (pat.index + pat.consumed - 1) === toks.length - 1) return "";
  return last === nm.given ? "" : last;
};

/* ---------------------------------------------------------------- naming the new parent */

GC.seed.UNKNOWN = /^(nn|n\.n\.|unknown|ukjent|private|n)$/i;

/* Which tier, and what the person is called. `docs/export-seed-rules.md` is the authority. */
GC.seed.plan = function (nm, pat, which, parentCount) {
  const surname = GC.seed.surname(nm, pat);
  const markerGiven = !nm.given || GC.seed.UNKNOWN.test(nm.given);

  if (which === "father" && pat && pat.father) {
    /* Tier 1 / 2 -- the patronymic NAMES the father, so he is attested rather than invented.
     * *"patronymics allow us to create an individual that is directly historically attested and
     * doesn't involve the NN on them."* */
    if (surname) return { tier: 1, first: pat.father, last: surname,
                          why: "patronymic " + pat.token + " (" + pat.system + ")" };
    if (markerGiven) return { skip: "tier 2 would read 'father of " + nm.given + "', which names nobody" };
    return { tier: 2, first: pat.father, last: "father of " + nm.given,
             why: "patronymic " + pat.token + ", no surname" };
  }

  if (pat && pat.system === "iberian-unknown") return { skip: "unmapped Iberian patronymic" };

  /* ⛔ TIER 3 IS ONLY WHEN ONE PARENT IS ALREADY THERE. Ruled 2026-09-05, on which parent a
   * person with NO parents and no patronymic should get: **the father, per the seed rules** --
   * `docs/export-seed-rules.md` tiers 4 and 5, `NN` plus the birth surname or `NN /father of X/`.
   * So the mother-first ordering in `docs/parent-walk-algorithm.md` governs the case where one
   * parent already exists, and the seed rules govern the empty case. This reported `tier 3,
   * mother absent` for people with zero parents until that ruling.
   *
   * The value of a tier 3 is the SLOT, not the label -- *"by creating this person we're actually
   * reducing ambiguity in the tree"*. */
  if (which === "mother" && parentCount >= 1) {
    return { tier: 3, first: "NN", last: "", why: "father present, mother absent" };
  }

  /* Tier 4 -- Decision 1: the given name is `NN` and the father does NOT inherit the child's. */
  if (surname) return { tier: 4, first: "NN", last: surname, why: "no patronymic, birth surname kept" };
  if (markerGiven) return { skip: "no surname and the given name is a marker" };
  return { tier: 5, first: "NN", last: "father of " + nm.given, why: "no surname" };
};

/* The rules on the SUGGESTED surname, 2026-09-05:
 *
 *     "if the suggested surname is the patronymic it is replaced with 'NN' and if it contains
 *      but isn't entirely the patronymic then the patronymic is removed with regex from the
 *      suggested surname"
 *
 * Applied to what Geni returns, because the suggestion does not exist until the profile is
 * saved. The point is that a father must never end up carrying his child's patronymic as a
 * surname -- `Ole Olsen` as the father of `Anders Olsen` names a family that does not exist.
 */
GC.seed.correctSurname = function (suggested, patronymic) {
  const sug = (suggested || "").trim();
  const pat = (patronymic || "").trim();
  if (!sug || !pat) return { surname: sug, changed: false };
  const foldEq = (a, b) => GC.seed.fold(a) === GC.seed.fold(b);

  if (foldEq(sug, pat)) return { surname: "NN", changed: true, why: "suggested == patronymic" };

  const kept = sug.split(/\s+/).filter((t) => !foldEq(t, pat));
  if (kept.length !== sug.split(/\s+/).length) {
    return { surname: kept.join(" ") || "NN", changed: true,
             why: "patronymic removed from the suggestion" };
  }
  return { surname: sug, changed: false };
};

/* ---------------------------------------------------------------- creating */

GC.seed.addParent = async function (which, p) {
  /* ⛔ EVERY STAGE IS RECORDED AS IT HAPPENS, because this function failed SILENTLY on
   * 2026-09-05 -- no result, and none of the states it defines for failure. A return value is
   * only useful if the function reaches its return, and the whole question here is whether it
   * does. `data-geni-collector-step` is written before each stage, so a job that dies leaves
   * its last completed stage on the page where the next read can see it. */
  const step = (s) => { document.documentElement.dataset.geniCollectorStep = s; };

  step("find-add-link");
  const link = GC.byText("a", /^add family$/i).find(GC.visible);
  if (!link) return { state: "no_add_link" };

  /* ⛔ `preventDefault` ON AN `href="#"` ANCHOR. Clicking it navigates to the `#` fragment, and
   * that navigation is the leading suspect for tearing the in-flight job down. The page's own
   * handler still runs -- the dialog opens either way -- so suppressing the default costs
   * nothing and removes a whole class of failure. */
  link.addEventListener("click", (e) => e.preventDefault(), { once: true });
  step("clicked-add-link");
  link.click();

  step("waiting-for-dialog");
  const ok = await GC.until(() => document.getElementById("page_profile_names_en-US_first_name") &&
                                  document.getElementById("submit_ifs"), 15000);
  if (!ok) return { state: "dialog_never_opened" };
  step("dialog-open");

  const $ = (id) => document.getElementById(id);
  const set = (el, v) => {
    if (!el) return;
    el.value = v;
    el.dispatchEvent(new Event("input", { bubbles: true }));
    el.dispatchEvent(new Event("change", { bubbles: true }));
  };

  /* Relationship is `parent`; FATHER vs MOTHER is the gender radio. Measured on the live dialog:
   * the options are parent/spouse/ex_spouse/partner/ex_partner/fiance/other/sibling/child. */
  const rel = $("relationship");
  if (!rel) return { state: "no_relationship_field" };
  set(rel, "parent");

  /* ⛔ SUGGEST SURNAMES **ON** -- ruled 2026-09-05 as the better option. This
   * REVERSES `docs/export-seed-rules.md` tier 3, which said to leave it off because Geni would
   * offer the child's surname *"which would be invented"*. The later ruling wins, and the
   * reasoning holds: a created parent carrying the child's surname is a better handle
   * than a bare `NN`, and it is what the rest of the tree already looks like. */
  const sug = $("suggest_surnames");
  if (sug && !sug.checked) sug.click();

  set($("page_profile_names_en-US_first_name"), p.first);
  set($("page_profile_names_en-US_middle_name"), "");
  /* ⛔ THE LAST NAME IS LEFT BLANK ON PURPOSE, so Geni's *Suggest surnames* fills it.
   *
   * Ruled 2026-09-05: the father is a first name taken from the patronymic plus the suggested
   * surname, and suggested surnames are always a good thing — they had been disabled for no
   * reason. So the surname is GENI'S, not ours -- which is
   * also what retires the token-parsing this file used to do, and with it the Spanish
   * two-surname problem that parsing had.
   *
   * **Measured 2026-09-05: the suggestion cannot be read before saving.** With the box ticked
   * and a first name typed, `page_profile_names_en-US_last_name` stays empty -- on typing, and
   * on focus. Geni applies it server-side when the profile is created. So the rules about the
   * suggested surname are applied to what comes BACK, in `GC.seed.correctSurname`, not to a
   * value inspected here. Writing anything into the field would suppress the suggestion, which
   * is the one thing that must not happen. */
  set($("page_profile_names_en-US_last_name"), "");

  const g = which === "mother" ? $("gender_f") : $("gender_m");
  if (g && !g.checked) g.click();

  /* Deceased: these are historical placeholders, and Geni redacts a living profile -- which is
   * the `Private` population in our own corpus. */
  const dead = $("page_profile_is_alive_false");
  if (dead && !dead.checked) dead.click();

  /* A dry-open: everything except the irreversible click, so the path can be exercised on a
   * real person without creating one. */
  if (p.stopBeforeSave) {
    const filled = {
      relationship: $("relationship").value,
      first: $("page_profile_names_en-US_first_name").value,
      last: $("page_profile_names_en-US_last_name").value,
      suggest: $("suggest_surnames").checked,
      gender: which === "mother" ? $("gender_f").checked : $("gender_m").checked,
      deceased: $("page_profile_is_alive_false").checked
    };
    const cancel = GC.byText("a,button", /^cancel$/i).find(GC.visible);
    if (cancel) cancel.click();
    step("cancelled");
    return { state: "would_have_saved", filled: filled };
  }

  /* ⛔ LET THE FORM SETTLE BEFORE SAVING, and specifically let *Suggest surnames* run.
   *
   * This is the difference between a save that works and one that silently does nothing, found
   * on 2026-09-06 by doing the same fill by hand: the manual run waited before clicking and
   * created the person; the extension clicked immediately and created nobody, twice. A scripted
   * `.click()` submits perfectly well -- `NN Himo` `6000000227615372858` was created by one --
   * so the trusted-event theory that suggested itself here is wrong.
   *
   * The surname is Geni's to fill and it arrives asynchronously, which is why the wait is on the
   * FIELD rather than on a clock: `GC.until` returns the moment the suggestion lands, and falls
   * through after 6s for the cases where Geni declines to suggest at all -- a child whose only
   * surname is a patronymic gets no suggestion, which is what `NN` mother of Kari Olsdatter
   * looked like. */
  await GC.until(() => ($("page_profile_names_en-US_last_name") || {}).value, 6000);
  step("form-settled");

  /* ⛔⛔ **TELL THE BACKGROUND BEFORE THE WRITE, NOT AFTER IT.**
   *
   * A creation is supposed to END the walk. The background only learns of one from the job's
   * RESULT, and on 2026-09-10 the results were the thing that went missing: tabs were closed
   * mid-job, confirmations timed out, and every lost result left the background believing no
   * creation had happened. It carried on climbing and carried on creating.
   *
   * A report that arrives after the write cannot cover the write. This one goes out first, so
   * the background's record of *a person may now exist* does not depend on this job surviving to
   * report. It is awaited: the click does not happen until the background has the flag.
   *
   * `CLAUDE.md` § *Code that is WRITTEN but never CALLED is not done* has a sibling here -- a
   * guard that only runs on the success path is not a guard. This one runs before the thing it
   * guards against. */
  let announced = false;
  try {
    const ack = await chrome.runtime.sendMessage({ type: "creating",
                                                  geni_id: String(p.childId || ""),
                                                  which: which, first: p.first, last: p.last });
    announced = !!(ack && ack.halted);
  } catch (e) { /* the ack stays false, and the next line decides what that means */ }

  /* ⛔ **A SCHEDULED WRITE THAT COULD NOT ANNOUNCE ITSELF DOES NOT HAPPEN.**
   *
   * `jobId` is set by `pump` and by nothing else, so it is exactly *the background is driving
   * this*. When it is driving, the halt is the thing that keeps a single creation from becoming
   * a run of them — and an unacknowledged message means the halt is not in place. A torn-down
   * worker resolves `sendMessage` as `undefined` with no rejection and no `lastError`
   * (`service-worker`'s own header documents that), which is why the ACK is checked rather than
   * the absence of a throw.
   *
   * The DOM-trigger path has no `jobId`: that is a person deliberately running one seed on one
   * page, there is no walk to stop, and it proceeds. */
  if (p.viaScheduler && !announced) {
    step("announce-failed");
    return { state: "announce_failed", first: p.first, last: p.last };
  }

  step("clicking-save");
  $("submit_ifs").click();
  step("saved-clicked");

  /* The confirmation is the page itself showing the parent it did not show before. § *Never run a
   * search to recover an ID. Bail.* -- Geni's search is banned outright and lags creation by an
   * unbounded amount. */
  /* THE ID OF THE PERSON JUST CREATED, AND THE EXTENSION MUST RETURN IT.
   *
   * The background queues the export from `pid` and from nothing else, so a creation that comes
   * back without one leaves the walk having written to Geni for no reason -- and leaves a human
   * to find the new profile by hand and submit the export themselves, which is exactly the
   * agentic step this whole design exists to remove. That happened on `NN Rouponi`
   * `6000000227683654853` on 2026-09-10.
   *
   * The old confirmation watched `f[which]`, i.e. the LABELLED block -- the same widget that
   * renders `Showing 12 of 14 people` and drops the parent off the end of the list. It is the
   * wrong instrument twice over: it is truncated, and it is not where the parent count lives.
   *
   * The prose is. Take the parent pids from BEFORE the write, wait for a pid that was not among
   * them, and that pid IS the person just created -- no search, no guessing, no second route to
   * the same person, which `docs/export-seed-rules.md` bans outright. */
  const before = new Set(p.beforePids || []);
  const fresh = () => GC.seed.family().parents.filter((x) => !before.has(x.pid));
  const got = await GC.until(() => fresh().length > 0, 60000);
  if (!got) return { state: "add_not_confirmed", first: p.first, last: p.last };
  const made = fresh()[0];
  return { state: "added", pid: made.pid, name: made.name, first: p.first, last: p.last };
};

/* ---------------------------------------------------------------- one person */

GC.runSeed = async function (job) {
  const report = (o) => Object.assign({ job: "seed", geni_id: String(job.geni_id),
                                        url: location.href }, o);

  /* ⛔ **`no_family_block` WAS A TIMEOUT, NOT A VERDICT, AND IT SILENTLY PRUNED THE FRONTIER.**
   *
   * Measured 2026-09-10 on the first `seedwalk`: 23 people walked, and **8 came back
   * `no_family_block`** — a third of them. Tobuldu Mirza Kamisch `6000000090673721908` was one,
   * and his page has the family module perfectly well when it is loaded in a FOREGROUND tab.
   * Several of the eight reported `url` still reading `/people/x/<id>`, which is the pre-redirect
   * URL: the page had not finished loading when the budget expired.
   *
   * The cost is not a missing row. A `no_family_block` enqueues nothing, so every one of those
   * eight took its two parents out of a breadth-first walk — and the walk then emptied its queue
   * and stopped without creating anybody. A state that reads as *this person has no family* was
   * really *this page was still loading*, which is the shape `CLAUDE.md` § *A pending path search
   * is NOT a miss* names in the other campaign.
   *
   * So: wait for the load to FINISH first, and give the module its own budget after that. The
   * 25000 was written for a tab somebody was looking at. */
  await GC.until(() => document.readyState === "complete", 60000);
  /* ⛔ WAIT FOR THE PROSE, NOT FOR THE CONTAINER. `GC.seed.family().found` is now the prose
   * block and only the prose block, so this waits for the thing the parent count is read from.
   * Waiting on `#family_profile_module` was waiting on an element that is present before it says
   * anything, and every second of that gap was a window in which a page read as parentless. */
  await GC.until(() => GC.seed.family().read, 60000);
  let fam = GC.seed.family();
  /* ⛔ `read`, NOT `found`. `found` means a `Son of` line exists, i.e. this person HAS parents --
   * requiring it before proceeding would skip exactly the parentless people the walk exists to
   * create on. `read` means the Immediate Family block rendered at least one relation, which is
   * what distinguishes *no parents* from *not loaded yet*. An unrendered block is not a person
   * with no family and must not reach `plan()`. */
  if (!fam.read) return report({ state: "family_not_read", module: fam.module });

  const nm = GC.seed.name();
  const pat = GC.seed.patronymic(nm);
  const n = fam.parents.length;

  /* ⛔ TWO PARENTS LISTED MEANS THE SLOT IS FULL. This is the guard whose absence put a spurious
   * third parent on a live profile: add neither, enqueue the mother then the father, carry on up. */
  if (n >= 2) {
    const byPid = {};
    fam.parents.forEach((p) => { byPid[p.pid] = p; });
    const enqueue = [];
    /* The order: mother first, then father. Where the labels name them, that order is exact;
     * where they do not, the listed order is kept rather than guessed at. */
    if (fam.mother && byPid[fam.mother.pid]) enqueue.push(fam.mother.pid);
    if (fam.father && byPid[fam.father.pid]) enqueue.push(fam.father.pid);
    for (const p of fam.parents) if (enqueue.indexOf(p.pid) === -1) enqueue.push(p.pid);
    return report({ state: "both_present", name: nm.display, parents: n,
                    enqueue: enqueue,
                    listed: fam.parents.map((p) => p.name).join(" | ") });
  }

  /* Exactly one parent: which one is missing comes from the label. With no label there is no
   * evidence of which, and § *Bail on anything weird* says skip rather than guess -- guessing
   * here is exactly what creates a second father. */
  let which;
  if (n === 1) {
    /* ⛔ **THE LABELLED BLOCK LOADS LATER THAN THE PROSE, AND WAITING FOR IT IS NOT OPTIONAL.**
     * `read` is satisfied by the prose alone, which is right -- the prose is what the parent
     * COUNT comes from. But with exactly one parent the prose cannot say which one it is
     * (`Son of X` is the same sentence for a lone father and a lone mother), and that is the
     * labelled block's one job. Deciding before it has rendered turned Constantine, lord of
     * Barbaron -- a plain tier 3, father present -- into `one parent listed and no label says
     * which`. A guard that fires on a page it did not wait for is a skip, not a safeguard. */
    if (!fam.father && !fam.mother) {
      /* ⛔⛔ **THE WIDGET TRUNCATES AND THE PARENT FALLS OFF IT. CLICK `View All`.**
       *
       * Measured on ONG Ewe Hai `6000000025128512415`, 2026-09-10, and on Constantine, lord of
       * Barbaron before him. The labelled block renders **"Showing 12 of 25 people"** and the
       * father is simply not among the twelve, so there is no `father` label anywhere in the DOM
       * and the guard below skips a person who is a plain tier 3. ONG is a MANDATORY export --
       * a figure at or above 250 makes it required -- and he was being skipped by a widget's
       * pagination.
       *
       * `View All` is the module's own control and expanding it renders every relative with its
       * label. Waiting alone never fixes this: the missing rows are not late, they are not
       * requested. */
      const viewAll = [...document.querySelectorAll("#family_profile_module a, .immediate-family a,"
                                                    + " #family_profile_module button")]
        .find((a) => /^view all$/i.test(((a.textContent || "").trim())));
      if (viewAll) {
        viewAll.click();
        await GC.until(() => { const f = GC.seed.family(); return !!(f.father || f.mother); }, 20000);
      }
      if (!GC.seed.family().father && !GC.seed.family().mother) {
        await GC.until(() => { const f = GC.seed.family(); return !!(f.father || f.mother); }, 20000);
      }
      fam = GC.seed.family();
    }
    if (fam.father && !fam.mother) which = "mother";
    else if (fam.mother && !fam.father) which = "father";
    else return report({ state: "skipped", reason: "one parent listed and no label says which",
                         name: nm.display, parents: n, enqueue: [] });
  } else {
    /* No parents at all. A patronymic overrides the default and takes the father first. */
    /* No parents at all. A patronymic still takes the father first -- it NAMES him, which is
     * what makes tiers 1 and 2 worth more than an `NN`. Without one it is also the father, per
     * the 2026-09-05 ruling and the seed rules' tiers 4 and 5. */
    which = "father";
  }

  const p = GC.seed.plan(nm, pat, which, n);
  if (p.skip) return report({ state: "skipped", which: which, reason: p.skip,
                              name: nm.display, parents: n, enqueue: [] });
  if (job.dryRun) {
    return report({ state: "proposed", which: which, tier: p.tier, first: p.first,
                    last: p.last, why: p.why, name: nm.display, parents: n, enqueue: [] });
  }
  /* The job's dry-open flag rides on the plan, which is what `addParent` receives. */
  p.stopBeforeSave = !!job.stopBeforeSave;
  /* Whose page the write happens on, so the background's pre-write flag names a person. */
  p.childId = String(job.geni_id);
  /* The parents that existed BEFORE the write, so the one that appears after it can be named. */
  p.beforePids = fam.parents.map((x) => x.pid);
  /* `jobId` is set by `pump` and by nothing else: it means the background is driving this walk,
   * and therefore that an unannounced write must not happen. */
  p.viaScheduler = !!job.jobId;
  const r = await GC.seed.addParent(which, p);
  /* An add that fails is a skip, not a stop: the walk takes the next person off the queue. */
  return report(Object.assign({ which: which, tier: p.tier, first: p.first, last: p.last,
                                why: p.why, name: nm.display, parents: n, enqueue: [] }, r));
};
