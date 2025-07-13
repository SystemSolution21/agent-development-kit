"""
Logging configuration module for the ADK application.
Provides a centralized function to configure logging for the application.
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

_ADK_LOGGER_SETUP_DONE = False


def setup_adk_logging(level: int = logging.INFO, log_to_console: bool = False) -> None:
    """
    Configures the root 'adk_log' logger. Should be called once at startup.

    This function is idempotent and will not add handlers more than once.

    Args:
        level: The minimum logging level to capture (e.g., logging.INFO).
        log_to_console: If True, logs will also be sent to the console.
    """
    global _ADK_LOGGER_SETUP_DONE
    if _ADK_LOGGER_SETUP_DONE:
        return

    # Use a single top-level logger for the application
    logger: logging.Logger = logging.getLogger(name="adk_log")
    logger.setLevel(level=level)
    # Prevent messages from propagating to the root logger
    logger.propagate = False

    # Create logs directory
    current_dir: Path = Path(__file__).parent.parent.resolve()
    logs_dir: Path = current_dir / "logs"
    logs_dir.mkdir(exist_ok=True)
    log_file: Path = logs_dir / "adk.log"

    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Rotating file handler
    file_handler = RotatingFileHandler(
        filename=log_file,
        maxBytes=10_000_000,  # 10 MB
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setFormatter(fmt=formatter)
    logger.addHandler(hdlr=file_handler)

    # Console handler
    if log_to_console:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(hdlr=console_handler)

    _ADK_LOGGER_SETUP_DONE = True
