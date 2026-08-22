import gzip, json, sys, glob, re
S="/tmp/claude-0/-home-user-geni/b1e7695e-6333-58b4-a736-5cdeb71809a8/scratchpad"
t=json.load(open(S+"/wd-targets.json"))
want=set(t["want"])
ID=re.compile(r'"id"\s*:\s*"(Q\d+)"')
out={}
files=sorted(glob.glob("wikidata/items/*.jsonl.gz"))
for n,f in enumerate(files,1):
    try:
        with gzip.open(f,"rt",encoding="utf-8") as fh:
            for line in fh:
                m=ID.search(line, 0, 200)
                if not m or m.group(1) not in want: continue
                d=json.loads(line)
                qid=d.get("id")
                if qid not in want: continue
                labels=d.get("labels",{})
                lab=(labels.get("en") or labels.get("mul") or next(iter(labels.values()),{}) or {}).get("value","")
                desc=(d.get("descriptions",{}).get("en") or {}).get("value","")
                out[qid]={"label":lab,"desc":desc}
    except Exception as e:
        print("ERR",f,e,file=sys.stderr)
    if n%200==0:
        print(f"{n}/{len(files)} found {len(out)}/{len(want)}",file=sys.stderr, flush=True)
    if len(out)==len(want): break
json.dump(out, open(S+"/wd-labels.json","w"))
print("done", len(out), file=sys.stderr)
