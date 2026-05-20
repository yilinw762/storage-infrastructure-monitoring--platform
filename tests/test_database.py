import pytest
from database.models import SessionLocal
from database.repository import insert_metric, get_latest_metrics, get_device_history
from sqlalchemy import text

SAMPLE_METRIC = {
    "device_id": "dev001",
    "used_tb": 250.0,
    "capacity_tb": 500.0,
    "latency_ms": 3.2,
    "iops": 45000,
    "health_status": "healthy",
}

def test_metric_inserts_successfully():
    db = SessionLocal()
    try:
        before = db.execute(text("SELECT COUNT(*) FROM metrics")).scalar()
        insert_metric(db, SAMPLE_METRIC)
        after = db.execute(text("SELECT COUNT(*) FROM metrics")).scalar()
        assert after == before + 1
    finally:
        db.close()

def test_get_latest_metrics_returns_list():
    metrics = get_latest_metrics(SessionLocal())
    assert isinstance(metrics, list)

def test_latest_metrics_have_required_fields():
    metrics = get_latest_metrics(SessionLocal())
    for m in metrics:
        assert "device_id" in m
        assert "hostname" in m
        assert "used_tb" in m
        assert "capacity_tb" in m
        assert "health_status" in m

def test_device_history_returns_for_known_device():
    db = SessionLocal()
    history = get_device_history(db, "dev001")
    assert isinstance(history, list)
    assert len(history) > 0

def test_device_history_unknown_device_returns_empty():
    db = SessionLocal()
    history = get_device_history(db, "nonexistent-device")
    assert history == []