from fastapi import FastAPI
from api.devices import router as devices_router
from api.metrics import router as metrics_router
from api.gateway import router as gateway_router
from dashboard.app import router as dashboard_router

app = FastAPI(title="storage-infrastructure-monitoring--platform")

app.include_router(devices_router)
app.include_router(metrics_router)
app.include_router(gateway_router)
app.include_router(dashboard_router)