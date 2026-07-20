import json
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

BASE="/sessions/gifted-happy-euler/mnt/kylas-crm-mcp-server/presales_june_analysis"
rows=json.load(open(BASE+"/master_dataset.json"))
S=json.load(open(BASE+"/summary_stats.json"))
DS="'Deals (237)'"
NROW=len(rows)  # 237
r1,r2=2,NROW+1

# ---- styles ----
NAVY="1F3864"; BLUE="2E5496"; LTBLUE="D6E0F0"; GREY="F2F2F2"
GREEN="C6EFCE"; GREENF="006100"; AMB="FFEB9C"; AMBF="9C6500"; RED="FFC7CE"; REDF="9C0006"
WHITE="FFFFFF"
thin=Side(style="thin",color="BFBFBF")
border=Border(left=thin,right=thin,top=thin,bottom=thin)
def hfont(sz=11,color=WHITE,b=True): return Font(name="Arial",size=sz,bold=b,color=color)
def font(sz=10,color="000000",b=False,italic=False): return Font(name="Arial",size=sz,bold=b,color=color,italic=italic)
def fill(c): return PatternFill("solid",fgColor=c)
wrap=Alignment(wrap_text=True,vertical="top")
ctr=Alignment(horizontal="center",vertical="center")
ctrw=Alignment(horizontal="center",vertical="center",wrap_text=True)
left=Alignment(horizontal="left",vertical="center")

wb=Workbook()

def title_row(ws,text,span,row=1,size=14):
    c=ws.cell(row=row,column=1,value=text)
    c.font=hfont(size,WHITE,True); c.fill=fill(NAVY); c.alignment=Alignment(horizontal="left",vertical="center")
    ws.merge_cells(start_row=row,start_column=1,end_row=row,end_column=span)
    ws.row_dimensions[row].height=26

def sub(ws,text,span,row,color=BLUE,size=11):
    c=ws.cell(row=row,column=1,value=text)
    c.font=hfont(size,WHITE,True); c.fill=fill(color); c.alignment=left
    ws.merge_cells(start_row=row,start_column=1,end_row=row,end_column=span)
    ws.row_dimensions[row].height=20

def kv_header(ws,headers,row,cols_start=1,fillc=BLUE):
    for i,h in enumerate(headers):
        c=ws.cell(row=row,column=cols_start+i,value=h)
        c.font=hfont(10,WHITE,True); c.fill=fill(fillc); c.alignment=ctrw; c.border=border

# =========================================================
# SHEET 1: READ ME
# =========================================================
ws=wb.active; ws.title="Read Me"
ws.sheet_view.showGridLines=False
for col,w in zip("AB",[26,120]): ws.column_dimensions[col].width=w
title_row(ws,"Pre-Sales June 2026 — Demo Quality Post-Mortem",2,1,15)
info=[
 ("Prepared for","Ketan Sabnis (CEO) — CRO-style post-mortem & action plan"),
 ("Source","Kylas CRM report 361026 'Deals Created By Pre-Sales (Creator)' — filter: Created By Team = 'Pre-sales team', Created At = June 2026"),
 ("Pre-sales team","Revati Ambike (126 demos), Ashwini Nirmal (107), Gayatri More (4)"),
 ("Scope","237 deals where a demo/meeting was actually CONDUCTED (Meeting Conducted = Yes). This equals the report's 237."),
 ("Important context","Pre-sales CREATED 328 deals in June; only 237 had a demo conducted (72%). 91 were created without a conducted demo."),
 ("Target being judged","200+ demos of 5+ user licenses (quality demos, not just count)."),
 ("","" ),
 ("How to read verdicts","pre_sales_verdict judges PRE-SALES work ONLY. A deal Sales failed to close can still be GREEN for pre-sales; a junk/sub-ICP demo is RED even if it wasn't sales' fault."),
 ("GREEN","Genuinely qualified demo — real person & company, real need, 5+ seats, info complete."),
 ("AMBER","Demo happened but qualification gaps — thin BANT, small size, wrong seniority, or missing info."),
 ("RED","Poor pre-sales work — junk/placeholder name, no real need, sub-ICP (1-user broker), or 'demo for the number'."),
 ("city_bucket","Main6 = the 6 cities with a physical sales rep (Pune, Mumbai, Delhi/NCR, Bangalore, Chennai, Hyderabad). Other = everywhere else."),
 ("onsite_or_online","Onsite = in-person/office visit demo. Online = tele/online demo. (Sell.Do's model favours in-person.)"),
 ("stall_blocker / owner","Primary reason the deal hasn't progressed and who owns that reason (Pre-sales / Sales / Customer / Product-Pricing)."),
 ("Data note","Some subagent-written creator labels were corrected against the report's own per-creator filters (authoritative). All 237 deals reconcile to the report."),
 ("Files","master_dataset.csv / .json = full data; summary_stats.json = all cross-tabs; deals/<id>.json = per-deal record incl. notes."),
]
r=3
for k,v in info:
    a=ws.cell(row=r,column=1,value=k); a.font=font(10,NAVY,True); a.alignment=Alignment(vertical="top",wrap_text=True)
    b=ws.cell(row=r,column=2,value=v); b.font=font(10); b.alignment=wrap
    if k in("GREEN","AMBER","RED"):
        a.fill=fill({"GREEN":GREEN,"AMBER":AMB,"RED":RED}[k]); a.font=font(10,{"GREEN":GREENF,"AMBER":AMBF,"RED":REDF}[k],True)
    ws.row_dimensions[r].height=30 if len(v)>90 else 18
    r+=1

# =========================================================
# SHEET 2: SCORECARD
# =========================================================
ws=wb.create_sheet("Scorecard")
ws.sheet_view.showGridLines=False
for col,w in zip("ABCDE",[42,14,14,16,60]): ws.column_dimensions[col].width=w
title_row(ws,"Executive Scorecard — June Pre-Sales Demos",5,1,15)
kv_header(ws,["Metric","Value","Denominator","% / vs Target","Read"],3)
def scr(row,metric,val,den,pct,read,flag=None):
    vals=[metric,val,den,pct,read]
    for i,v in enumerate(vals):
        c=ws.cell(row=row,column=1+i,value=v); c.border=border; c.alignment=(wrap if i in(0,4) else ctr)
        c.font=font(10, NAVY if i==0 else "000000", i==0)
    if flag:
        ws.cell(row=row,column=2).fill=fill(flag[0]); ws.cell(row=row,column=2).font=font(10,flag[1],True)
    ws.row_dimensions[row].height=30
r=4
scr(r,"Deals created by pre-sales (June)",328,"","—","Total deals stamped by the 3 pre-sales reps"); r+=1
scr(r,"Demos actually conducted",f"=COUNTA({DS}!A{r1}:A{r2})","=328","=B{}/C{}".format(r,r),"72% of created deals reached a conducted demo; 91 never did",(LTBLUE,"1F3864")); r+=1
scr(r,"TARGET: demos of 5+ licenses","=COUNTIF('Deals (237)'!I2:I238,\"Yes\")","=200","=B{}/C{}".format(r,r),"TARGET 200+. Only ~138 demos were 5+ seats — MISSED on quality",(RED,REDF)); r+=1
scr(r,"Demos that were <5 licenses (1-4)","=COUNTIF('Deals (237)'!I2:I238,\"No\")","=COUNTA('Deals (237)'!A2:A238)","=B{}/C{}".format(r,r),"~42% of demos were tiny 1-4 seat prospects",(AMB,AMBF)); r+=1
scr(r,"Pre-sales quality: GREEN","=COUNTIF('Deals (237)'!Q2:Q238,\"GREEN\")","=COUNTA('Deals (237)'!A2:A238)","=B{}/C{}".format(r,r),"Genuinely qualified demos",(GREEN,GREENF)); r+=1
scr(r,"Pre-sales quality: AMBER","=COUNTIF('Deals (237)'!Q2:Q238,\"AMBER\")","=COUNTA('Deals (237)'!A2:A238)","=B{}/C{}".format(r,r),"Real but thin qualification",(AMB,AMBF)); r+=1
scr(r,"Pre-sales quality: RED","=COUNTIF('Deals (237)'!Q2:Q238,\"RED\")","=COUNTA('Deals (237)'!A2:A238)","=B{}/C{}".format(r,r),"Poor / sub-ICP demos (should not have been booked)",(RED,REDF)); r+=1
scr(r,"Onsite (in-person) demos","=COUNTIF('Deals (237)'!M2:M238,\"Onsite\")","=COUNTA('Deals (237)'!A2:A238)","=B{}/C{}".format(r,r),"Only ~13% were in-person despite the offline model",(RED,REDF)); r+=1
scr(r,"Demos in Main-6 sales cities","=COUNTIF('Deals (237)'!K2:K238,\"Main6\")","=COUNTA('Deals (237)'!A2:A238)","=B{}/C{}".format(r,r),"67% in the 6 cities with a rep; 33% off-territory"); r+=1
scr(r,"Won / Booked (as of report date)","=COUNTIF('Deals (237)'!F2:F238,\"Won\")","=COUNTA('Deals (237)'!A2:A238)","=B{}/C{}".format(r,r),"~9% closed; 58% still open, 33% lost"); r+=1
scr(r,"Deals with 40+ licenses (true enterprise)",3,"=COUNTA('Deals (237)'!A2:A238)","=B{}/C{}".format(r,r),"Almost no genuine enterprise pipeline generated",(RED,REDF)); r+=1
scr(r,"Junk / placeholder contact names","=COUNTIF('Deals (237)'!N2:N238,\"No\")","=COUNTA('Deals (237)'!A2:A238)","=B{}/C{}".format(r,r),"Data-integrity leak in ~11% of demos",(AMB,AMBF)); r+=1
for rr in range(4,r):
    ws.cell(row=rr,column=4).number_format="0.0%"

# =========================================================
# SHEET 3: DEALS (237) — full detail
# =========================================================
ws=wb.create_sheet("Deals (237)")
ws.freeze_panes="C2"
cols=[("Deal ID",10),("Deal Name",22),("Creator",15),("Sales Owner",17),("Stage",17),("Status",9),
      ("Lic",6),("Tier",8),("5+?",6),("City",16),("Bucket",9),("Dev/Broker",13),("Onsite/Online",13),
      ("Name OK",8),("BANT",6),("BANT Flag",10),("Verdict",9),("Ent?",6),("Stall Blocker",17),
      ("Blocker Owner",13),("Prev CRM",14),("Won Value",11),("Notes",7),("One-line CRO verdict",70),("Notes (raw)",90)]
for i,(h,w) in enumerate(cols):
    ws.column_dimensions[get_column_letter(i+1)].width=w
    c=ws.cell(row=1,column=i+1,value=h); c.font=hfont(9,WHITE,True); c.fill=fill(BLUE); c.alignment=ctrw; c.border=border
ws.row_dimensions[1].height=30
def yn(v): return "Yes" if v in (True,"true","True") else ("No" if v in (False,"false","False") else "")
for ri,d in enumerate(rows,start=2):
    status="Won" if d["is_won"] else ("Lost" if d["is_lost"] else "Open")
    vals=[d["deal_id"],d["deal_name"],d["creator"],d["owner"],d["stage"],status,
          d["noOfLicenses"],d["license_tier"],("Yes" if d["is_5plus"] else "No"),
          d["city_clean"],d["city_bucket"],d["dev_or_broker"],d["onsite_or_online"],
          yn(d["name_valid"]),d["bant_score"],d["bant_flag"],d["pre_sales_verdict"],
          yn(d["enterprise_flag"]),d["stall_blocker"],d["blocker_owner"],d["prev_crm"],
          d["actualValue"] if d["is_won"] else None,d["notes_count"],d["one_line"],
          (d["notes_text"] or "")[:800]]
    for ci,v in enumerate(vals,start=1):
        c=ws.cell(row=ri,column=ci,value=v); c.border=border; c.font=font(9)
        c.alignment=wrap if ci in(2,24,25) else (left if ci in(4,5,10,12,19,20,21) else ctr)
    # color verdict cell (col 17)
    vc=ws.cell(row=ri,column=17); vd=d["pre_sales_verdict"]
    if vd in("GREEN","AMBER","RED"):
        vc.fill=fill({"GREEN":GREEN,"AMBER":AMB,"RED":RED}[vd]); vc.font=font(9,{"GREEN":GREENF,"AMBER":AMBF,"RED":REDF}[vd],True)
    sc=ws.cell(row=ri,column=6)
    if status=="Won": sc.fill=fill(GREEN); sc.font=font(9,GREENF,True)
    elif status=="Lost": sc.fill=fill(RED); sc.font=font(9,REDF,True)
    if vals[8]=="No": ws.cell(row=ri,column=9).font=font(9,REDF,True)
ws.auto_filter.ref=f"A1:Y{NROW+1}"

# =========================================================
# helper for simple count tables using COUNTIF/COUNTIFS
# =========================================================
def count_table(ws, start_row, title_text, headers, data_rows, span):
    sub(ws,title_text,span,start_row)
    hr=start_row+1
    kv_header(ws,headers,hr)
    r=hr+1
    for dr in data_rows:
        for i,v in enumerate(dr):
            c=ws.cell(row=r,column=1+i,value=v); c.border=border
            c.alignment=(left if i==0 else ctr); c.font=font(10, "000000", i==0)
        r+=1
    return r

# SHEET 4: PRE-SALES QUALITY
ws=wb.create_sheet("Pre-Sales Quality")
ws.sheet_view.showGridLines=False
for col,w in zip("ABCDEF",[26,12,12,12,12,12]): ws.column_dimensions[col].width=w
title_row(ws,"Pre-Sales Quality — Verdict Breakdown",6,1,14)
# Overall verdict table: title r3, header r4, data r5-r8
sub(ws,"Overall verdict (237 demos)",6,3)
kv_header(ws,["Verdict","Count","% of demos"],4)
overall=[("GREEN",GREEN,GREENF),("AMBER",AMB,AMBF),("RED",RED,REDF)]
rr=5
for v,cl,fc in overall:
    ws.cell(row=rr,column=1,value=v).font=font(10,fc,True); ws.cell(row=rr,column=1).fill=fill(cl)
    ws.cell(row=rr,column=2,value=f'=COUNTIF({DS}!Q2:Q238,"{v}")')
    ws.cell(row=rr,column=3,value=f'=B{rr}/237'); ws.cell(row=rr,column=3).number_format="0.0%"
    for cc in range(1,4): ws.cell(row=rr,column=cc).border=border; ws.cell(row=rr,column=cc).alignment=(left if cc==1 else ctr)
    rr+=1
ws.cell(row=rr,column=1,value="TOTAL").font=font(10,b=True)
ws.cell(row=rr,column=2,value="=SUM(B5:B7)").font=font(10,b=True)
ws.cell(row=rr,column=3,value=f'=B{rr}/237'); ws.cell(row=rr,column=3).number_format="0.0%"
for cc in range(1,4): ws.cell(row=rr,column=cc).border=border; ws.cell(row=rr,column=cc).alignment=(left if cc==1 else ctr)

start=11
sub(ws,"Quality by pre-sales rep",6,start)
kv_header(ws,["Creator","Demos","GREEN","AMBER","RED","% GREEN"],start+1)
creators=["Revati Ambike","Ashwini Nirmal","Gayatri More"]
rr=start+2
for cr in creators:
    ws.cell(row=rr,column=1,value=cr).font=font(10,b=True)
    ws.cell(row=rr,column=2,value=f'=COUNTIF({DS}!C2:C238,A{rr})')
    ws.cell(row=rr,column=3,value=f'=COUNTIFS({DS}!C2:C238,A{rr},{DS}!Q2:Q238,"GREEN")')
    ws.cell(row=rr,column=4,value=f'=COUNTIFS({DS}!C2:C238,A{rr},{DS}!Q2:Q238,"AMBER")')
    ws.cell(row=rr,column=5,value=f'=COUNTIFS({DS}!C2:C238,A{rr},{DS}!Q2:Q238,"RED")')
    ws.cell(row=rr,column=6,value=f'=C{rr}/B{rr}'); ws.cell(row=rr,column=6).number_format="0.0%"
    for cc in range(1,7): ws.cell(row=rr,column=cc).border=border; ws.cell(row=rr,column=cc).alignment=(left if cc==1 else ctr)
    rr+=1
# verdict by tier
start=rr+1
sub(ws,"Quality by licence tier (where do REDs come from?)",6,start)
kv_header(ws,["Tier","Demos","GREEN","AMBER","RED","% RED"],start+1)
tiers=["1-4","5-9","10-39","40+"]
rr=start+2
for t in tiers:
    ws.cell(row=rr,column=1,value=t).font=font(10,b=True)
    ws.cell(row=rr,column=2,value=f'=COUNTIF({DS}!H2:H238,A{rr})')
    ws.cell(row=rr,column=3,value=f'=COUNTIFS({DS}!H2:H238,A{rr},{DS}!Q2:Q238,"GREEN")')
    ws.cell(row=rr,column=4,value=f'=COUNTIFS({DS}!H2:H238,A{rr},{DS}!Q2:Q238,"AMBER")')
    ws.cell(row=rr,column=5,value=f'=COUNTIFS({DS}!H2:H238,A{rr},{DS}!Q2:Q238,"RED")')
    ws.cell(row=rr,column=6,value=f'=E{rr}/B{rr}'); ws.cell(row=rr,column=6).number_format="0.0%"
    for cc in range(1,7): ws.cell(row=rr,column=cc).border=border; ws.cell(row=rr,column=cc).alignment=(left if cc==1 else ctr)
    rr+=1

# SHEET 5: LICENSE & DEMO QUALITY
ws=wb.create_sheet("Licence & Demo Quality")
ws.sheet_view.showGridLines=False
for col,w in zip("ABCD",[26,14,14,50]): ws.column_dimensions[col].width=w
title_row(ws,"Licence Size & Demo Quality vs Target",4,1,14)
sub(ws,"Licence tier distribution (237 demos)",4,3)
kv_header(ws,["Tier","Demos","% of demos","Note"],4)
tnotes={"1-4":"Below the 5+ quality bar — mostly solo/tiny brokers","5-9":"Meets 5+ bar (SMB brokers/small developers)","10-39":"Healthy mid-market","40+":"True enterprise — almost none generated"}
rr=5
for t in ["1-4","5-9","10-39","40+"]:
    ws.cell(row=rr,column=1,value=t).font=font(10,b=True)
    ws.cell(row=rr,column=2,value=f'=COUNTIF({DS}!H2:H238,A{rr})')
    ws.cell(row=rr,column=3,value=f'=B{rr}/237'); ws.cell(row=rr,column=3).number_format="0.0%"
    ws.cell(row=rr,column=4,value=tnotes[t]).alignment=wrap
    for cc in range(1,5): ws.cell(row=rr,column=cc).border=border
    if t=="1-4": ws.cell(row=rr,column=1).fill=fill(RED)
    rr+=1
ws.cell(row=rr,column=1,value="TOTAL").font=font(10,b=True); ws.cell(row=rr,column=2,value="=SUM(B5:B8)").font=font(10,b=True)
for cc in range(1,5): ws.cell(row=rr,column=cc).border=border
rr+=2
sub(ws,"Target check: 200+ demos of 5+ licences",4,rr); rr+=1
kv_header(ws,["Segment","Demos","% of demos","Verdict vs target"],rr); rr+=1
ws.cell(row=rr,column=1,value="5+ licence demos (the target metric)").font=font(10,b=True)
ws.cell(row=rr,column=2,value=f'=COUNTIF({DS}!I2:I238,"Yes")')
ws.cell(row=rr,column=3,value=f'=B{rr}/237'); ws.cell(row=rr,column=3).number_format="0.0%"
ws.cell(row=rr,column=4,value="Target was 200+. Achieved ~138 → MISSED by ~31%").alignment=wrap
ws.cell(row=rr,column=1).fill=fill(RED)
for cc in range(1,5): ws.cell(row=rr,column=cc).border=border
rr+=1
ws.cell(row=rr,column=1,value="<5 licence demos (1-4)").font=font(10,b=True)
ws.cell(row=rr,column=2,value=f'=COUNTIF({DS}!I2:I238,"No")')
ws.cell(row=rr,column=3,value=f'=B{rr}/237'); ws.cell(row=rr,column=3).number_format="0.0%"
ws.cell(row=rr,column=4,value="Effort spent on sub-scale prospects").alignment=wrap
for cc in range(1,5): ws.cell(row=rr,column=cc).border=border

# SHEET 6: CITY ANALYSIS
ws=wb.create_sheet("City Analysis")
ws.sheet_view.showGridLines=False
for col,w in zip("ABCDE",[22,12,12,12,40]): ws.column_dimensions[col].width=w
title_row(ws,"City Analysis — Main-6 Rep Cities vs Rest",5,1,14)
sub(ws,"Main-6 (has a physical sales rep) vs Other",5,3)
kv_header(ws,["Bucket","Demos","Won","Win %","Read"],4)
rr=5
for b,read in [("Main6","6 cities with reps — should convert best & allow onsite"),("Other","No local rep — onsite hard, weaker conversion"),("Unknown","City not captured")]:
    ws.cell(row=rr,column=1,value=b).font=font(10,b=True)
    ws.cell(row=rr,column=2,value=f'=COUNTIF({DS}!K2:K238,A{rr})')
    ws.cell(row=rr,column=3,value=f'=COUNTIFS({DS}!K2:K238,A{rr},{DS}!F2:F238,"Won")')
    ws.cell(row=rr,column=4,value=f'=IF(B{rr}=0,0,C{rr}/B{rr})'); ws.cell(row=rr,column=4).number_format="0.0%"
    ws.cell(row=rr,column=5,value=read).alignment=wrap
    for cc in range(1,6): ws.cell(row=rr,column=cc).border=border
    rr+=1
rr+=1
sub(ws,"Main-6 city breakdown (demos & wins)",5,rr); rr+=1
kv_header(ws,["City","Demos","Won","Win %",""],rr); rr+=1
m6=S["main6_breakdown"]; m6w=S.get("main6_won",{})
for city in ["Pune","Mumbai/Thane","Delhi/NCR","Bangalore","Chennai","Hyderabad"]:
    dem=m6.get(city,0); won=m6w.get(city,0)
    ws.cell(row=rr,column=1,value=city).font=font(10,b=True)
    ws.cell(row=rr,column=2,value=dem); ws.cell(row=rr,column=3,value=won)
    ws.cell(row=rr,column=4,value=(won/dem if dem else 0)); ws.cell(row=rr,column=4).number_format="0.0%"
    for cc in range(1,6): ws.cell(row=rr,column=cc).border=border; ws.cell(row=rr,column=cc).alignment=(left if cc==1 else ctr)
    rr+=1
rr+=1
sub(ws,"Top cities by demo volume (all)",5,rr); rr+=1
kv_header(ws,["City","Demos","","",""],rr); rr+=1
for city,cnt in list(S["top_cities"].items())[:15]:
    ws.cell(row=rr,column=1,value=city); ws.cell(row=rr,column=2,value=cnt)
    for cc in range(1,3): ws.cell(row=rr,column=cc).border=border; ws.cell(row=rr,column=cc).alignment=(left if cc==1 else ctr)
    rr+=1

# SHEET 7: ONSITE vs ONLINE
ws=wb.create_sheet("Onsite vs Online")
ws.sheet_view.showGridLines=False
for col,w in zip("ABCDE",[20,12,12,12,55]): ws.column_dimensions[col].width=w
title_row(ws,"Onsite vs Online Demos (the offline-model gap)",5,1,14)
sub(ws,"Demo mode",5,3)
kv_header(ws,["Mode","Demos","% of demos","Won","Read"],4)
rr=5
for m,read in [("Onsite","In-person / office visit — the intended model"),("Online","Tele/online demo"),("Unknown","No signal in notes")]:
    ws.cell(row=rr,column=1,value=m).font=font(10,b=True)
    ws.cell(row=rr,column=2,value=f'=COUNTIF({DS}!M2:M238,A{rr})')
    ws.cell(row=rr,column=3,value=f'=B{rr}/237'); ws.cell(row=rr,column=3).number_format="0.0%"
    ws.cell(row=rr,column=4,value=f'=COUNTIFS({DS}!M2:M238,A{rr},{DS}!F2:F238,"Won")')
    ws.cell(row=rr,column=5,value=read).alignment=wrap
    for cc in range(1,6): ws.cell(row=rr,column=cc).border=border
    rr+=1
ws.cell(row=rr+1,column=1,value="Takeaway: only ~13% of demos were in-person. Sell.Do's differentiator is offline, on-ground selling; pre-sales is running an almost fully tele-demo motion. Onsite demos also skew to Main-6 cities where reps physically sit.").font=font(10,italic=True); ws.merge_cells(start_row=rr+1,start_column=1,end_row=rr+1,end_column=5); ws.row_dimensions[rr+1].height=44; ws.cell(row=rr+1,column=1).alignment=wrap

# SHEET 8: WHY DEALS STALLED
ws=wb.create_sheet("Why Deals Stalled")
ws.sheet_view.showGridLines=False
for col,w in zip("ABCD",[26,12,12,60]): ws.column_dimensions[col].width=w
title_row(ws,"Why Deals Didn't Move — Blockers & Ownership",4,1,14)
sub(ws,"Primary blocker (237 demos)",4,3)
kv_header(ws,["Blocker","Count","% ","What it means"],4)
bl_notes={"Quality/ICP":"Wrong-fit prospect (sub-scale / not a buyer)","Non-responsive":"Went dark after demo","Progressing":"Still live in pipeline","Competitor/Existing-CRM":"Chose/kept a rival tool","Timeline/Not-now":"Deferred purchase","Won":"Closed-won","BANT-weak":"Thin budget/authority/need/timeline","Budget":"Price/affordability","Sales-gap":"Sales follow-up/execution gap","Pre-sales-gap":"Pre-sales mistake surfaced later","Product/Pricing":"Lost on product or price fit"}
order=["Quality/ICP","Non-responsive","Progressing","Competitor/Existing-CRM","Timeline/Not-now","Won","BANT-weak","Budget","Sales-gap","Pre-sales-gap","Product/Pricing"]
rr=5
for b in order:
    ws.cell(row=rr,column=1,value=b).font=font(10,b=True)
    ws.cell(row=rr,column=2,value=f'=COUNTIF({DS}!S2:S238,A{rr})')
    ws.cell(row=rr,column=3,value=f'=B{rr}/237'); ws.cell(row=rr,column=3).number_format="0.0%"
    ws.cell(row=rr,column=4,value=bl_notes.get(b,"")).alignment=wrap
    for cc in range(1,5): ws.cell(row=rr,column=cc).border=border
    rr+=1
rr+=1
sub(ws,"Who owns the blocker?",4,rr); rr+=1
kv_header(ws,["Owner","Count","%","Read"],rr); rr+=1
own_notes={"Customer":"Buyer-side (budget/timeline/no-response) — often unavoidable","Pre-sales":"Pre-sales let a weak deal through (fixable at source)","Sales":"Sales execution/follow-up gap","Product/Pricing":"Lost on product or price","NA-Won":"Won deals"}
for o in ["Customer","Pre-sales","Sales","Product/Pricing","NA-Won"]:
    ws.cell(row=rr,column=1,value=o).font=font(10,b=True)
    ws.cell(row=rr,column=2,value=f'=COUNTIF({DS}!T2:T238,A{rr})')
    ws.cell(row=rr,column=3,value=f'=B{rr}/237'); ws.cell(row=rr,column=3).number_format="0.0%"
    ws.cell(row=rr,column=4,value=own_notes[o]).alignment=wrap
    for cc in range(1,5): ws.cell(row=rr,column=cc).border=border
    if o=="Pre-sales": ws.cell(row=rr,column=1).fill=fill(AMB)
    rr+=1

# ---- filtered list sheets ----
def list_sheet(name,title,headers,widths,recs,color_col=None):
    ws=wb.create_sheet(name); ws.freeze_panes="A2"
    for i,w in enumerate(widths): ws.column_dimensions[get_column_letter(i+1)].width=w
    for i,h in enumerate(headers):
        c=ws.cell(row=1,column=i+1,value=h); c.font=hfont(9,WHITE,True); c.fill=fill(BLUE); c.alignment=ctrw; c.border=border
    ws.row_dimensions[1].height=28
    for ri,rec in enumerate(recs,start=2):
        for ci,v in enumerate(rec,start=1):
            c=ws.cell(row=ri,column=ci,value=v); c.border=border; c.font=font(9)
            c.alignment=wrap if widths[ci-1]>=40 else (left if ci in(2,) else ctr)
        if color_col:
            vi=color_col-1; vd=str(rec[vi])
            cc=ws.cell(row=ri,column=color_col)
            if vd in("GREEN","AMBER","RED"): cc.fill=fill({"GREEN":GREEN,"AMBER":AMB,"RED":RED}[vd]); cc.font=font(9,{"GREEN":GREENF,"AMBER":AMBF,"RED":REDF}[vd],True)
    return ws

# SHEET 9: Enterprise & 40+
big=[r for r in rows if (r["noOfLicenses"] or 0)>=10 or r["enterprise_flag"] in (True,"true","True")]
big.sort(key=lambda x:-(x["noOfLicenses"] or 0))
recs=[[r["deal_id"],r["deal_name"],r["noOfLicenses"],r["city_clean"],r["dev_or_broker"],r["pre_sales_verdict"],r["stage"],r["owner"],r["one_line"]] for r in big]
list_sheet("Enterprise & 10+","Enterprise / 10+ licence deals",
  ["Deal ID","Name","Lic","City","Dev/Broker","Verdict","Stage","Owner","CRO one-line"],
  [10,22,7,15,13,9,17,16,70],recs,color_col=6)

# SHEET 10: Won
wonrecs=[[w["id"],w["name"],w["lic"],w["city"],w["val"],w["creator"],w["owner"]] for w in sorted(S["won_deals"],key=lambda x:-(x["val"] or 0))]
list_sheet("Won Deals","Won / Booked deals (June demos)",
  ["Deal ID","Name","Lic","City","Value (INR)","Creator","Sales Owner"],
  [10,22,7,16,13,15,18],wonrecs)

# SHEET 11: RED deals
reds=[r for r in rows if r["pre_sales_verdict"]=="RED"]
reds.sort(key=lambda x:(x["creator"],-(x["noOfLicenses"] or 0)))
redrecs=[[r["deal_id"],r["deal_name"],r["creator"],r["noOfLicenses"],r["city_clean"],r["dev_or_broker"],r["stall_blocker"],r["one_line"]] for r in reds]
list_sheet("RED Deals (47)","RED pre-sales demos — should not have been booked / poorly qualified",
  ["Deal ID","Name","Creator","Lic","City","Dev/Broker","Blocker","Why RED (CRO one-line)"],
  [10,22,15,6,15,13,16,80],redrecs)

# SHEET 12: Creator scorecard
ws=wb.create_sheet("Creator Scorecard")
ws.sheet_view.showGridLines=False
for col,w in zip("ABCDEFGHI",[20,10,12,10,10,10,12,12,12]): ws.column_dimensions[col].width=w
title_row(ws,"Per-Rep Scorecard (Pre-Sales)",9,1,14)
kv_header(ws,["Rep","Created","Demos","Demo%","GREEN","RED","%GREEN","5+ demos","Onsite"],3)
cvd=S["created_vs_demo"]; per=S["per_creator"]
rr=4
for cr in ["Revati Ambike","Ashwini Nirmal","Gayatri More"]:
    p=per[cr]; created=cvd[cr]["created"]
    vals=[cr,created,p["demos"],p["demos"]/created,p["GREEN"],p["RED"],p["GREEN"]/p["demos"] if p["demos"] else 0,p["5plus"],p["onsite"]]
    for ci,v in enumerate(vals,start=1):
        c=ws.cell(row=rr,column=ci,value=v); c.border=border; c.font=font(10,b=(ci==1)); c.alignment=(left if ci==1 else ctr)
    ws.cell(row=rr,column=4).number_format="0.0%"; ws.cell(row=rr,column=7).number_format="0.0%"
    rr+=1
ws.cell(row=rr,column=1,value="TOTAL").font=font(10,b=True)
tv=[cvd["TOTAL"]["created"],cvd["TOTAL"]["demo"],cvd["TOTAL"]["demo"]/cvd["TOTAL"]["created"],93,47,93/237,138,30]
for ci,v in enumerate(tv,start=2):
    c=ws.cell(row=rr,column=ci,value=v); c.border=border; c.font=font(10,b=True); c.alignment=ctr
ws.cell(row=rr,column=4).number_format="0.0%"; ws.cell(row=rr,column=7).number_format="0.0%"
ws.cell(row=rr+2,column=1,value="Note: 'Created' = all deals stamped by the rep in June; 'Demos' = those with a demo conducted (the 237). Demo% is the conversion from created → conducted; the gap is created deals where no demo happened.").font=font(9,italic=True)
ws.merge_cells(start_row=rr+2,start_column=1,end_row=rr+2,end_column=9); ws.cell(row=rr+2,column=1).alignment=wrap; ws.row_dimensions[rr+2].height=40

wb.save(BASE+"/Presales_June_PostMortem.xlsx")
print("saved workbook with sheets:",wb.sheetnames)
