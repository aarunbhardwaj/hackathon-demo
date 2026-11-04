import sqlite3
from pathlib import Path
from typing import Optional

from app.models import HandoffRecord

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
