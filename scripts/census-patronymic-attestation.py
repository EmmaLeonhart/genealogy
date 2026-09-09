"""How many fathers actually attest each `P144` *based on* source of each patronymic.

**`Q141336969` *Johansson* and `Q141290188` *Johansdotter* carried `P144` -> `Q58785388`
*Junna*, and neither is based on that name.** Those values were removed by hand, and it raised
the question of how a patronymic source is being defined at all. The answer: it has to be
genuinely attested in our own data.

**The counts already existed and were thrown away.** `build-patronymic-items.py` accumulates
`sources[token][father's given name] += 1` in a `Counter`, sorts the names by it, and then writes
only the names into `p144_names`. So the evidence for an attestation floor has been computed on
every run and discarded before anything could read it. This file writes it out.

**Why it matters, in one row.** `Johansson` has 4,512 attesting fathers: `Johan` 4,006 and
`Johannes` 436 -- and `Junna`, `Juhani`, `Jean`, `Joonas`, `John`, `Joen`, `Joan` and `Johannis`
one each. Every wrong source is a single father.

**The mechanism that let them in is `namemodel._skeleton`**, which deletes every vowel and folds
`j` -> `i`, so `johan johann john jean joen juhani junna jan jon joan` all reduce to `in` -- ten
distinct names, one skeleton. `_same_name` then calls them equal. Tightening the spelling rule is
not the answer: 45% of all `P144` values rest only on the skeleton, and most of those are right
(`Abrahamson` <- `Abram`, `Nilsdatter` <- `Nils`), which is what the skeleton exists for.

Writes `reports/patronymic-source-attestation.tsv`, sorted on the token and then on the count.
"""
import collections, csv, io, sys
sys.path.insert(0, "scripts")
import namemodel as nm

label, father = {}, {}
with io.open("reports/derived-labels.csv", encoding="utf-8", newline="") as fh:
    for r in csv.DictReader(fh):
        label[r["geni_id"]] = r.get("label_en") or r.get("label_mul") or ""
with io.open("reports/derived-family.csv", encoding="utf-8", newline="") as fh:
    for r in csv.DictReader(fh):
        f = (r.get("father") or "").strip()
        if f:
            father[r["geni_id"]] = f
print(f"{len(label):,} labels, {len(father):,} with a father", file=sys.stderr)

sources = collections.defaultdict(collections.Counter)
bearers = collections.Counter()
for g, lab in label.items():
    dad = label.get(father.get(g, ""), "")
    if not dad:
        continue
    dad_given = dad.split()[0]
    for tok in lab.split():
        if not nm.PATRONYMIC.match(tok):
            src = nm.latin_patronymic_source(tok, dad_given)
            if src:
                bearers[tok.casefold()] += 1
                sources[tok.casefold()][src] += 1
            continue
        if nm.patronymic_or_surname(tok, dad) != "patronymic":
            continue
        m = nm.PATRONYMIC_PARTS.match(tok)
        if not m:
            continue
        stem = m.group(1).casefold().rstrip("s")
        bearers[tok.casefold()] += 1
        for w in dad.split():
            if nm.PATRONYMIC.match(w):
                continue
            if nm._same_name(stem, w.casefold().rstrip("s")):
                sources[tok.casefold()][w] += 1
                break

with open("reports/patronymic-source-attestation.tsv", "w", encoding="utf-8", newline="") as out:
    w = csv.writer(out, delimiter="\t", lineterminator="\n")
    w.writerow(["token", "attesting_fathers", "source", "count", "share"])
    for tok in sorted(sources):
        tot = sum(sources[tok].values())
        for name, n in sorted(sources[tok].items(), key=lambda kv: (-kv[1], kv[0])):
            w.writerow([tok, bearers[tok], name, n, f"{n/tot:.4f}"])

# the shape of the decision
dist = collections.Counter()
for tok, srcs in sources.items():
    for name, n in srcs.items():
        dist[min(n, 10)] += 1
tot = sum(dist.values())
print(f"\n{tot:,} (token, source) pairs over {len(sources):,} tokens")
run = 0
for k in sorted(dist):
    run += dist[k]
    lab_k = f"{k}" if k < 10 else "10+"
    print(f"  attested by {lab_k:>3} father(s): {dist[k]:6,}   cumulative {run:6,} ({100*run/tot:5.1f}%)")
print("\njohansson / johansdotter / johannisson:")
for t in ("johansson", "johansdotter", "johannisson"):
    if t in sources:
        items = sorted(sources[t].items(), key=lambda kv: -kv[1])
        print(f"  {t} ({bearers[t]:,} attesting fathers): " +
              ", ".join(f"{n}={c}" for n, c in items))
