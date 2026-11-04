# Two-day hackathon guide: Shift Handoff Log

Participant playbook for building a small project **from scratch** during a hosted hackathon event. You implement the software in **your team repository**; the event platform collects git/forge activity and forward IDE/MCP signals inside the event window.

This guide does **not** ask you to modify the hackathon platform codebase. It gives you a concrete product idea, task breakdown, schedule, and evidence habits aligned with the official starter kit and MCP tools.

**Assumed duration:** about two days (roughly 12–16 hours of team time).  
**Audience:** participants (captains and teammates).

---

## 1. Before you start (about 30 minutes)

Complete these steps **once per event**, before you write application code.

### Event and team

- [ ] Sign in to the event site and complete enrollment (profile, git author email, team join or create).
- [ ] Captain connects the team **repository** on the event **workspace** (read-only forge link is enough for collection).
- [ ] Confirm event dates: commits and PR activity **inside the evidence window** count; work done before the event is not backfilled via MCP.

### Fresh repository for a fresh event

Start a **new** git repository for this event (or an empty default branch). Unpack this **starter kit** archive into the repo root—do not continue a personal debug repo unless your organizers say otherwise.

Files in this archive (same directory as this guide):

| File / folder | Your job |
|---------------|----------|
| [`specs/00-principles.md`](specs/00-principles.md) | Read; align team norms |
| [`specs/plan.md`](specs/plan.md) | Replace all `FILL:` with your plan |
| [`specs/NN-feature.md`](specs/NN-feature.md) | Template only—create **named** spec files per task (see [Task pack](#4-task-pack-3-core--1-optional-stretch)) |
| [`EVAL.md`](EVAL.md) | One row per task **before** implementation |
| [`DEMO.md`](DEMO.md) | Approved AC ids you will show live |
| [`DEPLOY.md`](DEPLOY.md) | Local run / deploy story (no secrets) |
| [`PULL_REQUEST_TEMPLATE.md`](PULL_REQUEST_TEMPLATE.md) | Use for every task PR |
| [`AGENTS.md`](AGENTS.md) | IDE/agent instructions for your repo |

**Rule:** Literal `FILL:` in DEMO, DEPLOY, or unchanged scaffolds is **boilerplate**, not evidence. Replace or remove every `FILL:` you rely on.

### Connect IDE and MCP

- [ ] Captain completes **Connect IDE**, copies the MCP URL and **bearer token** (shown once).
- [ ] In your IDE project (e.g. Cursor), add `.cursor/mcp.json` with the Streamable HTTP MCP URL and the Connect IDE credential in the HTTP Authorization header (organizer docs on the event site).
- [ ] Enable the MCP server; confirm **four tools** appear (not “0 tools”).
- [ ] Grant **IDE / MCP consent** when prompted so forward collection is allowed.

### Git identity

- [ ] Set git `user.email` to the **same email** you declared on the event profile. Mismatched author emails weaken commit linkage.

---

## 2. What you are building

### Project: Shift Handoff Log

**Problem:** Small teams lose context between shifts or focus blocks. Important warnings, unfinished work, and “gotchas” live in chat threads nobody reads.

**Solution:** A minimal **Shift Handoff Log** service where teammates record end-of-shift notes and the next person can list, filter, and export a short **briefing**.

### Users

- Teammates ending a focus block or “shift” who need to log state.
- The next teammate who needs a quick briefing before starting.

### In scope (hackathon bar)

- Create a handoff entry (who, timestamp, severity, summary text).
- List and filter handoffs (time range, severity).
- Export a markdown or JSON briefing for the next shift.
- Optional stretch: tiny read-only UI or single-page form.

### Out of scope (do not spend event time here)

- Multi-tenant SaaS, accounts for external customers, or production SLAs.
- High availability, advanced auth, or compliance certifications.
- Integrating with the hackathon platform’s internal APIs.

---

## 3. Architecture sketch (your choice)

Pick a stack your team knows. **Any language** is fine; the platform scores **spec discipline and evidence**, not framework fashion.

**Reference stack (if you have no preference):**

- **Storage:** SQLite (single file) or JSON file with a simple lock.
- **API:** Small HTTP server (e.g. Python FastAPI, Node Express, Go `net/http`).
- **UI (stretch):** Static HTML + fetch, or CLI only for core tasks.

**Good enough for the event:**

- Runs locally on one machine (`localhost`).
- Data survives restart (file or DB).
- Clear errors for invalid input (400-style behavior).
- One command or script documented in `DEPLOY.md` to start the service.

Draw a one-box diagram on a whiteboard or in `specs/plan.md`: Client → API → Storage.

---

## 4. Task pack (3 core + 1 optional stretch)

Each task follows the **same order**:

1. Write or update the **spec** (REQ/AC ids, status approved).
2. Add a row to **EVAL.md** (human planning—not automatic registration).
3. In the IDE, trigger **`practice.register_task`** **before** the first line of implementation for that task (the MCP client usually does this when you work against the spec; do not skip registration).
4. Implement on a **feature branch**, commit with **Spec:** trailers (see [Git, PRs, and evidence](#7-git-prs-and-evidence)).
5. Open a **PR** using the template; link AC ids and work item if you have one.
6. Optionally record **`sdd_workflow`** stages as you move through specify → slice → verification → demo.

### Task 1 — Create handoff entry

| Field | Value |
|-------|--------|
| Spec file | `specs/handoff-create.md` |
| REQ ids | `REQ-HANDOFF-CREATE-1`, `REQ-HANDOFF-CREATE-2` |
| AC ids | `AC-HANDOFF-CREATE-1`, `AC-HANDOFF-CREATE-2`, `AC-HANDOFF-CREATE-3` |
| Suggested size | **M** |
| Suggested clarity | **2** (after team review) |

**Intent:** Persist a handoff with author id (string), UTC timestamp, severity (`info` \| `warning` \| `critical`), and summary (max length enforced).

**Acceptance criteria (approve in spec before coding):**

- **AC-HANDOFF-CREATE-1:** Valid payload is stored and returns a stable id.
- **AC-HANDOFF-CREATE-2:** Missing required fields return a clear client error without storing partial rows.
- **AC-HANDOFF-CREATE-3:** Severity must be one of the enumerated values; invalid severity is rejected.

**EVAL.md row (example):**

| spec_path | ac_ids | size | clarity |
|-----------|--------|------|---------|
| `specs/handoff-create.md` | `AC-HANDOFF-CREATE-1,AC-HANDOFF-CREATE-2,AC-HANDOFF-CREATE-3` | M | 2 |

**Suggested branch:** `handoff/task1-create`

---

### Task 2 — List and filter handoffs

| Field | Value |
|-------|--------|
| Spec file | `specs/handoff-list.md` |
| REQ ids | `REQ-HANDOFF-LIST-1` |
| AC ids | `AC-HANDOFF-LIST-1`, `AC-HANDOFF-LIST-2`, `AC-HANDOFF-LIST-3` |
| Suggested size | **M** |
| Suggested clarity | **2** |

**Intent:** List handoffs newest-first with optional filters: `since` / `until` (ISO timestamps) and optional severity.

**Acceptance criteria:**

- **AC-HANDOFF-LIST-1:** Default list returns recent entries up to a documented limit.
- **AC-HANDOFF-LIST-2:** Filter by severity returns only matching rows.
- **AC-HANDOFF-LIST-3:** Invalid time parameters return a clear error without 500.

**EVAL.md row:**

| spec_path | ac_ids | size | clarity |
|-----------|--------|------|---------|
| `specs/handoff-list.md` | `AC-HANDOFF-LIST-1,AC-HANDOFF-LIST-2,AC-HANDOFF-LIST-3` | M | 2 |

**Suggested branch:** `handoff/task2-list`

---

### Task 3 — Export shift briefing

| Field | Value |
|-------|--------|
| Spec file | `specs/handoff-export.md` |
| REQ ids | `REQ-HANDOFF-EXPORT-1` |
| AC ids | `AC-HANDOFF-EXPORT-1`, `AC-HANDOFF-EXPORT-2` |
| Suggested size | **S** |
| Suggested clarity | **3** |

**Intent:** Produce a **markdown** (or JSON) document summarizing handoffs in a time window for the “next shift” (title, period, bullet list with severity + summary).

**Acceptance criteria:**

- **AC-HANDOFF-EXPORT-1:** Export for a valid window includes all handoffs in that window in readable order.
- **AC-HANDOFF-EXPORT-2:** Empty window returns an empty briefing structure, not an error.

**EVAL.md row:**

| spec_path | ac_ids | size | clarity |
|-----------|--------|------|---------|
| `specs/handoff-export.md` | `AC-HANDOFF-EXPORT-1,AC-HANDOFF-EXPORT-2` | S | 3 |

**Suggested branch:** `handoff/task3-export`

---

### Task 4 (stretch) — Minimal UI or auth stub

| Field | Value |
|-------|--------|
| Spec file | `specs/handoff-ui.md` |
| REQ ids | `REQ-HANDOFF-UI-1` |
| AC ids | `AC-HANDOFF-UI-1`, `AC-HANDOFF-UI-2` |
| Suggested size | **L** |
| Suggested clarity | **2** |

**Intent:** Single page: form to create a handoff + table of recent rows (read-only list is enough).

**Acceptance criteria:**

- **AC-HANDOFF-UI-1:** User can submit the same fields as Task 1 through the UI.
- **AC-HANDOFF-UI-2:** List view reflects data from Task 2 API (or shared storage).

Skip this task if Tasks 1–3 slip; a CLI-only demo is acceptable.

---

## 5. Two-day schedule (hour blocks)

Adjust to your event clock; keep **register-before-code** invariant each task.

### Day 1

| Block | Focus |
|-------|--------|
| **AM (3–4 h)** | Team kickoff; copy starter kit; fill `specs/plan.md`; write and approve `specs/handoff-create.md`; EVAL row Task 1; **register Task 1**; implement Task 1; PR + merge if ready |
| **PM (3–4 h)** | Spec + EVAL Task 2; register; implement list/filter; PR; start DEMO.md draft (AC ids only, no false claims) |

### Day 2

| Block | Focus |
|-------|--------|
| **AM (3–4 h)** | Spec + EVAL Task 3; register; implement export; PR; optional Task 4 if ahead |
| **PM (3–4 h)** | Finish DEPLOY.md (local run); rehearse demo; fill DEMO.md; retro declarations if your event uses them; buffer before `evidence_window_end` |

Leave the last **30–60 minutes** for demo polish and ensuring MCP stays connected—do not start a new spec in the final hour.

---

## 6. MCP and IDE habits

The hosted server exposes exactly four MCP tools:

| Tool | When you use it |
|------|------------------|
| `practice.register_task` | **Before** first implementation commit for each EVAL row |
| `sdd_workflow` | When entering a workflow stage (specify, design, slice, verification, demo, etc.) |
| `practice.mark_blended` | When you mix ad-hoc AI prompts with spec-grounded work on a task |
| `practice.event_status` | Optional connectivity check—not scored |

**Habits:**

- Use a stable **`client_request_id`** per task (e.g. `handoff-task1-create`) so idempotent registration replays cleanly.
- Do **not** put secrets, tokens, or private payloads in tool arguments.
- If MCP disconnects after idle, toggle the server off/on in IDE settings; collection is **forward-only** and does not backfill missed intervals.
- Continue normal development if a tool call fails once; fix MCP and keep working— but registration before code is worth getting right.


---

## 7. Git, PRs, and evidence

### Commits

- One task per branch when possible; imperative subject (e.g. `Handoff: implement create endpoint`).
- After successful **`register_task`**, use commit **trailers** the platform returns at registration when present:

```text
Spec: specs/handoff-create.md#AC-HANDOFF-CREATE-1
Spec: specs/handoff-create.md#AC-HANDOFF-CREATE-2
Practice: sdd
```

(`Practice:` line depends on your assigned arm; follow the trailer lines returned at registration when present.)

### Pull requests

Use [`PULL_REQUEST_TEMPLATE.md`](PULL_REQUEST_TEMPLATE.md):

- Checklist every **AC** this PR satisfies.
- **Work item:** tracker URL or key if you use one; otherwise state “N/A – hackathon repo only”.
- **Not in spec:** one honest line if you had to deviate.

### What the platform collects

- **Git/forge:** commits and PRs in the connected repo during the event window.
- **MCP:** IDE events **after** connect and consent, forward from registration and workflow tools.
- **My data (UI):** MCP metadata you can inspect; not a full code dump.

Past work before connect or outside the window is not imported via MCP.

---

## 8. Demo script (5–7 minutes)

Rehearse this once with `DEMO.md` open. Only claim AC ids listed there.

1. **Setup (30 s):** Show service running locally (command from `DEPLOY.md`); optional: workspace shows repo connected / fresh commit.
2. **Create (1 min):** Add a handoff with `warning` severity and a realistic summary (**AC-HANDOFF-CREATE-***).
3. **List (1 min):** Show default list and severity filter (**AC-HANDOFF-LIST-***).
4. **Export (1 min):** Generate briefing markdown for “last 24 hours” (**AC-HANDOFF-EXPORT-***).
5. **Traceability (1 min):** Show one merged PR with AC checklist and `Spec:` trailers in commits.
6. **Optional (1 min):** Stretch UI or show **My data** / MCP connection status if organizers ask.

If something fails live, explain which AC is blocked—do not claim demo coverage you did not show.

---

## 9. Definition of done checklist

Use this before you consider the hackathon project “submitted”:

- [ ] Every spec used for coding is **approved** (no `FILL:` in requirements or AC sections).
- [ ] **EVAL.md** has one row per implemented task with final size/clarity.
- [ ] Each implemented task was **`register_task`’d before** its first implementation commit.
- [ ] **DEMO.md** lists only AC ids you actually demonstrated.
- [ ] **DEPLOY.md** describes how to run locally without secrets; `FILL:` removed or N/A sections explained.
- [ ] At least **one PR per core task** (1–3) with template filled and AC boxes checked honestly.
- [ ] Commits in the event window use correct **author email** and **Spec:** trailers where registration provided them.
- [ ] MCP stayed connected during active IDE work, or you reconnected and continued with registration on new tasks.
- [ ] Team retro / declarations completed if the event requires them (before assessment window closes).

---

## 10. Pitfalls

| Pitfall | Why it hurts | What to do |
|---------|----------------|------------|
| Leaving `FILL:` in DEMO/DEPLOY | Extractors treat as boilerplate; demo/deploy claims don’t count | Replace every placeholder you depend on |
| Coding before `register_task` | Weak task linkage and trailer guidance | Register, then implement |
| Wrong git email | Commits won’t link to your participant identity | Match profile email |
| MCP disconnected for hours | Gap in forward IDE evidence | Re-enable MCP; don’t assume backfill |
| Claiming AC in DEMO without showing it | Assessment/demo mismatch | Demo only listed AC ids |
| One giant PR for all tasks | Hard to review and trace | Prefer one PR per task |
| Secrets in repo or MCP args | Security and disqualification risk | Use env vars locally; never commit tokens |

---

## 11. Appendix: REQ/AC id master list

Copy these ids consistently across specs, EVAL, DEMO, PR checklists, and commit trailers.

### `specs/handoff-create.md`

- REQ-HANDOFF-CREATE-1 — Store handoff record  
- REQ-HANDOFF-CREATE-2 — Validate input  
- AC-HANDOFF-CREATE-1 — Valid payload persisted with id  
- AC-HANDOFF-CREATE-2 — Missing fields rejected  
- AC-HANDOFF-CREATE-3 — Invalid severity rejected  

### `specs/handoff-list.md`

- REQ-HANDOFF-LIST-1 — Query handoffs  
- AC-HANDOFF-LIST-1 — Default recent list  
- AC-HANDOFF-LIST-2 — Severity filter  
- AC-HANDOFF-LIST-3 — Invalid time params rejected  

### `specs/handoff-export.md`

- REQ-HANDOFF-EXPORT-1 — Briefing export  
- AC-HANDOFF-EXPORT-1 — Window export content  
- AC-HANDOFF-EXPORT-2 — Empty window behavior  

### `specs/handoff-ui.md` (stretch)

- REQ-HANDOFF-UI-1 — Minimal UI  
- AC-HANDOFF-UI-1 — Create via UI  
- AC-HANDOFF-UI-2 — List via UI  

### Suggested DEMO.md AC list (core demo)

- AC-HANDOFF-CREATE-1  
- AC-HANDOFF-LIST-1  
- AC-HANDOFF-LIST-2  
- AC-HANDOFF-EXPORT-1  

---

---

*Document version: participant guide for Shift Handoff Log (two-day event). Shipped in the hosted starter kit archive.*
