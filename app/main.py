from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.models import HandoffCreate, HandoffRecord
from app.store import connect, init_db, insert_handoff

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


@app.exception_handler(ValueError)
async def value_error_handler(_request: Request, exc: ValueError):
    return JSONResponse(status_code=422, content={"detail": str(exc)})
