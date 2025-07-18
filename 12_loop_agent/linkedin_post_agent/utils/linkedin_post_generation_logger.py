"""
Logging configuration module for the LinkedIn Post Generator Application.
Provides a centralized function to configure logging for the application.
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

_LOGGER_SETUP_DONE = False


def setup_logging(level: int = logging.INFO, log_to_console: bool = False) -> None:
    """
    Configures the root 'linkedin_post_generation' logger. Should be called once at startup.

    This function is idempotent and will not add handlers more than once.

    Args:
        level: The minimum logging level to capture (e.g., logging.INFO).
        log_to_console: If True, logs will also be sent to the console.
    """
    global _LOGGER_SETUP_DONE
    if _LOGGER_SETUP_DONE:
        return

    # Single top-level logger for the application
    logger: logging.Logger = logging.getLogger(name="linkedin_post_generation")
    logger.setLevel(level=level)
    # Prevent messages from propagating to the root logger
    logger.propagate = False

    # Create logs directory
    current_dir: Path = Path(__file__).parent.parent.resolve()
    logs_dir: Path = current_dir / "logs"
    logs_dir.mkdir(exist_ok=True)
    log_file: Path = logs_dir / "linkedin_post_generation.log"

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
        console_handler: logging.StreamHandler = logging.StreamHandler()
        console_handler.setFormatter(fmt=formatter)
        logger.addHandler(hdlr=console_handler)

    _LOGGER_SETUP_DONE = True
