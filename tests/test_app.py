from fastapi.testclient import TestClient
from src.app_clean import app, activities

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # Expect at least one known activity from sample data
    assert "Chess Club" in data


def test_signup_and_unregister_flow():
    # Create a temporary activity for isolation
    activities["Test Activity"] = {
        "description": "Temporary activity for tests",
        "schedule": "Now",
        "max_participants": 5,
        "participants": [],
    }

    # Successful signup
    r = client.post("/activities/Test Activity/signup?email=test_user@example.com")
    assert r.status_code == 200
    assert "Signed up test_user@example.com" in r.json()["message"]

    # Duplicate signup should fail
    r2 = client.post("/activities/Test Activity/signup?email=test_user@example.com")
    assert r2.status_code == 400

    # Unregister the participant
    r3 = client.post("/activities/Test Activity/unregister?email=test_user@example.com")
    assert r3.status_code == 200
    assert "Unregistered test_user@example.com" in r3.json()["message"]

    # Unregistering a non-existent participant should return 400
    r4 = client.post("/activities/Test Activity/unregister?email=not_here@example.com")
    assert r4.status_code == 400

    # Clean up
    del activities["Test Activity"]


def test_invalid_activity_endpoints():
    # Signup to non-existing activity
    r = client.post("/activities/NoSuchActivity/signup?email=a@b.com")
    assert r.status_code == 404

    # Unregister from non-existing activity
    r2 = client.post("/activities/NoSuchActivity/unregister?email=a@b.com")
    assert r2.status_code == 404
import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_read_root():
    """Test that the root endpoint redirects to index.html"""
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307  # FastAPI uses 307 Temporary Redirect
    assert response.headers["location"] == "/static/index.html"

def test_get_activities():
    """Test getting all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    activities = response.json()
    assert isinstance(activities, dict)
    assert "Chess Club" in activities
    assert "Programming Class" in activities
from fastapi.testclient import TestClient
from src.app_clean import app, activities

client = TestClient(app)


def test_read_root_redirect():
    resp = client.get("/", follow_redirects=False)
    # FastAPI/Starlette uses 307 Temporary Redirect for path operations
    assert resp.status_code == 307
    assert resp.headers["location"] == "/static/index.html"


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_and_unregister_flow():
    # Isolated temporary activity
    activities["Test Activity"] = {
        "description": "Temporary activity for tests",
        "schedule": "Now",
        "max_participants": 5,
        "participants": [],
    }

    # Sign up
    r = client.post("/activities/Test Activity/signup?email=test_user@example.com")
    assert r.status_code == 200
    assert "Signed up test_user@example.com" in r.json()["message"]

    # Duplicate signup fails
    r2 = client.post("/activities/Test Activity/signup?email=test_user@example.com")
    assert r2.status_code == 400

    # Unregister
    r3 = client.post("/activities/Test Activity/unregister?email=test_user@example.com")
    assert r3.status_code == 200
    assert "Unregistered test_user@example.com" in r3.json()["message"]

    # Unregister non-existent participant
    r4 = client.post("/activities/Test Activity/unregister?email=not_here@example.com")
    assert r4.status_code == 400

    del activities["Test Activity"]


def test_signup_nonexistent_activity():
    r = client.post("/activities/NoSuchActivity/signup?email=a@b.com")
    assert r.status_code == 404


def test_unregister_nonexistent_activity():
    r = client.post("/activities/NoSuchActivity/unregister?email=a@b.com")
    assert r.status_code == 404
