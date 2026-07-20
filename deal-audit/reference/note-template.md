# Audit note template

Fill the bracketed parts. Keep it scannable. Use ✅ 🟡 ⚪ 🔴 consistently.
**The VERDICT line is always first.**

```
VERDICT: <🟢/🟡/🔴> <High confidence | Confirm on demo | Key data unverified> — <one-line reason>

🔍 DEAL AUDIT — Deal #<id> / <Company> (<contact>) · auto-research <DD-Mon-YYYY>

Classification: <Developer | Broker | Mandate company> <✅/flag> (<hybrid/caveat if any>)

Brand validity: <✅ VALID | 🔴 NO WEBSITE> —
 • Website: <url or "NONE — none found">
 • Instagram: <url / —>
 • LinkedIn: <url / —>
 • Facebook: <url / —>
 • Google Maps: <office address / —>
 • Portal listing(s): <url(s) / —>
 Legal entity: <name>.

Authority & org map:
 • Contact enrichment (primary contact): <name / title / company / seniority returned by enrich_deal_primary_contact | "not configured" | "unresolved">.
 • Deal contact: <name>, <designation> — <✅ verified-senior | 🟡 verified-junior →escalate | 🟡 plausible/unconfirmed | ⚪ not found | 🔴 placeholder> (via <enrichment / news / RERA / portal / LinkedIn / site>).
 • True decision maker: <same as contact | actually <name>, <role>>.
 • Other key people: <name – designation>; <name – designation> (numbers if found, else names/roles).
 • Sales should pursue / escalate to: <name/role>.

🔴 LICENCE COUNT — <verdict>. Claimed <n>.
 Footprint: <projects/towers/units or agents found, with source>.
 At <ratio> this supports ~<audited range> licences. LinkedIn: <band/followers/listed>.
 → Sales to confirm actual team size.

🔴 ESTIMATED VALUE — deal shows ₹<current>.
 At ₹1,700/licence: audited ~<range> → ₹<range>; ₹<claimed×1700> only if <claimed> verified.

⚪ NEED — <verified?>. <current CRM, lead-gen sources, ad-presence finding>.

⚪ BUDGET / TIMELINE — <from notes / blank>. Capture on demo.

Extra contact found (NOT added to fields): <number/email>. <Flag placeholder if any.> Existing phone left untouched.

Right-size: <seat range>. Hooks: <…>.
```

## Worked example — Deal #4398381 / AMBR Homes

A residential micro-developer: website lists 3 "projects" (one Sector-1
cluster); portals show Ambrosia = 1 tower, ~10 units, ready-to-move. Pre-sales
claimed 50 licences → audited ~5–10. Decision-maker "Nikhil" not found online;
director Magan Bhati found on the site but no contact → escalate target is
Magan Bhati. Verdict line: `VERDICT: 🔴 Key data unverified — micro
single-building developer, 50-licence claim ~5–10× above footprint, no verified
decision-maker`.

## Authority research reminder

Verify people across MANY sources (contact enrichment, news, RERA, MCA,
portal agent profiles, team pages) — not just LinkedIn. The
`enrich_deal_primary_contact` tool is the strongest single identity signal: it
resolves the primary contact's phone to the name/title/company/seniority
registered to that number. "Verified" ≠ "has a phone." Grade by seniority, name
the true decision maker, and always list other key people + who to escalate to.
A name from a pre-sales note with zero corroboration is ⚪ not found; a person
confirmed via enrichment or references is verified even without a new number. If
enrichment resolves the contact's phone to a *different* company/person than the
deal claims, that is 🔴 Conflicting.
