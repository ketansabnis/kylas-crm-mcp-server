import json, math, collections, statistics
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

BASE = "/sessions/zealous-brave-cerf/mnt/kylas-crm-mcp-server/marketing_weekly"
WK = "2026-07-19"
WK_START, WK_END = "2026-07-13", "2026-07-19"

# city -> (bucket, main6)  bucket: hc(Hyd/Chennai), metro(core), other
CITYMAP = {
 "Surat":("other",False),"Navi mumbai":("metro",True),"Raipur":("other",False),"Pune":("metro",True),
 "Mumbai":("metro",True),"Indore":("other",False),"noida":("metro",True),"Noida":("metro",True),
 "Nagpur":("other",False),"Vrundavan":("other",False),"Ahmedabad":("other",False),"Madhya Pradesh":("other",False),
 "Bangalore":("metro",True),"Lucknow":("other",False),"Odisha":("other",False),"Gurgaon":("metro",True),
 "Kolkata":("other",False),"Warangal":("other",False),"Delhi":("metro",True),"New delhi":("metro",True),
 "Chennai":("hc",True),"Jaipur":("other",False),"Jabalpur":("other",False),"Chattisgarh":("other",False),
 "Rajkot":("other",False),"Faridabad":("metro",True),"Gurugram":("metro",True),"Vishakhapatnam":("other",False),
 "Kota":("other",False),"pune":("metro",True),
}

# id, name, creator, owner, source, lic(claimed), typ, city, onsite(bool/None), bant, verdict,
# seats_verified, junk, dummy, unver, competitor, fu(sales followup after demo), fc(forecast), one_line
D = [
 (4536573,"Diyani","Ashwini Nirmal","Sakshi Kadu","Organic",10,"Channel partner","Surat",False,"Partial","AMBER",5,True,False,True,"Top Funnel",1,"OPEN","Matlani Real Estate, 15-yr Surat broker on Top Funnel; contact is marketing staff, owner phone resolves to a different person; ~5 real users vs 10."),
 (4534134,"Vikrant Shanbhag","Ashwini Nirmal","Alok Tiwari","Facebook",14,"Channel partner","Navi mumbai",False,"Strong","AMBER",1,False,False,False,"Neodove",0,"OPEN","Home Search Advisors, verified Founder/CEO on Neodove; strong DM but wants to start with 1 user (14 claimed). Quote sent, no follow-up yet."),
 (4533848,"Nayan","Revati Ambike","Sakshi Kadu","Organic",50,"Developer","Raipur",False,"Partial","AMBER",None,True,False,False,"Neodove",0,"OPEN","Wallfort Properties, large Raipur developer, real 50-seat need — but NO demo outcome note (ghost demo) and contact is Sales Head not owner."),
 (4532536,"Ankit","Revati Ambike","Sakshi Kadu","Google",30,"Developer","Pune",True,"Partial","GREEN",15,True,False,False,"AckoLead",1,"OPEN","Mittal Brothers, verified major Pune developer; onsite demo, quote sent 15 users, on AckoLead with real pain. Contact identity soft."),
 (4532311,"Ashwini Shelke","Ashwini Nirmal","Ankur Singhal","Google",15,"Developer","Mumbai",False,"Partial","AMBER",None,False,False,False,None,0,"OPEN","LeasePro — mislabeled Developer, actually a Mumbai leasing brokerage; contact is Head of Digital Mktg (influencer). No budget/timeline."),
 (4532079,"Sraveshwar Patidar","Revati Ambike","Ananya Kumari","Organic",5,"Channel partner","Indore",False,"Partial","AMBER",None,False,False,False,None,1,"OPEN","Solo Indore investment consultant on Sheets; verified owner. Quoted; budget below list; ~2-5 real seats."),
 (4519691,"Vishal","Ashwini Nirmal","Suraj Chauhan","Organic",5,"Channel partner","noida",False,"Partial","AMBER",None,True,False,False,None,1,"OPEN","Solo eXp Realty associate, personal brand; verified self-DM, proposal shared (~60k). 5 claimed but 1-2 realistic."),
 (4519600,"Yamini Chhabda","Revati Ambike","Ankur Singhal","Organic",250,"Developer","Nagpur",False,"Weak","RED",None,False,False,False,None,0,"OPEN","Mauli Infra, genuine Nagpur developer, but HR gatekeeper contact; disqualified post-demo ('use case not feasible'). 250-seat never validated."),
 (4519564,"Prakash Tomar","Ashwini Nirmal","Anuj Pathak","Facebook",5,"Channel partner","Vrundavan",False,"Weak","RED",None,False,False,True,None,0,"OPEN","Micro Vrindavan CP, zero footprint; contact resolves to a different rural person; marked Demo Conducted with NO demo note (ghost)."),
 (4518620,"Rakesh Kanjani","Ashwini Nirmal","Disha Kadam","Google",5,"Channel partner","Ahmedabad",False,"Partial","AMBER",4,False,False,False,None,0,"OPEN","Global Consultancy, verified Ahmedabad CP since 2014 on Excel; proposal requested. 4 real users; price-sensitive."),
 (4518543,"Anam Khan","Revati Ambike","Arzoo Choudhary","Google",10,"Developer","Madhya Pradesh",False,"Weak","RED",None,False,False,True,"Kolonizer",2,"OPEN","SRJ Varco, micro MP builder; contact enriches as HR at competitor Kolonizer, NOT the company — wrong/unverified contact."),
 (4517420,"Gayatri","Ashwini Nirmal","Pranith A B","WhatsApp",20,"Developer","Bangalore",True,"Partial","AMBER",50,True,False,True,None,0,"OPEN","Novel Reventus, Bangalore telecalling sales operation (no website); onsite demo, ~50 users, but contact identity MISMATCH. New POC given."),
 (4517126,"Mohan","Ashwini Nirmal","Sakshi Kadu","Google",7,"Channel partner","Lucknow",False,"Partial","AMBER",None,True,False,False,None,1,"OPEN","propInvesta Realty, solo Lucknow broker; verified owner, moving to close ('will send GST today'), now Hot Opportunity. ~2-4 real seats."),
 (4516809,"Trupikant Swain","Revati Ambike","Jawed Alam","Organic",5,"Channel partner","Odisha",False,"Partial","AMBER",None,False,False,False,None,0,"OPEN","Utkalproperty, verified CEO/founder, Bhubaneswar broker-influencer with real first-CRM need, 5 seats. Budget/timeline not captured."),
 (4516792,"Bishnoi Birbal","Ashwini Nirmal","Anuj Pathak","Facebook",5,"Channel partner","Ahmedabad",False,"Weak","RED",1,False,False,True,None,0,"CLOSED_UNQUALIFIED","Shree Balaji Realty, solo Ahmedabad broker, 1 real user; unverified contact; closed unqualified on budget."),
 (4514800,"Sanskar Singh","Revati Ambike","Suraj Chauhan","Google",5,"Channel partner","Gurgaon",False,"Partial","AMBER",None,False,False,False,None,0,"OPEN","Luxure Nest, early-stage Gurugram PropTech, no footprint; wants first CRM + AI, asked for 15-day trial before deciding."),
 (4513959,"Prashanta Das","Ashwini Nirmal","Jawed Alam","Google",5,"Channel partner","Kolkata",False,"Partial","AMBER",None,False,False,False,None,0,"OPEN","Laxmi Realty, small owner-operated Kolkata CP on Excel; verified proprietor, 4-5 users, asked detailed email follow-up."),
 (4513950,"Sukshith Shetty","Revati Ambike","Panchasheel Tare","Organic",5,"Developer","Bangalore",False,"Partial","AMBER",None,False,False,False,"Zoho",0,"OPEN","Aspada Developers (Shivamogga), genuine plotted+apartment developer on Zoho; quote sent (displacement play), budget not captured."),
 (4513785,"Sandeep","Ashwini Nirmal","Pranith A B","Organic",5,"Developer","Bangalore",False,"Partial","RED",3,True,False,True,None,1,"OPEN","CLPD, real 25-yr Bangalore developer, but contact 'Sandeep' resolves to a different person (D Eswara Reddy); scoped to 3 users."),
 (4512862,"Sanjay sahu","Ashwini Nirmal","Niket Rathod","Google",5,"Channel partner","Navi mumbai",True,"Partial","AMBER",2,False,True,False,"Privyr","OPEN_FU",1,"Skyline Realtech, verified Navi Mumbai CP; onsite demo, 2 real users (5 claimed), Privyr expiring, interested in AI. Dummy owner-phone."),
 (4512780,"Keshav Rajput","Ashwini Nirmal","Arzoo Choudhary","Facebook",10,"Channel partner","Noida",False,"Partial","RED",None,False,False,False,"4QT",1,"OPEN","Invest Advise Wealth Mgmt, established NCR consultancy; verified Sr Manager but confirmed staying on 4QT — came only to see AI calling."),
 (4512096,"Chandan Kumar","Revati Ambike","Santhana K","Organic",15,"Developer","Chennai",True,"Strong","GREEN",8,False,False,False,None,1,"CLOSED_WON","Rainbow Foundations, BSE-listed 30-yr Chennai developer; onsite demo, WON/booked ~Rs 2.47L at 8 users. Best deal of the week."),
 (4511975,"Praveen Chintapatla","Ashwini Nirmal","Panchasheel Tare","Organic",5,"Channel partner","Warangal",None,"Weak","RED",None,False,False,False,None,0,"OPEN","Bhoo Varaha Swamy Realtors, Warangal, zero footprint; marked demo conducted but only note is 'Ringing no response' — no real demo."),
 (4511830,"Mangal Baid","Revati Ambike","Jawed Alam","Organic",5,"Developer","Kolkata",False,"Partial","AMBER",None,False,False,False,None,0,"OPEN","Prasad Castings & Buildcon, verified RERA developer (185 unsold units, active ads, no CRM) — strong latent need; contact is Director of a different group entity."),
 (4510752,"Shivkumar Singh","Ashwini Nirmal","Alok Tiwari","WhatsApp",11,"Developer","Mumbai",True,"Weak","RED",None,False,False,False,None,0,"OPEN","'Shristi Group' identity unresolved (NO_DATA); onsite demo, owner then said channel partner and 'give me time' — no budget."),
 (4510681,"Chhavi Bansal","Revati Ambike","Arzoo Choudhary","Organic",35,"Developer","Gurgaon",False,"Weak","RED",15,False,False,False,None,2,"OPEN","VD Vanchers, claims developer w/ 6 projects & 35 seats but audit found an agent ~15 staff and no trace of the contact; half-finished demo."),
 (4510461,"Vaibhav Ahuja","Ashwini Nirmal","Arzoo Choudhary","Organic",5,"Channel partner","Delhi",False,"Strong","GREEN",None,False,False,False,None,2,"OPEN","Ananta Altitude, verified Co-Founder, NCR commercial-leasing advisory; strong BANT, 5 seats, warm across two sessions."),
 (4510425,"Ashish Midhal","Revati Ambike","Niket Rathod","Google",10,"Channel partner","Mumbai",False,"Weak","RED",None,False,True,False,None,1,"CLOSED_UNQUALIFIED","Digilabz, Delhi digital-marketing agency wanting an AI bot — off-ICP; dummy phone; closed unqualified."),
 (4509764,"Shyam Mithiya","Revati Ambike","Alok Tiwari","Facebook",25,"Channel partner","Mumbai",True,"Strong","GREEN",None,False,False,False,None,1,"CLOSED_WON","Bricksage Property Advisory, Mumbai broker 'in formation'; onsite demo, closed WON with Rs 90,000 paid despite thin footprint."),
 (4509559,"Shubham Gupta","Ashwini Nirmal","Disha Kadam","Google",6,"Channel partner","Jaipur",False,"Weak","AMBER",None,False,False,False,None,1,"OPEN","SBR Realty, Jaipur CP with confirmed 6-user team; no web footprint; Sales Head DM paused purchase ~3 months on budget."),
 (4509516,"Dweep Chaudhary","Revati Ambike","Sakshi Kadu","Google",10,"Developer","Gurgaon",False,"Partial","AMBER",None,False,False,True,None,1,"OPEN","Briston, real on-ICP Gurugram developer with township launch, quoted 10 users — but contact is a non-DM and mgmt unresponsive post-demo."),
 (4509163,"Monica Gill","Revati Ambike","Ankur Singhal","Organic",15,"Developer","Jabalpur",False,"Weak","AMBER",None,False,False,False,None,2,"OPEN","Patel Builders, Jabalpur, claimed developer; zero footprint & enrichment NO_DATA; demo+quote done (Rs1200/user+50k setup) but stalling."),
 (4509085,"Ashish Gupta","Ashwini Nirmal","Suraj Chauhan","Facebook",5,"Channel partner","New delhi",False,"Weak","RED",None,False,False,True,None,0,"OPEN","Jasron Real Estate, no footprint; contact resolves to an accountant at a different firm; demo done after no-shows, wants to loop in his boss."),
 (4508567,"Roshan Patel","Revati Ambike","Disha Kadam","Google",6,"Channel partner","Chattisgarh",False,"Weak","AMBER",5,False,False,True,"HubSpot",1,"OPEN","Shree Sidhi Vinayak Infra, 6-yr Bilaspur CP, ~5 users; contact phone resolves to a different person; familiar with HubSpot, wants 2-3 months."),
 (4508155,"Raj","Ashwini Nirmal","Ananya Kumari","Organic",5,"Channel partner","Rajkot",False,"Weak","RED",None,True,False,True,None,0,"OPEN","Affitto Space, Rajkot; phone MISMATCH (registered to 'aasha kumari'), no footprint; owner absent from demo, price-shopping other CRMs."),
 (4507980,"Sohaib Khan Pratap","Revati Ambike","Anuj Pathak","Google",5,"Developer","Surat",False,"Partial","AMBER",None,False,False,False,None,1,"OPEN","Ukaz Group, Surat residential developer (2 projects), verified contact but no web/RERA footprint; demo+quote (Rs36k) then going quiet."),
 (4497933,"Alima Hassan","Revati Ambike","Ganesh Vamsee","Google",6,"Channel partner","Bangalore",False,"Strong","GREEN",None,False,False,False,"Rolo CRM",3,"CLOSED_WON","Bridgekeys Infratech, RERA Bangalore broker on Rolo CRM; contact junior HR but deal closed WON, Rs 50,112 received 20-Jul."),
 (4497898,"Yash Patel","Revati Ambike","Ankur Singhal","Facebook",30,"Developer","Mumbai",True,"Strong","GREEN",None,False,False,False,None,1,"OPEN","Raj Group, verified Director of a 37-yr Mumbai/MMR developer; onsite demo, 30 seats, quote sent — senior, real, strong."),
 (4497625,"Tarun Dev Singh","Ashwini Nirmal","Arzoo Choudhary","WhatsApp",5,"Developer","Noida",False,"Weak","AMBER",None,False,False,False,None,4,"OPEN","Contact is a Digital Marketing Manager, not the buyer; company flip-flops (AP/Jaypee Infratech) — employer conflict; comparing CRM quotes."),
 (4497535,"Aksh Garg","Ashwini Nirmal","Suraj Chauhan","Organic",5,"Channel partner","Faridabad",False,"Partial","AMBER",None,False,False,False,None,1,"OPEN","SG Properties, Faridabad residential CP (Instagram-only); online demo 1+5 users incl WhatsApp API (800/user+32k), proposal shared, callback."),
 (4495252,"Vanish Mathur","Revati Ambike","Sakshi Kadu","Organic",5,"Developer","Jaipur",False,"Partial","AMBER",6,False,False,False,None,1,"OPEN","Charu Group, Jaipur residential developer (website confirmed) on Excel; ~6 users, actively researching CRMs, discussing internally."),
 (4495027,"Kanishk Garg","Ashwini Nirmal","Ankur Singhal","Organic",10,"Channel partner","Gurugram",False,"Weak","RED",None,False,False,False,None,1,"CLOSED_UNQUALIFIED","Elegant Homez, Gurugram CP (Aurum referral) wanted AI+CRM for 10; turned 'not interested' — closed unqualified."),
 (4493320,"Sai Venkata Rama Chandra Reddy","Ashwini Nirmal","Ganesh Vamsee","Organic",10,"Developer","Vishakhapatnam",True,"Partial","GREEN",None,False,False,False,"CloudBild",1,"OPEN","Burugupalli Infrastructures, Vizag developer (3 projects, 8 sales); onsite demo, on CloudBild with service issues — switch opportunity, quote pending."),
 (4458050,"Ompal Shekhawat","Ashwini Nirmal","Ankur Singhal","Organic",15,"Developer","Kota",False,"Weak","AMBER",None,False,False,False,None,0,"OPEN","Ompal Singh Shekhawat, verified specialist at Shubham Group (Kota developer); wants only lead management; long unresponsive, ~7 true seats, no follow-up logged."),
 (4457507,"Shubham Sonkusare","Ashwini Nirmal","Tejas Mehta","Organic",100,"Developer","Raipur",None,"Weak","RED",None,False,False,False,"Runo",0,"OPEN","Singhania Buildcon, Raipur developer on Runo; contact a new-joinee not on LinkedIn who refused a demo ('just send quote'). 100-seat unverified; ghost demo."),
 (4456125,"Anuj jha","Ashwini Nirmal","Niket Rathod","Google",7,"Channel partner","Navi mumbai",True,"Partial","AMBER",4,False,True,False,None,2,"OPEN","Sai Properties, no-footprint Kharghar broker; verified identity, onsite demo, 4 real users (7 claimed), quoted 600/user+5k. Dummy owner-phone."),
 (4456056,"Golak Patro","Ashwini Nirmal","Tejas Mehta","Facebook",20,"Channel partner","pune",True,"Weak","RED",None,False,False,False,"Leadrat",1,"OPEN","Flatcon Realtors, real Pune resale broker on Leadrat; but contact resolves to a STUDENT (role unconfirmed); disqualified post-demo (AI-only, no CRM need)."),
 (4410867,"Satish","Revati Ambike","Niket Rathod","Organic",4,"Channel partner","Mumbai",True,"Strong","AMBER",None,True,True,False,None,0,"OPEN","Soulful Properties, verified Founder, established Andheri West brokerage; onsite demo w/ both owners, quoted 4 seats. Strong but sub-5 + dummy phone + first-name only."),
 (4184031,"Arun Das","Revati Ambike","Panchasheel Tare","Organic",6,"Channel partner","Kolkata",None,"Weak","RED",None,False,False,False,None,0,"OPEN","Digital Synergie, Kolkata marketing agency wanting CRM for a client's leads; on Excel; unresponsive since April, no sales follow-up after demo."),
]

COLS = ["id","name","creator","owner","source","lic","typ","city","onsite","bant","verdict",
        "seats_verified","junk","dummy","unver","competitor","fu","fc","one_line"]
rows = [dict(zip(COLS, r)) for r in D]
N = len(rows)

# ---- conversion model ----
def tier(l):
    l = l or 0
    if l >= 10: return "10+"
    if l >= 5: return "5-10"
    return "<5"
def score(d):
    S = -2.2
    S += {"Strong":1.2,"None":-0.3,"Partial":-1.6,"Weak":-2.3}[d["bant"]]
    b = CITYMAP.get(d["city"], ("other",False))[0]
    S += {"hc":1.1,"metro":-0.3,"other":-0.2}[b]
    S += 0.6 if d["onsite"] is True else -0.1
    S += 0.3 if d["typ"]=="Developer" else -0.3
    S += {"10+":0.4,"5-10":0.2,"<5":-0.4}[tier(d["lic"])]
    S += {"Organic":0.4,"Google":0.0,"WhatsApp":0.0,"Facebook":-1.6,"Instagram":-1.6}.get(d["source"],0.0)
    p = 1/(1+math.exp(-S))
    if S >= -1.4: band="HOT"
    elif S >= -2.0: band="WARM"
    elif S >= -2.75: band="MID"
    else: band="COLD"
    return round(p,3), band
for d in rows:
    d["tier"]=tier(d["lic"]); d["prob"],d["band"]=score(d)
    d["main6"]=CITYMAP.get(d["city"],("other",False))[1]
    d["is5"]= (d["lic"] or 0)>=5
    d["mode"]="Onsite" if d["onsite"] is True else ("Online" if d["onsite"] is False else "?")

# ---- aggregates ----
verdict = collections.Counter(d["verdict"] for d in rows)
band = collections.Counter(d["band"] for d in rows)
tiers = collections.Counter(d["tier"] for d in rows)
five = sum(1 for d in rows if d["is5"])
dev = sum(1 for d in rows if d["typ"]=="Developer")
cp = N-dev
onsite_all = sum(1 for d in rows if d["onsite"] is True)
main6 = sum(1 for d in rows if d["main6"])
onsite_m6 = sum(1 for d in rows if d["main6"] and d["onsite"] is True)
enterprise40 = sum(1 for d in rows if (d["lic"] or 0)>=40)
wins = sum(1 for d in rows if d["fc"]=="CLOSED_WON")
# seat inflation: claimed>=5 but verified<5
inflated = [d for d in rows if d["seats_verified"] is not None and d["seats_verified"]<5 and (d["lic"] or 0)>=5]

SOURCE = {}
for s in ["Organic","Google","Facebook","WhatsApp"]:
    sub=[d for d in rows if d["source"]==s]
    SOURCE[s]={"demos":len(sub),"five":sum(1 for d in sub if d["is5"]),
      "green":sum(1 for d in sub if d["verdict"]=="GREEN"),"red":sum(1 for d in sub if d["verdict"]=="RED"),
      "dev":sum(1 for d in sub if d["typ"]=="Developer"),"hotwarm":sum(1 for d in sub if d["band"] in("HOT","WARM"))}

reps={}
for cr in ["Revati Ambike","Ashwini Nirmal","Gayatri More"]:
    sub=[d for d in rows if d["creator"]==cr]
    if not sub: continue
    reps[cr]={"demos":len(sub),"GREEN":sum(1 for d in sub if d["verdict"]=="GREEN"),
      "RED":sum(1 for d in sub if d["verdict"]=="RED"),"five":sum(1 for d in sub if d["is5"]),
      "dev":sum(1 for d in sub if d["typ"]=="Developer"),"onsite":sum(1 for d in sub if d["onsite"] is True),
      "hotwarm":sum(1 for d in sub if d["band"] in("HOT","WARM")),
      "badname":sum(1 for d in sub if d["junk"]),"unver":sum(1 for d in sub if d["unver"])}

alloc = collections.Counter(d["owner"] for d in rows)
routing={"dev_to_revati":sum(1 for d in rows if d["typ"]=="Developer" and d["creator"]=="Revati Ambike"),
 "dev_to_ashwini":sum(1 for d in rows if d["typ"]=="Developer" and d["creator"]=="Ashwini Nirmal"),
 "cp_to_ashwini":sum(1 for d in rows if d["typ"]!="Developer" and d["creator"]=="Ashwini Nirmal"),
 "cp_to_revati":sum(1 for d in rows if d["typ"]!="Developer" and d["creator"]=="Revati Ambike")}

alerts={"zero_followup":sum(1 for d in rows if (d["fu"] or 0)==0 and isinstance(d["fu"],int)),
 "dummy_phone":sum(1 for d in rows if d["dummy"]),"unverified":sum(1 for d in rows if d["unver"]),
 "bad_name":sum(1 for d in rows if d["junk"])}
# zero follow-up on open, non-dead demos worth chasing
zero_fu_open=[d for d in rows if (isinstance(d["fu"],int) and d["fu"]==0) and d["fc"]=="OPEN"]

# ---- funnel / campaigns / cohort / losses (from queries) ----
FUNNEL={"created":72,"demoed":35,"leak":37,"demos_conducted":49,"older_demoed":49-14}  # placeholder recompute below
FUNNEL={"created":72,"demoed":35,"leak":72-35,"demos_conducted":49}
CAMP={"Meta Lead-Gen (Apr-24)":5,"Meta Lead-Gen (Jun-25)":3,"Google Brand Search":4,"Google Search (jan24)":3,"Other/untagged paid":3}
utm_tagged=18
COHORT={"demos":104,"lost":38,"won":7,"open":104-38-7}

LOSS=[
 (4516792,"Budget",None,0),(4510425,"Budget",None,1),(4508380,"Wrong/Unverified-contact",None,1),
 (4476885,"Competitor/Existing-CRM","HomeLeads",5),(4474591,"Timeline/Not-now",None,3),(4473579,"Not-interested",None,4),
 (4463072,"Not-interested",None,1),(4462721,"Budget",None,3),(4460026,"Competitor/Existing-CRM","IQsetter",3),
 (4459146,"Timeline/Not-now",None,6),(4456258,"Competitor/Existing-CRM",None,3),(4449605,"Competitor/Existing-CRM","Realty Organiser",5),
 (4449519,"Timeline/Not-now",None,4),(4447660,"Not-interested",None,6),(4439543,"Budget",None,2),
 (4432338,"Not-interested",None,4),(4430091,"Not-interested",None,4),(4417522,"Timeline/Not-now",None,6),
 (4416482,"Competitor/Existing-CRM",None,2),(4415805,"Not-interested",None,4),(4404993,"Timeline/Not-now",None,7),
 (4404535,"Competitor/Existing-CRM","Vabble.io",1),(4403952,"Non-responsive",None,10),(4399655,"Non-responsive",None,3),
 (4396547,"Wrong/Unverified-contact",None,2),
 (4396191,"Non-responsive",None,8),(4390097,"Competitor/Existing-CRM",None,0),(4384448,"Competitor/Existing-CRM","Pixxie",7),
 (4375979,"Not-interested",None,7),(4375548,"Timeline/Not-now",None,12),(4365976,"Timeline/Not-now",None,10),
 (4364260,"Not-interested",None,5),(4359465,"Timeline/Not-now",None,8),(4359152,"Not-interested",None,8),
 (4334986,"Sub-ICP/Too-small",None,3),(4307373,"Competitor/Existing-CRM","Daebuild",10),(4250407,"Competitor/Existing-CRM",None,3),
 (4234642,"Timeline/Not-now",None,6),(4177640,"Competitor/Existing-CRM",None,1),(3972948,"Budget",None,4),
 (3809287,"Not-interested",None,1),(3643697,"Competitor/Existing-CRM",None,2),(3607120,"Competitor/Existing-CRM",None,3),
 (3581462,"Sub-ICP/Too-small",None,1),(3579293,"Competitor/Existing-CRM","NeoDove",7),(3557029,"Not-interested",None,6),
 (3398910,"Non-responsive",None,5),(3395177,"Timeline/Not-now",None,6),(3291277,"Competitor/Existing-CRM",None,6),
 (2593450,"Not-interested",None,10),
]
lr=collections.Counter(x[1] for x in LOSS)
comp=collections.Counter(x[2] for x in LOSS if x[2])
att=[x[3] for x in LOSS]
zero_loss=[x for x in LOSS if x[3]==0]
loss_price = lr["Budget"]+lr["Competitor/Existing-CRM"]

SNAP={"week_start":WK_START,"week_end":WK_END,"N":N,"five":five,"green":verdict["GREEN"],
 "verdict":dict(verdict),"band":dict(band),"tier":dict(tiers),"dev":dev,"cp":cp,
 "onsite_all":onsite_all,"main6":main6,"onsite_m6":onsite_m6,"enterprise40":enterprise40,"wins":wins,
 "seat_inflated":len(inflated),"source":SOURCE,"creator":{k:v["demos"] for k,v in reps.items()},
 "alloc":dict(alloc),"routing":routing,"alerts":alerts,
 "targets":{"five":50,"green":25,"devshare":0.5,"onsite_m6":0.4},
 "funnel":FUNNEL,"campaign":CAMP,"utm_tagged":utm_tagged,"cohort":COHORT,"reps":reps,
 "losses":{"n":len(LOSS),"avg_attempts":round(statistics.mean(att),1),"zero_followup":len(zero_loss),
   "reasons":dict(lr),"competitors":dict(comp),"price_related":loss_price}}
json.dump(SNAP,open(f"{BASE}/snapshot_{WK}.json","w"),indent=2)

# load prior snapshot for WoW
try: PREV=json.load(open(f"{BASE}/snapshot_2026-07-12.json"))
except: PREV=None

# ================= EXCEL =================
NAVY="1F3864";BLUE="2E5496";TEAL="1F6E6E";GREENBG="E2EFDA";AMB="FFF2CC";REDBG="FBE4E4";WHITE="FFFFFF";GREENF="1E7145";REDF="9C0006";GOLD="FFF4D6"
thin=Side(style="thin",color="BFBFBF");bd=Border(left=thin,right=thin,top=thin,bottom=thin)
def hf(s=10,c=WHITE,b=True):return Font(name="Arial",size=s,bold=b,color=c)
def f(s=9,c="000000",b=False):return Font(name="Arial",size=s,bold=b,color=c)
wrap=Alignment(wrap_text=True,vertical="top");ctr=Alignment(horizontal="center",vertical="center")
left=Alignment(horizontal="left",vertical="center");ctrw=Alignment(horizontal="center",vertical="center",wrap_text=True)
wb=Workbook()
def title(ws,t,span,c=NAVY):
    x=ws.cell(row=1,column=1,value=t);x.font=hf(12,WHITE,True);x.fill=PatternFill("solid",fgColor=c);x.alignment=left
    ws.merge_cells(start_row=1,start_column=1,end_row=1,end_column=span);ws.row_dimensions[1].height=24
def head(ws,hs,row,c=BLUE):
    for i,h in enumerate(hs):
        x=ws.cell(row=row,column=i+1,value=h);x.font=hf(9,WHITE,True);x.fill=PatternFill("solid",fgColor=c);x.alignment=ctrw;x.border=bd
def cv(ws,r,c,v,b=False,al=None,fill=None,fc="000000",nf=None):
    x=ws.cell(row=r,column=c,value=v);x.border=bd;x.font=f(9,fc,b);x.alignment=al or ctr
    if fill:x.fill=PatternFill("solid",fgColor=fill)
    if nf:x.number_format=nf
T=SNAP["targets"]

# 1 Scorecard
ws=wb.active;ws.title="Scorecard";ws.sheet_view.showGridLines=False
for c,w in zip("ABCDE",[36,14,12,10,58]):ws.column_dimensions[c].width=w
title(ws,f"Marketing & Pre-Sales weekly audit — {WK_START} to {WK_END}",5)
head(ws,["Metric","Actual","Target","Status","Read"],2)
def sc(r,m,a,t,ok,read):
    cv(ws,r,1,m,True,left);cv(ws,r,2,a,True,fill=(GREENBG if ok else REDBG),fc=(GREENF if ok else REDF))
    cv(ws,r,3,t);cv(ws,r,4,"ON" if ok else "MISS",True,fc=(GREENF if ok else REDF));cv(ws,r,5,read,al=wrap)
r=3
sc(r,"Deals created (pre-sales)",FUNNEL["created"],"—",True,"Top-of-funnel volume up sharply vs last week (51)");r+=1
sc(r,"Demo conducted (of those created)",f'{FUNNEL["demoed"]} ({FUNNEL["demoed"]/FUNNEL["created"]:.0%})',"≥85%",False,"49% show-rate — 37 of 72 new leads leaked with no demo");r+=1
sc(r,"Demos conducted (all, pre-sales)",N,"—",True,"49 demos — up from 43 last week");r+=1
sc(r,"Demos of 5+ licences (claimed)",five,T["five"],five>=T["five"],f"{five/N:.0%} of demos tagged 5+ — but {len(inflated)} verify to <5 real seats (seat inflation)");r+=1
sc(r,"GREEN (well-qualified)",verdict["GREEN"],T["green"],False,f"{verdict['GREEN']/N:.0%} GREEN — 3 of the 7 are the week's 3 wins");r+=1
sc(r,"RED (shouldn't be booked)",f'{verdict["RED"]} ({verdict["RED"]/N:.0%})',"<10%",False,"33% RED — ghost demos, unverified contacts, sub-ICP");r+=1
sc(r,"Developer share",f'{dev}/{N} ({dev/N:.0%})',"≥50%",False,"Below floor again — still CP-heavy");r+=1
sc(r,"Onsite (Main-6)",f'{onsite_m6}/{main6} ({onsite_m6/main6:.0%})',"≥40%",onsite_m6/main6>=0.4,"38% — sharply up from 15% last week; on-ground demos returning");r+=1
sc(r,"Enterprise (40+ seats, claimed)",enterprise40,"≥1",False,"3 claimed 40+ (Wallfort 50, Mauli 250, Singhania 100) — but ALL are ghost/disqualified/refused-demo. Zero real enterprise demos");r+=1
sc(r,"Wins booked",wins,"—",True,"3 wins: Rainbow Foundations (Chennai), Shyam/Bricksage & Alima/Bridgekeys (both Blr/Mum)");r+=1
sc(r,"HOT + WARM",band.get("HOT",0)+band.get("WARM",0),"—",True,f"{band.get('HOT',0)+band.get('WARM',0)} worth chasing; most landed COLD on Partial/Weak BANT");r+=1
r+=1
cv(ws,r,1,"COHORT ROT — prior fortnight's demos (29 Jun–12 Jul)",True,left,fill=REDBG);[cv(ws,r,c,"") for c in range(2,6)];r+=1
for lab,v,rd in [("Demos in that cohort",COHORT["demos"],""),
                 ("Already lost / unqualified",f'{COHORT["lost"]} ({COHORT["lost"]/COHORT["demos"]:.0%})',"37% dead within 1-3 weeks — roughly flat vs the prior cohort's 40%"),
                 ("Won",COHORT["won"],"7 wins from 104 demos"),("Still open",COHORT["open"],"")]:
    cv(ws,r,1,lab,True,left);cv(ws,r,2,v,True,fill=(REDBG if "lost" in lab.lower() else None));[cv(ws,r,c,"") for c in (3,4)];cv(ws,r,5,rd,al=wrap);r+=1

# 2 Pre-Sales Rep Scorecard
ws=wb.create_sheet("Pre-Sales Rep Scorecard");ws.sheet_view.showGridLines=False
for c,w in zip("ABCDEFGHI",[18,8,8,8,9,8,10,8,10]):ws.column_dimensions[c].width=w
title(ws,"Pre-sales rep quality — who is generating what",9,TEAL)
head(ws,["Rep","Demos","GREEN","RED","%GREEN","5+","Developer","Onsite","HOT/WARM"],2)
r=3
for cr,v in sorted(reps.items(),key=lambda kv:-kv[1]["demos"]):
    cv(ws,r,1,cr,True,left);cv(ws,r,2,v["demos"]);cv(ws,r,3,v["GREEN"]);cv(ws,r,4,v["RED"],fill=REDBG if v["RED"]/v["demos"]>0.3 else None)
    cv(ws,r,5,v["GREEN"]/v["demos"],nf="0%");cv(ws,r,6,v["five"]);cv(ws,r,7,v["dev"]);cv(ws,r,8,v["onsite"]);cv(ws,r,9,v["hotwarm"]);r+=1
r+=1
head(ws,["Data hygiene by rep","Junk names","Unverified contact","","","","","",""],r);r+=1
for cr,v in sorted(reps.items(),key=lambda kv:-kv[1]["demos"]):
    cv(ws,r,1,cr,True,left);cv(ws,r,2,v["badname"],fill=REDBG if v["badname"] else None);cv(ws,r,3,v["unver"],fill=REDBG if v["unver"] else None)
    [cv(ws,r,c,"") for c in range(4,10)];r+=1

# 3 Funnel & Campaigns
ws=wb.create_sheet("Funnel & Campaigns");ws.sheet_view.showGridLines=False
for c,w in zip("ABCD",[34,12,12,58]):ws.column_dimensions[c].width=w
title(ws,"Top-of-funnel: created → demo, and paid campaigns",4,TEAL)
head(ws,["Funnel step","Count","%","Read"],2)
r=3
cv(ws,r,1,"Deals created by pre-sales",True,left);cv(ws,r,2,FUNNEL["created"]);cv(ws,r,3,"100%");cv(ws,r,4,"",al=wrap);r+=1
cv(ws,r,1,"— of which demo conducted",True,left);cv(ws,r,2,FUNNEL["demoed"],fill=AMB);cv(ws,r,3,FUNNEL["demoed"]/FUNNEL["created"],nf="0%");cv(ws,r,4,"Show-rate 49% — worse than last week's 67%",al=wrap);r+=1
cv(ws,r,1,"— LEAK: created, no demo",True,left);cv(ws,r,2,FUNNEL["leak"],fill=REDBG,fc=REDF);cv(ws,r,3,FUNNEL["leak"]/FUNNEL["created"],nf="0%");cv(ws,r,4,"37 new leads never reached a demo — up from 17. Biggest single leak of the report",al=wrap);r+=1
r+=1
head(ws,["Paid campaign","Demos","","Read"],r);r+=1
cn={"Meta Lead-Gen (Apr-24)":"Meta lead forms (2024-dated campaign still tagging live leads — stale)",
    "Meta Lead-Gen (Jun-25)":"Meta lead forms","Google Brand Search":"High-intent brand search — keep",
    "Google Search (jan24)":"Prospecting search","Other/untagged paid":"3 tagged to other/PMax — check"}
for k,v in CAMP.items():
    fill=REDBG if k.startswith("Meta") else (GREENBG if k.startswith("Google") else None)
    cv(ws,r,1,k,True,left,fill);cv(ws,r,2,v);cv(ws,r,3,"");cv(ws,r,4,cn.get(k,""),al=wrap);r+=1
cv(ws,r,1,"Meta total",True,left,REDBG);cv(ws,r,2,8,True,fill=REDBG,fc=REDF);cv(ws,r,3,"");cv(ws,r,4,"8 of 18 tagged paid demos are Meta. Facebook source: 8 demos → 1 GREEN, 4 RED, 1 developer, 1 HOT/WARM",al=wrap);r+=1
cv(ws,r,1,"Google total",True,left,GREENBG);cv(ws,r,2,7,True,fill=GREENBG,fc=GREENF);cv(ws,r,3,"");cv(ws,r,4,"Google source: 15 demos, best size mix and a win (Bridgekeys). Scale.",al=wrap);r+=1
cv(ws,r,1,"UTM-tagged demos",True,left);cv(ws,r,2,utm_tagged);cv(ws,r,3,"");cv(ws,r,4,"18 of 26 paid-source demos carry a UTM campaign; 8 paid demos untagged — attribution gap",al=wrap)

# 4 Source
ws=wb.create_sheet("Source");ws.sheet_view.showGridLines=False
for c,w in zip("ABCDEFGH",[14,9,9,9,9,9,11,48]):ws.column_dimensions[c].width=w
title(ws,"Channel performance",8,TEAL)
head(ws,["Source","Demos","5+","GREEN","RED","Dev","HOT/WARM","Read"],2)
notes={"Organic":"Biggest channel (23), most developers, most HOT/WARM. Protect & grow.",
 "Google":"15 demos, best size mix + a win (Bridgekeys). Scale.",
 "Facebook":"8 demos → 1 GREEN, 4 RED, 1 developer. Still the problem channel — 4th week of confirmation. Cut/re-target.",
 "WhatsApp":"Only 3 demos, all low-quality (1 GREEN mislabel, mismatched contacts). Thin, watch."}
r=3
for s,v in sorted(SOURCE.items(),key=lambda kv:-kv[1]["demos"]):
    fill=REDBG if s in("Facebook","WhatsApp") else (GREENBG if s in("Organic","Google") else None)
    cv(ws,r,1,s,True,left,fill);cv(ws,r,2,v["demos"]);cv(ws,r,3,v["five"]);cv(ws,r,4,v["green"]);cv(ws,r,5,v["red"]);cv(ws,r,6,v["dev"]);cv(ws,r,7,v["hotwarm"]);cv(ws,r,8,notes.get(s,""),al=wrap);r+=1

# 5 Losses
ws=wb.create_sheet("Losses");ws.sheet_view.showGridLines=False
for c,w in zip("ABCD",[28,10,14,58]):ws.column_dimensions[c].width=w
title(ws,f"Deals lost last week ({len(LOSS)}, 5+ seats) — why, and how hard sales chased",4,TEAL)
head(ws,["Loss reason","Deals","Avg attempts","Read"],2)
r=3
for k,v in lr.most_common():
    sub=[x[3] for x in LOSS if x[1]==k]
    cv(ws,r,1,k,True,left);cv(ws,r,2,v);cv(ws,r,3,round(statistics.mean(sub),1) if sub else "")
    cv(ws,r,4,("Merge with Budget → the true 'lost on price' number" if k.startswith("Competitor") else ""),al=wrap);r+=1
cv(ws,r,1,"Price-related (Budget + Competitor)",True,left,GOLD);cv(ws,r,2,loss_price,True,fill=GOLD);cv(ws,r,3,"");cv(ws,r,4,f"{loss_price} of {len(LOSS)} losses ({loss_price/len(LOSS):.0%}) are price/incumbent — the dominant loss driver",al=wrap);r+=1
r+=1
head(ws,["Competitor we lost to (named)","Deals","","Read"],r);r+=1
for k,v in comp.most_common(10):
    cv(ws,r,1,k,True,left,REDBG if v>1 else None);cv(ws,r,2,v);cv(ws,r,3,"");cv(ws,r,4,"",al=wrap);r+=1
cv(ws,r,1,"(most competitor losses cite an unnamed 'other CRM')",al=left);[cv(ws,r,c,"") for c in (2,3,4)];r+=2
cv(ws,r,1,"Avg sales attempts before giving up",True,left);cv(ws,r,2,round(statistics.mean(att),1),True,fill=GOLD);cv(ws,r,3,"");cv(ws,r,4,"Bimodal: some chased 10-12 times, others killed early",al=wrap);r+=1
cv(ws,r,1,"Lost with ZERO follow-up",True,left);cv(ws,r,2,len(zero_loss),True,fill=REDBG,fc=REDF);cv(ws,r,3,"");cv(ws,r,4,f"#{zero_loss[0][0]} (budget) and #{zero_loss[1][0]} (lost to a competitor) — killed with no post-demo save attempt",al=wrap);r+=2
head(ws,["Deal","Reason","Attempts","Competitor"],r);r+=1
for x in sorted(LOSS,key=lambda z:z[3]):
    cv(ws,r,1,f"#{x[0]}",al=left);cv(ws,r,2,x[1],al=left);a=x[3]
    cv(ws,r,3,a,fill=REDBG if a==0 else None,fc=REDF if a==0 else "000000");cv(ws,r,4,x[2] or "",al=left);r+=1

# 6 HOT list
ws=wb.create_sheet("HOT list");ws.sheet_view.showGridLines=False
cols=[("Prob",7),("Band",7),("Deal ID",10),("Name",22),("Seats",6),("City",14),("Type",15),("Owner",16),("Follow-ups",9),("Next action",60)]
for i,(h,w) in enumerate(cols):ws.column_dimensions[get_column_letter(i+1)].width=w
title(ws,"Chase this week — HOT + WARM",len(cols),TEAL)
head(ws,[c[0] for c in cols],2)
r=3
for d in sorted([x for x in rows if x["band"] in("HOT","WARM")],key=lambda x:-x["prob"]):
    na=d["one_line"]
    vals=[d["prob"],d["band"],d["id"],d["name"],d["lic"],d["city"],d["typ"],d["owner"],d["fu"],na]
    for ci,v in enumerate(vals,1):
        cv(ws,r,ci,v,al=(wrap if ci==10 else (left if ci in(4,6,7,8) else ctr)),nf=("0%" if ci==1 else None))
    ws.cell(row=r,column=2).fill=PatternFill("solid",fgColor=GREENBG if d["band"]=="HOT" else AMB)
    if isinstance(d["fu"],int) and d["fu"]==0:
        ws.cell(row=r,column=9).fill=PatternFill("solid",fgColor=REDBG);ws.cell(row=r,column=9).font=f(9,REDF,True)
    r+=1
if band.get("HOT",0)+band.get("WARM",0)==0:
    cv(ws,r,1,"No demos scored HOT/WARM this week — see the strongest AMBER-GREEN in 'All demos'",al=left)

# 7 Allocation & Routing
ws=wb.create_sheet("Allocation & Routing");ws.sheet_view.showGridLines=False
for c,w in zip("ABCD",[26,12,14,54]):ws.column_dimensions[c].width=w
title(ws,"Sales allocation, and pre-sales lead routing",4,TEAL)
head(ws,["Sales owner","Demos","Even-split","Note"],2)
tgt=round(N/len(alloc),1);r=3
for o,c in sorted(alloc.items(),key=lambda kv:-kv[1]):
    cv(ws,r,1,o,True,left);cv(ws,r,2,c);cv(ws,r,3,tgt);cv(ws,r,4,("Under-fed" if c<tgt-1 else ("Over-fed" if c>tgt+1 else "In line")),al=left);r+=1
r+=1
head(ws,["Routing (developers→Revati, channel partners→Ashwini)","Count","","Verdict"],r);r+=1
for lab,k,good in [("Developers → Revati (correct)","dev_to_revati",True),("Developers → Ashwini (mis-routed)","dev_to_ashwini",False),
                   ("Channel partners → Ashwini (correct)","cp_to_ashwini",True),("Channel partners → Revati (mis-routed)","cp_to_revati",False)]:
    cv(ws,r,1,lab,True,left);cv(ws,r,2,routing[k],True,fill=(GREENBG if good else REDBG),fc=(GREENF if good else REDF));cv(ws,r,3,"");cv(ws,r,4,("Good" if good else "Mis-routed"),al=left);r+=1

# 8 All demos
ws=wb.create_sheet(f"All demos ({N})");ws.freeze_panes="A3"
cols=[("Deal ID",10),("Name",22),("Creator",14),("Owner",16),("Source",10),("Seats",6),("Tier",7),("City",14),("Type",15),("Mode",8),("BANT",8),("Verdict",8),("Prob",7),("Band",7),("Follow-ups",9),("One-line",58)]
for i,(h,w) in enumerate(cols):ws.column_dimensions[get_column_letter(i+1)].width=w
title(ws,f"All demos conducted {WK_START} to {WK_END}",len(cols))
head(ws,[c[0] for c in cols],2)
r=3
for d in sorted(rows,key=lambda x:-x["prob"]):
    vals=[d["id"],d["name"],d["creator"],d["owner"],d["source"],d["lic"],d["tier"],d["city"],d["typ"],d["mode"],d["bant"],d["verdict"],d["prob"],d["band"],d["fu"],d["one_line"]]
    for ci,v in enumerate(vals,1):
        cv(ws,r,ci,v,al=(wrap if ci==16 else (left if ci in(2,3,4,8,9) else ctr)),nf=("0%" if ci==13 else None))
    vc=ws.cell(row=r,column=12);vd=d["verdict"]
    vc.fill=PatternFill("solid",fgColor={"GREEN":GREENBG,"AMBER":AMB,"RED":REDBG}[vd]);vc.font=f(9,{"GREEN":GREENF,"AMBER":"9C6500","RED":REDF}[vd],True)
    r+=1
ws.auto_filter.ref=f"A2:P{r-1}"

# 9 WoW
ws=wb.create_sheet("WoW");ws.sheet_view.showGridLines=False
for c,w in zip("ABCD",[34,14,14,14]):ws.column_dimensions[c].width=w
title(ws,"Week over week",4,TEAL)
head(ws,["Metric","This wk (13-19 Jul)","Last wk (6-12 Jul)","Delta"],2)
def delta(a,b):
    try: return f"{a-b:+d}"
    except: return ""
if PREV:
    pv=PREV
    pairs=[("Demos conducted",N,pv["N"]),("5+ demos",five,pv["five"]),
     ("GREEN",verdict["GREEN"],pv["green"]),("RED",verdict["RED"],pv["verdict"].get("RED",0)),
     ("Developer share %",f"{dev/N:.0%}",f"{pv['dev']/pv['N']:.0%}"),
     ("Onsite Main-6",f"{onsite_m6}/{main6}",f"{pv['onsite_m6']}/{pv['main6']}"),
     ("HOT+WARM",band.get('HOT',0)+band.get('WARM',0),pv['band'].get('HOT',0)+pv['band'].get('WARM',0)),
     ("Wins",wins,pv.get("wins",2)),
     ("Created→demo leak",FUNNEL["leak"],pv["funnel"]["leak"]),
     ("Facebook demos",SOURCE["Facebook"]["demos"],pv["source"].get("Facebook",{}).get("demos",0)),
     ("Losses (5+)",len(LOSS),pv["losses"]["n"]),
     ("Cohort death rate",f'{COHORT["lost"]/COHORT["demos"]:.0%}',f'{pv["cohort"]["lost"]/pv["cohort"]["demos"]:.0%}')]
    r=3
    for m,a,b in pairs:
        cv(ws,r,1,m,True,left);cv(ws,r,2,a);cv(ws,r,3,b);cv(ws,r,4,delta(a,b) if isinstance(a,int) and isinstance(b,int) else "");r+=1
else:
    cv(ws,3,1,"No prior snapshot found",al=left)

wb.save(f"{BASE}/Marketing_Weekly_{WK}.xlsx")
print("SAVED",wb.sheetnames)
print("N",N,"5+",five,"GREEN",verdict["GREEN"],"AMBER",verdict["AMBER"],"RED",verdict["RED"])
print("bands",dict(band),"dev",dev,"cp",cp,"onsite_all",onsite_all,"main6",main6,"onsite_m6",onsite_m6)
print("tiers",dict(tiers),"ent40",enterprise40,"wins",wins,"inflated",len(inflated))
print("reps",{k:(v["demos"],v["GREEN"],v["RED"]) for k,v in reps.items()})
print("routing",routing)
print("alloc",dict(alloc))
print("losses",len(LOSS),"avg",round(statistics.mean(att),1),"zero",len(zero_loss),"price",loss_price)
print("HOTWARM deals",[(d["id"],d["band"],d["prob"]) for d in rows if d["band"] in("HOT","WARM")])
print("zero_fu_open",[d["id"] for d in zero_fu_open])
