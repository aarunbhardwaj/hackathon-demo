from datetime import datetime, timezone
from typing import Literal
from uuid import uuid4

from pydantic import BaseModel, Field, field_validator

Severity = Literal["info", "warning", "critical"]
SUMMARY_MAX_LEN = 2000


class HandoffCreate(BaseModel):
    author_id: str = Field(min_length=1, max_length=200)
    severity: Severity
    summary: str = Field(min_length=1, max_length=SUMMARY_MAX_LEN)


class HandoffRecord(BaseModel):
    id: str
    author_id: str
    severity: Severity
    summary: str
    created_at: datetime

    @classmethod
    def from_create(cls, payload: HandoffCreate) -> "HandoffRecord":
        return cls(
            id=str(uuid4()),
            author_id=payload.author_id,
            severity=payload.severity,
            summary=payload.summary,
            created_at=datetime.now(timezone.utc),
        )
