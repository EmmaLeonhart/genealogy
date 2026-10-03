# What this project is for

_Maintained by Claude: a running read of what the user is trying to do. It is
analysis, not a transcript, and it changes as understanding improves._

Work mode started: 2026-10-02 19:30 PST (from `date`), because the user said to
start.

## Current understanding

A research project on the **Inbe clan (忌部氏 / 斎部氏, also romanised Imbe)**
of ancient Japan: their genealogy, origins, regional branches and how they
spread. The concrete deliverable is a **GEDCOM genealogy** that traces as many
named Inbe people as possible back toward the clan's divine ancestors
(Futodama no Mikoto and the branch-ancestor deities), with every person and
link tied to a source.

## What supports it

- The user, in chat (2026-10-02, dictated): "I'm trying to do a research
  project on this clan, their genealogy, their origins, um, how they are spread
  about, basically everything"; "they're the one that feels like they're kind
  of the least real"; "I want you to help me learn about them. Learn about them
  and the different ones."
- "ideally, I want to, like, draw out a genealogy of them, like a GEDCOM
  genealogy of them."
- Folder name `INBE`, chosen by the user (`auto_named: false`).
- The user never named the clan in chat; Inbe is inferred from the folder name.
  I said so in chat and the user did not correct it.

## Constraints and decisions from the user

- The user thinks the full genealogy is probably not achievable but wants it
  attempted anyway: "I don't think like a genealogy file is actually doable.
  Um, I'm just telling you to do it anyways."
- The goal is to "trace the, the ancestry of all these different people ...
  ideally with like the, say Wikidata or something like that, Wikidata or
  family search to the gods." The user's guess: "I feel like family search is
  probably going to be best for getting to the gods, but I'm not really sure."
  So: evaluate both Wikidata and FamilySearch as routes to the gods, and report
  which works better.

- The user knows the branches are not all meant to be blood relatives and
  finds that confusing: "not all of them are supposed to be blood relatives.
  Um, it's just it's very confusing to me."
- Origin theories are wanted: "I'm interested in potential theories of their
  origins and stuff."
- Compare with the **Nakatomi**: "the Nakatomi clan have a much more like
  actually defined genealogy, which makes me a bit unsure about this, this
  clan." (One word in that message, "Kisu", was garbled by dictation; meaning
  unknown, not guessed.)
- Name: the user calls the Inbe "the hemp clan" in chat, because speech-to-text
  never gets "Imbe" right. "Hemp clan" in a message means the Inbe.

- **The core question, clarified 2026-10-02:** is there any documented
  generation-by-generation chain from a real Inbe person up to the Inbe's own
  divine ancestry (Futodama etc.)? "I'm only caring about ... this one specific
  clan and their specific divine ancestry. ... any generation by generation
  account, is fine. ... But I'm actually looking for one." Her current belief:
  "I'm pretty convinced that this clan does not have any such documented
  ancestry ... doesn't really have that many documented people in it either.
  But I'm trying to figure this stuff out."
- Answer what is asked, directly. Asked whether Wikidata takes the Oda to the
  gods, she did not want a detour into Nobunaga ("I didn't ask you about
  Nobunaga"). Paths to the gods through other clans (Taira, imperial line) are
  not what she is looking for: "If it doesn't, well then it's not what we're
  asking."

- **GEDCOM output (2026-10-02):** the user asked for a GEDCOM of the Ono
  pedigree, committed, pushed and opened in the default program (MyHeritage
  on this machine). Then: "English names should be the primary thing on
  there, and then the Japanese names would be put in the note ... make an
  English language version too that you open up. Just because I'm not really
  understanding it very well." Default from now on: genealogy outputs get an
  English-first version, with the Japanese in notes, and that is the one opened.

- Dates in GEDCOMs: plain years, no "EST" qualifier ("Your EST is just kinda
  ruining everything remove it", 2026-10-02).
- The user edits the GEDCOMs in MyHeritage and saves them at the top level,
  adding Wikidata links (and created Q141627252 for Tahiko no Sukune). Handle each
  one the same way: commit as landed, push, `git mv` into `genealogy/`, and fold
  any new QIDs into `make_ono_gedcom.py`.

- **End goal stated 2026-10-03:** "My end interest is potentially importing
  this tree onto Wikidata, although I'm not really sure how to ... present it
  properly with its records and such." So outputs should move toward a
  Wikidata-ready form: a roster of people with QIDs and Japanese/English
  names, and a plan for modelling a forged/legendary pedigree on Wikidata with
  references.
- Asked for a roster of "all the Wikidata items that are present for these plus
  their Japanese name and their English name ... alongside any notes".

- **Wikidata pipeline design (user, 2026-10-03):** batch 1 creates the source
  item; batch 2 creates the people unlinked, "described by" the source, with
  name, gender and estimated lifetime; batch 3 adds cited connections using the
  source with page and URL. SPARQL between batches finds the created items. "The
  source needs to exist before the people do ... Any other claims on them are
  going to be cited to that except for the dates, which are just estimations.
  So they are ... going to be deprecated estimations."

- Labels for new people (2026-10-03): "they get the name in Japanese and
  Chinese in the characters ... their English label, their multi-language
  label, their French label, and their Indonesian label and their Spanish label
  all are the same text that we usually would treat as being the English ...
  I'm not going to make a claim about what the Korean label is going to be."

- **QuickStatements tool (2026-10-03, after an angry correction):** use the
  standard tool at https://quickstatements.toolforge.org/#/batch, NOT
  QuickStatements 3.0 / qs-dev (which I had wrongly sent her to and whose OAuth
  page upset her). Pipes with **no spaces**. Standard QS cannot set rank, so
  the estimated dates are a separate step to be deprecated.
- The user made the source item herself: **Q141627872** ("Genealogical
  Record of the Inbe no Sukune clan", 斎部宿禰本系帳). Batch 1 is done.
- Batch 2 (people) submitted by me at her request as QuickStatements batch
  #289566, "Run in background", 2026-10-03; she confirmed it completed.
- Batch 3 (98 family links) submitted at her request as batch #289567.
  QIDs for all 49 people: `genealogy/wikidata/ono_qids.json`. Batch 4 (64
  estimated dates, to be deprecated) is generated but not run: standard QS
  cannot set the deprecated rank.

- **Real people are connected (user, 2026-10-03):** "I many times expressed
  the fact that no, we're not doing this. We are doing the form that actually
  connects them." Kobito and Shikobuchi get their pedigree parents like
  everyone else (disputed + cited); done as batch #289568. Do not hold back
  user-requested links on my own accuracy grounds; say a concern once, then do
  what she decided.

## Assumptions (mine)

- Unattested parent–child links are not invented. Where a source gives no
  link, the person goes into the GEDCOM unconnected, with a note. Links from
  user-contributed trees (FamilySearch, some Wikidata statements) are kept but
  marked low-confidence and traced to whatever they cite.
- Mythological genealogy (gods) is included as a clearly labelled layer,
  sourced to the Kojiki, Nihon Shoki, Kogo Shūi and Shinsen Shōjiroku.

- FamilySearch access (2026-10-02): "Yes, I do have a family search account,
  and you have the ability to ... use the browser extension to go on family
  search. Um, you also have permission to sign into family search automatically
  using my Google account in the event that you need to do that." Use Claude in
  Chrome for FamilySearch; signing in with her Google account is authorised.
- The user asked whether the Oda clan is an Inbe ("hemp clan") branch. Answered:
  mainstream view yes (Tsurugi Shrine priests of Oda, Echizen; Inbe no
  Chikazane), with the Taira descent as a later claim. Verify in the branches
  note.

## Open questions

- None blocking.

## Confidence

High that the subject is the Inbe clan and the deliverable is a sourced GEDCOM
plus research notes. Medium on how far the genealogy can honestly be connected.
