from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from app.utils.logger import set_correlation_id, clear_correlation_id, get_correlation_id


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    """Middleware to handle correlation ID for request tracing"""

    async def dispatch(self, request: Request, call_next):
        # Get correlation ID from header or generate new one
        correlation_id = request.headers.get('X-Correlation-ID') or request.headers.get('X-Request-ID')
        correlation_id = set_correlation_id(correlation_id)

        # Add correlation ID to response headers
        response = await call_next(request)
        response.headers['X-Correlation-ID'] = correlation_id

        # Clear after request
        clear_correlation_id()

        return response

