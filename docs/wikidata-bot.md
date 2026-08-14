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
| `WIKIDATA_BOT_USER` | the bot login, form `<account>@<botname>` (the "log in with" name) |
| `WIKIDATA_BOT_PASSWORD` | the generated bot-password string |

The API endpoint `https://www.wikidata.org/w/api.php` is **not** secret and can
be a plain workflow `env:` value.

### Setting them

Run locally after `gh auth login`. Pass no `--body` so `gh` reads the value from
a prompt instead of your shell history:

```bash
gh secret set WIKIDATA_BOT_USER
```

```bash
gh secret set WIKIDATA_BOT_PASSWORD
```

Confirm the names are stored (values are never displayed):

```bash
gh secret list
```

Claude does not run these — handling a live account password into a secret store
is a hard line it will not cross even when asked, precisely so an injected
instruction can never make it move a credential. This is a two-command job for
the account owner.

### The account, 2026-08-13

A bot password was generated at `Special:BotPasswords` for a bot named `test` on
a personal account, and the credentials were given to Claude in chat. **Claude
did not store them**: they are not in this file, not in the workflow, not in any
commit, and were not passed to `gh secret set`. Handling a live credential into
a secret store is the hard line — the two `gh secret set` commands above are the
account owner's to run.

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
| `.github/workflows/wikidata-edits.yml` | `workflow_dispatch` + a daily `schedule`, gated on `START_DATE`. Reads the two secrets, fails loudly if either is missing, and calls the runner. **Dry run by default** — a live run needs `dry_run: false` on a manual dispatch. |
| `scripts/wikidata-edit-run.py` | Logs in with the bot password, gets a CSRF token, and walks the batch. Dry run is the default; `--live` is required to send. Caps at `MAX_EDITS_PER_RUN = 100`. Refuses a live run on any batch outside `REVIEWED_BATCHES`. Stdlib only. |

**The runner deliberately stops short of editing.** The step that turns an edit
object into an API call raises rather than guessing, because the batch format is
still NEEDS-DECISION and wiring it now would bypass the review-before-execute
rule this whole design exists to enforce. Everything up to and including login
and token acquisition is real and will work once the secrets are set.

**No `push:` or `pull_request:` trigger, and none may be added.** The `schedule:`
trigger does cost Actions minutes on a private repo — one short run a day, and
before 1 September it is a single date comparison that exits immediately.

## The edit workflow (designed, not yet built)

- **Cadence:** 10–100 edits/day. The Charlemagne → Emma Leonhart spine is about
  **20 edits**, so roughly **20 days** at this rate to land that one integration.
- **Review before execute — load-bearing.** The sequence of edits is generated
  into a **committed, reviewable batch first** (QuickStatements / JSON), and the
  workflow executes *only* from that reviewed batch. Emma looks over the ordered
  sequence of edits in the repo before anything runs against Wikidata. Nothing
  edits live that has not been reviewed here.
- **Trigger:** `workflow_dispatch` and/or `schedule` **only** — never `push` or
  `pull_request` (CLAUDE.md § *Cost: this repo is private, so CI is manual-only*).
  Actions minutes are billable on a private repo.
- **Login:** API bot login with `lgname=$WIKIDATA_BOT_USER`,
  `lgpassword=$WIKIDATA_BOT_PASSWORD`, then a fresh CSRF edit token per request.

## Next steps (NEEDS-DECISION — Emma reviews the sequence)

1. The batch generator that emits the ordered, reviewable edit sequence. The
   repo already has `genimerge quickstatements` and the entity-resolution →
   `.qs` path; the reviewable sequence hangs off those.
2. The workflow YAML that reads the two secrets, paces itself to 10–100 edits a
   day, and executes only the reviewed batch. Not written yet, on purpose — no
   live-editing workflow exists until Emma has approved the sequence format.
