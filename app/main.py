from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path
from typing import Annotated, Literal, Optional

from fastapi import FastAPI, Query, Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse

from app.models import HandoffCreate, HandoffRecord, Severity
from app.store import connect, init_db, insert_handoff, list_handoffs

DB_PATH = Path(__file__).resolve().parent.parent / "handoffs.db"


@asynccontextmanager
async def lifespan(app: FastAPI):
    conn = connect(DB_PATH)
    init_db(conn)
    app.state.db = conn
    yield
    conn.close()


app = FastAPI(title="Shift Handoff Log", lifespan=lifespan)


@app.post("/handoffs", status_code=201)
def create_handoff(payload: HandoffCreate) -> HandoffRecord:
    record = HandoffRecord.from_create(payload)
    insert_handoff(app.state.db, record)
    return record


def _parse_iso(param: str, name: str) -> datetime:
    try:
        return datetime.fromisoformat(param.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"Invalid {name}: expected ISO-8601 timestamp") from exc


@app.get("/handoffs")
def get_handoffs(
    since: Optional[str] = None,
    until: Optional[str] = None,
    severity: Optional[Severity] = None,
    limit: Annotated[int, Query(ge=1, le=200)] = 50,
) -> list[HandoffRecord]:
    since_dt = _parse_iso(since, "since") if since else None
    until_dt = _parse_iso(until, "until") if until else None
    return list_handoffs(
        app.state.db,
        since=since_dt,
        until=until_dt,
        severity=severity,
        limit=limit,
    )


@app.exception_handler(ValueError)
async def value_error_handler(_request: Request, exc: ValueError):
    return JSONResponse(status_code=422, content={"detail": str(exc)})


class ExportResponse(BaseModel):
    format: Literal["markdown"]
    since: datetime
    until: datetime
    items: list[HandoffRecord]
    markdown: str


def _build_markdown(since: datetime, until: datetime, items: list[HandoffRecord]) -> str:
    lines = [
        "# Shift handoff briefing",
        "",
        f"**Period:** {since.isoformat()} — {until.isoformat()}",
        "",
    ]
    if not items:
        lines.append("_No handoffs in this window._")
    else:
        for item in items:
            lines.append(
                f"- **{item.severity}** ({item.author_id}, "
                f"{item.created_at.isoformat()}): {item.summary}"
            )
    return "\n".join(lines)


@app.get("/handoffs/export")
def export_handoffs(since: str, until: str) -> ExportResponse:
    since_dt = _parse_iso(since, "since")
    until_dt = _parse_iso(until, "until")
    items = list_handoffs(
        app.state.db,
        since=since_dt,
        until=until_dt,
        limit=200,
        ascending=True,
    )
    markdown = _build_markdown(since_dt, until_dt, items)
    return ExportResponse(
        format="markdown",
        since=since_dt,
        until=until_dt,
        items=items,
        markdown=markdown,
    )


@app.get("/health")
def health():
    return {"status": "ok"}
