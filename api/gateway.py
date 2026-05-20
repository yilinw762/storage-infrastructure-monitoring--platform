import os
from fastapi import APIRouter, Request, HTTPException, Depends  # type: ignore
from dotenv import load_dotenv
from sqlalchemy.orm import Session  # type: ignore

from api.devices import get_devices
from api.metrics import get_all_metrics
from database.models import get_db

load_dotenv()

GATEWAY_API_KEY = os.getenv("GATEWAY_API_KEY")

router = APIRouter()


def verify_api_key(request: Request):
    key = request.headers.get("X-API-Key")
    if key != GATEWAY_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
    return key


@router.get("/gateway/devices")
def gateway_devices(
    request: Request,
    key: str = Depends(verify_api_key),
    db: Session = Depends(get_db),
):
    return get_devices(db)


@router.get("/gateway/metrics")
def gateway_metrics(
    request: Request,
    key: str = Depends(verify_api_key),
    db: Session = Depends(get_db),
):
    return get_all_metrics(db)
