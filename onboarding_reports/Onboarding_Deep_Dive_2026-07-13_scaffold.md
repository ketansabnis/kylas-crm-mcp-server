# Onboarding Pipeline - Deep Dive & Major Concerns
**2026-07-13 - Kylas pipeline 27474 - 58 live deals (3 test deals excluded)**

## The headline

**35 of 58 deals (60%) did not genuinely move this run. 21 have not moved for two or more consecutive reviews (was 16 last run).**

| Run | Open | Progressed | Stuck | SUPER-RED |
|---|---|---|---|---|
| 2026-06-29 | 60 | 9 | 47 | 29 |
| 2026-07-02 | 67 | 34 | 25 | 21 |
| 2026-07-07 | 58 | 29 | 27 | 15 |
| 2026-07-10 | 61 | 20 | 33 | 16 |
| 2026-07-13 | 58 | 21 | 35 | 21 |

## 1. Reality check - what we tell customers vs what the ticket says

| Deal | Note says | Ticket | Live status | Verdict |
|---|---|---|---|---|
| **Kohinoor AI Calling** (stuck 7) | Few issues raised in outgoing calling; JIRA raised for the same. | ESTATE-21040 | **Won't Fix** | GHOST DEPENDENCY |
| **Times Group** (stuck 7) | Unit data uploaded but client reported multiple discrepancies; review  | ESTATE-18697 | **Done** | GHOST DEPENDENCY |
| **Kohinoor AI Calling** (stuck 7) | Few issues raised in outgoing calling; JIRA raised for the same. | ESTATE-20563 | **QA Clarification Required** | STUCK IN OUR QUEUE |
| **Mythri Builder AI Calling** (stuck 1) | Awaiting flow and feedback from customer. | ESTATE-20699 | **Tech Discussion** | STUCK IN OUR QUEUE |

## 2. Who is really blocking

**UNCLEAR** 21 - **CUSTOMER** 16 - **OWNER-INACTION** 8 - **VENDOR** 7 - **US-COMMERCIAL** 4 - **US-TECH** 2

**Parked in 'Pending on Customer' but the customer is not the blocker (5):** Calicut Landmark Builders Pvt. Ltd (OWNER-INACTION), Kohinoor AI Calling (US-TECH), Dhanraj Realbuild Llp (US-COMMERCIAL), Upcurve consumer Technologies Pvt Ltd (US-COMMERCIAL), Times Group (US-COMMERCIAL)

## 3. Escalation & commercial risk

| Account | Value | Age | Stuck | Flagged since | Days | Moved since? |
|---|---|---|---|---|---|---|
| **Upcurve consumer Technologies Pvt Ltd** | 1-2L | 90-180 d | 7 runs | 2026-07-02 | 11 | **NO** |
| **Dhanraj Realbuild Llp** | 5-7L | 60-90 d | 7 runs | 2026-07-07 | 6 | **NO** |
| **Times Group** | 7-10L | >180 d | 7 runs | 2026-07-13 | 0 | **NO** |
| **Supreme Vision Infrabuild Private Limited (Augusta Realty)** | 1-2L | <14 d | 1 runs | 2026-07-13 | 0 | **NO** |
| **Kunwarji Realtors** | >=10L | 60-90 d | 1 runs | 2026-07-13 | 0 | **NO** |

## 4. Owner scorecard

| Owner | Deals | Progressed | Stuck | SUPER-RED | No next task | Note theatre | >60d old |
|---|---|---|---|---|---|---|---|
| Muntazar Mhate | 14 | 4 | 10 | **10** | 10 | 0 | 1 |
| Raahul Ramanan R | 5 | 0 | 5 | **5** | 2 | 0 | 5 |
| Venkat Viswavardhan | 13 | 5 | 8 | **2** | 3 | 0 | 6 |
| Sahil Jane | 11 | 9 | 2 | **2** | 3 | 0 | 0 |
| Sanket Nampalliwar | 2 | 0 | 2 | **1** | 0 | 0 | 2 |
| Sourabh Sahu | 2 | 0 | 2 | **1** | 2 | 0 | 2 |
| Shweta Gouda | 9 | 3 | 4 | **0** | 6 | 0 | 0 |
| Shubham Dubey | 1 | 0 | 1 | **0** | 1 | 0 | 0 |
| Ganesh Vamsee | 1 | 0 | 1 | **0** | 1 | 0 | 0 |

## 5. Note theatre (same note re-pasted, zero delta)

_none_


## 6. What the pipeline is actually stuck on

**Trainings** 23 - **Meta/Facebook** 11 - **WhatsApp** 10 - **Bulk lead import** 8 - **IVR/Mcube/dialer** 7 - **Website** 6 - **Inventory** 6 - **Handover** 4 - **Portals** 3


## 7. CRM hygiene

- **28 of 58 deals have no next task.**
- **23 have no billed amount** (cannot rank by revenue at risk).
- 10 overdue tasks, 9 breached go-live dates, 1 deals with zero notes.
- **16 deals older than 60 days** still not live.

## SUPER-RED list

| Account | Owner | Runs stuck | Value | Age | Why |
|---|---|---|---|---|---|
| Ribitto Private Limited | Muntazar Mhate | 7 | blank | 30-60 d | Stage flipped out of Pending-on-Customer but the 12-Jul note is a verbatim resta |
| Calicut Landmark Builders Pvt. Ltd | Raahul Ramanan R | 7 | 5-7L | 60-90 d | No note since 8-Jul; Q&A / mobile / admin 2.0 trainings still not done. |
| SPR Construction Pvt Ltd | Raahul Ramanan R | 7 | blank | 60-90 d | No note since 8-Jul; still blocked on calling integration + booking-form doc. |
| Kohinoor AI Calling | Venkat Viswavardhan | 7 | blank | 60-90 d | Outgoing-calling issues persist; JIRA ESTATE-21040 still open, no customer testi |
| Dhanraj Realbuild Llp | Venkat Viswavardhan | 7 | 5-7L | 60-90 d | Customer still unhappy vs sales promises; call on pending pointers still not hel |
| Upcurve consumer Technologies Pvt Ltd | Raahul Ramanan R | 7 | 1-2L | 90-180 d | Refund legal-notice case (Amit Tare); no onboarding movement - should leave the  |
| Voora Developers | Raahul Ramanan R | 7 | 7-10L | >180 d | No new note/stage change since 2026-07-07. |
| Times Group | Sanket Nampalliwar | 7 | 7-10L | >180 d | Client-reported data discrepancies unresolved; review meeting rescheduled again. |
| Shrimant Developers | Muntazar Mhate | 5 | 1-2L | 30-60 d | Website integration still the open gap - 5th consecutive run. |
| NPS DEVELOPERS | Raahul Ramanan R | 3 | 3-5L | 60-90 d | No note since 8-Jul; AI-calling demo, Mcube concern, admin plan and WhatsApp all |
| Shree Automotive | Sourabh Sahu | 3 | 1-2L | >180 d | No new note/stage change since 2026-07-07. |
| Salahrealty Pvt Ltd | Muntazar Mhate | 2 | blank | <14 d | No note since 10-Jul; still waiting on inventory details from client. |
| Growthx Estates | Muntazar Mhate | 2 | 1-2L | <14 d | Same completed set; bulk lead import / portal / Meta / WhatsApp still pending on |
| Sunrise Housing (GHP Group) | Muntazar Mhate | 2 | 2-3L | 14-30 d | Same pending list (bulk lead import, Meta, website, WhatsApp) as last run. |
| Blueroof India | Muntazar Mhate | 2 | blank | 14-30 d | No note since 10-Jul; inventory/leads data and trainings still not done. |
| Leonaara PVt LTD | Sahil Jane | 2 | blank | 14-30 d | Interakt WhatsApp + Airtel/Mcube IVR still pending from our end - same blocker. |
| Axon Developer | Sahil Jane | 2 | 3-5L | 14-30 d | Still waiting on client's Mcube setup; CAPI/admin unchanged. |
| Red Estate Destination Pvt Ltd | Muntazar Mhate | 2 | 1-2L | 14-30 d | Client's Meta business verification still not through - same blocker for 2 runs. |
| Sohum Estate Agency (Sameer Chheda) | Muntazar Mhate | 2 | blank | 30-60 d | No note since 10-Jul; inventory demo (Monday) still the same open ask, nothing c |
| Real Estate Square | Muntazar Mhate | 2 | blank | 30-60 d | Bulk lead import still the only pending item, unchanged. |
| Sangram Group | Muntazar Mhate | 2 | blank | 30-60 d | No note since 10-Jul; 'no movement from client side' - same as last run, sales e |

---

## The asks

_[agent: 5 asks max, each with a named owner and a date]_

## Paste-ready version for the group

> _[agent: 3 concerns max, lead with the reality-check finding, name people only where the data is unambiguous]_
