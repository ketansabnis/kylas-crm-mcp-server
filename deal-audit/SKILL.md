---
name: deal-audit
description: >-
  Audit the pre-sales data on a Kylas CRM deal for Sell.do (real-estate sales
  CRM) and post an audit note to the deal. Use when asked to "audit a deal",
  "run the pre-sales audit", "qualify/validate this deal", "check a deal by ID
  before a demo", or when a pre-sales agent shares a deal for a sales demo. The
  skill enriches the deal's primary contact (phone + email) via
  enrich_deal_primary_contact to verify identity (name_validation), classifies
  the account (Developer / Broker / Mandate company), verifies the brand and
  footprint online (website, LinkedIn, Instagram, Facebook, Google Maps,
  property portals, advertising), checks the claimed licence count against that
  footprint, scores ICP + BANT + data integrity, and writes everything to a
  single audit note on the deal. It flags discrepancies — it never overwrites
  the pre-sales fields.
metadata:
  type: workflow
  domain: kylas-crm / sell.do real estate
---

# Sell.do Pre-Sales Deal Audit

## Purpose & context

Pre-sales agents create a deal when they want to hand it to **sales** for a
demo. They fill in everything they know — **across both structured fields AND
free-text notes**. This skill audits that data: it checks whether what was
written is correct and valid, enriches it with online research, and leaves a
sales rep everything they need before a demo. The customer base is real-estate
businesses buying **Sell.do**, a real-estate sales CRM.

**Golden rules**
- **Audit, don't overwrite.** Output is a single **note** on the deal. Never
  change the deal's fields (licences, estimated value, phone, contact, etc.).
- **Never change a phone number.** You may *find and list additional* numbers in
  the note, but the rep decides what to add.
- **A claim only counts when verified.** A name in a pre-sales note is not
  evidence. This is especially strict for **Authority** (see below). Online
  research and the contact enrichment (see Phase 5) are both valid
  evidence sources.
- **Always post the audit note automatically.** Do NOT ask for confirmation —
  posting the note to the deal is the expected end of every run. (Only the note
  is written; fields and phone numbers are never touched, so this is safe.)

## Phase 0 — Kylas session setup (mandatory, once per session)

1. `get_entity_labels()` first.
2. `get_deal_field_instructions()` before reading the deal.

**Enrichment availability check.** This skill uses the
`enrich_deal_primary_contact(deal_id)` MCP tool to resolve the deal's **primary
contact** to a verified identity. It requires the enrichment key to be set on the
MCP server. If the tool returns "not configured," fall back to online research
only for Authority and note in the audit that contact enrichment was unavailable.
Do not treat a missing key as a failure of the audit.

## Phase 1 — Pull the deal AND its notes

1. `get_deal(deal_id)` — capture every field, especially: No. of Licenses,
   Estimated Value, RE Developer/Channel partner, City, Previous CRM, Required
   Tools, Owner Phone, Source/Campaign, associated contacts/company.
2. `get_deal_notes(deal_id)` — **notes are first-class data.** Pre-sales store
   the qualification details here (type of deal, profile/decision maker, company
   name, dev vs channel partner, properties, lead-gen sources, team size,
   current CRM, challenges, price range, timeline).
3. If a note is truncated by the API, open the deal in the browser
   (`app.kylas.io/sales/deals/details/<id>`) and click "Read more" to get full
   text.
4. **Attribute notes correctly.** Note which agent wrote what (the qualifying
   pre-sales agent vs whoever ran the demo). If the user asks to rely on one
   agent's notes and exclude another's, honour that exactly.

## Phase 2 — Classify the business (drives everything downstream)

Do not trust the deal's label — confirm from the website/LinkedIn. Pick one:

- **Developer / builder** — owns & builds projects; sells own inventory.
- **Broker / channel partner** — resells others' inventory; often Gmail/personal
  domain; presence is portal listings rather than own projects.
- **Mandate company** (subset of broker) — holds exclusive sell-side mandates
  for specific projects; behaves like a developer's sales arm; multiple
  mandates, structured teams → largest licence potential among brokers.

Watch for hybrids (a small developer that also resells / acts as "investment
consultant"). Note it.

## Phase 3 — Collect the footprint (evidence base)

Search + fetch and record links for each:

- **Website** — existence is the baseline validity test. *No website = red
  flag.* Capture URL.
- **Project / inventory count** — the licence denominator:
  - Developer: count **ongoing (and recent) projects** from the **website** and
    **portals** (99acres, Magicbricks, Housing.com, NoBroker). Confirm scale
    (towers / units) — a "project" that is one small tower of ~10 units is tiny.
  - Mandate company: count **active mandates / projects represented**.
  - Broker: count **active sales agents** — triangulate LinkedIn headcount,
    portal agent count, number of offices.
- **Advertising presence (best validation signal)** — are they actually running
  ads? Check property portals for sponsored/featured listings and Meta Ad
  Library / Google. Active paid lead-gen validates *Need* and marketing
  maturity and hints at lead volume.
- **LinkedIn company** — employee band, follower count, *and number of real
  employee profiles* (e.g. "11-50 band, 13 followers, 0 listed employees" ≠ a
  50-person org).
- **Instagram / Facebook** — followers + posting activity = brand seriousness.
- **Google Maps** — real office + review count = legitimacy.
- **Email domain** — corporate domain vs Gmail (Gmail → small-operator signal).
- **RERA** — *do not assume you can crawl RERA portals.* If a RERA number/project
  count surfaces via website or portals, great — use it as an independent
  cross-check. Otherwise rely on website + portals for the project count.
- **Key people / org map** — actively research the people, don't just look for
  one LinkedIn hit. For the contact named on the deal AND the wider org:
  - **Contact enrichment (primary identity signal).** First check the deal's
    notes (Phase 1) for a recent **"CONTACT ENRICHMENT"** note — the hourly
    scheduler runs enrichment before this audit, so it is usually already there.
    - If that note exists, **use it** — do NOT call the tool again (saves cost).
    - If it is absent (e.g. a manual audit), call `enrich_deal_primary_contact(deal_id)`
      **once**. It picks the deal's **primary contact** (the one flagged
      "Decision maker"/stakeholder, else the first associated contact), sends that
      contact's primary **phone + email** to enrichment, posts the CONTACT
      ENRICHMENT note, attaches the full JSON to the deal, and returns: resolved
      identity, **name_validation** (MATCH/MISMATCH + the actual phone owner),
      validated contactability (emails/phones), and social/LinkedIn links. It
      excludes credit-bureau and compensation data. (One contact = one input.)
    This is the strongest single signal for *who the contact really is*. Use it to
    anchor the people research, then corroborate with the searches below.
  - Run **multiple** searches, not just LinkedIn: `"<name>" "<company>"`,
    `"<name>"` + role words (founder/director/owner/partner/proprietor/CEO/
    sales head), the company's own **team/about** page, **news / interviews /
    event speakers**, **MCA** director listings, **RERA** (firm proprietor or
    registered agent), and **portal agent profiles** (99acres, Magicbricks,
    Justdial, IndiaMART). A person is **verified** if credible references tie
    them to the company — LinkedIn is one source, not the only gate. (Many real
    Indian real-estate people have weak/no LinkedIn but show up in news, RERA,
    or portal listings.)
  - Always try to surface the **founder / director / owner** and **senior sales
    leaders** by **name + designation**, even when no phone/email is available.
    Names + roles are the deliverable; numbers are a bonus.
  - Detail handling for seniority + scoring is in Phase 5 (Authority).

## Phase 4 — Licence ↔ footprint math (per type)

Same logic (team size implied by what they actually run), different denominator:

| Type           | Count online                                   | Ratio                      | Licences ≈        |
|----------------|------------------------------------------------|----------------------------|-------------------|
| Developer      | Live + recent projects (website + portals)     | 4–5 staff/project (8–10 stretch) | projects × ratio  |
| Mandate company| Active mandates / projects represented         | 5–10 staff/mandate         | mandates × ratio  |
| Broker         | Active sales agents (LinkedIn + portals + offices) | direct headcount        | ≈ verified agents |

Rule of thumb for developers: **50 licences implies ~5–7+ projects running.**
If the footprint shows 1–3 small projects, a 50-licence claim likely overstates
the team relative to the footprint.

**Estimated value = audited licences × ₹1,700** (Sell.do average licence cost).
Always show **Claimed vs Audited vs Recommended** so any gap is visible.

## Phase 5 — Score every pre-sales field

Tag each material field: ✅ Verified · 🟡 Partial · ⚪ Unverified · 🔴 Conflicting.

- **Brand validity** — website (required) + LinkedIn/Instagram/FB/Maps/portals.
  No website → fail.
- **ICP fit** — are they genuinely a real-estate sales business with inventory /
  leads to manage? Developer/broker/mandate all qualify; size sets the tier.
- **Licence vs footprint** — claimed vs audited (Phase 4).
- **Estimated value** — recompute from audited licences.
- **Authority (graded, not binary)** — the job is to judge whether the person on
  the deal is a *real, senior enough* decision maker, and who else matters.
  Don't reduce it to "on LinkedIn + has a phone." Assess three things:
  1. **Identity verified?** Did the evidence tie this person to the company?
     Use **two** complementary sources:
     - **Contact enrichment** (the CONTACT ENRICHMENT note / `enrich_deal_primary_contact`)
       resolves the primary contact's phone+email to the name/title/company
       **registered to that number**, plus a **name_validation** verdict. This is
       decisive:
       • `name_validation = MATCH` and the resolved name ≈ the CRM contact → the
         contact is strongly **verified**.
       • `name_validation = MISMATCH`, or the resolved identity name ≠ the CRM
         contact, or the namelookup phone owner is a *different* person → the
         number does **not** belong to the contact. Treat the contact as
         **🔴 unverified**, name the actual phone owner, and flag it as
         unconfirmed until the rep re-confirms whose number this is.
     - **Multi-source web research** (Phase 3) — corroborate the enrichment.
     "Verified" is independent of whether we have a *new* number — a real person
     confirmed by enrichment or references is verified.
  2. **Seniority / decision level** — place them in the hierarchy, using the
     enriched title where available:
     - Owner / Founder / Director / Proprietor / CXO → **high** (true buyer)
     - VP / Head of Sales / Sales Director → **high-ish** (likely economic buyer
       for a CRM)
     - Project / Sales Manager, Team Lead → **medium** (influencer/champion, may
       not own budget)
     - Executive / Coordinator / Telecaller → **low** (gatekeeper at best)
  3. **Cross-check the pre-sales claim** — if the note labels the contact
     "decision maker" but enrichment/research shows the real owner/director is
     someone else, say so and name the true decision maker. If enrichment's
     `name_validation` disagrees with the pre-sales name, surface it.
  Then give an **authority confidence grade**:
  ✅ Verified-senior (high) · 🟡 Verified-junior (medium → escalate) ·
  🟡 Plausible-but-unconfirmed role (low-med) · ⚪ Not found (low) ·
  🔴 Conflicting / placeholder data.
  **Placeholder detection:** flag low-quality contacts — repeating-digit or
  sequential phones (e.g. +919999999999, 1234567890), obviously fake names, or
  throwaway emails → 🔴. (A clearly-junk Owner Phone is also not worth an
  enrichment call — skip enrichment and flag it.)
  **Solo brokers:** before calling an individual broker "unverifiable," check
  **RERA agent registration** and **portal agent profiles** — a broker with a
  real RERA agent ID is materially more qualified than one with no footprint.
  **Always list other key people** found (founder/director/sales head) with name
  + designation, and state **who sales should actually pursue / escalate to**.
- **Need** — current CRM (or none), lead-gen sources; verify the ad claim if you
  can. Right-size expected lead volume to their inventory.
- **Budget / Timeline** — usually in notes; flag if blank.

### Using `enrich_deal_primary_contact` (scope & cost)

- **At most one call per deal.** If a CONTACT ENRICHMENT note already exists on
  the deal (the hourly scheduler posts one before this audit runs), **reuse it**
  and do not call the tool again. Only call it yourself when that note is absent.
- The tool enriches only the **primary contact** (decision-maker flag wins, else
  the first associated contact), sending its **phone + email**. One contact = one
  input — never loop it over every contact.
- It is **BANT-focused**: it returns identity, professional profile (title /
  company / LinkedIn), social links, name_validation, and validated phone/email
  contactability. It deliberately **excludes credit-bureau and compensation**
  data — do not ask for or rely on those.
- The tool also posts its CONTACT ENRICHMENT note and attaches the full JSON to
  the deal automatically. If the contact has no usable phone or enrichment is not
  configured, it says so — fall back to web research and note it.
- Treat the enrichment as evidence, not gospel: corroborate a confident result
  with web research; a blank/low-confidence result is ⚪ Not found, not 🔴.
- If `name_validation = MISMATCH`, or the resolved identity / namelookup phone
  owner is a *different* person than the CRM contact, that is a strong
  **🔴 Conflicting** signal — call it out, name the real phone owner, and
  recommend the rep re-confirm the contact before the demo.

## Phase 5.5 — Conversion-probability score (predict, don't just describe)

After scoring the fields, compute a **conversion-probability band** from the values
you just **audited** (use the audited licence tier and the graded Authority/BANT, not
the raw pre-sales claims). Model fitted on June-2026 pre-sales demos (calibrated:
top-quintile 36.5% predicted vs 34.0% actual).

**Step 1 — start at `S = −2.2`** (base log-odds; base win-rate ≈ 10%).

**Step 2 — add the points that apply:**

| Feature | Value → points |
|---|---|
| **BANT** (your Phase-5 read) | Strong **+1.2** · None/Missing −0.3 · Partial **−1.6** · Weak **−2.3** |
| **City** | Hyderabad or Chennai **+1.1** · other non-metro −0.2 · core metro (Mumbai/Delhi-NCR/Bangalore/Pune) −0.3 |
| **Demo mode** | Onsite **+0.6** · Online −0.1 |
| **Account type** | Developer **+0.3** · Channel partner / Broker −0.3 |
| **Audited licences** | 10+ **+0.4** · 5–10 +0.2 · under 5 **−0.4** |
| **Source** (if known) | Organic +0.4 · Google / WhatsApp 0 · Facebook / Instagram **−1.6** |
| **Stage momentum** (open deals only) | Payment Confirmed +1.2 · Hot Opportunity +0.7 · Quote Sent +0.3 · Demo Conducted 0 |
| **Idle penalty** (open deals) | idle > 30 days −0.5 · idle > 60 days −1.0 |

**Step 3 — read the band off the total `S`** (no exponential needed):

| Total S | Band | ≈ Probability |
|---|---|---|
| S ≥ −1.4 | **🔥 HOT** | ≥ 20% |
| −2.0 ≤ S < −1.4 | **🟠 WARM** | 12–20% |
| −2.75 ≤ S < −2.0 | **🟡 MID** | 6–12% |
| S < −2.75 | **❄️ COLD** | < 6% |

(Exact probability if wanted: `p = 1 / (1 + e^(−S))`.)

**Worked examples**
- Developer, 30 seats, Hyderabad, onsite, Strong BANT, Organic:
  S = −2.2 +1.2 +1.1 +0.6 +0.3 +0.4 +0.4 = **+1.8 → 🔥 HOT (~86%)**.
- Channel partner, 2 seats, Jaipur, online, Weak BANT, Facebook:
  S = −2.2 −2.3 −0.2 −0.1 −0.3 −0.4 −1.6 = **−7.1 → ❄️ COLD (~0.1%)**.

**Why it matters:** on June data, demos in **HOT/WARM** held ~92% of all wins; **COLD**
(bottom ~60% of demos) held 1 of 25. So the band is a triage signal — HOT → route to a
**senior rep + push for an onsite**; COLD → deprioritise / don't burn a demo slot.

> Programmatic option: `score_deal.py` + `model_weights.json` (bundled in this skill's
> `scripts/` folder) compute the same number in code — call `score_deal(deal)` if the
> scheduler prefers to write `probability`+`band` to a deal field. Re-fit monthly.

## Phase 6 — Build the audit note

Assemble ONE note containing, **in this order**:

1. **VERDICT — first line, before anything else.** One line:
   `VERDICT: <🟢/🟡/🔴> <High confidence | Confirm on demo | Key data unverified>
   — <one-line reason>`. This is the analyst's read on data quality, not an
   instruction — the rep gets the picture at a glance and decides next steps.
1b. **CONVERSION — second line, right under VERDICT.** One line from Phase 5.5:
   `CONVERSION: <🔥 HOT | 🟠 WARM | 🟡 MID | ❄️ COLD> (~X%) — drivers: <e.g. Strong
   BANT, developer, 20 seats, Hyderabad>; drag: <e.g. online-only, idle 40d>`.
   This is the model's probability-to-convert prior — it tells the rep how hard to lean in.
2. Header: `🔍 DEAL AUDIT — Deal #<id> / <Company> (<contact>) · <date>`
   (Always title the note "Deal Audit" — never "Pre-Sales Audit".)
3. **Classification** (dev / broker / mandate, + hybrid caveat).
4. **Brand validity** with the **research links** (website, Instagram,
   LinkedIn, Facebook, Google Maps, portal listing) and legal entity + named
   founder/director. *Pre-sales rarely capture these links — always add them.*
5. **Authority & org map** — the deal contact with **verified? + seniority +
   confidence grade**; **what phone enrichment returned** for the Owner Phone
   (name / title / company / seniority, or "not configured / unresolved");
   whether they're the true decision maker (or who is); and **other key people**
   (name + designation) with **who sales should pursue / escalate to**.
6. **🔴/🟡/⚪ flags** for licence count, estimated value, need, budget/timeline —
   each as **Claimed → Audited → Recommended**.
7. **Extra contacts found** (clearly marked "not added to fields"); flag any
   placeholder data.
8. **Right-sized seat range + demo hooks** for the rep.

Keep it scannable (the rep reads it pre-demo). Use the established format in
`reference/note-template.md`.

## Phase 7 — Post the note (the action — always do this)

1. **Post automatically — do NOT ask for confirmation.** Call
   `add_note(entity_type="deal", entity_id=<deal_id>, text=<note>)` as the final
   step of every run.
2. Then show the user the posted note and confirm it's live on the deal.
3. **Touch nothing else on the deal** — only the note is written; fields and
   phone numbers are never modified.

## Verdict bands

These describe the **state of the data**, not an action. The verdict is the
analyst's read; sales decides what to do with the deal.

- **🟢 High confidence** — material fields verified; an online- or
  enrichment-verified, contactable decision maker exists.
- **🟡 Confirm on demo** — on-ICP, with a few items for the rep to confirm during
  the demo (e.g. budget/timeline not yet captured, licence count to reconcile,
  enrichment unavailable).
- **🔴 Key data unverified** — material fields could not be verified or look
  inconsistent (e.g. licence count appears overstated vs footprint alongside no
  verifiable decision-maker contact, no website found, or phone enrichment that
  points to a different contact/company). Surfaced for the rep's awareness so
  they can confirm before investing demo time.
