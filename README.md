# Network Service Monitoring Platform

A production-style monitoring and observability platform built using FastAPI, Redis, Docker, and AWS CloudWatch-compatible logging.

The platform continuously monitors registered services, tracks uptime, stores monitoring history, generates alerts for unhealthy services, and provides REST APIs for operational visibility.

---

## Features

### Service Registry

Register services dynamically for monitoring.

```http
POST /services
```

Example:

```json
{
  "service_name": "main-api",
  "url": "http://api:8000/health"
}
```

---

### Health Monitoring

Perform health checks against all registered services.

```http
GET /services/check
```

---

### Monitoring History

Store and retrieve historical monitoring records.

```http
GET /services/{service_name}/history
```

---

### Uptime Tracking

Calculate uptime percentage based on monitoring history.

```http
GET /services/{service_name}/uptime
```

---

### Alert Generation

Generate alerts when services become unhealthy or unreachable.

```http
GET /alerts
```

---

## Architecture

```text
                   +----------------+
                   |    FastAPI     |
                   +--------+-------+
                            |
                            |
                            v
                   +----------------+
                   |     Redis      |
                   +----------------+
                            |
         +------------------+------------------+
         |                                     |
         v                                     v
 Monitoring History                    Alert Storage

                            |
                            v

                 External Services
```

---

## Tech Stack

- Python
- FastAPI
- Redis
- Docker
- Docker Compose
- AWS CloudWatch Logging (Watchtower)
- HTTPX

---

## Project Structure

```text
network-service-monitoring-platform/
│
├── app/
│   ├── main.py
│   ├── models.py
│   ├── monitor.py
│   ├── worker.py
│   ├── redis_client.py
│   ├── logging_config.py
│   └── storage.py
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
└── tests/
```

---

## Run Locally

### Start Redis

```bash
brew services start redis
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Start FastAPI

```bash
python -m uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

---

## Run with Docker

```bash
docker compose up --build
```

---

## Future Improvements

- Email alerts
- Slack notifications
- AWS CloudWatch Metrics
- Prometheus integration
- Grafana dashboards
- Kubernetes deployment
- Service dependency mapping
- Authentication and RBAC

---

## Resume Impact

This project demonstrates:

- Backend API Development
- Distributed Service Monitoring
- Observability Engineering
- Redis Data Modeling
- Docker Containerization
- AWS Logging Integration
- Reliability Engineering Concepts
- Production Monitoring Workflows