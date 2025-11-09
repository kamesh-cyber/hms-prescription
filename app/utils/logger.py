import logging
import sys
from contextvars import ContextVar
from typing import Optional
import uuid

# Context variable to store correlation ID
correlation_id_var: ContextVar[Optional[str]] = ContextVar('correlation_id', default=None)


class CorrelationIdFilter(logging.Filter):
    """Filter to add correlation ID to log records"""

    def filter(self, record):
        record.correlation_id = correlation_id_var.get() or "no-correlation-id"
        return True


def setup_logger(name: str) -> logging.Logger:
    """
    Setup logger with correlation ID support

    Args:
        name: Logger name (usually __name__)

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)

    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    # Create console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)

    # Create formatter with correlation ID
    formatter = logging.Formatter(
        '%(asctime)s - [%(correlation_id)s] - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    handler.setFormatter(formatter)
    handler.addFilter(CorrelationIdFilter())

    logger.addHandler(handler)

    return logger


def set_correlation_id(correlation_id: Optional[str] = None) -> str:
    """
    Set correlation ID for current context

    Args:
        correlation_id: Correlation ID to set. If None, generates a new UUID

    Returns:
        The correlation ID that was set
    """
    if correlation_id is None:
        correlation_id = str(uuid.uuid4())

    correlation_id_var.set(correlation_id)
    return correlation_id


def get_correlation_id() -> Optional[str]:
    """
    Get current correlation ID from context

    Returns:
        Current correlation ID or None
    """
    return correlation_id_var.get()


def clear_correlation_id():
    """Clear correlation ID from current context"""
    correlation_id_var.set(None)

