# Demo — Shift Handoff Log

## Purpose

Show a local Shift Handoff Log: create a handoff, list with severity filter, and export a markdown briefing for the next shift.

## Approved acceptance criteria to demonstrate

- AC-HANDOFF-CREATE-1 — Valid handoff stored with stable id
- AC-HANDOFF-LIST-1 — Default list shows recent entries newest-first
- AC-HANDOFF-LIST-2 — Severity filter returns matching rows only
- AC-HANDOFF-EXPORT-1 — Export for a valid time window includes in-window handoffs

## Demo notes

1. Start the API per [DEPLOY.md](DEPLOY.md) (`http://127.0.0.1:8000`).
2. Create a handoff with `warning` severity via UI at `/` or `POST /handoffs`.
3. Open list view or `GET /handoffs?severity=warning`.
4. Call `GET /handoffs/export?since=...&until=...` for the last 24 hours and show markdown.
5. Optional: show a merged PR checklist with `Spec:` commit trailers.
