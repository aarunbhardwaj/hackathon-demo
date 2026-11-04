import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional

from app.models import HandoffRecord, Severity

DEFAULT_DB = Path(__file__).resolve().parent.parent / "handoffs.db"


def connect(db_path: Optional[Path] = None) -> sqlite3.Connection:
    path = db_path or DEFAULT_DB
    conn = sqlite3.connect(path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS handoffs (
            id TEXT PRIMARY KEY,
            author_id TEXT NOT NULL,
            severity TEXT NOT NULL,
            summary TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )
    conn.commit()


def insert_handoff(conn: sqlite3.Connection, record: HandoffRecord) -> HandoffRecord:
    conn.execute(
        """
        INSERT INTO handoffs (id, author_id, severity, summary, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            record.id,
            record.author_id,
            record.severity,
            record.summary,
            record.created_at.isoformat(),
        ),
    )
    conn.commit()
    return record


def _row_to_record(row: sqlite3.Row) -> HandoffRecord:
    return HandoffRecord(
        id=row["id"],
        author_id=row["author_id"],
        severity=row["severity"],
        summary=row["summary"],
        created_at=datetime.fromisoformat(row["created_at"]),
    )


def list_handoffs(
    conn: sqlite3.Connection,
    *,
    since: Optional[datetime] = None,
    until: Optional[datetime] = None,
    severity: Optional[Severity] = None,
    limit: int = 50,
    ascending: bool = False,
) -> list[HandoffRecord]:
    clauses: list[str] = []
    params: list[object] = []

    if since is not None:
        clauses.append("created_at >= ?")
        params.append(since.isoformat())
    if until is not None:
        clauses.append("created_at <= ?")
        params.append(until.isoformat())
    if severity is not None:
        clauses.append("severity = ?")
        params.append(severity)

    where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
    params.append(limit)
    query = f"""
        SELECT id, author_id, severity, summary, created_at
        FROM handoffs
        {where}
        ORDER BY created_at {'ASC' if ascending else 'DESC'}
        LIMIT ?
    """
    rows = conn.execute(query, params).fetchall()
    return [_row_to_record(row) for row in rows]
