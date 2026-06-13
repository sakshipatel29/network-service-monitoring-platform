# Network Service Monitoring Platform

A production-style backend monitoring platform built with FastAPI, Redis, Docker, and AWS CloudWatch.

## Features

- Service health monitoring
- Infrastructure status tracking
- Redis-backed monitoring cache
- Real-time alert generation
- CloudWatch observability integration
- Dockerized deployment
- REST APIs for service status

## Tech Stack

- Python
- FastAPI
- Redis
- Docker
- AWS CloudWatch

## Project Structure

```text
network-service-monitoring-platform/
├── app/
├── tests/
├── requirements.txt
├── README.md
└── .gitignore
```

## Run Locally

```bash
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

## API Docs

```text
http://127.0.0.1:8000/docs
```