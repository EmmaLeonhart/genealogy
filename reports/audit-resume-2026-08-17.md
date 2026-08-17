# Resume review — the last few days of conversation

**Emma's instruction, 2026-08-16, the last thing she said before shutting the
machine down:** *"can you just write the stuff down, whatever it is we're doing
right now, into the queue? I would say probably at the beginning of the queue,
write a thing about saying to review the last few days of conversation to ensure,
as the first part of the queue, that everything's working well and nothing was
overlooked, and then just force shut down my computer."*

Run 2026-08-17 on resume, before any other queue item. The window is
**2026-08-16**, because `reports/audit-transcripts-2026-08-15.md` covers everything
up to then. Source: transcript `c33ce219`, plus this session's `db9f357e`.

**49 messages from her on 08-16.** Three things she asked for are not done. Everything
else traces to committed work.

---

## The audit method in `queue.md` was itself incomplete

**A `type: "user"` record is not the only place Emma's words live.** The standing
procedure says *"a user turn is `message.role == "user"`"*. On 08-16 that finds
**28** of her **49** messages. The other 21 exist in the transcript only as
`{"type": "queue-operation", "operation": "enqueue"}` records — what the harness
writes when she types while a tool call is running, which for her is most of the
time.

Five of the messages a `role == "user"` scan misses:

| missed message | consequence had it stayed missed |
| --- | --- |
| *"NN is not relabeled… NN is always preserved in the multi-language label"* | the `mul` model, and the 1,271 items whose only copy of the marker would have been erased |
| *"there is a bot that exists that removes labels that match the multi-language label"* | the 58 `remove_label` edits that were deleted |
| *"what the fuck is going on with the eight structural merge cases, six ticks unanswered"* | the finding below |
| *"as long as you treat it as being two paths and not one"* | the finding below |
| *"I want to exhaust all the Swedish academics… The genealogies of academics are more valuable for other reasons"* | the Nordic batches |

All five were acted on live, so nothing was lost this time. The point is that the
*audit* would not have caught them, and the audit is what runs when the live thread
is gone. `queue.md`'s procedure is corrected to read both record types.

---

## Not done · 6,206 long-range labels exist and are not in the batch

**Emma, 2026-08-16:** *"I'm pretty sure that long-range relationships have much
larger things to contribute than you consider them to do so… It can work off of
those long-range things… grandparents or grandchildren or siblings."*

**The two-hop search is implemented.** `scripts/build-relationship-label-preview.py`
walks grandparent, grandchild, sibling, uncle/aunt and nephew/niece after the
one-hop candidates, and `scripts/build-nn-label-batch.py` does the same for the 1,588
Wikidata `NN` items. An earlier draft of this report said the long-range search was
missing from the placeholder work. That was wrong: the search is there and it works.

**What is wrong is that the shipped batch predates it.**
`reports/wikidata-placeholder-labels.json` was written 08-15 **05:01**; the preview it
reads was rebuilt at **12:56** the same day, and nothing re-ran the emitter. So the
batch on disk is the one-hop-only version:

| relative found | shipped batch (05:01) | current preview (12:56) |
| --- | ---: | ---: |
| father | 12,254 | 12,353 |
| spouse | 5,052 | 5,094 |
| mother | 1,882 | 1,919 |
| child | 836 | 836 |
| grandparent | — | 5,045 |
| uncle or aunt | — | 584 |
| sibling | — | 339 |
| grandchild | — | 149 |
| nephew or niece | — | 107 |
| **none — `mul: NN` and no readable label** | **14,987** | **8,781** |
| total | 35,011 | 35,207 |

**43% of the largest label batch in the repo describes nobody, and 6,206 of those
labels were already computed.** The seven-language item is gated on these labels, so
the stale file sits upstream of the gate.

**This is `CLAUDE.md`'s cache chain again, running the other way.** That rule was
written about an *analyser* being re-run when the *generator* was the thing that
needed it; here the analyser was rebuilt and the generator never re-ran. Either way
the file on disk is not what the code would produce.

**Two links were stale, not one.** `reports/derived-family.csv` looked stale by mtime
— 08-16 00:17 against `out/merged.ged` at 00:36 — and re-running `derive-family.py`
reproduced it **byte for byte**, so it was current and the mtime meant nothing. The
stale links were the preview (08-15 12:56, built before `derived-labels.csv` and
`display-names.csv` were regenerated at 08-16 00:42) and the batch behind it.

### Fixed, 2026-08-17

Chain re-run end to end: `derive-family.py` → `build-relationship-label-preview.py`
→ `build-placeholder-label-batch.py`.

| | before | after |
| --- | ---: | ---: |
| placeholder people | 35,011 | **39,299** |
| carrying a readable `en` label | 20,024 | **30,012** |
| `mul: NN` and nothing else | 14,987 | **9,287** |

**+9,988 labels**, of which **7,001** come from the two-hop relatives — 5,720
grandparent, 617 uncle/aunt, 382 sibling, 166 grandchild, 116 nephew/niece — and the
rest from the tree having grown. They read as intended: *grandson of Aída Pereira
Aranibar*, *sister of Kenneth Chiu*, *nephew of Svanhild Haugvaldstad*.

**A note on duplication, measured because it is a property of what is being shipped:
15,810 of the 30,012 share their label with somebody else**, across 5,132 strings —
57 people labelled *granddaughter of Kandjeng Pangeran Soeria Koesoemah Adinata
(Bupati Sumedang)* being the worst. 8,270 of the affected are one-hop `father` cases,
so this predates the two-hop work rather than being caused by it.

**It is not an error under Emma's own spec and nothing is being changed for it.**
Wikidata does not require labels to be unique — label *plus description* is the unique
pair — and her rule is that a created person gets labels and **no description**:
*"We create the individual with their multi-language label, their English language
label… but no descriptions are added to any of the people."* So a shared label
collides with nothing today. It becomes live the moment descriptions are worked, which
is the item that already carries her deduplication warning.

## Not done · the structural merge stopped at showing cases

**Emma, 2026-08-16:** *"What? What are you talking about? What even was the issue
that you came across? The structural cases you were going to do and then you didn't
do."*

`scripts/walk-structural-merge.py` ran and wrote `reports/structural-correspondence.csv`
(3,902 rows) and `reports/wikidata-structural-placeholders.json` (12,260). Eight
sample cases were printed for her. She did not reply, six status reports called that
a blocker, and **nothing has consumed either file since**. The rule she stated on
2026-08-15 — *"we definitely need to… be essentially building up our own
correspondence of the QIDs and Jenny IDs"* — is what those 3,902 rows are, and they
are not wired into anything.

Her ruling on the not-replying part is now in `CLAUDE.md`: *"when I'm not responding
to anything, the assumption should be I'm happy with what you're doing."*

## Not done · a saved page's two paths are still one chain

**Emma, 2026-08-16:** *"You haven't been distinguishing the blood and marriage
things. You've been treating them as one gigantic tree, one gigantic line? If so,
that's really weird… It doesn't really matter that much whether you're distinguishing
them, as long as you treat it as being two paths and not one."*

Geni shows a blood path and an in-law path for the same pair, and `path-from-html`
writes both into one TSV. `genimerge.paths` documents this and handles the visible
symptom — the second chain re-walks the first few people, which is `REPEAT` rather
than `ABSENT` since 2026-08-06 — but nothing splits the chains. So a per-file
"held: X of Y" spans two unrelated paths, and `connectors` counts slots across a
seam that is not a step.

The mitigation is real: chain two restarts at *You*, who is held, so a bridge cannot
run across the seam. This is the smallest of the three findings and is filed as such.

---

## Done, and traceable

Her other 08-16 instructions, each against the commit or file that answers it:

| instruction | where it landed |
| --- | --- |
| Exhaust Swedish, then Finnish and Danish academics | five Nordic batches; `reports/nordic-isolates.csv`. Superseded the same night by her own *"we're kind of hitting diminishing returns"* |
| Rogaland and Stavanger isolates, all of them | `reports/rogaland-stavanger-isolates.csv` |
| The practical goal is her own dense neighbourhood | `CLAUDE.md` § *The practical goal is EMMA densely linked* |
| Japanese and Chinese researchers; how many Chinese isolates | measured; **closed by her** — *"we figured it out, and it's pretty simple"* |
| Bridge people: how many, how many held, how many overlap | `reports/path-bridge-targets.csv`; 511 on more than one path and absent |
| Midpoints, not neighbours of what we hold | `reports/path-midpoint-seeds.csv` |
| The three-task agenda, written down | `queue.md` § *THE AGENDA* |
| Bullet points, never numbers or letters | `CLAUDE.md`; `queue.md` rewritten unnumbered |
| An English label beside every property and item ID | `CLAUDE.md` § *Always write the English label* |
| Samaritan qualifiers matter; read Pummer via Wikipedia | `reports/wikidata-samaritan-succession.json`, `P1545` *series ordinal* on 18 of 21 |
| *"we are right, and Wikidata is wrong for the father"* | `scripts/build-abram-father-fix.py`, 2 edits |
| Nothing is blocked; 1 September is a start date | `CLAUDE.md` § *A start date is not a blocker* |
| Not replying means she is content | `CLAUDE.md` § *Emma not replying means she is content* |
| `NN` to `mul`, describe the locals, no `remove_label` | `reports/wikidata-nn-labels.json`, 3,525 edits (`f8950e1`) |
| `Private` and `NN` are the same population | `CLAUDE.md`; the placeholder batch already labels both |
| Delete the byte-identical duplicate export | `95591e7` |
| Kill the browsers to save memory | done at the time |

**One she deferred herself and no one should pick up:** the user interview about her
business and the Extropic application — *"It's just not the immediate task right
now."* The 10:07 decision-interview cron covers project decisions and is not that.
