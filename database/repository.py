from sqlalchemy.orm import Session # type: ignore
from sqlalchemy import text # type: ignore

def insert_metric(db: Session, metric: dict):
    db.execute(text("""
        INSERT INTO metrics
            (device_id, used_tb, capacity_tb, latency_ms, iops, health_status)
        VALUES
            (:device_id, :used_tb, :capacity_tb, :latency_ms, :iops, :health_status)
    """), metric)
    db.commit()

def get_latest_metrics(db: Session):
    result = db.execute(text("""
        SELECT DISTINCT ON (device_id)
            m.device_id, d.hostname, d.location, d.vendor,
            m.used_tb, m.capacity_tb, m.latency_ms, m.iops,
            m.health_status, m.collected_at
        FROM metrics m
        JOIN devices d ON m.device_id = d.device_id
        ORDER BY device_id, collected_at DESC
    """)).mappings().all()
    return [dict(row) for row in result]

def get_device_history(db: Session, device_id: str, limit: int = 10):
    result = db.execute(text("""
        SELECT * FROM metrics
        WHERE device_id = :device_id
        ORDER BY collected_at DESC
        LIMIT :limit
    """), {"device_id": device_id, "limit": limit}).mappings().all()
    return [dict(row) for row in result]