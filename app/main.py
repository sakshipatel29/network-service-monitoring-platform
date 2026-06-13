from fastapi import FastAPI
import httpx
import json
from app.monitor import check_all_services
from app.redis_client import redis_client

from app.models import Service
from app.storage import services

app = FastAPI(
    title="Network Service Monitoring Platform",
    description="Backend platform for monitoring service health and infrastructure workflows.",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Network Service Monitoring Platform is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "network-monitoring-api"
    }


@app.post("/services")
def register_service(service: Service):

    redis_client.rpush(
        "services",
        service.model_dump_json()
    )

    return {
        "message": "Service registered successfully",
        "service": service
    }


@app.get("/services")
def get_services():

    stored_services = redis_client.lrange(
        "services",
        0,
        -1
    )

    services = [
        json.loads(service)
        for service in stored_services
    ]

    return {
        "total_services": len(services),
        "services": services
    }


@app.get("/services/check")
def check_services_health():
    results = check_all_services()

    return {
        "total_checked": len(results),
        "results": results
    }

@app.get("/services/{service_name}/history")
def get_service_history(service_name: str):
    stored_history = redis_client.lrange(
        f"history:{service_name}",
        0,
        -1
    )

    history = [
        json.loads(item)
        for item in stored_history
    ]

    return {
        "service_name": service_name,
        "total_checks": len(history),
        "history": history
    }

@app.get("/services/{service_name}/uptime")
def get_service_uptime(service_name: str):
    stored_history = redis_client.lrange(
        f"history:{service_name}",
        0,
        -1
    )

    history = [
        json.loads(item)
        for item in stored_history
    ]

    if not history:
        return {
            "service_name": service_name,
            "message": "No monitoring history found"
        }

    healthy_count = sum(
        1 for item in history
        if item["status"] == "healthy"
    )

    uptime_percentage = round(
        (healthy_count / len(history)) * 100,
        2
    )

    return {
        "service_name": service_name,
        "total_checks": len(history),
        "healthy_checks": healthy_count,
        "uptime_percentage": uptime_percentage
    }

@app.get("/alerts")
def get_alerts():
    stored_alerts = redis_client.lrange("alerts", 0, -1)

    alerts = [
        json.loads(alert)
        for alert in stored_alerts
    ]

    return {
        "total_alerts": len(alerts),
        "alerts": alerts
    }