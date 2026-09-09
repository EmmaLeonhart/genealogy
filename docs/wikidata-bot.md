# Wikidata bot: credentials and the edit workflow

The project exists to **add** genealogy to Wikidata (CLAUDE.md § *The purpose is
to ADD to Wikidata, not to correct it*). Those edits go through a Wikidata
**bot-password** account over the API, run by GitHub Actions. The credentials
live only in GitHub Actions **secrets** — they are never written into this repo,
not in a file, not in a workflow, not in a commit.

## Secrets

Set these in the repo's GitHub Actions secrets. Every value comes from the
account's `Special:BotPasswords` page; do not paste a value into any tracked
file. Per Emma's instruction the login name is a secret too, not just the
password.

| Secret name | Holds |
| --- | --- |
| `USERNAME` | the Wikidata account name |
| `BOT_NAME` | the bot's name from `Special:BotPasswords` |
| `BOT_PASSWORD` | the generated bot-password string |

**These are the three names Emma set on 2026-08-14** (screenshotted from the
repo's Actions secrets page), and the workflow and runner were changed to match
them — they previously read `WIKIDATA_BOT_USER` / `WIKIDATA_BOT_PASSWORD`, names
nothing had ever been stored under.

The API's `lgname` is the **joined** form `<account>@<botname>`, so
`scripts/wikidata-edit-run.py` builds it as `f"{USERNAME}@{BOT_NAME}"`. If
`USERNAME` already contains an `@` it is used as-is, so storing the joined login
in `USERNAME` also works.

The API endpoint `https://www.wikidata.org/w/api.php` is **not** secret and can
be a plain workflow `env:` value.

### Setting them

Run locally after `gh auth login`. Pass no `--body` so `gh` reads the value from
a prompt instead of your shell history:

```bash
gh secret set USERNAME
```

```bash
gh secret set BOT_NAME
```

```bash
gh secret set BOT_PASSWORD
```

Confirm the names are stored (values are never displayed):

```bash
gh secret list
```

Claude does not run these — handling a live account password into a secret store
is a hard line it will not cross even when asked, precisely so an injected
instruction can never make it move a credential. This is a three-command job for
the account owner, and Emma did it on 2026-08-14.

### The account, 2026-08-13

A bot password was generated at `Special:BotPasswords` for a bot named `test` on
a personal account, and the credentials were given to Claude in chat. **Claude
did not store them**: they are not in this file, not in the workflow, not in any
commit, and were not passed to `gh secret set`. Handling a live credential into
a secret store is the hard line — the `gh secret set` commands above are the
account owner's to run, and she ran them (or set them through the web UI) on
2026-08-14.

**Treat that password as burned and regenerate it.** It was pasted into a chat
transcript, which is a place credentials should not live. Revoke the `test` bot
password at `Special:BotPasswords`, generate a fresh one, and put *that* into
`WIKIDATA_BOT_PASSWORD`. Nothing downstream cares which password it is.

**Also: `test` is a poor bot name.** Wikidata bot policy and the edit filters
read the bot name; something like `genimerge` describes what the edits are and
makes them defensible on a talk page. Worth changing at the same time as the
regeneration, since both mean creating a new bot password anyway.

## Start date: 1 September 2026

Emma's instruction, 2026-08-13 — the actions start properly on **1 September
2026**. `.github/workflows/wikidata-edits.yml` enforces it: the first step
compares today's date against `START_DATE` and every later step is skipped
before it. Nothing else needs changing on the day; the gate opens itself.

## What is built

| file | what it does |
| --- | --- |
| `.github/workflows/wikidata-edits.yml` | `workflow_dispatch` + a daily `schedule`, gated on `START_DATE`. Reads the three secrets, fails loudly if any is missing, and calls the runner. **Dry run by default** — a live run needs `dry_run: false` on a manual dispatch. |
| `scripts/wikidata-edit-run.py` | Logs in with the bot password, gets a CSRF token, and walks the batch. Dry run is the default; `--live` is required to send. Caps at `MAX_EDITS_PER_RUN = 100`. Refuses a live run on any batch outside `REVIEWED_BATCHES`. Stdlib only. |

**The runner sends edits now.** It stopped short of it until 2026-09-05, raising
rather than guessing at the batch format; Emma settled the format question by
choosing what runs — the daily Garborg batch, through this bot-password path —
so `entity_data()` is the mapping and `Session.apply()` is the one place that
turns an edit object into a `wbeditentity` call.

**One call per edit object, and the object is the unit of atomicity.** A `CREATE`
carries its labels, aliases, descriptions and claims in a single request, so
there is no moment where the item exists unlabelled. `LAST` resolves through the
object's own `requires` and the QIDs this run minted — never by position, which
`genimerge.editorder` is entitled to shuffle.

**No `summary`.** `CLAUDE.md` § *NO descriptions and NO edit summaries* covers
the API path in as many words. The absence is deliberate.

**No `push:` or `pull_request:` trigger, and none may be added.** The old reason
was billing on a private repo; the repo went public on 2026-09-01, so the reason
is now that a workflow which sends edits is the last one that should fire on
every push.

## The edit workflow (designed, not yet built)

- **Cadence:** 10–100 edits/day. The Charlemagne → Empress Jingū spine is about
  **20 edits**, so roughly **20 days** at this rate to land that one integration.
- **Review before execute — load-bearing.** The sequence of edits is generated
  into a **committed, reviewable batch first** (QuickStatements / JSON), and the
  workflow executes *only* from that reviewed batch. Emma looks over the ordered
  sequence of edits in the repo before anything runs against Wikidata. Nothing
  edits live that has not been reviewed here.
- **Trigger:** `workflow_dispatch` and/or `schedule` **only** — never `push` or
  `pull_request`.
- **Login:** API bot login with `lgname=$USERNAME@$BOT_NAME`,
  `lgpassword=$BOT_PASSWORD`, then a fresh CSRF edit token per request.

## The two dates, and why there are two

| | date | gates |
| --- | --- | --- |
| `START_DATE` | **2026-09-01** | whether this repo may edit Wikidata **at all**. A hand-dispatched live run has been allowed since. |
| `AUTOMATION_START_DATE` | **2026-09-15** | whether the **schedule** sends anything. Before it, the scheduled run is a dry run. |

Emma, 2026-09-05: *"I want to on the 15th start all of this stuff
automatically"* — and, asked what starts and how, the daily Garborg batch
through the bot-password API.

They are two dates rather than one move because they gate different things and
both stay true. Collapsing them would either back-date the automation or re-lock
the manual path. Each is written twice — module and workflow, because the
workflow compares dates in bash before the module could be imported — and
`tests/test_wikidata_start_date.py` fails if either pair drifts.

**The schedule runs before the 15th anyway, as a dry run.** A gate that has never
been exercised is a gate nobody knows the state of; running it daily means a
break in the wiring shows up on an ordinary morning rather than on the day.

## The receipt is what makes a re-send safe

`reports/wikidata-edits-applied.tsv` — one row per applied edit,
`date, edit_id, kind, qid` — written as each edit lands and committed after the
run.

Re-sending is the normal case, not an accident: the daily file is regenerated
four times a day and the schedule reads whatever is committed, so the same
`CREATE` appears in two runs whenever the ledger refresh has not caught up with
what was made. Without the receipt the second run mints the person again.

Edit ids are a **hash of what the edit says**, not the line it sits on, so an id
survives the batch being regenerated with the lines in a different place. The
receipt keeps the QID as well as the id, because a create that is skipped still
has to answer the `LAST` pointing at it.
