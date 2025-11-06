# Use official Python runtime as base image
FROM python:3.11-slim

# Set working directory in container
WORKDIR /app


# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    default-libmysqlclient-dev \
    pkg-config && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .


# Expose port
EXPOSE 3001

# Health check

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3001"]

