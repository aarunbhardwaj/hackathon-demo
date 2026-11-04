"""AC-HANDOFF-EXPORT-1, AC-HANDOFF-EXPORT-2"""

from datetime import datetime, timedelta, timezone


def test_export_includes_window_entries(client):
    create = client.post(
        "/handoffs",
        json={
            "author_id": "sam",
            "severity": "warning",
            "summary": "Check logs before deploy.",
        },
    )
    assert create.status_code == 201
    now = datetime.now(timezone.utc)
    since = (now - timedelta(hours=1)).isoformat()
    until = (now + timedelta(hours=1)).isoformat()
    response = client.get("/handoffs/export", params={"since": since, "until": until})
    assert response.status_code == 200
    body = response.json()
    assert len(body["items"]) == 1
    assert "Check logs before deploy" in body["markdown"]
    assert body["items"][0]["author_id"] == "sam"


def test_export_empty_window(client):
    now = datetime.now(timezone.utc)
    since = (now + timedelta(days=1)).isoformat()
    until = (now + timedelta(days=2)).isoformat()
    response = client.get("/handoffs/export", params={"since": since, "until": until})
    assert response.status_code == 200
    body = response.json()
    assert body["items"] == []
    assert "No handoffs" in body["markdown"]
