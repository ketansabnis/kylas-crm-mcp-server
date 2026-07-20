#!/usr/bin/env python3
"""Deep-dive layer on top of the standard onboarding review.

Usage:
  python analyze_deep.py --data current_data.json --outdir <reports_dir> --date YYYY-MM-DD
                         [--jira jira_status.json]

Reads current_data.json (post-qualitative), the prior snapshots, and (optionally) the
live JIRA statuses the agent fetched, then:

  1. Appends 3 sheets to Onboarding_Pipeline_Review_<date>.xlsx:
       10. Reality Check (JIRA)      - what we tell the customer vs what the ticket says
       11. Who's Really Blocking     - customer / us-tech / us-commercial / vendor / owner-inaction
       12. Escalation & Risk Register- refund, legal, hold, churn, unhappy - and what happened since
  2. Writes deep_analysis_<date>.json (all computed numbers, so the narrative can't drift from data)
  3. Writes Onboarding_Deep_Dive_<date>.md - a scaffold with every number pre-filled and a
     paste-ready group message the agent finishes qualitatively.

Test deals (name contains 'test') are EXCLUDED from every statistic. They are not real work.
"""
import json, argparse, glob, os, re, datetime
from collections import Counter, defaultdict

ap=argparse.ArgumentParser()
ap.add_argument("--data",required=True); ap.add_argument("--outdir",required=True); ap.add_argument("--date",required=True)
ap.add_argument("--jira",default=None)
A=ap.parse_args()

CUR=json.load(open(A.data))
ALL=CUR["deals"]
D=[r for r in ALL if "test" not in (r["name"] or "").lower()]
TESTS=[r for r in ALL if r not in D]
BY={r["id"]:r for r in D}
JIRA=json.load(open(A.jira)) if (A.jira and os.path.exists(A.jira)) else {}

_pri=sorted([p for p in glob.glob(os.path.join(A.outdir,"snapshot_*.json"))
             if os.path.basename(p)[9:19] < A.date])
PRIORS=[json.load(open(p)) for p in _pri]
PREV=PRIORS[-1] if PRIORS else None

STUCK=lambda r: r["movement_verdict"] in ("Same-blocker","No-touch","No-activity")
SR=[r for r in D if r.get("stuck_streak",0)>=2]

# ---------------------------------------------------------------- 1. JIRA reality check
JIRA_RE=re.compile(r"\b([A-Z]{2,10}-\d{2,6})\b")
def keys_for(r):
    ks=list(r.get("jira_keys") or [])
    ks+= JIRA_RE.findall(((r.get("last_note_raw") or "")+" "+(r.get("last_note_text") or "")).upper())
    return sorted(set(ks))

DONEISH={"done","won't fix","wont fix","closed","released","cancelled","duplicate"}
def jira_flag(j, deal_stuck):
    """Classify a cited ticket against what the deal note implies."""
    st=(j.get("status") or "").strip(); low=st.lower()
    upd=j.get("updated") or ""
    try:
        stale_days=(datetime.date.fromisoformat(A.date)-datetime.date.fromisoformat(upd[:10])).days
    except Exception:
        stale_days=None
    if low in DONEISH and deal_stuck:
        sev="GHOST DEPENDENCY"
        why="Ticket is %s - the deal is still being held against a dependency that is closed. Customer is waiting for nothing."%st
    elif any(k in low for k in ("qa ","clarification","tech discussion","blocked","on hold","backlog")):
        sev="STUCK IN OUR QUEUE"
        why="Ticket sits in '%s' - this is our bottleneck, not the customer's."%st
    elif stale_days is not None and stale_days>14 and low not in DONEISH:
        sev="STALE TICKET"
        why="No update for %d days. The customer is being told it is in progress."%stale_days
    else:
        sev="OK"; why="Open and being worked (%s)."%st
    return sev, why, stale_days

reality=[]
for r in D:
    for k in keys_for(r):
        j=JIRA.get(k)
        if not j:
            reality.append({"deal":r["name"],"owner":r["owner"],"key":k,"severity":"NOT CHECKED",
                            "status":"-","fix":"-","updated":"-","stuck_streak":r.get("stuck_streak",0),
                            "note":(r.get("last_note_text") or "")[:120],
                            "why":"Ticket cited in the note but not fetched. Fetch it - this is where the lies hide."})
            continue
        sev,why,sd=jira_flag(j, STUCK(r))
        reality.append({"deal":r["name"],"owner":r["owner"],"key":k,"severity":sev,
                        "status":j.get("status","-"),"fix":j.get("fixVersion","-"),
                        "updated":(j.get("updated") or "-")[:10],"stuck_streak":r.get("stuck_streak",0),
                        "note":(r.get("last_note_text") or "")[:120],"why":why})
_sevrank={"GHOST DEPENDENCY":0,"STUCK IN OUR QUEUE":1,"STALE TICKET":2,"NOT CHECKED":3,"OK":4}
reality.sort(key=lambda x:(_sevrank.get(x["severity"],9), -x["stuck_streak"]))

# ---------------------------------------------------------------- 2. Who is really blocking
PAT={
 "US-COMMERCIAL": r"refund|legal|notice|false promise|not happy|unhappy|promised by sales|mis-?sold|escalat|discrepanc",
 "US-TECH":       r"jira|dev team|tech team|deployed|deployment|from our end|our side|bug|awaiting update from (the )?team|pending from our|in qa",
 "VENDOR":        r"mcube|interakt|wati|knowlarity|airtel|acefone|vendor|mailgun",
 "CUSTOMER":      (r"waiting (on|for)|awaiting|pending (from|on|with) (the )?(customer|client)|client (is )?(un)?available|"
                   r"no response|no movement from client|client will|client to|customer to|from (the )?(client|customer)'?s? end|"
                   r"no update from (the )?(client|customer)|client request|customer request|rescheduled"),
}
def blocker_owner(r):
    if r.get("blocker_owner"): return r["blocker_owner"]          # agent override wins
    t=(r.get("last_note_raw") or r.get("last_note_text") or "").lower()
    for cat in ("US-COMMERCIAL","US-TECH","VENDOR","CUSTOMER"):
        if re.search(PAT[cat],t): return cat
    if STUCK(r) and (r.get("no_task") or r["movement_verdict"]=="No-activity"): return "OWNER-INACTION"
    return "UNCLEAR"

for r in D: r["_blocker"]=blocker_owner(r)
blockmix=Counter(r["_blocker"] for r in D)
# the parking-lot check: parked in Pending-on-Customer but nobody is actually waiting on the customer
mislabelled=[r for r in D if r["stage"]=="Pending on Customer" and r["_blocker"] not in ("CUSTOMER","UNCLEAR")]
# and the inverse: blocked on us but NOT flagged as such anywhere
on_us=[r for r in D if r["_blocker"] in ("US-TECH","US-COMMERCIAL","VENDOR","OWNER-INACTION") and STUCK(r)]

# ---------------------------------------------------------------- 3. Escalation register
ESC=r"escalat|refund|legal|notice|not happy|unhappy|false promise|churn|on hold|pause[d]?\b|discrepanc"
def first_seen(i):
    """Earliest run whose note for this deal already contained escalation language."""
    for s in PRIORS:
        for r in s["deals"]:
            if r["id"]==i and re.search(ESC,((r.get("last_note_raw") or "")+" "+(r.get("last_note_text") or "")).lower()):
                return s["report_date"]
    return A.date
esc=[]
for r in D:
    t=((r.get("last_note_raw") or "")+" "+(r.get("last_note_text") or "")).lower()
    if re.search(ESC,t):
        fs=first_seen(r["id"])
        days=(datetime.date.fromisoformat(A.date)-datetime.date.fromisoformat(fs)).days
        esc.append({"id":r["id"],"name":r["name"],"owner":r["owner"],"stage":r["stage"],
                    "vband":r["vband"],"lic":r.get("lic"),"age":r["age"],
                    "streak":r.get("stuck_streak",0),"first_flagged":fs,"days_open":days,
                    "moved_since":"NO" if STUCK(r) else "yes",
                    "note":(r.get("last_note_text") or "")[:160]})
esc.sort(key=lambda e:(-e["days_open"],-e["streak"]))

# ---------------------------------------------------------------- 4. Owner scorecard (extended)
own=defaultdict(lambda:{"n":0,"prog":0,"stuck":0,"sr":0,"notask":0,"theatre":0,"old":0})
for r in D:
    o=own[r["owner"]]; o["n"]+=1
    if r["movement_verdict"]=="Progressed": o["prog"]+=1
    if STUCK(r): o["stuck"]+=1
    if r.get("stuck_streak",0)>=2: o["sr"]+=1
    if r.get("no_task"): o["notask"]+=1
    if r.get("restated"): o["theatre"]+=1
    if r["age"] in (">180 d","90-180 d","60-90 d"): o["old"]+=1
owners=sorted(own.items(), key=lambda kv:(-kv[1]["sr"], -kv[1]["stuck"]))

# ---------------------------------------------------------------- 5. Hygiene + trend
hyg={"deals":len(D),"tests_excluded":len(TESTS),
     "no_task":sum(1 for r in D if r.get("no_task")),
     "overdue_task":sum(1 for r in D if r.get("overdue_task")),
     "no_notes":[r["name"] for r in D if r.get("no_notes")],
     "no_billed":sum(1 for r in D if r["vband"]=="blank"),
     "overdue_golive":sum(1 for r in D if r.get("overdue_golive")),
     "stuck_and_no_task":[(r["name"],r["owner"]) for r in D if STUCK(r) and r.get("no_task")],
     "note_theatre":[(r["name"],r["owner"],r.get("note_similarity")) for r in D if r.get("restated")],
     "older_60d":sum(1 for r in D if r["age"] in (">180 d","90-180 d","60-90 d"))}
trend=[]
for s in PRIORS+[CUR]:
    dd=[r for r in s["deals"] if "test" not in (r["name"] or "").lower()]
    trend.append({"date":s["report_date"],"deals":len(dd),
                  "progressed":sum(1 for r in dd if r["movement_verdict"]=="Progressed"),
                  "stuck":sum(1 for r in dd if r["movement_verdict"] in ("Same-blocker","No-touch","No-activity")),
                  "superred":sum(1 for r in dd if r.get("stuck_streak",0)>=2)})

# blocker taxonomy across latest notes
TOPIC={"Trainings":r"training","Meta/Facebook":r"meta|facebook","WhatsApp":r"whatsapp|wati|interakt",
       "Bulk lead import":r"lead import|bulk lead","IVR/Mcube/dialer":r"mcube|ivr|dialer|knowlarity|airtel",
       "Website":r"website","Inventory":r"inventory","Portals":r"99acre|magic ?brick|housing|portal","Handover":r"handover|hand over"}
topics=Counter()
for r in D:
    t=(r.get("last_note_raw") or r.get("last_note_text") or "").lower()
    for k,p in TOPIC.items():
        if re.search(p,t): topics[k]+=1

OUT={"date":A.date,"headline":{"deals":len(D),
      "progressed":sum(1 for r in D if r["movement_verdict"]=="Progressed"),
      "stuck":sum(1 for r in D if STUCK(r)),
      "new":sum(1 for r in D if r["movement_verdict"]=="NEW"),
      "superred":len(SR),
      "superred_prev":sum(1 for r in (PREV["deals"] if PREV else []) if r.get("stuck_streak",0)>=2)},
     "trend":trend,"reality":reality,"blockmix":dict(blockmix),
     "mislabelled_pending":[(r["name"],r["_blocker"],r["owner"]) for r in mislabelled],
     "blocked_on_us":[(r["name"],r["_blocker"],r["owner"],r.get("stuck_streak",0)) for r in on_us],
     "escalations":esc,"owners":{k:v for k,v in owners},"hygiene":hyg,"topics":topics.most_common(),
     "superred":[(r["name"],r["owner"],r.get("stuck_streak"),r["vband"],r["age"],r.get("movement_reason","")) for r in
                 sorted(SR,key=lambda r:-r.get("stuck_streak",0))]}
json.dump(OUT,open(os.path.join(A.outdir,"deep_analysis_%s.json"%A.date),"w"),indent=1)

# ---------------------------------------------------------------- 6. Append sheets 10-12
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
XL=os.path.join(A.outdir,"Onboarding_Pipeline_Review_%s.xlsx"%A.date)
wb=load_workbook(XL)
thin=Side(style="thin",color="D9D9D9"); border=Border(thin,thin,thin,thin)
NAVY=PatternFill("solid",fgColor="1F3864")
hf=Font(name="Calibri",bold=True,color="FFFFFF",size=10)
red=PatternFill("solid",fgColor="F4CCCC"); amber=PatternFill("solid",fgColor="FCE5CD")
yellow=PatternFill("solid",fgColor="FFF2CC"); green=PatternFill("solid",fgColor="D9EAD3")
title=Font(name="Calibri",bold=True,size=15,color="1F3864"); sub=Font(name="Calibri",italic=True,size=9,color="666666")
reg=Font(name="Calibri",size=10)
FILL={"GHOST DEPENDENCY":red,"STUCK IN OUR QUEUE":amber,"STALE TICKET":yellow,"NOT CHECKED":yellow,"OK":green,
      "US-TECH":amber,"US-COMMERCIAL":red,"VENDOR":amber,"OWNER-INACTION":red,"CUSTOMER":green,"UNCLEAR":yellow}
def sheet(nm,hdrs,rows,widths,t,s_):
    if nm in wb.sheetnames: del wb[nm]      # idempotent: safe to re-run
    ws=wb.create_sheet(nm)
    ws["A1"]=t; ws["A1"].font=title; ws["A2"]=s_; ws["A2"].font=sub
    for c,h in enumerate(hdrs,1):
        x=ws.cell(row=4,column=c,value=h); x.font=hf; x.fill=NAVY; x.border=border
        x.alignment=Alignment(vertical="center",wrap_text=True)
    for i,row in enumerate(rows,5):
        for c,v in enumerate(row,1):
            x=ws.cell(row=i,column=c,value=v); x.font=reg; x.border=border
            x.alignment=Alignment(vertical="top",wrap_text=True)
        f=FILL.get(str(row[0]))
        if f: ws.cell(row=i,column=1).fill=f
    for c,w in enumerate(widths,1):
        ws.column_dimensions[chr(64+c)].width=w
    ws.freeze_panes="A5"
    return ws

sheet("10. Reality Check (JIRA)",
      ["Severity","Deal","Owner","Ticket","Live status","Fix ver","Last updated","Stuck runs","What the note tells the customer","Why it matters"],
      [[x["severity"],x["deal"],x["owner"],x["key"],x["status"],x["fix"],x["updated"],x["stuck_streak"],x["note"],x["why"]] for x in reality],
      [20,28,18,14,22,10,13,10,50,55],
      "Reality Check - JIRA cited in the note vs the live ticket",
      "GHOST DEPENDENCY = the ticket is closed/Won't Fix but the deal is still parked against it. Fix these first.")

sheet("11. Who's Really Blocking",
      ["Blocker","Deal","Owner","Stage","Stuck runs","Value","Age","Latest note"],
      [[r["_blocker"],r["name"],r["owner"],r["stage"],r.get("stuck_streak",0),r["vband"],r["age"],(r.get("last_note_text") or "")[:150]]
       for r in sorted(D,key=lambda r:({"US-COMMERCIAL":0,"OWNER-INACTION":1,"US-TECH":2,"VENDOR":3,"UNCLEAR":4,"CUSTOMER":5}.get(r["_blocker"],9),
                                        -r.get("stuck_streak",0)))],
      [18,30,18,22,10,10,10,70],
      "Who is really blocking each deal",
      "'Pending on Customer' with a non-CUSTOMER blocker = the stage is being used as a parking lot. %d such deals this run."%len(mislabelled))

sheet("12. Escalation & Risk Register",
      ["Blocker","Deal","Owner","Stage","Value","Licences","Age","Stuck runs","First flagged","Days open","Moved since?","Latest note"],
      [[BY[e["id"]]["_blocker"],e["name"],e["owner"],e["stage"],e["vband"],e["lic"],e["age"],e["streak"],
        e["first_flagged"],e["days_open"],e["moved_since"],e["note"]] for e in esc],
      [18,30,18,22,10,9,10,10,13,10,12,60],
      "Escalation & Risk Register",
      "Anything mentioning refund / legal / escalation / hold / unhappy. 'Moved since? = NO' means we logged the escalation and then did nothing.")
wb.save(XL)

# ---------------------------------------------------------------- 7. Deep-dive scaffold
h=OUT["headline"]
md=[]
md.append("# Onboarding Pipeline - Deep Dive & Major Concerns")
md.append("**%s - Kylas pipeline 27474 - %d live deals (%d test deals excluded)**\n"%(A.date,len(D),len(TESTS)))
md.append("## The headline\n")
md.append("**%d of %d deals (%d%%) did not genuinely move this run. %d have not moved for two or more consecutive reviews (was %d last run).**\n"
          %(h["stuck"],h["deals"],round(100*h["stuck"]/max(h["deals"],1)),h["superred"],h["superred_prev"]))
md.append("| Run | Open | Progressed | Stuck | SUPER-RED |\n|---|---|---|---|---|")
for t in trend[-5:]:
    md.append("| %s | %d | %d | %d | %d |"%(t["date"],t["deals"],t["progressed"],t["stuck"],t["superred"]))
md.append("\n## 1. Reality check - what we tell customers vs what the ticket says\n")
bad=[x for x in reality if x["severity"] in ("GHOST DEPENDENCY","STUCK IN OUR QUEUE","STALE TICKET","NOT CHECKED")]
if bad:
    md.append("| Deal | Note says | Ticket | Live status | Verdict |\n|---|---|---|---|---|")
    for x in bad[:12]:
        md.append("| **%s** (stuck %d) | %s | %s | **%s** | %s |"%(x["deal"],x["stuck_streak"],x["note"][:70],x["key"],x["status"],x["severity"]))
else:
    md.append("_No cited ticket contradicts its deal note this run._")
md.append("\n## 2. Who is really blocking\n")
md.append(" - ".join("**%s** %d"%(k,v) for k,v in sorted(blockmix.items(),key=lambda kv:-kv[1])))
md.append("\n**Parked in 'Pending on Customer' but the customer is not the blocker (%d):** %s\n"
          %(len(mislabelled), ", ".join("%s (%s)"%(r["name"],r["_blocker"]) for r in mislabelled) or "none"))
md.append("## 3. Escalation & commercial risk\n")
if esc:
    md.append("| Account | Value | Age | Stuck | Flagged since | Days | Moved since? |\n|---|---|---|---|---|---|---|")
    for e in esc[:12]:
        md.append("| **%s** | %s | %s | %d runs | %s | %d | **%s** |"%(e["name"],e["vband"],e["age"],e["streak"],e["first_flagged"],e["days_open"],e["moved_since"]))
md.append("\n## 4. Owner scorecard\n")
md.append("| Owner | Deals | Progressed | Stuck | SUPER-RED | No next task | Note theatre | >60d old |\n|---|---|---|---|---|---|---|---|")
for o,v in owners:
    md.append("| %s | %d | %d | %d | **%d** | %d | %d | %d |"%(o,v["n"],v["prog"],v["stuck"],v["sr"],v["notask"],v["theatre"],v["old"]))
md.append("\n## 5. Note theatre (same note re-pasted, zero delta)\n")
md.append(", ".join("**%s** (%s, %.0f%% identical)"%(n,o,(s or 0)*100) for n,o,s in hyg["note_theatre"]) or "_none_")
md.append("\n\n## 6. What the pipeline is actually stuck on\n")
md.append(" - ".join("**%s** %d"%(k,v) for k,v in OUT["topics"]))
md.append("\n\n## 7. CRM hygiene\n")
md.append("- **%d of %d deals have no next task.**\n- **%d have no billed amount** (cannot rank by revenue at risk).\n- %d overdue tasks, %d breached go-live dates, %d deals with zero notes.\n- **%d deals older than 60 days** still not live."
          %(hyg["no_task"],len(D),hyg["no_billed"],hyg["overdue_task"],hyg["overdue_golive"],len(hyg["no_notes"]),hyg["older_60d"]))
md.append("\n## SUPER-RED list\n")
md.append("| Account | Owner | Runs stuck | Value | Age | Why |\n|---|---|---|---|---|---|")
for n,o,s,v,a,why in OUT["superred"]:
    md.append("| %s | %s | %d | %s | %s | %s |"%(n,o,s,v,a,why[:80]))
md.append("\n---\n\n## The asks\n\n_[agent: 5 asks max, each with a named owner and a date]_\n")
md.append("## Paste-ready version for the group\n\n> _[agent: 3 concerns max, lead with the reality-check finding, name people only where the data is unambiguous]_\n")
MEMO=os.path.join(A.outdir,"Onboarding_Deep_Dive_%s.md"%A.date)
if os.path.exists(MEMO):
    # NEVER clobber a memo that has already been written/edited by a human.
    MEMO=os.path.join(A.outdir,"Onboarding_Deep_Dive_%s_scaffold.md"%A.date)
    print("  (memo already exists - scaffold written alongside it, not over it)")
open(MEMO,"w").write("\n".join(md))

print("Deep dive written -> %s"%os.path.basename(MEMO))
print("  headline:",h)
print("  JIRA flags:",Counter(x["severity"] for x in reality))
print("  blockers:",dict(blockmix))
print("  mislabelled Pending-on-Customer:",len(mislabelled))
print("  escalations:",len(esc))
print("  note theatre:",len(hyg["note_theatre"]))
