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
