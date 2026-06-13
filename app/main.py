from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI(
    title="Network Service Monitoring Platform",
    description="Backend platform for monitoring service health and infrastructure workflows.",
    version="1.0.0"
)

class Service(BaseModel):
    service_name: str
    url: str

services: List[Service] = []

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