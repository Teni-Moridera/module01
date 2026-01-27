from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def sample_payload():
    return {
        "students": [
            {
                "id": 1,
                "name": "Ivanov",
                "group": "PR-21",
                "grades": [
                    {"subject": "Math", "score": 80, "date": "2025-12-15"},
                    {"subject": "CS", "score": 90, "date": "2025-12-18"},
                ],
            }
        ]
    }


def test_upload_and_statistics():
    response = client.post("/api/upload/json", json=sample_payload())
    assert response.status_code == 200

    stats = client.get("/api/statistics")
    assert stats.status_code == 200
    data = stats.json()
    assert data["student_count"] == 1
    assert data["average_score"] == 85


def test_export_json():
    client.post("/api/upload/json", json=sample_payload())
    response = client.get("/api/export/json")
    assert response.status_code == 200
    data = response.json()
    assert data["format"] == "json"
