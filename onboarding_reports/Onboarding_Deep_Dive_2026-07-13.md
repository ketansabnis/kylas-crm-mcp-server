# Onboarding Pipeline — Deep Dive & Major Concerns
**13-Jul-2026 · Run 8 · Kylas pipeline 27474 · 58 live deals (3 test deals excluded)**

---

## The headline

**35 of 58 deals (60%) did not genuinely move this run. 21 have now not moved for two or more consecutive reviews — up from 16 last run.** The pipeline is not draining: ~5 deals exit per run, 5–8 enter. We have been flat at ~60 open deals for three weeks.

| Run | Open | Progressed | Stuck | SUPER-RED |
|---|---|---|---|---|
| 29-Jun | 60 | 9 | 47 | 29 |
| 02-Jul | 67 | 34 | 25 | 21 |
| 07-Jul | 58 | 29 | 27 | 15 |
| 10-Jul | 61 | 20 | 33 | 16 |
| **13-Jul** | **58** | **21** | **35** | **21** |

But the real finding is not the stuck count. It is **why** they are stuck. Three of the loudest "waiting on customer / waiting on tech" excuses do not survive contact with the actual JIRA.

---

## 1. We are telling customers a fix is coming that is not coming

| Deal | What the OB note tells the customer | What the JIRA actually says |
|---|---|---|
| **Kohinoor AI Calling** (stuck 7 runs) | "JIRA raised for bulk-call list, timeline 11.2" | **ESTATE-21040 = Won't Fix.** Severity marked *Critical*. Closed. Customer is waiting for a build that will never ship. |
| **Kohinoor AI Calling** | "issues raised in outgoing calling" | **ESTATE-20563 = QA Clarification Required** since 1-Jul. Fix version 11.0 *already released on 8-Jul* — it shipped without this. |
| **Mythri Builder AI Calling** (60–90 d) | "Awaiting flow and feedback from customer" | **ESTATE-20699 = Tech Discussion**, untouched since 26-Jun, raised 21-May. It has not even cleared feasibility. We are blaming the customer for our own queue. |
| **Times Group** (>180 d, 7–10L, 50 licences, stuck 7 runs) | Still parked on "FM app / UAT discrepancies" | **ESTATE-18697 = Done**, released, last touched **13-Feb-2026**. The dependency cleared five months ago. Nothing is blocking this account except us. |

**Ask:** every OB note that cites a JIRA must carry the live status. If the JIRA is Won't Fix or Done, the deal must move or the customer must be told the truth this week.

## 2. The entire AI-calling book is stalled

GGC, Mythri and Kohinoor — **3 of 3 AI-calling deals** — are 60–90 days old, all sitting in *Pending on Customer*, none live. Every one of them is blocked on a tech/vendor loop (Mcube, bot flow, bulk-call list), not on the customer. This is a product-readiness problem being logged as an onboarding problem.

**Ask:** one decision on AI calling — is it sellable today or not? If not, stop pushing it into onboarding.

## 3. Commercial risk sitting untouched

| Account | Value | Age | Streak | Status |
|---|---|---|---|---|
| **Kunwarji Realtors** | ≥10L, 50+ licences | 60–90 d | stuck | Client escalated **to you and Siddharth on 3-Jul** about *our* rollout delays and asked for on-site presence. **No note since 7-Jul.** Nothing has happened since the escalation. |
| **Times Group** | 7–10L, 50 licences | >180 d | 7 runs | See above — blocked on nothing. |
| **Dhanraj Realbuild** | 5–7L | 60–90 d | 7 runs | "Customer not happy with what sales promised vs delivered… looks like a refund case." The call to address it **still has not been held** after 7 reviews. |
| **Voora Developers** | 7–10L | >180 d | 7 runs | EPR docs + external handover pending since February. |
| **Upcurve** | — | 90–180 d | 7 runs | Refund **legal notice** with Amit Tare. This is not an onboarding deal — it is inflating our pipeline. |

**Ask:** Kunwarji and Dhanraj need a call this week, owned by Sanket/Ankur, not by the OB rep. Upcurve and any other legal/refund case must be moved out of the onboarding pipeline.

## 4. Owner concentration — the load is not the problem, the follow-through is

| Owner | Deals | Progressed | Stuck | SUPER-RED | No next task |
|---|---|---|---|---|---|
| **Muntazar Mhate** | 14 | 4 | 10 | **10** | **10 of 14** |
| **Raahul Ramanan** | 5 | **0** | 5 | **5** | 2 |
| Venkat Viswavardhan | 13 | 5 | 8 | 2 | 3 |
| Shweta Gouda | 9 | 3 | 4 | 0 | 6 |
| **Sahil Jane** | 11 | **9** | 2 | 2 | 3 |

- **Raahul has zero deals progressed** — 5 of 5 stuck, streaks of 3 to 7 runs (Calicut, SPR, NPS, Upcurve, Voora). Nothing in his book has moved in a month.
- **Muntazar carries 10 of the 21 SUPER-REDs**, and 10 of his 14 deals have **no next task recorded in the CRM at all**. His notes are healthy-looking; his accounts are not moving.
- **Sahil Jane is the benchmark** — 9 of 11 progressed with a comparable book size. Whatever he is doing on cadence should be the standard.

## 5. "Note theatre" — five notes are verbatim re-posts

Verified by diffing the note bodies, one week apart. **All five are the same author (Muntazar's account, user 71240)** and all five are byte-identical over everything the CRM will show us:

| Deal | Note on 5-Jul | Note on 12-Jul | Verdict |
|---|---|---|---|
| **Growthx Estates** | #51864498 | #52324544 | Identical Completed/Pending block |
| **Sunrise Housing** | #51863275 | #52324171 | Identical Completed/Pending block |
| **Real Estate Square** | #51858004 | #52322293 | Identical Completed/Pending block |
| **Red Estate Destination** | #51858593 | #52322546 | Identical Completed/Pending block |
| **Ribitto** | #51857843 | #52321136 | Identical Completed/Pending block |

A week of work produced a re-paste. Any check based on "has a recent note" reads all five as active.

**Ribitto is the one that fooled the report.** Its stage was flipped out of *Pending on Customer* — which reads as progress — while the note was a verbatim re-post. The only substantive update (10-Jul) says *our* tech is still fixing Mailgun and the lead-capture form. It has been re-classified **stuck, 7 runs**, which is why the SUPER-RED count is **21, not 20**.

Separately, **Shrimant Developers** has now reported *"website integration pending"* for **five consecutive reviews**. The note text changes slightly each week; the blocker never does.

**Ask:** a note is only valid if it states **(a) what changed since the last note, (b) who owes what, (c) by when.** A restated task list is not a status update.

## 6. Four artefacts explain most of the pipeline

Blocker mentions across the latest note on every open deal:

- Trainings **23** · Meta/Facebook **11** · WhatsApp **10** · Bulk lead import **8** · Mcube/IVR **7** · Website **6** · Inventory **6**

Strip out trainings (which are downstream) and nearly every stall traces to **four things the customer was never asked for up front**: the **WhatsApp number**, **Meta admin access**, the **lead file**, and the **inventory file**.

**Ask:** these four become mandatory pre-kickoff gating items — collected at order-form stage. No kickoff call without them.

## 7. CRM hygiene is breaking the review itself

- **28 of 58 deals have no next task.** Half the pipeline has no scheduled next action.
- **23 of 58 have no billed amount** — we cannot rank by revenue at risk.
- **10 overdue tasks**, **9 breached target go-live dates**, 1 deal (Doff Estate Post Sales) with **zero notes** since creation.

## 8. Where "Pending on Customer" is really "pending on us"

13 deals sit in *Pending on Customer*. At least 5 are ours: **Kohinoor** (Won't-Fix JIRA), **Times** (dependency already Done), **Dhanraj** (commercial dispute), **Voora** (internal handover), **Leonaara** (Interakt cannot send outgoing messages — our vendor). The stage is being used as a parking lot.

---

## The five asks

1. **Kohinoor + Mythri:** tell them the truth about the JIRAs this week — and decide whether AI calling is sellable at all.
2. **Kunwarji + Dhanraj:** senior-led call within 48 hours. Both are escalated, both have been idle since the escalation.
3. **Raahul's book (5 deals, 0 movement) and Muntazar's 10 SUPER-REDs:** reviewed line-by-line with Sanket this week.
4. **Every deal gets a next task in Kylas by Wednesday.** No next task = no owner = no movement.
5. **Legal/refund cases (Upcurve, possibly Dhanraj) exit the onboarding pipeline.**
