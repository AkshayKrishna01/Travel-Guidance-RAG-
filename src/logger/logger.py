import logging
import json
import sys
import os
from datetime import datetime
from typing import Any
from enum import Enum

class LogLevel(Enum):
    """Log level enumeration"""
    DEBUG = "debug"
    INFO = "info"
    WARN = "warn"
    ERROR = "error"
    FATAL = "fatal"

class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging"""
    
    def format(self, record):
        """Format log record as JSON"""
        log_entry = {
            "time": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
            "caller": f"{record.filename}:{record.lineno}"
        }
        
        # Add extra fields if present
        if hasattr(record, 'fields') and record.fields:
            log_entry.update(record.fields)
        
        # Add exception info if present
        if record.exc_info:
            log_entry["stacktrace"] = self.formatException(record.exc_info)
        
        return json.dumps(log_entry, ensure_ascii=False)

class Logger:
    """
    Logger wrapper class providing structured logging
    Equivalent to Go Zap Logger functionality
    """
    
    def __init__(self, name: str = "app", log_level: str = "info"):
        """
        Initialize logger with specified name and log level
        
        Args:
            name: Logger name
            log_level: Log level (debug, info, warn, error, fatal)
        """
        self.name = name
        self._logger = self._setup_logger(name, log_level)
    
    def _setup_logger(self, name: str, log_level: str) -> logging.Logger:
        """Setup and configure the logger"""
        # Create logger
        logger = logging.getLogger(name)
        
        # Set log level
        level = self._get_log_level(log_level)
        logger.setLevel(level)
        
        # Remove existing handlers to avoid duplicates
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
        
        # Create handlers
        stdout_handler = logging.StreamHandler(sys.stdout)
        stderr_handler = logging.StreamHandler(sys.stderr)
        
        # Set handler levels
        stdout_handler.setLevel(logging.DEBUG)
        stderr_handler.setLevel(logging.ERROR)
        
        # Create formatter
        formatter = JSONFormatter()
        stdout_handler.setFormatter(formatter)
        stderr_handler.setFormatter(formatter)
        
        # Add handlers to logger
        logger.addHandler(stdout_handler)
        logger.addHandler(stderr_handler)
        
        # Prevent propagation to avoid duplicate logs
        logger.propagate = False
        
        return logger
    
    def _get_log_level(self, log_level: str) -> int:
        """Convert string log level to logging level constant"""
        level_map = {
            "debug": logging.DEBUG,
            "info": logging.INFO,
            "warn": logging.WARNING,
            "error": logging.ERROR,
            "fatal": logging.CRITICAL
        }
        return level_map.get(log_level.lower(), logging.INFO)
    
    def _log(self, level: int, msg: str, **fields):
        """Internal log method with fields support"""
        # Create log record
        record = self._logger.makeRecord(
            name=self._logger.name,
            level=level,
            fn="",
            lno=0,
            msg=msg,
            args=(),
            exc_info=None
        )
        
        # Add custom fields
        record.fields = fields
        
        # Handle the record
        self._logger.handle(record)
    
    def debug(self, msg: str, **fields):
        """
        Log a message at DEBUG level
        
        Args:
            msg: Log message
            **fields: Additional structured fields
        """
        if self._logger.isEnabledFor(logging.DEBUG):
            self._log(logging.DEBUG, msg, **fields)
    
    def info(self, msg: str, **fields):
        """
        Log a message at INFO level
        
        Args:
            msg: Log message
            **fields: Additional structured fields
        """
        if self._logger.isEnabledFor(logging.INFO):
            self._log(logging.INFO, msg, **fields)
    
    def warn(self, msg: str, **fields):
        """
        Log a message at WARNING level
        
        Args:
            msg: Log message
            **fields: Additional structured fields
        """
        if self._logger.isEnabledFor(logging.WARNING):
            self._log(logging.WARNING, msg, **fields)
    
    def warning(self, msg: str, **fields):
        """Alias for warn method"""
        self.warn(msg, **fields)
    
    def error(self, msg: str, **fields):
        """
        Log a message at ERROR level
        
        Args:
            msg: Log message
            **fields: Additional structured fields
        """
        if self._logger.isEnabledFor(logging.ERROR):
            self._log(logging.ERROR, msg, **fields)
    
    def fatal(self, msg: str, **fields):
        """
        Log a message at CRITICAL level and exit
        
        Args:
            msg: Log message
            **fields: Additional structured fields
        """
        self._log(logging.CRITICAL, msg, **fields)
        self.sync()
        sys.exit(1)
    
    def critical(self, msg: str, **fields):
        """
        Log a message at CRITICAL level (alias for fatal without exit)
        
        Args:
            msg: Log message
            **fields: Additional structured fields
        """
        self._log(logging.CRITICAL, msg, **fields)
    
    def exception(self, msg: str, **fields):
        """
        Log an exception with stack trace
        
        Args:
            msg: Log message
            **fields: Additional structured fields
        """
        # Get current exception info
        import sys
        exc_info = sys.exc_info()
        
        if exc_info and exc_info[0] is not None:
            record = self._logger.makeRecord(
                name=self._logger.name,
                level=logging.ERROR,
                fn="",
                lno=0,
                msg=msg,
                args=(),
                exc_info=exc_info
            )
            record.fields = fields
            self._logger.handle(record)
        else:
            self.error(msg, **fields)
    
    def sync(self):
        """Flush any buffered log entries"""
        for handler in self._logger.handlers:
            if hasattr(handler, 'flush'):
                handler.flush()
    
    def set_level(self, log_level: str):
        """
        Change the log level dynamically
        
        Args:
            log_level: New log level (debug, info, warn, error, fatal)
        """
        level = self._get_log_level(log_level)
        self._logger.setLevel(level)
    
    def add_field(self, key: str, value: Any):
        """
        Add a persistent field to all future log messages
        
        Args:
            key: Field name
            value: Field value
        """
        if not hasattr(self._logger, 'persistent_fields'):
            self._logger.persistent_fields = {}
        self._logger.persistent_fields[key] = value

def new_logger(log_level: str = "info", name: str = "app") -> Logger:
    """
    Factory function to create a new logger instance
    Equivalent to Go's NewLogger function
    
    Args:
        log_level: Log level (debug, info, warn, error, fatal)
        name: Logger name
        
    Returns:
        Logger instance
    """
    return Logger(name=name, log_level=log_level)

def get_logger(name: str = "app") -> Logger:
    """
    Get or create a logger with the specified name
    
    Args:
        name: Logger name
        
    Returns:
        Logger instance
    """
    log_level = os.getenv('LOG_LEVEL', 'info')
    return Logger(name=name, log_level=log_level)

# Global logger instance for simple usage
_default_logger = None

def get_default_logger() -> Logger:
    """Get the default logger instance"""
    global _default_logger
    if _default_logger is None:
        log_level = os.getenv('LOG_LEVEL', 'info')
        _default_logger = Logger(name="app", log_level=log_level)
    return _default_logger

# Convenience functions for direct logging
def debug(msg: str, **fields):
    """Log debug message using default logger"""
    get_default_logger().debug(msg, **fields)

def info(msg: str, **fields):
    """Log info message using default logger"""
    get_default_logger().info(msg, **fields)

def warn(msg: str, **fields):
    """Log warning message using default logger"""
    get_default_logger().warn(msg, **fields)

def error(msg: str, **fields):
    """Log error message using default logger"""
    get_default_logger().error(msg, **fields)

def fatal(msg: str, **fields):
    """Log fatal message using default logger and exit"""
    get_default_logger().fatal(msg, **fields)

def exception(msg: str, **fields):
    """Log exception using default logger"""
    get_default_logger().exception(msg, **fields)

# Usage Examples and Documentation
"""
Usage Examples:

1. Basic Usage:
   from logger.logger import new_logger
   
   logger = new_logger("info", "my_service")
   logger.info("Service started", service="user_service", port=8080)

2. With Error Codes:
   from logger.logger import get_logger
   from error_codes.error_codes import ErrorCode, ApplicationError
   
   logger = get_logger("user_service")
   
   try:
       # Some operation
       pass
   except Exception as e:
       logger.error("Operation failed", 
                   error=str(e), 
                   error_code="GIRUDO_SQL_005",
                   user_id=123)

3. Convenience Functions:
   from logger.logger import info, error, debug
   
   info("User created", user_id=123, email="user@example.com")
   error("Database connection failed", host="localhost", port=5432)
   debug("Processing request", request_id="abc-123")

4. Exception Logging:
   try:
       # Some operation that might fail
       pass
   except Exception:
       logger.exception("Unexpected error occurred", 
                       operation="user_creation",
                       user_id=123)

5. Environment Configuration:
   # Set LOG_LEVEL environment variable
   # LOG_LEVEL=debug python main.py
   
   logger = get_logger()  # Uses LOG_LEVEL from environment

Output Format:
{
  "time": "2024-01-15T10:30:45.123Z",
  "level": "INFO",
  "logger": "user_service",
  "msg": "User created successfully",
  "caller": "user_service.py:45",
  "user_id": 123,
  "email": "user@example.com"
}
"""