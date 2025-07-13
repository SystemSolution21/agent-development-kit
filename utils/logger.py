"""
Logging configuration module for the ADK application.
Provides centralized logging setup with both file and console output.
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


class AdkLogger:
    """Logger class for ADK applications with file and console output."""

    @staticmethod
    def setup(module_name: str, level: int) -> logging.Logger:
        """
        Configure and return a logger instance with both file and console handlers.

        Args:
            module_name: Name of the module requesting the logger
            level: Logging level (e.g., logging.DEBUG, logging.INFO)

        Returns:
            logging.Logger: Configured logger instance
        """
        # Create logs directory
        current_dir: Path = Path(__file__).parent.parent.resolve()
        logs_dir: Path = current_dir / "logs"
        logs_dir.mkdir(exist_ok=True)

        # Configure log file
        log_file: Path = logs_dir / "adk_application.log"

        # Create and configure logger
        logger: logging.Logger = logging.getLogger(name=module_name)
        logger.setLevel(level=level)
        logger.propagate = False  # Prevent messages from propagating to the root logger

        # Create formatters and handlers
        formatter: logging.Formatter = logging.Formatter(
            fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        # Rotating file handler
        if not any(
            isinstance(handler, RotatingFileHandler)
            and handler.baseFilename == str(log_file)
            for handler in logger.handlers
        ):
            file_handler: RotatingFileHandler = RotatingFileHandler(
                filename=log_file,
                maxBytes=10_000_000,  # 10 MB
                backupCount=5,
                encoding="utf-8",
            )
            file_handler.setFormatter(fmt=formatter)
            logger.addHandler(hdlr=file_handler)

        # # Console handler
        # console_handler: logging.StreamHandler = logging.StreamHandler()
        # console_handler.setFormatter(fmt=formatter)
        # # Add console handlers to logger
        # logger.addHandler(hdlr=console_handler)

        return logger
