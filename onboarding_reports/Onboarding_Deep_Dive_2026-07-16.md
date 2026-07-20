# Onboarding Pipeline - Deep Dive & Major Concerns
**2026-07-16 - Kylas pipeline 27474 - 60 live deals (3 test deals excluded)**

## The headline

**43 of 60 deals (72%) did not genuinely move this run. 29 have not moved for two or more consecutive reviews (was 21 last run).**

| Run | Open | Progressed | Stuck | SUPER-RED |
|---|---|---|---|---|
| 2026-07-02 | 67 | 34 | 25 | 21 |
| 2026-07-07 | 58 | 29 | 27 | 15 |
| 2026-07-10 | 61 | 20 | 33 | 16 |
| 2026-07-13 | 58 | 21 | 35 | 21 |
| 2026-07-16 | 60 | 4 | 43 | 29 |

## 1. Reality check - what we tell customers vs what the ticket says

| Deal | Note says | Ticket | Live status | Verdict |
|---|---|---|---|---|
| **Kohinoor AI Calling** (stuck 8) | Outgoing AI calling issues; JIRAs raised (bulk-call list ESTATE-21040, | ESTATE-21040 | **Won't Fix** | GHOST DEPENDENCY |
| **Kohinoor AI Calling** (stuck 8) | Outgoing AI calling issues; JIRAs raised (bulk-call list ESTATE-21040, | SS-12176 | **Done** | GHOST DEPENDENCY |
| **Times Group** (stuck 8) | Inventory data uploaded; client reports discrepancies; internal data-v | ESTATE-18697 | **Done** | GHOST DEPENDENCY |
| **Mythri Builder AI Calling** (stuck 2) | AI calling flow built/tested; awaiting customer feedback and confirmat | SS-12285 | **Tech Discussion** | STUCK IN OUR QUEUE |
| **Shree Automotive** (stuck 4) | Twin of Shree Honda: OB reinitiation meeting 8 Jul; stalled since Sep- | SEP-2025 | **-** | NOT CHECKED |
| **Shree Honda** (stuck 2) | OB reinitiation meeting scheduled 8 Jul with POC/Director; long-stalle | SEP-2025 | **-** | NOT CHECKED |

## 2. Who is really blocking

**OWNER-INACTION** 23 - **UNCLEAR** 14 - **CUSTOMER** 14 - **VENDOR** 5 - **US-TECH** 3 - **US-COMMERCIAL** 1

**Parked in 'Pending on Customer' but the customer is not the blocker (10):** Doff Estate (VENDOR), Navkar Realty (OWNER-INACTION), VAZHRAA NIRMAAN PRIVATE LIMITED (OWNER-INACTION), Calicut Landmark Builders Pvt. Ltd (OWNER-INACTION), GGC AI Calling (OWNER-INACTION), Kohinoor AI Calling (US-TECH), Dreamworks Realtors (OWNER-INACTION), Dhanraj Realbuild Llp (OWNER-INACTION), Voora Developers (OWNER-INACTION), Times Group (US-COMMERCIAL)

## 3. Escalation & commercial risk

| Account | Value | Age | Stuck | Flagged since | Days | Moved since? |
|---|---|---|---|---|---|---|
| **Dhanraj Realbuild Llp** | 5-7L | 60-90 d | 8 runs | 2026-07-07 | 9 | **NO** |
| **Times Group** | 7-10L | >180 d | 8 runs | 2026-07-13 | 3 | **NO** |
| **Kunwarji Realtors** | >=10L | 60-90 d | 2 runs | 2026-07-13 | 3 | **NO** |
| **SPR Construction Pvt Ltd** | blank | 60-90 d | 8 runs | 2026-07-16 | 0 | **NO** |
| **Sangram Group** | blank | 30-60 d | 3 runs | 2026-07-16 | 0 | **NO** |
| **PROPKART4U** | blank | 14-30 d | 1 runs | 2026-07-16 | 0 | **NO** |
| **Shri Krish Housing and Properties Pvt Ltd** | 5-7L | 30-60 d | 1 runs | 2026-07-16 | 0 | **NO** |
| **Northstone Realty** | blank | 60-90 d | 0 runs | 2026-07-16 | 0 | **yes** |

## 4. Owner scorecard

| Owner | Deals | Progressed | Stuck | SUPER-RED | No next task | Note theatre | >60d old |
|---|---|---|---|---|---|---|---|
| Muntazar Mhate | 13 | 1 | 10 | **8** | 12 | 0 | 0 |
| Venkat Viswavardhan | 12 | 2 | 10 | **8** | 3 | 0 | 6 |
| Raahul Ramanan R | 8 | 0 | 4 | **4** | 6 | 0 | 4 |
| Sahil Jane | 11 | 0 | 8 | **2** | 5 | 0 | 0 |
| Shweta Gouda | 10 | 1 | 5 | **2** | 8 | 0 | 1 |
| Sourabh Sahu | 3 | 0 | 3 | **2** | 2 | 0 | 2 |
| Sanket Nampalliwar | 2 | 0 | 2 | **2** | 0 | 0 | 2 |
| Shubham Dubey | 1 | 0 | 1 | **1** | 1 | 0 | 0 |

## 5. Note theatre (same note re-pasted, zero delta)

_none_


## 6. What the pipeline is actually stuck on

**Trainings** 21 - **Bulk lead import** 12 - **WhatsApp** 8 - **Meta/Facebook** 7 - **Inventory** 6 - **IVR/Mcube/dialer** 5 - **Website** 3 - **Handover** 3 - **Portals** 2


## 7. CRM hygiene

- **37 of 60 deals have no next task.**
- **27 have no billed amount** (cannot rank by revenue at risk).
- 17 overdue tasks, 12 breached go-live dates, 8 deals with zero notes.
- **15 deals older than 60 days** still not live.

## SUPER-RED list

| Account | Owner | Runs stuck | Value | Age | Why |
|---|---|---|---|---|---|
| Ribitto Private Limited | Muntazar Mhate | 8 | blank | 30-60 d | Still Mailgun/lead-capture pending; note is a 'this week' plan, no completion. S |
| Calicut Landmark Builders Pvt. Ltd | Raahul Ramanan R | 8 | 5-7L | 60-90 d | No note after 2026-07-13 (last run) and no stage change - nothing happened since |
| SPR Construction Pvt Ltd | Raahul Ramanan R | 8 | blank | 60-90 d | No note after 2026-07-13 (last run) and no stage change - nothing happened since |
| Kohinoor AI Calling | Venkat Viswavardhan | 8 | blank | 60-90 d | No note after 2026-07-13 (last run) and no stage change - nothing happened since |
| Dhanraj Realbuild Llp | Venkat Viswavardhan | 8 | 5-7L | 60-90 d | No note after 2026-07-13 (last run) and no stage change - nothing happened since |
| Voora Developers | Raahul Ramanan R | 8 | 7-10L | >180 d | No note after 2026-07-13 (last run) and no stage change - nothing happened since |
| Times Group | Sanket Nampalliwar | 8 | 7-10L | >180 d | No note after 2026-07-13 (last run) and no stage change - nothing happened since |
| Shrimant Developers | Muntazar Mhate | 6 | 1-2L | 30-60 d | Website gap dropped from note; admin training + handover only 'targeted this wee |
| NPS DEVELOPERS | Raahul Ramanan R | 4 | 3-5L | 60-90 d | No note after 2026-07-13 (last run) and no stage change - nothing happened since |
| Shree Automotive | Sourabh Sahu | 4 | 1-2L | >180 d | No note after 2026-07-13 (last run) and no stage change - nothing happened since |
| Salahrealty Pvt Ltd | Muntazar Mhate | 3 | blank | <14 d | Still waiting inventory from client; 'this week' plan restates the same ask. |
| Growthx Estates | Muntazar Mhate | 3 | 1-2L | 14-30 d | Same pending items (Meta, bulk lead) re-planned as 'this week'. No completion. |
| Sunrise Housing (GHP Group) | Muntazar Mhate | 3 | 2-3L | 14-30 d | Base setup still being followed up; bulk lead/Meta/website/WhatsApp all still pe |
| Blueroof India | Muntazar Mhate | 3 | blank | 14-30 d | Meta/training/handover all 'tentative this week'. Scheduled != done. |
| Leonaara PVt LTD | Sahil Jane | 3 | blank | 30-60 d | No note after 2026-07-13 (last run) and no stage change - nothing happened since |
| Axon Developer | Sahil Jane | 3 | 3-5L | 30-60 d | No note after 2026-07-13 (last run) and no stage change - nothing happened since |
| Sohum Estate Agency (Sameer Chheda) | Muntazar Mhate | 3 | blank | 30-60 d | Inventory demo 'agreed for Monday' last week has slipped to 'this week' again. D |
| Sangram Group | Muntazar Mhate | 3 | blank | 30-60 d | 'No movement from client'; now threatening to put on hold. Moving toward hold is |
| Doff Estate Post Sales | Shubham Dubey | 2 | 5-7L | <14 d | No note after 2026-07-13 (last run) and no stage change - nothing happened since |
| Yashoda Infra Developer | Shweta Gouda | 2 | blank | 14-30 d | No note after 2026-07-13 (last run) and no stage change - nothing happened since |
| Navkar Realty | Venkat Viswavardhan | 2 | 3-5L | 14-30 d | Hold-till-13-Jul deadline passed; follow-up slipped (owner unwell). Nothing the  |
| VENDSPACEZ PRIVATE LIMITED | Venkat Viswavardhan | 2 | 3-5L | 14-30 d | No note after 2026-07-13 (last run) and no stage change - nothing happened since |
| Strata Capital Holdings | Shweta Gouda | 2 | blank | 30-60 d | No note after 2026-07-13 (last run) and no stage change - nothing happened since |
| VAZHRAA NIRMAAN PRIVATE LIMITED | Venkat Viswavardhan | 2 | 2-3L | 30-60 d | No note after 2026-07-13 (last run) and no stage change - nothing happened since |
| GGC AI Calling | Venkat Viswavardhan | 2 | blank | 60-90 d | No note after 2026-07-13 (last run) and no stage change - nothing happened since |
| Mythri Builder AI Calling | Venkat Viswavardhan | 2 | blank | 60-90 d | No note after 2026-07-13 (last run) and no stage change - nothing happened since |
| Kunwarji Realtors | Sanket Nampalliwar | 2 | >=10L | 60-90 d | No note after 2026-07-13 (last run) and no stage change - nothing happened since |
| Dreamworks Realtors | Venkat Viswavardhan | 2 | 5-7L | 60-90 d | No note after 2026-07-13 (last run) and no stage change - nothing happened since |
| Shree Honda | Sourabh Sahu | 2 | 2-3L | >180 d | No note after 2026-07-13 (last run) and no stage change - nothing happened since |

---

## The asks

1. **Venkat — Kohinoor AI Calling (stuck 8 runs).** The bot ticket (ESTATE-20563 / cited as SS-12176) shipped in v11.0 on **8-Jul** and the other cited ticket ESTATE-21040 is **Won't Fix**. Nothing is pending on the customer. Confirm delivery with the client and move the deal to go-live / hand-over by **Fri 18-Jul**.
2. **Venkat — Mythri Builder AI Calling (stuck 2).** ESTATE-20699 (cited as SS-12285) has sat in **"Tech Discussion" — our queue — since 26-Jun**, yet the note reads "awaiting customer feedback." Get a feasibility decision from Sharayu + tech by **Thu 17-Jul** and correct the note so it stops blaming the customer.
3. **Sanket — Times Group (₹7-10L, 50 lic, >180 days, stuck 8).** ESTATE-18697 has been **Done since 13-Feb** (5 months). Re-book the data-discrepancy review and set a real go-live date by **Fri 18-Jul**, or escalate to a commercial call. Separately, revisit the three MUST items (routing, pipeline, lead-import) marked "Not required" on a 50-licence account.
4. **Muntazar — his book (8 of 13 SUPER-RED).** This week's notes are "This week: <plan>" across almost every deal — plans, not completions. Land one **completed** milestone each on the four oldest (Ribitto ss8, Shrimant ss6, Sohum ss3, Sangram ss3), or hand them back to sales, by the **Mon 21-Jul** review.
5. **Venkat / Raahul / Muntazar — 9 GO-LIVE FICTION deals.** Each has an Actual Go-Live date set while a MUST item is still open (GRUHAM live-dated 5-May, VAZHRAA, Shrimant, SPR, NPS, Calicut, Kunwarji, i5, Shri Krish). Reconcile each: close the open MUST item, or clear the false go-live date, by **Mon 21-Jul**.

## Paste-ready version for the group

> **Onboarding review — 16 Jul.** Three things to action before Monday:
>
> **1. We're holding deals against tickets that are already closed.** Kohinoor's AI-calling bot shipped on 8-Jul (ESTATE-20563) and its other ask is Won't Fix — yet the deal has sat in "Pending on Customer" for 8 reviews. Times Group is parked on a ticket (ESTATE-18697) that's been **Done since February**. Mythri is being told "awaiting your feedback" while its ticket sits in **our own** Tech Discussion queue since 26-Jun. @Venkat @Sanket — please re-check the live ticket before the next update and move these.
>
> **2. Movement stalled: only 4 of 60 deals genuinely progressed, and SUPER-RED rose 21 → 29.** Most of this week's notes are "this week: <plan>" — intent, not completion. A new note is not movement. @Muntazar — 8 of your 13 are SUPER-RED; let's land one completed milestone each on the four oldest by Monday.
>
> **3. 9 deals show an Actual Go-Live date with a must-have step still open** (incl. GRUHAM live-dated 5-May, Shrimant, SPR, NPS). Either finish the open step or clear the date — a go-live date we don't mean makes the whole pipeline unreadable.

---

### For Ketan — before you post

- **The Muntazar point names one person hard** (8/13 SUPER-RED, the "this week: <plan>" pattern is almost entirely his book). It's accurate, but you may want a private word before it goes to the group.
- **Don't read Shweta's blank-field rate as neglect.** Her high "not tracked" number is inflated by **4 brand-new deals** she picked up this run (Winter Home, Sunita, Gagan Tondon, Northstone) that legitimately have empty checklists. Same for Raahul (4 new) and Sahil (3 new). 13 of 63 deals are new this run.
- **The AI-calling deals (GGC, Mythri, Kohinoor) disclaim CRM MUST items** as "Not required" — that is probably legitimate (bot-only scope), unlike Times Group, which disclaimed core CRM setup on a full 50-licence account. Weight Times Group, not the bots.
- **Data caveat:** 27 of 60 deals still have no billed amount, so the value bands lean on the licence count. "SEP-2025" in the reality-check sheet is a false-positive (a date, not a ticket).
