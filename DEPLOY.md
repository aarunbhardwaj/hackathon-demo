# Deploy — local Shift Handoff Log

## Deployment target

Single-machine **local** run for hackathon demo. SQLite file `handoffs.db` is created in the repository root on first start.

## Workflow

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Optional UI: open `http://127.0.0.1:8000/` after Task 4 static assets are present.

## Verification

Example checks (run after the server is up):

- Smoke: `curl -s http://127.0.0.1:8000/health` returns `{"status":"ok"}`.
- Create smoke: `curl -s -X POST http://127.0.0.1:8000/handoffs -H 'Content-Type: application/json' -d '{"author_id":"demo","severity":"info","summary":"Smoke test"}'` returns HTTP 201 with an `id`.
- Post-deploy: run `pytest -q` in another terminal with the venv activated.

## Rollback

Stop uvicorn (Ctrl+C). Remove `handoffs.db` to reset stored handoffs; reinstall dependencies only if `requirements.txt` changed.

## Linked acceptance criteria

- AC-HANDOFF-CREATE-1 — Service accepts create via HTTP
- AC-HANDOFF-LIST-1 — List endpoint available on same process
- AC-HANDOFF-EXPORT-1 — Export endpoint available on same process
- AC-HANDOFF-UI-1 — Static UI served from `/` when enabled
