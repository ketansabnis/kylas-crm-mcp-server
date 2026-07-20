#!/usr/bin/env python3
import json, os, datetime
BASE=os.path.dirname(os.path.abspath(__file__))
F=json.load(open(os.path.join(BASE,"fresh.json")))
PRIOR=json.load(open(os.path.join(BASE,"snapshot_2026-07-02.json")))
pby={r["id"]:r for r in PRIOR["deals"]}
RUN=F["run_date"]
run_dt=datetime.date(2026,7,7)

deals=F["deals"]
ids=[d[0] for d in deals]
name={d[0]:d[1] for d in deals}
owner={d[0]:d[2] for d in deals}

def S(k): return set(F[k])
stage_of={}
for st,lst in F["stages"].items():
    for i in lst: stage_of[i]=st
cat_of={}
for c,lst in F["cat"].items():
    for i in lst: cat_of[i]=c

not_signedup=S("not_signedup"); overdue_golive=S("overdue_golive")
overdue_task=S("overdue_task"); future_task=set(F["future_task"])
idle5=set(F["idle_gt5"]); idle7=set(F["idle_gt7"])
ca14=set(F["age"]["ca14"]); ca30=set(F["age"]["ca30"]); ca60=set(F["age"]["ca60"])
ca90=set(F["age"]["ca90"]); ca180=set(F["age"]["ca180"])
notes={int(k):v for k,v in F["notes"].items()}
newdeals={int(k):v for k,v in F["newdeals"].items()}

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

def vband(b):
    if b is None: return "blank"
    if b>=1000000: return ">=10L"
    if b>=700000: return "7-10L"
    if b>=500000: return "5-7L"
    if b>=300000: return "3-5L"
    if b>=200000: return "2-3L"
    if b>=100000: return "1-2L"
    return "<1L"

def lband(l):
    if l is None: return "<10/blank"
    if l>=50: return ">=50"
    if l>=20: return "20-49"
    if l>=10: return "10-19"
    return "<10/blank"

def note_date(ep):
    if ep is None: return None
    d=datetime.datetime(1970,1,1)+datetime.timedelta(milliseconds=ep+19800000)  # IST
    return d.strftime("%Y-%m-%d")

def cadence_of(ds):
    if ds is None: return "No note"
    if ds<=5: return "OK (<=5d)"
    if ds<=10: return "Watch"
    return "Stale"

recs=[]
for i in ids:
    p=pby.get(i)
    ep,txt=notes.get(i,[None,""])
    nd=note_date(ep)
    ds=None if nd is None else (run_dt-datetime.date(*map(int,nd.split("-")))).days
    nv=newdeals.get(i)
    billed = nv["billed"] if nv else (p.get("billed") if p else None)
    recv   = nv["recv"]   if nv else (p.get("recv")   if p else None)
    lic    = nv["lic"]    if nv else (p.get("lic")    if p else None)
    cat=cat_of.get(i,"(none)")
    high=bool((billed and billed>=300000) or (lic and lic>=30))
    is_new = p is None
    rec={
        "id":i,"name":name[i],"owner":owner[i],"stage":stage_of.get(i,"?"),
        "age":age_band(i),"idle":idle_bucket(i),
        "last_note_epoch":ep,"last_note_date":nd,"last_note_text":txt,
        "dsince":ds,"cadence":cadence_of(ds),
        "overdue_golive": i in overdue_golive,
        "not_signedup": i in not_signedup,
        "no_task": (i not in overdue_task) and (i not in future_task),
        "overdue_task": i in overdue_task,
        "no_notes": ep is None,
        "category":cat,
        "suggested": (p.get("suggested") if p else cat if cat!="(none)" else "C"),
        "gflag": (p.get("gflag") if p else "OK"),
        "greason": (p.get("greason") if p else "new deal this run"),
        "vband": vband(billed),"lband": lband(lic),
        "brand": (p.get("brand") if p else ""),
        "billed":billed,"recv":recv,"lic":lic,
        "high_value":high,
        "nstep": (p.get("nstep") if p else "Log first note + confirm kickoff / next milestone."),
        "pending_verdict": (p.get("pending_verdict","") if p else ""),
        "pending_action": (p.get("pending_action","") if p else ""),
        "movement_verdict":"BASELINE","movement_reason":"","stuck_streak":0,
    }
    recs.append(rec)

# Ensure every Pending-on-Customer deal has a pending_verdict (build_report Sheet6 requires it)
PEND_DEFAULT={
 4241966:("Moving slowly","AI calling: call scheduled but customer didn't join; reschedule next week and chase feedback toward handover."),
 4233715:("Moving slowly","Outbound AI calling in customer testing; ESTATE-21040 bulk-call Jira raised (ETA 11.2). Confirm test results."),
 4147287:("Moving","Knowlarity issue resolved, lead import + hierarchy done; chase inventory + WhatsApp workflow (6-7 Jul)."),
 4144089:("Customer-blocked","Concall with Ankur + customer Mon on virtual-number pricing / GRE-form expectations; MIS shared. AI calling unpaid, Meta verification pending."),
 4079157:("Moving slowly","Setup long done; onsite visit scheduled tomorrow to complete pending trainings, then handover."),
 4337048:("Moving","Portal/IVR + admin training done; inventory file received. Finish inventory upload + bulk lead."),
 4299438:("Stalled","Most tasks done; bulk lead + FB pending on customer since ~14-Jun. Chase or flag HOLD."),
 4255693:("Stalled","Lead import with client, hierarchy approval + inventory pending; Meta/WA call rescheduled at client request. Chase."),
 3575524:("STUCK","Voora: pending client doc review + external handover since Feb. Sanket to call MD, align visit."),
 3623014:("STUCK","Escalated, OB on Pause - POC unresponsive. Escalate to sales or move to HOLD."),
 3304063:("Moving slowly","Shree Honda: DND/NDNC received, Mcube setup next. Confirm setup + push to signup."),
 3304062:("Moving slowly","Shree Automotive: DND/NDNC received, Mcube setup next. Confirm setup + push to signup."),
 3302998:("Customer-blocked","Times: unit UAT with client; awaiting UAT feedback + FM app approval. Set UAT deadline."),
}
_by={r["id"]:r for r in recs}
for i in F["stages"]["Pending on Customer"]:
    r=_by[i]
    if not r.get("pending_verdict"):
        v=PEND_DEFAULT.get(i,("Unknown","Owner to log status + next step immediately."))
        r["pending_verdict"],r["pending_action"]=v

# owner_gaps
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

OUT={
 "report_date":RUN,
 "run_label":"Run 6 (Tue 07-Jul-2026, refreshed) vs 02-Jul & 29-Jun",
 "run_index":6,
 "pipeline_id":27474,
 "pipeline_name":"Sell.do Onboarding Pipeline",
 "owner_gaps":owner_gaps,
 "deals":recs,
}
json.dump(OUT,open(os.path.join(BASE,"current_data.json"),"w"),indent=1)
print("assembled",len(recs),"deals")
print("stages:",{k:len(v) for k,v in F["stages"].items()})
print("new deals:",[r["id"] for r in recs if r["id"] not in pby])
print("dropped:",[i for i in pby if i not in set(ids)])
print("idle:",{b:sum(1 for r in recs if r["idle"]==b) for b in ["<=5 d","5-7 d","7-15 d"]})
print("no_task:",sum(1 for r in recs if r["no_task"]),"overdue_task:",sum(1 for r in recs if r["overdue_task"]),"no_notes:",sum(1 for r in recs if r["no_notes"]))
