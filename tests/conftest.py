import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.store import connect, init_db


@pytest.fixture
def client():
    with tempfile.TemporaryDirectory() as tmp:
        db_path = Path(tmp) / "test.db"
        conn = connect(db_path)
        init_db(conn)
        app.state.db = conn
        with TestClient(app) as c:
            yield c
        conn.close()
