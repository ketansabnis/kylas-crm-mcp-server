# Open-Deal Triage Guide (for scoring the open pre-sales pipeline)

Today = **2026-07-06**. Each deal is an OPEN Sell.Do (real-estate CRM) deal that has had a demo. Produce a triage record per deal.

## Extract from get_deal + get_deal_notes
- name, owner (sales rep), pipeline stage, noOfLicenses, cfCity, cfReDeveloperOrChannelPartner (Developer/Channel partner/Broker), created_at, updated_at, cfMeetingConductedOn, cfOwnerPhoneNumber, cfPreviousCrm.
- notes: read ALL. Capture the latest status, who last acted, and any BANT signals. Note the DATE of the most recent substantive note.

## Derived fields
1. **aging_days** = today − created_at (days). **idle_days** = today − updated_at (days).
2. **tier3**: <5 / 5-10 / 10+ (from licences).
3. **city_class**: HOT (Hyderabad/Chennai), CORE (Mumbai/Thane, Delhi/NCR, Bangalore, Pune), OTHER.
4. **onsite_or_online**: from notes (in-person/office visit = Onsite; else Online).
5. **name_valid**: false for junk/placeholder (single word + ".", gibberish, "T Rex").
6. **bant**: read Budget / Authority / Need / Timeline from notes. If notes have NO real BANT, set **bant_flag="MISSING"** and note "needs re-qualification". Else grade **bant_flag** = Strong / Partial / Weak / None.
7. **rubric_verdict**: GREEN (genuinely qualified: real co + need + 5+ + info complete), AMBER (real but thin), RED (junk/sub-ICP/placeholder).

## Conversion probability (use the model)
Start **S = −2.2**, then add:
- BANT: Strong +1.2 · None/MISSING −0.3 · Partial −1.6 · Weak −2.3
- City: HOT +1.1 · OTHER −0.2 · CORE −0.3
- Mode: Onsite +0.6 · Online −0.1
- Type: Developer +0.3 · Channel partner/Broker −0.3
- Size: 10+ +0.4 · 5-10 +0.2 · <5 −0.4
Then **stage bump** (open-pipeline momentum): Payment Confirmed +1.2 · Hot Opportunity +0.7 · Quote Sent +0.3 · Demo Conducted +0.0 · Demo Scheduled −0.3.
Then **idle penalty**: if idle_days > 30 subtract 0.5; if idle_days > 60 subtract 1.0 (total).
**probability p = 1/(1+e^(−S))**. Band: HOT p≥0.20 · WARM 0.12–0.20 · MID 0.06–0.12 · COLD <0.06.
Record conv_prob (rounded 0-1) and band.

## Next action for Sales (specific, 1 line)
Based on stage + notes, e.g.: "Send revised quote for 8 seats & confirm GST split" / "Call DM Mr X, book onsite close meeting" / "Chase pending payment link" / "Re-confirm decision maker before next demo". Be concrete, name the step.

## Churn call — pick ONE with a reason
- **KEEP** — qualified, active, owner engaged, recent notes → stay with current sales; just execute next action.
- **REASSIGN-NEW-SALES** — good/qualified deal but STALLED on the rep (idle_days high, "no update"/no-notes gaps, owner not following up) → hand to a sharper closer.
- **BACK-TO-PRESALES** — never properly qualified (BANT MISSING / wrong contact / decision maker unconfirmed) → re-qualify before more sales effort.
- **DISQUALIFY** — RED / sub-ICP / junk contact / repeatedly non-responsive over many attempts / not-a-real-buyer → close-lost, stop spending demo capacity.

## Output — write ONE JSON per deal to
/sessions/gifted-happy-euler/mnt/kylas-crm-mcp-server/presales_june_analysis/open_focus/<deal_id>.json
with: deal_id, name, owner, stage, noOfLicenses, tier3, city_clean, city_class, dev_broker,
created_at, updated_at, aging_days, idle_days, onsite_or_online, name_valid,
bant_budget, bant_authority, bant_need, bant_timeline, bant_flag,
rubric_verdict, conv_prob, band, next_action, churn_call, churn_reason, one_line, notes_text (trimmed ~500 chars).
Valid JSON only. Be decisive.
