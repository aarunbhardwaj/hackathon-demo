# Handoff list and filter

## Status

approved

## Intent

The next teammate needs to see recent handoffs and narrow them by time range or severity without reading the full history.

## Requirements

- REQ-HANDOFF-LIST-1 — The service lists stored handoffs newest-first with optional filters.

## Acceptance criteria

- AC-HANDOFF-LIST-1 — `GET /handoffs` with no filters returns up to 50 entries ordered by `created_at` descending.
- AC-HANDOFF-LIST-2 — Optional query parameter `severity` returns only rows matching that severity.
- AC-HANDOFF-LIST-3 — Invalid `since` or `until` ISO-8601 values return HTTP 422 without a server error.

## API

- `GET /handoffs?since=&until=&severity=&limit=`
- `limit` defaults to 50, max 200.
- `since` / `until` are inclusive bounds on `created_at` (UTC).

## Out of scope

- Full-text search on summary
- Cursor-based pagination beyond limit cap

## Open questions

- None.

## Amendments

- 2026-11-04 — Initial approval for Task 2.
