/* The control panel. It does no work itself -- everything runs in the background so closing
 * this popup does not stop a run. */

const $ = (id) => document.getElementById(id);
const send = (m) => chrome.runtime.sendMessage(m);

function parseQueue(text) {
  const out = [];
  for (const raw of text.split("\n")) {
    const line = raw.trim();
    if (!line || line.startsWith("#")) continue;
    const m = line.match(/^(export|path)?\s*([0-9]+)(?:\s+(blood|inlaw))?(?:\s+(.*))?$/i);
    if (!m) continue;
    out.push({
      job: (m[1] || "path").toLowerCase(),
      geni_id: m[2],
      kind: (m[3] || "blood").toLowerCase(),
      label: (m[4] || "").trim()
    });
  }
  return out;
}

async function refresh() {
  const s = await send({ type: "status" });
  if (!s) return;
  const byState = {};
  for (const r of s.results) byState[r.state] = (byState[r.state] || 0) + 1;
  $("stat").textContent =
    (s.running ? "RUNNING" : "stopped") +
    "   queued " + (s.queue || []).length +
    "   in flight " + Object.keys(s.active || {}).length +
    "   done " + (s.results || []).length + "\n" +
    Object.entries(byState).sort().map(([k, v]) => "  " + k + "  " + v).join("\n");
}

$("load").onclick = async () => {
  const q = parseQueue($("q").value);
  await send({ type: "load", queue: q });
  await chrome.storage.local.set({
    concurrency: Math.max(1, +$("conc").value || 6),
    staggerMs: Math.max(2, +$("stag").value || 60) * 1000,
    waitMs: Math.max(1, +$("wait").value || 10) * 60000
  });
  refresh();
};
$("start").onclick = async () => { await send({ type: "start" }); refresh(); };
$("stop").onclick = async () => { await send({ type: "stop" }); refresh(); };

/* Results leave as a TSV download, filed by `scripts/file-geni-downloads.py` alongside the
 * captures. The popup has a DOM, so the same Blob click the captures use works here. */
$("save").onclick = async () => {
  const s = await send({ type: "status" });
  const cols = ["at", "job", "geni_id", "kind", "state", "steps", "hasTarget", "requested",
                "first", "last", "saved", "family_tree", "blood_relatives", "ancestors",
                "descendants", "followers", "description", "url", "error"];
  const rows = [cols.join("\t")];
  for (const r of s.results || []) {
    const st = r.stats || {};
    rows.push(cols.map((c) => {
      const v = (c in st) ? st[c] : r[c];
      return v === undefined || v === null ? "" : String(v).replace(/[\t\r\n]+/g, " ");
    }).join("\t"));
  }
  const b = new Blob([rows.join("\n") + "\n"], { type: "text/tab-separated-values" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(b);
  a.download = "geni-collector-results.tsv";
  a.click();
};

refresh();
setInterval(refresh, 2000);
