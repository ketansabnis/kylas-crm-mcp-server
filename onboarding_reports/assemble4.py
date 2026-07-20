#!/usr/bin/env python3
"""Assemble fresh_2026-07-16.json + current_data.json from the merged deal_fields
and notes pulls (Run 9, Thu 16-Jul-2026)."""
import json, os, glob, datetime
BASE = os.path.dirname(os.path.abspath(__file__))
RUN = "2026-07-16"
run_dt = datetime.date(2026, 7, 16)

# ---- merge pulled files ----
DF = {}
for p in sorted(glob.glob(os.path.join(BASE, "deal_fields_2026-07-16_*.json"))):
    DF.update(json.load(open(p)))
NT = {}
for p in sorted(glob.glob(os.path.join(BASE, "notes_2026-07-16_*.json"))):
    NT.update(json.load(open(p)))
DF = {int(k): v for k, v in DF.items()}
NT = {int(k): v for k, v in NT.items()}
ids = list(DF.keys())

PRIOR = json.load(open(os.path.join(BASE, "snapshot_2026-07-13.json")))
pby = {r["id"]: r for r in PRIOR["deals"]}

# ---- membership sets from live search_entity (Step 1.8 / 1.3) ----
overdue_task = {4458749,4402389,4402374,4389699,4389674,4375201,4370308,4357637,4337048,4241966,4233760,4230613,4177642,4147287,4144089,3575524,3302998}
future_task  = {4531331,4482302,4479599,4458771,4435090,4269153}
idle5 = {4499510,4494717,4491940,4479594,4475303,4475289,4255693,4230613,4177642,3968505,3304063,3304062,3302998}
idle7 = {4491940,4479594,4475303,4475289,4255693,4230613,4177642,3304063,3304062}
idle15 = set()

def dparse(s):
    if not s: return None
    try: return datetime.date.fromisoformat(str(s)[:10])
    except Exception: return None

def age_band(created):
    d = dparse(created)
    if not d: return "<14 d"
    days = (run_dt - d).days
    if days < 14: return "<14 d"
    if days < 30: return "14-30 d"
    if days < 60: return "30-60 d"
    if days < 90: return "60-90 d"
    if days < 180: return "90-180 d"
    return ">180 d"

def vband_of(billed):
    b = billed or 0
    if b >= 1000000: return ">=10L"
    if b >= 700000: return "7-10L"
    if b >= 500000: return "5-7L"
    if b >= 300000: return "3-5L"
    if b >= 200000: return "2-3L"
    if b >= 100000: return "1-2L"
    return "blank"

def lband_of(lic):
    l = lic or 0
    if l >= 50: return ">=50"
    if l >= 20: return "20-49"
    if l >= 10: return "10-19"
    return "<10/blank"

def idle_bucket(i):
    if i in idle15: return "7-15 d"   # kept for schema compatibility
    if i in idle7: return "7-15 d"
    if i in idle5: return "5-7 d"
    return "<=5 d"

def note_date(ep):
    if ep is None: return None
    return (datetime.datetime(1970,1,1)+datetime.timedelta(milliseconds=ep+19800000)).strftime("%Y-%m-%d")

def cadence_of(ds):
    if ds is None: return "No note"
    if ds <= 5: return "OK (<=5d)"
    if ds <= 10: return "Watch"
    return "Stale"

CAT_MAP = {"A":"A","B":"B","C":"C","Broker":"Broker","Push to OB":"Push to OB"}

recs = []
for i in ids:
    d = DF[i]; p = pby.get(i)
    ep, raw, gist, jira = (NT.get(i) or [None,"","",[]])
    nd = note_date(ep)
    ds = None if nd is None else (run_dt - dparse(nd)).days
    billed = d.get("billed"); recv = d.get("recv"); lic = d.get("licences")
    cat = CAT_MAP.get(d.get("category"), "(none)")
    high = bool((billed and billed >= 300000) or (lic and lic >= 30))
    golive_overdue = bool(dparse(d.get("targetGoLive")) and dparse(d.get("targetGoLive")) < run_dt)
    not_su = (d.get("activation") == "Yet to sign up")
    recs.append({
        "id": i, "name": d["name"], "owner": d["owner"], "stage": d["stage"],
        "age": age_band(d.get("created")), "idle": idle_bucket(i),
        "last_note_epoch": ep, "last_note_date": nd,
        "last_note_raw": (raw or "")[:300], "last_note_text": gist or "",
        "jira_keys": jira or [],
        "dsince": ds, "cadence": cadence_of(ds),
        "overdue_golive": golive_overdue, "not_signedup": not_su,
        "no_task": (i not in overdue_task) and (i not in future_task),
        "overdue_task": i in overdue_task, "no_notes": ep is None,
        "category": cat,
        "suggested": (p.get("suggested") if p else (cat if cat not in ("(none)","Push to OB") else "C")),
        "gflag": (p.get("gflag") if p else "OK"),
        "greason": (p.get("greason") if p else "new deal this run"),
        "vband": vband_of(billed), "lband": lband_of(lic),
        "brand": (p.get("brand") if p else ""),
        "billed": billed, "recv": recv, "lic": lic, "high_value": high,
        "nstep": (p.get("nstep") if p else "Log first note + confirm kickoff / next milestone."),
        "pending_verdict": (p.get("pending_verdict","") if p else ""),
        "pending_action": (p.get("pending_action","") if p else ""),
        "blocker_owner": (p.get("blocker_owner") if p else None),
        "movement_verdict": "BASELINE", "movement_reason": "", "stuck_streak": 0,
    })

# pending-on-customer default verdicts (carry prior; new ones = Unknown)
_by = {r["id"]: r for r in recs}
for r in recs:
    if r["stage"] == "Pending on Customer" and not r.get("pending_verdict"):
        r["pending_verdict"], r["pending_action"] = ("Unknown", "Owner to log status + next step immediately.")

# owner gaps
from collections import defaultdict
og = defaultdict(lambda: {"n":0,"nonotes":[],"pending":[]})
for r in recs:
    o = r["owner"]; og[o]["n"] += 1
    if r["no_notes"]: og[o]["nonotes"].append(r["name"])
    if r["stage"] == "Pending on Customer": og[o]["pending"].append(r["name"])
owner_gaps = {}
for o, dd in sorted(og.items(), key=lambda kv:-kv[1]["n"]):
    parts = [f"{dd['n']} deal(s)."]
    if dd["nonotes"]: parts.append("no notes: "+", ".join(dd["nonotes"][:6])+".")
    if dd["pending"]: parts.append("pending-on-customer: "+", ".join(dd["pending"][:6])+".")
    owner_gaps[o] = " ".join(parts)

# stages membership for fresh.json + sanity
stages = defaultdict(list)
for r in recs: stages[r["stage"]].append(r["id"])
for st in ["Open","Kickoff Done","Onboarding In Progress","Pending on Customer","Under Usage Tracking"]:
    stages.setdefault(st, [])

OUT = {"report_date": RUN,
       "run_label": "Run 9 (Thu 16-Jul-2026) vs 13-Jul & 10-Jul",
       "run_index": 9, "pipeline_id": 27474,
       "pipeline_name": "Sell.do Onboarding Pipeline",
       "owner_gaps": owner_gaps, "deals": recs}
json.dump(OUT, open(os.path.join(BASE, "current_data.json"), "w"), indent=1)

# fresh membership snapshot
cat = defaultdict(list)
for r in recs: cat[r["category"]].append(r["id"])
fresh = {"run_date": RUN,
         "deals": [[r["id"], r["name"], r["owner"]] for r in recs],
         "stages": {k: stages[k] for k in ["Open","Kickoff Done","Onboarding In Progress","Pending on Customer","Under Usage Tracking"]},
         "not_signedup": [r["id"] for r in recs if r["not_signedup"]],
         "overdue_golive": [r["id"] for r in recs if r["overdue_golive"]],
         "overdue_task": sorted(overdue_task), "future_task": sorted(future_task),
         "cat": {k: v for k, v in cat.items()},
         "idle_gt5": sorted(idle5), "idle_gt7": sorted(idle7), "idle_gt15": sorted(idle15),
         "notes": {str(i): [NT.get(i,[None])[0], (NT.get(i,[None,""])[1] or "")] for i in ids}}
json.dump(fresh, open(os.path.join(BASE, "fresh_2026-07-16.json"), "w"), indent=1)

print("assembled", len(recs), "deals")
print("stages:", {k: len(stages[k]) for k in ["Open","Kickoff Done","Onboarding In Progress","Pending on Customer","Under Usage Tracking"]})
print("sum stages:", sum(len(stages[k]) for k in ["Open","Kickoff Done","Onboarding In Progress","Pending on Customer","Under Usage Tracking"]))
new = [i for i in ids if i not in pby]
dropped = [i for i in pby if i not in set(ids)]
print("NEW this run:", [(i, DF[i]['name']) for i in new])
print("DROPPED since 13-Jul:", [(i, pby[i]['name']) for i in dropped])
print("no_task:", sum(1 for r in recs if r['no_task']), "overdue_task:", sum(1 for r in recs if r['overdue_task']), "no_notes:", sum(1 for r in recs if r['no_notes']))
print("overdue_golive:", sum(1 for r in recs if r['overdue_golive']), "not_signedup:", sum(1 for r in recs if r['not_signedup']))
print("jira cited:", {r['id']: r['jira_keys'] for r in recs if r['jira_keys']})
