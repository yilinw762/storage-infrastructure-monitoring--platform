from fastapi import APIRouter, Depends, HTTPException # type: ignore
from sqlalchemy.orm import Session # type: ignore
from sqlalchemy import text # type: ignore
from database.models import get_db

router = APIRouter()

@router.get("/devices")
def get_devices(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT * FROM devices")).mappings().all()
    return [dict(row) for row in result]

@router.get("/devices/{device_id}")
def get_device(device_id: str, db: Session = Depends(get_db)):
    result = db.execute(
        text("SELECT * FROM devices WHERE device_id = :id"),
        {"id": device_id}
    ).mappings().first()
    if not result:
        raise HTTPException(status_code=404, detail="Device not found")
    return dict(result)