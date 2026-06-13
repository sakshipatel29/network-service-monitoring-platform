from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "Network Service Monitoring Platform is running"


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert response.json()["service"] == "network-monitoring-api"


def test_metrics_endpoint():
    response = client.get("/metrics")

    assert response.status_code == 200
    assert "service_check_total" in response.text
    assert "service_up" in response.text
    assert "alert_total" in response.text