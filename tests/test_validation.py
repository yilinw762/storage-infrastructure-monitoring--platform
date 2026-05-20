import pytest
from validation.validators import validate_metrics, ValidationError

VALID = {
    "device_id": "dev001",
    "capacity_tb": 500,
    "used_tb": 300,
    "latency_ms": 2.5,
    "iops": 50000,
    "health_status": "healthy",
}

def test_valid_metrics_pass():
    result = validate_metrics(VALID.copy())
    assert result["device_id"] == "dev001"

def test_missing_device_id_raises():
    bad = {**VALID, "device_id": None}
    with pytest.raises(ValidationError):
        validate_metrics(bad)

def test_negative_capacity_raises():
    bad = {**VALID, "capacity_tb": -100}
    with pytest.raises(ValidationError):
        validate_metrics(bad)

def test_negative_used_raises():
    bad = {**VALID, "used_tb": -1}
    with pytest.raises(ValidationError):
        validate_metrics(bad)

def test_used_exceeds_capacity_raises():
    bad = {**VALID, "used_tb": 600, "capacity_tb": 500}
    with pytest.raises(ValidationError):
        validate_metrics(bad)

def test_negative_latency_raises():
    bad = {**VALID, "latency_ms": -0.5}
    with pytest.raises(ValidationError):
        validate_metrics(bad)

def test_invalid_health_status_raises():
    bad = {**VALID, "health_status": "unknown"}
    with pytest.raises(ValidationError):
        validate_metrics(bad)

def test_all_valid_health_statuses_pass():
    for status in ["healthy", "warning", "critical"]:
        result = validate_metrics({**VALID, "health_status": status})
        assert result["health_status"] == status

def test_used_equal_to_capacity_is_valid():
    edge = {**VALID, "used_tb": 500, "capacity_tb": 500}
    result = validate_metrics(edge)
    assert result is not None