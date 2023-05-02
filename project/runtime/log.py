import logging

import colorlog
import google.cloud.logging

_LOGGER = logging.getLogger(__name__)


def setup(environment: str, level: int = logging.DEBUG):
    """Set up logging."""

    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(
        colorlog.ColoredFormatter(
            fmt=(
                "[%(asctime)s.%(msecs)03d] "
                "%(log_color)s%(levelname)s %(name)s - %(threadName)s%(reset)s: "
                "%(message)s"
            ),
            datefmt="%H:%M:%S",
            log_colors={
                "DEBUG": "green",
                "INFO": "blue",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            },
        )
    )
    if environment == "production":
        client = google.cloud.logging.Client()
        client.setup_logging(log_level=level)
    root_logger.addHandler(console_handler)
    _LOGGER.info("💁🏻‍♀️ Logging set up.")
