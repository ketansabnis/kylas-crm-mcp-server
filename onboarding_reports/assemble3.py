#!/usr/bin/env python3
import json, os, datetime
BASE=os.path.dirname(os.path.abspath(__file__))
F=json.load(open(os.path.join(BASE,"fresh_2026-07-13.json")))
PRIOR=json.load(open(os.path.join(BASE,"snapshot_2026-07-10.json")))
pby={r["id"]:r for r in PRIOR["deals"]}
RUN=F["run_date"]; run_dt=datetime.date(2026,7,13)

deals=F["deals"]; ids=[d[0] for d in deals]
name={d[0]:d[1] for d in deals}; owner={d[0]:d[2] for d in deals}
stage_of={}
for st,lst in F["stages"].items():
    for i in lst: stage_of[i]=st
cat_of={}
for c,lst in F["cat"].items():
    for i in lst: cat_of[i]=c
S=lambda k:set(F[k])
not_signedup=S("not_signedup"); overdue_golive=S("overdue_golive")
overdue_task=S("overdue_task"); future_task=S("future_task")
idle5=S("idle_gt5"); idle7=S("idle_gt7")
A=F["age"]; ca14=set(A["ca14"]); ca30=set(A["ca30"]); ca60=set(A["ca60"]); ca90=set(A["ca90"]); ca180=set(A["ca180"])
V=F["value"]; L=F["lic"]
notes={int(k):v for k,v in F["notes"].items()}
newd={int(k):v for k,v in F["newdeals"].items()}

def idle_bucket(i):
    if i in idle7: return "7-15 d"
    if i in idle5: return "5-7 d"
    return "<=5 d"
def age_band(i):
    if i not in ca14: return "<14 d"
    if i not in ca30: return "14-30 d"
    if i not in ca60: return "30-60 d"
    if i not in ca90: return "60-90 d"
    if i not in ca180: return "90-180 d"
    return ">180 d"
def vband_of(i):
    if i in set(V["v10L"]): return ">=10L"
    if i in set(V["v7L"]): return "7-10L"
    if i in set(V["v5L"]): return "5-7L"
    if i in set(V["v3L"]): return "3-5L"
    if i in set(V["v2L"]): return "2-3L"
    if i in set(V["v1L"]): return "1-2L"
    return "blank"
def lband_of(i):
    if i in set(L["l50"]): return ">=50"
    if i in set(L["l20"]): return "20-49"
    if i in set(L["l10"]): return "10-19"
    return "<10/blank"
def note_date(ep):
    if ep is None: return None
    return (datetime.datetime(1970,1,1)+datetime.timedelta(milliseconds=ep+19800000)).strftime("%Y-%m-%d")
def cadence_of(ds):
    if ds is None: return "No note"
    if ds<=5: return "OK (<=5d)"
    if ds<=10: return "Watch"
    return "Stale"

recs=[]
for i in ids:
    p=pby.get(i); ep,txt=notes.get(i,[None,""])
    nd=note_date(ep)
    ds=None if nd is None else (run_dt-datetime.date(*map(int,nd.split("-")))).days
    nv=newd.get(i)
    billed = nv["billed"] if nv else (p.get("billed") if p else None)
    recv   = nv["recv"]   if nv else (p.get("recv")   if p else None)
    lic    = nv["lic"]    if nv else (p.get("lic")    if p else None)
    cat=cat_of.get(i,"(none)")
    high=bool((billed and billed>=300000) or (lic and lic>=30))
    recs.append({
      "id":i,"name":name[i],"owner":owner[i],"stage":stage_of.get(i,"?"),
      "age":age_band(i),"idle":idle_bucket(i),
      "last_note_epoch":ep,"last_note_date":nd,"last_note_text":txt,
      "dsince":ds,"cadence":cadence_of(ds),
      "overdue_golive": i in overdue_golive,"not_signedup": i in not_signedup,
      "no_task": (i not in overdue_task) and (i not in future_task),
      "overdue_task": i in overdue_task,"no_notes": ep is None,
      "category":cat,
      "suggested": (p.get("suggested") if p else (cat if cat not in ("(none)","Push to OB") else "C")),
      "gflag": (p.get("gflag") if p else "OK"),
      "greason": (p.get("greason") if p else "new deal this run"),
      "vband": vband_of(i),"lband": lband_of(i),
      "brand": (p.get("brand") if p else ""),
      "billed":billed,"recv":recv,"lic":lic,"high_value":high,
      "nstep": (p.get("nstep") if p else "Log first note + confirm kickoff / next milestone."),
      "pending_verdict": (p.get("pending_verdict","") if p else ""),
      "pending_action": (p.get("pending_action","") if p else ""),
      "movement_verdict":"BASELINE","movement_reason":"","stuck_streak":0,
    })

PEND_DEFAULT={
 4446753:("Moving","Inventory uploaded; only WhatsApp number pending from client. Chase number, then close."),
 4402389:("Customer-blocked","Customer asked to hold till 13-Jul; pending details due today. Chase today or escalate to sales."),
 4370308:("Moving","Sales training done; admin training to be scheduled. Book the date."),
 4241966:("Moving slowly","AI calling: pushing Netram for outgoing calls; no customer confirmation yet."),
 4233760:("Stalled","Awaiting flow + feedback from customer on AI calling. Set a deadline."),
 4233715:("Moving slowly","Outgoing-calling issues raised; JIRA open (ESTATE-21040). Track ETA."),
 4147287:("Customer-blocked","WhatsApp flow promised by Monday; no update on inventory. Chase both."),
 4144089:("STUCK","Customer unhappy vs sales promises, possible refund case. Needs Ankur/sales call now."),
 4079157:("Moving","Onsite sales training done; admin training then handover to AM."),
 3623014:("STUCK","Refund legal-notice case with Amit Tare. Not an onboarding item - move out of pipeline."),
 3575524:("STUCK","Voora: pending EPR docs + external handover since Feb. Escalate."),
 3302998:("Customer-blocked","Times: client reported data discrepancies; review meeting rescheduled. Fix a date."),
 4255693:("Moving","Calicut: Q&A + mobile + admin training 2.0 planned this week."),
}
_by={r["id"]:r for r in recs}
for i in F["stages"]["Pending on Customer"]:
    r=_by[i]
    v=PEND_DEFAULT.get(i)
    if v: r["pending_verdict"],r["pending_action"]=v
    elif not r.get("pending_verdict"): r["pending_verdict"],r["pending_action"]=("Unknown","Owner to log status + next step immediately.")

from collections import defaultdict
og=defaultdict(lambda:{"n":0,"nonotes":[],"pending":[]})
pend=set(F["stages"]["Pending on Customer"])
for r in recs:
    o=r["owner"]; og[o]["n"]+=1
    if r["no_notes"]: og[o]["nonotes"].append(r["name"])
    if r["id"] in pend: og[o]["pending"].append(r["name"])
owner_gaps={}
for o,d in sorted(og.items(),key=lambda kv:-kv[1]["n"]):
    parts=[f"{d['n']} deal(s)."]
    if d["nonotes"]: parts.append("no notes: "+", ".join(d["nonotes"][:5])+".")
    if d["pending"]: parts.append("pending-on-customer: "+", ".join(d["pending"][:5])+".")
    owner_gaps[o]=" ".join(parts)

OUT={"report_date":RUN,"run_label":"Run 8 (Mon 13-Jul-2026) vs 10-Jul & 07-Jul","run_index":8,
     "pipeline_id":27474,"pipeline_name":"Sell.do Onboarding Pipeline",
     "owner_gaps":owner_gaps,"deals":recs}
json.dump(OUT,open(os.path.join(BASE,"current_data.json"),"w"),indent=1)
print("assembled",len(recs))
print("stages:",{k:len(v) for k,v in F["stages"].items()})
print("new:",[r["id"] for r in recs if r["id"] not in pby])
print("dropped:",[i for i in pby if i not in set(ids)])
print("no_task:",sum(1 for r in recs if r["no_task"]),"overdue_task:",sum(1 for r in recs if r["overdue_task"]),"no_notes:",sum(1 for r in recs if r["no_notes"]))
