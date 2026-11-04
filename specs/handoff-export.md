# Handoff export briefing

## Status

approved

## Intent

The incoming shift lead wants a single markdown document summarizing handoffs in a chosen time window.

## Requirements

- REQ-HANDOFF-EXPORT-1 — The service produces a markdown briefing for handoffs within a requested time window.

## Acceptance criteria

- AC-HANDOFF-EXPORT-1 — For valid `since` and `until`, the export includes every handoff in that window, ordered oldest to newest in the body, with title and period header.
- AC-HANDOFF-EXPORT-2 — When no handoffs fall in the window, the response is HTTP 200 with an empty items list and a markdown body stating no entries (not an error).

## API

- `GET /handoffs/export?since=<iso>&until=<iso>`
- Response JSON: `{ "format": "markdown", "since", "until", "items": [...], "markdown": string }`

## Out of scope

- PDF or email delivery

## Open questions

- None.

## Amendments

- 2026-11-04 — Initial approval for Task 3.
