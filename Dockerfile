# syntax=docker/dockerfile:1

# Stage 1: Builder
FROM python:3.11-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Final
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/home/appuser/.local/bin:${PATH}"

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home appuser

USER appuser
WORKDIR /app

COPY --from=builder /root/.local /home/appuser/.local
COPY . .

# Hugging Face requires listening on port 7860
EXPOSE 7860

# Use gunicorn with port 7860
CMD ["gunicorn", "--bind", "0.0.0.0:7860", "--workers", "3", "--access-logfile", "-", "sso_platform.wsgi:application"]
