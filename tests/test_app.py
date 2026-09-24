from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)


def reset_activity_participants(activity_name: str, emails=None):
    if emails is None:
        activities[activity_name]["participants"] = []
    else:
        activities[activity_name]["participants"] = list(emails)


def test_signup_adds_participant_to_activity():
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    reset_activity_participants(activity_name, ["existing@mergington.edu"])

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert email in activities[activity_name]["participants"]
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"


def test_signup_rejects_duplicate_participant():
    # Arrange
    activity_name = "Chess Club"
    email = "existing@mergington.edu"
    reset_activity_participants(activity_name, [email])

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_removes_participant_from_activity():
    # Arrange
    activity_name = "Chess Club"
    email = "student-to-remove@mergington.edu"
    reset_activity_participants(activity_name, [email, "keep@mergington.edu"])

    # Act
    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    # Assert
    assert response.status_code == 200
    assert email not in activities[activity_name]["participants"]
    assert response.json()["message"] == f"Removed {email} from {activity_name}"


def test_unregister_missing_participant_returns_404():
    # Arrange
    activity_name = "Chess Club"
    email = "missing@mergington.edu"
    reset_activity_participants(activity_name, ["keep@mergington.edu"])

    # Act
    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"
