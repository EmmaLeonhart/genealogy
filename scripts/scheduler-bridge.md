# Driving the scheduler without the toolbar

`background.js` has always answered `status`, `start`, `stop` and `load` over
`chrome.runtime.sendMessage` — but only from an extension context, and the only one that existed
was the toolbar popup. The toolbar is browser chrome and `chrome-extension://` URLs are refused
the same way `chrome://` ones are, so *"start it from the toolbar"* was a manual step on Emma
every single run. That is why the scheduler had never run once.

`content/router.js` now relays those messages from a data attribute, the same channel the job
trigger uses:

```js
const ask = async (m) => {
  const root = document.documentElement;
  root.dataset.geniCollectorScheduler = JSON.stringify(m);
  delete root.dataset.geniCollectorSchedulerResult;
  document.dispatchEvent(new Event("geni-collector-scheduler"));
  for (let i = 0; i < 25; i++) {
    await new Promise(x => setTimeout(x, 400));
    if (root.dataset.geniCollectorSchedulerResult)
      return JSON.parse(root.dataset.geniCollectorSchedulerResult);
  }
  return { timeout: true };
};

await ask({ type: "status" });                     // running, queue, results, endId
await ask({ type: "load", queue: [ /* jobs */ ] }); // replaces the queue
await ask({ type: "start" });                       // begins opening tabs
await ask({ type: "stop" });                        // stops opening NEW tabs only
```

Run it on any `geni.com` profile page — the content scripts only load there.

**It relays and does not interpret.** Exports one at a time because that is Geni's limit, tabs
held open while a search runs, the seed queue dropped once an ancestor is added: all of that stays
in `background.js`. A bridge that made decisions would be a second scheduler.

## ⛔ `stop` does not cancel a submitted export

Geni has no cancel. `stop` prevents new tabs opening and nothing more — Emma, on being offered a
kill: *"you think you can kill a geni export read the fucking docs you can't."*

## ⛔ A STORED SETTING SHADOWS ITS DEFAULT, PERMANENTLY

`state()` is `Object.assign({}, DEFAULTS, stored)`, so anything the popup ever wrote wins forever.
Measured 2026-09-06: `concurrency` reads **6** while `DEFAULTS` says **12** — her *"update it to
batches double the older size on all things"* moved the default and the stored value shadowed it.
**Changing a `DEFAULTS` number does not change a running profile.** Send `load`/`start` with the
value you mean, or clear the key.
