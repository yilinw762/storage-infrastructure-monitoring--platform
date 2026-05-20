import random
from fastapi import APIRouter, Depends # type: ignore
from sqlalchemy.orm import Session # type: ignore
from sqlalchemy import text # type: ignore
from database.models import get_db

router = APIRouter()

def simulate_metrics(device: dict) -> dict:
    capacity = float(device["capacity_tb"])
    used = round(random.uniform(0.4, 0.95) * capacity, 2)
    health_options = ["healthy"] * 7 + ["warning"] * 2 + ["critical"] * 1
    return {
        "device_id":     device["device_id"],
        "used_tb":       used,
        "capacity_tb":   capacity,
        "latency_ms":    round(random.uniform(0.5, 12.0), 2),
        "iops":          random.randint(5000, 150000),
        "health_status": random.choice(health_options),
    }

@router.get("/metrics")
def get_all_metrics(db: Session = Depends(get_db)):
    devices = db.execute(text("SELECT * FROM devices")).mappings().all()
    return [simulate_metrics(dict(d)) for d in devices]

@router.get("/metrics/{device_id}")
def get_device_metrics(device_id: str, db: Session = Depends(get_db)):
    device = db.execute(
        text("SELECT * FROM devices WHERE device_id = :id"),
        {"id": device_id}
    ).mappings().first()
    if not device:
        return {"error": "Device not found"}
    return simulate_metrics(dict(device))

@router.get("/health")
def health_check():
    return {"status": "ok", "service": "storage-api"}