import logging

from project.runtime import log


def setup(environment: str) -> None:
    """Set up runtime dependencies."""

    log.setup(environment, logging.INFO)
