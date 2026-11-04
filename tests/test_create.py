"""AC-HANDOFF-CREATE-1, AC-HANDOFF-CREATE-2, AC-HANDOFF-CREATE-3"""


def test_valid_payload_persisted_with_id(client):
    response = client.post(
        "/handoffs",
        json={
            "author_id": "alex",
            "severity": "warning",
            "summary": "Deploy pipeline still red on staging.",
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["id"]
    assert body["author_id"] == "alex"
    assert body["severity"] == "warning"
    assert body["created_at"]


def test_missing_required_fields_rejected(client):
    response = client.post(
        "/handoffs",
        json={"author_id": "alex", "severity": "info"},
    )
    assert response.status_code == 422


def test_invalid_severity_rejected(client):
    response = client.post(
        "/handoffs",
        json={
            "author_id": "alex",
            "severity": "urgent",
            "summary": "Should not store.",
        },
    )
    assert response.status_code == 422
