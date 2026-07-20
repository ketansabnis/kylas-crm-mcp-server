---
name: onboarding-pipeline-review
description: >-
  Generate the Sell.do Onboarding Pipeline review (Kylas deal pipeline 27474) as a dated
  multi-sheet Excel plus a qualitative deep-dive, store it, and compare against the last
  2-3 runs to flag deals that have not genuinely moved (SUPER-RED). Cross-checks every JIRA
  cited in an onboarding note against the live ticket, classifies who is REALLY blocking each
  deal, and maintains an escalation register. Use when asked to "run the onboarding review",
  "onboarding pipeline report", "Monday/Thursday onboarding review", or to compare onboarding
  reports week-over-week. Runs Mon & Thu.
---

# Onboarding Pipeline Review (Sell.do, Kylas pipeline 27474)

Produces a **12-sheet Excel + a deep-dive memo** for the CEO/CRO and Onboarding Head, saved dated,
compared against prior runs.

The point of this review is **not** to report status. The owners already report status, every week,
in the notes. The point is to find **where the reported status is not true** — and to say so with
evidence. Everything below exists because a previous run got fooled.

---

## Storage
All runs live in `onboarding_reports/` inside the connected workspace:
- `Onboarding_Pipeline_Review_YYYY-MM-DD.xlsx` — the report (12 sheets)
- `Onboarding_Deep_Dive_YYYY-MM-DD.md` — the memo + paste-ready group message
- `snapshot_YYYY-MM-DD.json` — machine record, source of truth for comparison
- `deep_analysis_YYYY-MM-DD.json` — every computed number behind the memo
- `jira_status_YYYY-MM-DD.json` — live status of every JIRA cited in a note
- `fresh_YYYY-MM-DD.json` — raw membership sets from the Kylas pull

**Never delete prior snapshots.** They are the comparison history and the escalation clock.

---

## Run procedure

### Step 0 — Set the run date and windows
`RUN_DATE` = today (YYYY-MM-DD). Compute cutoffs (calendar days before RUN_DATE):
**5d, 7d, 15d** (last activity), **14d, 30d, 60d, 90d, 180d** (deal age).
Format `YYYY-MM-DDT00:00:00.000Z`, timeZone `Asia/Kolkata`.
Call `get_entity_labels()` first. Ensure openpyxl (`pip install openpyxl --break-system-packages`).

### Step 1 — Pull from Kylas (entity `deal`, pipeline `27474`, `forecastingType=OPEN`)
Record the **membership** (deal IDs) of each set into `fresh_RUN_DATE.json`:

1. **All open deals** — `search_entity(deal,[pipeline=27474, forecastingType=OPEN], size 100)`.
2. **Stages** (`pipelineStage=`): Open `189650`, Kickoff Done `189654`, Onboarding In Progress `189655`, Pending on Customer `213154`, Under Usage Tracking `189656`. *Sanity check: the five must sum to the total.*
3. **Last activity** (`latestActivityCreatedAt` `less`): RUN-5d, RUN-7d, RUN-15d.
4. **Deal age** (`createdAt` `less`): RUN-14d, RUN-30d, RUN-60d, RUN-90d, RUN-180d.
5. **Value** (`cfBilledAmount` `greater_or_equal`): 1000000, 700000, 500000, 300000, 200000, 100000.
6. **Licences** (`noOfLicenses` `greater_or_equal`): 50, 20, 10.
7. **Customer Category** (`cfCustomerCategory` `equal`): A `136713`, B `136714`, C `136715`, Broker `186493`, Push-to-OB `201673`.
8. **Tasks**: `taskDueOn` `less` RUN_DATE (overdue) and `greater_or_equal` RUN_DATE (future). *No-task = in neither set.*
9. **Go-live overdue**: `cfTargetGoLiveDate` `less` RUN_DATE.
10. **Activation**: `cfAccountActivationStatus` `equal` `136882` ("Yet to sign up").
11. **New deals**: `get_deal(id)` for every deal not in the prior snapshot — this is the only way to get billed / received / licences for them.
12. **Notes**: see Step 2. This is the step that decides whether the review is any good.

### Step 2 — Notes: read them properly (the single biggest trap)
`get_deal_notes` returns notes **UNSORTED and PAGINATED**. Page 1 is *not* the newest notes.
A `size=3` or `size=5` call routinely misses the most recent note entirely — which silently turns a
stuck deal into a "progressed" one, or vice versa.

**Procedure, no shortcuts:**
- Call `get_deal_notes(id, size=5)`. Read the reported **total**.
- If `total > 5`, page through **every** page (`page=1`, `page=2`, … — the param is 0-indexed, so `page=1` is the second page) until you have seen all of them.
- Take the note with the **maximum `Created` epoch**. That, and only that, is the latest note.
- Batch 12-15 calls at a time to avoid 429s.

Store **two** things per deal:
- `last_note_raw` — the raw note text, first ~300 chars, verbatim. **The scripts compare these to detect re-pasted notes. If you store only your own summary, the detector is blind.**
- `last_note_text` — your one-line gist for humans.

Also record `jira_keys` — every `ESTATE-nnnnn` / `SS-nnnnn` mentioned in *any* of the deal's notes.

### Step 3 — Assemble `current_data.json`
Build `{report_date, run_label, run_index, pipeline_id, pipeline_name, owner_gaps, deals:[…]}` using
the record schema below. Derive bands/flags from the Step-1 membership sets.

Carry forward from the prior snapshot: `brand`, `suggested`, `gflag`, `greason`, `nstep`,
`pending_verdict`, `blocker_owner`. **Do NOT carry forward `vband`/`lband`** — recompute them from
this run's live buckets (the carried-forward `billed` figure is frequently null; the buckets are truth).

### Step 4 — Pre-classify movement
`python3 scripts/compare.py --data current_data.json --outdir onboarding_reports --date RUN_DATE`

It settles the deterministic cases and prints a REVIEW list, **restated-notes first**, each with a
similarity score and a suggested verdict. Three rules are baked in — read the docstring.

### Step 5 — Qualitative judgement (the actual job)
For every REVIEW deal, read `note_prev` vs `note_now` **and the stage**, then set
`movement_verdict` + a one-line `movement_reason`:

- **Progressed** — a blocker was actually resolved, a task was actually completed, or the deal was handed over/closed. `stuck_streak = 0`.
- **Same-blocker** — the note restates the same pending ask. `stuck_streak = prev + 1`.

**A new note is not movement. A stage flip is not movement. Only a change in substance is movement.**

Tests to apply before you accept a "Progressed":
- If `restated: true` (≥80% identical to last week's note) → it is **Same-blocker** unless you can name the specific thing that changed.
- If the newest note predates the last run → nothing happened since the last review. compare.py already marks this `No-activity`; do not overturn it because the note "looks recent".
- If the note says a training/call is *scheduled*, that is not progress. It is progress when it is *completed*. A date that slips ("today" → "next week") is **Same-blocker**.
- "Waiting on customer" is only Progressed if the *thing being waited for* changed.

### Step 6 — JIRA reality check (do not skip this — it is where the truth is)
Collect every JIRA key from `jira_keys`. Fetch each one live via the Jira MCP
(`getJiraIssue` / `searchJiraIssuesUsingJql` on `selldo.atlassian.net`, fields: summary, status,
assignee, updated, fixVersions, priority). Write `jira_status_RUN_DATE.json`:

```json
{"ESTATE-21040": {"summary":"…","status":"Won't Fix","statusCategory":"done",
                  "fixVersion":"11.3","updated":"2026-07-13","assignee":"…"}}
```

`analyze_deep.py` then flags each cited ticket:
- **GHOST DEPENDENCY** — ticket is Done / Won't Fix / Closed, but the deal is *still* parked against it. The customer is waiting for something that will never arrive, or that arrived months ago. **This is the finding that matters most. Lead with it.**
- **STUCK IN OUR QUEUE** — QA Clarification / Tech Discussion / Blocked. The customer is being told "raised with tech" while it sits in our own queue.
- **STALE TICKET** — no update in >14 days.

*(13-Jul-2026, for calibration: Kohinoor had been waiting since May on ESTATE-21040, marked
**Won't Fix**, severity Critical. Times Group — 7-10L, 50 licences, >180 days open — was parked on
ESTATE-18697, which had been **Done since February**. Neither owner knew. Both had been reporting
"pending on customer / tech" for seven consecutive reviews.)*

### Step 6b — Scope coverage: what did they skip?
Flagging stuck deals creates an incentive to *stop tracking* the hard items. The two ways scope
disappears are **"Not required"** and **a blank field** — and both look identical to a finished task
in any report that only counts what is Completed.

So every run must also check the deal against the **master checklist** (`MASTER_CHECKLIST.md`):

1. `get_deal(id)` for **every** open deal and record the ~38 `cf*` setup/status fields, coding each
   `Completed=C, Initiated=I, Waiting on customer=W, Not required=N, absent="-"`, plus `segment`
   (`cfReDeveloperOrChannelPartner`), `cfRequiredTools` (**what sales actually sold** — this is the
   scope contract), `cfHandoverStatus`, `cfOnboardingFeedbackReceived`, `cfActualStartDate`,
   `cfActualGoLiveDate`. Write `deal_fields_RUN_DATE.json`.
   *(58 `get_deal` calls is a lot of context — delegate them to sub-agents in batches of ~18 and have
   each return only the compact JSON.)*
2. `python3 scripts/coverage.py --fields deal_fields_RUN_DATE*.json --data current_data.json --outdir onboarding_reports --date RUN_DATE`

It appends **sheets 13-14** and flags: **CHALLENGE** ("Not required" on a MUST item), **NOT TRACKED**
(blank), **NO LEAD SOURCE** (nothing flowing into the CRM), **SOLD NOT DELIVERED** (on the order form,
never built), **GO-LIVE FICTION**, **PREMATURE HANDOVER**, **NO FEEDBACK**, **STALLED ITEM**.

It also prints the **owner integrity table** — each owner's "Not required" rate vs blank-field rate.
*(13-Jul baseline: Muntazar/Venkat/Sourabh disclaim ~60% of the checklist; Shweta leaves 69% blank.
Different tactics, same effect: a report with nothing red in it. Times Group had lead routing,
pipeline stages AND lead import all marked "Not required" — on a ₹9.4L, 50-licence account.)*

### Step 7 — Build
```
python3 scripts/build_report.py  --data current_data.json --outdir onboarding_reports --date RUN_DATE
python3 scripts/analyze_deep.py  --data current_data.json --outdir onboarding_reports --date RUN_DATE \
                                 --jira onboarding_reports/jira_status_RUN_DATE.json
python3 scripts/coverage.py      --fields onboarding_reports/deal_fields_RUN_DATE*.json \
                                 --data current_data.json --outdir onboarding_reports --date RUN_DATE
```
`build_report.py` writes sheets 1-9 + `snapshot_RUN_DATE.json`.
`analyze_deep.py` appends sheets **10-12**, writes `deep_analysis_RUN_DATE.json`, and generates the
**deep-dive memo scaffold with every number pre-filled**.
`coverage.py` appends sheets **13-14** and writes `coverage_RUN_DATE.json`.

Then recalc with the xlsx skill's `scripts/recalc.py` and confirm **0 errors**.

### Step 8 — Finish the memo and deliver
`analyze_deep.py` leaves two placeholders in the memo: **the asks** and **the paste-ready group
message**. Fill them in yourself — that is the judgement the scripts cannot do.

- **The asks: maximum five.** Each has a named owner and a date. An ask without a name is noise.
- **The paste-ready message: maximum three concerns.** Lead with the reality-check finding if there is one — it is the only thing in the report that nobody in the room already knows.
- Name individuals only where the data is unambiguous, and say so plainly when a person's book is skewed toward older/harder accounts. Flag to Ketan when a finding is pointed enough that he may want a private word before posting it to the group.
- Present the **xlsx and the memo**. Lead the chat summary with: progressed vs stuck, the SUPER-RED count and direction of travel, then the reality-check table.

---

## Movement & escalation rules
- **Moved** = a blocker resolved, a task completed, handed over, or closed.
- **Stuck** = `Same-blocker` or `No-activity`.
- **SUPER-RED** = `stuck_streak >= 2` → row turns red, escalate.
- Moving *into* Pending on Customer / On Hold is **not** progress.
- New deals = "NEW this run". Progress clears any red.

---

## Pitfalls — every one of these has already caught us out

1. **Notes are unsorted and paginated.** Page 1 ≠ newest. Scan every page, take the max epoch. (Step 2.)
2. **A recent note ≠ recent activity.** If the newest note predates the last run, we simply hadn't paged deep enough last time. Nothing happened. `No-activity`.
3. **Note theatre.** Owners re-paste the same "Completed Tasks / Pending Tasks" block weekly with zero delta. Any "has a new note" check reads these as green. `compare.py` scores similarity on the **raw** text — which is why you must store `last_note_raw`.
4. **Ghost JIRA dependencies.** Deals sit for months against tickets that are Done or Won't Fix. Nobody re-reads the ticket. Always fetch it live.
5. **"Pending on Customer" is a parking lot.** Sheet 11 flags every deal in that stage where the customer is *not* actually the blocker. Historically ~5 per run: refund cases, our own QA queue, internal handovers.
6. **Test deals pollute the stats.** "Sell.do test", "test deal Push to OB…" — `analyze_deep.py` excludes anything with "test" in the name. Quote the excluded count so the numbers reconcile.
7. **`billed` is null on ~40% of deals.** Never rank by `billed` alone — use `vband`/`lband` from the live buckets, and report the data gap as a finding.
8. **Scheduled ≠ done.** "Training scheduled Friday" appearing three weeks running is a stuck deal, not an active one.
9. **The stage-flip trap.** An owner can flip a stage without anything changing. Judge on note substance.
10. **Escalations go quiet after the escalation.** The register (sheet 12) tracks days-since-first-flagged and whether the deal has moved *since* — the answer is usually "NO".
11. **Scope disappears rather than fails.** The moment you flag stuck deals, the cheapest fix is to stop tracking the hard items — "Not required", or just leave the field blank. Counting only Completed makes both look fine. Sheets 13-14 exist for this; never report movement without also reporting coverage.
12. **A blank field is worse than an ugly one.** "Waiting on customer" for 60 days is at least visible. A blank is not on anyone's list at all.

## How people behave (read this before judging a note)
- **Effort is reported; outcomes are not.** Notes are dense with activity ("followed up", "call scheduled", "email initiated") and thin on completion. Grade on completion.
- **The blame gradient runs outward.** The default written blocker is the customer, then the vendor, then tech, and almost never the owner. Sheet 11 exists to correct for this. When a note says "awaiting customer feedback", check whether *we* owe them something first — often we do.
- **Silence is the strongest signal.** The deals with no note, no next task, and no stage change are in worse shape than the ones with an ugly note. Ugly notes mean somebody is still engaged.
- **Escalations get logged, not worked.** Once a deal is marked escalated/refund/hold, activity on it typically *stops* — the label feels like the action. Check what happened after the flag, not before.
- **A good owner looks the same as a bad one in the weekly notes.** The separator is the next-task field and completion rate, not note volume. Cross-reference the owner scorecard (sheet 3 / 11) before drawing conclusions about any person.
- **Load is rarely the excuse it appears to be.** Compare owners on progressed-per-deal, not deal count — the highest-throughput owner has typically had a comparable book to the most-stuck one.
- **People manage the metric, not the account.** Whatever you flag, they will optimise. Flag stuck deals → they post a note. Flag missing notes → the note becomes a re-paste. Flag incomplete checklists → items become "Not required" or go blank. Every new check needs its own counter-check, which is why the review reads *movement* (sheets 4/9), *truth* (sheets 10-12) and *coverage* (sheets 13-14) together. A deal that is moving, honest and complete is doing well. Two out of three is a story.

---

## Record schema (per deal)
```
id, name, owner, stage, category(A/B/C/Broker/Push to OB/(none)), suggested, gflag, greason,
vband, lband, brand, billed, recv, lic, idle, age, dsince, cadence,
last_note_epoch, last_note_date, last_note_raw, last_note_text, jira_keys[],
nstep, overdue_golive, not_signedup, high_value, no_task, overdue_task, no_notes,
pending_verdict, pending_action, blocker_owner,
movement_verdict, movement_reason, stuck_streak, restated, note_similarity
```
`blocker_owner` (optional, agent-set) overrides the keyword classifier in `analyze_deep.py`:
`CUSTOMER | US-TECH | US-COMMERCIAL | VENDOR | OWNER-INACTION`.

## Sheets
1. Stats · 2. Exec Summary · 3. Owner Scorecard · 4. **Deal-Level Tracker** (cols E/F = movement flag + prev→now detail, stuck-first) · 5. Large-Stuck-Attention · 6. Pending-on-Customer Check · 7. Customer Category · 8. Re-grade · 9. **Comparison & Movement** · 10. **Reality Check (JIRA)** · 11. **Who's Really Blocking** · 12. **Escalation & Risk Register**

## Notes
- First run is the baseline (no comparison). Comparison is meaningful from run 2.
- `build_report.py` auto-loads the 2 most recent priors; `analyze_deep.py` reads **all** of them (the escalation clock needs the full history).
- Exec-summary and category narratives are hand-written prose; every table, count and date is data-bound.
