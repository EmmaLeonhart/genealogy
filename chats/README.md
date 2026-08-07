# chats/

Saved claude.ai conversations that decided something in this repo, kept the same
way `geni_pages/` keeps saved Geni profile pages: the browser's "save page"
output, `.html` plus its `_files` directory, committed whole.

A saved page is the record; the `.md` beside it is the **text extracted from
that page** for reading and grepping, since the HTML is a rendered app dump.
Where a conversation changed a design, the *decision* lives in `todo.md` /
`CLAUDE.md` — these files are the source it came from, not a second copy of it.

| file | what it settled |
| --- | --- |
| `Claude's inefficient wiki data querying - Claude.html` / `wikidata-querying-2026-08-07.md` | The Wikidata download: dump-first for the seed set, batched commits rather than per-item, an explicit state store, and the expectation that the expansion frontier is small. Folded into `todo.md` § 8a-revised. |
