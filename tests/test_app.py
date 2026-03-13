import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

# Helper to reset activities for test isolation
def reset_activities():
    for activity in activities.values():
        activity["participants"] = [p for p in activity["participants"] if p.endswith("@mergington.edu")]

@pytest.fixture(autouse=True)
def setup_and_teardown():
    reset_activities()
    yield
    reset_activities()


def test_get_activities():
    # Arrange: None needed
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert "Chess Club" in response.json()


def test_signup_success():
    # Arrange
    email = "newstudent@mergington.edu"
    activity = "Chess Club"
    assert email not in activities[activity]["participants"]
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert response.status_code == 200
    assert email in activities[activity]["participants"]
    assert response.json()["message"] == f"Signed up {email} for {activity}"


def test_signup_duplicate():
    # Arrange
    activity = "Chess Club"
    email = activities[activity]["participants"][0]
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_signup_activity_not_found():
    # Arrange
    email = "ghost@mergington.edu"
    activity = "Nonexistent"
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_success():
    # Arrange
    activity = "Chess Club"
    email = activities[activity]["participants"][0]
    # Act
    response = client.post(f"/activities/{activity}/unregister", params={"email": email})
    # Assert
    assert response.status_code == 200
    assert email not in activities[activity]["participants"]
    assert response.json()["message"] == f"Removed {email} from {activity}"


def test_unregister_not_found():
    # Arrange
    activity = "Chess Club"
    email = "notfound@mergington.edu"
    assert email not in activities[activity]["participants"]
    # Act
    response = client.post(f"/activities/{activity}/unregister", params={"email": email})
    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Participant not found in this activity"


def test_unregister_activity_not_found():
    # Arrange
    email = "ghost@mergington.edu"
    activity = "Nonexistent"
    # Act
    response = client.post(f"/activities/{activity}/unregister", params={"email": email})
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
