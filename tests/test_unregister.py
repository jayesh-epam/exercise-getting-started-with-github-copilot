from urllib.parse import quote


def test_unregister_successfully_removes_participant(client):
    activity = "Chess Club"
    email = "daniel@mergington.edu"

    response = client.delete(f"/activities/{quote(activity, safe='')}/participants/{quote(email, safe='')}")

    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity}"

    activities_response = client.get("/activities")
    participants = activities_response.json()[activity]["participants"]
    assert email not in participants


def test_unregister_fails_for_unknown_activity(client):
    response = client.delete(
        f"/activities/{quote('Unknown Activity', safe='')}/participants/{quote('student@mergington.edu', safe='')}"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_fails_for_non_registered_participant(client):
    activity = "Chess Club"
    email = "not.registered@mergington.edu"

    response = client.delete(f"/activities/{quote(activity, safe='')}/participants/{quote(email, safe='')}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_unregister_handles_url_encoded_email_path_parameter(client):
    activity = "Programming Class"
    email = "student+coding@mergington.edu"

    signup_response = client.post(f"/activities/{quote(activity, safe='')}/signup", params={"email": email})
    assert signup_response.status_code == 200

    unregister_response = client.delete(
        f"/activities/{quote(activity, safe='')}/participants/{quote(email, safe='')}"
    )
    assert unregister_response.status_code == 200

    activities_response = client.get("/activities")
    participants = activities_response.json()[activity]["participants"]
    assert email not in participants