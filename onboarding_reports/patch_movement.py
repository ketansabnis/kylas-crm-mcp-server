import json, os
BASE=os.path.dirname(os.path.abspath(__file__))
d=json.load(open(os.path.join(BASE,"current_data.json")))
V={
 4255693:("Progressed",0,"Multiple items completed (WhatsApp templates, hierarchy, inventory, booking form, cost sheets, payment schedule); only trainings left."),
 4472721:("Progressed",0,"Inventory follow-up completed; admin training slipped on client hardware issue."),
 4457232:("Progressed",0,"Meta, 99acres, offline dialer and sales training (laptop+mobile) completed."),
 4430582:("Progressed",0,"Setup, routing, IVR, offline dialer, SV form and laptop sales training completed."),
 4412002:("Progressed",0,"Setup, Meta, inventory, bulk import, admin + mobile sales training completed."),
 4389674:("Progressed",0,"Facebook CAPI and usage check completed; handover doc in preparation."),
 4438366:("Progressed",0,"Native WhatsApp (the prior blocker) completed; trainings slipped to next week."),
 4479594:("Progressed",0,"Sales and admin training both completed; Meta/WA on hold on client Meta account."),
 4478489:("Progressed",0,"Lead import completed; native WhatsApp awaiting client number."),
 4458771:("Progressed",0,"Facebook and SV form completed; sales training scheduled Wed."),
 4458766:("Progressed",0,"Admin training completed, account live in OB, handover planned this week."),
 4458749:("Progressed",0,"Handover and Q&A completed, account live - effectively wrapped."),
 4531331:("Progressed",0,"Core setup (users/projects/reports/routing) completed; trainings pending."),
 4511483:("Progressed",0,"Users/projects/reports/99acres/MagicBricks completed; lead import waiting on customer."),
 4510268:("Progressed",0,"First note logged; users/projects/reports completed; Meta+website upcoming."),
 4510245:("Progressed",0,"Account/team setup completed (1 user pending activation); integrations pending client."),
 4510214:("Progressed",0,"Core setup, routing, lead import, website, inventory completed; Mcube awaiting vendor."),
 4480069:("Progressed",0,"99 Acres property portal integration completed."),
 4299438:("Same-blocker",9,"Moved into Pending; transactional email still broken, sales training still deferred behind it."),
 4255681:("Same-blocker",9,"Calling-integration blocker persists; now escalated to Ketan - escalation is not resolution."),
 4233715:("Same-blocker",9,"AI-calling still blocked (ESTATE-21040 / SS-12176); only a call being scheduled."),
 4144089:("Same-blocker",9,"Refund/churn risk deepening; customer refuses AI-calling, wants unavailable sourcing changes."),
 3575524:("Same-blocker",9,"Same blockers: balance payment + Manoj's pointers, still awaited."),
 4177642:("Same-blocker",5,"Owner states nothing moved this week; escalated to sales."),
 4389699:("Same-blocker",4,"WhatsApp Interakt still pending on dev; trainings only scheduled, not done."),
 4370391:("Same-blocker",4,"Moved into Pending; inventory-layout demo slipped (client unavailable)."),
 4345401:("Same-blocker",4,"Moved into Pending; on-hold email sent; sales training only assured for Monday."),
 4402389:("Same-blocker",3,"No progress - customer POC on sick leave; all items pushed to next week."),
 4402374:("Same-blocker",3,"Admin training still only being scheduled a week later - scheduled != done."),
 4375201:("Same-blocker",3,"Mcube still blocked (recordings not captured); raised to vendor, client waiting."),
 4370308:("Same-blocker",3,"Admin training restated as awaiting customer availability - same ask."),
 4241966:("Same-blocker",3,"Still only arranging a call; AI-calling adoption not started."),
 4233760:("Same-blocker",3,"Still awaiting BOT feedback/adoption; now via a new POC (SS-12285)."),
 4479599:("Same-blocker",2,"Still in Kickoff Done; core setup gated on website + lead import; fancy number is a side item."),
 4449587:("Same-blocker",2,"Moved into Pending; AiSensy + inventory + cost sheet all awaited from client."),
 4435090:("Same-blocker",2,"Owner notes little concrete movement; trainings pending client availability."),
 4336926:("Same-blocker",2,"Account already live last week; only Facebook added; moved into Pending with hold threat."),
 3968505:("Same-blocker",2,"Still awaiting Sourcing rework from dev (ETA 29 Jul); customer un-progressed."),
 4482302:("Same-blocker",1,"Only a next-week plan (lead import 20th, training, IVR follow-up); nothing completed this week."),
 4482197:("Same-blocker",1,"Sales training rescheduled again on client unavailability - repeat slip."),
 4446753:("Same-blocker",1,"Restated: sales training done last week, onsite Wed, still awaiting WhatsApp number."),
}
by={r["id"]:r for r in d["deals"]}
miss=[i for i in V if i not in by]
assert not miss, miss
for i,(v,s,reason) in V.items():
    r=by[i]; r["movement_verdict"]=v; r["stuck_streak"]=s; r["movement_reason"]=reason
json.dump(d,open(os.path.join(BASE,"current_data.json"),"w"),indent=1)
from collections import Counter
print("verdicts:",dict(Counter(r["movement_verdict"] for r in d["deals"])))
sr=[r for r in d["deals"] if r["stuck_streak"]>=2 and "test" not in r["name"].lower()]
print("SUPER-RED (streak>=2, excl test):",len(sr))
for r in sorted(sr,key=lambda x:-x["stuck_streak"]):
    print(" ",r["stuck_streak"],r["id"],r["name"][:30],"|",r["owner"],"|",r["stage"])
