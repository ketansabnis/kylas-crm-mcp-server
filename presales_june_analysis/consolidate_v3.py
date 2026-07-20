import json, glob, os, csv, collections, datetime
BASE="/sessions/gifted-happy-euler/mnt/kylas-crm-mcp-server/presales_june_analysis"

def tier3(lic):
    if lic is None: return "unknown"
    if lic<5: return "<5"
    if lic<=10: return "5-10"
    return "10+"
def parsedt(s):
    if not s: return None
    try: return datetime.datetime.fromisoformat(s.replace("Z","+00:00"))
    except: return None
def m6(cc):
    cc=(cc or "").lower()
    if "pune" in cc or "pimpri" in cc: return "Pune"
    if any(x in cc for x in ["mumbai","thane","navi","borivali","chembur","andheri","kalyan"]): return "Mumbai/Thane"
    if any(x in cc for x in ["delhi","noida","gurgaon","gurugram","ghaziabad","faridabad","ncr"]): return "Delhi/NCR"
    if "bangal" in cc or "bengal" in cc: return "Bangalore"
    if "chennai" in cc: return "Chennai"
    if "hyderab" in cc or "secunderab" in cc: return "Hyderabad"
    return "Other"

# ---------- DEMOS: re-tier + attach source stats ----------
rows=json.load(open(BASE+"/master_dataset.json"))
for r in rows: r["tier3"]=tier3(r["noOfLicenses"])
json.dump(rows, open(BASE+"/master_dataset.json","w"), indent=1)

# ---------- CLOSURES (real June revenue) ----------
cf=[f for f in glob.glob(BASE+"/closures/*.json") if os.path.basename(f)[:-5].isdigit()]
seed_creator={}  # attribute creator via v2 seed if present else blank
try:
    for s in json.load(open(BASE+"/deal_ids_v2.json")): seed_creator[s["deal_id"]]=s["creator"]
except: pass
clo=[]
JUN30=datetime.datetime(2026,6,30,23,59,59,tzinfo=datetime.timezone(datetime.timedelta(hours=5,minutes=30)))
for f in cf:
    d=json.load(open(f))
    lic=d.get("noOfLicenses")
    try: lic=int(lic)
    except: lic=None
    dev=d.get("cfReDeveloperOrChannelPartner")
    if isinstance(dev,dict): dev=dev.get("name")
    billed=d.get("cfBilledAmount") or 0
    try: billed=int(billed)
    except: billed=0
    recv=d.get("cfActualPaymentReceived") or 0
    try: recv=int(recv)
    except: recv=0
    demo=parsedt(d.get("cfMeetingConductedOn"))
    upd=parsedt(d.get("updated_at"))
    # closure date proxy: updated_at, clamped to <= Jun30 (all closed in June per filter)
    close_est=upd
    if close_est is None or close_est>JUN30: close_est=JUN30
    days=None
    if demo and close_est:
        days=(close_est-demo).days
        if days<0: days=0
    clo.append({"deal_id":d.get("deal_id"),"name":d.get("deal_name"),"owner":d.get("owner"),
      "creator":seed_creator.get(d.get("deal_id"),""),"city":d.get("cfCity"),"main6":m6(d.get("cfCity")),
      "lic":lic,"tier3":tier3(lic),"dev_broker":dev,"billed":billed,"received":recv,
      "demo_date":d.get("cfMeetingConductedOn"),"close_days_est":days,"created_at":d.get("created_at")})
json.dump(clo, open(BASE+"/closures_dataset.json","w"), indent=1)
with open(BASE+"/closures_dataset.csv","w",newline="") as fh:
    w=csv.DictWriter(fh,fieldnames=list(clo[0].keys())); w.writeheader()
    [w.writerow(x) for x in clo]

def agg(key,items):
    g=collections.defaultdict(lambda:{"n":0,"rev":0,"days":[]})
    for x in items:
        k=str(x[key]); g[k]["n"]+=1; g[k]["rev"]+=x["billed"]
        if x["close_days_est"] is not None: g[k]["days"].append(x["close_days_est"])
    out={}
    for k,v in g.items():
        out[k]={"deals":v["n"],"revenue":v["rev"],"avg_days":round(sum(v["days"])/len(v["days"]),1) if v["days"] else None}
    return out
C={}
C["n_closures"]=len(clo)
C["total_billed"]=sum(x["billed"] for x in clo)
C["total_received"]=sum(x["received"] for x in clo)
C["by_main6"]=agg("main6",clo)
C["by_tier3"]=agg("tier3",clo)
C["by_devbroker"]=agg("dev_broker",clo)
C["by_creator"]=agg("creator",clo)
alldays=[x["close_days_est"] for x in clo if x["close_days_est"] is not None]
C["avg_close_days_overall"]=round(sum(alldays)/len(alldays),1)
C["median_close_days"]=sorted(alldays)[len(alldays)//2]
# velocity by size and by dev/broker already in by_tier3/by_devbroker avg_days
C["top_deals"]=sorted([{"id":x["deal_id"],"name":x["name"],"city":x["city"],"lic":x["lic"],"dev_broker":x["dev_broker"],"billed":x["billed"],"days":x["close_days_est"]} for x in clo],key=lambda z:-z["billed"])[:15]

# ---------- MARKETING SOURCE FUNNEL (gathered via filter counts) ----------
SRC={
 "Organic":{"demos":95,"fiveplus":56,"won":13},
 "Google":{"demos":74,"fiveplus":49,"won":7},
 "Facebook":{"demos":47,"fiveplus":24,"won":1},
 "Sell.Do Interakt (WhatsApp)":{"demos":32,"fiveplus":14,"won":3},
 "Instagram":{"demos":3,"fiveplus":1,"won":0},
 "Outreach":{"demos":1,"fiveplus":1,"won":1},
 "My operator":{"demos":1,"fiveplus":0,"won":0},
}
for k,v in SRC.items():
    v["win_rate"]=round(v["won"]/v["demos"],4) if v["demos"] else 0
    v["fiveplus_rate"]=round(v["fiveplus"]/v["demos"],4) if v["demos"] else 0
C["source_funnel"]=SRC
C["source_demos_total"]=sum(v["demos"] for v in SRC.values())
json.dump(C, open(BASE+"/closures_analytics.json","w"), indent=1)

print("CLOSURES:",C["n_closures"],"| billed",C["total_billed"],"received",C["total_received"])
print("avg close days",C["avg_close_days_overall"],"median",C["median_close_days"])
print("\nby main6:")
for k,v in sorted(C["by_main6"].items(),key=lambda kv:-kv[1]["revenue"]): print(" ",k,v)
print("\nby tier3:")
for k,v in C["by_tier3"].items(): print(" ",k,v)
print("\nby dev/broker:")
for k,v in C["by_devbroker"].items(): print(" ",k,v)
print("\nby creator:")
for k,v in C["by_creator"].items(): print(" ",k,v)
print("\nSOURCE FUNNEL:")
for k,v in sorted(SRC.items(),key=lambda kv:-kv[1]["demos"]): print(f"  {k}: {v['demos']} demos, {int(v['fiveplus_rate']*100)}% 5+, {v['won']} won ({v['win_rate']*100:.1f}%)")
print("\nDEMO tier3 recount:",collections.Counter(r["tier3"] for r in rows))
# demo win-rate by tier3 for model
for t in ["<5","5-10","10+"]:
    sub=[r for r in rows if r["tier3"]==t]; w=sum(1 for r in sub if r["is_won"])
    print(f"  demos tier {t}: {len(sub)} demos, {w} won = {w/len(sub)*100:.1f}%")
