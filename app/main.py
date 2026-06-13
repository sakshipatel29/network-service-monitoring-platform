from fastapi import FastAPI
import httpx

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
    services.append(service)

    return {
        "message": "Service registered successfully",
        "service": service
    }


@app.get("/services")
def get_services():
    return {
        "total_services": len(services),
        "services": services
    }


@app.get("/services/check")
def check_services_health():
    results = []

    for service in services:
        try:
            response = httpx.get(service.url, timeout=5)

            results.append({
                "service_name": service.service_name,
                "url": service.url,
                "status_code": response.status_code,
                "status": "healthy" if response.status_code == 200 else "unhealthy"
            })

        except Exception as e:
            results.append({
                "service_name": service.service_name,
                "url": service.url,
                "status": "unreachable",
                "error": str(e)
            })

    return {
        "total_checked": len(results),
        "results": results
    }