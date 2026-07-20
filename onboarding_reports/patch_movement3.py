#!/usr/bin/env python3
import json, os
BASE=os.path.dirname(os.path.abspath(__file__))
cur=json.load(open(os.path.join(BASE,"current_data.json")))
by={r["id"]:r for r in cur["deals"]}

# id -> (verdict, reason, stuck_streak)
V={
 # --- Progressed ---
 4482302:("Progressed","Website + Wati WhatsApp + Meta integrations all completed (were open at kickoff).",0),
 4479599:("Progressed","Account/user/report setup completed; now only lead-import data + website changes pending on client.",0),
 4480069:("Progressed","Moved Open -> Onboarding In Progress; blocked only on corrected Order Form from sales.",0),
 4479594:("Progressed","Moved Kickoff Done -> Onboarding In Progress; Meta + WhatsApp call booked for Tuesday.",0),
 4478489:("Progressed","Moved Open -> Onboarding In Progress; Meta integration live (lead #38).",0),
 4461524:("Progressed","Setup + trainings all completed; only handover feedback form outstanding.",0),
 4458771:("Progressed","User/project/report config completed (was only a task list last run); now waiting on client for Meta + WhatsApp.",0),
 4458766:("Progressed","Sales training completed (Meta was on hold last run); only admin training left.",0),
 4458749:("Progressed","All trainings completed; account moving to handover.",0),
 4449587:("Progressed","Portals (99Acres/India Residential), Meta, MCube IVR, admin training and LivServ chatbot all completed this run.",0),
 4446753:("Progressed","Inventory uploaded (was the blocker); only client's WhatsApp number outstanding.",0),
 4435090:("Progressed","Lead import completed; Meta + sales training now queued.",0),
 4411978:("Progressed","Admin training completed; account moving to handover (website gap cleared).",0),
 4382895:("Progressed","Q&A session completed; account moving to handover (admin training was the 2-run blocker).",0),
 4357637:("Progressed","Sales training completed (was scheduled last run); admin training this week.",0),
 4357586:("Progressed","All onboarding tasks now completed (lead-import/Meta data issues resolved); only handover feedback form left.",0),
 4337048:("Progressed","Inventory upload now in progress (file issues resolved); bulk lead + Knowlarity due from customer.",0),
 4336926:("Progressed","Sales/pre-sales training completed; bulk lead + website still pending on client.",0),
 4313304:("Progressed","Account handed over to support; only cost sheet outstanding.",0),
 4299438:("Progressed","Moved Pending on Customer -> Onboarding In Progress; tech working on Mailgun / lead-capture-form issues.",0),
 4079157:("Progressed","Onsite sales training completed; admin training being booked, then AM handover.",0),
 3968505:("Progressed","GRE form delivered to customer (was 'expected to deploy'); awaiting their sign-off.",0),

 # --- Same-blocker (note restates the same ask) ---
 4482197:("Same-blocker","Kick-off missed again (client unavailable on 10 Jul); still not held.",1),
 4453288:("Same-blocker","Client now wants sales training only after post-sales setup and owner is asking to put account on Hold - go-live not advanced.",1),
 4438366:("Same-blocker","Native WhatsApp still blocked on client's contact number; sales training still unscheduled.",1),
 4402389:("Same-blocker","Customer asked to hold till 13-Jul; pending WhatsApp template dump / AI details unchanged.",1),
 4370308:("Same-blocker","Admin training slipped from 'today' to 'next week' - same ask, no completion.",1),
 4375201:("Same-blocker","Client unavailable again; Mcube test and integrations still not started.",1),
 4241966:("Same-blocker","Still chasing Netram to run outgoing calls - same ask as last run.",1),
 4233760:("Same-blocker","Still awaiting flow + feedback from customer on the AI bot.",1),
 4147287:("Same-blocker","WhatsApp flow still 'to be shared by Monday'; still no update on inventory.",1),

 # --- Same-blocker, streak >= 2 (SUPER-RED) ---
 4472721:("Same-blocker","No note since 10-Jul; still waiting on inventory details from client.",2),
 4457232:("Same-blocker","Same completed set; bulk lead import / portal / Meta / WhatsApp still pending on client.",2),
 4430582:("Same-blocker","Same pending list (bulk lead import, Meta, website, WhatsApp) as last run.",2),
 4389699:("Same-blocker","Interakt WhatsApp + Airtel/Mcube IVR still pending from our end - same blocker.",2),
 4389674:("Same-blocker","Still waiting on client's Mcube setup; CAPI/admin unchanged.",2),
 4386888:("Same-blocker","Client's Meta business verification still not through - same blocker for 2 runs.",2),
 4364225:("Same-blocker","Bulk lead import still the only pending item, unchanged.",2),
 4370376:("Same-blocker","Website integration still the open gap - 5th consecutive run.",5),
 4255693:("Same-blocker","No note since 8-Jul; Q&A / mobile / admin 2.0 trainings still not done.",7),
 4255681:("Same-blocker","No note since 8-Jul; still blocked on calling integration + booking-form doc.",7),
 4233715:("Same-blocker","Outgoing-calling issues persist; JIRA ESTATE-21040 still open, no customer testing.",7),
 4177642:("Same-blocker","No note since 8-Jul; AI-calling demo, Mcube concern, admin plan and WhatsApp all still open.",3),
 4144089:("Same-blocker","Customer still unhappy vs sales promises; call on pending pointers still not held. Possible refund.",7),
 3623014:("Same-blocker","Refund legal-notice case (Amit Tare); no onboarding movement - should leave the pipeline.",7),
 3302998:("Same-blocker","Client-reported data discrepancies unresolved; review meeting rescheduled again.",7),
}
for i,(v,reason,streak) in V.items():
    r=by[i]; r["movement_verdict"]=v; r["movement_reason"]=reason; r["stuck_streak"]=streak

# No-touch / NEW already set by compare.py; add reasons where blank
NT={
 4491940:"No notes at all since the deal was created (Open).",
 4481260:"No note since 10-Jul - 'no response to calls'.",
 4402374:"No note since 10-Jul; admin training still to be scheduled.",
 4230613:"No note since 7-Jul; client escalation on rollout timelines still open.",
 3304063:"No note since 7-Jul; awaiting outcome of the 8-Jul re-initiation meeting.",
 3304062:"No note since 7-Jul; awaiting outcome of the 8-Jul re-initiation meeting.",
 3575524:"No note since 7-Jul; EPR docs + external handover still pending.",
}
for i,reason in NT.items():
    r=by[i]
    if not r.get("movement_reason"): r["movement_reason"]=reason

json.dump(cur,open(os.path.join(BASE,"current_data.json"),"w"),indent=1)
from collections import Counter
c=Counter(r["movement_verdict"] for r in cur["deals"])
print(dict(c))
sr=[(r["id"],r["name"],r["stuck_streak"],r["owner"]) for r in cur["deals"] if r["stuck_streak"]>=2]
print("SUPER-RED:",len(sr))
for x in sorted(sr,key=lambda t:-t[2]): print("  ",x)
