import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_get_devices_returns_200():
    response = client.get("/devices")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_devices_has_expected_fields():
    response = client.get("/devices")
    devices = response.json()
    assert len(devices) > 0
    for device in devices:
        assert "device_id" in device
        assert "hostname" in device
        assert "location" in device
        assert "capacity_tb" in device

def test_get_single_device():
    response = client.get("/devices/dev001")
    assert response.status_code == 200
    assert response.json()["device_id"] == "dev001"

def test_get_nonexistent_device_returns_404():
    response = client.get("/devices/does-not-exist")
    assert response.status_code == 404

def test_get_metrics_returns_200():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_metrics_have_required_fields():
    response = client.get("/metrics")
    for m in response.json():
        assert "device_id" in m
        assert "used_tb" in m
        assert "capacity_tb" in m
        assert "latency_ms" in m
        assert "iops" in m
        assert "health_status" in m

def test_gateway_rejects_missing_key():
    response = client.get("/gateway/devices")
    assert response.status_code == 401

def test_gateway_rejects_wrong_key():
    response = client.get("/gateway/devices", headers={"X-API-Key": "wrongkey"})
    assert response.status_code == 401

def test_gateway_accepts_valid_key():
    response = client.get("/gateway/devices", headers={"X-API-Key": "supersecretkey123"})
    assert response.status_code == 200