const fs=require("fs");
const {Document,Packer,Paragraph,TextRun,Table,TableRow,TableCell,AlignmentType,
 LevelFormat,HeadingLevel,BorderStyle,WidthType,ShadingType,PageNumber,Header,Footer,PageBreak,
 TableOfContents}=require("docx");

const NAVY="1F3864",BLUE="2E5496",TEAL="1F6E6E",GREENF="1E7145",REDF="9C0006",AMBF="9C6500",LT="EAF1FA",GREY="F2F2F2",GOLD="FFF4D6",GREENBG="E2EFDA",REDBG="FBE4E4";
const CW=9360;
const B={style:BorderStyle.SINGLE,size:1,color:"BFBFBF"};
const bd={top:B,bottom:B,left:B,right:B};
const R=(t,o={})=>new TextRun({text:t,font:"Arial",...o});
const P=(runs,o={})=>new Paragraph({children:Array.isArray(runs)?runs:[R(runs)],spacing:{after:120,...(o.spacing||{})},...o});
const H1=t=>new Paragraph({heading:HeadingLevel.HEADING_1,children:[R(t)],spacing:{before:280,after:140}});
const H2=t=>new Paragraph({heading:HeadingLevel.HEADING_2,children:[R(t)],spacing:{before:200,after:100}});
const src=t=>new Paragraph({children:[R("Source: "+t,{italics:true,size:16,color:"666666"})],spacing:{after:160}});
const bullet=(t,o={})=>new Paragraph({numbering:{reference:"b",level:0},spacing:{after:70},children:Array.isArray(t)?t:[R(t)]});
const numi=(t,ref="n")=>new Paragraph({numbering:{reference:ref,level:0},spacing:{after:80},children:Array.isArray(t)?t:[R(t)]});
function cell(t,{w,fill,bold,color,align}={}){
  const runs=Array.isArray(t)?t:[R(String(t),{bold,color,size:18})];
  return new TableCell({borders:bd,width:{size:w,type:WidthType.DXA},
    shading:fill?{fill,type:ShadingType.CLEAR}:undefined,
    margins:{top:60,bottom:60,left:110,right:110},
    children:[new Paragraph({alignment:align||AlignmentType.LEFT,children:runs})]});
}
function table(headers,rows,widths,opts={}){
  const hr=new TableRow({tableHeader:true,children:headers.map((h,i)=>cell([R(h,{bold:true,color:"FFFFFF",size:18})],{w:widths[i],fill:opts.headFill||BLUE,align:i===0?AlignmentType.LEFT:AlignmentType.CENTER}))});
  const body=rows.map(r=>new TableRow({children:r.map((c,i)=>{
    let fill=undefined,color=undefined,bold=false;
    if(typeof c==="object"&&c!==null&&!Array.isArray(c)){fill=c.fill;color=c.color;bold=c.bold;c=c.t;}
    return cell(String(c),{w:widths[i],fill,color,bold,align:i===0?AlignmentType.LEFT:AlignmentType.CENTER});
  })}));
  return new Table({width:{size:widths.reduce((a,b)=>a+b,0),type:WidthType.DXA},columnWidths:widths,rows:[hr,...body]});
}
const kicker=(t)=>new Paragraph({spacing:{before:60,after:120},children:[R(t,{bold:true,color:BLUE,size:18})]});

const content=[];
// ---------- COVER ----------
content.push(new Paragraph({spacing:{before:1600,after:60},children:[R("MARKETING & PRE-SALES AUDIT",{bold:true,size:44,color:NAVY})]}));
content.push(new Paragraph({spacing:{after:40},children:[R("Demand Quality, Revenue Reality, Pipeline Health & Action Plan",{size:28,color:"333333"})]}));
content.push(new Paragraph({spacing:{after:240},children:[R("Sell.Do — Kylas CRM · Pre-Sales team (Revati Ambike, Ashwini Nirmal, Gayatri More)",{size:20,color:"555555"})]}));
content.push(new Paragraph({border:{top:{style:BorderStyle.SINGLE,size:12,color:TEAL,space:6}},spacing:{after:200},children:[R("")]}));
content.push(P([R("Audience: ",{bold:true}),R("Marketing & Pre-Sales teams (shared manager)")]));
content.push(P([R("Period reviewed: ",{bold:true}),R("June 2026 (demand quality) and Jan–Jun 2026 (revenue). Pipeline snapshot as of 6 Jul 2026.")]));
content.push(P([R("Purpose: ",{bold:true}),R("An evidence-based audit of the pre-sales/marketing funnel — what we generated, what actually converts, where revenue really comes from, and a prioritised plan. Every figure is traceable to a Kylas query or the per-deal dataset cited alongside it.")]));
content.push(P([R("Status: ",{bold:true}),R("Internal — for review and action.")]));
content.push(new Paragraph({children:[new PageBreak()]}));

// ---------- METHODOLOGY ----------
content.push(H1("0. How to read this report (scope, data & method)"));
content.push(P("So the findings can be actioned rather than debated, here is exactly how every number was produced. Anyone can reproduce them in Kylas with the filters below."));
content.push(bullet([R("Who counts as Pre-Sales: ",{bold:true}),R("the CRM team “Pre-sales team” (Kylas report 361026 filter: Created-By Team = Pre-sales team). Members with activity in the period: Revati Ambike, Ashwini Nirmal, Gayatri More.")]));
content.push(bullet([R("June demo universe (253): ",{bold:true}),R("deals with a meeting/demo actually conducted in June — cfMeetingConductedOn between 01–30 Jun 2026 (IST), created by the Pre-sales team. The CRM list view shows 241 only because its default time cut-off is 17:00 on the 1st/30th; the full calendar month is 253.")]));
content.push(bullet([R("Revenue universe (closures): ",{bold:true}),R("deals in the Sell.Do Deal Pipeline (5313) that reached Won/Booked (stage 35813) with actualClosureDate in the period, created by the Pre-sales team. Revenue = cfBilledAmount; cash = cfActualPaymentReceived.")]));
content.push(bullet([R("Open pipeline: ",{bold:true}),R("forecastingType = OPEN, pipeline 5313, created 2026, Pre-sales team (480 deals). The triage focuses on the 150 that are genuinely workable: demo done, 5+ licences, updated since 15 May.")]));
content.push(bullet([R("Quality verdict (GREEN/AMBER/RED) and conversion probability: ",{bold:true}),R("an independent read produced for this audit by reading every deal’s structured fields AND free-text notes against a fixed rubric, then a probability model fitted on the June outcomes. This is NOT the hourly CRON’s output; it has since been wired into the deal-audit skill so the CRON now stamps the same band.")]));
content.push(bullet([R("Coverage note: ",{bold:true}),R("253/253 June demos and 150/150 open deals were fetched with full notes. For the 6-month closures, 208 of 216 were fetched cleanly (96%); totals below are on the 208 and are therefore slight under-counts, not over-counts.")]));
content.push(src("Kylas CRM search API (pipeline 5313), report 361026, and per-deal exports stored in master_dataset.csv, closures_dataset.csv, closures6m/, open_pipeline_focus.csv."));

// ---------- EXEC SUMMARY ----------
content.push(H1("1. Executive summary"));
content.push(P([R("The engine produces plenty of activity but not enough of the ",{}),R("right",{italics:true}),R(" activity. In June, pre-sales ran 253 demos; only 98 (39%) were genuinely well-qualified, and effectively all revenue traced back to those. Real money is made by developers (80% of June revenue) and by a handful of high-intent channels (Organic, Google) — while a large share of effort goes to sub-scale channel partners, a Facebook channel that converts at 2%, and demos that were never properly qualified. The good news: the levers are specific and measurable.")]));
content.push(kicker("The seven findings, in priority order:"));
content.push(numi([R("Quality, not volume, is the whole game. ",{bold:true}),R("GREEN demos convert 24.5%; AMBER 1.0%; RED 0%. 24 of 25 June wins were GREEN.")]));
content.push(numi([R("We missed the quality target. ",{bold:true}),R("Target was 200+ demos of 5+ licences; we delivered 146. 107 demos (42%) were 1–4 seats and converted at 6.5%.")]));
content.push(numi([R("Revenue is developer-driven. ",{bold:true}),R("Developers = 80% of June revenue (₹50.0L of ₹62.4L) and close ~2× faster than channel partners — yet we run more channel-partner demos.")]));
content.push(numi([R("Marketing spend is mis-aimed. ",{bold:true}),R("Organic (13.7% win) and Google (9.5%, best size mix) work; Facebook is 19% of demos but 2.1% win — and the single biggest paid cluster, Meta “Lead-Gen Conversion” (~40 demos), maps to that weak Facebook source.")]));
content.push(numi([R("Off-territory developers are a real, ignored market. ",{bold:true}),R("Over 6 months, non-rep cities produced ~₹77L (29% of revenue); ~₹50L of that was developers closing remotely (East belt: Kolkata, Ranchi, Bhubaneswar).")]));
content.push(numi([R("Leads are distributed by availability, not strength. ",{bold:true}),R("Revati converts developers 24% (Ashwini 3.7%); Ashwini converts channel partners 11.7% (Revati 4.8%). Routing ignores this.")]));
content.push(numi([R("A third of the “qualified” open book shouldn’t be there. ",{bold:true}),R("Of 150 workable open deals, only 32 are truly HOT/WARM; 27 need re-qualification, 24 are stalling on the rep, 23 are dead.")]));
content.push(new Paragraph({spacing:{before:120}}));
content.push(kicker("Headline scoreboard"));
content.push(table(["Metric","Value","Read"],[
 ["June demos conducted","253","Activity was high"],
 [{t:"Well-qualified (GREEN)",bold:true},{t:"98 (39%)",fill:GREENBG},"Where ~all revenue comes from"],
 [{t:"Demos of 5+ licences vs target",bold:true},{t:"146 vs 200",fill:REDBG,color:REDF},"Quality target missed"],
 ["June revenue (billed / collected)","₹62.4L / ₹45.4L","42 closures"],
 [{t:"Developer share of June revenue",bold:true},{t:"80%",fill:GOLD},"₹50.0L of ₹62.4L"],
 ["6-month revenue (208 closures)","₹2.67 Cr","Jan–Jun 2026"],
 [{t:"Off-territory revenue (6-mo)",bold:true},{t:"~₹77L (29%)",fill:GOLD},"Developer-led, no local rep"],
 ["Onsite demos","33 of 253 (13%)","Off-model; onsite wins 15.2% vs 9.1%"],
 ["Open pipeline worth working now","32 of 150 (HOT+WARM)","~₹9.8L ACV"],
],[3400,2400,3560]));
content.push(src("Kylas: cfMeetingConductedOn Jun 2026 (n=253); closures pipeline 5313 stage 35813 (n=42 June, 208 six-month); analytics_v2.json; closures_analytics.json."));

// ---------- 2 DEMAND QUALITY ----------
content.push(new Paragraph({children:[new PageBreak()]}));
content.push(H1("2. Demand quality — the 253 June demos"));
content.push(H2("2.1 What GREEN, AMBER and RED mean"));
content.push(P([R("Every demo was graded on ",{}),R("how well pre-sales qualified it",{bold:true}),R(" — not on whether Sales later closed it. A demo is scored by reading the deal’s structured fields AND the free-text notes against a fixed rubric covering five things: (1) is the contact a real, named decision-maker; (2) is it a real company with a genuine CRM need; (3) is the size adequate (5+ seats); (4) is the key information captured (BANT, city, current tool); and (5) is the data clean (no junk/placeholder name or dummy phone). The verdict is the analyst’s read on data quality — the picture a sales rep gets before the demo.")]));
content.push(table(["Verdict","What it means for a demo","Typical signals we saw"],[
 [{t:"GREEN",fill:GREENBG,color:GREENF,bold:true},{t:"Genuinely qualified. A real, named decision-maker at a real company, a clear CRM need, 5+ seats, and the key facts captured. Good pre-sales work — even if Sales later loses it."},{t:"Owner/MD engaged; verified company; ~5–40+ seats; budget/timeline noted. E.g. M3M (100 seats), Doff Estates (25)."}],
 [{t:"AMBER",fill:GOLD,color:AMBF,bold:true},{t:"A real demo but with qualification gaps. Thin/partial BANT, small size, a junior or unconfirmed contact (not the decision-maker), or missing information. On-ICP, but the rep must confirm things before it can close."},{t:"Manager (not owner) attended; ~3–5 seats; price discussed but no budget/timeline; contact identity not fully verified."}],
 [{t:"RED",fill:REDBG,color:REDF,bold:true},{t:"Poor pre-sales work — should not have been booked. Junk/placeholder contact, no real need, wrong ICP (a 1-seat individual or tiny broker with no intent), or a “demo for the number” with no substance."},{t:"Placeholder name (“T Rex”) or dummy phone (+91 9999999999); 1–2 seats; not actually looking; enrichment resolves to a different/unrelated person."}],
],[1150,4610,3600]));
content.push(P([R("Why this matters: ",{bold:true}),R("the verdict grades pre-sales only, so it is fair to the team — a GREEN demo that Sales fails to close stays GREEN (the miss is downstream), and a RED demo cannot be rescued by Sales. It also turns out to be an accurate forecast: in §3, GREEN demos convert 24.5% while RED convert 0%.")]));
content.push(src("Audit rubric applied to all 253 deals’ fields + notes (master_dataset.csv). The same rubric is now embedded in the hourly deal-audit skill."));
content.push(H2("2.2 The distribution"));
content.push(P([R("On the stated target — 200+ demos of 5+ user licences — we delivered 146 (58%). First, the quality split:")]));
content.push(table(["Pre-sales quality verdict","Demos","% of demos"],[
 [{t:"GREEN — genuinely qualified",color:GREENF,bold:true},"98","39%"],
 [{t:"AMBER — real but thin",color:AMBF,bold:true},"98","39%"],
 [{t:"RED — poor / sub-ICP",color:REDF,bold:true},"57","22%"],
 [{t:"Total",bold:true},"253","100%"],
],[4560,2400,2400]));
content.push(src("Rubric scoring of all 253 deals’ fields + notes (master_dataset.csv). GREEN/AMBER/RED defined in the audit rubric."));
content.push(P([R("The licence-size split shows where the gap is — 42% of demos were sub-5-seat prospects:")]));
content.push(table(["Licence tier","Demos","% ","Win rate","GREEN rate"],[
 [{t:"Under 5 seats",fill:REDBG},"107","42%","6.5%","14%"],
 ["5–10 seats","116","46%","12.1%","54%"],
 ["10+ seats","30","12%","13.3%","67%"],
],[3360,1400,1200,1700,1700]));
content.push(src("cfMeetingConductedOn Jun 2026; noOfLicenses; is_won as of 6 Jul 2026 (n=253). analytics_v2.json winrate_by_tier3."));
content.push(P([R("Read: ",{bold:true}),R("42% of demos were sub-5-seat prospects that convert at roughly half the rate and account for most RED verdicts. Volume was partly manufactured by lowering the bar.")]));

// ---------- 3 WHAT CONVERTS ----------
content.push(H1("3. What actually converts (the strongest evidence in this pack)"));
content.push(P("Win-rate cut every way the data allows. The signals are unusually clean and they compound — the “ideal” demo is a Strong-BANT developer, 5+ seats, seen in person."));
content.push(table(["Cut","Best segment (win rate)","Worst segment"],[
 [{t:"Quality verdict",bold:true},{t:"GREEN 24.5%",fill:GREENBG},"AMBER 1.0% / RED 0%"],
 [{t:"BANT",bold:true},{t:"Strong 27.9%",fill:GREENBG},"Partial/Weak/None ~0.6%"],
 [{t:"Account type",bold:true},"Developer 13.3%","Channel partner 7.5%"],
 [{t:"Demo mode",bold:true},"Onsite 15.2%","Online 9.1%"],
 [{t:"City",bold:true},"Hyderabad/Chennai 24–27%","Pune 0% / NCR 7%"],
 [{t:"Licence size",bold:true},"10+ seats 13.3%","Under 5 seats 6.5%"],
],[2600,3560,3200]));
content.push(src("analytics_v2.json (win-rate by verdict, bant_flag, dev/broker, onsite, main6 city, tier3), n=253 June demos."));
content.push(P([R("Because GREEN/Strong-BANT predicts revenue almost perfectly, we built a calibrated probability model (top-quintile predicted 36.5% vs 34.0% actual). Its practical use: ",{}),R("the 98 demos scoring ≥5% probability captured 96% of all wins — the other 155 demos produced one win between them.",{bold:true}),R(" The model is now wired into the hourly deal-audit skill so every deal gets a HOT/WARM/MID/COLD band.")]));
content.push(src("model_weights.json + score_deal.py; calibration on n=253. Threshold table in Presales_June_PostMortem.xlsx → Convert Model."));

// ---------- 4 REVENUE ----------
content.push(new Paragraph({children:[new PageBreak()]}));
content.push(H1("4. Revenue reality — closures, not demos"));
content.push(P([R("Revenue must be read on ",{}),R("deals that closed",{italics:true}),R(", not demos that happened. June closures (42 deals) totalled ",{}),R("₹62.4L billed / ₹45.4L collected",{bold:true}),R(" — more than double the ₹29.4L attributable to June-demo wins, because large developer deals demoed months earlier close in June (e.g. Kaustubh/Gurgaon ₹8.2L, 30 seats, demoed April).")]));
content.push(table(["June closures by account type","Deals","Revenue","Avg demo→close"],[
 [{t:"Developer",bold:true,fill:GOLD},{t:"24",fill:GOLD},{t:"₹50.0L (80%)",fill:GOLD},{t:"~28 days",fill:GOLD}],
 ["Channel partner","18","₹12.4L (20%)","~49 days"],
],[3960,1200,2400,1800]));
content.push(src("Closures pipeline 5313 stage 35813, actualClosureDate Jun 2026 (n=42). closures_analytics.json. Velocity estimated from won-stage timestamp (exact close date not exposed by the connector)."));
content.push(P([R("Over the last six months, pre-sales closed ",{}),R("₹2.67 Cr across 208 deals",{bold:true}),R(". Developers dominate both revenue and speed; the takeaway for both teams is that developer, 5+-seat accounts are where the money is — and they are under-fed at the top of the funnel.")]));

// ---------- 5 MARKETING ----------
content.push(H1("5. Top of funnel — where leads come from and what converts"));
content.push(P("Lead source is captured on all 253 demos; UTM campaign / sub-source is captured on the paid ones (~43% of demos — Organic and WhatsApp correctly carry none). Channel ROI is stark:"));
content.push(table(["Source","Demos","% 5+ seats","Won","Win rate","Read"],[
 [{t:"Organic",bold:true,fill:GREENBG},"95","58%","13","13.7%","Champion — highest volume & yield"],
 [{t:"Google",bold:true,fill:GREENBG},"74","66%","7","9.5%","Best size mix; reliable paid lever"],
 [{t:"Facebook",bold:true,fill:REDBG},"47","51%","1","2.1%","19% of demos, 4% of wins — broken"],
 ["WhatsApp (Interakt)","32","43%","3","9.4%","Decent inbound"],
 ["Instagram","3","33%","0","0%","Negligible"],
],[1700,1000,1500,900,1200,3060]));
content.push(src("Kylas source field, per-source counts via search API (cfMeetingConductedOn Jun 2026, Pre-sales team). closures_analytics.json source_funnel."));
content.push(P([R("Read: ",{bold:true}),R("Facebook is burning ~1 in 5 demos for ~1 in 25 wins. Organic (SEO/brand/referral) is the cheapest, highest-intent source; Google is the best paid channel and brings the best size mix.")]));
content.push(H2("5.1 Which paid campaigns (UTM / sub-source)"));
content.push(P([R("Contrary to a common assumption, the paid demos ",{}),R("are",{italics:true}),R(" attributed — utmCampaign and subSource carry the campaign on the Google/Facebook leads (Organic simply has none). The paid demos concentrate in a few named campaigns:")]));
content.push(table(["Campaign cluster","Platform","June demos"],[
 [{t:"Meta “Lead-Gen Conversion” (Apr-2024 + Jun-2025)",fill:REDBG},"Facebook / Meta","~40"],
 ["Google Search (search-jan24, -south, ai-calling)","Google","~32"],
 [{t:"Google Brand Search (+ -south)",fill:GREENBG},"Google","~23"],
 ["Performance Max (traffic / retarget / competitor)","Google","~4"],
 ["YouTube retarget","Google","1"],
 ["No UTM — Organic / WhatsApp / direct","—","136"],
],[4560,2600,2200]));
content.push(src("Kylas report 361026 re-grouped by UTM Campaign and Sub Source, Last Month (created-in-June basis, n=237). Sub Source mirrors UTM Campaign."));
content.push(P([R("Read: ",{bold:true}),R("the biggest single paid cluster — Meta “Lead-Gen Conversion” (~40 demos) — is exactly the Facebook source that converts at 2.1%; the Google Search and (especially) Brand-Search campaigns are the better converters. So the paid re-allocation is concrete: move budget from the Meta lead-gen forms toward Google Brand/Search. Two data issues to fix: one live ad passes a broken “{{campaign.name}}” UTM, and several campaign names are stale (2024-dated campaigns still tagging 2026 leads), which blurs fresh-spend attribution.")]));

// ---------- 6 GEOGRAPHY ----------
content.push(H1("6. Geography — rep cities vs off-territory"));
content.push(P([R("We have reps in six cities (Pune, Mumbai, Delhi/NCR, Bangalore, Chennai, Hyderabad). They convert ~2× better on average, and Hyderabad/Chennai are the best closers — but they are ",{}),R("starved",{italics:true}),R(" of demos, while Pune (HQ) converted 0% in June. Over six months, non-rep cities still produced ~₹77L (29% of revenue), and that is developer-led:")]));
content.push(table(["Off-territory (6-month closures)","Deals","Revenue"],[
 ["All non-rep cities","63","~₹77L (29% of total)"],
 [{t:"— of which Developers",bold:true,fill:GOLD},{t:"38",fill:GOLD},{t:"~₹50L",fill:GOLD}],
 ["— of which Channel partners","25","~₹27L"],
],[4560,1600,3200]));
content.push(src("closures6m/ (n=208 fetched of 216); city normalised from cfCity. Off-territory = cities outside the six rep cities."));
content.push(P([R("Standout off-territory developer markets (6-month, by developer revenue): ",{bold:true}),R("Kolkata (~₹9.5L; Amina/Doff 25 seats ₹4.44L), Jaipur (₹3.9L), Ranchi (₹3.5L; Kavita 25 seats), Bhubaneswar (₹4.3L; 15 seats), Coimbatore, Calicut (a 40-seat developer, ₹2.66L). These are real mid-market builders closing remotely with no local rep — an East-India developer belt in particular.")]));
content.push(P([R("Nuance both teams must hold: ",{bold:true}),R("for developers, territory barely matters (they close remotely); for brokers/channel partners it does (they need onsite hand-holding). So concentrate the ",{}),R("broker",{italics:true}),R(" motion in rep cities, and run ",{}),R("developer",{italics:true}),R(" demand-gen nationally.")]));

// ---------- 7 DISTRIBUTION ----------
content.push(new Paragraph({children:[new PageBreak()]}));
content.push(H1("7. Lead distribution & rep performance"));
content.push(P("Leads appear to be distributed by availability, not by rep strength — and the two reps have opposite strengths, so the current routing leaves conversion on the table."));
content.push(table(["Rep","Demos","Developer / CP mix","10+ seat deals","Overall win"],[
 ["Revati Ambike","135","37% / 62%","23","11.9%"],
 ["Ashwini Nirmal","114","47% / 53%","6","7.9%"],
],[2600,1200,2760,1800,1000]));
content.push(P([R("The crossover (the key point):",{bold:true})]));
content.push(table(["Win rate by segment","On Developers","On Channel partners"],[
 [{t:"Revati Ambike",bold:true},{t:"24.0%",fill:GREENBG,bold:true},"4.8%"],
 [{t:"Ashwini Nirmal",bold:true},"3.7%",{t:"11.7%",fill:GREENBG,bold:true}],
],[3560,2900,2900]));
content.push(src("master_dataset.csv, creator × dev/broker × is_won (n=249 for the two reps). Source routing checked via per-source × creator counts — roughly proportional to volume, i.e. no strength-based routing."));
content.push(P([R("Read: ",{bold:true}),R("Revati is the developer closer (6× Ashwini on developers) and already handles almost all large deals; Ashwini is the channel-partner closer (2.4× Revati). Yet developers — 80% of revenue — are split ~50/50. Routing developers → Revati and channel partners → Ashwini should lift both segments. (June deals are still maturing, so absolute rates will rise; the relative pattern is the signal, strongest for Revati-on-developers with 12 wins.)")]));

// ---------- 8 OPEN PIPELINE ----------
content.push(H1("8. Open pipeline health & triage"));
content.push(P([R("Of 480 open pre-sales deals, 150 are genuinely workable (demo done, 5+ seats, active since mid-May). Scoring each on probability + a keep/churn call shows the open book is much thinner than it looks:")]));
content.push(table(["Conversion band","Deals","","Churn call","Deals"],[
 [{t:"HOT",color:GREENF,bold:true},"16","",{t:"KEEP (current sales)",bold:true},"76"],
 [{t:"WARM",color:AMBF,bold:true},"16","","REASSIGN → new sales","24"],
 ["MID","26","","BACK → pre-sales (re-qualify)","27"],
 ["COLD","92","","DISQUALIFY (close-lost)","23"],
],[2100,1000,600,3560,1200]));
content.push(src("open_pipeline_focus.csv (n=150). Probability from the model; churn call from stage + notes + idle-days."));
content.push(P([R("Only 32 deals (HOT+WARM, ~₹9.8L ACV) are worth chasing this week. Critically, ~1 in 3 of the “qualified” book (27 re-qualify + 23 disqualify) should never have reached sales as live pipeline — the dominant cause is a wrong/junior/unverified contact, a pre-sales qualification miss the audit already flags. A further 24 are real deals decaying on rep follow-up. Per-deal next actions and owners are in the accompanying workbook.")]));
content.push(src("Open_Pipeline_Focus.xlsx (WORK NOW, Reassign, Back-to-Pre-Sales, Disqualify sheets)."));

// ---------- 9 SYSTEMIC ----------
content.push(H1("9. Systemic issues (fix once, benefit everywhere)"));
content.push(P("Why deals don’t move — the largest fixable cause sits upstream with qualification and data quality, not closing:"));
content.push(bullet([R("Root-cause of stalls: ",{bold:true}),R("Quality/ICP (60) and BANT-weak (18) together ≈ 31% of demos never had a chance; 63 stalls are pre-sales-owned vs 43 sales-owned. (Source: analytics_v2.json blocker + blocker_owner, n=253.)")]));
content.push(bullet([R("Contact integrity: ",{bold:true}),R("27 of 253 demos (11%) carried junk/placeholder names, and the dummy phone +919999999999 recurs; enrichment repeatedly resolves the deal phone to a different person. These pass into sales as “qualified.”")]));
content.push(bullet([R("Attribution mostly works — two small gaps to close: ",{bold:true}),R("paid demos DO carry utmCampaign / subSource (~43% of demos; Organic correctly has none), so channel and campaign are measurable. The gaps are (a) one live ad passing a broken “{{campaign.name}}” UTM, and (b) stale campaign names (Apr-2024 / Jan-2024 campaigns still tagging Jun-2026 leads), which blur fresh-spend attribution. Note: the picklist ‘campaign’ field is unused — attribution lives in the UTM/sub-source fields, not there.")]));
content.push(bullet([R("City field is messy: ",{bold:true}),R("cfCity contains misspellings (Banagalore, Guregaon, Ahemdabad) and states entered as cities (“Tamil Naidu”, “Andhra Pradesh”, “Odisha”), which corrupts any territory/routing logic. Switch to a validated dropdown.")]));

// ---------- 10 ACTION PLAN ----------
content.push(new Paragraph({children:[new PageBreak()]}));
content.push(H1("10. Prioritised action plan"));
content.push(P("Owner key: M = Marketing, PS = Pre-Sales, S = Sales (shared manager to sequence). Each action lists the metric that proves it worked."));
content.push(H2("P0 — do this month (highest leverage)"));
content.push(numi([R("[PS] Gate every demo before it is booked. ",{bold:true}),R("Require verified company + real phone (auto-reject 9999999999 / single-word names), a named decision-maker, BANT ≥ Partial, and 5+ seats. Run deal-audit before the demo. Metric: RED demos <10%; junk-name demos ~0.")],"p0"));
content.push(numi([R("[M] Re-aim ad spend to what converts. ",{bold:true}),R("Scale Google, invest in Organic (SEO/brand/content); fix Facebook targeting to developer/large-account lookalikes or move its budget to Google; drop Instagram. Metric: blended demo→win ≥ 12%; Facebook win-rate ≥ 8% or spend reallocated.")],"p0"));
content.push(numi([R("[M+PS] Bias the whole funnel to developers & 5+ seats. ",{bold:true}),R("Developers are 80% of revenue. Set a developer-share floor (≥50% of demos) and a 5-seat minimum. Metric: 5+ seat demos ≥ 200/month; developer share ≥ 50%.")],"p0"));
content.push(numi([R("[PS/S] Route by strength. ",{bold:true}),R("Send developer leads to Revati, channel-partner leads to Ashwini. Metric: developer win-rate on the developer-closer maintained ≥20%.")],"p0"));
content.push(H2("P1 — next 30–60 days"));
content.push(numi([R("[M] Run a remote developer desk for tier-2 / off-territory. ",{bold:true}),R("Prioritise the East belt (Kolkata, Ranchi, Bhubaneswar, Siliguri), Gujarat and tier-2 South. Metric: off-territory developer revenue ≥ current ₹50L/6-mo run-rate, tracked monthly.")],"p1"));
content.push(numi([R("[M] Tighten attribution and act on it. ",{bold:true}),R("Fix the broken “{{campaign.name}}” UTM and refresh stale campaign names so fresh spend is readable; then reallocate from the Meta “Lead-Gen Conversion” cluster (biggest paid volume, weakest conversion) toward Google Brand/Search. Metric: 100% of paid deals carry a clean campaign; Meta lead-gen win-rate ≥8% or budget moved.")],"p1"));
content.push(numi([R("[PS] Concentrate the broker motion in rep cities & fix Pune. ",{bold:true}),R("Push demand into Hyderabad/Chennai (best closers); root-cause Pune (0% in June). Metric: Hyderabad+Chennai demo volume up; Pune win-rate >0%.")],"p1"));
content.push(numi([R("[S] Sales-hygiene SLA + auto-reassign. ",{bold:true}),R("Any HOT/WARM deal idle >21 days escalates/reassigns. Metric: recover the ~₹4.5L currently stalled on reps; median idle on HOT/WARM <14 days.")],"p1"));
content.push(H2("P2 — structural / ongoing"));
content.push(numi([R("[M] Force onsite for HOT deals in rep cities, ",{bold:true}),R("especially Hyderabad/Chennai/NCR where onsite is <15% today (onsite ≈ 3× revenue per demo). Metric: ≥40% of Main-6 demos in person.")],"p2"));
content.push(numi([R("[PS] Grow Organic with competitor-comparison content ",{bold:true}),R("(vs Zoho, Leadrat, Buildesk, Kit19) and developer case studies. Metric: Organic demo volume and win-rate trend up.")],"p2"));
content.push(numi([R("[M/PS] Stand up a named-account enterprise lane ",{bold:true}),R("(40+ seat developers, CXO multi-threading). Metric: ≥15 enterprise (40+) demos/month vs ~5.")],"p2"));
content.push(numi([R("[Ops] Clean the data. ",{bold:true}),R("Validated cfCity dropdown; keep the conversion model re-fitted monthly (it’s already in the deal-audit CRON). Metric: zero states-as-cities; band stamped on every new deal.")],"p2"));

// ---------- APPENDIX ----------
content.push(H1("Appendix — data sources & artifacts"));
content.push(P("Every figure in this report is reproducible from these, all stored in the presales_june_analysis folder:"));
content.push(bullet("master_dataset.csv — 253 June demos, per-deal fields + verdict + BANT + probability."));
content.push(bullet("closures_dataset.csv / closures_analytics.json — 42 June closures (revenue, velocity, source funnel)."));
content.push(bullet("closures6m/ — 208 of 216 six-month closures (city, type, billed) for the geography analysis."));
content.push(bullet("open_pipeline_focus.csv + Open_Pipeline_Focus.xlsx — 150 open deals: probability, next action, churn call."));
content.push(bullet("Presales_June_PostMortem.xlsx — 14 sheets: What Converts, City Deep-Dive, Marketing Source, Convert Model, Revenue (Closures), etc."));
content.push(bullet("model_weights.json + score_deal.py — the conversion model, now embedded in the deal-audit skill."));
content.push(P([R("Reproduce the counts in Kylas: ",{italics:true,size:18}),R("Pre-sales team = report 361026 filter; demos = cfMeetingConductedOn in period; closures = pipeline 5313 / stage 35813 / actualClosureDate in period; open = forecastingType OPEN + pipeline 5313.",{size:18,italics:true})]));

// ---------- DOC ----------
const doc=new Document({
 styles:{default:{document:{run:{font:"Arial",size:21}}},
  paragraphStyles:[
   {id:"Heading1",name:"Heading 1",basedOn:"Normal",next:"Normal",quickFormat:true,run:{size:28,bold:true,font:"Arial",color:NAVY},paragraph:{spacing:{before:280,after:140},outlineLevel:0}},
   {id:"Heading2",name:"Heading 2",basedOn:"Normal",next:"Normal",quickFormat:true,run:{size:23,bold:true,font:"Arial",color:BLUE},paragraph:{spacing:{before:200,after:100},outlineLevel:1}},
  ]},
 numbering:{config:[
   {reference:"b",levels:[{level:0,format:LevelFormat.BULLET,text:"•",alignment:AlignmentType.LEFT,style:{paragraph:{indent:{left:600,hanging:280}}}}]},
   {reference:"n",levels:[{level:0,format:LevelFormat.DECIMAL,text:"%1.",alignment:AlignmentType.LEFT,style:{paragraph:{indent:{left:560,hanging:300}}}}]},
   {reference:"p0",levels:[{level:0,format:LevelFormat.DECIMAL,text:"%1.",alignment:AlignmentType.LEFT,style:{paragraph:{indent:{left:560,hanging:300}}}}]},
   {reference:"p1",levels:[{level:0,format:LevelFormat.DECIMAL,text:"%1.",alignment:AlignmentType.LEFT,style:{paragraph:{indent:{left:560,hanging:300}}}}]},
   {reference:"p2",levels:[{level:0,format:LevelFormat.DECIMAL,text:"%1.",alignment:AlignmentType.LEFT,style:{paragraph:{indent:{left:560,hanging:300}}}}]},
 ]},
 sections:[{
   properties:{page:{size:{width:12240,height:15840},margin:{top:1440,right:1440,bottom:1440,left:1440}}},
   footers:{default:new Footer({children:[new Paragraph({alignment:AlignmentType.CENTER,children:[R("Marketing & Pre-Sales Audit · Sell.Do · Confidential — Internal · Page ",{size:16,color:"888888"}),new TextRun({children:[PageNumber.CURRENT],font:"Arial",size:16,color:"888888"})]})]})},
   children:content
 }]
});
Packer.toBuffer(doc).then(b=>{fs.writeFileSync("Marketing_PreSales_Audit_June2026.docx",b);console.log("written",b.length,"bytes");});
