import json, glob, os, csv, collections
BASE="/sessions/gifted-happy-euler/mnt/kylas-crm-mcp-server/presales_june_analysis"
rows=[]
for f in glob.glob(BASE+"/open_focus/*.json"):
    if not os.path.basename(f)[:-5].isdigit(): continue
    d=json.load(open(f))
    def num(x):
        try: return float(x)
        except: return None
    p=num(d.get("conv_prob"))
    if p is not None and p>1: p=p/100.0
    band=str(d.get("band","")).upper().strip()
    ch=str(d.get("churn_call","")).upper()
    if "REASSIGN" in ch: ch="REASSIGN-NEW-SALES"
    elif "PRESALES" in ch or "PRE-SALES" in ch: ch="BACK-TO-PRESALES"
    elif "DISQUAL" in ch: ch="DISQUALIFY"
    elif "KEEP" in ch: ch="KEEP"
    lic=d.get("noOfLicenses")
    try: lic=int(lic)
    except: lic=None
    rows.append({"deal_id":d.get("deal_id"),"name":d.get("name"),"owner":d.get("owner"),"stage":d.get("stage"),
      "licences":lic,"tier3":d.get("tier3"),"city":d.get("city_clean"),"city_class":d.get("city_class"),
      "dev_broker":d.get("dev_broker"),"onsite":d.get("onsite_or_online"),"bant_flag":d.get("bant_flag"),
      "verdict":str(d.get("rubric_verdict","")).upper(),"conv_prob":round(p,3) if p is not None else None,"band":band,
      "idle_days":d.get("idle_days"),"aging_days":d.get("aging_days"),
      "churn_call":ch,"churn_reason":d.get("churn_reason"),"next_action":d.get("next_action"),"one_line":d.get("one_line")})
# rank
bandrank={"HOT":0,"WARM":1,"MID":2,"COLD":3,"":4}
rows.sort(key=lambda r:(-(r["conv_prob"] or 0),))
json.dump(rows, open(BASE+"/open_pipeline_focus.json","w"), indent=1)
cols=list(rows[0].keys())
with open(BASE+"/open_pipeline_focus.csv","w",newline="") as fh:
    w=csv.DictWriter(fh,fieldnames=cols); w.writeheader()
    for r in rows: w.writerow(r)
N=len(rows)
band=collections.Counter(r["band"] for r in rows)
churn=collections.Counter(r["churn_call"] for r in rows)
print("N",N,"| band",dict(band),"| churn",dict(churn))
worknow=[r for r in rows if r["band"] in("HOT","WARM")]
print("\n=== WORK-NOW (HOT+WARM):",len(worknow),"deals ===")
for r in worknow:
    print(f"  {r['conv_prob']:.2f} {r['band']:4s} #{r['deal_id']} {r['name'][:22]:22s} {str(r['licences']):>3s}u {str(r['city'])[:12]:12s} {r['owner'][:16]:16s} [{r['churn_call']}] -> {str(r['next_action'])[:70]}")
def bucket(name,cc):
    sub=[r for r in rows if r["churn_call"]==cc]
    print(f"\n=== {name}: {len(sub)} ===")
    for r in sorted(sub,key=lambda x:-(x['conv_prob'] or 0))[:40]:
        print(f"  #{r['deal_id']} {r['name'][:24]:24s} {str(r['licences']):>3s}u {r['owner'][:15]:15s} idle{r['idle_days']} — {str(r['churn_reason'])[:80]}")
bucket("REASSIGN-NEW-SALES","REASSIGN-NEW-SALES")
bucket("BACK-TO-PRESALES","BACK-TO-PRESALES")
bucket("DISQUALIFY","DISQUALIFY")
# revenue-weighted: sum licences*1700 for keep+worknow
def val(r): return (r["licences"] or 0)*1700
print("\nPipeline INR (licences x1700):")
for cc in ["KEEP","REASSIGN-NEW-SALES","BACK-TO-PRESALES","DISQUALIFY"]:
    sub=[r for r in rows if r["churn_call"]==cc]; print(f"  {cc}: {len(sub)} deals, ~INR {sum(val(r) for r in sub):,}")
print("  WORK-NOW HOT+WARM: ~INR", f"{sum(val(r) for r in worknow):,}")
