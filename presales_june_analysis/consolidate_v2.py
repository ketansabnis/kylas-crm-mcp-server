import json, glob, os, csv, collections, statistics, datetime
BASE="/sessions/gifted-happy-euler/mnt/kylas-crm-mcp-server/presales_june_analysis"
seed=json.load(open(BASE+"/deal_ids_v2.json"))
seedmap={s["deal_id"]:(s["creator"],s["creator_id"]) for s in seed}
universe=[s["deal_id"] for s in seed]
rows=[]
missing=[]
for did in universe:
    p=f"{BASE}/deals/{did}.json"
    if not os.path.exists(p): missing.append(did); continue
    d=json.load(open(p))
    cr,crid=seedmap[did]; d["creator"]=cr; d["creator_id"]=crid
    b=d.get("bant") or {}
    lic=d.get("noOfLicenses")
    try: lic=int(lic)
    except: lic=None
    stage=(d.get("stage") or ""); sl=stage.lower()
    is_won=("won" in sl) or ("booked" in sl)
    is_lost=("lost" in sl) or ("unqualified" in sl)
    # normalize main6 city
    cc=(d.get("city_clean") or d.get("cfCity") or "")
    ccl=cc.lower()
    def m6(ccl):
        if "pune" in ccl or "pimpri" in ccl or "pcmc" in ccl: return "Pune"
        if "mumbai" in ccl or "thane" in ccl or "navi" in ccl or "borivali" in ccl or "chembur" in ccl or "andheri" in ccl: return "Mumbai/Thane"
        if any(x in ccl for x in["delhi","noida","gurgaon","gurugram","ghaziabad","faridabad","ncr"]): return "Delhi/NCR"
        if "bangal" in ccl or "bengal" in ccl: return "Bangalore"
        if "chennai" in ccl: return "Chennai"
        if "hyderab" in ccl or "secunderab" in ccl: return "Hyderabad"
        return None
    main6=m6(ccl)
    def gd(v):
        try: return int(v)
        except: return None
    rows.append({
      "deal_id":did,"deal_name":d.get("deal_name"),"creator":cr,"owner":d.get("owner"),
      "stage":stage,"is_won":is_won,"is_lost":is_lost,"is_open":not is_won and not is_lost,
      "created_at":d.get("created_at"),"updated_at":d.get("updated_at"),"cfMeetingConductedOn":d.get("cfMeetingConductedOn"),
      "noOfLicenses":lic,"license_tier":d.get("license_tier"),"is_5plus":(lic is not None and lic>=5),
      "city_raw":d.get("cfCity"),"city_clean":cc,"city_bucket":d.get("city_bucket"),"main6":main6 or "",
      "dev_or_broker":d.get("cfReDeveloperOrChannelPartner"),"onsite_or_online":d.get("onsite_or_online"),
      "name_valid":d.get("name_valid"),"enterprise_flag":d.get("enterprise_flag"),
      "pre_sales_verdict":str(d.get("pre_sales_verdict")).upper(),
      "stall_blocker":d.get("stall_blocker"),"blocker_owner":d.get("blocker_owner"),
      "bant_score":b.get("bant_score"),"bant_flag":b.get("bant_flag"),
      "prev_crm":d.get("cfPreviousCrm"),"actualValue":d.get("actualValue"),
      "one_line":d.get("one_line"),"notes_count":d.get("notes_count"),"notes_text":d.get("notes_text"),
    })
print("universe",len(universe),"rows",len(rows),"missing",missing)
rows.sort(key=lambda x:(x["creator"], -(x["noOfLicenses"] or 0)))
json.dump(rows, open(BASE+"/master_dataset.json","w"), indent=1)
with open(BASE+"/master_dataset.csv","w",newline="") as fh:
    w=csv.DictWriter(fh,fieldnames=list(rows[0].keys())); w.writeheader()
    for r in rows: w.writerow(r)
N=len(rows)
def rate(sub):
    return (sum(1 for r in sub if r["is_won"]), len(sub), (sum(1 for r in sub if r["is_won"])/len(sub) if sub else 0))
def group_winrate(key, order=None, minn=1):
    keys=order or sorted(set(str(r[key]) for r in rows))
    out=[]
    for k in keys:
        sub=[r for r in rows if str(r[key])==k]
        if len(sub)<minn: continue
        w,n,rt=rate(sub)
        g=sum(1 for r in sub if r["pre_sales_verdict"]=="GREEN")
        out.append({"key":k,"demos":n,"won":w,"win_rate":round(rt,4),"green":g,"green_rate":round(g/n,4) if n else 0,
                    "5plus":sum(1 for r in sub if r["is_5plus"]),"onsite":sum(1 for r in sub if r["onsite_or_online"]=="Onsite")})
    return out
A={}
A["N"]=N
A["verdict"]=dict(collections.Counter(r["pre_sales_verdict"] for r in rows))
A["tier"]=dict(collections.Counter(r["license_tier"] for r in rows))
A["5plus"]=sum(1 for r in rows if r["is_5plus"]); A["under5"]=N-A["5plus"]
A["won"]=sum(1 for r in rows if r["is_won"]); A["lost"]=sum(1 for r in rows if r["is_lost"]); A["open"]=sum(1 for r in rows if r["is_open"])
A["onsite"]=dict(collections.Counter(r["onsite_or_online"] for r in rows))
A["dev_broker"]=dict(collections.Counter(r["dev_or_broker"] for r in rows))
# WIN RATE permutations
A["winrate_by_bucket"]=group_winrate("city_bucket",["Main6","Other","Unknown"])
A["winrate_by_main6"]=group_winrate("main6",["Pune","Mumbai/Thane","Delhi/NCR","Bangalore","Chennai","Hyderabad"])
A["winrate_by_tier"]=group_winrate("license_tier",["1-4","5-9","10-39","40+"])
A["winrate_by_devbroker"]=group_winrate("dev_or_broker",["Developer","Channel partner","Broker"])
A["winrate_by_onsite"]=group_winrate("onsite_or_online",["Onsite","Online","Unknown"])
A["winrate_by_verdict"]=group_winrate("pre_sales_verdict",["GREEN","AMBER","RED"])
A["winrate_by_bantflag"]=group_winrate("bant_flag",["Strong","Partial","Weak","None"])
A["winrate_by_creator"]=group_winrate("creator",["Revati Ambike","Ashwini Nirmal","Gayatri More"])
# prev CRM: had a CRM vs never
def prevbucket(r):
    p=(r["prev_crm"] or "").lower()
    if not p or p=="none": return "Unknown"
    if "never" in p: return "Never used CRM"
    return "Had a CRM"
for r in rows: r["_prev"]=prevbucket(r)
A["winrate_by_prevcrm"]=group_winrate("_prev",["Had a CRM","Never used CRM","Unknown"])
# top cities by volume with winrate
cityc=collections.Counter(r["city_clean"] for r in rows if r["city_clean"])
top=[]
for city,cnt in cityc.most_common(25):
    sub=[r for r in rows if r["city_clean"]==city]
    w,n,rt=rate(sub)
    top.append({"city":city,"demos":n,"won":w,"win_rate":round(rt,4),
                "green":sum(1 for r in sub if r["pre_sales_verdict"]=="GREEN"),
                "5plus":sum(1 for r in sub if r["is_5plus"]),
                "onsite":sum(1 for r in sub if r["onsite_or_online"]=="Onsite")})
A["top_cities"]=top
# onsite by main6 (are rep cities getting onsite?)
A["onsite_by_main6"]={}
for c in ["Pune","Mumbai/Thane","Delhi/NCR","Bangalore","Chennai","Hyderabad"]:
    sub=[r for r in rows if r["main6"]==c]
    A["onsite_by_main6"][c]={"demos":len(sub),"onsite":sum(1 for r in sub if r["onsite_or_online"]=="Onsite")}
# won deals full
A["won_deals"]=sorted([{"id":r["deal_id"],"name":r["deal_name"],"lic":r["noOfLicenses"],"city":r["city_clean"],
    "bucket":r["city_bucket"],"val":gd(r["actualValue"]) or 0,"onsite":r["onsite_or_online"],
    "dev_broker":r["dev_or_broker"],"creator":r["creator"],"owner":r["owner"]} for r in rows if r["is_won"]],key=lambda x:-x["val"])
# revenue by cuts
def rev(sub): return sum((gd(r["actualValue"]) or 0) for r in sub if r["is_won"])
A["revenue_total"]=rev(rows)
A["revenue_by_bucket"]={b:rev([r for r in rows if r["city_bucket"]==b]) for b in ["Main6","Other","Unknown"]}
A["revenue_by_main6"]={c:rev([r for r in rows if r["main6"]==c]) for c in ["Pune","Mumbai/Thane","Delhi/NCR","Bangalore","Chennai","Hyderabad"]}
A["revenue_by_onsite"]={m:rev([r for r in rows if r["onsite_or_online"]==m]) for m in ["Onsite","Online"]}
A["revenue_by_tier"]={t:rev([r for r in rows if str(r["license_tier"])==t]) for t in ["1-4","5-9","10-39","40+"]}
# onsite win rate detail
ons=[r for r in rows if r["onsite_or_online"]=="Onsite"]; onl=[r for r in rows if r["onsite_or_online"]=="Online"]
A["onsite_detail"]={"onsite":rate(ons),"online":rate(onl)}
# blocker
A["blocker"]=dict(collections.Counter(r["stall_blocker"] for r in rows))
A["blocker_owner"]=dict(collections.Counter(r["blocker_owner"] for r in rows))
# main6 vs other: tier mix (are we bringing bigger deals in rep cities?)
def tiermix(sub):
    return {t:sum(1 for r in sub if str(r["license_tier"])==t) for t in ["1-4","5-9","10-39","40+"]}
A["tiermix_main6"]=tiermix([r for r in rows if r["city_bucket"]=="Main6"])
A["tiermix_other"]=tiermix([r for r in rows if r["city_bucket"]=="Other"])
# creator per stats
A["per_creator"]={}
for cr in ["Revati Ambike","Ashwini Nirmal","Gayatri More"]:
    sub=[r for r in rows if r["creator"]==cr]; w,n,rt=rate(sub)
    A["per_creator"][cr]={"demos":n,"won":w,"win_rate":round(rt,4),
      "GREEN":sum(1 for r in sub if r["pre_sales_verdict"]=="GREEN"),
      "RED":sum(1 for r in sub if r["pre_sales_verdict"]=="RED"),
      "5plus":sum(1 for r in sub if r["is_5plus"]),"onsite":sum(1 for r in sub if r["onsite_or_online"]=="Onsite"),
      "revenue":rev(sub)}
json.dump(A, open(BASE+"/analytics_v2.json","w"), indent=1, default=str)
# pretty print key tables
def show(title,lst):
    print("\n==",title,"==")
    for x in lst: print("  ",x)
print("VERDICT",A["verdict"],"| 5+",A["5plus"],"/",N,"| won",A["won"],"lost",A["lost"],"open",A["open"],"| revenue",A["revenue_total"])
show("WIN RATE by city bucket",A["winrate_by_bucket"])
show("WIN RATE by main6 city",A["winrate_by_main6"])
show("WIN RATE by tier",A["winrate_by_tier"])
show("WIN RATE by dev/broker",A["winrate_by_devbroker"])
show("WIN RATE by onsite",A["winrate_by_onsite"])
show("WIN RATE by verdict",A["winrate_by_verdict"])
show("WIN RATE by BANT flag",A["winrate_by_bantflag"])
show("WIN RATE by prev CRM",A["winrate_by_prevcrm"])
show("TOP CITIES",A["top_cities"])
print("\nonsite_by_main6",A["onsite_by_main6"])
print("revenue_by_bucket",A["revenue_by_bucket"])
print("revenue_by_main6",A["revenue_by_main6"])
print("revenue_by_onsite",A["revenue_by_onsite"])
print("tiermix main6",A["tiermix_main6"],"other",A["tiermix_other"])
print("per_creator",json.dumps(A["per_creator"]))
