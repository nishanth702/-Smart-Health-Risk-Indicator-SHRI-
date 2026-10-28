# Multi-stage lightweight production Dockerfile for SHRI Microservice
FROM python:3.11-slim as builder

WORKDIR /app

# Install system build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt fastapi uvicorn pydantic

# Production runner image
FROM python:3.11-slim

WORKDIR /app

# Create non-root clinical user for enterprise security
RUN groupadd -r shriuser && useradd -r -g shriuser shriuser

# Copy installed wheels from builder
COPY --from=builder /root/.local /home/shriuser/.local
ENV PATH=/home/shriuser/.local/bin:$PATH

# Copy application source code
COPY . .
RUN chown -R shriuser:shriuser /app

USER shriuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
