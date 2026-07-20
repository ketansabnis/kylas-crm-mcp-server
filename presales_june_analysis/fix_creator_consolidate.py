import json, glob, os, csv, collections
BASE="/sessions/gifted-happy-euler/mnt/kylas-crm-mcp-server/presales_june_analysis"
D=BASE+"/deals"
seed=json.load(open(BASE+"/deal_ids.json"))
seedmap={s["deal_id"]:(s["creator"],s["creator_id"]) for s in seed}
files=[f for f in glob.glob(D+"/*.json") if os.path.basename(f)[:-5].isdigit()]
rows=[]
for f in files:
    d=json.load(open(f))
    did=d.get("deal_id")
    # AUTHORITATIVE creator from seed (report-derived), overwrite unreliable JSON label
    cr,crid=seedmap.get(did,(d.get("creator"),d.get("creator_id")))
    d["creator"]=cr; d["creator_id"]=crid
    json.dump(d, open(f,"w"), indent=1)  # persist corrected creator back to per-deal file
    b=d.get("bant") or {}
    lic=d.get("noOfLicenses")
    try: lic=int(lic)
    except: lic=None
    stage=(d.get("stage") or ""); sl=stage.lower()
    is_won=("won" in sl) or ("booked" in sl)
    is_lost=("lost" in sl) or ("unqualified" in sl)
    rows.append({
      "deal_id":did,"deal_name":d.get("deal_name"),"creator":cr,"owner":d.get("owner"),
      "pipeline":d.get("pipeline"),"stage":stage,"is_won":is_won,"is_lost":is_lost,"is_open":not is_won and not is_lost,
      "created_at":d.get("created_at"),"updated_at":d.get("updated_at"),
      "noOfLicenses":lic,"license_tier":d.get("license_tier"),"is_5plus":(lic is not None and lic>=5),
      "city_raw":d.get("cfCity"),"city_clean":d.get("city_clean"),"city_bucket":d.get("city_bucket"),
      "dev_or_broker":d.get("cfReDeveloperOrChannelPartner"),"onsite_or_online":d.get("onsite_or_online"),
      "name_valid":d.get("name_valid"),"enterprise_flag":d.get("enterprise_flag"),
      "pre_sales_verdict":str(d.get("pre_sales_verdict")).upper(),
      "stall_blocker":d.get("stall_blocker"),"blocker_owner":d.get("blocker_owner"),
      "bant_budget":b.get("budget"),"bant_authority":b.get("authority"),"bant_need":b.get("need"),
      "bant_timeline":b.get("timeline"),"bant_score":b.get("bant_score"),"bant_flag":b.get("bant_flag"),
      "prev_crm":d.get("cfPreviousCrm"),"products":d.get("products"),"actualValue":d.get("actualValue"),
      "one_line":d.get("one_line"),"notes_count":d.get("notes_count"),"notes_text":d.get("notes_text"),
    })
rows.sort(key=lambda x:(x["creator"], -(x["noOfLicenses"] or 0)))
json.dump(rows, open(BASE+"/master_dataset.json","w"), indent=1)
with open(BASE+"/master_dataset.csv","w",newline="") as fh:
    w=csv.DictWriter(fh,fieldnames=list(rows[0].keys())); w.writeheader()
    for r in rows: w.writerow(r)
def dist(k): return dict(collections.Counter(str(r[k]) for r in rows))
cc=collections.Counter(r["creator"] for r in rows)
per={}
for cr in cc:
    sub=[r for r in rows if r["creator"]==cr]
    per[cr]={"demos":len(sub),
      "GREEN":sum(1 for r in sub if r["pre_sales_verdict"]=="GREEN"),
      "AMBER":sum(1 for r in sub if r["pre_sales_verdict"]=="AMBER"),
      "RED":sum(1 for r in sub if r["pre_sales_verdict"]=="RED"),
      "5plus":sum(1 for r in sub if r["is_5plus"]),
      "onsite":sum(1 for r in sub if r["onsite_or_online"]=="Onsite"),
      "won":sum(1 for r in sub if r["is_won"]),
      "name_invalid":sum(1 for r in sub if r["name_valid"] in (False,"false","False")),
    }
print("creator counts (from seed):",dict(cc))
print("per-creator:",json.dumps(per,indent=1))
print("5plus_true:",sum(1 for r in rows if r["is_5plus"]),"5plus_false:",sum(1 for r in rows if not r["is_5plus"]))
print("verdict:",dist("pre_sales_verdict"))
# reload summary_stats and patch creator sections
S=json.load(open(BASE+"/summary_stats.json"))
S["creator_counts"]=dict(cc)
S["per_creator"]=per
S["created_vs_demo"]={"Revati Ambike":{"created":164,"demo":126},"Ashwini Nirmal":{"created":158,"demo":107},"Gayatri More":{"created":6,"demo":4},"TOTAL":{"created":328,"demo":237}}
json.dump(S, open(BASE+"/summary_stats.json","w"), indent=1)
print("patched summary_stats.json")
