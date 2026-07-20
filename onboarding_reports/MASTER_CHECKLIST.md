# Sell.do Onboarding — Master Checklist
**The definition of "done" for an onboarding. Built 13-Jul-2026 from the Kylas deal custom fields + the recurring items across the open-deal note corpus.**

Every item below maps to a Kylas deal field, so coverage is machine-checkable every run
(`scripts/coverage.py` → Sheets 13 & 14).

Four possible states per item: **Completed · Initiated · Waiting on customer · Not required.**
A **blank** field is a fifth, unofficial state — and it is the most dangerous one, because
blank work is invisible work.

---

## Tier 1 — MUST HAVE
*The account is not live without these. "Not required" is not an acceptable answer — if an owner
claims it, they must say why, on the deal, in writing.*

| # | Item | Kylas field | Segment |
|---|---|---|---|
| 1 | Account activated (signed up) | `cfAccountActivationStatus` | all |
| 2 | User logins created | `cfUsersSetup` | all |
| 3 | Projects created | `cfProjectsSetup` | Developer (Basic for Broker/CP) |
| 4 | Lead routing configured | `cfRoutingSetup` | all |
| 5 | Pipeline / stages configured | `cfPipelineSetupStatus` | all |
| 6 | Existing leads imported | `cfLeadImport` | all |
| 7 | **≥1 lead source live** | any of `cfWebsiteIntegrationStatus`, `cfFacebookLeadgenIntegrationStatus`, `cfPropertyPortalIntegrationStatus`, `cfGoogleLeadsIntegrationStatus` | all |
| 8 | Sales / pre-sales training | `cfSalesTrainingStatus` | all |
| 9 | Admin training | `cfAdminTrainingStatus` | all |
| 10 | Channel-partner module | `cfChannelPartnerSetupStatus` | Channel-partner accounts |
| **Exit** | Handover status + onboarding feedback | `cfHandoverStatus`, `cfOnboardingFeedbackReceived` | all |

**Item 7 is the one nobody checks.** A CRM with no lead source is a database nobody fills.
**30 of 58 open deals currently have no lead source live.**

## Tier 2 — BASIC
*Standard for the segment. "Not required" is allowed, but it should be a decision someone made —
not a way of clearing a row.*

| Item | Kylas field | Segment |
|---|---|---|
| Website integration | `cfWebsiteIntegrationStatus` (+ `cfWebsiteIntegrationMethod`) | all |
| Meta / Facebook lead-gen | `cfFacebookLeadgenIntegrationStatus` | all |
| Property portals (99acres, Housing, MagicBricks) | `cfPropertyPortalIntegrationStatus` | all |
| WhatsApp integration | `cfWhatsappIntegrationStatus` (+ `cfWhatsappVendor`) | all |
| WhatsApp templates | `cfWhatsappTemplateSetupStatus` | all |
| Cloud telephony / IVR | `cfCloudTelephonySetup` (+ `cfCloudTelephonyVendor`) | all |
| DLT (SMS) registration | `cfDltSetup` | all |
| Offline dialer / tracker app | `cfOfflineTrackerAppSetup` | all |
| Workflow automation | `cfWorkflowAutomationSetupStatus` | all |
| Inventory / units loaded | `cfInventorySetup` | Developer |
| Site-visit form | `cfSiteVisitFormSetupStatus` | Developer |
| Marketing training | `cfMarketingTrainingStatus` | all |

## Tier 3 — ENHANCED
*Only if sold. The order form (`cfRequiredTools`) is the contract — anything on it must end up Completed.*

`cfRequiredTools` options: **AI Calling · CP Management Tool · IRIS · NPS Tool · Budgeting Tool · Personal WA · Native WA · AI Content · CRM**

| Item | Kylas field |
|---|---|
| Google / LinkedIn lead-gen | `cfGoogleLeadsIntegrationStatus`, `cfLinkedinLeadsIntegrationStatus` |
| Cost-sheet template | `cfCostSheetTemplateSetupStatus` |
| Payment-schedule template | `cfPaymentScheduleTemplateSetupStatus` |
| Booking documents / Bookings import | `cfBookingDocumentsSetupStatus`, `cfBookingsImport` |
| Post-sales templates | `cfPostSalesTemplatesSetup` |
| Sales / Owner / Marketing dashboards | `cfSalesDashboardSetupStatus`, `cfOwnerDashboardSetupStatus`, `cfMarketingDashboardSetupStatus` |
| Goals, ROI config | `cfGoalsSetupStatus`, `cfRoiConfigurationSetupStatus` |
| Bulk dialer | `cfBulkDialerSetupStatus` |
| Email sub-domain | `cfEmailSubdomainSetup` |
| ERP / Zoho Analytics / Approvals / Online meeting | `cfErpIntegrationStatus`, `cfZohoAnalyticsSetupStatus`, `cfApprovalSetupStatus`, `cfOnlineMeetingIntegration` |

---

## How the coverage check catches skipping

| Flag | Trigger | Why it matters |
|---|---|---|
| **CHALLENGE** | "Not required" on a **MUST** item | The commonest way to make a hard task disappear. |
| **NOT TRACKED** | Blank on a Must/Basic item | Invisible work. Reads as "fine" in every report that only counts Completed. |
| **NO LEAD SOURCE** | No lead source Completed | We delivered a CRM with nothing flowing into it. |
| **SOLD NOT DELIVERED** | On `cfRequiredTools` but the setup field is blank / Not required | We billed for it and didn't build it. |
| **GO-LIVE FICTION** | Actual Go-Live date set while MUST items are open | The date is decorative. |
| **PREMATURE HANDOVER** | Handed over with MUST items open | Support inherits our unfinished work. |
| **NO FEEDBACK** | Handed over without the feedback form | No closing signal from the customer. |
| **STALLED ITEM** | Initiated / Waiting > 30 days after start | The item is parked, not progressing. |

---

## Baseline — 13-Jul-2026 (58 open deals)

| Flag | Count |
|---|---|
| NOT TRACKED (blank Must/Basic fields) | **149** |
| STALLED ITEM | 83 |
| **NO LEAD SOURCE** | **30 deals** |
| **CHALLENGE ("Not required" on a MUST)** | **23** |
| GO-LIVE FICTION | 12 |
| NO FEEDBACK at handover | 5 |
| PREMATURE HANDOVER | 2 |
| SOLD NOT DELIVERED | 1 |

### The 23 CHALLENGE items — MUST-haves marked "Not required"

- **Times Group** (₹9.4L, 50 licences): **lead routing, pipeline stages AND lead import** all marked *Not required*. On an enterprise account. This is why it has sat >180 days.
- **SKYTOWN** (₹7.3L), **Navkar** (₹5L), **GRUHAM** (₹4.8L), **VENDSPACEZ** (₹3.5L), **VRUSHABADRI**, **Shrimant**, **Properties Boutique**: lead import marked *Not required*.
- **All three AI-calling deals** (GGC, Mythri, Kohinoor): lead import, sales training **and** admin training all *Not required* — i.e. we sold an AI calling bot and formally decided the customer needs no leads and no training.
- **Red Estate, Upcurve, Palli, Ribitto**: channel-partner module *Not required* — on accounts that are Channel-partner segment.

### Two different ways of hiding — and both look clean

| Owner | Deals | "Not required" rate | Blank-field rate | Avg MUST complete |
|---|---|---|---|---|
| Sourabh Sahu | 2 | **68%** | 3% | 57% |
| Venkat Viswavardhan | 13 | **62%** | 8% | 72% |
| Sanket Nampalliwar | 2 | **61%** | 3% | 58% |
| Muntazar Mhate | 14 | **58%** | 3% | 59% |
| Raahul Ramanan | 5 | 52% | 2% | 77% |
| Sahil Jane | 11 | 45% | 29% | 62% |
| **Shweta Gouda** | 9 | 10% | **69%** | **40%** |
| Ganesh Vamsee | 1 | 0% | **100%** | 0% |

**Muntazar / Venkat / Sourabh disclaim the checklist** (mark it Not required).
**Shweta and Ganesh simply never fill it in.** Both strategies produce a report with nothing red in it.

### GO-LIVE FICTION — 12 deals have an Actual Go-Live date with MUST items still open
Kunwarji (₹14.3L), Calicut (₹6.3L), Shri Krish (₹5.3L), GRUHAM (₹4.8L), NPS (₹4.3L), i5 (₹3.5L), Gram (₹3.3L), VAZHRAA, Upcurve, Shrimant, Real Estate Square, SPR.

---

## What the CRM cannot see

These recur constantly in the notes but have **no field**, so they can never be tracked or flagged:
**hierarchy setup · sourcing setup · clock-in/clock-out · GPS tracking · Meta business verification · CAPI integration · landing pages · Q&A session · mobile training · feedback-form chase.**

If it matters enough to appear in every third note, it should be a field. Until then it is invisible work — and invisible work is exactly what goes missing.
