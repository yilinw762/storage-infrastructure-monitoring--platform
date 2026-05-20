from sqlalchemy import text
from database.models import SessionLocal

def report_high_utilization(threshold: float = 0.9):
    db = SessionLocal()
    try:
        result = db.execute(text("""
            SELECT DISTINCT ON (m.device_id)
                m.device_id, d.hostname, d.location,
                m.used_tb, m.capacity_tb,
                ROUND((m.used_tb / m.capacity_tb * 100)::numeric, 1) AS utilization_pct
            FROM metrics m
            JOIN devices d ON m.device_id = d.device_id
            ORDER BY m.device_id, m.collected_at DESC
        """)).mappings().all()
        flagged = [dict(r) for r in result if float(r["used_tb"]) / float(r["capacity_tb"]) > threshold]
        return flagged
    finally:
        db.close()

def report_avg_utilization():
    db = SessionLocal()
    try:
        result = db.execute(text("""
            SELECT ROUND(AVG(used_tb / capacity_tb * 100)::numeric, 2) AS avg_utilization_pct
            FROM metrics
        """)).scalar()
        return float(result) if result else 0.0
    finally:
        db.close()

def report_capacity_by_location():
    db = SessionLocal()
    try:
        result = db.execute(text("""
            SELECT location, SUM(capacity_tb) AS total_capacity_tb
            FROM devices
            GROUP BY location
            ORDER BY total_capacity_tb DESC
        """)).mappings().all()
        return [dict(r) for r in result]
    finally:
        db.close()