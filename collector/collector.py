import requests
from validation.validators import validate_metrics, ValidationError
from database.models import SessionLocal
from database.repository import insert_metric

STORAGE_API_URL = "http://localhost:8001/metrics"

def collect_and_store():
    print("Collector: fetching metrics...")
    try:
        response = requests.get(STORAGE_API_URL, timeout=10)
        response.raise_for_status()
        metrics_list = response.json()
    except Exception as e:
        print(f"Collector: failed to fetch metrics — {e}")
        return

    db = SessionLocal()
    success = 0
    errors = 0

    try:
        for raw in metrics_list:
            try:
                validated = validate_metrics(raw)
                insert_metric(db, validated)
                success += 1
            except ValidationError as ve:
                print(f"Validation error for {raw.get('device_id')}: {ve}")
                errors += 1
    finally:
        db.close()

    print(f"Collector: {success} metrics stored, {errors} validation errors.")