# Onboarding Pipeline - Deep Dive & Major Concerns
**2026-07-20 - Kylas pipeline 27474 - 62 live deals (3 test deals excluded)**

## The headline

**29 of 62 deals (47%) did not genuinely move this run. 25 have not moved for two or more consecutive reviews (was 29 last run).**

| Run | Open | Progressed | Stuck | SUPER-RED |
|---|---|---|---|---|
| 2026-07-07 | 58 | 29 | 27 | 15 |
| 2026-07-10 | 61 | 20 | 33 | 16 |
| 2026-07-13 | 58 | 21 | 35 | 21 |
| 2026-07-16 | 60 | 4 | 43 | 29 |
| 2026-07-20 | 62 | 25 | 29 | 25 |

## 1. Reality check - what we tell customers vs what the ticket says

| Deal | Note says | Ticket | Live status | Verdict |
|---|---|---|---|---|
| **Kohinoor AI Calling** (stuck 9) | Schedule call to discuss customer pointers (dependent on Sharayu/custo | ESTATE-21040 | **Won't Fix** | GHOST DEPENDENCY |
| **Kohinoor AI Calling** (stuck 9) | Schedule call to discuss customer pointers (dependent on Sharayu/custo | SS-12176 | **Done** | GHOST DEPENDENCY |
| **Times Group** (stuck 9) | Data uploaded but client reports discrepancies; internal validation me | ESTATE-18697 | **Done** | GHOST DEPENDENCY |
| **Mythri Builder AI Calling** (stuck 3) | Connect with new POC for BOT feedback and push adoption. | SS-12285 | **Tech Discussion** | STUCK IN OUR QUEUE |

## 2. Who is really blocking

**UNCLEAR** 29 - **CUSTOMER** 16 - **OWNER-INACTION** 8 - **VENDOR** 4 - **US-TECH** 3 - **US-COMMERCIAL** 2

**Parked in 'Pending on Customer' but the customer is not the blocker (3):** Navkar Realty (OWNER-INACTION), Ribitto Private Limited (US-TECH), Times Group (US-COMMERCIAL)

## 3. Escalation & commercial risk

| Account | Value | Age | Stuck | Flagged since | Days | Moved since? |
|---|---|---|---|---|---|---|
| **Veedhan Buildtech** | blank | 30-60 d | 0 runs | 2026-06-18 | 32 | **yes** |
| **Aryma Infra (OPC)Pvt Ltd** | 1-2L | 14-30 d | 0 runs | 2026-07-02 | 18 | **yes** |
| **Dhanraj Realbuild Llp** | 5-7L | 60-90 d | 9 runs | 2026-07-07 | 13 | **NO** |
| **VASTU INFINITY AND VENTURES LLP** | blank | 14-30 d | 0 runs | 2026-07-10 | 10 | **yes** |
| **Times Group** | 7-10L | >180 d | 9 runs | 2026-07-13 | 7 | **NO** |
| **Kunwarji Realtors** | >=10L | 60-90 d | 3 runs | 2026-07-13 | 7 | **NO** |
| **Sangram Group** | blank | 30-60 d | 4 runs | 2026-07-16 | 4 | **NO** |
| **Shri Krish Housing and Properties Pvt Ltd** | 5-7L | 30-60 d | 2 runs | 2026-07-16 | 4 | **NO** |
| **NPS DEVELOPERS** | 3-5L | 60-90 d | 5 runs | 2026-07-20 | 0 | **NO** |
| **Leonaara PVt LTD** | 1-2L | 30-60 d | 4 runs | 2026-07-20 | 0 | **NO** |
| **SHREYA CAPITAL ADVISORY SERVICES LLP** | 3-5L | <14 d | 0 runs | 2026-07-20 | 0 | **yes** |
| **Apex Realty Hub** | blank | <14 d | 0 runs | 2026-07-20 | 0 | **yes** |

## 4. Owner scorecard

| Owner | Deals | Progressed | Stuck | SUPER-RED | No next task | Note theatre | >60d old |
|---|---|---|---|---|---|---|---|
| Venkat Viswavardhan | 12 | 0 | 11 | **9** | 0 | 0 | 5 |
| Muntazar Mhate | 12 | 7 | 5 | **5** | 10 | 0 | 0 |
| Raahul Ramanan R | 9 | 4 | 4 | **3** | 6 | 0 | 5 |
| Sourabh Sahu | 3 | 0 | 3 | **3** | 3 | 0 | 2 |
| Sahil Jane | 15 | 8 | 2 | **2** | 3 | 0 | 0 |
| Sanket Nampalliwar | 2 | 0 | 2 | **2** | 0 | 0 | 2 |
| Shweta Gouda | 9 | 6 | 2 | **1** | 2 | 0 | 0 |

## 5. Note theatre (same note re-pasted, zero delta)

_none_


## 6. What the pipeline is actually stuck on

**Trainings** 25 - **Bulk lead import** 16 - **Meta/Facebook** 15 - **IVR/Mcube/dialer** 11 - **Inventory** 11 - **WhatsApp** 11 - **Portals** 8 - **Handover** 8 - **Website** 5


## 7. CRM hygiene

- **24 of 62 deals have no next task.**
- **28 have no billed amount** (cannot rank by revenue at risk).
- 7 overdue tasks, 10 breached go-live dates, 3 deals with zero notes.
- **14 deals older than 60 days** still not live.

## SUPER-RED list

| Account | Owner | Runs stuck | Value | Age | Why |
|---|---|---|---|---|---|
| Ribitto Private Limited | Muntazar Mhate | 9 | blank | 30-60 d | Moved into Pending; transactional email still broken, sales training still defer |
| SPR Construction Pvt Ltd | Raahul Ramanan R | 9 | blank | 60-90 d | Calling-integration blocker persists; now escalated to Ketan - escalation is not |
| Kohinoor AI Calling | Venkat Viswavardhan | 9 | blank | 60-90 d | AI-calling still blocked (ESTATE-21040 / SS-12176); only a call being scheduled. |
| Dhanraj Realbuild Llp | Venkat Viswavardhan | 9 | 5-7L | 60-90 d | Refund/churn risk deepening; customer refuses AI-calling, wants unavailable sour |
| Voora Developers | Raahul Ramanan R | 9 | 7-10L | >180 d | Same blockers: balance payment + Manoj's pointers, still awaited. |
| Times Group | Sanket Nampalliwar | 9 | 7-10L | >180 d | No note after 2026-07-16 (last run) and no stage change - nothing happened since |
| NPS DEVELOPERS | Raahul Ramanan R | 5 | 3-5L | 60-90 d | Owner states nothing moved this week; escalated to sales. |
| Shree Automotive | Sourabh Sahu | 5 | 1-2L | >180 d | No note after 2026-07-16 (last run) and no stage change - nothing happened since |
| Leonaara PVt LTD | Sahil Jane | 4 | 1-2L | 30-60 d | WhatsApp Interakt still pending on dev; trainings only scheduled, not done. |
| Sohum Estate Agency (Sameer Chheda) | Muntazar Mhate | 4 | blank | 30-60 d | Moved into Pending; inventory-layout demo slipped (client unavailable). |
| Sangram Group | Muntazar Mhate | 4 | blank | 30-60 d | Moved into Pending; on-hold email sent; sales training only assured for Monday. |
| Navkar Realty | Venkat Viswavardhan | 3 | 3-5L | 30-60 d | No progress - customer POC on sick leave; all items pushed to next week. |
| VENDSPACEZ PRIVATE LIMITED | Venkat Viswavardhan | 3 | 3-5L | 30-60 d | Admin training still only being scheduled a week later - scheduled != done. |
| Strata Capital Holdings | Shweta Gouda | 3 | blank | 30-60 d | Mcube still blocked (recordings not captured); raised to vendor, client waiting. |
| VAZHRAA NIRMAAN PRIVATE LIMITED | Venkat Viswavardhan | 3 | 2-3L | 30-60 d | Admin training restated as awaiting customer availability - same ask. |
| GGC AI Calling | Venkat Viswavardhan | 3 | blank | 60-90 d | Still only arranging a call; AI-calling adoption not started. |
| Mythri Builder AI Calling | Venkat Viswavardhan | 3 | blank | 60-90 d | Still awaiting BOT feedback/adoption; now via a new POC (SS-12285). |
| Kunwarji Realtors | Sanket Nampalliwar | 3 | >=10L | 60-90 d | No note after 2026-07-16 (last run) and no stage change - nothing happened since |
| Shree Honda | Sourabh Sahu | 3 | 2-3L | >180 d | No note after 2026-07-16 (last run) and no stage change - nothing happened since |
| Propnsafe Realty LLP | Sahil Jane | 2 | 1-2L | <14 d | Still in Kickoff Done; core setup gated on website + lead import; fancy number i |
| Rajparis Civil Construction | Muntazar Mhate | 2 | 3-5L | 14-30 d | Moved into Pending; AiSensy + inventory + cost sheet all awaited from client. |
| SWARAJYA REALTORS PRIVATE LIMITED | Venkat Viswavardhan | 2 | 2-3L | 14-30 d | Owner notes little concrete movement; trainings pending client availability. |
| i5 Housing and Properties LLP | Sourabh Sahu | 2 | 3-5L | 30-60 d | No note after 2026-07-16 (last run) and no stage change - nothing happened since |
| Shri Krish Housing and Properties Pvt Ltd | Muntazar Mhate | 2 | 5-7L | 30-60 d | Account already live last week; only Facebook added; moved into Pending with hol |
| GRUHAM SPACES LLP | Venkat Viswavardhan | 2 | 3-5L | 90-180 d | Still awaiting Sourcing rework from dev (ETA 29 Jul); customer un-progressed. |

---

## The asks

1. **Venkat — kill the ghost tickets on the AI-calling book by Wed 22-Jul.** Kohinoor is parked on **ESTATE-21040, which is Won't Fix**, and its bot ticket (ESTATE-20563) is already Done — the customer is waiting for a feature we have declined. Tell Kohinoor the truth, re-scope, and stop citing dead tickets in the note. Same discipline across GGC and Mythri.
2. **Sharayu — give Mythri's bot (ESTATE-20699) a go/no-go by Thu 23-Jul.** It has sat in **Tech Discussion, untouched since 26-Jun**, while the note tells the customer we're "awaiting their feedback". It is our queue, not theirs.
3. **Sanket — close or escalate Times Group by Wed 22-Jul.** 7–10L, >180 days open, parked on **ESTATE-18697 which has been Done since 13-Feb**; the only live issue is the data-discrepancy review. Get the validation call done or escalate it commercially — it cannot sit another review.
4. **Venkat + Siddharth — make the Dhanraj refund/save call by Wed 22-Jul.** 5–7L, now an active churn/refund risk (customer refuses AI-calling, wants sourcing changes we can't deliver). This needs a commercial decision, not another follow-up.
5. **Sourabh & Sanket — work or formally park the four dead accounts by Thu 23-Jul.** Shree Honda, Shree Automotive, i5 Housing (Sourabh) and Kunwarji Realtors (Sanket, ≥10L) have had **no note since 7–11 Jul and no stage change**. Either log a real next step or move them to On-Hold so they stop inflating the live pipeline.

## Paste-ready version for the group

> **Onboarding review — Mon 20 Jul.** 25 of 62 deals progressed this run (a real rebound from 4 last Thursday); 29 are still stuck and 25 have not moved in two-plus reviews (down from 29).
>
> **1. We're parking customers against tickets that are already dead.** Kohinoor is waiting on ESTATE-21040 — marked **Won't Fix**; Times Group is parked on ESTATE-18697 — **Done since February**; and Mythri's bot has been in **Tech Discussion, untouched since 26 June** while the note says we're "awaiting customer feedback". Owners: please re-read the live ticket before you write "pending on tech".
>
> **2. The AI-calling book is the concentration risk.** Kohinoor, Mythri, GGC and Dhanraj are all stuck on the same AI-calling gap. **Dhanraj (5–7L) is now a refund risk** — Venkat + Siddharth to make the save/refund call this week.
>
> **3. Trainings are the single biggest blocker (25 deals), and hygiene is masking it** — 24 deals have no next task and 28 have no billed amount, so we can't rank by revenue at risk. If you own a stuck deal, the ask this week is a completed training or a logged next step, not a re-posted plan.

---

## For Ketan — before you post (not for the group)

- **Venkat: 0 of 12 progressed, 9 SUPER-RED.** On paper that's the worst book in the room — but it is skewed: he holds all four AI-calling accounts (genuinely blocked on the feature/vendor) and five of his deals are 60-days-plus. The honest read is a bad *allocation*, not simply a bad owner. Worth a private word on rebalancing before it lands as public criticism.
- **Sourabh (3 deals, 0 progressed, all 3 SUPER-RED)** and **Sanket (2 deals, both SUPER-RED, both ≥7L)** are small books that are entirely stuck — quiet, not loud. Silence, not ugly notes.
- **Coverage integrity:** Shweta leaves ~66% of checklist fields blank; Venkat/Muntazar/Sourabh disclaim ~46% as "Not required". Different tactics, same effect — a checklist with nothing red on it. Sheets 13–14 have the detail if you want to press on it.
