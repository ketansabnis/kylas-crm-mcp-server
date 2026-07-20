#!/usr/bin/env python3
"""Deterministic pre-classification of movement vs the previous run.

Usage: python compare.py --data current_data.json --outdir <reports_dir> --date YYYY-MM-DD

What it does
------------
- Loads the most recent prior snapshot in <reports_dir>.
- Sets movement_verdict for the cases that can be decided WITHOUT judgement.
- Flags the rest as REVIEW so the agent reads note_prev vs note_now.

Three rules encoded here that were learned the hard way (see SKILL.md "Pitfalls"):

1. STALE-NOTE RULE. A note whose date is on/before the PREVIOUS run's report date is
   not evidence of activity - it just means we finally paginated deep enough to see it.
   No stage change + newest note predates the last run  =>  "No-activity" (stuck), NOT REVIEW.

2. RESTATED-NOTE RULE. Owners re-paste the same "Completed Tasks / Pending Tasks" block
   every week. A new note with >=0.80 text similarity to the previous note is note theatre.
   It is still sent to REVIEW, but pre-tagged `restated:true` with a suggested Same-blocker
   verdict, so the default is "stuck unless proven otherwise".

3. STAGE-FLIP RULE. Moving INTO "Pending on Customer" / "On Hold" is not progress.
"""
import json, argparse, glob, os, re, datetime
from difflib import SequenceMatcher

RANK={"Open":1,"Kickoff Done":2,"Onboarding In Progress":3,"Pending on Customer":3,
      "Under Usage Tracking":4,"Handover Complete":5,"On Hold":0,"Churn":0}
RESTATE_THRESHOLD=0.80

ap=argparse.ArgumentParser()
ap.add_argument("--data",required=True); ap.add_argument("--outdir",required=True); ap.add_argument("--date",required=True)
A=ap.parse_args()

def norm(t):
    t=(t or "").lower().replace("&nbsp;"," ")
    t=re.sub(r"[^a-z0-9 ]+"," ",t)
    return re.sub(r"\s+"," ",t).strip()

def sim(a,b):
    a,b=norm(a),norm(b)
    if not a or not b: return 0.0
    return SequenceMatcher(None,a,b).ratio()

cur=json.load(open(A.data)); recs=cur["deals"]
pri=sorted([p for p in glob.glob(os.path.join(A.outdir,"snapshot_*.json"))
            if os.path.basename(p)[9:19] < A.date])
if not pri:
    for r in recs:
        r["movement_verdict"]="BASELINE"; r["movement_reason"]="First run."; r["stuck_streak"]=0
    json.dump(cur,open(A.data,"w"),indent=1)
    print("BASELINE - no prior, nothing to compare."); raise SystemExit

prev=json.load(open(pri[-1])); pby={r["id"]:r for r in prev["deals"]}
PREV_RUN_DATE=prev.get("report_date") or os.path.basename(pri[-1])[9:19]

review=[]; auto={"NEW":0,"Progressed":0,"No-activity":0,"REVIEW":0}
for r in recs:
    i=r["id"]; p=pby.get(i)
    if not p:
        r["movement_verdict"]="NEW"; r["movement_reason"]="New in pipeline this run."
        r["stuck_streak"]=0; r["restated"]=False; auto["NEW"]+=1; continue

    prev_streak=p.get("stuck_streak",0)
    stage_changed = r["stage"]!=p["stage"]
    forward = stage_changed and RANK.get(r["stage"],3) > RANK.get(p["stage"],3)
    new_note = r.get("last_note_epoch")!=p.get("last_note_epoch")
    nd=r.get("last_note_date")
    # Rule 1: newest note predates (or equals) the last run => nothing happened since
    note_is_stale = (nd is None) or (nd <= PREV_RUN_DATE)
    # Rule 2: similarity is measured on the RAW note text, never on our own gist
    s=sim(p.get("last_note_raw") or p.get("last_note_text"),
          r.get("last_note_raw") or r.get("last_note_text"))
    r["note_similarity"]=round(s,2)
    r["restated"]=bool(new_note and s>=RESTATE_THRESHOLD)

    if forward:
        r["movement_verdict"]="Progressed"
        r["movement_reason"]="Stage %s -> %s."%(p["stage"],r["stage"])
        r["stuck_streak"]=0; auto["Progressed"]+=1
    elif note_is_stale and not stage_changed:
        r["movement_verdict"]="No-activity"
        r["movement_reason"]="No note after %s (last run) and no stage change - nothing happened since the last review."%PREV_RUN_DATE
        r["stuck_streak"]=prev_streak+1; auto["No-activity"]+=1
    else:
        r["movement_verdict"]="REVIEW"; r["movement_reason"]=""
        r["stuck_streak"]=prev_streak; auto["REVIEW"]+=1
        review.append({
            "id":i,"name":r["name"],"owner":r["owner"],
            "stage_prev":p["stage"],"stage_now":r["stage"],
            "note_prev_date":p.get("last_note_date"),"note_now_date":nd,
            "note_prev":(p.get("last_note_text") or "")[:300],
            "note_now":(r.get("last_note_text") or "")[:300],
            "prev_streak":prev_streak,
            "restated":r["restated"],"similarity":round(s,2),
            "suggested":"Same-blocker (note restates the previous one - prove otherwise)" if r["restated"] else "read it",
        })

json.dump(cur,open(A.data,"w"),indent=1)
review.sort(key=lambda d:(not d["restated"], -d["prev_streak"]))
print("Deterministic pass: %s"%auto)
print("Prev run date used for the stale-note rule: %s"%PREV_RUN_DATE)
print("\n%d deal(s) need qualitative REVIEW (restated-first):"%len(review))
print(json.dumps(review,indent=1))
