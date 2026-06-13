import os
import httpx
from dotenv import load_dotenv

from app.logging_config import logger

load_dotenv()


def send_slack_alert(alert: dict):
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")

    if not webhook_url:
        logger.info("Slack webhook URL not configured. Skipping Slack notification.")
        return

    message = {
        "text": (
            f" *Service Alert*\n"
            f"*Service:* {alert['service_name']}\n"
            f"*Status:* {alert['status']}\n"
            f"*URL:* {alert['url']}\n"
            f"*Time:* {alert['created_at']}"
        )
    }

    try:
        response = httpx.post(webhook_url, json=message, timeout=5)
        response.raise_for_status()
        logger.info(f"Slack alert sent for service={alert['service_name']}")

    except Exception as e:
        logger.error(f"Failed to send Slack alert: {e}")