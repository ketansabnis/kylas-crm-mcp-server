import json
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
BASE="/sessions/gifted-happy-euler/mnt/kylas-crm-mcp-server/presales_june_analysis"
rows=json.load(open(BASE+"/master_dataset.json"))
A=json.load(open(BASE+"/analytics_v2.json"))
C=json.load(open(BASE+"/closures_analytics.json"))
MODEL=json.load(open(BASE+"/model_weights.json"))
DS="'Deals (253)'"; N=len(rows); r2=N+1
NAVY="1F3864"; BLUE="2E5496"; TEAL="1F6E6E"; LTBLUE="D6E0F0"; GREY="F2F2F2"
GREEN="C6EFCE"; GREENF="006100"; AMB="FFEB9C"; AMBF="9C6500"; RED="FFC7CE"; REDF="9C0006"; WHITE="FFFFFF"; GOLD="FFF2CC"
thin=Side(style="thin",color="BFBFBF"); border=Border(left=thin,right=thin,top=thin,bottom=thin)
def hf(sz=11,c=WHITE,b=True): return Font(name="Arial",size=sz,bold=b,color=c)
def f(sz=10,c="000000",b=False,it=False): return Font(name="Arial",size=sz,bold=b,color=c,italic=it)
wrap=Alignment(wrap_text=True,vertical="top"); ctr=Alignment(horizontal="center",vertical="center")
ctrw=Alignment(horizontal="center",vertical="center",wrap_text=True); left=Alignment(horizontal="left",vertical="center")
wb=Workbook()
def title(ws,t,span,row=1,sz=14,c=NAVY):
    cell=ws.cell(row=row,column=1,value=t); cell.font=hf(sz,WHITE,True); cell.fill=PatternFill("solid",fgColor=c)
    cell.alignment=Alignment(horizontal="left",vertical="center"); ws.merge_cells(start_row=row,start_column=1,end_row=row,end_column=span); ws.row_dimensions[row].height=26
def band(ws,t,span,row,c=BLUE):
    cell=ws.cell(row=row,column=1,value=t); cell.font=hf(11,WHITE,True); cell.fill=PatternFill("solid",fgColor=c)
    cell.alignment=left; ws.merge_cells(start_row=row,start_column=1,end_row=row,end_column=span); ws.row_dimensions[row].height=20
def head(ws,hs,row,c=BLUE,start=1):
    for i,h in enumerate(hs):
        x=ws.cell(row=row,column=start+i,value=h); x.font=hf(10,WHITE,True); x.fill=PatternFill("solid",fgColor=c); x.alignment=ctrw; x.border=border
def cellv(ws,row,col,v,bold=False,al=None,fillc=None,fc="000000",nf=None):
    x=ws.cell(row=row,column=col,value=v); x.border=border; x.font=f(10,fc,bold); x.alignment=al or ctr
    if fillc: x.fill=PatternFill("solid",fgColor=fillc)
    if nf: x.number_format=nf
    return x
def vfill(v): return {"GREEN":GREEN,"AMBER":AMB,"RED":RED}.get(v)
def vfont(v): return {"GREEN":GREENF,"AMBER":AMBF,"RED":REDF}.get(v,"000000")

# ---------- Read Me ----------
ws=wb.active; ws.title="Read Me"; ws.sheet_view.showGridLines=False
ws.column_dimensions["A"].width=27; ws.column_dimensions["B"].width=122
title(ws,"Pre-Sales June 2026 — Demo Quality Post-Mortem (v2: demos CONDUCTED in June)",2,1,14)
info=[
 ("Universe","253 demos whose Meeting-Conducted date falls in June 2026, created by the Pre-sales team (Revati/Ashwini/Gayatri). This is 'demos DONE in June', not 'deals created in June'."),
 ("Why 253 vs 241","The CRM list view used a 17:00 cut-off on 1-Jun & 30-Jun; full calendar-June (00:00-23:59) = 253. Same filter otherwise (Created-By team = Pre-sales)."),
 ("Target judged","200+ demos of 5+ user licences. Achieved 146 → still missed (~73%)."),
 ("Headline finding","Qualification quality, not volume, is the whole game: GREEN demos win 24.5%, AMBER 1.0%, RED 0%. All 25 wins came from GREEN/Strong-BANT deals. The 57 RED + 98 AMBER demos (61% of effort) produced 1 win between them."),
 ("Verdict meaning","pre_sales_verdict judges PRE-SALES work only. GREEN=genuinely qualified; AMBER=real but thin; RED=poor/sub-ICP (shouldn't have been booked)."),
 ("city_bucket","Main6 = 6 cities with a physical rep (Pune, Mumbai, Delhi/NCR, Bangalore, Chennai, Hyderabad). Other = elsewhere."),
 ("Data","master_dataset.csv/.json = 253-row data; analytics_v2.json = every cross-tab; deals/<id>.json = per-deal record incl. notes."),
]
r=3
for k,v in info:
    a=ws.cell(row=r,column=1,value=k); a.font=f(10,NAVY,True); a.alignment=Alignment(vertical="top",wrap_text=True)
    b=ws.cell(row=r,column=2,value=v); b.font=f(10); b.alignment=wrap
    ws.row_dimensions[r].height=42 if len(v)>110 else 26; r+=1

# ---------- Scorecard ----------
ws=wb.create_sheet("Scorecard"); ws.sheet_view.showGridLines=False
for c,w in zip("ABCDE",[44,13,13,14,66]): ws.column_dimensions[c].width=w
title(ws,"Executive Scorecard — 253 demos conducted in June",5,1,14)
head(ws,["Metric","Value","Denom","%","Read"],3)
def scr(row,m,val,den,pctf,read,flag=None):
    cellv(ws,row,1,m,True,left); cellv(ws,row,2,val); cellv(ws,row,3,den);
    c4=cellv(ws,row,4,pctf,nf="0.0%"); cellv(ws,row,5,read,al=wrap)
    if flag: ws.cell(row=row,column=2).fill=PatternFill("solid",fgColor=flag[0]); ws.cell(row=row,column=2).font=f(10,flag[1],True)
    ws.row_dimensions[row].height=30
r=4
scr(r,"Demos conducted in June",253,"","", "Full-month; the report universe"); ws.cell(row=r,column=4).value=None; r+=1
scr(r,"TARGET: demos of 5+ licences",146,200,"=B{}/C{}".format(r,r),"Target 200+ → MISSED (~73%). 107 demos were 1-4 seats.",(RED,REDF)); r+=1
scr(r,"Pre-sales quality: GREEN",98,253,"=B{}/C{}".format(r,r),"Genuinely qualified — and where ~all revenue comes from",(GREEN,GREENF)); r+=1
scr(r,"Pre-sales quality: AMBER",98,253,"=B{}/C{}".format(r,r),"Real but thin — converted just 1.0%",(AMB,AMBF)); r+=1
scr(r,"Pre-sales quality: RED",57,253,"=B{}/C{}".format(r,r),"Poor/sub-ICP — converted 0.0%",(RED,REDF)); r+=1
scr(r,"Won / booked",25,253,"=B{}/C{}".format(r,r),"₹29.4L booked. 53% still open, 37% lost"); r+=1
scr(r,"Revenue booked (INR)",2938999,"","","All 25 wins; avg ~₹1.18L/deal"); ws.cell(row=r,column=4).value=None; ws.cell(row=r,column=2).number_format="#,##0"; r+=1
scr(r,"Onsite (in-person) demos",33,253,"=B{}/C{}".format(r,r),"Only 13% in-person; onsite wins 15.2% vs online 9.1%",(RED,REDF)); r+=1
scr(r,"Demos in Main-6 rep cities",172,253,"=B{}/C{}".format(r,r),"68% in rep cities; 32% off-territory"); r+=1
scr(r,"True enterprise (40+ seats)",5,253,"=B{}/C{}".format(r,r),"Enterprise pipeline still near-absent",(RED,REDF)); r+=1
scr(r,"GREEN win-rate vs AMBER vs RED","24.5%","1.0% / 0%","","THE signal: quality predicts revenue almost perfectly",(GREEN,GREENF)); ws.cell(row=r,column=4).value=None; r+=1

# ---------- Deals (253) ----------
ws=wb.create_sheet("Deals (253)"); ws.freeze_panes="C2"
cols=[("Deal ID",10),("Deal Name",21),("Creator",14),("Sales Owner",16),("Stage",16),("Status",8),("Lic",5),("Tier",7),("5+?",5),
 ("City",15),("Main-6",13),("Bucket",8),("Dev/Broker",12),("Onsite/Online",12),("Name OK",7),("BANT",5),("BANT Flag",9),
 ("Verdict",9),("Blocker",16),("Blocker Owner",12),("Won Value",10),("CRO one-line",64),("Notes (raw)",80)]
for i,(h,w) in enumerate(cols):
    ws.column_dimensions[get_column_letter(i+1)].width=w
    x=ws.cell(row=1,column=i+1,value=h); x.font=hf(9,WHITE,True); x.fill=PatternFill("solid",fgColor=BLUE); x.alignment=ctrw; x.border=border
ws.row_dimensions[1].height=30
def yn(v): return "Yes" if v in(True,"true","True") else ("No" if v in(False,"false","False") else "")
for ri,d in enumerate(rows,start=2):
    st="Won" if d["is_won"] else ("Lost" if d["is_lost"] else "Open")
    vals=[d["deal_id"],d["deal_name"],d["creator"],d["owner"],d["stage"],st,d["noOfLicenses"],d["license_tier"],
     ("Yes" if d["is_5plus"] else "No"),d["city_clean"],d["main6"],d["city_bucket"],d["dev_or_broker"],d["onsite_or_online"],
     yn(d["name_valid"]),d["bant_score"],d["bant_flag"],d["pre_sales_verdict"],d["stall_blocker"],d["blocker_owner"],
     (d["actualValue"] if d["is_won"] else None),d["one_line"],(d["notes_text"] or "")[:800]]
    for ci,v in enumerate(vals,start=1):
        x=ws.cell(row=ri,column=ci,value=v); x.border=border; x.font=f(9)
        x.alignment=wrap if ci in(3,22,23) else (left if ci in(4,5,10,11,13,19,20) else ctr)
    vc=ws.cell(row=ri,column=18); vd=d["pre_sales_verdict"]
    if vfill(vd): vc.fill=PatternFill("solid",fgColor=vfill(vd)); vc.font=f(9,vfont(vd),True)
    sc=ws.cell(row=ri,column=6)
    if st=="Won": sc.fill=PatternFill("solid",fgColor=GREEN); sc.font=f(9,GREENF,True)
    elif st=="Lost": sc.fill=PatternFill("solid",fgColor=RED); sc.font=f(9,REDF,True)
ws.auto_filter.ref=f"A1:W{r2}"

# ---------- What Converts ----------
ws=wb.create_sheet("What Converts"); ws.sheet_view.showGridLines=False
for c,w in zip("ABCDEFG",[26,10,10,11,10,11,40]): ws.column_dimensions[c].width=w
title(ws,"What Actually Converts — win-rate by every cut",7,1,14,TEAL)
def wtable(row,label,data,keyname,note_map=None,highlight=None):
    band(ws,label,7,row); head(ws,[keyname,"Demos","Won","Win %","GREEN","%GREEN","Note"],row+1)
    rr=row+2
    for x in data:
        cellv(ws,rr,1,x["key"],True,left); cellv(ws,rr,2,x["demos"]); cellv(ws,rr,3,x["won"])
        cellv(ws,rr,4,x["win_rate"],nf="0.0%"); cellv(ws,rr,5,x["green"]); cellv(ws,rr,6,x["green_rate"],nf="0.0%")
        cellv(ws,rr,7,(note_map or {}).get(x["key"],""),al=wrap)
        if highlight and x["key"] in highlight:
            for cc in range(1,8): ws.cell(row=rr,column=cc).fill=PatternFill("solid",fgColor=GOLD)
        # color win rate
        if x["win_rate"]>=0.15: ws.cell(row=rr,column=4).font=f(10,GREENF,True)
        elif x["win_rate"]<0.05: ws.cell(row=rr,column=4).font=f(10,REDF,True)
        rr+=1
    return rr+1
r=3
r=wtable(r,"By pre-sales quality verdict (the strongest signal)",A["winrate_by_verdict"],"Verdict",
   {"GREEN":"Genuinely qualified — 24 of 25 wins","AMBER":"Thin — 1 win in 98","RED":"Sub-ICP — zero wins"},highlight=["GREEN"])
r=wtable(r,"By BANT strength",A["winrate_by_bantflag"],"BANT",
   {"Strong":"All 24 wins here — capturing real BANT IS the job","Partial":"1 win in 82","Weak":"0 wins","None":"0 wins"},highlight=["Strong"])
r=wtable(r,"By account type",A["winrate_by_devbroker"],"Type",
   {"Developer":"Wins 13.3% & 52% GREEN — our best segment","Channel partner":"Wins 7.5% & 29% GREEN — we over-run these"},highlight=["Developer"])
r=wtable(r,"By demo mode",A["winrate_by_onsite"],"Mode",
   {"Onsite":"15.2% win, 58% GREEN, ~3x revenue/demo","Online":"9.1% win — but 87% of demos"},highlight=["Onsite"])
r=wtable(r,"By licence tier (<5 / 5-10 / 10+)",A["winrate_by_tier3"],"Tier",
   {"<5":"6.5% win, 14% GREEN — 42% of demos, low yield","5-10":"12.1% win, 54% GREEN","10+":"13.3% win, 67% GREEN"},highlight=["5-10","10+"])
r=wtable(r,"By pre-sales rep",A["winrate_by_creator"],"Rep",
   {"Revati Ambike":"11.9% win, ₹21.6L, 43% GREEN","Ashwini Nirmal":"7.9% win, ₹7.8L, 34% GREEN"})

# ---------- City Deep-Dive ----------
ws=wb.create_sheet("City Deep-Dive"); ws.sheet_view.showGridLines=False
for c,w in zip("ABCDEFGH",[18,9,8,9,9,8,12,34]): ws.column_dimensions[c].width=w
title(ws,"City Deep-Dive — where we win, where we waste",8,1,14,TEAL)
band(ws,"Main-6 rep cities (demos, wins, quality, revenue)",8,3)
head(ws,["City","Demos","Won","Win %","GREEN","Onsite","Revenue","Read"],4)
m6notes={"Pune":"HQ — 14 demos, 0 wins, 0 GREEN-heavy. Broken at home.","Mumbai/Thane":"Best onsite (36%). Solid.","Delhi/NCR":"Biggest volume, low 7% yield — high effort, thin return.","Bangalore":"22-24 demos, ~6-8% — under-performs.","Chennai":"27% win — best rate, tiny volume. DOUBLE DOWN.","Hyderabad":"24% win, ₹4.9L — 2nd best. DOUBLE DOWN."}
rr=5
rev6=A["revenue_by_main6"]; ons6=A["onsite_by_main6"]
for x in A["winrate_by_main6"]:
    c=x["key"]; cellv(ws,rr,1,c,True,left); cellv(ws,rr,2,x["demos"]); cellv(ws,rr,3,x["won"])
    cellv(ws,rr,4,x["win_rate"],nf="0.0%"); cellv(ws,rr,5,x["green"]); cellv(ws,rr,6,ons6[c]["onsite"])
    cellv(ws,rr,7,rev6[c],nf="#,##0"); cellv(ws,rr,8,m6notes.get(c,""),al=wrap)
    if x["win_rate"]>=0.2:
        for cc in range(1,9): ws.cell(row=rr,column=cc).fill=PatternFill("solid",fgColor=GOLD)
    elif x["won"]==0:
        ws.cell(row=rr,column=4).font=f(10,REDF,True)
    rr+=1
rr+=1
band(ws,"Main-6 vs Other — volume vs yield",8,rr); rr+=1
head(ws,["Bucket","Demos","Won","Win %","GREEN","Onsite","Revenue",""],rr); rr+=1
for x in A["winrate_by_bucket"]:
    if x["key"]=="Unknown": continue
    b=x["key"]; cellv(ws,rr,1,b,True,left); cellv(ws,rr,2,x["demos"]); cellv(ws,rr,3,x["won"])
    cellv(ws,rr,4,x["win_rate"],nf="0.0%"); cellv(ws,rr,5,x["green"]); cellv(ws,rr,6,x["onsite"])
    cellv(ws,rr,7,A["revenue_by_bucket"][b],nf="#,##0"); cellv(ws,rr,8,"")
    rr+=1
rr+=1
band(ws,"All cities by volume — spot the mismatch (high win-rate + low volume = grow here)",8,rr); rr+=1
head(ws,["City","Demos","Won","Win %","GREEN","5+","Onsite","Opportunity flag"],rr); rr+=1
for x in A["top_cities"]:
    cellv(ws,rr,1,x["city"],True,left); cellv(ws,rr,2,x["demos"]); cellv(ws,rr,3,x["won"])
    cellv(ws,rr,4,x["win_rate"],nf="0.0%"); cellv(ws,rr,5,x["green"]); cellv(ws,rr,6,x["5plus"]); cellv(ws,rr,7,x["onsite"])
    flag=""
    if x["demos"]>=8 and x["win_rate"]>=0.18: flag="GROW — high win, add demos"
    elif x["demos"]>=10 and x["win_rate"]<0.05: flag="FIX/CUT — high effort, low yield"
    cellv(ws,rr,8,flag,al=wrap)
    if flag.startswith("GROW"):
        for cc in range(1,9): ws.cell(row=rr,column=cc).fill=PatternFill("solid",fgColor=GOLD)
    elif flag.startswith("FIX"):
        for cc in range(1,9): ws.cell(row=rr,column=cc).fill=PatternFill("solid",fgColor=RED)
    rr+=1

# ---------- Pre-Sales Quality ----------
ws=wb.create_sheet("Pre-Sales Quality"); ws.sheet_view.showGridLines=False
for c,w in zip("ABCDEF",[26,11,11,11,11,11]): ws.column_dimensions[c].width=w
title(ws,"Pre-Sales Quality",6,1,14)
band(ws,"Overall verdict (253 demos)",6,3); head(ws,["Verdict","Count","% demos","Won","Win %",""],4)
rr=5
for v in ["GREEN","AMBER","RED"]:
    x=[y for y in A["winrate_by_verdict"] if y["key"]==v][0]
    cellv(ws,rr,1,v,True,left,vfill(v),vfont(v)); cellv(ws,rr,2,x["demos"]); cellv(ws,rr,3,x["demos"]/253,nf="0.0%")
    cellv(ws,rr,4,x["won"]); cellv(ws,rr,5,x["win_rate"],nf="0.0%"); cellv(ws,rr,6,"")
    rr+=1
rr+=1
band(ws,"Quality by rep",6,rr); head(ws,["Rep","Demos","GREEN","RED","%GREEN","Win %"],rr+1); rr+=2
for cr,p in A["per_creator"].items():
    cellv(ws,rr,1,cr,True,left); cellv(ws,rr,2,p["demos"]); cellv(ws,rr,3,p["GREEN"]); cellv(ws,rr,4,p["RED"])
    cellv(ws,rr,5,p["GREEN"]/p["demos"] if p["demos"] else 0,nf="0.0%"); cellv(ws,rr,6,p["win_rate"],nf="0.0%"); rr+=1
rr+=1
band(ws,"Quality by tier (where REDs come from)",6,rr); head(ws,["Tier","Demos","GREEN","%GREEN","Win %",""],rr+1); rr+=2
for x in A["winrate_by_tier"]:
    cellv(ws,rr,1,x["key"],True,left); cellv(ws,rr,2,x["demos"]); cellv(ws,rr,3,x["green"]); cellv(ws,rr,4,x["green_rate"],nf="0.0%"); cellv(ws,rr,5,x["win_rate"],nf="0.0%"); cellv(ws,rr,6,"")
    rr+=1

# ---------- Why Deals Stalled ----------
ws=wb.create_sheet("Why Deals Stalled"); ws.sheet_view.showGridLines=False
for c,w in zip("ABCD",[26,11,10,58]): ws.column_dimensions[c].width=w
title(ws,"Why Deals Didn't Move",4,1,14)
band(ws,"Primary blocker",4,3); head(ws,["Blocker","Count","%","Meaning"],4)
bln={"Quality/ICP":"Wrong-fit prospect","Non-responsive":"Went dark post-demo","Progressing":"Still live","Competitor/Existing-CRM":"Chose/kept a rival","Timeline/Not-now":"Deferred","Won":"Closed-won","BANT-weak":"Thin BANT","Budget":"Price/affordability","Sales-gap":"Sales follow-up gap","Pre-sales-gap":"Pre-sales error","Product/Pricing":"Lost on product/price"}
rr=5
for k,v in sorted(A["blocker"].items(),key=lambda kv:-kv[1]):
    cellv(ws,rr,1,k,True,left); cellv(ws,rr,2,v); cellv(ws,rr,3,v/253,nf="0.0%"); cellv(ws,rr,4,bln.get(k,""),al=wrap); rr+=1
rr+=1
band(ws,"Who owns the blocker?",4,rr); head(ws,["Owner","Count","%","Read"],rr+1); rr+=2
own={"Customer":"Buyer-side (budget/timeline/no-response)","Pre-sales":"Weak deal let through — fixable at source","Sales":"Execution/follow-up gap","Product/Pricing":"Lost on product/price","NA-Won":"Won"}
for k,v in sorted(A["blocker_owner"].items(),key=lambda kv:-kv[1]):
    cellv(ws,rr,1,k,True,left); cellv(ws,rr,2,v); cellv(ws,rr,3,v/253,nf="0.0%"); cellv(ws,rr,4,own.get(k,""),al=wrap)
    if k=="Pre-sales": ws.cell(row=rr,column=1).fill=PatternFill("solid",fgColor=AMB)
    rr+=1

# ---------- filtered lists ----------
def lst(name,ttl,hs,ws_widths,recs,color=None):
    ws=wb.create_sheet(name); ws.freeze_panes="A2"
    for i,w in enumerate(ws_widths): ws.column_dimensions[get_column_letter(i+1)].width=w
    for i,h in enumerate(hs):
        x=ws.cell(row=1,column=i+1,value=h); x.font=hf(9,WHITE,True); x.fill=PatternFill("solid",fgColor=BLUE); x.alignment=ctrw; x.border=border
    ws.row_dimensions[1].height=26
    for ri,rec in enumerate(recs,start=2):
        for ci,v in enumerate(rec,start=1):
            x=ws.cell(row=ri,column=ci,value=v); x.border=border; x.font=f(9); x.alignment=wrap if ws_widths[ci-1]>=40 else (left if ci==2 else ctr)
        if color:
            vd=str(rec[color-1]); cc=ws.cell(row=ri,column=color)
            if vfill(vd): cc.fill=PatternFill("solid",fgColor=vfill(vd)); cc.font=f(9,vfont(vd),True)
    return ws
big=[r for r in rows if (r["noOfLicenses"] or 0)>=10 or r["enterprise_flag"] in(True,"true","True")]
big.sort(key=lambda x:-(x["noOfLicenses"] or 0))
lst("Enterprise & 10+","Enterprise / 10+ licence deals",["Deal ID","Name","Lic","City","Dev/Broker","Verdict","Stage","Owner","CRO one-line"],
   [10,21,6,14,12,9,15,15,66],[[r["deal_id"],r["deal_name"],r["noOfLicenses"],r["city_clean"],r["dev_or_broker"],r["pre_sales_verdict"],r["stage"],r["owner"],r["one_line"]] for r in big],color=6)
wonrecs=[[w["id"],w["name"],w["lic"],w["city"],w["bucket"],w["val"],w["onsite"],w["dev_broker"],w["creator"],w["owner"]] for w in A["won_deals"]]
lst("Won Deals","Won / booked (25) — sorted by value",["Deal ID","Name","Lic","City","Bucket","Value INR","Mode","Dev/Broker","Creator","Owner"],
   [10,20,6,14,9,11,9,12,14,16],wonrecs)
reds=[r for r in rows if r["pre_sales_verdict"]=="RED"]; reds.sort(key=lambda x:(x["creator"],-(x["noOfLicenses"] or 0)))
lst("RED Deals","RED pre-sales demos — sub-ICP / shouldn't have been booked",["Deal ID","Name","Creator","Lic","City","Dev/Broker","Blocker","Why RED"],
   [10,21,14,6,14,12,15,74],[[r["deal_id"],r["deal_name"],r["creator"],r["noOfLicenses"],r["city_clean"],r["dev_or_broker"],r["stall_blocker"],r["one_line"]] for r in reds])
# ---------- Revenue (Closures) ----------
ws=wb.create_sheet("Revenue (Closures)"); ws.sheet_view.showGridLines=False
for c,w in zip("ABCDE",[24,12,14,13,40]): ws.column_dimensions[c].width=w
title(ws,"Real June Revenue — 42 deals CLOSED in June (any demo date)",5,1,14,TEAL)
band(ws,"Headline",5,3)
cellv(ws,4,1,"Closures (won in June)",True,left); cellv(ws,4,2,C["n_closures"]); cellv(ws,4,3,"",); cellv(ws,4,4,""); cellv(ws,4,5,"vs only 25 wins from June-demos — closures are the true revenue lens",al=wrap)
cellv(ws,5,1,"Billed / booked (INR)",True,left); cellv(ws,5,2,C["total_billed"],nf="#,##0"); cellv(ws,5,3,"collected:"); cellv(ws,5,4,C["total_received"],nf="#,##0"); cellv(ws,5,5,"~73% cash-collected",al=wrap)
cellv(ws,6,1,"Avg demo-to-close (days, est.)",True,left); cellv(ws,6,2,C["avg_close_days_overall"]); cellv(ws,6,3,"median"); cellv(ws,6,4,C["median_close_days"]); cellv(ws,6,5,"Estimated — connector doesn't expose exact close date (proxy: won-stage timestamp)",al=wrap)
rr=8
band(ws,"By account type — developers dominate revenue AND close faster",5,rr); head(ws,["Type","Deals","Revenue INR","Avg days",""],rr+1); rr+=2
for k in ["Developer","Channel partner"]:
    v=C["by_devbroker"].get(k,{"deals":0,"revenue":0,"avg_days":None})
    cellv(ws,rr,1,k,True,left); cellv(ws,rr,2,v["deals"]); cellv(ws,rr,3,v["revenue"],nf="#,##0"); cellv(ws,rr,4,v["avg_days"]); cellv(ws,rr,5,"")
    if k=="Developer":
        for cc in range(1,6): ws.cell(row=rr,column=cc).fill=PatternFill("solid",fgColor=GOLD)
    rr+=1
rr+=1
band(ws,"By deal size",5,rr); head(ws,["Tier","Deals","Revenue INR","Avg days",""],rr+1); rr+=2
for k in ["<5","5-10","10+"]:
    v=C["by_tier3"].get(k,{"deals":0,"revenue":0,"avg_days":None})
    cellv(ws,rr,1,k,True,left); cellv(ws,rr,2,v["deals"]); cellv(ws,rr,3,v["revenue"],nf="#,##0"); cellv(ws,rr,4,v["avg_days"]); cellv(ws,rr,5,""); rr+=1
rr+=1
band(ws,"By city",5,rr); head(ws,["City","Deals","Revenue INR","Avg days",""],rr+1); rr+=2
for k,v in sorted(C["by_main6"].items(),key=lambda kv:-kv[1]["revenue"]):
    cellv(ws,rr,1,k,True,left); cellv(ws,rr,2,v["deals"]); cellv(ws,rr,3,v["revenue"],nf="#,##0"); cellv(ws,rr,4,v["avg_days"]); cellv(ws,rr,5,""); rr+=1
rr+=1
band(ws,"Top 15 closed deals",5,rr); head(ws,["Deal","City","Lic","Type","Billed INR"],rr+1); rr+=2
for x in C["top_deals"]:
    cellv(ws,rr,1,x["name"],True,left); cellv(ws,rr,2,x["city"],al=left); cellv(ws,rr,3,x["lic"]); cellv(ws,rr,4,x["dev_broker"],al=left); cellv(ws,rr,5,x["billed"],nf="#,##0"); rr+=1

# ---------- Marketing Source ----------
ws=wb.create_sheet("Marketing Source"); ws.sheet_view.showGridLines=False
for c,w in zip("ABCDEF",[26,10,10,10,10,40]): ws.column_dimensions[c].width=w
title(ws,"Top-of-Funnel — demos & conversion by SOURCE",6,1,14,TEAL)
band(ws,"Where the 253 demos came from, and which source converts",6,3)
head(ws,["Source","Demos","% 5+","Won","Win %","Read"],4)
srcnote={"Organic":"Champion — highest volume & win-rate. Invest SEO/content/brand.","Google":"Best size mix (66% 5+). Scale paid search.","Facebook":"47 demos, 1 win — 4-5x worse. Fix targeting or cut.","Sell.Do Interakt (WhatsApp)":"Decent inbound WA channel.","Instagram":"Negligible & 0 wins.","Outreach":"n=1","My operator":"n=1"}
rr=5
for s,v in sorted(C["source_funnel"].items(),key=lambda kv:-kv[1]["demos"]):
    cellv(ws,rr,1,s,True,left); cellv(ws,rr,2,v["demos"]); cellv(ws,rr,3,v["fiveplus_rate"],nf="0%"); cellv(ws,rr,4,v["won"]); cellv(ws,rr,5,v["win_rate"],nf="0.0%"); cellv(ws,rr,6,srcnote.get(s,""),al=wrap)
    if s=="Facebook":
        for cc in range(1,7): ws.cell(row=rr,column=cc).fill=PatternFill("solid",fgColor=RED)
    elif s in("Organic","Google"):
        for cc in range(1,7): ws.cell(row=rr,column=cc).fill=PatternFill("solid",fgColor=GOLD)
    rr+=1
rr+=1
cellv(ws,rr,1,"Campaign field usable? NO — only 1 of 253 demos has a campaign tagged. UTM fields empty. Source is the only reliable attribution; fix campaign/UTM capture to measure ad spend properly.",al=wrap)
ws.merge_cells(start_row=rr,start_column=1,end_row=rr,end_column=6); ws.row_dimensions[rr].height=44; ws.cell(row=rr,column=1).font=f(10,REDF,True)

# ---------- Convert Model ----------
ws=wb.create_sheet("Convert Model"); ws.sheet_view.showGridLines=False
for c,w in zip("ABCDE",[22,14,14,14,42]): ws.column_dimensions[c].width=w
title(ws,"Conversion-Probability Model — for the hourly CRON",5,1,14,TEAL)
cellv(ws,2,1,"score = base + sum(feature weights) [+ source]. probability = 1/(1+e^-score). Fitted on 253 June demos. Files: model_weights.json + score_deal.py (drop-in, no dependencies).",al=wrap)
ws.merge_cells(start_row=2,start_column=1,end_row=2,end_column=5); ws.row_dimensions[2].height=30
rr=4
band(ws,"Feature weights (log-odds; + = more likely to convert)",5,rr); head(ws,["Feature","Value","Weight","",""],rr+1); rr+=2
for fname,d in MODEL["feature_log_lr"].items():
    for v,wt in sorted(d.items(),key=lambda kv:-kv[1]):
        cellv(ws,rr,1,fname,True,left); cellv(ws,rr,2,v,al=left); cellv(ws,rr,3,round(wt,2)); cellv(ws,rr,4,""); cellv(ws,rr,5,"")
        ws.cell(row=rr,column=3).font=f(10,GREENF if wt>0 else REDF,True); rr+=1
rr+=1
band(ws,"Marketing source adjustment (optional add-on)",5,rr); head(ws,["Source","Weight","","",""],rr+1); rr+=2
for s,wt in sorted(MODEL["source_log_lr_optional"].items(),key=lambda kv:-kv[1]):
    cellv(ws,rr,1,s,True,left); cellv(ws,rr,2,round(wt,2)); ws.cell(row=rr,column=2).font=f(10,GREENF if wt>0 else REDF,True); cellv(ws,rr,3,""); cellv(ws,rr,4,""); cellv(ws,rr,5,""); rr+=1
rr+=1
band(ws,"Calibration — predicted vs actual (quintiles, 253 demos)",5,rr); head(ws,["Band","n","Predicted","Actual",""],rr+1); rr+=2
calib=[("HOT (top 20%)",50,"36.5%","34.0%"),("Warm",50,"13.9%","14.0%"),("Mid",50,"2.7%","0.0%"),("Cool",50,"1.1%","2.0%"),("Cold (bot 20%)",53,"0.5%","0.0%")]
for nm,n,p,a in calib:
    cellv(ws,rr,1,nm,True,left); cellv(ws,rr,2,n); cellv(ws,rr,3,p); cellv(ws,rr,4,a); cellv(ws,rr,5,""); rr+=1
rr+=1
band(ws,"If we only worked demos above a probability threshold",5,rr); head(ws,["Threshold","Demos","% of wins kept","Win-rate",""],rr+1); rr+=2
thr=[("P >= 5%",98,"96%","24.5%"),("P >= 10%",87,"92%","26.4%"),("P >= 15%",80,"88%","27.5%"),("P >= 20%",49,"68%","34.7%"),("P >= 30%",35,"56%","40.0%")]
for nm,n,wk,wrr in thr:
    cellv(ws,rr,1,nm,True,left); cellv(ws,rr,2,n); cellv(ws,rr,3,wk); cellv(ws,rr,4,wrr); cellv(ws,rr,5,"")
    if nm=="P >= 5%":
        for cc in range(1,6): ws.cell(row=rr,column=cc).fill=PatternFill("solid",fgColor=GOLD)
    rr+=1
rr+=1
cellv(ws,rr,1,"How to wire: run score_deal.py in the hourly CRON alongside the BANT/quality audit; write probability + band (HOT/WARM/MID/COLD) to a deal field. Route HOT to onsite + senior reps; auto-deprioritise COLD (P<5% captured just 1 of 25 wins). Re-fit monthly as data grows.",al=wrap)
ws.merge_cells(start_row=rr,start_column=1,end_row=rr,end_column=5); ws.row_dimensions[rr].height=46; ws.cell(row=rr,column=1).font=f(10,NAVY,True)

# Creator scorecard
ws=wb.create_sheet("Creator Scorecard"); ws.sheet_view.showGridLines=False
for c,w in zip("ABCDEFGH",[20,9,9,9,9,9,9,13]): ws.column_dimensions[c].width=w
title(ws,"Per-Rep Scorecard",8,1,14)
head(ws,["Rep","Demos","Won","Win %","GREEN","RED","Onsite","Revenue INR"],3)
rr=4
for cr,p in A["per_creator"].items():
    cellv(ws,rr,1,cr,True,left); cellv(ws,rr,2,p["demos"]); cellv(ws,rr,3,p["won"]); cellv(ws,rr,4,p["win_rate"],nf="0.0%")
    cellv(ws,rr,5,p["GREEN"]); cellv(ws,rr,6,p["RED"]); cellv(ws,rr,7,p["onsite"]); cellv(ws,rr,8,p["revenue"],nf="#,##0"); rr+=1
wb.save(BASE+"/Presales_June_PostMortem.xlsx")
print("saved:",wb.sheetnames)
