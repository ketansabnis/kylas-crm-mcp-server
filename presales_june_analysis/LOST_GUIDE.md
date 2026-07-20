# Lost/Unqualified Deal — lifecycle & sales-effort extraction

Today = 2026-07-07. Each deal is a pre-sales-created Sell.Do deal (5+ licences) now Closed Lost or Closed Unqualified. Produce one record per deal.

## From get_deal
- name, owner (sales rep), pipelineStage, forecastingType-equivalent (stage tells you: "Closed Lost" vs "Closed Unqualified"), noOfLicenses, cfCity, createdAt, updatedAt, cfMeetingConductedOn.

## From get_deal_notes (read ALL notes, note author IDs and dates)
Pre-sales creators = 9062 (Revati), 54132 (Ashwini), 82379 (Gayatri). Anyone else writing notes after the demo is effectively the sales side (owner/closer).

## Derived fields
1. **created_at**, **demo_date** = cfMeetingConductedOn, **lost_date** = updatedAt (proxy — lost deals aren’t onboarded, so last-touch ≈ when marked lost; if the last substantive note is clearly the loss note, you may use its date).
2. **days_created_to_demo** = demo_date − created_at (days; null if no demo date).
3. **days_demo_to_lost** = lost_date − demo_date (days).
4. **days_total** = lost_date − created_at (days).
5. **stage** = "Lost" or "Unqualified" (from pipelineStage).
6. **sales_attempts** = count of DISTINCT sales-side follow-up attempts AFTER the demo and BEFORE the deal was marked lost. Count each dated attempt to reach/progress the client by the sales owner: a call (incl. "RNR"/"ring no response"/"not connected"/"switched off"), a WhatsApp/message, a follow-up, a quote/proposal chase, a reminder. Rules:
   - Count attempts, not outcomes. Two calls on the same note/day = 2 if clearly two attempts, else 1.
   - Do NOT count pre-sales qualification notes (by 9062/54132/82379) or the enrichment/audit notes.
   - If notes are sparse/none post-demo, sales_attempts = 0.
7. **loss_reason** = ONE of: "Non-responsive" | "Budget" | "Competitor/Existing-CRM" | "Timeline/Not-now" | "Not-interested" | "Sub-ICP/Too-small" | "Product-gap" | "Wrong/Unverified-contact" | "Other". Base it on the notes (esp. the final ones).
8. **one_line** = <=160 char summary: reason + how hard sales chased (e.g. "Non-responsive; sales made 5 calls/WA over 12 days then gave up").

## Output — write ONE JSON per deal to
/sessions/gifted-happy-euler/mnt/kylas-crm-mcp-server/presales_june_analysis/lost_deals/<deal_id>.json
Keys: deal_id, name, owner, creator_id (the createdBy note author if identifiable else null), stage, noOfLicenses, city,
created_at, demo_date, lost_date, days_created_to_demo, days_demo_to_lost, days_total,
sales_attempts, loss_reason, one_line, notes_count.
Valid JSON only. Be decisive.
