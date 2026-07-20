# Patch: add Conversion-Probability scoring to the `deal-audit` skill

This adds a **conversion-probability score** (HOT / WARM / MID / COLD + ~%) to the
audit note the hourly scheduler already posts. It reuses the fields the audit
already establishes — no new tool calls. Model fitted on June 2026 (253 pre-sales
demos, 25 wins); top-quintile calibration 36.5% predicted vs 34.0% actual.

## How to install (you must do this — skills are edited in Settings → Capabilities)

1. Open **Settings → Capabilities → deal-audit** (edit the skill).
2. Paste **Section A** below into `SKILL.md` as a new phase, **between Phase 5
   (Score every pre-sales field) and Phase 6 (Build the audit note)** — call it
   **Phase 5.5**.
3. Paste **Section B** line into Phase 6, right **after the VERDICT line** (item 1),
   and into `reference/note-template.md`.
4. (Optional, programmatic path) If you'd rather the CRON compute the number in
   code and write it to a deal field, ship `score_deal.py` + `model_weights.json`
   (in this folder) with the scheduler and call `score_deal(deal)` — see Section C.

Re-fit monthly as data grows (Section D).

---

## Section A — new **Phase 5.5 — Conversion-probability score**

> ## Phase 5.5 — Conversion-probability score (predict, don't just describe)
>
> After scoring the fields, compute a **conversion-probability band** from the
> features you just audited. This is an empirical model (June-2026 pre-sales
> demos) — use the **audited** values, not the raw pre-sales claims (e.g. use the
> audited licence tier and the graded Authority/BANT, not the unverified note).
>
> **Step 1 — start at S = −2.2** (the base log-odds; base win-rate ≈ 10%).
>
> **Step 2 — add the points that apply:**
>
> | Feature | Value → points |
> |---|---|
> | **BANT** (your Phase-5 read) | Strong **+1.2** · None −0.3 · Partial **−1.6** · Weak **−2.3** |
> | **City** | Hyderabad or Chennai **+1.1** · other non-metro −0.2 · core metro (Mumbai/Delhi-NCR/Bangalore/Pune) −0.3 |
> | **Demo mode** | Onsite **+0.6** · Online −0.1 |
> | **Account type** | Developer **+0.3** · Channel partner / Broker −0.3 |
> | **Audited licences** | 10+ **+0.4** · 5–10 +0.2 · under 5 **−0.4** |
> | **Source** (if known) | Organic +0.4 · Google / WhatsApp 0 · Facebook / Instagram **−1.6** |
>
> **Step 3 — read the band off the total S** (no exponential needed):
>
> | Total S | Band | ≈ Probability |
> |---|---|---|
> | S ≥ −1.4 | **🔥 HOT** | ≥ 20% |
> | −2.0 ≤ S < −1.4 | **🟠 WARM** | 12–20% |
> | −2.75 ≤ S < −2.0 | **🟡 MID** | 6–12% |
> | S < −2.75 | **❄️ COLD** | < 6% |
>
> (Exact probability if you want it: `p = 1 / (1 + e^(−S))`.)
>
> **Worked examples**
> - Developer, 30 seats, Hyderabad, onsite, Strong BANT, Organic:
>   S = −2.2 +1.2 +1.1 +0.6 +0.3 +0.4 +0.4 = **+1.8 → 🔥 HOT (~86%)**.
> - Channel partner, 2 seats, Jaipur, online, Weak BANT, Facebook:
>   S = −2.2 −2.3 −0.2 −0.1 −0.3 −0.4 −1.6 = **−7.1 → ❄️ COLD (~0.1%)**.
>
> **Why it matters (state it in the note when useful):** on June data, demos in
> the **HOT/WARM** bands held **~92% of all wins**; **COLD** (bottom ~60% of
> demos) held **1 of 25 wins**. So the band is a triage signal: HOT → route to a
> **senior rep + push for an onsite**; COLD → deprioritise / don't burn a demo slot.

---

## Section B — add to the audit note (Phase 6) and the template

Insert as the **second line of the note, right after the VERDICT line**:

```
CONVERSION: <🔥 HOT | 🟠 WARM | 🟡 MID | ❄️ COLD> (~X%) — drivers: <e.g. Strong BANT, developer, 20 seats, Hyderabad>; drag: <e.g. online-only>
```

Example:
```
VERDICT: 🟢 High confidence — verified 20-seat Thane developer, decision maker confirmed.
CONVERSION: 🔥 HOT (~82%) — drivers: Strong BANT, developer, 20 seats, onsite; drag: none.
```

---

## Section C — programmatic path (optional)

If the scheduler computes it in code instead of by rubric, use the exact model:

```python
from score_deal import score_deal
score_deal({
  "licences": 20, "account_type": "Developer", "mode": "Onsite",
  "city": "Thane", "bant": "Strong", "source": "Organic",   # source optional
})
# -> {"probability": 0.8x, "band": "HOT"}
```

`score_deal.py` is dependency-free and reads `model_weights.json` (both in this
folder). Write `probability` + `band` to a deal custom field, then build views /
routing rules on it. The rubric in Section A and this code produce the same
numbers (the rubric is the code's weights rounded for mental math).

---

## Section D — keep it honest

- **Re-fit monthly.** Re-run `build_model.py` on the trailing month's demos; the
  weights are just empirical win-rates by feature, so they should track reality.
- **It's a prior, not a verdict.** A COLD deal a rep believes in can still be
  worked — the band decides *default* effort/routing, not a hard gate.
- **Watch data drift.** If Facebook targeting is fixed or a new source scales,
  its weight will change — that's expected; the monthly re-fit captures it.
- **Model provenance:** base rate 9.9%; strongest positive signals BANT-Strong
  (+1.2) and HOT cities (+1.1); strongest negatives BANT-Weak (−2.3) and
  Facebook source (−1.6).
