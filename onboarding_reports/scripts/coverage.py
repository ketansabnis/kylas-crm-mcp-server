#!/usr/bin/env python3
"""SCOPE COVERAGE - the master onboarding checklist, and what the team quietly skipped.

Usage:
  python coverage.py --fields deal_fields_<date>.json [more.json ...] \
                     --data current_data.json --outdir onboarding_reports --date YYYY-MM-DD

Why this exists
---------------
Once you start flagging stuck deals, the cheapest way to look unstuck is to stop tracking the
hard items - mark them "Not required", or never fill the field at all. A blank field and a
finished task look identical in every report that only counts what is Completed.

So this scores every deal against a MASTER CHECKLIST derived from (a) the Kylas deal custom
fields and (b) the recurring items in the onboarding notes, and flags the ways scope disappears:

  NOT TRACKED      - a Must/Basic item with no value at all. Invisible work. The worst state.
  CHALLENGE        - "Not required" claimed on a MUST item. Nobody goes live without these.
  NO LEAD SOURCE   - not one lead source integrated. The CRM has nothing flowing into it.
  STALLED ITEM     - Initiated / Waiting on customer for longer than the deal has any excuse for.
  PREMATURE HANDOVER - handed over / go-live date set while Must items are still open.
  NO FEEDBACK      - handed over without the onboarding feedback form.

Tiers
-----
MUST     - the account is not live without it. "Not required" is not an acceptable answer.
BASIC    - standard for this segment. "Not required" is acceptable but must be a real decision.
ENHANCED - only if sold (see Required Tools on the deal) or explicitly asked for.

Codes in the fields file: C=Completed, I=Initiated, W=Waiting on customer, N=Not required, -=blank.
"""
import json, argparse, os, datetime
from collections import Counter, defaultdict

# ---------------------------------------------------------------- MASTER CHECKLIST
# key: (label, tier_by_segment, notes)
# tier_by_segment: dict segment -> MUST | BASIC | ENHANCED   ("*" = all segments)
CHECKLIST = {
 # --- foundation: no account works without these ---
 "usersSetup":        ("User logins created",            {"*": "MUST"}),
 "projectsSetup":     ("Projects created",               {"Developer": "MUST", "*": "BASIC"}),
 "routingSetup":      ("Lead routing configured",        {"*": "MUST"}),
 "pipelineSetup":     ("Pipeline / stages configured",   {"*": "MUST"}),
 "leadImport":        ("Existing leads imported",        {"*": "MUST"}),
 # --- lead sources: at least ONE must be live (checked as a group, see LEAD_SOURCES) ---
 "website":           ("Website integration",            {"*": "BASIC"}),
 "facebook":          ("Meta / Facebook lead-gen",       {"*": "BASIC"}),
 "propertyPortal":    ("Property portals (99acres etc)", {"*": "BASIC"}),
 "google":            ("Google lead-gen",                {"*": "ENHANCED"}),
 "linkedin":          ("LinkedIn lead-gen",              {"*": "ENHANCED"}),
 # --- comms ---
 "whatsapp":          ("WhatsApp integration",           {"*": "BASIC"}),
 "whatsappTemplate":  ("WhatsApp templates",             {"*": "BASIC"}),
 "cloudTelephony":    ("Cloud telephony / IVR",          {"*": "BASIC"}),
 "dlt":               ("DLT (SMS) registration",         {"*": "BASIC"}),
 "offlineTracker":    ("Offline dialer / tracker app",   {"*": "BASIC"}),
 # --- real-estate core ---
 "inventorySetup":    ("Inventory / units loaded",       {"Developer": "BASIC", "*": "ENHANCED"}),
 "siteVisitForm":     ("Site-visit form",                {"Developer": "BASIC", "*": "ENHANCED"}),
 "channelPartner":    ("Channel-partner module",         {"Channel partner": "MUST", "Broker": "BASIC", "*": "ENHANCED"}),
 "workflow":          ("Workflow automation",            {"*": "BASIC"}),
 # --- enablement: an un-trained account is a churned account ---
 "salesTraining":     ("Sales / pre-sales training",     {"*": "MUST"}),
 "adminTraining":     ("Admin training",                 {"*": "MUST"}),
 "marketingTraining": ("Marketing training",             {"*": "BASIC"}),
 # --- post-sales suite (sold separately) ---
 "costSheet":         ("Cost-sheet template",            {"*": "ENHANCED"}),
 "paymentSchedule":   ("Payment-schedule template",      {"*": "ENHANCED"}),
 "bookingDocs":       ("Booking documents",              {"*": "ENHANCED"}),
 "bookingsImport":    ("Bookings import",                {"*": "ENHANCED"}),
 "postSalesTemplates":("Post-sales templates",           {"*": "ENHANCED"}),
 # --- reporting / misc ---
 "salesDashboard":    ("Sales dashboard",                {"*": "ENHANCED"}),
 "ownerDashboard":    ("Owner dashboard",                {"*": "ENHANCED"}),
 "marketingDashboard":("Marketing dashboard",            {"*": "ENHANCED"}),
 "goals":             ("Goals setup",                    {"*": "ENHANCED"}),
 "roi":               ("ROI configuration",              {"*": "ENHANCED"}),
 "bulkDialer":        ("Bulk dialer",                    {"*": "ENHANCED"}),
 "emailSubdomain":    ("Email sub-domain",               {"*": "ENHANCED"}),
 "erp":               ("ERP integration",                {"*": "ENHANCED"}),
 "zohoAnalytics":     ("Zoho analytics",                 {"*": "ENHANCED"}),
 "approval":          ("Approval setup",                 {"*": "ENHANCED"}),
 "onlineMeeting":     ("Online-meeting integration",     {"*": "ENHANCED"}),
}
LEAD_SOURCES = ["website", "facebook", "propertyPortal", "google", "linkedin"]

# Required Tools (what sales sold) -> the field that proves we delivered it
TOOL_TO_FIELD = {
 "Native WA": "whatsapp", "Personal WA": "whatsapp",
 "CP Management Tool": "channelPartner",
 "AI Calling": "cloudTelephony",
 "CRM": "usersSetup",
}
STALL_DAYS = 30   # an item Initiated/Waiting for longer than this on an older deal is stalled

ap = argparse.ArgumentParser()
ap.add_argument("--fields", nargs="+", required=True)
ap.add_argument("--data", default=None, help="current_data.json (for movement verdicts / stuck streaks)")
ap.add_argument("--outdir", required=True)
ap.add_argument("--date", required=True)
A = ap.parse_args()

F = {}
for p in A.fields:
    F.update(json.load(open(p)))
F = {int(k): v for k, v in F.items() if "test" not in (v.get("name") or "").lower()}

MOVE = {}
if A.data and os.path.exists(A.data):
    for r in json.load(open(A.data))["deals"]:
        MOVE[r["id"]] = r
RUN = datetime.date.fromisoformat(A.date)

def tier(field, segment):
    t = CHECKLIST[field][1]
    return t.get(segment or "*", t.get("*", "ENHANCED"))

def age_days(d):
    s = d.get("actualStart") or ""
    try:
        return (RUN - datetime.date.fromisoformat(s[:10])).days
    except Exception:
        return None

findings = []          # one row per flagged item
per_deal = {}          # id -> summary

for did, d in F.items():
    seg = d.get("segment")
    age = age_days(d)
    must = [f for f in CHECKLIST if tier(f, seg) == "MUST"]
    basic = [f for f in CHECKLIST if tier(f, seg) == "BASIC"]
    must_done = sum(1 for f in must if d.get(f) == "C")
    basic_done = sum(1 for f in basic if d.get(f) == "C")
    # a Basic item legitimately marked Not required still counts as "resolved" for the %
    basic_resolved = sum(1 for f in basic if d.get(f) in ("C", "N"))

    flags = []
    DEAL_LEVEL = {"PREMATURE HANDOVER", "GO-LIVE FICTION", "NO FEEDBACK"}
    def add(sev, field, why):
        label = "(whole deal)" if sev in DEAL_LEVEL else (CHECKLIST[field][0] if field in CHECKLIST else field)
        findings.append({"deal": d["name"], "id": did, "owner": d["owner"], "stage": d["stage"],
                         "severity": sev, "item": label,
                         "tier": "-" if sev in DEAL_LEVEL else (tier(field, seg) if field in CHECKLIST else "-"),
                         "value": "-" if sev in DEAL_LEVEL else d.get(field, "-"), "why": why,
                         "licences": d.get("licences"), "billed": d.get("billed"),
                         "stuck_streak": (MOVE.get(did) or {}).get("stuck_streak", 0)})
        flags.append(sev)

    # 1. Must-have items that are blank or disclaimed
    for f in must:
        v = d.get(f, "-")
        if v == "-":
            add("NOT TRACKED", f, "Must-have item with no value at all - this work is invisible.")
        elif v == "N":
            add("CHALLENGE", f, "Marked 'Not required' on a MUST item. No account goes live without this.")
    # 2. Basic items never tracked
    for f in basic:
        if d.get(f, "-") == "-":
            add("NOT TRACKED", f, "Standard item for this segment, left blank.")
    # 3. No lead source at all
    if not any(d.get(f) == "C" for f in LEAD_SOURCES):
        pend = [f for f in LEAD_SOURCES if d.get(f) in ("I", "W")]
        add("NO LEAD SOURCE", "website",
            "Not one lead source is live (%s). The CRM has nothing flowing into it."
            % ("all marked N/blank" if not pend else "in progress: " + ", ".join(pend)))
    # 4. Sold but not delivered
    for t in (d.get("tools") or []):
        f = TOOL_TO_FIELD.get(t)
        if f and d.get(f) in ("N", "-"):
            add("SOLD NOT DELIVERED", f, "'%s' is on the order form (Required Tools) but the setup is %s."
                % (t, "not tracked" if d.get(f) == "-" else "marked Not required"))
    # 5. Stalled items on older deals
    if age and age > STALL_DAYS:
        for f in must + basic:
            if d.get(f) in ("I", "W"):
                add("STALLED ITEM", f, "Still '%s' after %d days since start."
                    % ("Initiated" if d.get(f) == "I" else "Waiting on customer", age))
    # 6. Premature handover / go-live fiction
    open_must = [CHECKLIST[f][0] for f in must if d.get(f) not in ("C",)]
    if (d.get("handover") or "").startswith("Handed over") and open_must:
        add("PREMATURE HANDOVER", "usersSetup",
            "Handed over with %d MUST item(s) not completed: %s." % (len(open_must), ", ".join(open_must[:4])))
    if d.get("actualGoLive") and open_must:
        add("GO-LIVE FICTION", "usersSetup",
            "Actual Go-Live date is set (%s) but %d MUST item(s) are still open: %s."
            % (str(d["actualGoLive"])[:10], len(open_must), ", ".join(open_must[:4])))
    # 7. Handed over without feedback
    if (d.get("handover") or "").startswith("Handed over") and d.get("feedback") != "Yes":
        add("NO FEEDBACK", "usersSetup", "Handed over without the onboarding feedback form.")

    per_deal[did] = {
        "name": d["name"], "owner": d["owner"], "stage": d["stage"], "segment": seg,
        "category": d.get("category"), "licences": d.get("licences"), "billed": d.get("billed"),
        "age": age, "must_total": len(must), "must_done": must_done,
        "must_pct": round(100 * must_done / max(len(must), 1)),
        "basic_total": len(basic), "basic_done": basic_done,
        "basic_pct": round(100 * basic_resolved / max(len(basic), 1)),
        "not_tracked": sum(1 for f in must + basic if d.get(f, "-") == "-"),
        "not_required": sum(1 for f in CHECKLIST if d.get(f) == "N"),
        "not_required_pct": round(100 * sum(1 for f in CHECKLIST if d.get(f) == "N") / len(CHECKLIST)),
        "open_must": open_must, "flags": Counter(flags),
        "stuck_streak": (MOVE.get(did) or {}).get("stuck_streak", 0),
    }

# ---------------------------------------------------------------- owner integrity
own = defaultdict(lambda: {"deals": 0, "nr": 0, "cells": 0, "nt": 0, "must_pct": []})
for did, s in per_deal.items():
    d = F[did]
    o = own[s["owner"]]
    o["deals"] += 1
    o["nr"] += sum(1 for f in CHECKLIST if d.get(f) == "N")
    o["nt"] += sum(1 for f in CHECKLIST if d.get(f, "-") == "-")
    o["cells"] += len(CHECKLIST)
    o["must_pct"].append(s["must_pct"])
owners = []
for o, v in own.items():
    owners.append({"owner": o, "deals": v["deals"],
                   "not_required_rate": round(100 * v["nr"] / max(v["cells"], 1)),
                   "not_tracked_rate": round(100 * v["nt"] / max(v["cells"], 1)),
                   "avg_must_pct": round(sum(v["must_pct"]) / max(len(v["must_pct"]), 1))})
owners.sort(key=lambda x: -x["not_required_rate"])

SEV = ["CHALLENGE", "NOT TRACKED", "NO LEAD SOURCE", "SOLD NOT DELIVERED",
       "PREMATURE HANDOVER", "GO-LIVE FICTION", "NO FEEDBACK", "STALLED ITEM"]
findings.sort(key=lambda f: (SEV.index(f["severity"]) if f["severity"] in SEV else 9, -(f["billed"] or 0)))

OUT = {"date": A.date, "deals": len(F), "findings": findings, "per_deal": per_deal,
       "owners": owners, "summary": Counter(f["severity"] for f in findings)}
json.dump(OUT, open(os.path.join(A.outdir, "coverage_%s.json" % A.date), "w"), indent=1, default=str)

# ---------------------------------------------------------------- sheet 13
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
XL = os.path.join(A.outdir, "Onboarding_Pipeline_Review_%s.xlsx" % A.date)
if os.path.exists(XL):
    wb = load_workbook(XL)
    thin = Side(style="thin", color="D9D9D9"); border = Border(thin, thin, thin, thin)
    NAVY = PatternFill("solid", fgColor="1F3864")
    hf = Font(name="Calibri", bold=True, color="FFFFFF", size=10)
    red = PatternFill("solid", fgColor="F4CCCC"); amber = PatternFill("solid", fgColor="FCE5CD")
    yellow = PatternFill("solid", fgColor="FFF2CC"); green = PatternFill("solid", fgColor="D9EAD3")
    title = Font(name="Calibri", bold=True, size=15, color="1F3864")
    sub = Font(name="Calibri", italic=True, size=9, color="666666"); reg = Font(name="Calibri", size=10)
    FILL = {"CHALLENGE": red, "GO-LIVE FICTION": red, "PREMATURE HANDOVER": red, "SOLD NOT DELIVERED": red,
            "NO LEAD SOURCE": amber, "NOT TRACKED": amber, "NO FEEDBACK": yellow, "STALLED ITEM": yellow}

    def sheet(nm, hdrs, rows, widths, t, s_, fillcol=0):
        if nm in wb.sheetnames: del wb[nm]
        ws = wb.create_sheet(nm)
        ws["A1"] = t; ws["A1"].font = title; ws["A2"] = s_; ws["A2"].font = sub
        for c, h in enumerate(hdrs, 1):
            x = ws.cell(row=4, column=c, value=h); x.font = hf; x.fill = NAVY; x.border = border
            x.alignment = Alignment(vertical="center", wrap_text=True)
        for i, row in enumerate(rows, 5):
            for c, v in enumerate(row, 1):
                x = ws.cell(row=i, column=c, value=v); x.font = reg; x.border = border
                x.alignment = Alignment(vertical="top", wrap_text=True)
            f = FILL.get(str(row[fillcol]))
            if f: ws.cell(row=i, column=fillcol + 1).fill = f
        for c, w in enumerate(widths, 1):
            ws.column_dimensions[chr(64 + c)].width = w
        ws.freeze_panes = "A5"

    sheet("13. Scope Coverage",
          ["Flag", "Deal", "Owner", "Stage", "Checklist item", "Tier", "Value", "Licences", "Billed", "Stuck runs", "Why it matters"],
          [[f["severity"], f["deal"], f["owner"], f["stage"], f["item"], f["tier"], f["value"],
            f["licences"], f["billed"], f["stuck_streak"], f["why"]] for f in findings],
          [20, 30, 18, 22, 26, 10, 8, 9, 11, 10, 62],
          "Scope Coverage - what was skipped, disclaimed, or never tracked",
          "CHALLENGE = 'Not required' on a MUST item. NOT TRACKED = blank field: the work is invisible, not done. Both are ways scope quietly disappears.")

    rows = sorted(per_deal.items(), key=lambda kv: (kv[1]["must_pct"], -(kv[1]["billed"] or 0)))
    sheet("14. Coverage by Deal",
          ["Deal", "Owner", "Segment", "Stage", "Licences", "Billed", "Days since start",
           "MUST done", "MUST %", "BASIC %", "Not tracked", "'Not required' %", "Open MUST items"],
          [[s["name"], s["owner"], s["segment"], s["stage"], s["licences"], s["billed"], s["age"],
            "%d/%d" % (s["must_done"], s["must_total"]), s["must_pct"], s["basic_pct"],
            s["not_tracked"], s["not_required_pct"], ", ".join(s["open_must"])] for _, s in rows],
          [30, 18, 16, 22, 9, 11, 14, 11, 9, 9, 11, 14, 60],
          "Coverage by Deal - how much of the checklist is actually done",
          "Sorted worst-first by MUST %. 'Not required' % is the share of the whole checklist this owner disclaimed on this deal.")
    wb.save(XL)

print("Coverage written. deals=%d" % len(F))
print("findings:", dict(OUT["summary"]))
print("\nOwner integrity (how much of the checklist each owner disclaims or never fills):")
print("%-22s %6s %14s %14s %10s" % ("OWNER", "DEALS", "'Not required'", "'Not tracked'", "avg MUST%"))
for o in owners:
    print("%-22s %6d %13d%% %13d%% %9d%%" % (o["owner"], o["deals"], o["not_required_rate"], o["not_tracked_rate"], o["avg_must_pct"]))
print("\nWorst MUST coverage:")
for did, s in sorted(per_deal.items(), key=lambda kv: kv[1]["must_pct"])[:12]:
    print("  %-34s %-18s MUST %3d%%  open: %s" % (s["name"][:34], s["owner"][:18], s["must_pct"], ", ".join(s["open_must"][:4])))
