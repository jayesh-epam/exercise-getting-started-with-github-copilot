def test_get_activities_returns_expected_shape(client):
    response = client.get("/activities")

    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, dict)
    assert len(payload) > 0

    required_keys = {"description", "schedule", "max_participants", "participants"}
    for _, details in payload.items():
        assert required_keys.issubset(details.keys())
        assert isinstance(details["participants"], list)