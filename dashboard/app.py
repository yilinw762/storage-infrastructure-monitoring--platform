from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy import text  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from api.metrics import simulate_metrics
from database.models import get_db

router = APIRouter(tags=["dashboard"])


@router.get("/", response_class=HTMLResponse, include_in_schema=False)
def home() -> str:
    return """
    <html>
        <head>
            <title>Storage Monitoring Platform</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 2rem;
                    line-height: 1.5;
                }
                a {
                    color: #0057b8;
                    text-decoration: none;
                }
                a:hover {
                    text-decoration: underline;
                }
            </style>
        </head>
        <body>
            <h1>Storage Monitoring Platform</h1>
            <p>The API is running.</p>
            <p><a href="/dashboard">Open dashboard</a></p>
        </body>
    </html>
    """


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(db: Session = Depends(get_db)) -> str:
    devices = db.execute(text("SELECT * FROM devices")).mappings().all()
    device_rows = [dict(device) for device in devices]
    metrics = [simulate_metrics(device) for device in device_rows]

    total_capacity = round(sum(metric["capacity_tb"] for metric in metrics), 2)
    total_used = round(sum(metric["used_tb"] for metric in metrics), 2)
    avg_utilization = round((total_used / total_capacity) * 100, 1) if total_capacity else 0.0
    healthy_count = sum(1 for metric in metrics if metric["health_status"] == "healthy")
    warning_count = sum(1 for metric in metrics if metric["health_status"] == "warning")
    critical_count = sum(1 for metric in metrics if metric["health_status"] == "critical")

    rows_html = "".join(
        f"""
        <tr>
            <td>{metric["device_id"]}</td>
            <td>{metric["used_tb"]} TB</td>
            <td>{metric["capacity_tb"]} TB</td>
            <td>{round((metric["used_tb"] / metric["capacity_tb"]) * 100, 1)}%</td>
            <td>{metric["latency_ms"]} ms</td>
            <td>{metric["iops"]}</td>
            <td>{metric["health_status"].title()}</td>
        </tr>
        """
        for metric in metrics
    )

    return f"""
    <html>
        <head>
            <title>Storage Dashboard</title>
            <style>
                :root {{
                    color-scheme: light;
                }}
                body {{
                    font-family: Arial, sans-serif;
                    margin: 2rem;
                    background: #f4f7fb;
                    color: #16324f;
                }}
                h1, h2 {{
                    margin-bottom: 0.5rem;
                }}
                .stats {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
                    gap: 1rem;
                    margin: 1.5rem 0 2rem;
                }}
                .card {{
                    background: white;
                    border-radius: 12px;
                    padding: 1rem;
                    box-shadow: 0 8px 24px rgba(22, 50, 79, 0.08);
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    background: white;
                    border-radius: 12px;
                    overflow: hidden;
                    box-shadow: 0 8px 24px rgba(22, 50, 79, 0.08);
                }}
                th, td {{
                    padding: 0.85rem 1rem;
                    text-align: left;
                    border-bottom: 1px solid #e6edf5;
                }}
                th {{
                    background: #16324f;
                    color: white;
                }}
                tr:last-child td {{
                    border-bottom: none;
                }}
            </style>
        </head>
        <body>
            <h1>Storage Infrastructure Dashboard</h1>
            <p>Live summary generated from the current device inventory.</p>

            <div class="stats">
                <div class="card"><h2>{len(metrics)}</h2><p>Devices</p></div>
                <div class="card"><h2>{total_used} / {total_capacity} TB</h2><p>Used Capacity</p></div>
                <div class="card"><h2>{avg_utilization}%</h2><p>Average Utilization</p></div>
                <div class="card"><h2>{healthy_count} healthy</h2><p>{warning_count} warning, {critical_count} critical</p></div>
            </div>

            <table>
                <thead>
                    <tr>
                        <th>Device</th>
                        <th>Used</th>
                        <th>Capacity</th>
                        <th>Utilization</th>
                        <th>Latency</th>
                        <th>IOPS</th>
                        <th>Health</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html or '<tr><td colspan="7">No devices found.</td></tr>'}
                </tbody>
            </table>
        </body>
    </html>
    """
