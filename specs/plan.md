# Implementation plan — Shift Handoff Log

## Summary

Deliver a local HTTP service backed by SQLite so teammates can record end-of-shift handoffs, query them with filters, and export a markdown briefing for the next shift. Work proceeds in three core tasks (create, list, export) with optional minimal UI afterward. Each task is spec-approved, registered, implemented on its own branch, and merged via PR with AC traceability.

## Plan items

- Implement persistence and `POST /handoffs` for validated handoff records (REQ-HANDOFF-CREATE-1, REQ-HANDOFF-CREATE-2)
- Verify create behavior with automated tests (AC-HANDOFF-CREATE-1, AC-HANDOFF-CREATE-2, AC-HANDOFF-CREATE-3)
- Implement `GET /handoffs` with default ordering, limit, and optional filters (REQ-HANDOFF-LIST-1)
- Verify list and filter behavior with automated tests (AC-HANDOFF-LIST-1, AC-HANDOFF-LIST-2, AC-HANDOFF-LIST-3)
- Implement `GET /handoffs/export` for markdown briefings in a time window (REQ-HANDOFF-EXPORT-1)
- Verify export and empty-window behavior with automated tests (AC-HANDOFF-EXPORT-1, AC-HANDOFF-EXPORT-2)
- Document local run and smoke checks in DEPLOY.md; list demo AC ids in DEMO.md
- Optional: static page for create and list (REQ-HANDOFF-UI-1, AC-HANDOFF-UI-1, AC-HANDOFF-UI-2)

## Traceability

| Plan item | REQ ids | AC ids (verification) |
| --- | --- | --- |
| Create endpoint | REQ-HANDOFF-CREATE-1, REQ-HANDOFF-CREATE-2 | AC-HANDOFF-CREATE-1 … 3 |
| List endpoint | REQ-HANDOFF-LIST-1 | AC-HANDOFF-LIST-1 … 3 |
| Export endpoint | REQ-HANDOFF-EXPORT-1 | AC-HANDOFF-EXPORT-1, AC-HANDOFF-EXPORT-2 |
| Optional UI | REQ-HANDOFF-UI-1 | AC-HANDOFF-UI-1, AC-HANDOFF-UI-2 |

Architecture: Client (CLI, tests, or browser) → FastAPI → SQLite file on disk.
