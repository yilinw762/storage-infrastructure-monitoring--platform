from sqlalchemy import text
from database.models import SessionLocal

def report_device_summary():
    db = SessionLocal()
    try:
        result = db.execute(text("""
            SELECT
                d.device_id, d.hostname, d.vendor, d.location,
                COUNT(m.id)   AS sample_count,
                ROUND(AVG(m.latency_ms)::numeric, 2) AS avg_latency_ms,
                ROUND(AVG(m.iops)::numeric, 0)       AS avg_iops,
                ROUND(AVG(m.used_tb / m.capacity_tb * 100)::numeric, 1) AS avg_utilization_pct
            FROM devices d
            LEFT JOIN metrics m ON d.device_id = m.device_id
            GROUP BY d.device_id, d.hostname, d.vendor, d.location
            ORDER BY avg_utilization_pct DESC NULLS LAST
        """)).mappings().all()
        return [dict(r) for r in result]
    finally:
        db.close()

def report_critical_devices():
    db = SessionLocal()
    try:
        result = db.execute(text("""
            SELECT DISTINCT ON (m.device_id)
                m.device_id, d.hostname, d.location, m.health_status, m.collected_at
            FROM metrics m
            JOIN devices d ON m.device_id = d.device_id
            WHERE m.health_status IN ('warning', 'critical')
            ORDER BY m.device_id, m.collected_at DESC
        """)).mappings().all()
        return [dict(r) for r in result]
    finally:
        db.close()