/* The parent walk: go up the ancestry adding whichever parent is missing.
 *
 * `docs/parent-walk-algorithm.md` is Emma's dictation and the authority on the ORDER. This file
 * implements it; `docs/export-seed-rules.md` decides what a created person is CALLED.
 *
 * ⛔ THE ORDER IS THE SPECIFICATION. Her words: *"I am giving you a very, very specific ordering
 * of things."* Per person:
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

/* Which parents exist, and who they are -- the pids are what gets enqueued. A missing label is a
 * missing parent: Geni prints `father` only when there is one. Measured on Ane Oline Jonsdatter
 * Raugstad, whose block carries `husband, son, daughter, father` and no `mother`. */
GC.seed.family = function () {
  const fam = document.querySelector("#family_profile_module, .immediate-family, #immediate_family");
  const out = { father: null, mother: null, found: !!fam };
  if (!fam) return out;
  for (const lbl of fam.querySelectorAll("*")) {
    if (lbl.children.length !== 0) continue;
    const t = (lbl.textContent || "").trim().toLowerCase();
    if (t !== "father" && t !== "mother") continue;
    let n = lbl.parentElement, hop = 0, a = null;
    while (n && hop < 4 && !a) { a = n.querySelector("a[data-profile-id]"); n = n.parentElement; hop++; }
    if (a) out[t] = { pid: a.getAttribute("data-profile-id"), name: (a.textContent || "").trim() };
  }
  return out;
};

/* The person's own name, off the page.
 *
 * The GIVEN name is the first token and the SURNAME is the last, unless the last IS the
 * patronymic. That is what makes `Ole Larsen Tjåland` a tier 1 -- given `Ole`, patronymic
 * `Larsen`, surname `Tjåland`, so the father is `Lars /Tjåland/` -- while `Anders Olsen` has no
 * surname left and falls to tier 2. **A Nordic farm name IS a surname** (Emma, 2026-08-18: *"uhh
 * farm names are surnames here lol"*), and the standing warning applies: do not reason a surname
 * out of existence. She ruled that way twice, on farm names and on `-ez`. */
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
 * not of *Rodrígu*. Emma, 2026-08-18: *"-ez is a real patronymic in some cases lol and we do treat
 * it as one in historical contexts."* The reading that `-ez` had fossilised into an inherited
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

/* A particle names the father in the tokens after it, UP TO THE NEXT PARTICLE -- her ruling,
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
GC.seed.plan = function (nm, pat, which) {
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

  /* Tier 3 -- the other parent is present and this one is not. No surname: Geni's *Suggest
   * surnames* would offer the child's, which would be invented. The value is the SLOT, not the
   * label -- *"by creating this person we're actually reducing ambiguity in the tree"*. */
  if (which === "mother") return { tier: 3, first: "NN", last: "", why: "mother absent" };

  /* Tier 4 -- Decision 1: the given name is `NN` and the father does NOT inherit the child's. */
  if (surname) return { tier: 4, first: "NN", last: surname, why: "no patronymic, birth surname kept" };
  if (markerGiven) return { skip: "no surname and the given name is a marker" };
  return { tier: 5, first: "NN", last: "father of " + nm.given, why: "no surname" };
};

/* ---------------------------------------------------------------- creating */

GC.seed.addParent = async function (which, p) {
  const link = GC.byText("a", /^add family$/i).find(GC.visible);
  if (!link) return { state: "no_add_link" };
  link.click();

  const ok = await GC.until(() => document.getElementById("page_profile_names_en-US_first_name") &&
                                  document.getElementById("submit_ifs"), 15000);
  if (!ok) return { state: "dialog_never_opened" };

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

  /* ⛔ SUGGEST SURNAMES OFF. Left on, Geni offers the child's surname and a tier 3 `NN` acquires
   * a family name nobody attested. The seed rules call this out by name. */
  const sug = $("suggest_surnames");
  if (sug && sug.checked) sug.click();

  set($("page_profile_names_en-US_first_name"), p.first);
  set($("page_profile_names_en-US_middle_name"), "");
  set($("page_profile_names_en-US_last_name"), p.last);

  const g = which === "mother" ? $("gender_f") : $("gender_m");
  if (g && !g.checked) g.click();

  /* Deceased: these are historical placeholders, and Geni redacts a living profile -- which is
   * the `Private` population in our own corpus. */
  const dead = $("page_profile_is_alive_false");
  if (dead && !dead.checked) dead.click();

  $("submit_ifs").click();

  /* The confirmation is the page itself showing the parent it did not show before. § *Never run a
   * search to recover an ID. Bail.* -- Geni's search is banned outright and lags creation by an
   * unbounded amount. */
  const got = await GC.until(() => {
    const f = GC.seed.family();
    return !!f[which];
  }, 25000);
  if (!got) return { state: "add_not_confirmed" };
  const f = GC.seed.family();
  return { state: "added", pid: f[which] ? f[which].pid : "", first: p.first, last: p.last };
};

/* ---------------------------------------------------------------- one person */

GC.runSeed = async function (job) {
  const report = (o) => Object.assign({ job: "seed", geni_id: String(job.geni_id),
                                        url: location.href }, o);

  await GC.until(() => !!document.querySelector("#family_profile_module, .immediate-family"), 25000);
  const fam = GC.seed.family();
  if (!fam.found) return report({ state: "no_family_block" });

  const nm = GC.seed.name();
  const pat = GC.seed.patronymic(nm);

  /* THE ORDER. A patronymic overrides the default and checks the father first, because the
   * patronymic is what names him. Otherwise the mother is checked first. */
  const order = pat && pat.father ? ["father", "mother"] : ["mother", "father"];

  for (const which of order) {
    if (fam[which]) continue;
    const p = GC.seed.plan(nm, pat, which);
    if (p.skip) return report({ state: "skipped", which: which, reason: p.skip,
                                name: nm.display, enqueue: [] });
    if (job.dryRun) {
      return report({ state: "proposed", which: which, tier: p.tier, first: p.first,
                      last: p.last, why: p.why, name: nm.display, enqueue: [] });
    }
    const r = await GC.seed.addParent(which, p);
    /* An add that fails is a skip, not a stop: the walk takes the next person off the queue. */
    return report(Object.assign({ which: which, tier: p.tier, first: p.first, last: p.last,
                                  why: p.why, name: nm.display, enqueue: [] }, r));
  }

  /* Both parents present: add neither, and enqueue the MOTHER then the FATHER, in that order. */
  const enqueue = [];
  if (fam.mother) enqueue.push(fam.mother.pid);
  if (fam.father) enqueue.push(fam.father.pid);
  return report({ state: "both_present", name: nm.display, enqueue: enqueue,
                  mother: fam.mother ? fam.mother.name : "", father: fam.father ? fam.father.name : "" });
};
