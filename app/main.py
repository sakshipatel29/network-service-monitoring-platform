from fastapi import FastAPI

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