import json, glob, os, csv, collections, statistics
BASE="/sessions/gifted-happy-euler/mnt/kylas-crm-mcp-server/presales_june_analysis"
rows=[]
for f in glob.glob(BASE+"/lost_deals/*.json"):
    if not os.path.basename(f)[:-5].isdigit(): continue
    d=json.load(open(f))
    def num(x):
        try:
            v=float(x); return v
        except: return None
    stage=str(d.get("stage") or "")
    stage="Unqualified" if "nqual" in stage.lower() else ("Lost" if "lost" in stage.lower() else stage)
    sa=num(d.get("sales_attempts")); sa=int(sa) if sa is not None else 0
    rows.append({"deal_id":d.get("deal_id"),"name":d.get("name"),"owner":d.get("owner"),"stage":stage,
      "licences":d.get("noOfLicenses"),"city":d.get("city"),
      "d_create_demo":num(d.get("days_created_to_demo")),"d_demo_lost":num(d.get("days_demo_to_lost")),
      "d_total":num(d.get("days_total")),"has_demo":bool(d.get("demo_date")),
      "attempts":sa,"loss_reason":str(d.get("loss_reason") or "Other"),"one_line":d.get("one_line")})
json.dump(rows,open(BASE+"/lost_dataset.json","w"),indent=1)
with open(BASE+"/lost_dataset.csv","w",newline="") as fh:
    w=csv.DictWriter(fh,fieldnames=list(rows[0].keys())); w.writeheader(); [w.writerow(r) for r in rows]
N=len(rows)
def stat(vals):
    vals=[v for v in vals if v is not None and v>=0]
    if not vals: return (None,None,len(vals))
    return (round(statistics.mean(vals),1), int(statistics.median(vals)), len(vals))
def block(sub,label):
    cd=stat([r["d_create_demo"] for r in sub])
    dl=stat([r["d_demo_lost"] for r in sub])
    tt=stat([r["d_total"] for r in sub])
    nodemo=sum(1 for r in sub if not r["has_demo"])
    at=[r["attempts"] for r in sub]
    print(f"\n== {label} (n={len(sub)}) ==")
    print(f"  created->demo:  avg {cd[0]}d  median {cd[1]}d   (n with demo {cd[2]}; no-demo {nodemo})")
    print(f"  demo->lost:     avg {dl[0]}d  median {dl[1]}d")
    print(f"  total cycle:    avg {tt[0]}d  median {tt[1]}d")
    print(f"  sales attempts: avg {round(statistics.mean(at),2)}  median {int(statistics.median(at))}  (0={sum(1 for a in at if a==0)}, 1-2={sum(1 for a in at if 1<=a<=2)}, 3-5={sum(1 for a in at if 3<=a<=5)}, 6-10={sum(1 for a in at if 6<=a<=10)}, 11+={sum(1 for a in at if a>10)})")
    print(f"  gave up in <=2 attempts: {sum(1 for a in at if a<=2)} ({sum(1 for a in at if a<=2)/len(sub)*100:.0f}%)")
allr=rows; lost=[r for r in rows if r["stage"]=="Lost"]; unq=[r for r in rows if r["stage"]=="Unqualified"]
block(allr,"ALL lost/unqualified"); block(lost,"CLOSED LOST"); block(unq,"CLOSED UNQUALIFIED")
print("\n== LOSS REASON distribution ==")
lr=collections.Counter(r["loss_reason"] for r in rows)
for k,v in lr.most_common(): print(f"  {k:26s} {v:3d} ({v/N*100:4.0f}%)")
print("\n== avg sales attempts BY loss reason (did sales chase or give up?) ==")
for k,_ in lr.most_common():
    sub=[r for r in rows if r["loss_reason"]==k]; at=[r["attempts"] for r in sub]
    dl=stat([r["d_demo_lost"] for r in sub])
    print(f"  {k:26s} n={len(sub):3d}  avg attempts {round(statistics.mean(at),1):4}  demo->lost median {dl[1]}d")
print("\n== attempts distribution overall ==")
at=[r["attempts"] for r in rows]
print(f"  0 attempts: {sum(1 for a in at if a==0)} ({sum(1 for a in at if a==0)/N*100:.0f}%)")
print(f"  1-2: {sum(1 for a in at if 1<=a<=2)}  3-5: {sum(1 for a in at if 3<=a<=5)}  6-10: {sum(1 for a in at if 6<=a<=10)}  11+: {sum(1 for a in at if a>10)}")
print(f"  overall avg {round(statistics.mean(at),2)} median {int(statistics.median(at))} max {max(at)}")
# save analytics
A={"N":N,"lost":len(lost),"unq":len(unq),
   "loss_reason":dict(lr),
   "timing":{"all":{"cd":stat([r['d_create_demo'] for r in rows]),"dl":stat([r['d_demo_lost'] for r in rows]),"tt":stat([r['d_total'] for r in rows])},
             "lost":{"cd":stat([r['d_create_demo'] for r in lost]),"dl":stat([r['d_demo_lost'] for r in lost]),"tt":stat([r['d_total'] for r in lost])},
             "unq":{"cd":stat([r['d_create_demo'] for r in unq]),"dl":stat([r['d_demo_lost'] for r in unq]),"tt":stat([r['d_total'] for r in unq])}},
   "no_demo":sum(1 for r in rows if not r['has_demo']),
   "attempts_avg":round(statistics.mean(at),2),"attempts_median":int(statistics.median(at)),
   "attempts_dist":{"0":sum(1 for a in at if a==0),"1-2":sum(1 for a in at if 1<=a<=2),"3-5":sum(1 for a in at if 3<=a<=5),"6-10":sum(1 for a in at if 6<=a<=10),"11+":sum(1 for a in at if a>10)},
   "attempts_by_reason":{k:round(statistics.mean([r['attempts'] for r in rows if r['loss_reason']==k]),1) for k in lr},
   "reason_by_stage":{s:dict(collections.Counter(r['loss_reason'] for r in rows if r['stage']==s)) for s in ['Lost','Unqualified']},
}
json.dump(A,open(BASE+"/lost_analytics.json","w"),indent=1)
print("\nsaved lost_dataset.csv + lost_analytics.json")
