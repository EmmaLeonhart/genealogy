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

## Not done · long-range relatives are missing from the batch that needs them most

**Emma, 2026-08-16:** *"I'm pretty sure that long-range relationships have much
larger things to contribute than you consider them to do so… It can work off of
those long-range things… grandparents or grandchildren or siblings."*

That was applied to `scripts/build-nn-label-batch.py` — 1,588 Wikidata items — which
now searches parent → spouse → child → **sibling → grandparent → grandchild**.

It was **not** applied to `scripts/build-placeholder-label-batch.py`, which is
twenty-two times larger and stops at child:

| relative found | edits |
| --- | ---: |
| father | 12,254 |
| spouse | 5,052 |
| mother | 1,882 |
| child | 836 |
| **none — `mul: NN` and no readable label** | **14,987** |
| total | 35,011 |

**43% of the largest label batch in the repo describes nobody.** Each of those
14,987 people has a parent, spouse and child who are all themselves unnamed — which
is precisely the population a sibling, grandparent or grandchild can reach and the
reason she raised long-range relatives at all. Her seven-language item is gated on
these labels, so the gap is upstream of the gate.

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
