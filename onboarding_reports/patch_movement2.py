#!/usr/bin/env python3
import json, os, datetime
BASE=os.path.dirname(os.path.abspath(__file__))
run_dt=datetime.date(2026,7,10)
cur=json.load(open(os.path.join(BASE,"current_data.json")))
prev=json.load(open(os.path.join(BASE,"snapshot_2026-07-07.json")))
pby={r["id"]:r for r in prev["deals"]}
by={r["id"]:r for r in cur["deals"]}

# corrected latest notes (id -> [epoch, gist]) from size-10 re-fetch
corrected={
 4386888:[1783311997012,"Completed incl website; client applied Meta Business verification, expected today."],
 4364225:[1783310237607,"Completed incl Admin Training, Offline Dialer, Sales training; Pending Bulk Lead Import."],
 4345401:[1782890459591,"Client to update re new WhatsApp number & bulk lead import."],
 4370376:[1783311043276,"Completed incl Offline Dialer; Pending Website Integration (initiated)."],
 4336926:[1783307979846,"Completed user/project/report/routing; Pending Bulk Lead (sample shared) + Website (awaiting dev email)."],
 4313304:[1783240871585,"Completed incl Property Portal, Website, Routing, MCube; low usage/IRIS watched."],
 4204921:[1783398960110,"Awaiting customer update on cost sheet; handover call to be scheduled this week."],
 4079157:[1782818965559,"Client to check team availability and confirm day for onsite visit."],
 3968505:[1783495624878,"GRE-form feedback expected to deploy today EOD; will share with customer after testing."],
 3623014:[1782129671917,"Escalated account, Onboarding on Pause as POC unresponsive."],
 3575524:[1783403866770,"Follow-up with AM team on new tasks; plan handover post EPR docs confirmation."],
 3417644:[1783421951079,"Completed: user activation, fresh lead import, report config, pipeline stages, revised sales training, custom sales dashboard; 99acres listing IDs requested."],
 3302998:[1782126824374,"Unit data uploaded to demo, dashboards ready; client UAT, feedback due 23 Jun EOD."],
}
def note_date(ep):
    if ep is None: return None
    d=datetime.datetime(1970,1,1)+datetime.timedelta(milliseconds=ep+19800000)
    return d.strftime("%Y-%m-%d")
def cadence_of(ds):
    if ds is None: return "No note"
    if ds<=5: return "OK (<=5d)"
    if ds<=10: return "Watch"
    return "Stale"
def set_note(r,ep,txt):
    r["last_note_epoch"]=ep; nd=note_date(ep); r["last_note_date"]=nd
    r["last_note_text"]=txt
    r["dsince"]=None if nd is None else (run_dt-datetime.date(*map(int,nd.split("-")))).days
    r["cadence"]=cadence_of(r["dsince"])

for i,(ep,txt) in corrected.items():
    if i in by: set_note(by[i],ep,txt)

# If our captured note is OLDER than prior run's, we missed the newest note -> carry prior note forward
for i,r in by.items():
    p=pby.get(i)
    if not p: continue
    ce=r.get("last_note_epoch"); pe=p.get("last_note_epoch")
    if ce is not None and pe is not None and ce<pe:
        set_note(r,pe,p.get("last_note_text",""))

# Movement verdicts for the 43 REVIEW deals: id -> (verdict, reason, streak)
V={
 4458749:("Progressed","Dialer + sales training now completed (were pending); Meta call still Monday.",0),
 4453288:("Progressed","Lead import completed; Meta integration call scheduled 9th.",0),
 4446753:("Progressed","Mcube resolved; only inventory + WhatsApp number now pending on customer (file due EOD).",0),
 4438366:("Progressed","Meta integration now live (lead #215 captured).",0),
 4435090:("Progressed","Project file imported (was pending); duplicate-lead-storage requirement raised with dev.",0),
 4411978:("Same-blocker","Same completed set; website integration still the open gap.",1),
 4402389:("Progressed","AI-calling feedback received (was awaited); only WhatsApp template dump now pending on customer.",0),
 4402374:("Progressed","Sales training completed; admin training to be scheduled next week.",0),
 4389699:("Same-blocker","WhatsApp (Interakt) + IVR (Airtel) still pending, now blocked on our end.",1),
 4389674:("Same-blocker","CAPI integration still pending; only a Monday meeting scheduled.",1),
 4386888:("Same-blocker","No new note since last run; Meta Business verification still awaited.",1),
 4383383:("Same-blocker","Website & Meta integration still pending; only a call scheduled.",1),
 4382895:("Same-blocker","No task newly completed; website pending, admin training only scheduled.",2),
 4375201:("Progressed","Inventories uploaded, clock-in/out & native WhatsApp now completed.",0),
 4370376:("Same-blocker","No new note since last run; website integration still the sole open task.",4),
 4370308:("Progressed","Sales training completed; Meta not required, WhatsApp reuse in progress.",0),
 4364225:("Same-blocker","No new note since last run; bulk lead import still pending.",1),
 4358959:("Progressed","Near handover; customer raised new lead-import & website-integration asks (details due EOD).",0),
 4357637:("Progressed","Workflow-clarity calls completed with client; sales training scheduled Friday.",0),
 4357586:("Same-blocker","Same status: Meta leads blocked on bad date/stage format; website discussion ongoing.",1),
 4345401:("Same-blocker","No new note since last run; WhatsApp number & bulk lead still pending on customer.",1),
 4337048:("Progressed","Meta, 99Acres, CommonFloor, CP form & trainings completed; WhatsApp call today.",0),
 4336926:("Same-blocker","No new note since last run; bulk lead + website still pending.",1),
 4325921:("Same-blocker","Near handover but nothing newly completed; only requesting admin-training slots.",2),
 4313304:("Same-blocker","No new note since last run; low usage / IRIS issue persists.",2),
 4299438:("Same-blocker","Bulk lead + Facebook still pending on customer, unchanged.",6),
 4255693:("Same-blocker","Still customer-blocked (lead/hierarchy/inventory); project-plan rework pending.",6),
 4255681:("Same-blocker","Client still holding implementation until calling integration done.",6),
 4241966:("Progressed","Explainer call completed; new ask to connect calls with Highrise CRM (feasibility check).",0),
 4233760:("Progressed","AI-calling feedback implemented & tested; awaiting customer confirmation.",0),
 4233715:("Same-blocker","Same bulk-outgoing-call issue; 7-Jul call rescheduled again.",6),
 4230613:("Progressed","Client escalation meeting held (CEO + Siddharth); rollout-timeline concerns & onsite ask raised.",0),
 4204921:("Same-blocker","Still awaiting customer cost-sheet feedback; handover call not yet held.",2),
 4177642:("Same-blocker","No new note since last run; WhatsApp / post-sales re-OB still pending on client details.",2),
 4147287:("Progressed","Channel-partner data imported; now awaiting WhatsApp workflow + inventory from customer.",0),
 4144089:("Same-blocker","Same GRE-form / post-sales dispute; Ankur + customer call again today.",6),
 4079157:("Same-blocker","No new note since last run; onsite training visit still not scheduled.",1),
 3968505:("Same-blocker","Same GRE-form JIRA deploy blocker, only day-shifted.",6),
 3623014:("Same-blocker","OB still on pause; POC unresponsive.",6),
 3575524:("Same-blocker","Still awaiting EPR docs / external handover; long-stalled.",6),
 3417644:("Progressed","Fresh note: revised sales training + custom sales dashboard completed; 99acres listing IDs requested.",0),
 3304062:("Same-blocker","Mcube setup still not done; only a re-initiation meeting scheduled.",2),
 3302998:("Same-blocker","Still awaiting client UAT feedback on inventory; no movement since June.",6),
}
for i,(v,rs,ss) in V.items():
    r=by[i]; r["movement_verdict"]=v; r["movement_reason"]=rs; r["stuck_streak"]=ss

json.dump(cur,open(os.path.join(BASE,"current_data.json"),"w"),indent=1)

# summary
from collections import Counter
c=Counter(r.get("movement_verdict") for r in cur["deals"])
sr=[r for r in cur["deals"] if r.get("stuck_streak",0)>=2]
print("verdict counts:",dict(c))
prog=sum(1 for r in cur['deals'] if r['movement_verdict']=='Progressed')
stuck=sum(1 for r in cur['deals'] if r['movement_verdict'] in ('Same-blocker','No-touch'))
new=sum(1 for r in cur['deals'] if r['movement_verdict']=='NEW')
print("progressed:",prog,"stuck:",stuck,"new:",new,"total:",len(cur['deals']))
print("SUPER-RED (>=2):",len(sr))
for r in sorted(sr,key=lambda x:-x['stuck_streak']):
    print("  x%d %s (%s) - %s"%(r['stuck_streak'],r['name'],r['stage'],r['movement_reason']))
# overdue go-live count
og=sum(1 for r in cur['deals'] if r.get('overdue_golive'))
print("overdue go-live:",og)
