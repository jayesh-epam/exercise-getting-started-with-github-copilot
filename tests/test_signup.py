from urllib.parse import quote


def test_signup_successfully_adds_participant(client):
    activity = "Chess Club"
    email = "newstudent@mergington.edu"

    response = client.post(f"/activities/{quote(activity, safe='')}/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity}"

    activities_response = client.get("/activities")
    participants = activities_response.json()[activity]["participants"]
    assert email in participants


def test_signup_fails_for_unknown_activity(client):
    response = client.post("/activities/Unknown%20Activity/signup", params={"email": "student@mergington.edu"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_fails_for_duplicate_participant(client):
    activity = "Chess Club"
    existing_email = "michael@mergington.edu"

    response = client.post(f"/activities/{quote(activity, safe='')}/signup", params={"email": existing_email})

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_handles_url_encoded_email_values(client):
    activity = "Science Club"
    email = "student+robotics@mergington.edu"

    response = client.post(f"/activities/{quote(activity, safe='')}/signup", params={"email": email})

    assert response.status_code == 200

    activities_response = client.get("/activities")
    participants = activities_response.json()[activity]["participants"]
    assert email in participants