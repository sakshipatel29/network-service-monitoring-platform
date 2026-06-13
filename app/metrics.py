from prometheus_client import Counter, Gauge


SERVICE_CHECK_TOTAL = Counter(
    "service_check_total",
    "Total number of service health checks",
    ["service_name", "status"]
)

SERVICE_UP = Gauge(
    "service_up",
    "Service health status: 1 healthy, 0 unhealthy/unreachable",
    ["service_name"]
)

ALERT_TOTAL = Counter(
    "alert_total",
    "Total number of generated alerts",
    ["service_name", "status"]
)