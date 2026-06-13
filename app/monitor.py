import json
from datetime import datetime, timezone

import httpx

from app.redis_client import redis_client


def get_registered_services():
    stored_services = redis_client.lrange("services", 0, -1)

    return [
        json.loads(service)
        for service in stored_services
    ]


def check_single_service(service):
    checked_at = datetime.now(timezone.utc).isoformat()

    try:
        response = httpx.get(service["url"], timeout=5)

        status = "healthy" if response.status_code == 200 else "unhealthy"

        result = {
            "service_name": service["service_name"],
            "url": service["url"],
            "status": status,
            "status_code": response.status_code,
            "checked_at": checked_at
        }

    except Exception as e:
        result = {
            "service_name": service["service_name"],
            "url": service["url"],
            "status": "unreachable",
            "error": str(e),
            "checked_at": checked_at
        }

    redis_client.lpush(
        f"history:{service['service_name']}",
        json.dumps(result)
    )

    if result["status"] != "healthy":
        alert = {
            "service_name": service["service_name"],
            "url": service["url"],
            "status": result["status"],
            "message": f"Alert: {service['service_name']} is {result['status']}",
            "created_at": checked_at
        }

        redis_client.lpush(
            "alerts",
            json.dumps(alert)
        )

    redis_client.ltrim(
        f"history:{service['service_name']}",
        0,
        49
    )

    return result


def check_all_services():
    services = get_registered_services()
    results = []

    for service in services:
        result = check_single_service(service)
        results.append(result)

    return results