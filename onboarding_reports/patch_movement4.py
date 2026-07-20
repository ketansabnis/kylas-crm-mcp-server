#!/usr/bin/env python3
"""Apply qualitative movement verdicts for Run 9 (2026-07-16) REVIEW deals.
Rule applied: a 'This week: <plan>' note is intent, not completion -> Same-blocker.
Only an actually-completed task / cleared blocker -> Progressed."""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))
cur = json.load(open(os.path.join(BASE, "current_data.json")))
by = {r["id"]: r for r in cur["deals"]}

# id -> (verdict, reason, stuck_streak, blocker_owner_or_None)
V = {
 4299438: ("Same-blocker", "Still Mailgun/lead-capture pending; note is a 'this week' plan, no completion. Streak 8.", 8, "US-TECH"),
 4370376: ("Same-blocker", "Website gap dropped from note; admin training + handover only 'targeted this week' - not done. actualGoLive set with items open.", 6, "OWNER-INACTION"),
 4472721: ("Same-blocker", "Still waiting inventory from client; 'this week' plan restates the same ask.", 3, "CUSTOMER"),
 4457232: ("Same-blocker", "Same pending items (Meta, bulk lead) re-planned as 'this week'. No completion.", 3, "CUSTOMER"),
 4430582: ("Same-blocker", "Base setup still being followed up; bulk lead/Meta/website/WhatsApp all still pending. Plan note.", 3, "CUSTOMER"),
 4412002: ("Same-blocker", "Meta/training/handover all 'tentative this week'. Scheduled != done.", 3, "OWNER-INACTION"),
 4370391: ("Same-blocker", "Inventory demo 'agreed for Monday' last week has slipped to 'this week' again. Date slip = stuck.", 3, "CUSTOMER"),
 4345401: ("Same-blocker", "'No movement from client'; now threatening to put on hold. Moving toward hold is not progress.", 3, "CUSTOMER"),
 4402389: ("Same-blocker", "Hold-till-13-Jul deadline passed; follow-up slipped (owner unwell). Nothing the customer owed changed. Now SUPER-RED.", 2, "OWNER-INACTION"),
 4480069: ("Progressed", "Internal order-form blocker (dev booked as CP module) cleared; account setup now starting.", 0, None),
 4458771: ("Same-blocker", "Still waiting client to complete Meta & WhatsApp; 'this week' plan restates the ask.", 1, "CUSTOMER"),
 4449587: ("Same-blocker", "Active but note is a 'this week' plan (AiSensy + inventory/cost sheet), pending client details. No stated completion.", 1, "CUSTOMER"),
 4446753: ("Progressed", "Sales training completed since last note; onsite visit booked. Still awaiting WhatsApp number but a task actually closed.", 0, "CUSTOMER"),
 4336926: ("Same-blocker", "Account live but bulk lead + website still no client update; threatening hold. Restates prior.", 1, "CUSTOMER"),
}
for i, (v, why, ss, bo) in V.items():
    r = by[i]
    r["movement_verdict"] = v
    r["movement_reason"] = why
    r["stuck_streak"] = ss
    if bo: r["blocker_owner"] = bo

json.dump(cur, open(os.path.join(BASE, "current_data.json"), "w"), indent=1)
from collections import Counter
print("verdicts:", Counter(r["movement_verdict"] for r in cur["deals"]))
sr = [r for r in cur["deals"] if r["stuck_streak"] >= 2 and "test" not in r["name"].lower()]
print("SUPER-RED (streak>=2):", len(sr))
for r in sorted(sr, key=lambda x:-x["stuck_streak"]):
    print("  ss%-2d %-34s %-18s %s" % (r["stuck_streak"], r["name"][:34], r["owner"][:18], r["stage"]))
