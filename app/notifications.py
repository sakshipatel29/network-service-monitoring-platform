import os
import httpx
from dotenv import load_dotenv

from app.logging_config import logger
import smtplib
from email.message import EmailMessage

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

def send_email_alert(alert: dict):
    email_enabled = os.getenv("EMAIL_ALERTS_ENABLED", "false").lower() == "true"

    if not email_enabled:
        logger.info("Email alerts are disabled. Skipping email notification.")
        return

    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    smtp_username = os.getenv("SMTP_USERNAME")
    smtp_password = os.getenv("SMTP_PASSWORD")
    alert_email_from = os.getenv("ALERT_EMAIL_FROM")
    alert_email_to = os.getenv("ALERT_EMAIL_TO")

    required_values = [
        smtp_host,
        smtp_username,
        smtp_password,
        alert_email_from,
        alert_email_to
    ]

    if not all(required_values):
        logger.warning("Email alert configuration is incomplete. Skipping email notification.")
        return

    email = EmailMessage()
    email["Subject"] = f"Service Alert: {alert['service_name']} is {alert['status']}"
    email["From"] = alert_email_from
    email["To"] = alert_email_to

    email.set_content(
        f"""
Service Alert

Service Name: {alert['service_name']}
Status: {alert['status']}
URL: {alert['url']}
Time: {alert['created_at']}
Message: {alert['message']}
"""
    )

    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(email)

        logger.info(f"Email alert sent for service={alert['service_name']}")

    except Exception as e:
        logger.error(f"Failed to send email alert: {e}")