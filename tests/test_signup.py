import src.app as app_module


def test_signup_success_adds_participant(client):
    activity_name = "Chess Club"
    email = "new_student@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
    assert email in app_module.activities[activity_name]["participants"]


def test_signup_unknown_activity_returns_404(client):
    response = client.post(
        "/activities/Unknown%20Club/signup", params={"email": "student@mergington.edu"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_duplicate_returns_400(client):
    activity_name = "Chess Club"
    existing_email = app_module.activities[activity_name]["participants"][0]

    response = client.post(
        f"/activities/{activity_name}/signup", params={"email": existing_email}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_full_activity_returns_400(client):
    activity_name = "Full Club"
    app_module.activities[activity_name] = {
        "description": "Already at capacity",
        "schedule": "Fridays, 1:00 PM - 2:00 PM",
        "max_participants": 1,
        "participants": ["full@mergington.edu"],
    }

    response = client.post(
        f"/activities/{activity_name}/signup", params={"email": "new@mergington.edu"}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Activity is full"
