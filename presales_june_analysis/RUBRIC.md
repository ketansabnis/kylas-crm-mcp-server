# Per-Deal Assessment Rubric (Pre-Sales June Post-Mortem)

You are assessing a real-estate SaaS (Sell.Do) sales DEMO created by the PRE-SALES team.
Every deal in scope had a demo/meeting CONDUCTED (Meeting Conducted = Yes).
The PRE-SALES team's job: generate a QUALIFIED demo for a sales rep — right person, real
company, real need, adequate size, correct info captured. What happens AFTER (closing) is
Sales' job. Judge PRE-SALES quality independently of the sales outcome.

## Fields to extract from get_deal
- deal_id, deal_name
- owner (sales rep who owns it), pipeline, stage, pipeline_stage_reason
- created_at, updated_at, meeting_conducted, cfMeetingConductedOn
- noOfLicenses (int; null if missing)
- cfCity (raw string)
- cfReDeveloperOrChannelPartner (Developer / Broker / Channel partner / null)
- estimatedValue, actualValue, products
- source, campaign, cfPreviousCrm, cfRequiredTools
- cfSales, cfFirstSalesOwner, cfOwnerPhoneNumber (present or not)

## Fields to extract from get_deal_notes
- notes_count
- notes_text: concatenate all notes (author + date + body), trim each note to ~400 chars.
  Look for pre-sales notes, sales notes, and AI/BANT notes.

## Derived / judgement fields (YOUR analysis)
1. license_tier: "40+" | "10-39" | "5-9" | "1-4" | "unknown"  (from noOfLicenses)
2. city_bucket: classify cfCity ->
   - "Main6" if city is Pune, Mumbai (incl Navi Mumbai/Thane), Delhi/NCR (Delhi, New Delhi,
     Noida, Gurgaon/Gurugram, Ghaziabad, Faridabad, NCR), Bangalore/Bengaluru, Chennai, Hyderabad.
   - "Other" if any other identifiable Indian city/region.
   - "Unknown" if blank/unclear.
   Also record city_clean (normalized city name).
3. onsite_or_online: "Onsite" | "Online" | "Unknown"
   - Onsite = notes mention in-person/office visit/F2F/"went to"/"met at".
   - Online = notes mention zoom/google meet/online demo/call/screen share, OR default when a
     demo happened with no in-person signal (most tele-demos are online).
   - Unknown only if truly no signal.
4. name_valid: true/false — is the contact a real, full human/company name?
   false for junk: single word + ".", gibberish, obvious placeholder ("T Rex", "Jaat", "Sapna .").
5. bant: object with short reads:
   - budget: what notes say about budget/price/affordability (or "no signal")
   - authority: is contact the decision maker/owner? (or "no signal")
   - need: real estate CRM need / pain / current tool (or "no signal")
   - timeline: when they want to buy / urgency (or "no signal")
   - bant_score: 0-4 (count of B/A/N/T with a genuine positive signal)
   - bant_flag: "Strong"(3-4) | "Partial"(2) | "Weak"(1) | "None"(0)
6. enterprise_flag: true if (noOfLicenses>=40) OR (clearly large/reputed developer with valid
   company name). Else false.
7. pre_sales_verdict: "GREEN" | "AMBER" | "RED"  <-- HEADLINE
   - GREEN: genuinely qualified demo — real person, real company/need, licenses captured,
     adequate size (5+), info complete. Good pre-sales work EVEN IF sales later lost it.
   - AMBER: demo happened but qualification gaps — thin BANT, small size, missing info,
     unclear decision maker, or borderline ICP.
   - RED: poor pre-sales work — junk/placeholder name, no real need, wrong ICP (individual/tiny
     broker with 1 licence and no intent), obviously unqualified, or clearly a "demo for the
     number" with no substance.
8. stall_blocker: primary reason it hasn't progressed/closed — ONE of:
   "Won" | "Progressing" | "Non-responsive" | "Sales-gap" | "Budget" | "Quality/ICP" |
   "BANT-weak" | "Timeline/Not-now" | "Competitor/Existing-CRM" | "Pre-sales-gap" | "Other"
9. blocker_owner: "Pre-sales" | "Sales" | "Customer" | "Product/Pricing" | "NA-Won"
10. one_line: <=160 char verdict sentence, CRO tone, naming the real reason.

## Output
Write ONE json file per deal to:
/sessions/gifted-happy-euler/mnt/kylas-crm-mcp-server/presales_june_analysis/deals/<deal_id>.json
with ALL extracted + derived fields above. Keep notes_text but trimmed. Valid JSON only.
Be decisive on verdicts; use "unknown"/"no signal" only when notes truly lack the info.
