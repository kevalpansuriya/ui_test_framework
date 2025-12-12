from typing import Optional
import logging
import os
from datetime import datetime
from pathlib import Path


class Logger:
    """
    Logger utility class following SRP - handles only logging functionality
    """
    
    def __init__(self, logPath: str = "logs", logLevel: int = logging.INFO) -> None:
        self.logPath: str = logPath
        self.logLevel: int = logLevel
        self.logger: logging.Logger
        self._setupLogger()
    
    def _setupLogger(self) -> None:
        """Setup logger configuration"""
        # Create logs directory if it doesn't exist
        Path(self.logPath).mkdir(parents=True, exist_ok=True)
        
        # Create log file name with timestamp
        logFileName = f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        logFilePath = os.path.join(self.logPath, logFileName)
        
        # Get or create named logger to avoid pytest capturing issues
        self.logger = logging.getLogger("test_framework")
        self.logger.setLevel(self.logLevel)

        # Create formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        # Add file handler once
        if not any(isinstance(h, logging.FileHandler) for h in self.logger.handlers):
            fileHandler = logging.FileHandler(logFilePath)
            fileHandler.setLevel(self.logLevel)
            fileHandler.setFormatter(formatter)
            self.logger.addHandler(fileHandler)

        # Add console handler once (ensures console output even under pytest)
        if not any(isinstance(h, logging.StreamHandler) for h in self.logger.handlers):
            consoleHandler = logging.StreamHandler()
            consoleHandler.setLevel(self.logLevel)
            consoleHandler.setFormatter(formatter)
            self.logger.addHandler(consoleHandler)

        # Allow propagation to pytest's logging system so logs appear in HTML report
        # This allows pytest to capture logs and include them in the HTML report
        self.logger.propagate = True
    
    def getLogger(self, name: Optional[str] = None) -> logging.Logger:
        """Get logger instance"""
        if name:
            return logging.getLogger(name)
        return self.logger
    
    def info(self, message: str) -> None:
        """Log info message"""
        self.logger.info(message)
    
    def error(self, message: str) -> None:
        """Log error message"""
        self.logger.error(message)
    
    def warning(self, message: str) -> None:
        """Log warning message"""
        self.logger.warning(message)
    
    def debug(self, message: str) -> None:
        """Log debug message"""
        self.logger.debug(message)
    
    def critical(self, message: str) -> None:
        """Log critical message"""
        self.logger.critical(message)

