import logging
import os

import watchtower


def setup_logger():
    logger = logging.getLogger("monitoring-platform")
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )

    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    if os.getenv("ENABLE_CLOUDWATCH", "false").lower() == "true":
        cloudwatch_handler = watchtower.CloudWatchLogHandler(
            log_group=os.getenv(
                "CLOUDWATCH_LOG_GROUP",
                "network-service-monitoring-platform"
            ),
            stream_name=os.getenv(
                "CLOUDWATCH_STREAM_NAME",
                "fastapi-monitoring-service"
            )
        )

        cloudwatch_handler.setFormatter(formatter)
        logger.addHandler(cloudwatch_handler)

    return logger


logger = setup_logger()