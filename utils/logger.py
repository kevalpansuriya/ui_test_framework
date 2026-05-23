"""Simple logging helper for tests and page objects."""

import logging
from datetime import datetime
from pathlib import Path


def get_logger(name: str, log_dir: str = "logs") -> logging.Logger:
    """
    Return a logger that writes to console and a timestamped log file.

    Args:
        name: Logger name (usually the module or class name).
        log_dir: Folder where log files are stored.
    """
    Path(log_dir).mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    log_file = Path(log_dir) / f"test_{datetime.now():%Y%m%d_%H%M%S}.log"
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    logger.propagate = True
    return logger
