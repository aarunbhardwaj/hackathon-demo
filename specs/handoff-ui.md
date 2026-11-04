# Minimal handoff UI

## Status

approved

## Intent

Teammates who prefer a browser can submit handoffs and skim recent entries without using curl.

## Requirements

- REQ-HANDOFF-UI-1 — A single static page creates handoffs and shows recent rows via the existing API.

## Acceptance criteria

- AC-HANDOFF-UI-1 — The page form submits the same fields as Task 1 (`author_id`, `severity`, `summary`) to `POST /handoffs` and shows success or validation errors.
- AC-HANDOFF-UI-2 — The page loads recent handoffs from `GET /handoffs` and renders author, severity, summary, and timestamp.

## Out of scope

- Client-side routing and authentication

## Open questions

- None.

## Amendments

- 2026-11-04 — Initial approval for Task 4 stretch.
