def test_root_redirects_to_static_index(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_expected_structure(client):
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data

    sample_activity = next(iter(data.values()))
    assert isinstance(sample_activity, dict)
    assert {
        "description",
        "schedule",
        "max_participants",
        "participants",
    }.issubset(sample_activity.keys())
    assert isinstance(sample_activity["participants"], list)
