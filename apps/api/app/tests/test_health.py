from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

EXPECTED = {
    "success": True,
    "message": "ExamFlow API is running",
    "service": "ExamFlow by M.B. Technosoft Pvt Ltd",
    "version": "0.1.0",
    "environment": "development",
}


def test_root_health_response():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == EXPECTED


def test_health_response():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == EXPECTED


def test_v1_health_response():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == EXPECTED
