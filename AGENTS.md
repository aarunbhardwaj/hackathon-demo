# MCP collection contract

This document is loaded by the hosted hackathon application. It is not installed on a developer machine and is not read by a local IDE agent at runtime. It defines what the hosted MCP server **stores** when the IDE MCP client sends the four collection tools.

## Scope

- **Collection only.** Accepted tool calls become stored MCP events. They do not score practice, assign tiers, or publish markers. No stored call by itself proves practice or changes a score.
- **Evaluation later.** Practice judgments run on the server after stored MCP and repository evidence exist, using the separate evaluation policy in `specs/00-principles.md`.

## Four collection tools

When the IDE MCP client invokes a tool, the server validates input, applies idempotency, redacts or rejects oversize arguments, persists an `IDEEvent`, and returns the logical result. Triggers match BUILD AC-3.15:

1. **`practice.event_status`** — at IDE session start (after successful initialize). Connection lifecycle and status calls are instrumentation; they are not scored.
2. **`practice.register_task`** — when an unregistered `EVAL.md` row is first encountered **before** the first implementation action for that task. Registration of a `human` task is not AI assistance.
3. **`sdd_workflow`** — before each AI interaction for the active task, including stage `deploy` before deploy-related AI interaction.
4. **`practice.mark_blended`** — when both spec-context and free-form AI interactions occur on the same task.

Participants work normally in the IDE. The workspace has no participant-operated register, sync, or workflow controls.

### Stored semantics (registration and workflow)

**`practice.register_task`** persists the task, criterion links, and zero or one immutable original arm assignment when the team enabled arm bonus before IDE connection. The tool result includes **`trailer_lines`**: one `Spec: <spec_path>#<AC-id>` line per registered criterion and, when an original arm exists, one `Practice: <original-arm>` line. Replaying the same `client_request_id` returns byte-identical `trailer_lines`. The IDE MCP client adds those lines to commits it creates for that task; the team workspace may display task, arm, and trailers for visibility only.

**`sdd_workflow`** records workflow stage timing for the active task. Stage `deploy` requires a `task_id`. When `task_id` is present, `interaction_kind` must be `initial` or `reprompt`. Stage `reflect` may omit spec references. Deploy calls provide workflow context only; they do not assert that a deployment ran.

**`practice.mark_blended`** requires an existing task and a nonempty reason. The server appends contamination history and sets the task effective arm to `half-sdd` without redrawing the original assignment or rewriting stored registration trailer guidance.

## Retry and failure

- On one transient HTTP **429** or **5xx**, the IDE client may retry **once** with the **same idempotency identity**.
- Validation, authentication, consent, and policy failures are terminal and are not retried.
- A failed automatic call must not block IDE work. Continued failure surfaces `Assessment sync delayed`; dependent signals may become `unobservable`, not zero.

## Argument privacy

Tool arguments must not contain secrets, credentials, personal data, raw logs, unrelated prompt dumps, or private evidence. The prompt bundle never contains an event URL, bearer token, tenant id, participant id, repository credential, or provider secret.

## Non-goals

This contract does not embed MCP configuration, assign arms outside registration, compute rubric formulas, or instruct anyone to download or execute a starter archive on a laptop.
