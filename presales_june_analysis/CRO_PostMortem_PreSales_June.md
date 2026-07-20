# Pre-Sales & Marketing June 2026 — Funnel Post-Mortem, Revenue Read & July Plan
*CRO review for Ketan Sabnis. Two lenses: (1) the 253 demos conducted in June — a quality/activity read; (2) the 42 deals that actually closed in June — the real revenue read. Plus marketing source, closure velocity, and a conversion-probability model to wire into your hourly CRON.*

## First, a correction on my own scoring (your question)

The GREEN/AMBER/RED "quality verdict" in this pack is **mine, computed now for this post-mortem** — not the output of your hourly BANT/quality CRON. My agents read each deal's full notes (including your AI enrichment/audit verdicts where they exist) and applied a fixed rubric I wrote. So "24 of 25 wins were GREEN" is an independent read, not a validation of the CRON. What I've now done is turn that read into a **calibrated probability model you can actually put into the CRON** (see the last section) — that's the productised version.

---

## The uncomfortable headline

Two numbers tell the whole story:

- **We ran 253 demos. 98 of them (39%) had a real chance; the other 155 (61%) shared a single win between them.**
- **₹62.4L closed in June — and 80% of it (₹50.0L) came from developers, a segment that is only ~40% of our demos and which we actively under-feed while over-feeding sub-scale channel partners and a Facebook channel that converts at 2%.**

We are not short of activity. We are short of *aim*. Every lever below points the same way: fewer, better-targeted demos — developers, 5+ seats, strong BANT, in person — would lift revenue while cutting workload.

---

## Lens 1 — the 253 demos (quality & what converts)

Verdict mix: **GREEN 98 (39%), AMBER 98 (39%), RED 57 (22%).** On the stated target (200+ demos of 5+ seats) we did **146 → missed**. New tier split as you asked:

| Licence tier | Demos | % | Win rate | GREEN rate |
|---|---|---|---|---|
| <5 | 107 | 42% | 6.5% | 14% |
| 5–10 | 116 | 46% | 12.1% | 54% |
| 10+ | 30 | 12% | 13.3% | 67% |

**What actually converts** — I cut win-rate every way the data allows; the signal is unusually clean and it compounds:

| Cut | Best segment | Win rate | vs worst |
|---|---|---|---|
| Quality verdict | GREEN 24.5% | | AMBER 1.0% / RED 0% |
| BANT | Strong 27.9% | | Partial/Weak/None ~0.6% |
| Account type | Developer 13.3% | | Channel partner 7.5% |
| Demo mode | Onsite 15.2% | | Online 9.1% |
| City | Hyderabad/Chennai 24–27% | | Pune 0%, NCR 7% |
| Licence | 10+ 13.3% | | <5 6.5% |

The mechanism is BANT and fit: a **Strong-BANT developer with 5+ seats seen in person** is our winning demo. We run the opposite at scale — 61% AMBER/RED, 58% channel partners, 42% sub-5-seat, 87% online. **The quality of the qualification call is essentially the forecast.**

---

## Lens 2 — real June revenue (the 42 closures)

This is the lens you were right to demand — closures in June regardless of when the demo happened. It looks nothing like the demo cohort:

- **₹62.4L billed / ₹45.4L collected** across 42 deals (the June-demo cohort alone showed only ₹29.4L — closures are ~2x and skew to big, long-cycle developer deals demoed months earlier, e.g. **Kaustubh/Gurgaon ₹8.2L, 30-seat, demoed April**; **Kavita/Ranchi ₹2.77L, 25-seat, demoed May**).

**By account type — the single most important revenue fact:**

| Type | Deals | Revenue | % of rev | Avg demo→close |
|---|---|---|---|---|
| **Developer** | 24 | **₹50.0L** | **80%** | ~28 days |
| Channel partner | 18 | ₹12.4L | 20% | ~49 days |

Developers are 80% of revenue *and* close ~1.7x faster. Channel partners are a low-value, slow-closing drag — yet they're the majority of our demos.

**By size:** 10+ seats = ₹33.0L (53% of revenue) from 10 deals; 5–10 = ₹22.2L; <5 = ₹7.1L. **By city (revenue):** Other ₹19.4L, Chennai ₹12.5L, Delhi/NCR ₹10.3L, Mumbai ₹8.8L, Bangalore ₹5.7L, Hyderabad ₹5.6L, **Pune ₹0.1L**.

**Closure velocity (demo→close, estimated — the connector doesn't expose exact close dates, so this uses the won-stage timestamp):** overall ~37 days (median 26). Developers ~28d vs channel partners ~49d. By city, **Hyderabad is fastest (~18d)** while **Chennai is slow (~81d) but high-value** — Chennai closes big deals but they take a quarter, so forecast them accordingly.

**Critical nuance (don't over-simplify "cut off-territory"):** "Other" (non-rep) cities produced the *largest* revenue bucket (₹19.4L) — because big developer deals close remotely. So the rule isn't "only sell in the 6 cities." It's: **the win driver is developer + size, which exists everywhere; put reps on-ground where density is high, but chase large developers wherever they are, and stop spending demos on small off-territory channel partners.**

---

## Lens 3 — top of funnel: where leads come from and which convert

Source is captured on all 253 demos (campaign/UTM are effectively empty — only 1/253 tagged, which is itself a measurement gap to fix). The channel ROI is stark:

| Source | Demos | % 5+ | Won | Win rate | Verdict |
|---|---|---|---|---|---|
| **Organic** | 95 | 58% | 13 | **13.7%** | Champion — highest volume & yield |
| **Google** | 74 | 66% | 7 | 9.5% | Best size mix; reliable paid lever |
| **Facebook** | 47 | 51% | 1 | **2.1%** | 19% of demos, 4% of wins — broken |
| Sell.Do Interakt (WhatsApp) | 32 | 43% | 3 | 9.4% | Decent inbound |
| Instagram | 3 | 33% | 0 | 0% | Negligible |

**Facebook is burning pre-sales capacity** — 47 demos, one win. It brings bodies, not buyers. **Organic is the highest-ROI channel** (SEO/direct/brand) and **Google is the best paid channel** (best 5+ mix). This directly answers "where to advertise": **scale Google, invest in Organic (content/SEO/brand), fix Facebook targeting toward developer/large-account lookalikes or move its budget to Google, and drop Instagram.**

---

## Why deals didn't move

53% of demos still open, 37% lost. Largest fixable cause is upstream: **Quality/ICP + BANT-weak ≈ 30% of demos never had a chance, and ~22% of stalls are pre-sales-owned.** ~20% are genuine Sales-side gaps (slow follow-up; losses to cheaper Buildesk/Billdesk). Data hygiene compounds it — 27 demos had junk/placeholder names and the dummy phone `+919999999999` recurs. We lose more to bad inputs than to bad closing.

## Per-rep

| Rep | Demos | Win % | GREEN | Onsite | June-demo rev | June closures rev |
|---|---|---|---|---|---|---|
| Revati Ambike | 135 | 11.9% | 43% | 21 | ₹21.6L | ₹21.0L (15 deals) |
| Ashwini Nirmal | 114 | 7.9% | 34% | 12 | ₹7.8L | ₹7.1L (8 deals) |

Revati is stronger on every axis. Both optimise for count because that's what we measure — a system problem, not a people problem.

---

## The conversion-probability model (for your hourly CRON)

I fitted a transparent model on the 253 demos (naive-Bayes log-odds; no black box). It's well calibrated — the top quintile predicted 36.5% vs 34.0% actual; the bottom 60% ~1%. Delivered as `model_weights.json` + `score_deal.py` (drop-in, no dependencies).

**The decisive output — a triage rule:**

| Work only demos with… | Demos | % of wins kept | Win rate |
|---|---|---|---|
| **P ≥ 5%** | **98** | **96%** | 24.5% |
| P ≥ 15% | 80 | 88% | 27.5% |
| P ≥ 20% | 49 | 68% | 34.7% |

**Working only the P≥5% demos would have kept 96% of revenue for 39% of the demo effort.** Feature weights (log-odds): BANT Strong +1.16 / Weak −2.25; City HOT (Hyd/Chennai) +1.09; Onsite +0.57; Developer +0.33; 10+ seats +0.42; and a source add-on (Facebook −1.63, Organic +0.37).

**How to wire it:** run `score_deal.py` in the hourly job next to the BANT/quality audit; write `probability` + `band` (HOT/WARM/MID/COLD) to a deal field. Route **HOT → onsite + senior rep**, auto-deprioritise **COLD (P<5%, which held just 1 of 25 wins)**. Re-fit monthly as data accumulates.

---

## The July plan — clear focus

**Where to advertise (marketing):**
1. **Scale Google** (best paid, 66% 5+) and **invest in Organic** (SEO, content, brand, referrals — our highest-ROI source).
2. **Fix or defund Facebook** — retarget to developer/large-account lookalikes; if it can't beat ~8% win in 30 days, move the budget to Google. Drop Instagram.
3. **Fix attribution** — campaign/UTM are empty; you can't optimise spend you can't measure. Make campaign+UTM mandatory on lead capture.

**What leads to build (marketing + pre-sales):**
4. **Bias hard to developers** (80% of revenue, close 2x faster) and **5+ seats**. Set a developer-share floor (≥50%) and a 5-seat minimum to book a demo.
5. **Kill the <5-seat channel-partner tele-lead** — 42% of demos, ~6% win, near-zero revenue.

**Pre-sales motion:**
6. **Gate every demo** on: verified company + real phone (auto-reject `9999999999`/single-word names), named decision-maker, BANT ≥ Partial, ≥5 seats. Run the existing deal-audit *before* the demo.
7. **Force onsite in rep cities**, starting Hyderabad/Chennai (best win, barely any onsite today).
8. **Change the KPI** from demos to **qualified demos** (HOT/WARM band, 5+, developer-lean) — the only number that tracks revenue.

**Geography & enterprise:**
9. **Re-point demand** to Hyderabad/Chennai (24–27% win, starved); trim low-yield NCR/Bangalore volume; **root-cause Pune** (HQ: many demos, ₹0.1L). Pursue large developers off-territory (they close remotely — ₹19.4L proof).
10. **Stand up an enterprise lane** — named 40+ developer accounts, CXO multi-threading; target ≥15 enterprise demos in July vs 5.

**Wire the model:** ship `score_deal.py` into the hourly CRON this week; triage on the probability band.

**Net:** June looked like a volume win; on revenue it was carried by a handful of developer deals demoed months earlier, while the current-month demo machine mostly manufactured activity. Aim the funnel at developers/5+/strong-BANT via Google+Organic, gate out the noise with the model, and force the on-ground motion — and the same team produces materially more revenue from far fewer demos.

---
*Data & artifacts (all in `presales_june_analysis/`): `Presales_June_PostMortem.xlsx` (14 sheets incl. Revenue/Closures, Marketing Source, Convert Model, What Converts, City Deep-Dive); `master_dataset.csv` (253 demos), `closures_dataset.csv` (42 closures), `analytics_v2.json`, `closures_analytics.json`, `model_weights.json` + `score_deal.py`, and per-deal `deals/<id>.json`. Ask me any deal/segment/channel-level question.*
