# Meta queue

**Dictated 2026-09-20.** It exists because PR #254 rewrites `queue.md` itself, so the ordinary
queue cannot hold a plan whose first item is *merge the thing that rewrites the queue*. This file
is folded into `queue.md` once the merges have settled — that is its ending, not an afterthought.

Same rules as `queue.md`: bullets, never numbers; an item is DELETED when done, never annotated.

---

## The order. Top to bottom.

- **Merge PR #254 `misc/file-size-guard` into `main`.** *"there is a pull request going on right
  now that merges one branch into the main ... It essentially cleared up, cleared off every single
  queue item, or at least it should have."* Title: *a size guard, the name-item shard, and 47,692
  path permalinks out of email*. Expect `queue.md` to be rewritten by it.

- **Then merge `exports/2026-09-19`** — the descendants branch, and the most advanced one.
  *"a new kind of descendant scanning thing, particularly looking at the Baltic Germans, and the
  potential descent and my potential Rurikid descent through this one specific guy who has a
  descent from antiquity, and of which I consider to be my best for this thing."*

- **⛔ PUT A LINK ON THE GITHUB PAGES SITE TO THE ACTION THAT REDOES EVERYTHING.** One workflow,
  one link, running the whole chain: *"synoptic tree rebuilding, checking, refreshing the ledger,
  building the quick statements, and running them on Wikidata."*

- **⛔ THEN THE DESCRIPTION UNIQUENESS REVIEW, AND IT IS A MEASUREMENT BEFORE IT IS A CHANGE.**
  Mass-generate the description that WOULD be written for every individual we would make, into a
  **committed CSV kept current by CI/CD**, then read it for how unique they are.
  *"the descriptions need to be unique."*
  - unique -> continue, nothing to decide.
  - **not unique -> `AskUserQuestion`**, on the specific collisions rather than in general.
  - Why it matters, and it is not academic: Wikibase refuses a creation only when the label AND
    a non-empty description both match, so a description that repeats is a guard that does not
    guard. § *A blank description is not a guard, it is the absence of one.*

- **Then merge `exports/2026-09-19` again**, to pick up what it has gathered since.

- **⛔ AND FROM THIS POINT ON, MERGE THAT BRANCH EVERY HOUR ON THE HOUR.** Set up before the
  research starts, not after: *"at the end of this meta queue, like before the research starts,
  you're going to have a thing that every hour on the hour merges in the content from that
  descendants report based branch."*

- **THEN THE RESEARCH: is there a lead into her ancestry among these descendants?**
  - The material is the descendants roster being built on that branch — *"we're kind of
    developing a very large roster of his descendants"* — plus the general 6N descendants.
  - The other side is **her own ~8,000 ancestors**. If they are not already to hand, the
    **ancestors report function** produces them: *"which is very similar and works the exact same
    way, except for ancestors of a person."* Pick the form that matches most easily; that choice
    is the point of using the report rather than something else.
  - **⛔ FUZZY STRING MATCHING IS RIGHT HERE, AND IT USUALLY IS NOT.** Stated explicitly:
    *"this is one of the few situations in which fuzzy string matching might actually be good."*
    Looking for common given names, common surnames, **and common managing individuals**.
  - **⛔ THE MANAGING INDIVIDUAL IS A LEAD AND IT WAS THROWN AWAY.** The original 6N descendants
    batch omitted it because *"Claude decided to use its own discretion to omit the managing
    individual, which is not a thing you're supposed to do."* It is signal, not metadata: two
    people managed by one account is a connection. Anything regathered carries it.

- **Fold this file into `queue.md` and delete it.**

---

## Standing, while the above runs

- **The path requester runs, and a drained batch is not a finished campaign.** Measured
  2026-09-20: **70,044 of 251,607 really attempted, 140,692 never** — about 18 more batches of
  8,000, ~141 hours at 1,000/hour. The 40,871 parked CBDB rows are deliberate.
  ⛔ It drained at 21:03:42Z and sat dead **2.6 hours** before anyone noticed, and it was Emma
  who noticed, not the six-hour check. At six hours a drain can cost most of a batch.

- **The pipeline loop runs**: compose -> pull -> send both halves -> repeat, and it never pushes,
  because a push cancels the PENDING pipeline run and that is what froze the batch all night.

- **⛔ NOT A DUPLICATE PAIR.** `Q141502962` and `Q141498725` were called a duplicate here and are
  not one. Ruled 2026-09-20: *"that duplicate pair is not a duplicate pair. It seems to me that
  you kind of assume I'm not changing things when I am changing things. To my knowledge, there's
  no duplicate pairs anymore."* **The judgment that those become entry points stands** and is
  done. The error was reading a cached ledger as the live state.
