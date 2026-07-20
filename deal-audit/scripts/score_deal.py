"""Standalone conversion-probability scorer for the Sell.Do pre-sales CRON.
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
