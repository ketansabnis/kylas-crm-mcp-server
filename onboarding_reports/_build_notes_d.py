import json

# newest-note body (verbatim as returned), max epoch, gist, jira keys (distinct, uppercase)
N = {}

N["4269153"] = (1784091355284,
  "This Client Was on Hold &amp; we are resuming it from today onwards. Today we will be covering sales training Completed Tasks: User Activation Lead Import - As discussed, you don't want to upload any leads in the CRM.&nbsp; ​ Project Creation&nbsp; Clock In Clock Out Option Default Report Configuration &nbsp; Pending Tasks: Meta Integration - Please do let us know once the Campaigns are live Dialer App Sales Training - Sales Training scheduled today at 3:00pm. Admin Training Not Required: Website Integration Property Portal Integration Google ads Inventories Management No IVR Required as calling will be done using Personal Phone",
  "Resumed after hold; sales training today, Meta/dialer/admin pending; broker with no lead upload.",
  [])

N["4255693"] = (1783516955567,
  "This week's Task:-&nbsp; * Q&amp;A Session * Mobile Training * Admin Training 2.0",
  "This-week plan: Q&A session, mobile training, Admin Training 2.0.",
  [])

N["4255681"] = (1783944320207,
  "This weeks Pointers * Get pointers moved - and drop email.&nbsp; * Sankit will speak with Dev * Add Ketan in Calling in JIRA.&nbsp; &nbsp;",
  "Weekly pointers; client blocking implementation until calling integration done; escalate calling JIRA.",
  [])

N["4241966"] = (1783713926577,
  "Pushing Netram to do outgoing calling.&nbsp;",
  "Pushing customer (Netram) to start outgoing AI calling; reports/handover discussion pending.",
  [])

N["4233760"] = (1783713883576,
  "Awaiting flow and feedback from customer.",
  "AI calling flow built/tested; awaiting customer feedback and confirmation.",
  ["SS-12285"])

N["4233715"] = (1783713906471,
  "Few issues raised in outgoing calling. JIRA Raised for the same.",
  "Outgoing AI calling issues; JIRAs raised (bulk-call list ESTATE-21040, AI calling SS-12176).",
  ["ESTATE-21040", "SS-12176"])

N["4230613"] = (1783401767413,
  "We had a meeting with the client on 0 3rd July 2026 , along with Ketan Sir and Siddharth. &nbsp; During the discussion, the client expressed concerns regarding the rollout timelines and the delay in the implementation process. They also requested that a member of our team be available at their office for 3–5 days to assist their team with the ongoing challenges and complete the pending setups. &nbsp; The onsite visit will be planned once this week's deployments are completed. &nbsp; As discussed, the majority of the Jira tickets, including the mobile-related enhancements, are planned for deployment by 15th July 2026 . Following the deployment, we will provide dedicated support for the next 15 days to ensure a smooth transition and completion of the pending activities. Based on the current plan, we are targeting to complete the implementation by the end of July 2026 or, at the latest, during the first week of August 2026 .",
  "Escalation meeting with Ketan/Siddharth; client unhappy on delays; onsite + JIRA deploys by 15 Jul, go-live end-Jul/early-Aug.",
  [])

N["4177642"] = (1783517438607,
  "This week's Tasks: * Initiate AI calling - &nbsp;Get them to take a demo.&nbsp; * Mcube - Concern * Plan Admin * Finish WhatsApp.&nbsp;",
  "This-week plan: initiate AI calling demo, Mcube concern, plan admin training, finish WhatsApp.",
  [])

N["4147287"] = (1783713972451,
  "Whatsapp flow will be shared by Monday. &nbsp; No update on inventory.",
  "Awaiting WhatsApp flow (by Monday) and inventory files from customer; CP imported.",
  [])

N["4144089"] = (1783713947780,
  "Have to arrange a call with customer on pending pointers.",
  "Likely refund/churn risk: customer says sales over-promised (GRE/post-sales); AI calling is blocker.",
  [])

N["3968505"] = (1783713369250,
  "GRE form delivered, awaiting update from customer on the same.",
  "GRE walk-in form delivered; awaiting customer feedback; flagged as Re-OB.",
  [])

N["3575524"] = (1783944042767,
  "This weeks task:- * Schedule online call by tomorrow.&nbsp; * Update on Manoj Pointers.&nbsp; * Ask amit to follow-up on payment *&nbsp;",
  "Weekly plan: schedule call, Manoj pointers, chase payment; pending docs review + external handover.",
  [])

N["3304063"] = (1783415092241,
  "As discussed with the client's POC ( Mr. Mithilesh ) and Director ( Mr. Abhishek ), we have scheduled a meeting for tomorrow (8th July 2026) to reinitiate the OB process. &nbsp; The meeting will primarily focus on the following activities; &nbsp; Reviewing the current OB status. Discussing the pending setup activities. Finalizing the implementation plan and priorities. Addressing the client's open concerns and queries. Agreeing on the next steps and timelines for completion.",
  "OB reinitiation meeting scheduled 8 Jul with POC/Director; long-stalled since Sep-2025 (2 customization JIRAs).",
  [])

N["3304062"] = (1783415098472,
  "As discussed with the client's POC ( Mr. Mithilesh ) and Director ( Mr. Abhishek ), we have scheduled a meeting for tomorrow (8th July 2026) to reinitiate the OB process. &nbsp; The meeting will primarily focus on the following activities; &nbsp; Reviewing the current OB status. Discussing the pending setup activities. Finalizing the implementation plan and priorities. Addressing the client's open concerns and queries. Agreeing on the next steps and timelines for completion.",
  "Twin of Shree Honda: OB reinitiation meeting 8 Jul; stalled since Sep-2025 pending customization.",
  [])

N["3302998"] = (1783402010067,
  "The data has been uploaded successfully. However, the client has reported multiple discrepancies in the uploaded data. To address these issues, we requested a meeting with the client so that we could review the discrepancies together and resolve them over a call. However, the meeting was rescheduled from the client's end. &nbsp; An internal data validation meeting has been scheduled today ( 7th July 2026 ) with the Tech team and Siddharth. Following this discussion, we have requested the client to join a meeting with us so that they can walk us through the reported discrepancies. At present, we are not observing any inconsistencies from our end, and we will try to identify and resolve the issues during the call. &nbsp; Apart from this, the majority of the technical deliverables have been completed. The only pending items are the formula-based custom fields and the Roles &amp; Access configuration.",
  "Inventory data uploaded; client reports discrepancies; internal data-validation meeting 7 Jul; formula fields + roles pending.",
  ["ESTATE-18697"])

order = ["4269153","4255693","4255681","4241966","4233760","4233715","4230613",
         "4177642","4147287","4144089","3968505","3575524","3304063","3304062","3302998"]

out = {}
for did in order:
    epoch, raw, gist, jira = N[did]
    out[did] = [epoch, raw[:300], gist, jira]

p = "/sessions/eager-friendly-knuth/mnt/kylas-crm-mcp-server/onboarding_reports/notes_2026-07-16_d.json"
with open(p, "w") as f:
    json.dump(out, f, indent=2, ensure_ascii=False)
print("wrote", p, "deals:", len(out))
for did in order:
    print(did, out[did][0], "jira=", out[did][3], "| len raw", len(out[did][1]))
