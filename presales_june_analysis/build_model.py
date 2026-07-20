"""Build a transparent conversion-probability model from the 253 June demos.
Naive-Bayes likelihood-ratio scorecard -> dependency-free scoring function for the hourly CRON.
Features (all known at/after demo, available in CRM): licence tier, developer-vs-CP, onsite, city class, BANT.
Plus a separate marketing SOURCE multiplier (from aggregate source win-rates)."""
import json, collections, math
BASE="/sessions/gifted-happy-euler/mnt/kylas-crm-mcp-server/presales_june_analysis"
rows=json.load(open(BASE+"/master_dataset.json"))
N=len(rows); W=sum(1 for r in rows if r["is_won"]); L=N-W
base_rate=W/N; base_odds=W/L

def city_class(r):
    m=r.get("main6") or ""
    if m in ("Hyderabad","Chennai"): return "HOT"
    if m in ("Mumbai/Thane","Delhi/NCR","Bangalore","Pune"): return "CORE"
    return "OTHER"
def dev_class(r):
    return "Developer" if r.get("dev_or_broker")=="Developer" else "ChannelPartner"
def onsite_class(r):
    return "Onsite" if r.get("onsite_or_online")=="Onsite" else "Online"
def tier_class(r):
    return r.get("tier3") or "unknown"
def bant_class(r):
    return (r.get("bant_flag") or "None")

FEATS={"tier":tier_class,"dev":dev_class,"onsite":onsite_class,"city":city_class,"bant":bant_class}
# Laplace-smoothed likelihood ratios LR(v)=P(v|win)/P(v|loss)
weights={}
for fname,fn in FEATS.items():
    wins=[r for r in rows if r["is_won"]]; loss=[r for r in rows if not r["is_won"]]
    vals=set(fn(r) for r in rows)
    weights[fname]={}
    for v in vals:
        pw=(sum(1 for r in wins if fn(r)==v)+1)/(len(wins)+len(vals))
        pl=(sum(1 for r in loss if fn(r)==v)+1)/(len(loss)+len(vals))
        weights[fname][v]=round(math.log(pw/pl),4)  # log-LR (additive)
log_base_odds=math.log(base_odds)

# SOURCE multiplier (aggregate win-rates vs base) -> log-LR approx
src_wr={"Organic":0.137,"Google":0.095,"Facebook":0.021,"Sell.Do Interakt (WhatsApp)":0.094,"Instagram":0.02,"Outreach":0.5,"My operator":0.05}
src_log={}
for s,wr in src_wr.items():
    wr=min(max(wr,0.005),0.95); od=wr/(1-wr)
    src_log[s]=round(math.log(od)-log_base_odds,4)

model={"base_rate":round(base_rate,4),"log_base_odds":round(log_base_odds,4),
       "feature_log_lr":weights,"source_log_lr_optional":src_log,
       "note":"score = log_base_odds + sum(feature_log_lr[feat][value]) [+ source_log_lr]. prob=1/(1+exp(-score))."}
json.dump(model, open(BASE+"/model_weights.json","w"), indent=2)

def score(r, use_source=None):
    s=log_base_odds
    for fname,fn in FEATS.items():
        s+=weights[fname].get(fn(r),0)
    if use_source and use_source in src_log: s+=src_log[use_source]
    return 1/(1+math.exp(-s))
# calibration on the 253 (no source, since per-deal source unknown)
for r in rows: r["_p"]=score(r)
rows_sorted=sorted(rows,key=lambda r:-r["_p"])
print("base rate %.1f%%  base_odds %.3f"%(base_rate*100,base_odds))
print("\n=== log-LR weights (higher = more likely to convert) ===")
for f,d in weights.items():
    print(" ",f,{k:round(v,2) for k,v in sorted(d.items(),key=lambda kv:-kv[1])})
print("\nsource log-LR:",{k:round(v,2) for k,v in sorted(src_log.items(),key=lambda kv:-kv[1])})
# decile calibration
print("\n=== calibration: predicted vs actual (sorted by prob, quintiles) ===")
import statistics
n=len(rows_sorted); q=n//5
bands=[("HOT (top 20%)",0,q),("Warm",q,2*q),("Mid",2*q,3*q),("Cool",3*q,4*q),("Cold (bottom 20%)",4*q,n)]
for name,a,b in bands:
    seg=rows_sorted[a:b]; pred=statistics.mean(r["_p"] for r in seg); act=sum(1 for r in seg if r["is_won"])/len(seg)
    print(f"  {name:20s} n={len(seg):3d}  pred {pred*100:5.1f}%  actual {act*100:5.1f}%")
# threshold table
print("\n=== if we only pursued demos above a probability threshold ===")
for th in [0.05,0.10,0.15,0.20,0.30]:
    seg=[r for r in rows if r["_p"]>=th]; w=sum(1 for r in seg if r["is_won"])
    print(f"  P>= {int(th*100):2d}%: {len(seg):3d} demos capture {w}/{W} wins ({w/W*100:.0f}% of wins) at {w/len(seg)*100 if seg else 0:.1f}% win-rate")
# write standalone scorer
open(BASE+"/score_deal.py","w").write('''"""Standalone conversion-probability scorer for the Sell.Do pre-sales CRON.
No dependencies. Load model_weights.json (exported from June 2026 data) and call score_deal(deal).
`deal` dict keys: licences:int, account_type:'Developer'|'ChannelPartner', mode:'Onsite'|'Online',
city:str (raw), bant:'Strong'|'Partial'|'Weak'|'None', source:str (optional, e.g. 'Facebook')."""
import json, math, os
_M=json.load(open(os.path.join(os.path.dirname(__file__),"model_weights.json")))
def _tier(lic):
    if lic is None: return "unknown"
    return "<5" if lic<5 else ("5-10" if lic<=10 else "10+")
def _city(c):
    c=(c or "").lower()
    if any(x in c for x in["hyderab","secunderab","chennai"]): return "HOT"
    if any(x in c for x in["pune","mumbai","thane","navi","delhi","noida","gurgaon","gurugram","ghaziabad","faridabad","ncr","bangal","bengal"]): return "CORE"
    return "OTHER"
def score_deal(deal):
    s=_M["log_base_odds"]; W=_M["feature_log_lr"]
    s+=W["tier"].get(_tier(deal.get("licences")),0)
    s+=W["dev"].get("Developer" if deal.get("account_type")=="Developer" else "ChannelPartner",0)
    s+=W["onsite"].get("Onsite" if deal.get("mode")=="Onsite" else "Online",0)
    s+=W["city"].get(_city(deal.get("city")),0)
    s+=W["bant"].get(deal.get("bant","None"),0)
    src=deal.get("source")
    if src and src in _M.get("source_log_lr_optional",{}): s+=_M["source_log_lr_optional"][src]
    p=1/(1+math.exp(-s))
    band="HOT" if p>=0.20 else "WARM" if p>=0.12 else "MID" if p>=0.06 else "COLD"
    return {"probability":round(p,3),"band":band}
if __name__=="__main__":
    print(score_deal({"licences":30,"account_type":"Developer","mode":"Onsite","city":"Hyderabad","bant":"Strong","source":"Organic"}))
    print(score_deal({"licences":2,"account_type":"ChannelPartner","mode":"Online","city":"Jaipur","bant":"Weak","source":"Facebook"}))
''')
print("\nwrote model_weights.json + score_deal.py")
