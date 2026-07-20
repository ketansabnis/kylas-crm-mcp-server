import json, glob, os, csv, collections
BASE="/sessions/gifted-happy-euler/mnt/kylas-crm-mcp-server/presales_june_analysis"
D=BASE+"/deals"
files=[f for f in glob.glob(D+"/*.json") if os.path.basename(f)[:-5].isdigit()]
rows=[]
for f in files:
    d=json.load(open(f))
    b=d.get("bant") or {}
    lic=d.get("noOfLicenses")
    try: lic=int(lic)
    except: lic=None
    stage=(d.get("stage") or "")
    sl=stage.lower()
    is_won = ("won" in sl) or ("booked" in sl)
    is_lost = ("lost" in sl) or ("unqualified" in sl)
    is_open = not is_won and not is_lost
    r={
      "deal_id":d.get("deal_id"),"deal_name":d.get("deal_name"),
      "creator":d.get("creator"),"owner":d.get("owner"),
      "pipeline":d.get("pipeline"),"stage":stage,
      "is_won":is_won,"is_lost":is_lost,"is_open":is_open,
      "created_at":d.get("created_at"),"updated_at":d.get("updated_at"),
      "noOfLicenses":lic,"license_tier":d.get("license_tier"),
      "is_5plus": (lic is not None and lic>=5),
      "city_raw":d.get("cfCity"),"city_clean":d.get("city_clean"),"city_bucket":d.get("city_bucket"),
      "dev_or_broker":d.get("cfReDeveloperOrChannelPartner"),
      "onsite_or_online":d.get("onsite_or_online"),
      "name_valid":d.get("name_valid"),
      "enterprise_flag":d.get("enterprise_flag"),
      "pre_sales_verdict":str(d.get("pre_sales_verdict")).upper(),
      "stall_blocker":d.get("stall_blocker"),"blocker_owner":d.get("blocker_owner"),
      "bant_budget":b.get("budget"),"bant_authority":b.get("authority"),
      "bant_need":b.get("need"),"bant_timeline":b.get("timeline"),
      "bant_score":b.get("bant_score"),"bant_flag":b.get("bant_flag"),
      "prev_crm":d.get("cfPreviousCrm"),"products":d.get("products"),
      "actualValue":d.get("actualValue"),
      "one_line":d.get("one_line"),
      "notes_count":d.get("notes_count"),"notes_text":d.get("notes_text"),
    }
    rows.append(r)
rows.sort(key=lambda x:(x["creator"], -(x["noOfLicenses"] or 0)))
# master json + csv
json.dump(rows, open(BASE+"/master_dataset.json","w"), indent=1)
cols=list(rows[0].keys())
with open(BASE+"/master_dataset.csv","w",newline="") as fh:
    w=csv.DictWriter(fh,fieldnames=cols); w.writeheader()
    for r in rows: w.writerow(r)

def dist(key):
    c=collections.Counter(str(r[key]) for r in rows); return dict(c)
def cross(a,b):
    c=collections.defaultdict(lambda:collections.Counter())
    for r in rows: c[str(r[a])][str(r[b])]+=1
    return {k:dict(v) for k,v in c.items()}

N=len(rows)
summary={
 "N":N,
 "verdict":dist("pre_sales_verdict"),
 "tier":dist("license_tier"),
 "is_5plus_true":sum(1 for r in rows if r["is_5plus"]),
 "is_5plus_false":sum(1 for r in rows if not r["is_5plus"]),
 "city_bucket":dist("city_bucket"),
 "onsite":dist("onsite_or_online"),
 "dev_or_broker":dist("dev_or_broker"),
 "stage":dist("stage"),
 "won":sum(1 for r in rows if r["is_won"]),
 "lost":sum(1 for r in rows if r["is_lost"]),
 "open":sum(1 for r in rows if r["is_open"]),
 "enterprise_flag_true":sum(1 for r in rows if r["enterprise_flag"] in (True,"true","True")),
 "name_invalid":sum(1 for r in rows if r["name_valid"] in (False,"false","False")),
 "blocker":dist("stall_blocker"),
 "blocker_owner":dist("blocker_owner"),
 "verdict_by_creator":cross("creator","pre_sales_verdict"),
 "creator_counts":dist("creator"),
 "verdict_by_tier":cross("license_tier","pre_sales_verdict"),
 "city_by_verdict":cross("city_bucket","pre_sales_verdict"),
 "won_by_city":{k:sum(1 for r in rows if r["city_bucket"]==k and r["is_won"]) for k in ["Main6","Other","Unknown"]},
 "count_by_city":{k:sum(1 for r in rows if r["city_bucket"]==k) for k in ["Main6","Other","Unknown"]},
 "won_by_tier":{},
 "won_by_creator":{},
 "onsite_by_verdict":cross("onsite_or_online","pre_sales_verdict"),
 "5plus_by_creator":{},
 "onsite_by_creator":{},
 "won_by_verdict":cross("pre_sales_verdict","is_won"),
}
for t in ["1-4","5-9","10-39","40+","unknown"]:
    summary["won_by_tier"][t]=sum(1 for r in rows if str(r["license_tier"])==t and r["is_won"])
for cr in summary["creator_counts"]:
    tot=sum(1 for r in rows if r["creator"]==cr)
    summary["won_by_creator"][cr]=sum(1 for r in rows if r["creator"]==cr and r["is_won"])
    summary["5plus_by_creator"][cr]=sum(1 for r in rows if r["creator"]==cr and r["is_5plus"])
    summary["onsite_by_creator"][cr]=sum(1 for r in rows if r["creator"]==cr and r["onsite_or_online"]=="Onsite")
# city detail among Main6 and Other
cityc=collections.Counter(r["city_bucket"]+"|"+str(r["city_clean"]) for r in rows)
# top cities
topcity=collections.Counter(str(r["city_clean"]) for r in rows)
summary["top_cities"]=dict(topcity.most_common(20))
# main6 city breakdown
def norm_main(cc):
    cc=(cc or "").lower()
    if "pune" in cc: return "Pune"
    if "mumbai" in cc or "thane" in cc or "navi" in cc: return "Mumbai/Thane"
    if any(x in cc for x in ["delhi","noida","gurgaon","gurugram","ghaziabad","faridabad","ncr"]): return "Delhi/NCR"
    if "bangal" in cc or "bengal" in cc: return "Bangalore"
    if "chennai" in cc: return "Chennai"
    if "hyderab" in cc: return "Hyderabad"
    return None
main6=collections.Counter()
main6won=collections.Counter()
for r in rows:
    m=norm_main(r["city_clean"]) or norm_main(r["city_raw"])
    if m:
        main6[m]+=1
        if r["is_won"]: main6won[m]+=1
summary["main6_breakdown"]=dict(main6)
summary["main6_won"]=dict(main6won)
# enterprise & 40+ lists
summary["forty_plus_deals"]=[{"id":r["deal_id"],"name":r["deal_name"],"lic":r["noOfLicenses"],"city":r["city_clean"],"verdict":r["pre_sales_verdict"],"stage":r["stage"],"owner":r["owner"]} for r in rows if (r["noOfLicenses"] or 0)>=40]
summary["enterprise_deals"]=[{"id":r["deal_id"],"name":r["deal_name"],"lic":r["noOfLicenses"],"city":r["city_clean"],"verdict":r["pre_sales_verdict"],"stage":r["stage"]} for r in rows if r["enterprise_flag"] in (True,"true","True")]
summary["won_deals"]=[{"id":r["deal_id"],"name":r["deal_name"],"lic":r["noOfLicenses"],"city":r["city_clean"],"val":r["actualValue"],"creator":r["creator"],"owner":r["owner"]} for r in rows if r["is_won"]]
json.dump(summary, open(BASE+"/summary_stats.json","w"), indent=1)
print(json.dumps(summary, indent=1))
