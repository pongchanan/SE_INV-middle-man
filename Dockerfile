FROM python:3.11-slim as builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    netcat-traditional \
    postgresql-client \
    libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Final stage
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    netcat-traditional \
    postgresql-client \
    libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN useradd -m myuser && \
    chown -R myuser:myuser /app

# Copy wheels from builder
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

# Install dependencies
RUN pip install --no-cache /wheels/*

# Copy project files
COPY . .

# Create necessary directories
RUN mkdir -p /app/static /app/staticfiles && \
    chown -R myuser:myuser /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Remove Django settings and configure FastAPI environment
ENV ENVIRONMENT=development
ENV PYTHONPATH=/app

# Switch to non-root user
USER myuser

# Expose port
EXPOSE 8000

# Run FastAPI via uvicorn in development mode
CMD ["fastapi", "dev", "src/main.py"]