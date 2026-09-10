# Names, labels, patronymics and transliteration

**Moved out of `CLAUDE.md` on 2026-09-09, verbatim.** The ruling was to cut `CLAUDE.md`
to under 1,000 lines and put the evidence for each rule on a page that `CLAUDE.md`
cites. Nothing here was reworded, shortened or dropped in the move — this is the
reasoning, the measurements and the post-mortems behind the one-line rules.

---

### The NN/Private label algorithm applies to EVERY unnamed person. It is not optional

**"Create it with no label" is not one of the options.** The algorithm is:

    mul  NN Garborg                                  <- marker + the surname, which survives redaction
    en   son of Arne Olaus Fjørtoft Garborg          <- formulaic, from the nearest named relative
    nb   sønn av Arne Olaus Fjørtoft Garborg
    ja   アルネ・オーラウス・フョルトフト・ガルボルグの息子
    zh   阿尔内·奥劳斯·夫约托夫特·加尔博格之子

**`scripts/build-nn-label-batch.py` owns the language table** — ten languages with the
right relationship word per sex and the right preposition per direction (`datter af` but
`mor til`). Import it; do not restate it. It excludes Slavic and Welsh because they
inflect the name after the relationship word, and it excludes `ja`/`zh` **only** because
the relative's name is usually not transliterated — where it is, as in the Garborg family,
they are emitted.

**`PRIVATE`, `NN`, `UKJENT` and the rest are one population.** A private individual whose
name is not exported comes out as an `NN`, so they are the same thing here.

### An obvious unknown-word marker goes straight in. Stop asking

**A word or phrase meaning *the name is unknown* is a marker.** Add it to
`scripts/labels.WORDS_MEANING_UNKNOWN` with its corpus count in the comment, and move on.
`Name Not Known` (45 people) and `Unknown Wife` (37) are markers; cases this obvious need
no ruling.

**The one boundary: words yes, punctuation no.** A label that is nothing but punctuation
is handled separately, and `Nechama (?) Heller` is a name with a bracketed hole, not a
marker.

**This does not widen `NOT_A_NAME`.** Detection and suppression are different questions,
as that module already says: an `unknown Bloomfield` is detected and still keeps a label —
it becomes `NN Bloomfield`. `label_for()` still empties `Private` and `<private>` and
nothing else.

### The label gate, and the order

**No creation runs until `ja`, `zh` and `ko` labels exist on everything.** That gate sits
immediately before Wikidata editing.

**The order is not the obvious one: create the relatives first, then label.** The
structural placeholders are created, then the other creations, and only then the
`set_labels` edits — each carrying the full set. Labelling first would mean labelling
people whose relatives do not exist yet, and the NN descriptive labels are built *from*
those relatives.

**The three directions the labels are MADE in**, never copied: CJK → English
(romanisation), English → CJK, and English → the four remaining scripts (`hi`, `ar`, `ru`,
`el` — `scripts/build-four-script-labels.py`, 151,320 labels).

**Name items first is what makes it tractable.** Transliterate a token once in its name
item and every bearer inherits it: 140,764 distinct tokens across 396,377 people, of which
the CJK part is 30,876 Han, 1,552 Hangul, 92 kana.

**The one hard problem stays hard: which culture a CJK name is.** Han characters do not
say whether a name is Chinese, Japanese or Korean — 陳 is *Chen*, *Chin* or *Jin*. Kana
and Hangul are decisive; bare Han is not. **Do not guess from the name**; the tree settles
it, via neighbours and which exports they came from.

### CJK INCLUDES KOREAN. `ko` ranks with `zh`, not with the leftovers

Korean is as important as Chinese here. The C, the J and the K are three languages, and
any place this repo says "CJK" and means Han plus kana is wrong.

- **The creation gate is `ja` + `zh` + `ko`**, not `ja` + `zh`.
- **The token funnel mints all three.** `reports/garborg-name-transliterations.tsv` carries
  a `ja`, a `zh` and a `ko` column.
- **`ko` is derivable by rule and `P1814` kana is not.** A Han character has a regular
  hanja reading; a Japanese *name* reading does not follow from the characters. So `ko` is
  engine work like `zh`, while kana stays agentic.

**The 1,552 Hangul tokens are decisive evidence of culture** — kana and Hangul settle
which culture a CJK name is where bare Han does not, so those people must be labelled in
their own language rather than only used to disambiguate others.

### ALL THREE readings are produced for everyone. Culture only picks which goes on top

The kana name, the Korean name and the Mandarin reading of every character are all
produced, so the `mul` label holds every label the item could ever have; which one is
promoted to the top is set later, and the other two become `Amul` aliases.

**So the culture classifier is OFF the critical path.** It no longer decides whether a
person gets a label; it decides which alias is promoted to `mul`. That is one line, per
person, movable afterwards — a wrong verdict costs a reordering, not a wrong name and not
a missing one. The people the walk cannot classify stop being blocked and become a roster.

**This is why the classifier must not be perfected.** It is an ill-scoped problem that
attracts scope creep. The gate and the roster are the deliverable. Confirmed cultures
propagate by network proximity, so the roster shrinks as people are settled.

**The character table is the unit, not the person.** `reports/han-readings.tsv` is 4,688
rows for 41,154 people, reusable by every emitter: `ko` 4,688, `zh` 4,682, `ja`
candidate-only. `scripts/import-unihan.py` builds it from Unicode's Unihan — **a data
file, not a dependency**, so § *Stdlib only* is intact.

**`ko` needs TWO sources and neither alone is right.** `hanja` returns one reading;
Unihan's `kHangul` lists several. 金 is `금 김`, and taking the first gave 金庾信 as 금유신
when the man is **김유신, Kim Yu-sin** — the commonest surname in Korea read as the wrong
word. 沈 is 심/침 and the surname is 심. Measured over all 4,688: the two agree 3,543 times
and differ 100, and almost every difference is **두음법칙**, the initial-sound rule —
`hanja` gives the word-initial form (隴 농, 礼 예) and Unihan the base reading (롱, 례).
Neither is wrong. Coverage is complementary, ~1,000 characters each way, so both are
merged and **every reading is kept** — § *One name item per USAGE*, where a token in two
roles is not an ambiguity to resolve.

**Alternates vary the SURNAME TOKEN ONLY** — Geni writes given names first, so that is the
last token. That is where the alternation changes a name; varying every position on a
four-character name yields sixteen aliases nobody searches for.

**`ja` is the one that stays research.** `pykakasi` reads *surnames* correctly out of its
dictionary — 青山 あおやま, 酒井 さかい, 藤原 ふじわら — and falls back to on'yomi on
*given* names, where Japanese personal readings are irregular: 幸豊 → こうほう for
**Yukitoyo**. So it is a candidate column, never an emitted one, and
`scripts/fetch-kana-readings.py` remains the sourced answer. That measurement is what *a
kana reading is not derivable by rule* looks like in data.

**A Han range written with LITERAL boundary characters is a bug waiting to happen.**
U+F900 CJK COMPATIBILITY IDEOGRAPH and U+8C48 render identically, and NFC normalisation
maps the first to the second — so `豈-﫿` silently becomes U+8C48–U+FAFF, which contains
the whole Hangul Syllables block. It cost **5,338 Korean people**, whose names are already
Hangul, being counted as Han, found unreadable and dropped; skips went 5,350 → 12 on the
fix. The tell was that only 2 characters in the corpus lacked a reading, which cannot
explain 13% of the population failing. **Write the range as ASCII `\uXXXX` escapes** — the
literal form did not survive one edit round-trip here.

### A GENERATION SUFFIX GOES LAST. A regnal ordinal stays where it is

| | where it goes | property |
| --- | --- | --- |
| **generation suffix** — `d.y.`, `d.e.`, `den yngre`, `Jr.`, `Sr.` | **the END of the label**, whatever position Geni wrote it in | — |
| **regnal ordinal** — `Abisha III`, `Robert VII` | **stays put**, after the given name | `P7338` *regnal ordinal* |

    Lars Jonson d.y. Skrudland  ->  mul  Lars Jonson Skrudland II
                                    en   Lars Jonson Skrudland Jr.

`namemodel.normalise_generation_suffix` removes the token and appends the converted form.
`GENERATION_SUFFIX` holds **no bare Roman numeral**, so a regnal ordinal is never a match and
cannot move — structural rather than a special case. A label already carrying the numeral does
not gain a second one: `Daniel Ström II, dy` keeps its `II`, and the comma that introduced the
suffix goes with the suffix.

**A suffix STAYS in the languages that use it.** `nb`, `nn`, `no`, `da` and `sv` keep their own
form where their own grammar puts it, `fi` keeps `nuorempi`, English keeps `Jr.`, and every
other language takes the `mul` shape.

**`namemodel.SUFFIX_LANGUAGES` keys on the FORM, never on a list of Scandinavian languages** —
the two pairs differ by one letter and belong to different places: `d.ä.`/`den äldre` are
Swedish, `d.e.`/`den eldre` are Norwegian and Danish. A "Scandinavian keeps everything" rule
would leave a Swedish `den eldre` and a Norwegian `d.ä.` in place, each of which is the other
language's spelling. **A region subtag inherits its base language**: `en-ca` and `en-us` were
the only English labels being rewritten to `II` — 2 of the first run's 60, both wrong, found by
reading the sample rather than the count.

Measured over the 11,827 live labels on 1,465 items: **19 kept native** (`sv` 7, `fi` 6, `nb` 2,
`en-ca` 1, `en-us` 1, `nn` 1, `da` 1), **58 normalised** (`ast`, `nl`, `pap`, `sl`, `sq`, `ca`,
`es`, `ga`, `fr`, `tr`). Each language is normalised **from its own label**, never overwritten
with `mul` — a French or German label may spell the name differently for good reason.

**The CJK labels follow the `mul` form**: they are the transliteration of the primary label.
`ラース・ヨンソン・スクルドランド2世`.

**⛔ A GENERATION SUFFIX IS A FACT ABOUT THE PERSON, NOT ABOUT ONE NAME STRING.** `Q141242551`
and `Q141219063` are two different men, both labelled *Lars Osmundsen Nese*. The younger has
three name records: `Lars Osmundsen /Foss-Eikeland/ d. y.` carrying `NSFX` = `d. y.`, and
`Lars Osmundsen /Foss-Eikeland/` carrying `_MARNM` = `Nese`. § *The MARRIED name is the real
name* takes the label from the second and the suffix is on the first, so a rule matching against
the label STRING finds nothing and drops it.

`namemodel.generation_suffix_key` reads the suffix off **every** record and
`normalise_generation_suffix` takes it as an argument, so it survives a label built from a
different record and survives the creation block's married-name rebuild, which discards the
label entirely. **234 people, 19 of them already with an item.** Only the person's own `NSFX`
counts: matching a suffix anywhere in a rendered name gives 515 and sweeps in `Señor de
Campofrío` and a bare `King` left by a title truncation.

**⛔ IT MUST NOT REACH AN ITEM SOMEBODY ELSE LABELLED. Measured before it shipped: 240 items**
hold a Wikidata label that is exactly ours minus the suffix — `Q6230601` *Marcus Wallenberg*,
`Q47102` *Joseph Smith*, `Q768342` *Augustine Washington* — and ungated this ground would have
rewritten every one to `… Jr.`. The other correction grounds are gated by construction; a
suffix Geni records says nothing about who wrote the label, so this one needs its own test.
`wikidata_en`/`wikidata_mul` from the bulk store is the evidence available: non-empty means the
item was labelled independently of us. **910 held back, 12 still reachable.**

**The correction is tested like the abbreviation one** — the live label plus this person's own
suffix must equal exactly what we want — and it is the only ground that emits a different
string per language, `II` for `mul` and `Jr.` for `en`.

**Wire it everywhere or it does nothing.** `normalise_generation_suffix` was wired into
`derive-labels.py` and the label-corrections pass and **not** into the block that writes a new
item's `Lmul`/`Len`/`Lja`/`Lzh`/`Lko`, so every creation carried the Norwegian abbreviation in
all five languages and `label_in` transliterated it as a name: `…・ドイ・…`, `…디…`. § *Code
that is WRITTEN but never CALLED is not done*.

### THE NAME-ITEM DUPLICATE GUARD NEEDS THE CONTRIBUTIONS, because search LAGS

A batch tried to create `Låge-Håland` when `Q141257135` already held that label and
description. The creation was refused, and the refusal broke the **four `LAST` lines after
it** — which is what a mid-batch `CREATE` failure costs.

**The refusal is the guard working**; § *THE ONE EXCEPTION* is the rule that makes a name
item's description refuse a duplicate. The generator should not have proposed it.

**Four lookups, and all four missed — each for its own reason, so no single one is the fix:**

| lookup | why it missed |
| --- | --- |
| `out/wikidata/name-items-in-store.tsv.gz` | the offline download predates the item |
| the bearers' own `P734`/`P5056` | they do not point at it yet |
| `reports/created-name-items.tsv` | **nothing ever refreshed it** |
| live `wbsearchentities` | reads the **search index** |

**⛔ `wbsearchentities` reads the SEARCH INDEX, which Wikidata populates asynchronously.** An
item is retrievable by `wbgetentities` immediately and may not be findable by *search* for some
time after. So the live check is blind in exactly the window a daily cadence duplicates in — an
item created by yesterday's batch or by an earlier run of today's. It stays as the last resort,
because it catches items created by **other people**, which contributions cannot.

**`refresh-created-name-items.py` is the source with no lag** — it reads the account's
contributions for page creations whose `P31` is a name class, and follows redirects so a
merged-away item resolves to its survivor. It runs inside `build-garborg-day.py --compose`
beside the ledger refresh, and **fails the run** for the same reason the ledger does: a stale
file does not look like an error, it looks like work to do, and the work it invents is
re-creating what exists.

### A TITLE IS NOT A NAME, and Geni already said so — in `NSFX`

`Q2183430` *Benedicta Ebbesdotter of Hvide* went out with `P735` given name **Queen** as middle
name 3 and `P734` family name **Sweden**.

**The GEDCOM was right the whole way.** The record is
`1 NAME Bengta Ebbesdotter /Ebbesdatter Galen/` with `2 NSFX Queen of Sweden` — the title in
the name-**suffix** field, which is where it belongs. `build-display-names.py` concatenates
every piece into `display_name`, `derive-labels.py` appends `nsfx` again when it builds the
married-name alias, and the name model then parses that rendered string positionally. **A field
whose entire purpose is *this part is not a name* became two name items.**

**`NSFX` holds two different things, measured over 1,856,150 name records** — 86,947 carry one:

| shape | count | examples |
| --- | ---: | --- |
| **single token** | 30,730 | `II` 2,224 · `I` 1,836 · `Jr.` 1,693 · `Sr.` 1,436 · `Graf` 464 · `Knight` 274 |
| **multi-word with a connective** | **42,391** | `Pharaoh of Egypt` · `Queen of Egypt` · `King of Assyria` · `i København` · `til Gullaug` |
| multi-word, no connective | 13,826 | `d. y.` · `Patrizio Napoletano` · `132, 91, 44, 9` |

**Only the phrase form is dropped**, and the connective is doing the work rather than the word
list. Over the 1,295,226 labelled people the rule truncates **10,619 and leaves 5,945 alone**,
and reading the second list is what established it: `Sarah Bishop`, `Anne Greve`, `Anna King`
and `Nicholas Henry Pope` are real surnames a bare word list would have destroyed. Truncation is
at the **earliest** title word once any of them qualifies, so `Prins, Hertig av Västergötland`
goes as one stack — **171 labels stack titles that way and every one is genuine**.
`reports/title-tails-dropped.tsv` is the census: **18,165 people**.

**`namemodel.drop_title_tail` is the one place**, called inside `statements_for` on the label
and on `givn`/`surn`/`marnm` alike, because there are two emitters and they have disagreed
before. **It does not touch the LABEL.** What a person's `mul` label should read is a separate
question from what becomes a `P735`, and this changes only the second.

**DROP TITLES, KEEP ORDINALS.** `Graf` 464, `Knight` 274, `Kt.` 400 and `Donna` 209 stop
becoming name items, while `II` 2,224, `I` 1,836, `Jr.` 1,693, `Sr.` 1,436, `d.y.` 598, `d.e.`
369 and the CJK generation numerals stay — the ordinals carry `P7338` *regnal ordinal* and are
part of what the person is called. `namemodel.NAME_SUFFIX_TITLES` is the list, **297 tokens read
off the values with their counts**, and it drops 7,917 of the 30,730 occurrences, 25.8%.

**What SURVIVES the filter is the test, and it is why this is a list and not a rule.** Under the
ordinals sit Norwegian farm surnames — `Ytteren` 26, `Altermark` 26, `Skonseng` 17, `Sandnes`
16, `Sveen` 16, `Kjærulf` 15 — ordinary names that happen to be in the suffix field. Anything
that dropped what it did not recognise would have deleted them.

**Two collisions were found by measuring and both would have been silent.** `i` casefolds
together with the Roman numeral `I`, 1,836 people, so `i` is not on the list at all — the same
trap `_drop_territorial` already carries a comment about. And matching on a dot-stripped form
put `d.e.` (369, Swedish *den äldre*) onto the particle `de`. Nothing is dot-stripped; every
surface form the corpus holds is listed instead.
**`drop_title_suffix` matches the person's OWN `NSFX` exactly**, never a bare word list against
a trailing token — `Anna King` keeps her surname while `Dániel IV Esterházy de Galántha Graf`
loses the `Graf`. 17 people carry `King` as a suffix and far more as a name.

### The same title, at the other two ends of a name field

Two more shapes, both emitting a live statement, both fixed with the same list and neither
reachable by the tail rule:

- **A LEADING title.** `Q110410743` carries `_MARNM` = `Graf von Maltzahn, Freiherr zu
  Wartenberg und Penzlin` and emitted `P734` *family name* `Q1158367` **Graf**.
  `drop_leading_title` strips it and keeps `von Maltzahn` — **`_PARTICLE` is deliberately not
  in that set**, because `von` is an integral part of what those people are called and
  `name_shape` already stops it becoming an item. It never strips to empty: a field whose only
  token is a title keeps it, which is what protects `King`.
- **A WHOLLY TERRITORIAL field.** `Q2705969` *Guaimar II of Salerno Gybbosus* carries `_MARNM`
  = `of Salerno` and emitted `P734` **Salerno**. `drop_title_tail` skips index 0 on purpose — a
  label must never truncate to nothing — but a *field* may, and `drop_leading_territorial`
  empties it. Nobody's family name is Salerno.

**English `of` is a territorial opener IN THE NAME MODEL and only there.** Measured: 16,165
labelled people carry a non-initial bare `of` with something after it, and the tails are places
without exception — `of Egypt` 324, `of Axum` 126, `of Armenia` 83, `of Burgundy` 77,
`of Denmark` 55, `of Sweden` 44, `of that Ilk` 58. No family name in this corpus is introduced
by English `of`. It stays out of `build-garborg-day._drop_territorial`, which trims the label
before transliteration: what `Anne of Denmark` should read in CJK is a question about her label,
answered in § *A TITLE INSIDE A LABEL*.

**The additions pass was NOT passing `fields` at all, and that is the whole root cause.**
Without them `statements_for` falls back to parsing the rendered label positionally, and the
rendered label is `givn + surn + NSFX` run together. The creation path always passed them.
Fixing it moved name statements **145 → 157** on the live batch — the titles and places out, and
real surnames the positional parse had been missing in: `Fleming`, `Boije`, `Henckel`,
`Donnersmarck`, `Oxenstierna`, `Munck`, `Olofsson`, `Eriksdotter`.

### A DESCRIPTION MARKER COMES OUT OF THE LABEL. `ogift` is not a name

`ogift` is Swedish for **unmarried**, and `Q141313961` was live as *Helena Maria Linnerhielm
ogift*.

**The token was never a name statement, and the machinery to keep it out already existed.** It
sits in `namemodel._DESCRIPTION`, a description of the person and never a name, so
`drop_title_suffix` has always kept it out of `P735` and `P734`. What nothing removed it from is
the **label**: `build-display-names.py` concatenates `givn + surn + NSFX` into `display_name`
and `derive-labels.py` takes that string whole.

**The fact is NOT re-emitted as anything.** Nothing goes in its place. The Geni-rendered string
is what `P1810` *subject named as* carries on the `P2600` by design, so the marker is not lost —
it stays as the name Geni renders. **No `P26` *spouse* with no value, no alias, no per-language
rendering.** This is what § *A TITLE IS NOT A NAME* already does with `Graf` and `Queen`.

**SCOPE IS DESCRIPTION MARKERS ONLY.** `drop_title_suffix` would strip `Graf`, `MP` and `Kt.`
from **7,075** labels, 6,385 of them beyond this change; only the 631 markers are in scope. So a
title in a label stays, and § *A TITLE IS NOT A NAME*'s *"it does not touch the LABEL"* is
intact for titles. The difference that makes the two separable: **a title is a thing the person
was; a description marker is an annotation about the record.**

`namemodel.drop_description_suffix` is the one place. Three call sites, wired together rather
than a day apart — `derive-labels.py` (the label and the married-name alias), and both the
correction path and the **creation** block of `build-garborg-day.py`. § *Code that is WRITTEN
but never CALLED is not done* is why the creation block is on that list.

**It matches the person's OWN `NSFX`, never a bare word list against a trailing token** — the
exactness that keeps `Anna King` her surname, and it matters here too: 34 people carry `Twin` or
`Infant` in a *name* field and are untouched. **The comma that introduced the marker goes with
it**, so `Josiah Wood I, twin` becomes `Josiah Wood I` and not `Josiah Wood I,`. **Never to
empty**: a label that is nothing but a marker keeps it.

**Measured over the real corpus, 1,451,993 people: 689 labels change**, plus 7 married-name
aliases. `reports/description-markers-in-labels.tsv` is the census, one row per person, with the
before and after — `twin` 238, `tvilling` 91, `infant` 69, `ug` 52, `ugift` 51, `tvill` 34,
`ogift` 25, `legendary` 18, `concubine` 12, `heiress` 10, `oä` 8, `solteira` 8, `fictional` 6,
`mistress` 6, `fictitious` 5, `tv` 3. **Only one of the 631 is live on Wikidata**, and the
correction path emits it for `mul`, `en`, `en-ca`, `en-us` and `fr`, every language the item
carried it in.

**The corroboration is that three labels moved INTO exact agreement with Wikidata**, 11,154 →
11,157 of 40,898 in `reports/labels.md`. Nothing was tuned to produce that; it is what a correct
removal looks like from the outside.

### A BARE GIVEN NAME IS NOT A LABEL. The farm name is the surname; `NN` fills what is left

A single given name is not an acceptable label. Two rules, and the order between them matters:

| | |
| --- | --- |
| **a surname exists** | use it — `Ånon i /Byre/` → **`Ånon Byre`** |
| **no surname is recorded** | **`Given NN`** — the mirror of `NN Garborg` |

**THE FARM NAME IS THE SURNAME, and the territorial rule was eating it.** Geni files him
`Ånon i /Byre/` — `GIVN` *Ånon i*, `SURN` **Byre** — and Norwegian `i` is the farm designation
that joins them. `drop_label_title` reads `i Byre` as a territorial tail, which is right for
`Judith of Flanders` (§ *A TITLE INSIDE A LABEL*) and wrong here: the place **is** the family
name. `namemodel.keep_own_surname` is the discriminator and it is the person's **OWN
`SURN`/`_MARNM`, never a word list** — the same exactness `drop_title_suffix` and
`drop_description_suffix` use, and for the same reason.

**Only when the truncation leaves ONE token.** `Ragnhild Toresdatter Håland i Gjesdal` still
becomes `Ragnhild Toresdatter Håland`: she has a name either way, and the rescue is for the case
where the label would otherwise be a bare given name.

**Measured: 19 labels move** — `Ånon Byre`, `Henrik Hebnes`, `Peder Mælum`, `Arne Tomb`,
`Olav Tomb`, `Gyrid Øvrebø`, `Sigrid Frang`, `Børild Tjørn`, `Bjorn Grude`, `Louis Steyn`, four
`Chiang`s. Reading them is what set the `av` exclusion: **`Sigward i av Norge` files `av Norge`
as its surname and that is a country**, so a rescued tail that itself opens with a territorial
word is refused. `Louis` is why the comma goes: Geni's `SURN` for him is literally `Steyn,`.

**The FIELD usually carries the preposition, and that is 9 of the 19** — `Arne /på Tomb/` files
`SURN` = `på Tomb`, not `Tomb`. Matching the exact string alone rescued 10; comparing against
the field with a leading farm opener stripped rescued the rest.

**`Marina til Jylland` → `Marina Jylland` is the one to watch.** Jylland is a Danish region, so
it is the `Judith of Flanders` shape — but Geni files it in her `SURN`, and separating a farm
from a region needs a gazetteer, which is the inference this repo refuses everywhere else. The
field is the evidence.

**`Given NN` is not a new shape.** `labels.strip_markers` already says so: `Sara NN` — given
name known, surname unknown — is already right and is left alone. Geni writes `Sara /NN/` when
it records the gap; this writes the same string when Geni leaves the surname empty, which is the
same fact about the same person. **12,596 people**, about one per day's batch.

**⛔ `mul` GETS THE MARKER; EVERY OTHER LANGUAGE GETS PROSE.**

    mul  Sigrid NN                     <- the marker, where the unknown half is
    en   daughter of …                 <- prose, from the nearest named relative
    ja   …の娘

**`Ånon` is NOT an example of this** — he has `Byre` and is rescued above. The population here
is people Geni records with a given name and nothing else: `Sigrid`, `Helvig`, `Katarzyna`,
`Mads`, `Håkon`.

**So these people belong on the DESCRIPTIVE path, not the named one** — § *`NN` is PRESERVED in
`mul`* with the halves swapped, and the same branch `NN Garborg` already takes.
`_carries_marker` cannot find them, which is why the branch test is the **fields**: one token,
and no surname Geni actually records. `Ånon i /Byre/` carries no marker at all, and
`Maria /No name/` has already had hers dropped upstream.

**This reconciles with `labels.drop_marker_surname`**, which deletes a trailing marker —
`Maria /No name/` → `Maria` — over **2,167 people**. Both hold together: the deletion stands, so
the prose form `No name` never reaches a label, and the marker comes back **normalised** as
`Maria NN`.

**598 single-token labels that are a SURNAME or a title residue get nothing** — `Grand`, `King`,
`Queen`, left where `drop_title_tail` dropped a royal style. Appending `NN` there would assert
that somebody's surname is their given name, so the third guard is that the token must be the
person's own `GIVN`.

### PARSE PATRONYMICS BY FORM. Do not parse a name positionally

**Names are not parsed positionally.** There is no standardised representation of patronymics in
GEDCOM, and positional parsing is the ultimate cause of most of the name defects in this repo.
Patronymics are numerous but extremely regular, and they are parsed **by form**: `x-son`,
`x-sen`, `bin x`, `ap x`, `ben x`, `bar x`, `fitz x`, `ferch x`.

**`NSFX` is never a name component.** The components are the father name, the middle name, the
first name and the last name; `NSFX` is none of them, so `drop_name_suffix` removes the whole of
it before any classification. That does not contradict § *DROP TITLES, KEEP ORDINALS*: an
ordinal stays in the rendered label and stays available as `P7338` *regnal ordinal*, a
**qualifier** on the given name. What it stops being is a `P735` or `P734` of its own, which
`II` never should have been.

**`PATRONYMIC` matched six endings and the corpus holds far more.** Measured over 5,416,925 name
tokens: `-son` 187,432 · `-sen` 162,015 · `-dotter` 106,075 · `-datter` 105,351 · `-dtr` 15,849
· `-søn` 2,072 · `-dóttir` 1,424 · `-ović` 961 · `-wicz` 873 · `-ovna/-evna` 198 ·
`-ovich/-evich` 186 · `-sønn` 118. Plus the standalone particles, which had no handling at all:
`ap` 6,702 · `verch` 1,881 · `ben` 1,558 · `bin` 1,477 · `ab` 1,261 · `ferch` 1,234 · `ibn` 865
· `bint` 465 · `bat` 342 · `bar` 315.

**`join_particles` makes `ben Phinhas` ONE token before anything classifies it**, so `classify`
and `classify_fields` need no lookahead and cannot disagree. It also stops `ben` being thrown
away: `ben` is in `PARTICLES`, so `name_shape` dropped it and left `Phinhas` to be read as an
ordinary name. It must never become a `P734` family name of its own — and before this it was
becoming nothing at all. Joined, `Abisha III ben Phinhas ben Yittzhaq ben Shalma` parses as
three `P5056` links, which is what `name modelling.txt` specifies and what nothing could emit
before.

**Scale: 32,558 name records carry a patronymic the old pattern missed** —
`reports/patronymic-forms-newly-detected.tsv`, sorted on the Geni id. `dtr` 15,636 · `ap` 6,620 ·
`søn` 1,983 · `verch` 1,863 · `ben` 1,505 · `ab` 1,258 · `ferch` 1,232 · `dóttir` 1,106 ·
`ovich` 946 · `wicz` 873.

**The LATIN GENITIVE is a patronymic form too.** `Q141312682` *Zacharias Olai Plantin* had
`Olai` read as a family name. The rule is: detect the form, then confirm it against the
father's own given name, so `Petri` on an Italian is not swept up. Swedish and Finnish clergy of the 16th to 18th centuries are named this way as a
matter of course — `Olaus Petri Niurenius`, `Nicolaus Olai Plantin`, `Johannes Benedicti`,
`Petrus Martini`.

**The shape alone decides nothing: 99,005 tokens match it and 1,544 survive the father test.**
`namemodel.latin_patronymic` reconstructs the NOMINATIVE from the stem — `Olai` → `olaus`,
`Johannis` → `johannes`, `Jonæ` → `jonas`, `Samuelis` → `samuel` — and compares it to the
father's own **given** name as a string, folding case and diacritics and nothing else. That
strictness is the whole discriminator: `_skeleton`, which `patronymic_or_surname` uses, confirmed
`Morris` from a father `Meir`, `Zachris` from `Zacharias`, `Kylili` from `Kylilis` and `Maakebzgi`
from `MAKebzgi`. Matching any token of the father's LABEL rather than his given name let a
Cypriot `-is` surname confirm its own inherited form. A Roman numeral is excluded outright —
`VIII` reduced to a stem `vi` and confirmed 29 times before that guard.

**A token the father carries himself is inherited, not derived.** The son of `Olaus Petri` is
`Olai`, never `Petri`, so a `Petri` whose father is also `Petri` is a family name that began as a
patronymic generations back — the same rule, and the same reasoning, `patronymic_or_surname`
applies to the `-son` forms.

**Two forms of one patronymic can sit on one person and both are emitted.** *Zacharias Olai
Plantin* carries `Olofsson` in `SURN` and `Olai` in `_MARNM`; both become `P5056` *patronym or
matronym* with `P144` *based on* the father, and neither carries `P1545` — the ordinal would
assert a generation chain that is not there.

**Four things were measured and REFUSED**, each of which would have put a `P5056` on somebody it
does not belong to:

- **`-es` 76,975 and `-ez` 29,929** — `Jones`, `Alcides`, `Ramirez`, `Perez`. Patronymic in
  origin, inherited surnames by the time they reach us.
- **`-ian` 9,800** — mostly `Christian` and `Sebastian`, which are given names.
- **`Mac`, `Mc`, `Fitz`, `O'`, 9,670** — a patronymic form elsewhere; in this corpus they are
  **attached and inherited**: `MacKinnon`, `McIntosh`, `Fitzalan`, `O'Neill`. Not one occurs as a
  separate token. A separate `Fitz` token would qualify and there is none.
- **Unaccented `ni` and `ui`** — capitalised `Ni` heads `Ni Choon`, a Chinese name, as often as a
  Gaelic one. The accented `ní`/`uí` are unambiguous; it costs 17 occurrences.

**Case is NOT a discriminator for the Semitic particles**, checked rather than assumed:
`Ben Alan`, `Ben Zev`, `Nethanel Ben Yehiel`, `Yitzhak Ben Shmuel` are all Hebrew *ben* — 168
capitalised against 1,346 lower. `bar` has the one real residue, `van Bar Opper-Lotharingen`
being a place in Lorraine, 10 of 185.

**One edge case left alone** — `name modelling.txt` § *edge cases*:

- **`Abisha III`.** The regnal ordinal sits in `GIVN`, not `NSFX`, so the suffix rule does not
  reach it and it still reads as a second given name rather than a `P7338` *regnal ordinal*
  qualifier.

**A particle takes everything up to the NEXT particle.** `bin Haji Muhammad` is a single
patronymic: `Haji` is an honorific and
the father is *Haji Muhammad*, so stopping after one token names the wrong man. Stopping at the
next particle is what makes both readings hold at once — `bin Haji Putih` is one patronymic while
`ben Phinhas ben Yittzhaq ben Shalma` stays three links rather than collapsing into one, which is
`name modelling.txt`'s own worked example.

**`reports/patronymic-identifications.tsv` is every identification**, one row per token per
person: **599,825 over 1,856,150 name records, 20,798 distinct tokens, 36 forms.** Sorted on the
Geni id. The review page built from it is grouped by form, opens on the largest form the widening
added, and carries the example bearers, because spotting a `Ni Choon` needs the person rather than
the token.

**A REVIEW PAGE GOES ON GITHUB PAGES, unlinked. Not an Actions artifact.** An Actions artifact
needs a sign-in and is inaccessible; GitHub Pages does not. So
`scripts/build-pages-site.ALONGSIDE` is the list, `scripts/build-patronymic-identifications-page.py`
is the generator, and the page lands at `/patronymic-identifications.html` beside the batch
**without a link to it** — nothing competes with the daily batch, which is the whole of the
site. A page added to that tuple and **not** to `pages.yml`'s sparse checkout is silently
not published: the runner never checks the file out and the copy is a no-op.
`tests/test_repo_invariants.py::test_every_page_published_alongside_is_in_the_pages_sparse_checkout`
is that check now, over `ALONGSIDE` and over `BATCHES`, so the two files cannot drift apart
unnoticed again.

**⛔ AND THE GENERATOR HAS TO RUN ON THE AUTOMATIC PATH, or the page is a photograph.**
`build-pages-site.py` COPIES `out/`; it generates nothing. So a page whose generator no workflow
runs is published forever as whatever was last committed by hand. Measured 2026-09-09, before
the fix: of the four pages with a generator, `pipeline.yml` ran **one**.

    parent-review.html          build-parent-candidates.py                pipeline.yml
    family-review.html          build-family-candidates.py                review-decks.yml ONLY
    pick-one-review.html        build-pick-one-candidates.py              review-decks.yml ONLY
    patronymic-identifications  build-patronymic-identifications-page.py  NOTHING RAN IT

`review-decks.yml` is `workflow_dispatch` only, so two of the three decks refreshed exactly when
somebody remembered to ask — and a deck retires what has been answered on every rebuild, so a
deck that does not rebuild is a deck that **re-asks**. All four run in `pipeline.yml` now, one
step each and every one `continue-on-error`, because the QuickStatements are the deliverable and
a page riding along must not lose a run that has already produced them. `review-decks.yml` stays
as the on-demand path, for the reason its own header gives.

**⛔ THE SITE PUBLISHES TWO BATCH FILES, and the second one had no page at all.**
`reports/wikidata-garborg-name-items.txt` is **not** folded into `wikidata-garborg-day.txt` —
zero `Den "patronymic"` lines appear in the day batch, and the counts are 94 creations against
12. `--compose` runs that generator as its own step and hard-fails without it. Meanwhile
`pipeline.yml`'s issue body has offered *"[name items](…/wikidata-garborg-name-items.html)"* on
every single run, to a **404**, because `build-pages-site.py`'s docstring asserted *"there is no
second page to publish"* and nobody measured it. `BATCHES` is the list now; `index.html` is still
the day batch and nothing else. A comment asserting a property nobody checked answers the
question for the next reader, wrongly — the same failure as the `pages.yml` sha comment.

**Two generator-less pages are FROZEN and that is not a defect to fix.**
`duplicate-surnames.html` and `duplicate-name-items-we-made.html` were built by hand on
2026-09-07 and no script in the repo names them. They are findings pages — a measurement at a
date — so there is nothing for CI to regenerate. Do not write generators for them to make the
table above look complete.

**Rank the landing form by NEW BEARERS, never by whether any exist.** `-sen` gained seven tokens in
the widening — trailing-dot spellings like `Simonsen.` — so "has a new token" landed the page on its
**162,246** long-established identifications instead of the **15,636** nobody has read. `-sdtr`
is 1,103 of 1,103 tokens new and is what the page should open on.

### A PATRONYMIC SOURCE COMES FROM THE FATHER'S GIVEN NAME. Not from anywhere in his label

`Q141336969` *Johansson* and `Q141290188` *Johansdotter* went live with `P144` *based on*
`Q58785388` *Junna*, and neither is based on that name. **The floor is attestation**: attested
in our own data, plus agentic inference or manual approval.

**`Junna` is the farm name in `Juho Niilonpoika Junna`.** The source walk in
`build-patronymic-items.py` iterated **every word** of the father's label, so a surname three
positions along could attest a patronymic 4,512 people bear — while the Latin-genitive branch
sitting beside it already read `dad.split()[0]` and could not. `namemodel.given_name_run` is now
the one place: the leading run up to the father's own patronymic, or all but the last token when
he carries none.

**⛔ BOTH ATTESTATION FLOORS ARE REFUTED, and the census is the record.**
`scripts/census-patronymic-sources.py` → `reports/patronymic-source-attestation.tsv`, **9,825
(token, source) pairs over 6,864 tokens** with the father count, the share and an example bearer.
Nothing on disk carried that number before: the plan file writes the accepted *names* and not
their weight, so a 4,000-father source read the same as a one-father one.

| rule | pairs dropped | tokens losing every source |
| --- | ---: | ---: |
| fathers >= 2 | 3,999 | **2,654** |
| share >= 10% | 1,573 | 0 |
| first vowel agrees | 407 | 132 |
| vowel agrees OR share >= 10% | 168 | 0 |
| **the father's given-name position** | **64** | 47 |

* **A father-count floor is destructive.** A token three people bear has three attesting fathers
  at most, so `>= 2` takes the derivation off 2,654 tokens.
* **A share floor drops mostly GOOD pairs** — `johnsen ← Johannes` (8 fathers), `henriksen ←
  Henrich` (38), `christiansdatter ← Christen` (14), `olsson ← Olaus` (4). Dropping those is
  precisely what the multi-valued rule exists to prevent.
* Even the tightest blend leaves 168, and **reading all 168 shows most are genuine** —
  `knutsen ← Canuti`, `mortensen ← Martinus`, `staffansson ← Stefan`, `paulsen ← Poul`.

**Position separates them and no threshold does.** Every wrong pair is in the 64:
`johansson ← Junna`, `larsson ← Luur` (from `Anders Andersson Luur Läraktig`), `bjørnsen ← Brun`,
`andersen ← Aanderaa`, `jensen ← in`. A second group falls out for free — `jesenhausen ←
Jesenhaus`, `ekmansson ← Ekman`, `lüttringhausen` — inherited German and Swedish surnames
`patronymic_or_surname` had let through, whose "source" was the same family name in the father's
surname slot. This is § *PARSE PATRONYMICS BY FORM* again: **a threshold was being reached for
where a structural test belongs.**

**A REMOVAL NAMES A VALUE WE CAN IDENTIFY AS OURS AND WITHDRAWN — never "not in today's plan".**
The plan carries a `p144_withdrawn` column: what the unscoped walk would have produced and the
scoped one does not, computed in the same run so it maintains itself. `build-garborg-name-items`
emits `-Q… P144 …` only where all three hold — the item is in `reports/created-name-items.tsv`,
the value is live on it, and the plan names that value as withdrawn. **9 values across 8 tokens.**
A value added by hand is in no withdrawn list and cannot be reached from there; § *The purpose is
to ADD to Wikidata, not to correct it* holds for everybody else's statements, and correcting what
we added is scoped to ours.

### A MATRONYMIC DERIVES FROM THE MOTHER. A female-looking source in the father walk is not one

**The 53 `P144` values whose given-name item is `Q11879590` *female given name* are the WRONG
population**, which reading the rows says plainly:

    adriansdatter <- Adrian (Q372250)      jonesdatter  <- Jone (Q14436586)
    brynildsen    <- Brynild (Q33093604)   herlaugson   <- Herlaug (Q16427631)

`Adrian`, `Jone`, `Brynild`, `Herlaug`, `Fridleif`, `Geirlaug`, `Gunnleif` are Norwegian and Old
Norse **male** names carrying a wrong or unisex `P31` on Wikidata. **A source in the father walk
IS the father's name**, so it cannot make a matronymic however Wikidata classes it. 50 tokens
would have been reclassified on a property of the *name item* rather than of the person.

**Nothing had ever walked the mother.** `census-patronymic-sources.py` now does both:

    father   9,825 pairs over 6,864 tokens
    mother     669 pairs over   476 tokens
    ONLY by a mother   110 tokens, 214 people   <- the matronymics

`Mariasson`, `Mariasdotter`, `Annasson`, `Evasdotter`, `Britasson`, `Evasson`, `Bodilsen`,
`Elinason`, `Rannveigsson`, `Ulrikasdotter`, `Johannasdotter`, `Klarasson` — the son of *Maria*
is `Mariasson`, and that is unambiguous. It answers the question standing in
`build-garborg-name-items`' own comment that matronymic fires for nothing: it fired for nothing
because the mothers were never looked at.

**Two things the mother walk does NOT do, and both are deliberate.**
`patronymic_or_surname` asks whether the *father* carries the same token, so it is a father test
by construction and is not applied on the mother side — there the token's shape and the mother's
given name are the whole evidence. And the Latin-genitive branch stays on the father, since
`name modelling.txt` models that form as his.

**`Q1076664` *matronymic* is the class**, the sibling of `Q110874` *patronymic*. It is in
neither `reports/wikidata-labels.tsv` nor `out/wikidata/name-items-in-store.tsv.gz` (whose 463
patronymic-kind items are all `Q110874`), and a sandbox with no egress cannot look it up, so the
id had to be supplied rather than derived — § *Do not guess these*. Its description reads
*"personal name component based on ones mother's given name"*.

**Only the NAME ITEM changes. Nothing on the person moves.** `P5056` is *patronym or matronym* —
one property for both — so a matronymic bearer carries exactly what a patronymic bearer does, and
what differs is the item's `P31` and its `Den "matronymic"` description, the latter already in
`DESCRIPTION_FOR`.

**The verdict lives in the PLAN, not in the classifier.** `namemodel.classify_fields` reads one
token and `Mariasdotter` looks exactly like `Jonsdotter`; what separates them is whose given name
attests the stem, which is a corpus-wide fact. So `build-patronymic-items.py` writes a `usage`
column and `build-garborg-name-items.matronymic_tokens()` reads it — the same division that makes
`based_on_targets` *"a lookup, not a decision"*. The usage stays `patronymic` for every lookup
keyed on `(token, usage)`.

**A token BOTH parents attest is an ordinary patronymic.** Requiring the father side to be empty
is what keeps this to the 110: a `Jonsdotter` whose mother happens to be `Jona` derives from her
father, and the mother sharing a stem is a coincidence rather than a derivation.

### An abbreviated patronymic is EXPANDED, and `dtr` was never the only form

**An abbreviation in a `mul` label is a compliance defect.** Wikidata `mul` labels take the full
form, so `Anna Ormsd Byre` is `Anna Ormsdatter Byre`.

**The machinery all existed and the pattern matched one form.**
`census-abbreviated-patronymics.py` carried `\b(\w+?)(dtr)\.?` — so `Ormsd`, `Johansdr`,
`Olsdt.` matched nothing, nothing expanded them, and `expand_abbreviations` had no row to find.
Widening to the genitive-preserving family took the census **11,187 → 11,803 rows**: `dr` 325,
`d` 164, `dr.` 58, `d.` 54, `dt.` 33, `dt` 23, and 15 more `dtr`.

**The `s` is load-bearing.** A patronymic always carries the genitive — `Orms` + `d`. Allowing a
bare `d` matched `Svend` 606, `Halvard` 322, `Hand` 92 and `Old` 19, real given names whose stem
happens to be attested with `datter`. Requiring the `s` removes every one and loses nothing.

**Three things were measured and REFUSED, and each would have rewritten somebody's name:**

- **The male side does not exist.** The same shape on `sen`/`son` stems matches `Foss` 762,
  `Ross` 498, `Strauss` 324, `Hess` 241, `Moss` 199, `Voss` 139 — surnames, 3,704 occurrences of
  them. There is no safe male pattern in this data.
- **`(?![a-zø])` is not a letter test.** It let `Þorbjörg Ormsdóttir` match as `Ormsd` and offered
  to "expand" it to `Ormsdatter` — an Icelandic name rewritten as a Norwegian one. `(?!\w)`
  fixes it and removed **52 rows**.
- **A new form with no corpus evidence is SKIPPED, not defaulted.** The `dr` family is largely
  Dutch — `Willemsdr`, `Cornelisdr`, `Jansdr`, `Bruijstensdr` — where the full form is *dochter*,
  and falling through to `datter` turns a Dutch woman into a Norwegian one. **433 of the first
  run's 1,314 new rows landed there.** `dtr` keeps the old fallback, being Norwegian by
  construction.

**`expand_abbreviations` ran on the CREATION path only**, so an item created before the census
covered its form kept the abbreviation forever and nothing noticed. `_label_corrections` now
takes an expansion as its own ground for a correction, alongside the birth-name case — and the
test is that **the live label expands to exactly what we want**, so the only difference between
the two IS the abbreviation and nothing else can be rewritten. An item already fixed by hand simply
matches and is skipped, which `Q141271379` demonstrates.

**Four went out in the first batch** — `Marit Ormsd Byre`, `Ranveig Olsd Trevland`,
`Anna Ivarsd Stokka`, `Magdalena Lauritsd Hogganvik` — and the rest drain under the 60-a-batch
label cap.

**One left alone and worth knowing:** `Rakel Marie Bertelsdt Bertelsdottir Idland` carries both
the abbreviation and the full Icelandic form, and the corpus majority expands it to `Bertelsdatter`
while the record itself says `Bertelsdottir`. `FULL` reads `datter`/`dotter` and not `dóttir`, so
that evidence is invisible to it. One row; mapping Icelandic onto the Norwegian pair is a
decision.

### TRANSLITERATE THE ENGLISH READING. Faithfulness to the source language destroys more than it saves

**Transliterate the English reading by default.** Improvising for faithfulness to the source
language is theoretically better and destroys more than it saves, where the English reading comes
out at a consistent quality.

`scripts/translit_ko_latin.py` is a hand-rolled engine, and so is `translit_no.py` — neither is a
standard program, which is worth knowing before trusting either.

**The principle: a consistent English reading beats an improvised source-faithful one.** The
Korean engine was trying to honour Norwegian phonology and produced `군느브죄르느` for
`Gunnbjørn`; read plainly it is `군뵈른`. Where the two conflict, take the consistent one.

**The measured damage was one mechanism: the engine never used a 받침 where it could.**

    Gunnbjørn   군느브죄르느  ->  군뵈른        Abjörn    압죄르느  ->  압죄른
    Ahlemann    아흐레만느    ->  아흐레만      Adwin     아드위느  ->  아드윈
    Knutsson    크누촌        ->  크누트손      Bjørn     브죄른    ->  뵈른

**1,245 tokens carried the `느` filler; 115 remain.** Four bugs, each one a slot that existed
and was not filled: the epenthetic `으` syllable was composed with no final, so a word-final
cluster split in two (`-rn` as 르느 rather than 른); the `w`/`y` merged-vowel branches dropped the
final slot; a doubled nasal or liquid with no vowel after it was kept, so the second had nowhere
to go; and the palatal set was missing `bj fj mj pj vj` while already holding `nj lj gj hj`.
`ts` was read as the /ts/ affricate when every `ts` in this corpus is a patronymic boundary —
`Knut + sson` — and the affricate belongs to `tz`, which is what `Fritz` has.

**⛔ KOREAN HAS NO ATTESTATION COLUMN TO CHECK AGAINST — 0 of 38,376.** Every `ja` and `zh` change
is scored against the 5,902 tokens Wikidata itself supplies; Korean has nothing, so its rules are
argued from the writing system rather than measured against a corpus. Closing that gap needs a
fetch of Korean labels from Wikidata, which a sandbox cannot reach and Actions can.

### ⛔ WIKIDATA'S LABEL BEATS OURS. An existing `mul` is not ours to overwrite

**Where Wikidata already holds a label, it beats our derived one.** The rule has been violated
by `mul` labels being overwritten with the English form.

**`Q6197518` is the worked case and the vote is exactly 2–2:**

    Svantepolk Knutsson    fr, sv   — and what `mul` already holds
    Svantepolk of Viby     en, nl

`consensus_latin_label` breaks a tie with English, so the batch was about to replace a correct
`mul` with the English territorial form. **The incumbent `mul` now breaks its own tie, before
English.**

**`mul` still does not VOTE, and that distinction is the whole safety of it.** The reason it was
excluded is right and unchanged — a wrong `mul` must not defend its own position, or no
correction could ever reach an item. It does not have to: any string with strictly more votes
still wins outright, and a lone correcting label is a majority of one. What the incumbent wins is
a **tie**, which is precisely the case where there is no consensus to overturn it with.

**Six items across the 1,791 with live labels, and every one is the same shape** — the English
label carrying a title or a territorial that has no business in `mul`:

    Q109296398  Fredrika Eleonora Horn        would have become  … Horn af Ekebyholm
    Q110548812  Maria Stjernblad                                 Baroness Maria Stjernblad
    Q111989591  Margareta Fordbohm                               burgeress Margareta Frodbom, heiress of Ingemarshov
    Q6197518    Svantepolk Knutsson                              Svantepolk of Viby

**The general rule this is one instance of:** where Wikidata already holds a label, it beats our
derived one. Our label is a *proposal*, and § *The purpose is to ADD to Wikidata, not to correct
it* is the same principle from the other side. The narrow exceptions are corrections of **our own
earlier writes** — an abbreviation we expanded, the birth-name flip, a description marker, a
generation suffix — each of which `_label_corrections` names and tests for specifically. A
consensus vote is not one of those: it is us imposing a reading on an item somebody else labelled.

### A TITLE INSIDE A LABEL TAKES THE NATIVE FORM IN CJK, never a transliteration

**イタリアのベレンガーリオ1世** — the native form, `の` for *of*, `王` for *king*, and the same
shape for `zh` and `ko`. Not a transliteration of the English words.

Without the rule, the Arne → Charlemagne line emitted:

    Q274606   Berengar I, emperor of the Romans   ->  ベレンガル・I・エムペロル・オフ・テ・ロマンス
    Q43974    Louis I, The Pious                  ->  ルイ・I・ザ・ピオウス
    Q3743799  Knut Valdemarsson, Duke of Estland  ->  クヌート・…・デューク・オフ・エストランド・アンド・ロランド

`オフ` is the English word *of* spelled in katakana, `テ` is *the*, `アンド` is *and* — the same
failure as the `ソン・オフ・` relationship descriptions of 2026-09-03, in a new place. The table
holds katakana for words that were never names: `of` オフ, `the` テ, `and` アンド, `king` キング,
`duke` ドケ, `count` コウント, `emperor` エムペロル, `bishop` ビスホプ. **17,376 people carry a
bare `of`/`the`/`and` after the first token.**

§ *A TITLE IS NOT A NAME* leaves what `Anne of Denmark` should read in CJK as a separate
question about the LABEL; this is that question answered. `scripts/cjk_titles.py` is the
vocabulary: 29 titles, 80 territories and peoples, 20 epithets, each with its `ja`/`zh`/`ko`
form. `label_in` splits the tail with `namemodel.drop_title_tail`, renders it from the
vocabulary, and composes it BEFORE the name, which is where Japanese and Chinese put it.

    Berengar I, emperor of the Romans          ローマ人皇帝ベレンガル1世   罗马人皇帝贝伦加尔一世
    Berengar II of Ivrea, king of Italy        イタリア王ベレンガル2世
    Louis I, The Pious                         敬虔王ルイ1世              虔诚者路易一世
    Baldwin IV the Bearded, count of Flanders  フランドル伯ボールドウィン4世
    Rozala of Italy                            イタリアのロザラ
    Judith of Flanders                         フランドルのジュディス

**⛔ AN UNKNOWN PLACE OR TITLE IS DROPPED, NEVER TRANSLITERATED.** That is the whole point: a
rule-transliterated `Italy` is `イタリ`, and rendering a word it does not know as a name is what
produced `オフ` and `テ` in the first place. A tail outside the vocabulary yields the name alone.

**Four rules the cases forced, each of which was wrong first:**

* **A katakana title takes `の`, a kanji one attaches.** `エジプトのファラオ` against `エジプト王`.
* **A bare territory takes `の`; a territory WITH a title does not.** `イタリアのロザラ` against
  `イタリア王ベレンガル2世` — reading only the front of `of Ivrea, king of Italy` gave
  `イタリア王のベレンガル2世`, so `is_bare_place` follows the same comma recursion as `render_tail`.
* **A tail can stack two titles** — `of Ivrea, king of Italy` — and the first connective swallows
  the rest as one unfindable place. Retry on the part after the last comma.
* **A title WINS over an epithet.** `フランドル伯髭王ボールドウィン4世` stacks two bynames where
  Japanese writes one.

**Measured over the first 6,000 labels: 5,723 render, and 2 carry a whole-segment English
function word** — `Anna King`, whose surname genuinely is King, and one quoted epithet outside the
vocabulary. **The Latin `mul` label is untouched**; only the CJK forms change.

**The 29 spine people with no title in their label ship first**, once the rule bugs below are
fixed.

### THE RULE IS VALIDATED AGAINST THE ATTESTED COLUMN, and that is what catches a bad fix

**`reports/garborg-name-transliterations.tsv` holds 5,902 tokens whose `ja` came from Wikidata
rather than from the rule.** Agreement with those is a measurement the rule cannot argue with,
and it is the test any change to `scripts/translit_no.py` is scored on:

    baseline          809  (13.7%)
    + geminates     1,014  (17.2%)
    + `dt`          1,023
    - `dj`/`lj`     1,025  (17.4%)

**It caught a fix that made things worse.** Emitting the plain coda for every geminate
fixed `Anna` (アナ → アンナ) and broke `Abba` (アッバ → アブバ), scoring **803 against the
baseline's 809** — worse than doing nothing. A geminate is three things: nasal → `ン`, liquid →
nothing, otherwise → `ッ`.

**And it caught a regression on names that are not Norwegian.** Adding `dj`/`lj` as /j/ onsets is
right for `Djupvik` and wrong for Indonesian `AMIDJAJA`, which lost a consonant entirely
(アミドヤヤ → アミヤヤ). Removing them scored *better*. `tj` and `vj` were never added, for the
same reason: nothing in the data says which language a token belongs to.

**`dt` is one /t/ and the corpus proves it** — of the 24 `-dt` tokens with an attested rendering,
**0 end in `ドト`** (`Schmidt` シュミット ja 33×, `Brandt` ブラント 14×) while **201 of 201**
rule-made ones did. Chinese agrees independently: of the 4 with a real `zh` attestation, 0 contain
德特.

**⛔ NO NOTE IN THAT TABLE HAS EVER CITED A KOREAN ATTESTATION — 0 of 38,376.** The check runs
against `ja` and `zh` only, so the **entire `ko` column is rule output that has never been
compared to anything**, including on rows marked *attested*: `Schmidt` carries `스미드트` where
Korean writes `슈미트`. Given § *CJK INCLUDES KOREAN*, that is a larger hole than any rule bug
here, and nothing addresses it.

### ⛔ A NAME FIELD THAT NAMES A RELATIVE IS NOT A NAME. Geni puts the husband in `GIVN`

`Q141352505` went out carrying the names of her relatives, and the source is **Geni's own
field**, not a Wikidata label. She is recorded `NAME NN ektefelle Søren Jonson /Aukland/`, so her
`GIVN` reads **`NN ektefelle Søren Jonson`**:
`ektefelle` is Norwegian for *spouse* and the rest is her HUSBAND. Parsed positionally it gave
her his given name `Søren` as `P735` with `P3831` *middle name*, his patronymic `Jonson` as
`P5056`, and `Aukland` as `P734` — three statements, all about a different person.

**The tell is structural: an unknown-name MARKER, then a relationship WORD.** `NN` says the name
is missing, `ektefelle` says what follows describes a relation. Neither alone is enough — `NN
Aukland` is the legitimate marker-plus-surname shape and is untouched — and together they cannot
be a name. `build-garborg-day.names_a_relative` reads the relationship words out of
`build-nn-label-batch.WORDS`, the same table `_relationship_prefixes` uses, so a language added
there is covered with no second edit.

**552 people, and reading them is what fixed the shape:** `NN ektefelle Ole Tollefson`,
`Unknown wife of Brand Hereson`, `NN daughter of Walter & Eva`,
`unknown mother of Geoffroy (concubine of Richard I)`, `Unknown Child of Henry I & Mathilda`.

**The field is emptied at the `fields` LOADER, once.** Both `name_lines` call sites sit behind
`_has_given_name`, which then stops firing; `statements_tokens` cannot put a relative's name
into `name-tokens-needed.tsv`; and there is one place to read rather than two that have
disagreed before. The label path is unaffected — these people are `redacted` on the marker in
their label and take `describe_all`.

**This is § *A DESCRIPTION IS NOT A NAME* in the GEDCOM FIELD rather than in the label.**
`is_relationship_description` guards the label and could never have seen this.

`Q141352505` went live with `P735`, `P734` and `P5056` from that field. Only 1 of the 552 is in
the ledger, so that was the whole exposure.

### ⛔ A GUARD IN ONE EMITTER IS NOT A GUARD. And NO GIVEN NAME IS NOT NO NAME

`Q141353755` — `mul` `NN ektefelle Tollak Jonsson III Aukland` — went live carrying `P735` given
name *Tollak*, her HUSBAND; and people created with no given name were getting no name links at
all while their name items existed.

**Two defects, one shape: a rule enforced at a CALL SITE rather than in the model.**

* **`names_a_relative` lived in `build-garborg-day.py` alone.** § *A NAME FIELD THAT NAMES A
  RELATIVE IS NOT A NAME* was fixed on 2026-09-07 in that file's `fields` loader.
  **`build-garborg-name-items.py` builds its own `fields` straight from `display-names.csv`** and
  never went through it, so it emitted a husband's given name as `P735` for two days after the
  fix was called done. It is in **`namemodel.classify_fields`** now, which every emitter goes
  through. The loader keeps its own copy for a different job — stopping `statements_tokens`
  putting a relative's name into `reports/name-tokens-needed.tsv`, which the next day's name-item
  step ranks first.
* **`_has_given_name` gated the WHOLE name block.** So a person with no given name got no `P734`
  and no `P5056` either — `NN Andersson`, `NN Skjelbrei`, every `<private> Surname`, and
  `En dodfodd son Bielke`, the very case the function was written for. **Its own docstring
  promised the opposite** — *"`Bielke` still reaches `P734` through the ordinary path"* — and it
  could not, because the caller never let it. Deleted, from both the additions path and the
  creation path. **6,978 statements unlocked** — 6,709 `P734`, 269 `P5056`, **zero** `P735` — on
  6,595 people.

**⛔ A REDACTED PERSON'S SURNAME IS A `P734`.** The creation path's `if not redacted:` was the
same failure with a different name. § *Redacted people go in* already says it: `<private>
/Larsson/` withholds the GIVEN name and not the family one, and the surname *"feeds the `P734`
family-name work"*. The gate was built on a redundancy argument over **three** people —
*"`Garborg` is their father's family name, which `P22` already says"* — and redundancy is never a
reason to withhold a statement (§ *The purpose is to ADD to Wikidata*). It then generalised over
a `redacted` test that has widened enormously since: **114,782** people carry a marker or
`<private>`, of whom **4,798** have a name the model resolves today.

**Nothing was needed in its place, and that is measured rather than argued.** The marker never
becomes a name: `<private> Garborg` yields `P734` Garborg alone, `Private` yields nothing, and
`En dodfodd son Bielke` yields `P734` Bielke alone.

**⛔ AND A GUARD MASKS WHAT IT GUARDS. Removing these surfaced two live defects underneath:**

* **`drop_leading_title` MANUFACTURES A NAME OUT OF "THERE IS NO NAME".** It reads `Stillborn` as
  a title, so `Stillborn Son` reached `classify_fields` as `Son` and `Stillborn daughter 1` as
  `daughter 1` — and `is_description` matches the phrase **whole**, so it never saw one. **296
  stillborn people** would have gained `P735` *Son*, *daughter* and *1*. `statements_for` now
  blanks `givn` when `is_description` fires on the **raw** field, before the drop chain.
* **THE MARKER VOCABULARY WAS IN TWO PLACES AND `scripts/labels` OWNS IT.** § *An obvious
  unknown-word marker goes straight in* says a new marker goes into
  `labels.WORDS_MEANING_UNKNOWN` **and nothing else** — so `namemodel.UNKNOWN_MARKERS`, a
  hand-kept set, was blind to **28** markers added there since: `未知`, `佚名`, `unbekannt`,
  `onbekend`, `inconnu`, and `某`, an approved marker and the whole given name on **275**
  people. Every one was emitting `P735` given name `某` — *a certain
  one*. `name_shape` unions both now.

**The check before calling a name rule done:** *is it in `namemodel`, or in the emitter I was
looking at?* There are two emitters and they have disagreed before — § *A TITLE IS NOT A NAME*
says so in as many words. This is § *Code that is WRITTEN but never CALLED is not done* with the
call site present and wrong rather than absent.

### A PERSON IS CREATED WITH THEIR NAME LINKS. Two things were stopping it

**A person is created already carrying their name links, and this was not happening
reliably.** Measured on one batch: of **56** people
created, **9 carried no name statement at all**, and of the 184 they should have carried,
**107 had no item to link to**. Exactly **1 of the 56** could link every token.

**⛔ CAUSE ONE — the first `NAME` record is often the one with NO components.** Geni writes the
bare rendered form as one record and the parsed one as another:

    0  Anders Persson Hägg   givn=''       surn=''        marnm=''
    1  Anders /Persson/      givn='Anders' surn='Persson' marnm='Persson Hägg'

`fields` took row 0 first-wins, `statements_for` had nothing to parse, and the person went out
with no name at all. **The components are backfilled from the first row that has them;
`display_name` is NOT** — that column is what `P1810` *subject named as* carries, and for
`Anders Persson Hägg` the bare row is the fuller rendering. Two questions off two rows.

**⛔ CAUSE TWO — the name-item step cannot see who the ring is about to create.**
`build-garborg-name-items.py` draws its bearers from `garborg-qids.tsv`, people who **already**
hold a QID, and ranks by bearer count. A token needed by somebody being created today was
invisible to it and lost to tokens borne by hundreds of long-standing ledger people. The cap is
40 name items a day against **~90 new tokens a batch**.

`build-garborg-day.py --compose` now writes `reports/name-tokens-needed.tsv` and the name step
ranks those first — the two run in that order, which is what makes it possible.
**It does not make TODAY's links appear**: a person and a name item minted in one batch cannot
point at each other. It makes tomorrow's land, which is § *The batches are a SEQUENCE* working
rather than drifting.

**Gating creation on full name coverage was measured and REFUSED**: 1 of 56 people qualifies,
so it would stop the ring rather than fix it.

### A TOKEN THE CORPUS NEVER USES AS A FIRST GIVEN NAME IS NOT A GIVEN NAME

`Q141352791` — an item labelled `Garborg`, `P31` *given name* — was minted by our own generator
for two people. `Garborg` is a surname.

**The cause is positional parsing, in a new place.** Geni files both bearers as `GIVN` =
`Arne Garborg` / `Siri Garborg` with an **empty `SURN`**, so the name model reads the second
token as a middle name. Neither has a Garborg parent — `Martin Tollefson Tunheim` and
`Sigurd Sverre Ravn Talle` — so they are children named after the writer, and `Garborg` is his
surname. Our own `name-item-plan.csv` already holds it as `family`, 39 bearers, `Q30250555`.
§ *PARSE PATRONYMICS BY FORM. Do not parse a name positionally*.

**⛔ THE TEST IS CATEGORICAL AND IS NOT A DOMINANCE RATIO.** § *One name item per USAGE* — a
token that is both a surname and a given name gets both objects — forbids ADJUDICATING between
two real usages, and is untouched. This asks a different question: **is there a given-name usage at all?** A token that is a first given name **zero**
times and a family name **at least once** has none. Nothing is weighed.

    Garborg    first 0       later 4       family 285   -> refused
    Maria      first 31,129  later 18,255  family 50    -> untouched
    Johan      first 25,273  later 7,390   family 14    -> untouched
    Waldemar   first 101     later 270     family 0     -> untouched

`scripts/census-given-name-attestation.py` → `reports/given-name-attestation.tsv`, 301,196
tokens. **A missing census file means every token passes**, so a derived file that was not built
cannot silently start refusing names.

**Two rules were tried on the way here and BOTH are refuted — do not propose either again:**

* ***"the token is a family name elsewhere"*** — **242,831 people**, headed by `Maria`, `Marie`,
  `Elisabeth`, `Johan`, `Gustaf`. Being a surname somewhere says nothing at all.
* ***"`SURN` empty and `_MARNM` present, so the last `GIVN` token is the birth surname"*** —
  **168,309 people**, and the last token is `Johan` 2,773, `Fredrik` 2,427, `Maria` 2,419, then
  `Waldemar`, `Verónica`, `Hazel`. It would have rewritten every one of their names.

**The two live statements are still wrong and nothing here removes them.** `Q141168788` and
`Q141216501` each carry `P735` → `Q141352791` with `P3831` *middle name*. A `P734` in its place
would assert Garborg is their family name, which their parents contradict, so the honest
correction is removal and `Q141352791` orphaned — not yet wired.

### A middle initial keeps its Latin letter in every language

`John F. Smith` becomes **ジョン・F・スミス** and **约翰·F·史密斯**. Dropping the initial loses
what the Latin label carries, and rendering it エフ invents a reading nobody uses.

**A bare lowercase letter is a WORD, not an initial.** The first rule was
`^[A-Za-z]\.?$` with an `.upper()`, and it turned `Ragnhild Toresdatter Håland i Gjesdal` into
`ラグンヒル・トーレスダッテル・ホーランド・I・イェスダール` — Norwegian `i` means *in*. An
initial is capitalised, or carries a full stop; case is never changed. Found by reading the
emitted batch, which is the only thing that would have found it.

`scripts/labels.transliterate_token` is the single place that does it, and both emitters call it.
**It is the one exception to *partial is worse than absent*, and it is barely one** — an initial
is not a name being half-rendered, it is a letter that is the same letter in every script. An
unknown *name* still blocks the whole label, which `tests/test_join_sanity.py` pins.

**12,805 tokens sit in the middle-initial position**, and every name containing one was getting
no `ja`/`zh` label at all.

### Redacted people go in. `Private` never becomes a label

**Redacted data still goes to Wikidata, because it is still informative.**

**Geni has TWO redaction markers and they withhold different amounts.** Of the
corpus's 390,560 profiles:

| form | count | what survives |
| --- | ---: | --- |
| `Private` | **16,402** | nothing; the whole name is gone |
| `<private> /Surname/` | **3,605** | **the surname is real data** |
| `NN` or blank | 772 | nothing |

`<private> /HUÁNG 黃/`, `<private> /Rådestad/`, `<private> /Larsson/` — the
**given name** is withheld and the family name is not. Treating those as fully
redacted throws away 3,605 surnames, which is exactly the material worth having.
`surname_of()` exposes it; a bare surname is not a person's label, so it
feeds the `P734` family-name work rather than the label.

- **The person is created.** What is informative is the structure, and none of it
  is redacted: the Geni ID, the sex, the parents, the children, the dates.
- **The item gets no label.** "Private" is a redaction marker, not a name, and an
  item labelled that asserts something false while being impossible to find. The
  `P2600` is what makes it retrievable.

`scripts/labels.py` is the single place that decides this — `label_for()` returns `''` for
`Private` and `<private>` **and nothing else**. `NN` is *nomen nescio*, a genealogist saying the
name is unknown: a real statement about a person, not Geni withholding data, so it is not in that
set. A caller that falls back to the raw string when it gets `''` reintroduces the whole
problem.

**This is the same rule as the Samaritan "wives" in `docs/future-modelling.md`,
with the opposite outcome, and the difference is what to check for.** `daughter
of Sanballat the Horonite` is also not a name — but she has no identifier and no
structure, so there is nothing to create. A `Private` profile has both. The test
is never "is the label bad", it is "is there anything real underneath it".

**Do not confuse redacted with unnamed.** The seed of
`exports/samaritans/export-Forest-6000000178794141887.ged` is
`NN /bint Aabed-El ben Asher ben Matzliach/` — that is how she is *recorded*, not Geni
withholding a name it holds, and her record comes through complete. Only 29 of that export's
4,820 people are `Private` at all, so an export seeded on a living person is **not**
substantially redacted.

### A parenthesised token in `SURN`/`_MARNM` is THREE different things

5,866 occurrences over 2,495 distinct tokens, across 1,697,887 name records, ruled case by case
from the raw records.

| shape | example | tokens / occurrences | ruling |
| --- | --- | ---: | --- |
| **any name-shaped token** | `Turesson (Bielke)`, `Weirman (Weyerman)` | 2,478 / 5,553 | **BOTH** — a second `P734` *family name* with the parens stripped, **coequal and unqualified**, plus an `Amul` alias carrying the bracketed form |
| **particle or honorific** | `(de) Worms`, `Henriques (D.)` | 9 / 205 | **into the `mul` label**, never a name item |
| **unknown-name marker** | `(anonyma)`, `(incognita)`, `(?)` | 8 / 108 | **an NN marker** — joins `Private`/`NN`/`Ukjent` |

**A particle belongs in the `mul` label**, because it is an integral part of what the people are
called. So `de` is not dropped and is not an item — it belongs in the label the person is read
by. `(de)` occurs 97 times and bare `de` 125,328, so this
governs a large population beyond the parenthesised ones.

**Nothing tells a noble house from a spelling variant, and nothing needs to.** The two shapes
are identical, so `Weirman (Weyerman)` yields **two `P734` statements** plus the alias. This is § *One name item per USAGE* again: a token in two
roles is not an ambiguity to resolve.

**And no qualifier on either.** Both surnames are coequal properties. Nothing marks one as
primary, because nothing in the data says one is.

**Two discriminators were built and both are gone.** Bare-form frequency was refuted by the
census written for it — `Voehl` occurs 20 times unparenthesised and `Loewenberg` 292, so
`Vöhl (Voehl)` and `Levi (Loewenberg)` came out as houses when they are plainly spellings.
String similarity to the neighbouring token did separate every ruled case, and was a similarity
heuristic in a repo that bans them. **Emitting both removed the question instead of settling
it**, which is worth remembering the next time a rule appears to need a threshold.

### A nickname alias carries the SURNAME. `P1449` is NOT emitted

`Q141189102` *Sigrid "Sally" Manilva Tunheim* was given an alias of `Sally` rather than
`Sally Ekman`. The alias carries the surname:

    Amul  alias      Sally Ekman        <- nickname + the MARRIED surname
    Amul  alias      Sigrid Manilva Ekman

**`P1449` is dropped.** It is monolingual text, so it needs a language tag; the tag being
emitted was `en`, declaring `Byre` and `Christophersdatter` to be English words. **No right tag is available
either** — the nickname is Norwegian on a person whose label is language-neutral `mul`, and
guessing a language per person is the inference this repo refuses everywhere else.

**The nickname is not lost.** It is still recognised, still kept out of the given names, and
still reaches Wikidata as the `Amul` alias above, which is all that is wanted: `Lmul` and
`Amul`.

**The drop lives in `namemodel.statements_for`, the one place that models a name.** It sat in
`build-garborg-day.py` for a day instead, so the model went on producing `P1449` while nothing
could emit it, and `model-vs-reality.py` reported **66 people missing a nickname** no batch
would ever add. A phantom gap is worse than a silent one, because it reads as work.

The married surname is used because § *The MARRIED name is the real name* makes it the form the
primary label takes, so the alias is the same person's name with the nickname swapped in.

**Wikidata's own rule is why the bare form is useless**, checked 2026-08-26 against
`Help:Aliases`: *"the purpose of aliases is only to find entities in searches"*. A bare `Sally`
is not something anybody would search.

**The label stays the FULL name, and quotes never go in a label.** Two alternatives were looked
up rather than guessed — nickname-as-label with the full name as alias, and keeping the quotes
inside the label. `Help:Label` supports nickname-as-label only
where the nickname genuinely IS the common name (*Xavi* against *Xavier Hernández i Creus*);
`Help:Default values for labels and aliases` makes the default label the native full name in
Latin script. **Nothing on any of the three help pages puts quotation marks inside a label.**
For a 19th-century farm woman there is no source saying she was commonly known as Sally — Geni
records only that she was called it — so the full name stays the label.

### The MARRIED name is the real name. `mul` carries it, and no batch adds an `Aen`

**The married name is always the real name**, and it is the primary `mul` label; the birth name
follows as an `Amul`. No `Aen` is ever added — only non-Latin scripts get an alias for a birth
name that cannot live in `Amul`.

    en    Aagot Garborg      <- married, primary
    mul   Aagot Garborg      <- married again. `mul` is the real label.
    Amul  Aagot Nyvold       <- the BIRTH name, an ALIAS
    ja    オーゴット・ガルボルグ    <- transliteration of the PRIMARY form
    Aja   (birth form, where it differs)

**`(first amul added if applicable)` is a preservation step, not an ordering quirk.** A label
REPLACES, so whatever the item currently reads in `mul` goes out as an `Amul` on the line
*above* the `Lmul` that overwrites it. Some of those are hand edits — `Q141152600` holds
*Stena Eivindsdatter Garborg*, which nothing in this repo could reconstruct.

**`Aen` is never emitted.** `mul` is the language-neutral label and an alias living only in
`en` is invisible to every other language. The one exception is a **non-Latin** birth form,
which cannot live in `mul` and gets `Aja`/`Azh` — a different language code, not an `en` one.
A *removal* (`-Q123 Aen "..."`) is fine and is how the wrong ones already on Wikidata come
off. `tests/test_p2600_batches.py` fails any batch that adds one.

**Two emitters disagreed on this until 2026-08-26** — `build-garborg-day.py` had the married
name in both labels, `build-label-corrections.py` had the **birth** name as `Lmul`. Neither
was tested against the other, and the alias half was got wrong twice in opposite directions:
`Aen` alone, then `Aen` *and* `Amul`.

### `NN` is PRESERVED in `mul`. Descriptive labels are ADDED in other languages

**`NN` is never relabelled.** It is always preserved in the language-neutral label; the other
languages gain descriptive labels for the relationships. So the shape on a Wikidata item for an
unnamed person is **both**:

    mul  NN                              <- the marker, never removed
    en   daughter of Fujiwara no Tadaki   <- descriptive, added

**This nearly went wrong at scale.** `build-nn-label-batch.py` emitted
`set_label` on `en` with `"replaces": "NN"`, and NN lives in `en` on **1,549** of
the 1,588 such items and in `mul` on only **278** — so the batch would have erased
the only copy on 1,271 items. Measured over the store, not supposed:

    en 1549 · nl 671 · mul 278 · cy 25 · be 6 · pl 4 · ru 3 · da 3 · ca 3

The fix is two edits per item, the `mul` one declared as a dependency of the `en`
one, so the marker is written before the slot holding it is reused. An item whose
`en` already says something real is left alone (36 of them).

**And it went wrong AGAIN on 2026-09-03, in the other direction: the description was promoted
INTO `mul` and then transliterated as a name.** `Q141249589` went out as `Amul "NN"` followed by
`Lmul "son of Astri Torchelsdatter Øvre Time"` — the marker demoted to an alias and the English
sentence made the language-neutral label — and then as
`Lja "ソン・オフ・アストリ・トルケルスダッテル・オヴレ・ティメ"`, which is the English words *son* and *of*
spelled out in katakana. `zh` and `ko` the same: `松·奥夫·`, `손 오프`. Eight labels in one batch, on a rolling window
with 2,552 behind it, and it was caught on the published site rather than in the generator.

**One cause, two symptoms.** `consensus_latin_label` reads the `en` label first — and for these
people `en` is our own descriptive sentence, by design. Nothing anywhere said *a description is
not a name*, so it became the `mul` label and then went through `label_in`, the name
transliterator.

**`build-garborg-day.is_relationship_description` is now that sentence, and `label_in` refuses
one outright** — the choke point, so every caller is covered including ones written later. Its
prefixes are derived from `build-nn-label-batch.WORDS`, never restated, so the direction rule
(`datter af` but `mor til`) and any language added there come free. `describe_all` already built
the right CJK form — `…の息子`, `…之子`, `…의 아들` — so refusing loses nothing. It is a PREFIX test:
`Anne of Denmark` is a name.

**A relative whose own label is a description names nobody either**, and it composed rather than
stopping: `daughter of father of`, `wife of Son of Menon III Pharsalos`. 21 of those are sitting
in `reports/wikidata-placeholder-labels.json`. Same fix as a marker — fall through to the next
relative, never reconstruct.

**`Private` and `NN` are the same population and get the same treatment**, because a private
individual whose name is not exported comes out as an `NN`. The rule one section down — *`Private` never becomes a label* — was right about what must
not be written and wrong to stop there: emptying it leaves an item with no way to
be read at all, which is the same objection. **Neither marker is a label; neither
person is left unlabelled.**

### `name modelling.txt` is the authority on how a name is modelled

**Hand-written, in the repo root.** It supersedes what this file previously said, and where the
two disagree it wins. Anything unclear in the modelling goes to `AskUserQuestion`.

**The patronymic is `P5056` patronym or matronym — NOT `P735` with a qualifier.** This file used
to say the patronymic was a `P735` given name carrying `P3831` → `Q110874`, with the name item an
instance of `Q110874`. The model gives the patronymic **its own property**, parallel to `P735`
and `P734` rather than nested inside `P735`:

    Vladimir Putin (Q7747)
      P735 given name          Vladimir (Q2253934)
        P1545 series ordinal   1
        P7452 reason for preferred rank  usual forename (Q3409033)
      P5056 patronym or matronym  Vladimirovich (Q27670878)
        P144 based on          Vladimir Putin (Q19300851)  ← his father
      P734 family name         Putin (Q30524893)

**`P144` based on points at the FATHER, the person.** Not at a name item — *his father, who has
the same name*. That is a different claim
from what this file recorded before, which had `P144` on a patronymic *name item*
pointing at the name it derives from.

**The first given name carries `P7452` → `Q3409033` usual forename.** A middle
name instead carries `P3831` → `Q245025`, which is unchanged:

    Donald Trump (Q22686)
      P735 Donald (Q13422248)   P1545 1   P7452 usual forename (Q3409033)
      P735 John   (Q4925477)    P1545 2   P3831 middle name (Q245025)
      P734 Trump  (Q16944413)

**Chained patronymics get one `P5056` each, ordered by `P1545`.** The worked example, which is
**not on Wikidata yet** — it is what should be there:

    Abisha III ben Phinhas ben Yittzhaq ben Shalma (Q107534535)
      P735 Abisha    P1545 1   P7452 usual forename   P7338 regnal ordinal 3
      P5056 ben Phinhas    P144 Phinhas ben Yittzhaq ben Shalma   P1545 1
      P5056 ben Yittzhaq   P144 Yittzhaq ben Shalma               P1545 2
      P5056 ben Shalma     P144 Shalma                            P1545 3

So `P144` on each link points at **the person that link names** — the father, then
the grandfather, then the great-grandfather — and `P1545` numbers the links
outward from the bearer. The regnal ordinal sits on the **given name**, not on the
person.

**The data problem, and it governs how the tokens are read:** some people have patronyms and no
surnames, some surnames and no patronyms, some first name + middle name + patronym, some first
name + patronym + given name. Geni's surname field does not reliably correspond to a surname
rather than a patronym, so **both** the given names and the surname are checked for which it is.

**Both fields, always.** A patronym can be in `GIVN` or in `SURN`, and which field
it sits in decides nothing.

**Edge cases go to `AskUserQuestion`, not to a rule.**

**`Q3409032` and `Q3409033` are adjacent and are different things** — *unisex
given name* and *usual forename*. Confirmed offline against
`reports/wikidata-labels.tsv`, along with `P5056`, `P7452` and `P7338`.

**What survives from the old text:** Geni writes `Ole Olsen` into `GIVN`, so the
patronymic lands in the position a middle name occupies — `Olsen` is a *given*
token for 742 people and a surname for 266, measured in `reports/name-classes.md`.
*"The daughter and son would be the same thing"* — `-son` and `-datter` are one
category.

**How a patronymic item records what it derives from: `P144` based on.** Measured
on 2026-08-15 over the 633 items that are `instance of` `Q110874`: **`P144` on
119 of them**, plus `P5278` *surname for other gender* on 97 — which is the
`Olsson` ↔ `Olsdotter` pairing. `P1705` native label (513), `P282` writing system
(579) and `P407` language of work or name (370) are the near-universal ones.
The derivation is also stated in the item's **description text**, not only as a claim.

**That measurement is the one live Wikidata query this project has made since the
rule, and it was authorised specifically** — a question about Wikidata's own modelling
conventions is a legitimate reason to query it, where wanting to figure out something about a
random individual is not. It was one aggregate
`SPARQL` query, no per-item lookups, run only after the local store was checked
and found not to hold `Q110874` — the store is a Geni-shaped slice of **people**
and carries almost no name items. **The rule is unchanged**: the exception was
for a question about Wikidata's own modelling conventions that the store cannot
answer, granted explicitly, once.

**`P3831`, `Q110874`, `Q245025` and `Q202444` were confirmed offline**, against
`reports/wikidata-labels.tsv` from the bulk download.

`P1545` is how a person with several given names keeps them in order: each P735
statement carries the ordinal of that name within the full given-name string.
`genimerge.namelinks` emits it (`SERIES_ORDINAL`), and it has not yet appeared
in a generated batch, because no matched person so far has more than one
given-name token. So it is correct-by-confirmation rather than
correct-by-observation — the first batch that includes one is worth reading
closely.

**Date qualifiers** — the GEDCOM modifiers map onto these

| GEDCOM | Wikidata |
| --- | --- |
| `ABT` / `EST` / `CAL` | P1480 sourcing circumstances = `Q5727902` circa |
| `BEF` | P1326 latest date |
| `AFT` | P1319 earliest date |
| `BET x AND y` | P1319 earliest date + P1326 latest date |

**References** — P248 stated in, P854 reference URL, P813 retrieved,
P143 imported from Wikimedia project.
