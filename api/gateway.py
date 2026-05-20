import os
from fastapi import APIRouter, Request, HTTPException, Depends # type: ignore
from dotenv import load_dotenv

load_dotenv()

GATEWAY_API_KEY = os.getenv("GATEWAY_API_KEY")

router = APIRouter()

def verify_api_key(request: Request):
    key = request.headers.get("X-API-Key")
    if key != GATEWAY_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
    return key

@router.get("/gateway/devices")
def gateway_devices(request: Request, key: str = Depends(verify_api_key)):
    import httpx
    resp = httpx.get("http://localhost:8000/devices")
    return resp.json()

@router.get("/gateway/metrics")
def gateway_metrics(request: Request, key: str = Depends(verify_api_key)):
    import httpx
    resp = httpx.get("http://localhost:8000/metrics")
    return resp.json()