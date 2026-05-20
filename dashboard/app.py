from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database.models import get_db
from database.repository import get_latest_metrics
from reports.utilization import report_avg_utilization, report_capacity_by_location
from reports.analytics import report_critical_devices

router = APIRouter()
templates = Jinja2Templates(directory="dashboard/templates")

@router.get("/", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):
    metrics = get_latest_metrics(db)
    avg_util = report_avg_utilization()
    capacity_by_loc = report_capacity_by_location()
    alerts = report_critical_devices()

    for m in metrics:
        util = float(m["used_tb"]) / float(m["capacity_tb"]) * 100
        m["utilization_pct"] = round(util, 1)

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "metrics": metrics,
            "avg_utilization": avg_util,
            "capacity_by_location": capacity_by_loc,
            "alerts": alerts,
            "device_count": len(metrics),
        },
    )