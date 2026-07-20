---
name: presales-marketing-weekly
description: >-
  Weekly Marketing & Pre-Sales funnel review for Sell.Do (Kylas CRM). Use when asked to
  "run the marketing weekly", "weekly pre-sales review", "marketing analysis for last week",
  "how did demand-gen do last week", or on the Monday schedule. Analyses demos conducted in
  the prior week (Mon-Sun) created by the Pre-sales team: source & UTM-campaign performance,
  demo quality (GREEN/AMBER/RED, 5+ seats, developer vs channel partner), conversion-probability
  bands (HOT/WARM/MID/COLD), city / off-territory split, allocation by sales person vs targets,
  lead-routing check, data-hygiene alerts, zero-follow-up alerts and competitor-loss watch.
  Produces a dated multi-sheet Excel plus a short written readout, and compares week-over-week.
metadata:
  type: workflow
  domain: kylas-crm / sell.do marketing + pre-sales
---

# Sell.Do — Weekly Marketing & Pre-Sales Review

## Purpose

Answer one question every Monday: **did we generate the right demand last week, and where do we spend/fix next?**
Judge quality and mix — not just volume. Volume without quality is the failure mode this review exists to catch.

---

## ⚙️ TARGETS — EDIT THESE (single source of truth)

```
WEEKLY_DEMO_TARGET_5PLUS   = 50     # qualified demos of 5+ licences per week (from the 200+/month goal)
WEEKLY_GREEN_TARGET        = 25     # of those, genuinely well-qualified (GREEN)
DEVELOPER_SHARE_FLOOR      = 0.50   # >= 50% of demos should be Developers (they are ~80% of revenue)
ONSITE_SHARE_TARGET_MAIN6  = 0.40   # >= 40% of Main-6 city demos should be in person
SALES_REP_ALLOCATION       = "even" # or a dict of {rep: weekly demo target}, e.g. {"Alok Tiwari": 8, ...}
```
If the user has given real targets, use those and say so. Otherwise use these and state that they are defaults.

---

## Phase 0 — Session setup (mandatory)

1. `get_entity_labels()` first.
2. `get_deal_field_instructions()` once.
3. Determine **last week** = previous Monday 00:00 to Sunday 23:59 **IST**. State the exact window in the output.

## Phase 1 — Who is Pre-Sales (verify, don't assume)

The Pre-sales team is the CRM team used by report **361026** ("Deals Created By Pre-Sales (Creator)",
filter: Created-By Team = *Pre-sales team*, team id 839). Known members:

| Rep | user id |
|---|---|
| Revati Ambike | 9062 |
| Ashwini Nirmal | 54132 |
| Gayatri More | 82379 |

**The roster can change.** If counts look wrong, re-check the team in report 361026 and update the ids.
`get_deal` does NOT expose `createdBy` — always attribute the creator via the `createdBy` filter, never from the deal record.

## Phase 2 — Pull last week's demos (the universe)

Demos = deals whose **demo actually happened** last week, created by pre-sales:

```
search_entity("deal", filters=[
  {"field":"cfMeetingConductedOn","operator":"greater_or_equal","value":"<Mon>T00:00:00+05:30","type":"DATETIME_PICKER"},
  {"field":"cfMeetingConductedOn","operator":"less_or_equal","value":"<Sun>T23:59:59+05:30","type":"DATETIME_PICKER"},
  {"field":"createdBy","operator":"in","value":[9062,54132,82379]}
], size=100)   # page through all
```
Then `get_deal` + `get_deal_notes` for each (page notes; notes are first-class data).
Use a **subagent fan-out** if the count is large — but weekly volume is usually ~50-70, so serial is fine.

**Do not** use "created last week" — that is the wrong lens. Demos conducted is the activity that matters.

## Phase 3 — Source & campaign performance (the "where to spend" view)

**Source** (populated on every deal). Count demos, 5+ share and wins per source using filter-counts:
add `{"field":"source","operator":"equal","value":<id>}` to the Phase-2 filter.

| Source | id | June-2026 baseline |
|---|---|---|
| Organic | 14774 | best: 13.7% win |
| Google | 8832 | 9.5% win, best size mix |
| Facebook | 8833 | **2.1% win — the problem channel** |
| Sell.Do Interakt (WhatsApp) | 48853 | 9.4% win |
| Instagram | 190307 | ~0 |

**UTM campaign / Sub Source** — attribution DOES exist for paid (Organic correctly has none).
`get_deal` does not expose these, so count them with `utmCampaign` **equal** filters against the known list:

- `Sell.do Lead Gen Conversion Campaign - April 2024` (Meta/Facebook lead-gen)
- `Sell.do Lead Gen Conversion Campaign - June 2025` (Meta)
- `Selldo-search-jan24` (Google search)
- `Selldo-google-brand-search` (Google brand)
- `Selldo-search-south-jan2024`, `Selldo-google-brand-search-south`
- `Pmax-traffic`, `Pmax-traffic-retarget`, `Sell.do-pmax-traffic-competitor`
- `Sell.do-search-ai-calling-observation`, `Sell.do-youtube-traffic-retarget-newtool`

Also count `utmCampaign is_not_empty`. **If the named campaigns don't sum to that total, a NEW campaign has
appeared — surface it prominently and add it to this list.** Flag any broken UTM (e.g. literal `{{campaign.name}}`)
and stale campaign names (2024-dated campaigns still tagging current leads).

## Phase 3.5 — Created → demo funnel (the invisible leak)

Volume of demos hides how many leads never made it to a demo. Count:
- **Deals CREATED** last week by pre-sales (`createdAt` in window + `createdBy in [team]`).
- **Of those, how many have `cfMeetingConducted = true`** → **show-rate**.
- **LEAK = created − demoed.** (Week of 6–12 Jul: 51 created, 34 demoed = 67% show-rate, **17 leaked**.)
List the leaked deals (they are either bad leads or no-shows) and say which.
Also report demos conducted that were created in *earlier* weeks (older deals finally demoed).

## Phase 4 — Demo quality (per deal)

For each demo, from fields + notes:

- **licences** → tier `<5` / `5-10` / `10+`. Track the **5+ count vs WEEKLY_DEMO_TARGET_5PLUS**.
- **account type** — Developer vs Channel partner. Track **developer share vs DEVELOPER_SHARE_FLOOR**.
- **onsite vs online** (from notes: in-person/office visit = Onsite).
- **quality verdict**:
  - **GREEN** — real named decision-maker, real company + CRM need, 5+ seats, key facts captured.
  - **AMBER** — real but thin: partial BANT, small size, junior/unconfirmed contact, missing info.
  - **RED** — should not have been booked: junk/placeholder contact, no real need, sub-ICP (1-2 seat), demo-for-the-number.
- **BANT** grade: Strong / Partial / Weak / None.
- **seat_inflation** — compare the claimed `noOfLicenses` against what the notes/audit actually verify
  (e.g. "5 claimed / 2 real"). Flag every inflated deal: the 5+ target is being gamed by unverified seat counts.
- **enterprise (40+ seats)** — count them. **A week with zero 40+ demos is a red flag — say so loudly.**

## Phase 5 — Conversion probability (HOT/WARM/MID/COLD)

Start `S = -2.2`, add:

| Feature | Points |
|---|---|
| BANT | Strong **+1.2** · None −0.3 · Partial **−1.6** · Weak **−2.3** |
| City | Hyderabad/Chennai **+1.1** · other non-metro −0.2 · core metro (Mumbai/Delhi-NCR/Bangalore/Pune) −0.3 |
| Mode | Onsite **+0.6** · Online −0.1 |
| Type | Developer **+0.3** · Channel partner −0.3 |
| Licences | 10+ **+0.4** · 5–10 +0.2 · under 5 **−0.4** |
| Source | Organic +0.4 · Google/WhatsApp 0 · Facebook/Instagram **−1.6** |

Band: **HOT** S ≥ −1.4 (≥20%) · **WARM** ≥ −2.0 · **MID** ≥ −2.75 · **COLD** below.
(Exact: `p = 1/(1+e^-S)`. Same model as the deal-audit skill — keep them in sync.)
Output the **HOT list** with the next action for sales — that is the most-used part of this report.

## Phase 6 — Geography

Main-6 rep cities = Pune, Mumbai/Thane, Delhi/NCR, Bangalore, Chennai, Hyderabad. Everything else = **off-territory**.
- Hyderabad & Chennai convert best (24–27%) but are usually starved — call out if they got few demos.
- Pune (HQ) has historically converted ~0% — flag if it stays flat.
- **Off-territory developers are NOT junk**: they close remotely and were ~29% of 6-month revenue (East belt:
  Kolkata, Ranchi, Bhubaneswar, Siliguri; also Gujarat and tier-2 South). Surface any off-territory developer demos.
- Report `Onsite share of Main-6 demos` vs **ONSITE_SHARE_TARGET_MAIN6**.

## Phase 6.5 — Pre-sales rep quality scorecard (the coaching tool)

"Rep" here = **pre-sales rep** (Revati / Ashwini / Gayatri). For EACH, report side-by-side:
**demos · GREEN · RED · %GREEN · 5+ count · developer count · onsite · HOT/WARM · junk names · unverified contacts.**
This is the manager's coaching view — it shows *who* is generating the junk, not just that junk exists.
(Week of 6–12 Jul: Revati 27 demos / 6 GREEN / 11 RED; Ashwini 16 / 1 GREEN / 5 RED and 8 unverified contacts.)

## Phase 7 — Allocation by sales person vs targets, and routing

1. **Allocation** — count last week's demos by **sales owner** (the deal's owner). Compare to `SALES_REP_ALLOCATION`
   (even split across active owners unless targets given). Flag anyone materially over/under-fed, and anyone with
   **zero** demos assigned.
2. **Pre-sales split** — demos by creator (Revati / Ashwini / Gayatri).
3. **Routing check (important)** — historical: **Revati converts Developers ~24%** (Ashwini 3.7%);
   **Ashwini converts Channel partners ~11.7%** (Revati 4.8%). So the rule is *developers → Revati,
   channel partners → Ashwini*. Report how many demos followed vs broke this rule.

## Phase 8 — Hygiene & risk alerts (short, specific, actionable)

- **Junk/placeholder contacts** — single-word or nonsense names, dummy phone `+919999999999`, sequential numbers.
- **Unverified contact** — audit/enrichment note says name_validation MISMATCH or resolves to a different person.
- **Missing data** — no city, no licences, no owner phone.
- **Zero follow-up alert** — demos from last week (and the week before) with **no sales-side note since the demo**.
  Historically 17% of lost deals got zero post-demo follow-up — catch it in-week.
- **Competitor-loss watch** — any deals lost last week to a rival (Leadrat, LeadSquared, Zoho, Buildesk, Billdesk,
  Kit19, 4QT, Privyr, TeleCRM). If one name spikes, say so.

## Phase 8.5 — Cohort follow-through (does last fortnight's work survive?)

Take the demos conducted in the **previous 2 weeks** (i.e. the fortnight BEFORE last week) and check their status now:
**still open / won / already lost-or-unqualified.** A high early-death rate means we are booking demos that die on contact.
(Cohort 22 Jun–5 Jul: 107 demos → **43 already dead (40%)**, 2 won, 62 open.) Flag if the death rate climbs.

## Phase 8.6 — Losses last week: why, and did sales actually chase?

Pull deals (5+ licences, pre-sales-created) that became **Closed Lost / Closed Unqualified** last week
(`forecastingType in [CLOSED_LOST, CLOSED_UNQUALIFIED]` + `updatedAt` in window). For each, read the notes and record:
- **loss_reason** — Non-responsive | Budget | Competitor/Existing-CRM | Timeline/Not-now | Not-interested |
  Sub-ICP/Too-small | Product-gap | Wrong/Unverified-contact | Other
- **competitor** we lost to (name it), and
- **sales_attempts** = distinct sales-side follow-ups after the demo (exclude pre-sales authors 9062/54132/82379 and the audit author).

Report: reason mix, **avg attempts**, **deals lost with ZERO follow-up** (name them — these are free losses), and any
**competitor appearing more than once**. Merge Competitor + Budget to see the true "we lost on price" number.
(Week of 6–12 Jul: 56 losses, avg 6.0 attempts, **8 lost with zero follow-up**, **Buildesk took 3 on price undercut**.)

## Phase 9 — Week-over-week

1. Save a dated snapshot: `marketing_weekly/<YYYY-MM-DD>_snapshot.json` (all metrics + per-deal rows).
2. Load the **previous 1–2 snapshots** and show deltas for: total demos, 5+ demos, GREEN%, developer share,
   onsite share, HOT count, demos by source, and win/loss counts.
3. Call out anything that moved >20% either way, and anything that has been drifting the wrong way 2+ weeks running.

## Phase 10 — Output

**A. Excel** → `marketing_weekly/Marketing_Weekly_<YYYY-MM-DD>.xlsx`, sheets:
1. `Scorecard` — metrics vs TARGETS (green/red), enterprise 40+ count, cohort-rot block, WoW deltas.
2. `Pre-Sales Rep Scorecard` — per rep: demos / GREEN / RED / %GREEN / 5+ / developer / onsite / HOT-WARM / junk names / unverified.
3. `Funnel & Campaigns` — created → demo → leak; paid campaigns (Meta vs Google Brand/Search vs PMax).
4. `Source` — demos / 5+ / GREEN / RED / developer / HOT-WARM per source.
5. `Losses` — reason mix, avg sales attempts, zero-follow-up losses, competitors (named), per-deal list.
6. `HOT list` — deals to chase this week with next action and follow-up count.
7. `Allocation & Routing` — demos per sales owner vs target; pre-sales routing adherence.
8. `All demos` — every demo, filterable.
9. `WoW` — this week vs last 1–2 weeks (from snapshots).

**B. Chat readout** (short, CRO tone — no fluff):
- One-line verdict on the week.
- Scorecard vs targets (5+ demos, GREEN, developer share, onsite).
- Best & worst channel, with the specific spend action.
- Allocation/routing problems, named.
- The HOT list (top 5) and the alerts that need action today.
- What moved vs last week.

**C. Ready-to-post team update (ALWAYS produce this — it is the point of the review)**

Write a **ready-to-paste Microsoft Teams message** to
`marketing_weekly/Teams_Update_<YYYY-MM-DD>.md`, addressed directly to the Marketing + Pre-Sales team
(they share one manager). Show it in chat too, in a single copy-paste block.

**Rules for this message — follow exactly:**
- **Addressed to the team**, written as the manager/CRO would say it. Start with `**Team —**`.
- **Keep it under ~350 words.** It must be readable on a phone.
- **Use bold + bullets only. NO tables** (they render badly in Teams). No headers deeper than bold lines.
- **Lead with the verdict**, not the data. One sentence.
- **Always include a "What went well" section** — name the people/deals that did good work. A review that is
  only criticism gets ignored. Be honest but not demoralising.
- **Every action must have a named owner and a deadline.** No "we should" — say "Revati — do X by Wednesday".
- **Name specific deals/campaigns/cities.** Vague = ignored.
- End with where the full detail lives (the Excel filename).
- Do not invent anything: every number must come from the analysis above.

**Template:**

```
**Team — Marketing & Pre-Sales, week of <dates>**

**Verdict:** <one sentence — the honest read on the week>

**Where we landed**
- Qualified demos (5+ seats): **X** vs target Y
- Well-qualified (GREEN): **X** vs target Y  ·  RED (shouldn't have been booked): **X**
- Developer share: **X%** (floor 50%)  ·  Onsite in our 6 rep cities: **X%** (target 40%)
- Created → demo: **X of Y** made it to a demo (**Z leaked**)
- Worth chasing now: **N** HOT/WARM

**What went well**
- <name the rep / deal / channel that did good work — be specific>

**What needs fixing this week**
- <problem, named — e.g. "Facebook: 11 demos → 0 worth chasing">
- <problem, named>

**Actions**
1. **<Owner>** — <specific action> — **by <day>**
2. **<Owner>** — <specific action> — **by <day>**
3. **<Owner>** — <specific action> — **by <day>**

**Chase these now (no follow-up logged since the demo)**
- #<id> <Name> (<seats> seats, <city>) → **<Owner>**
- #<id> <Name> (<seats> seats, <city>) → **<Owner>**

Full detail: `Marketing_Weekly_<date>.xlsx`
```

## Golden rules

- **Quality over volume.** A week of 70 demos where 40 are sub-5-seat channel partners is a bad week — say so plainly.
- **Never invent numbers.** Every figure comes from a Kylas query; if something can't be fetched, say so.
- **Be specific and name names** (reps, campaigns, cities, deals). Vague reviews get ignored.
- **Read-only.** This skill never modifies deals — it only reads and reports.
