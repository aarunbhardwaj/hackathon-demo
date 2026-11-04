"""AC-HANDOFF-UI-1, AC-HANDOFF-UI-2 — static shell served at root."""


def test_index_page_served(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Shift Handoff Log" in response.text
    assert 'id="create-form"' in response.text
