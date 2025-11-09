# Logging and Correlation ID Implementation

## Overview

The prescription service now includes comprehensive logging with correlation ID support for distributed tracing across requests.

## Features

- ✅ Structured logging with correlation IDs
- ✅ Automatic correlation ID generation
- ✅ Support for X-Correlation-ID and X-Request-ID headers
- ✅ Correlation ID in response headers
- ✅ INFO and ERROR level logging (no debug logs)
- ✅ Contextual logging across the entire request lifecycle

## Architecture

### Components

1. **Logger Utility** (`app/utils/logger.py`)
   - `setup_logger()`: Creates logger with correlation ID support
   - `set_correlation_id()`: Sets correlation ID for current request context
   - `get_correlation_id()`: Retrieves current correlation ID
   - `clear_correlation_id()`: Clears correlation ID after request

2. **Correlation ID Middleware** (`app/middleware/__init__.py`)
   - Extracts correlation ID from request headers
   - Generates new correlation ID if not provided
   - Adds correlation ID to response headers
   - Manages correlation ID lifecycle

3. **Log Format**
   ```
   YYYY-MM-DD HH:MM:SS - [correlation-id] - module.name - LEVEL - message
   ```

## Usage

### Making Requests with Correlation ID

#### Option 1: Client provides correlation ID
```bash
curl -H "X-Correlation-ID: my-custom-id-123" \
  http://localhost:8000/api/v1/prescriptions/1
```

#### Option 2: Server generates correlation ID
```bash
curl http://localhost:8000/api/v1/prescriptions/1
```

### Response Headers

Every response includes the correlation ID:
```
X-Correlation-ID: abc123-def456-ghi789
```

### Log Output Example

```
2024-01-15 10:30:45 - [abc123-def456-ghi789] - app.routes.prescription - INFO - Fetching prescription with id=1
2024-01-15 10:30:45 - [abc123-def456-ghi789] - app.routes.prescription - INFO - Successfully fetched prescription with id=1
```

## Logging Levels Used

### INFO Level
- Request started/completed
- Database operations (create, fetch, etc.)
- Data seeding and initialization
- Successful operations

### ERROR Level
- Failed database operations
- Validation errors
- HTTP exceptions
- Database connection failures
- CSV file not found
- Any unexpected errors

## Tracing a Request

To trace a specific request through the logs:

```bash
# Make a request with custom correlation ID
curl -H "X-Correlation-ID: trace-123" \
  -X POST http://localhost:8000/api/v1/prescriptions/ \
  -H "Content-Type: application/json" \
  -d '{
    "appointment_id": 1,
    "patient_id": 40,
    "doctor_id": 21,
    "medication": "Paracetamol",
    "dosage": "0-1-1",
    "days": 5
  }'

# Search logs for that correlation ID
docker-compose logs app | grep "trace-123"
```

Output:
```
2024-01-15 10:30:45 - [trace-123] - app.routes.prescription - INFO - Creating prescription for appointment_id=1, patient_id=40
2024-01-15 10:30:45 - [trace-123] - app.services.prescription_service - INFO - Created prescription: id=301, appointment_id=1
2024-01-15 10:30:45 - [trace-123] - app.routes.prescription - INFO - Successfully created prescription with id=301
```

## Implementation Details

### Context Variables

The correlation ID is stored using Python's `contextvars`, which provides isolation between concurrent requests:

```python
from contextvars import ContextVar

correlation_id_var: ContextVar[Optional[str]] = ContextVar('correlation_id', default=None)
```

This ensures that each request has its own correlation ID, even in async environments.

### Middleware Order

The correlation ID middleware must be added **before** other middlewares:

```python
# Add Correlation ID middleware first
app.add_middleware(CorrelationIdMiddleware)

# Then add CORS and other middlewares
app.add_middleware(CORSMiddleware, ...)
```

## Logged Operations

### Application Lifecycle
- ✅ Application startup
- ✅ Application shutdown
- ✅ Database connection attempts
- ✅ Database schema creation
- ✅ Data seeding

### API Operations
- ✅ Create prescription
- ✅ Get prescription by ID
- ✅ Get all prescriptions (with filters)
- ✅ Get prescriptions by patient
- ✅ Get prescriptions by doctor
- ✅ Get prescriptions by appointment

### Error Scenarios
- ✅ Prescription not found
- ✅ Database errors
- ✅ Validation errors
- ✅ CSV file errors
- ✅ Connection failures

## Testing Correlation ID

### Test Script

```python
import requests

# Test 1: Server generates correlation ID
response = requests.get('http://localhost:8000/api/v1/prescriptions/1')
print(f"Generated ID: {response.headers.get('X-Correlation-ID')}")

# Test 2: Client provides correlation ID
headers = {'X-Correlation-ID': 'test-12345'}
response = requests.get('http://localhost:8000/api/v1/prescriptions/1', headers=headers)
print(f"Client ID: {response.headers.get('X-Correlation-ID')}")
```

### Expected Results

1. Each request gets a unique correlation ID
2. Client-provided IDs are preserved
3. Same correlation ID appears in all logs for a request
4. Correlation ID is returned in response headers

## Benefits

1. **Distributed Tracing**: Track requests across multiple services
2. **Debugging**: Quickly find all logs related to a specific request
3. **Monitoring**: Correlate errors with specific user actions
4. **Performance**: Identify slow operations for specific requests
5. **Auditing**: Complete audit trail with correlation IDs

## Integration with External Services

When calling external services (e.g., appointment service), forward the correlation ID:

```python
from app.utils.logger import get_correlation_id
import httpx

correlation_id = get_correlation_id()
headers = {'X-Correlation-ID': correlation_id}

response = httpx.get('http://appointment-service/api/appointments/1', headers=headers)
```

## Production Considerations

1. **Log Aggregation**: Use tools like ELK Stack, Splunk, or CloudWatch
2. **Search**: Index logs by correlation ID for fast searching
3. **Retention**: Keep logs for compliance and debugging
4. **Monitoring**: Alert on ERROR level logs
5. **Performance**: Logging is async and doesn't block requests

## Future Enhancements

- [ ] Add request duration logging
- [ ] Add user ID to log context
- [ ] Integrate with OpenTelemetry
- [ ] Add log sampling for high-traffic environments
- [ ] Export logs to centralized logging system

