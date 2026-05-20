class ValidationError(Exception):
    pass

def validate_metrics(data: dict) -> dict:
    device_id    = data.get("device_id")
    capacity_tb  = data.get("capacity_tb")
    used_tb      = data.get("used_tb")
    latency_ms   = data.get("latency_ms")
    iops         = data.get("iops")
    health_status = data.get("health_status")

    valid_health_states = {"healthy", "warning", "critical"}

    if not device_id:
        raise ValidationError("device_id is required")

    if capacity_tb is None or capacity_tb <= 0:
        raise ValidationError(f"Invalid capacity_tb: {capacity_tb}")

    if used_tb is None or used_tb < 0:
        raise ValidationError(f"Invalid used_tb: {used_tb}")

    if used_tb > capacity_tb:
        raise ValidationError(
            f"used_tb ({used_tb}) exceeds capacity_tb ({capacity_tb})"
        )

    if latency_ms is None or latency_ms < 0:
        raise ValidationError(f"Invalid latency_ms: {latency_ms}")

    if iops is None or iops < 0:
        raise ValidationError(f"Invalid iops: {iops}")

    if health_status not in valid_health_states:
        raise ValidationError(
            f"Invalid health_status '{health_status}'. "
            f"Must be one of {valid_health_states}"
        )

    return data