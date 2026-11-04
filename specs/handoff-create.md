# Handoff create

## Status

approved

## Intent

Teammates ending a focus block need to persist a structured handoff so the next person sees who left the note, when, how urgent it is, and a short summary.

## Requirements

- REQ-HANDOFF-CREATE-1 — The service stores a handoff record with author id, UTC timestamp, severity, and summary text.
- REQ-HANDOFF-CREATE-2 — The service validates required fields and enumerated severity before persisting.

## Acceptance criteria

- AC-HANDOFF-CREATE-1 — A valid JSON payload is stored and the response includes a stable string id for the new row.
- AC-HANDOFF-CREATE-2 — Missing any required field (`author_id`, `severity`, `summary`) returns HTTP 422 and does not insert a partial row.
- AC-HANDOFF-CREATE-3 — Severity must be exactly `info`, `warning`, or `critical`; any other value returns HTTP 422 without storing.

## API

- `POST /handoffs`
- Request body: `{ "author_id": string, "severity": "info"|"warning"|"critical", "summary": string }` (max 2000 characters for summary)
- Server sets `created_at` to current UTC ISO-8601 if not supplied; clients may omit timestamp.
- Success: HTTP 201 with `{ "id": string, "author_id", "severity", "summary", "created_at" }`

## Out of scope

- Authentication and multi-user identity providers
- Attachments or rich text

## Open questions

- None for hackathon scope.

## Amendments

- 2026-11-04 — Initial approval for Task 1.
