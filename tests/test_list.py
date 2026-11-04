"""AC-HANDOFF-LIST-1, AC-HANDOFF-LIST-2, AC-HANDOFF-LIST-3"""

import time


def _create(client, author: str, severity: str, summary: str):
    return client.post(
        "/handoffs",
        json={"author_id": author, "severity": severity, "summary": summary},
    )


def test_default_list_newest_first(client):
    _create(client, "a", "info", "first")
    time.sleep(0.01)
    _create(client, "b", "warning", "second")
    response = client.get("/handoffs")
    assert response.status_code == 200
    items = response.json()
    assert len(items) == 2
    assert items[0]["summary"] == "second"
    assert items[1]["summary"] == "first"


def test_severity_filter(client):
    _create(client, "a", "info", "low")
    _create(client, "b", "critical", "high")
    response = client.get("/handoffs", params={"severity": "critical"})
    assert response.status_code == 200
    items = response.json()
    assert len(items) == 1
    assert items[0]["severity"] == "critical"


def test_invalid_since_rejected(client):
    response = client.get("/handoffs", params={"since": "not-a-date"})
    assert response.status_code == 422
