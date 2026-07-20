import json, glob, os, math, collections, statistics
BASE="/sessions/gifted-happy-euler/mnt/kylas-crm-mcp-server/marketing_weekly"
WK="2026-07-12"; WSTART="2026-07-06"
SRC={}
for s,ids in {
 "Facebook":[2233926,2936414,4459651,4462488,4462721,4463072,4474147,4476885,4477694,4478486,4480493],
 "Organic":[3932086,4371017,4457247,4463792,4473011,4473367,4473579,4473779,4474591,4475161,4481170,4495442,4497602],
 "Google":[4459518,4474327,4474498,4474633,4477974,4478884,4481146,4481390,4482359,4494040],
 "WhatsApp":[2363883,4295712,4463623,4472783,4474942,4475026,4494374],
}.items():
    for i in ids: SRC[i]=s
REVATI=[2233926,2363883,2936414,4295712,4371017,4456141,4457247,4459518,4462488,4462721,4463072,4463623,4472783,4473011,4473367,4474591,4476885,4477694,4477736,4478486,4478884,4480493,4481390,4482359,4494374,4495442,4497602]
SRC_ADJ={"Organic":0.4,"Google":0.0,"WhatsApp":0.0,"Facebook":-1.6,"Instagram":-1.68}
rows=[]
for f in glob.glob(BASE+"/deals_"+WK+"/*.json"):
    if not os.path.basename(f)[:-5].isdigit(): continue
    d=json.load(open(f)); i=d["deal_id"]
    src=SRC.get(i,"Unknown")
    p=float(d.get("prob") or 0.01); p=min(max(p,0.001),0.999)
    S=math.log(p/(1-p))+SRC_ADJ.get(src,0.0)
    p2=1/(1+math.exp(-S))
    band="HOT" if p2>=0.20 else "WARM" if p2>=0.12 else "MID" if p2>=0.06 else "COLD"
    lic=d.get("licences")
    try: lic=int(lic)
    except: lic=None
    d.update({"source":src,"creator":"Revati Ambike" if i in REVATI else "Ashwini Nirmal",
              "prob":round(p2,3),"band":band,"licences":lic,
              "is5plus":(lic is not None and lic>=5)})
    rows.append(d)
N=len(rows)
def C(k): return collections.Counter(str(r.get(k)) for r in rows)
main6=lambda c:(c or "").lower()
def m6(c):
    c=(c or "").lower()
    for k in ["pune","mumbai","thane","navi","delhi","noida","gurgaon","gurugram","ghaziabad","faridabad","ncr","bangal","bengal","chennai","hyderab"]:
        if k in c: return True
    return False
five=sum(1 for r in rows if r["is5plus"]); green=sum(1 for r in rows if r["verdict"]=="GREEN")
dev=sum(1 for r in rows if r.get("dev_broker")=="Developer")
m6rows=[r for r in rows if m6(r.get("city"))]
onsite_m6=sum(1 for r in m6rows if r.get("onsite")=="Onsite")
onsite_all=sum(1 for r in rows if r.get("onsite")=="Onsite")
T={"five":50,"green":25,"devshare":0.50,"onsite_m6":0.40}
hot=[r for r in rows if r["band"]=="HOT"]; warm=[r for r in rows if r["band"]=="WARM"]
zero_fu=[r for r in rows if (r.get("sales_followup_since_demo") or 0)==0]
dummy=[r for r in rows if r.get("dummy_phone")]
unver=[r for r in rows if r.get("unverified_contact")]
badname=[r for r in rows if r.get("name_valid") is False]
# source perf
sp={}
for s in ["Organic","Google","Facebook","WhatsApp","Unknown"]:
    sub=[r for r in rows if r["source"]==s]
    if not sub: continue
    sp[s]={"demos":len(sub),"five":sum(1 for r in sub if r["is5plus"]),
           "green":sum(1 for r in sub if r["verdict"]=="GREEN"),
           "red":sum(1 for r in sub if r["verdict"]=="RED"),
           "dev":sum(1 for r in sub if r.get("dev_broker")=="Developer"),
           "hotwarm":sum(1 for r in sub if r["band"] in("HOT","WARM"))}
# allocation by owner
alloc=collections.Counter(r.get("owner") for r in rows)
# routing check
routing={"dev_to_revati":sum(1 for r in rows if r.get("dev_broker")=="Developer" and r["creator"]=="Revati Ambike"),
         "dev_to_ashwini":sum(1 for r in rows if r.get("dev_broker")=="Developer" and r["creator"]=="Ashwini Nirmal"),
         "cp_to_ashwini":sum(1 for r in rows if r.get("dev_broker")=="Channel partner" and r["creator"]=="Ashwini Nirmal"),
         "cp_to_revati":sum(1 for r in rows if r.get("dev_broker")=="Channel partner" and r["creator"]=="Revati Ambike")}
snap={"week_start":WSTART,"week_end":WK,"N":N,"five":five,"green":green,"verdict":dict(C("verdict")),
      "band":dict(C("band")),"tier":dict(C("tier")),"dev":dev,"cp":N-dev,"onsite_all":onsite_all,
      "main6":len(m6rows),"onsite_m6":onsite_m6,"source":sp,"creator":dict(C("creator")),
      "alloc":dict(alloc),"routing":routing,
      "alerts":{"zero_followup":len(zero_fu),"dummy_phone":len(dummy),"unverified":len(unver),"bad_name":len(badname)},
      "targets":T}
json.dump(snap,open(BASE+f"/snapshot_{WK}.json","w"),indent=2)
json.dump(rows,open(BASE+f"/deals_{WK}.json","w"),indent=1)
print(f"WEEK {WSTART} -> {WK}  |  demos={N}")
print(f"5+ seats: {five} / target {T['five']}   GREEN: {green} / target {T['green']}")
print("verdict",dict(C("verdict")),"| band",dict(C("band")),"| tier",dict(C("tier")))
print(f"developer {dev} ({dev/N*100:.0f}%) vs CP {N-dev}  [floor 50%]")
print(f"onsite {onsite_all}/{N} all; Main-6 onsite {onsite_m6}/{len(m6rows)} [target 40%]")
print("\nSOURCE:")
for s,v in sorted(sp.items(),key=lambda kv:-kv[1]["demos"]):
    print(f"  {s:9s} demos {v['demos']:2d} | 5+ {v['five']:2d} | GREEN {v['green']} | RED {v['red']} | dev {v['dev']} | HOT/WARM {v['hotwarm']}")
print("\nCREATOR:",dict(C("creator")))
print("ROUTING:",routing)
print("\nALLOCATION by sales owner:")
for o,c in alloc.most_common(): print(f"  {o:22s} {c}")
print("\nALERTS: zero-followup",len(zero_fu),"| dummy phone",len(dummy),"| unverified contact",len(unver),"| junk name",len(badname))
print("\nHOT/WARM list:")
for r in sorted(hot+warm,key=lambda x:-x["prob"]):
    print(f"  {r['prob']:.2f} {r['band']:4s} #{r['deal_id']} {str(r['name'])[:22]:22s} {str(r['licences']):>3s}u {str(r.get('city'))[:12]:12s} {str(r.get('owner'))[:16]:16s} fu={r.get('sales_followup_since_demo')} -> {str(r.get('next_action'))[:60]}")
print("\nZERO-FOLLOWUP (any band):")
for r in sorted(zero_fu,key=lambda x:-x["prob"])[:12]:
    print(f"  {r['prob']:.2f} {r['band']:4s} #{r['deal_id']} {str(r['name'])[:22]:22s} {str(r.get('owner'))[:16]:16s} {r['verdict']}")
