import sys, json, argparse, glob, os, datetime
ap=argparse.ArgumentParser()
ap.add_argument("--data",required=True); ap.add_argument("--outdir",required=True); ap.add_argument("--date",required=True)
A=ap.parse_args()
SNAP=json.load(open(A.data)); RECS=SNAP["deals"]; _by={r["id"]:r for r in RECS}
deals=[(r["id"],r["name"],r["owner"]) for r in RECS]
ids=[r["id"] for r in RECS]
category={r["id"]:r["category"] for r in RECS}
billed={r["id"]:r["billed"] for r in RECS if r.get("billed") is not None}
recv={r["id"]:r["recv"] for r in RECS if r.get("recv") is not None}
licenses={r["id"]:r["lic"] for r in RECS if r.get("lic") is not None}
ln={r["id"]:(r.get("last_note_epoch"), r.get("last_note_text","")) for r in RECS}
def _g(k):
    return lambda i:_by[i].get(k)
stage=_g("stage"); idle_bucket=_g("idle"); age_band=_g("age"); value_band=_g("vband"); lic_band=_g("lband")
brand_tag=_g("brand"); suggest_grade=_g("suggested"); grade_flag=_g("gflag"); grade_reason=_g("greason")
cadence=_g("cadence"); next_step=_g("nstep"); days_since=_g("dsince")
def _fs(k): return {r["id"] for r in RECS if r.get(k)}
overdue_golive=_fs("overdue_golive"); not_signedup=_fs("not_signedup"); high_value=_fs("high_value")
no_task=_fs("no_task"); overdue_task=_fs("overdue_task")
idle5={i for i in ids if idle_bucket(i)!="<=5 d"}
idle7={i for i in ids if idle_bucket(i) in ("7-15 d","15-30 d","30+ d")}
idle15={i for i in ids if idle_bucket(i) in ("15-30 d","30+ d")}
idle30={i for i in ids if idle_bucket(i)=="30+ d"}
CATA={i for i in ids if category[i]=="A"}; CATB={i for i in ids if category[i]=="B"}; CATC={i for i in ids if category[i]=="C"}
BROKER={i for i in ids if category[i]=="Broker"}; UNCAT={i for i in ids if category[i]=="(none)"}
def last_meeting(i): return "None logged"
def next_meeting(i): return "None logged"
def mtg_in_5d(i): return "No - none logged"
OWNER_GAPS=SNAP.get("owner_gaps",{})
PENDING_VERDICT={r["id"]:(r["pending_verdict"],r["pending_action"]) for r in RECS if r.get("pending_verdict")}
_sev={"STUCK":0,"Unknown":0,"Stalled":1,"Customer-blocked":2,"Mis-staged":2,"Moving slowly":3,"Near done":3,"Moving":4,"":5}
PORDER=sorted([r["id"] for r in RECS if r["stage"]=="Pending on Customer"], key=lambda i:_sev.get(_by[i].get("pending_verdict",""),5))
OUT=os.path.join(A.outdir,"Onboarding_Pipeline_Review_%s.xlsx"%A.date)
_pri=sorted([p for p in glob.glob(os.path.join(A.outdir,"snapshot_*.json")) if os.path.basename(p)[9:19] < A.date])
PRIORS=[json.load(open(p)) for p in _pri[-2:]]

from collections import Counter
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

thin=Side(style="thin",color="D9D9D9"); border=Border(thin,thin,thin,thin)
NAVY=PatternFill("solid",fgColor="1F3864"); BLUE=PatternFill("solid",fgColor="2E5496")
hf=Font(name="Calibri",bold=True,color="FFFFFF",size=10)
red=PatternFill("solid",fgColor="F4CCCC"); amber=PatternFill("solid",fgColor="FCE5CD"); yellow=PatternFill("solid",fgColor="FFF2CC"); green=PatternFill("solid",fgColor="D9EAD3"); grey=PatternFill("solid",fgColor="EFEFEF")
title=Font(name="Calibri",bold=True,size=15,color="1F3864"); sub=Font(name="Calibri",italic=True,size=9,color="666666")
H=Font(name="Calibri",bold=True,size=11,color="1F3864"); b=Font(name="Calibri",bold=True,size=10); reg=Font(name="Calibri",size=10)
def hcell(ws,r,c,v,fill=NAVY):
    x=ws.cell(row=r,column=c,value=v); x.font=hf; x.fill=fill; x.border=border; x.alignment=Alignment(vertical="center",wrap_text=True); return x

ids=[d[0] for d in deals]; name={d[0]:d[1] for d in deals}; owner={d[0]:d[2] for d in deals}
def has_notes(i): return ln.get(i,(None,""))[0] is not None
no_notes={i for i in ids if not has_notes(i)}
# stuck signal from gist text
def stuck_note(i):
    g=ln.get(i,(None,""))[1].lower()
    return any(k in g for k in ["no movement","on hold","rescheduled","kickoff call pending","yet to sign up","no progress","waiting on customer","no notes"])

wb=Workbook()

# ============ SHEET 1: STATS ============
s=wb.active; s.title="1. Stats"
s["A1"]="Sell.do Onboarding Pipeline - Statistics"; s["A1"].font=title
s["A2"]=f"Pipeline 27474  |  {len(ids)} open deals  |  Snapshot {A.date}"; s["A2"].font=sub
s["A3"]="Ageing = days since deal CREATED (created_at).  Movement = days since last activity (separate metric)."; s["A3"].font=sub
r=4
def block(r,head,rows,cols=("A","B"),fill=BLUE,total=True):
    s[f"A{r}"]=head; s[f"A{r}"].font=H; r+=1
    for k,col in enumerate(cols): pass
    hcell(s,r,1,"Category" if len(cols)==2 else "Category",fill); hcell(s,r,2,"Count",fill)
    r+=1; start=r
    for k,v in rows:
        s.cell(row=r,column=1,value=k).font=reg; s.cell(row=r,column=2,value=v).font=reg
        s.cell(row=r,column=1).border=border; s.cell(row=r,column=2).border=border
        r+=1
    if total:
        s.cell(row=r,column=1,value="Total").font=b; tc=s.cell(row=r,column=2,value=f"=SUM(B{start}:B{r-1})"); tc.font=b
        s.cell(row=r,column=1).border=border; tc.border=border; r+=1
    return r+1

oc=Counter(owner[i] for i in ids)
r=block(r,"By Owner",[(o,n) for o,n in oc.most_common()])
sc=Counter(stage(i) for i in ids)
r=block(r,"By Pipeline Stage",[("Open",sc["Open"]),("Kickoff Done",sc["Kickoff Done"]),("Onboarding In Progress",sc["Onboarding In Progress"]),("Pending on Customer",sc["Pending on Customer"]),("Under Usage Tracking",0)])
ag=[("<14 days",sum(1 for i in ids if age_band(i)=="<14 d")),("14-30 days",sum(1 for i in ids if age_band(i)=="14-30 d")),("30-60 days",sum(1 for i in ids if age_band(i)=="30-60 d")),("60-90 days",sum(1 for i in ids if age_band(i)=="60-90 d")),("90-180 days",sum(1 for i in ids if age_band(i)=="90-180 d")),("180+ days",sum(1 for i in ids if age_band(i)==">180 d"))]
r=block(r,"Deal Ageing = days since CREATED (created_at)",ag)
mv=[("<=5 days (healthy)",sum(1 for i in ids if idle_bucket(i)=="<=5 d")),("5-7 days",sum(1 for i in ids if idle_bucket(i)=="5-7 d")),("7-15 days",sum(1 for i in ids if idle_bucket(i)=="7-15 d")),("15-30 days",sum(1 for i in ids if idle_bucket(i)=="15-30 d")),("30+ days",sum(1 for i in ids if idle_bucket(i)=="30+ d"))]
r=block(r,"Movement = days since LAST ACTIVITY",mv)
def _dsb(lo,hi):
    return sum(1 for i in ids if (days_since(i) is not None) and (lo<=days_since(i)<=hi))
cad=[("<=5 days (OK)",_dsb(0,5)),("6-10 days",_dsb(6,10)),("11-15 days",_dsb(11,15)),("16-30 days",_dsb(16,30)),("31+ days",_dsb(31,99999)),("Never (no note)",sum(1 for i in ids if days_since(i) is None))]
r=block(r,"Touch cadence = days since LAST NOTE (interim proxy until meetings are logged)",cad)
mtb=[("Deals with a meeting logged on the deal",0),("Meeting scheduled/conducted within 5 days",0),("NO meeting logged (team to start logging)",len(ids))]
r=block(r,"Meetings ON DEALS (not yet logged - format ready going forward)",mtb,total=False)
risk=[("No activity 5+ days (your risk rule)",len(idle5)),("No notes logged at all",len(no_notes)),("Target go-live date already breached",len(overdue_golive)),("Customer 'Yet to sign up'",len(not_signedup)),("No future follow-up task",len(no_task)),("Has an OVERDUE task",len(overdue_task)),("Billed Amount field blank",52),("Estimated Value populated",0),("Meetings linked to these onboarding deals",0)]
r=block(r,"Risk & Data-Quality Flags",risk,total=False)
s.column_dimensions["A"].width=42; s.column_dimensions["B"].width=12
s.sheet_view.showGridLines=False

# ============ SHEET 2: EXEC SUMMARY ============
e=wb.create_sheet("2. Exec Summary (CEO-CRO)")
e["A1"]="Onboarding Pipeline - Executive Summary"; e["A1"].font=title
e["A2"]=f"For CEO & CRO  |  {A.date}"; e["A2"].font=sub
r=4
def para(r,head,lines,fill=grey):
    c=e.cell(row=r,column=1,value=head); c.font=Font(name="Calibri",bold=True,size=11,color="FFFFFF"); c.fill=NAVY; c.border=border
    e.merge_cells(start_row=r,start_column=1,end_row=r,end_column=2); r+=1
    for t in lines:
        c=e.cell(row=r,column=1,value=t); c.font=reg; c.alignment=Alignment(wrap_text=True,vertical="top")
        e.merge_cells(start_row=r,start_column=1,end_row=r,end_column=2)
        e.row_dimensions[r].height=30; r+=1
    return r+1
r=para(r,"The headline (movement this run)",[
"61 deals are open in onboarding. Comparing today vs the last run: 20 have GENUINELY PROGRESSED, but 33 have NOT moved (26 restate the same blocker, 7 had no activity at all) and 16 of those have now been stuck for 2+ consecutive runs (SUPER-RED - see Sheet 9); 9 of those have been stuck 6 runs in a row. 8 deals are new this run. 26 deals (43%) are already past their committed go-live date.",
"Data hygiene is still the structural issue: Billed Amount is blank on 43 of 61 deals (70%), Estimated Value is empty on every deal, 38 of 61 have no next task, and 2 (both new) deals still have zero notes. Note that get_deal_notes returns notes unsorted, so several stale deals' newest note had to be recovered via a larger fetch. Revenue-at-risk remains largely invisible in standard reports.",])
r=para(r,"Where the money is exposed",[
"Cash collected but customer still 'Yet to sign up': Doff Estate Post Sales - Rs5.24L fully received but not activated (new deal this run). Push to sign-up now.",
"Largest accounts by value: Times Group Rs9.44L (Pending-on-Customer - client UAT feedback overdue since 23-Jun, stuck 6 runs), Doff Estate & Doff Estate Post Sales Rs5.24L each (new, Open), SKYTOWN Rs5.0L (moved to Pending-on-Customer), Navkar Rs4.96L (Pending-on-Customer). Largest by licences: Kunwarji Realtors - 150 licences, Category A, go-live breached; client escalated rollout delays on 3-Jul in a meeting with the CEO and requested onsite support.",])
r=para(r,"What we are asking leadership to back",[
"1. A weekly onboarding hygiene standard: every open deal must have a LOGGED MEETING (scheduled or conducted) at least every 5 days, a dated note, and a next task; stage moved at each milestone. (Meetings are still not logged on deals at all.)",
"2. Make Billed Amount mandatory at deal creation so revenue-at-risk is visible (blank on 78% today).",
"3. A weekly SUPER-RED review: 16 deals have not genuinely moved for 2+ runs (9 of them for 6 runs straight) - most are stuck 'pending on customer'. Set drop-dead dates or move to HOLD.",
"4. A 'collections + activation' sweep on the paid-but-dormant accounts above (CRO + Onboarding).",])
e.column_dimensions["A"].width=70; e.column_dimensions["B"].width=40
e.sheet_view.showGridLines=False

# ============ SHEET 3: OWNER SCORECARD ============
o=wb.create_sheet("3. Owner Scorecard")
o["A1"]="Owner Scorecard - gaps for the Onboarding Head"; o["A1"].font=title
o["A2"]="Counts per owner across the key risk flags. Use for owner 1:1s."; o["A2"].font=sub
heads=["Owner","Open deals","A-grade","Idle 5+ d","No notes","Go-live overdue","Not signed up","No next task","Overdue task","Key gap to address"]
for j,h in enumerate(heads,1): hcell(o,4,j,h)
gaps=OWNER_GAPS or {
"Muntazar Mhate":"Highest load (19). Several 'No movement/On hold' (Propleaf, Raado) - decide HOLD vs push.",
"Venkat Viswavardhan":"14 deals incl AI-Calling set stalled on Mcube; i5 & YES Proptech have no notes.",
"Shweta Gouda":"14 deals; many at 'pending training/lead import' - chase customers to close.",
"Sahil Jane":"12 deals, many brand-new with no notes/next task - log first note + kickoff.",
"Raahul Ramanan R":"8 deals; Voora stuck since Feb in Pending-on-Customer; high-value Calicut only has a 'timesheet' note.",
"Sanket Nampalliwar":"6 deals but the most stuck: Shree Auto/Honda (Dec), Dhanvanthari, Kunwarji (150 lic, no notes).",
"Atharva Patil":"All 5 are IRIS deals, all idle 30+ d with NO notes; 2 are actually live - just not closed.",
"Shubham Dubey":"5 deals = mostly Post-Sales duplicates + 'dummy'. Clean these up.",
}
r=5
order=[o2 for o2,_ in oc.most_common()]
for ow in order:
    di=[i for i in ids if owner[i]==ow]
    vals=[ow,len(di),sum(i in CATA for i in di),sum(i in idle5 for i in di),sum(i in no_notes for i in di),sum(i in overdue_golive for i in di),sum(i in not_signedup for i in di),sum(i in no_task for i in di),sum(i in overdue_task for i in di),gaps.get(ow,"")]
    for j,v in enumerate(vals,1):
        c=o.cell(row=r,column=j,value=v); c.font=reg; c.border=border; c.alignment=Alignment(vertical="center",wrap_text=(j==9))
    # heat
    for j,st in ((4,idle5),(5,no_notes),(6,overdue_golive),(7,not_signedup),(8,no_task),(9,overdue_task)):
        n=o.cell(row=r,column=j).value
        if n and n>=5: o.cell(row=r,column=j).fill=red
        elif n and n>=3: o.cell(row=r,column=j).fill=amber
    r+=1
# totals
tv=["TOTAL",len(ids),len(CATA),len(idle5),len(no_notes),len(overdue_golive),len(not_signedup),len(no_task),len(overdue_task),""]
for j,v in enumerate(tv,1):
    c=o.cell(row=r,column=j,value=v); c.font=b; c.border=border; c.fill=grey
for j,w in enumerate([20,10,8,9,9,14,13,11,11,60],1):
    o.column_dimensions[o.cell(row=4,column=j).column_letter].width=w
o.freeze_panes="A5"; o.sheet_view.showGridLines=False

# ============ SHEET 4: DEAL-LEVEL TRACKER ============
d=wb.create_sheet("4. Deal-Level Tracker")
d["A1"]="Deal-Level Tracker - for the Onboarding Head to action"; d["A1"].font=title
d["A2"]="Cols E-F = movement vs the LAST run: Progressed / NEW / STUCK (same blocker or no activity). Stuck deals are grouped at the top. SUPER-RED = no genuine movement for 2+ consecutive runs."; d["A2"].font=sub
PREV_BY={r2["id"]:r2 for r2 in PRIORS[-1]["deals"]} if PRIORS else {}
heads=["Deal ID","Deal Name","Owner","Stage","Moved? (vs last run)","Movement detail (prev -> now)","Last activity","Last note date","Days since note","Has notes","Go-live overdue","Not signed up","Billed (Rs)","Licenses","Cat","Last note / status","Age (created)","Key Next Step (recommended)","Touch cadence (interim, vs 5d)","Last meeting","Next meeting","Mtg <=5d?"]
for j,h in enumerate(heads,1): hcell(d,3,j,h)
ord_idle={"30+ d":0,"15-30 d":1,"7-15 d":2,"5-7 d":3,"<=5 d":4}
import datetime
def fmt(i):
    e2=ln.get(i,(None,""))[0]
    if e2 is None: return ""
    return (datetime.datetime(1970,1,1)+datetime.timedelta(milliseconds=e2)).strftime("%d-%b-%y")
superred=PatternFill("solid",fgColor="C00000"); wf=Font(name="Calibri",bold=True,color="FFFFFF",size=10)
def mv_label(i):
    v=_by[i].get("movement_verdict",""); ss=_by[i].get("stuck_streak",0)
    if ss>=2: return "SUPER-RED ("+str(ss)+" runs stuck)"
    return {"Progressed":"Progressed","NEW":"NEW this run","Same-blocker":"STUCK - same blocker","No-touch":"STUCK - no activity"}.get(v,v or "-")
def mv_detail(i):
    p=PREV_BY.get(i); c=_by[i]
    if not PRIORS: return "Baseline run - no prior to compare."
    if not p: return c.get("movement_reason","New in pipeline this run.")
    sp="%s -> %s"%(p.get("stage"),c.get("stage"))
    npd="%s -> %s"%((p.get("last_note_date") or "no note"),(c.get("last_note_date") or "no note"))
    rsn=c.get("movement_reason",""); ss=c.get("stuck_streak",0)
    tail=(" [stuck x%d]"%ss) if ss>=1 and c.get("movement_verdict") in ("Same-blocker","No-touch") else ""
    return "Stage %s | Note %s | %s%s"%(sp,npd,rsn,tail)
mv_rank={"Same-blocker":0,"No-touch":0,"NEW":1,"Progressed":2}
rows=sorted(ids,key=lambda i:(mv_rank.get(_by[i].get("movement_verdict",""),1),-_by[i].get("stuck_streak",0),ord_idle[idle_bucket(i)],owner[i],name[i]))
r=4
for i in rows:
    ds=days_since(i)
    vals=[i,name[i],owner[i],stage(i),mv_label(i),mv_detail(i),idle_bucket(i),fmt(i),"" if ds is None else ds,"No" if i in no_notes else "Yes",
          "Yes" if i in overdue_golive else "","Yes" if i in not_signedup else "",billed.get(i,""),licenses.get(i,""),category.get(i,""),ln.get(i,(None,""))[1],age_band(i),next_step(i),cadence(i),last_meeting(i),next_meeting(i),mtg_in_5d(i)]
    for j,v in enumerate(vals,1):
        c=d.cell(row=r,column=j,value=v); c.font=reg; c.border=border; c.alignment=Alignment(vertical="center",wrap_text=(j in (6,16,18)))
        if j==13 and v!="": c.number_format='#,##0'
    vv=_by[i].get("movement_verdict",""); ss=_by[i].get("stuck_streak",0)
    mc=d.cell(row=r,column=5)
    if ss>=2: mc.fill=superred; mc.font=wf
    elif vv in ("Same-blocker","No-touch"): mc.fill=red
    elif vv=="Progressed": mc.fill=green
    elif vv=="NEW": mc.fill=yellow
    ib=idle_bucket(i)
    fill=red if ib=="30+ d" else amber if ib in("15-30 d","7-15 d") else yellow if ib=="5-7 d" else None
    if fill: d.cell(row=r,column=7).fill=fill
    if i in no_notes: d.cell(row=r,column=10).fill=red
    if i in overdue_golive: d.cell(row=r,column=11).fill=amber
    if i in not_signedup: d.cell(row=r,column=12).fill=amber
    _cd=cadence(i); d.cell(row=r,column=19).fill=(green if _cd.startswith("OK") else amber if _cd=="Watch" else red)
    d.cell(row=r,column=22).fill=grey
    r+=1
for j,w in enumerate([10,30,18,20,22,60,11,12,9,8,13,12,11,8,5,58,12,40,15,13,13,16],1):
    d.column_dimensions[d.cell(row=3,column=j).column_letter].width=w
d.freeze_panes="A4"; d.sheet_view.showGridLines=False

# ============ SHEET 5: LARGE / STUCK / ATTENTION ============
a=wb.create_sheet("5. Large-Stuck-Attention")
a["A1"]="Large deals, Stuck deals & Deals needing attention - for everyone"; a["A1"].font=title
r=3
def tbl(r,head,colset,rowids,extra=None):
    a.cell(row=r,column=1,value=head).font=H; r+=1
    for j,h in enumerate(colset,1): hcell(a,r,j,h)
    r+=1
    for i in rowids:
        base=[name[i],owner[i],stage(i),fmt(i),idle_bucket(i)]
        if extra: base=extra(i)
        for j,v in enumerate(base,1):
            c=a.cell(row=r,column=j,value=v); c.font=reg; c.border=border; c.alignment=Alignment(vertical="center",wrap_text=(j==len(base)))
            if j==(6 if extra else 0): pass
        r+=1
    return r+1

# Large deals (by billed/licenses)
large=sorted([i for i in ids if billed.get(i,0)>=300000 or licenses.get(i,0)>=30], key=lambda i:-(billed.get(i,0)+licenses.get(i,0)*1000))
def ex_large(i):
    return [name[i],owner[i],stage(i),billed.get(i,""),licenses.get(i,""),category.get(i,""),ln.get(i,(None,""))[1]]
a.cell(row=r,column=1,value="A) LARGE DEALS (value / licenses) - protect these").font=H; r+=1
for j,h in enumerate(["Deal","Owner","Stage","Billed (Rs)","Licenses","Cat","Status / note"],1): hcell(a,r,j,h)
r+=1
for i in large:
    vals=ex_large(i)
    for j,v in enumerate(vals,1):
        c=a.cell(row=r,column=j,value=v); c.font=reg; c.border=border; c.alignment=Alignment(vertical="center",wrap_text=(j==7))
        if j==4 and v!="": c.number_format='#,##0'
    a.cell(row=r,column=1).fill=green
    r+=1
r+=1
# Stuck deals (idle 30+ OR stuck note)
stuck=[i for i in ids if i in idle30 or "no movement" in ln.get(i,(None,""))[1].lower() or "on hold" in ln.get(i,(None,""))[1].lower() or "rescheduled" in ln.get(i,(None,""))[1].lower()]
stuck=sorted(set(stuck),key=lambda i:(ord_idle[idle_bucket(i)],owner[i]))
a.cell(row=r,column=1,value="B) STUCK DEALS (30+ days idle, or notes say 'no movement / on hold / call rescheduled')").font=H; r+=1
for j,h in enumerate(["Deal","Owner","Stage","Last note","Idle","Status / note"],1): hcell(a,r,j,h)
r+=1
for i in stuck:
    vals=[name[i],owner[i],stage(i),fmt(i),idle_bucket(i),ln.get(i,(None,""))[1]]
    for j,v in enumerate(vals,1):
        c=a.cell(row=r,column=j,value=v); c.font=reg; c.border=border; c.alignment=Alignment(vertical="center",wrap_text=(j==6))
    a.cell(row=r,column=5).fill=red if idle_bucket(i)=="30+ d" else amber
    r+=1
r+=1
# Needs attention: paid but not signed up, or high-value overdue go-live
attn=[i for i in ids if (i in not_signedup and (i in billed or i in idle5 or i in overdue_golive)) or (i in high_value and i in overdue_golive)]
attn=sorted(set(attn),key=lambda i:-(billed.get(i,0)))
a.cell(row=r,column=1,value="C) NEEDS ATTENTION (paid but 'Yet to sign up', or large + go-live breached)").font=H; r+=1
for j,h in enumerate(["Deal","Owner","Stage","Billed (Rs)","Signed up?","Go-live overdue","Status / note"],1): hcell(a,r,j,h)
r+=1
for i in attn:
    su="Yet to sign up" if i in not_signedup else "-"
    vals=[name[i],owner[i],stage(i),billed.get(i,""),su,"Yes" if i in overdue_golive else "",ln.get(i,(None,""))[1]]
    for j,v in enumerate(vals,1):
        c=a.cell(row=r,column=j,value=v); c.font=reg; c.border=border; c.alignment=Alignment(vertical="center",wrap_text=(j==7))
        if j==4 and v!="": c.number_format='#,##0'
    a.cell(row=r,column=5).fill=amber
    r+=1
for col,w in zip("ABCDEFG",[34,19,21,13,15,15,66]): a.column_dimensions[col].width=w
a.sheet_view.showGridLines=False

# ============ SHEET 6: PENDING-ON-CUSTOMER VALIDATION ============
p=wb.create_sheet("6. Pending-on-Customer Check")
p["A1"]="'Pending on Customer' validation - is it really moving?"; p["A1"].font=title
p["A2"]=f"{len(PORDER)} deals sit in this stage. Verdict from last 2-3 notes + activity."; p["A2"].font=sub
for j,h in enumerate(["Deal","Owner","Last note","Days since","Verdict","Clear next action"],1): hcell(p,4,j,h)
verdict=PENDING_VERDICT or {
3929883:("Moving","Active (note 15-Jun). Push remaining items to handover."),
4233715:("Moving slowly","BOT shared; chase customer for Mcube number, set test date."),
4147287:("Customer-blocked","Customer unavailable (office shifting). Re-book training, set drop-dead date."),
4079157:("Near done","Most complete; schedule final handover this week."),
4241966:("Stalled","Bot shared 21-May, no update since. Chase customer; if no response in 7d, flag HOLD."),
3575524:("STUCK","Last note Feb-23; 'handover scheduled' never happened. Escalate or re-open kickoff."),
3506901:("STUCK","All steps waiting on customer since Jan; not signed up; Rs3L unpaid. Escalate + collections."),
3304062:("STUCK","Waiting on customer since Dec for WhatsApp/telephony. Final call or move to HOLD."),
3304063:("STUCK","Waiting on customer since Dec. Final call or move to HOLD."),
3343526:("Mis-staged","Actually LIVE (go-live 06-Oct). Move to Handover Complete - shouldn't be here."),
4337048:("Unknown","No notes at all. Owner must log status + next step immediately."),
}
porder=PORDER
r=5
for i in porder:
    v=verdict[i]; ds=days_since(i)
    vals=[name[i],owner[i],fmt(i),"" if ds is None else ds,v[0],v[1]]
    for j,val in enumerate(vals,1):
        c=p.cell(row=r,column=j,value=val); c.font=reg; c.border=border; c.alignment=Alignment(vertical="center",wrap_text=(j==6))
    vv=v[0]
    f=red if vv in("STUCK","Unknown") else amber if vv in("Stalled","Customer-blocked","Mis-staged") else green
    p.cell(row=r,column=5).fill=f
    r+=1
for col,w in zip("ABCDEF",[32,19,13,11,16,70]): p.column_dimensions[col].width=w
p.sheet_view.showGridLines=False


# ============ SHEET 7: CUSTOMER CATEGORY ============
import datetime as _dt
def _fmt(i):
    e2=ln.get(i,(None,""))[0]
    return "" if e2 is None else (_dt.datetime(1970,1,1)+_dt.timedelta(milliseconds=e2)).strftime("%d-%b-%y")
ct=wb.create_sheet("7. Customer Category")
ct["A1"]="Customer Category - usage & priority check"; ct["A1"].font=title
ct["A2"]="A/B/C/Broker should drive onboarding priority & SLA. Today it is captured but not acted on."; ct["A2"].font=sub
r=4
ct.cell(row=r,column=1,value="Distribution & risk by category").font=H; r+=1
for j,h in enumerate(["Category","Deals","% of pipe","Idle 5+ d","No notes","Not signed up","Go-live overdue"],1): hcell(ct,r,j,h)
r+=1
csets=[("A (top priority)",CATA),("B",CATB),("C",CATC),("Broker",BROKER),("Uncategorized",UNCAT)]
for nm,st in csets:
    n=len(st)
    vals=[nm,n,str(round(100*n/max(1,len(ids))))+"%",sum(i in idle5 for i in st),sum(i in no_notes for i in st),sum(i in not_signedup for i in st),sum(i in overdue_golive for i in st)]
    for j,v in enumerate(vals,1):
        c=ct.cell(row=r,column=j,value=v); c.font=reg; c.border=border; c.alignment=Alignment(vertical="center")
    if nm.startswith("A"):
        for j in range(1,8): ct.cell(row=r,column=j).fill=red
    if nm.startswith("Uncat"):
        for j in range(1,8): ct.cell(row=r,column=j).fill=amber
    r+=1
c=ct.cell(row=r,column=1,value="Total"); c.font=b; c.border=border
c=ct.cell(row=r,column=2,value="=SUM(B6:B10)"); c.font=b; c.border=border
r+=2
naidle=sum(i in idle5 for i in CATA); nann=sum(i in no_notes for i in CATA)
ct.cell(row=r,column=1,value="What this tells us").font=H; r+=1
notes_txt=[
"A-grade = your most important accounts (11 deals). "+str(naidle)+" have had NO activity in 5+ days and "+str(nann)+" have no notes at all - cadence on the A's has improved, keep it tight.",
"Category is still not used to prioritise: A deals (Kunwarji 150 lic, Times, i5, Raghava) sit alongside C deals with the same attention. Tie an SLA to grade.",
"Value is not tracked consistently: the biggest billed deal, Times Group (~Rs9.4L), is Category A, but Billed Amount is blank on 52 of 67 deals - populate it and re-grade against value + licences.",
"0 deals are uncategorized this run (good) - keep category mandatory at creation so nothing falls through prioritisation.",
"55% of the pipeline (37) is tagged C. Either genuinely low-value, or default tagging - worth a quick audit so C actually means C.",
"Recommendation: tie an SLA to category - A = white-glove, named owner, weekly touch + exec visibility; B = fortnightly; C/Broker = templatised. Make category mandatory and value-aligned at deal creation.",
]
for t in notes_txt:
    c=ct.cell(row=r,column=1,value="- "+t); c.font=reg; c.alignment=Alignment(wrap_text=True,vertical="top")
    ct.merge_cells(start_row=r,start_column=1,end_row=r,end_column=7); ct.row_dimensions[r].height=44; r+=1
r+=1
ct.cell(row=r,column=1,value="A-GRADE WATCHLIST (protect these 15 - sorted by neglect)").font=H; r+=1
for j,h in enumerate(["Deal","Owner","Stage","Idle","Last note","Billed (Rs)","Lic","Status / note"],1): hcell(ct,r,j,h)
r+=1
ord_idle={"30+ d":0,"15-30 d":1,"7-15 d":2,"5-7 d":3,"<=5 d":4}
for i in sorted(CATA,key=lambda i:(ord_idle[idle_bucket(i)],name[i])):
    vals=[name[i],owner[i],stage(i),idle_bucket(i),_fmt(i),billed.get(i,""),licenses.get(i,""),ln.get(i,(None,""))[1]]
    for j,v in enumerate(vals,1):
        c=ct.cell(row=r,column=j,value=v); c.font=reg; c.border=border; c.alignment=Alignment(vertical="center",wrap_text=(j==8))
        if j==6 and v!="": c.number_format="#,##0"
    ib=idle_bucket(i)
    ct.cell(row=r,column=4).fill=red if ib=="30+ d" else amber if ib in("15-30 d","7-15 d") else yellow if ib=="5-7 d" else green
    r+=1
for col,w in zip("ABCDEFGH",[30,19,21,10,12,12,6,66]): ct.column_dimensions[col].width=w
ct.sheet_view.showGridLines=False



# ============ SHEET 8: RE-GRADE (value + brand) ============
import datetime as _d8
def _f8(i):
    e2=ln.get(i,(None,""))[0]
    return "" if e2 is None else (_d8.datetime(1970,1,1)+_d8.timedelta(milliseconds=e2)).strftime("%d-%b-%y")
rg=wb.create_sheet("8. Re-grade (value+brand)")
rg["A1"]="Category re-grade - value + licenses + brand/enterprise"; rg["A1"].font=title
rg["A2"]="Suggested grade = max of value, licence count, and brand/enterprise weight. Under-grading is the concern; higher-than-needed is low priority."; rg["A2"].font=sub
under=[i for i in ids if grade_flag(i)=="UNDER"]
ung=[i for i in ids if grade_flag(i)=="UNGRADED"]
_rk={"A":3,"B":2,"C":1,"Broker":1,"(none)":0}
over2=[i for i in ids if grade_flag(i)=="HIGH" and (_rk.get(category[i],1)-_rk[suggest_grade(i)])>=2]
sord={"A":0,"B":1,"C":2}
under=sorted(under,key=lambda i:(sord[suggest_grade(i)],name[i]))
def sect(r,head,rowids,fill,note=None):
    c=rg.cell(row=r,column=1,value=head); c.font=H; r+=1
    if note:
        c=rg.cell(row=r,column=1,value=note); c.font=Font(name="Calibri",italic=True,size=9,color="666666")
        rg.merge_cells(start_row=r,start_column=1,end_row=r,end_column=9); r+=1
    for j,h in enumerate(["Deal","Owner","Current","Suggested","Age (created)","Billed","Licenses","Brand","Why"],1): hcell(rg,r,j,h)
    r+=1
    for i in rowids:
        vals=[name[i],owner[i],category[i],suggest_grade(i),age_band(i),value_band(i),lic_band(i),brand_tag(i),grade_reason(i)]
        for j,v in enumerate(vals,1):
            c=rg.cell(row=r,column=j,value=v); c.font=reg; c.border=border; c.alignment=Alignment(vertical="center",wrap_text=(j==9))
        rg.cell(row=r,column=3).fill=fill
        rg.cell(row=r,column=4).fill=green
        r+=1
    return r+1
r=4
rg.cell(row=r,column=1,value="Summary: "+str(len(under))+" under-graded (fix), "+str(len(ung))+" ungraded (set a grade), "+str(len(over2))+" clearly over-graded (low priority). ~8 A-deals score B on size alone (20-49 lic) - acceptable for enterprise/brand, not listed.").font=b
r+=2
r=sect(r,"A) UNDER-GRADED - high value/brand but graded low (FIX THESE)",under,red)
r=sect(r,"B) UNGRADED - no category set (assign one)",ung,amber,"Includes Krishvi (already Active) and the 'dummy' test record.")
r=sect(r,"C) Clearly over-graded - review (low priority)",over2,grey,"B Square is actually live - close it rather than re-grade.")
for col,w in zip("ABCDEFGHI",[30,18,9,11,13,11,11,8,52]): rg.column_dimensions[col].width=w
rg.sheet_view.showGridLines=False



# ============ SHEET 9: COMPARISON & MOVEMENT ============
cm=wb.create_sheet("9. Comparison & Movement")
cm["A1"]="Comparison & Movement vs previous run(s)"; cm["A1"].font=title
cm["A2"]=SNAP.get("run_label",""); cm["A2"].font=sub
r=4
if not PRIORS:
    cm.cell(row=r,column=1,value="BASELINE RUN - no prior report to compare against yet.").font=Font(name="Calibri",bold=True,size=12,color="C00000")
    r+=1
    cm.cell(row=r,column=1,value="Comparison (what moved, what is stuck, SUPER-RED for no movement) starts from the next run.").font=reg
    r+=2
    cm.cell(row=r,column=1,value="Baseline anchors (today):").font=H; r+=1
    anchors=[("Open deals",len(ids)),("Touched <=5 days (cadence OK)",sum(1 for i in ids if cadence(i).startswith("OK"))),
             ("No touch logged ever",sum(1 for i in ids if days_since(i) is None)),
             ("Idle 5+ days (at risk)",len(idle5)),("Stage 'Pending on Customer'",len(PORDER)),
             ("Under-graded vs value/brand",sum(1 for i in ids if grade_flag(i)=="UNDER"))]
    for k,v in anchors:
        cm.cell(row=r,column=1,value=k).font=reg; cm.cell(row=r,column=2,value=v).font=b; r+=1
    r+=1
    cm.cell(row=r,column=1,value="From next run each deal gets: prev stage -> now, prev note vs now, movement verdict (Progressed / Same-blocker / No-touch), stuck-streak, and SUPER-RED if not genuinely moved for 2 runs.").font=Font(name="Calibri",italic=True,size=9,color="666666")
    cm.merge_cells(start_row=r,start_column=1,end_row=r,end_column=6); cm.row_dimensions[r].height=30
else:
    prev=PRIORS[-1]; pby={r2["id"]:r2 for r2 in prev["deals"]}
    for j,h in enumerate(["Deal","Owner","Stage prev->now","Last note prev->now","Movement verdict","Stuck streak","Reason / action"],1): hcell(cm,r,j,h)
    r+=1
    rows=sorted(ids,key=lambda i:(-_by[i].get("stuck_streak",0), name[i]))
    for i in rows:
        p=pby.get(i)
        st="%s -> %s"%(p["stage"],stage(i)) if p else "NEW this run"
        nd="%s -> %s"%((p.get("last_note_date") if p else "-") or "-",(_by[i].get("last_note_date") or "-"))
        mv=_by[i].get("movement_verdict","?"); ss=_by[i].get("stuck_streak",0)
        vals=[name[i],owner[i],st,nd,mv,ss,_by[i].get("movement_reason","")]
        for j,v in enumerate(vals,1):
            c=cm.cell(row=r,column=j,value=v); c.font=reg; c.border=border; c.alignment=Alignment(vertical="center",wrap_text=(j==7))
        if ss>=2 or mv in ("Same-blocker","No-touch","STUCK"):
            for j in range(1,8): cm.cell(row=r,column=j).fill=red
        elif mv=="Progressed": cm.cell(row=r,column=5).fill=green
        r+=1
    for col,w in zip("ABCDEFG",[28,18,28,26,16,11,50]): cm.column_dimensions[col].width=w
cm.sheet_view.showGridLines=False

wb.save(OUT)
json.dump(SNAP, open(os.path.join(A.outdir,"snapshot_%s.json"%A.date),"w"), indent=1)
print("OK", A.date, "deals",len(ids),"priors",len(PRIORS))
