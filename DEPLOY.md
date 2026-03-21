# Production Deployment Guide

This platform is containerized for production deployment.

## Mandatory Environment Variables

The following environment variables MUST be set for the application to function in production:

- `DJANGO_SECRET_KEY`: A strong, random string used for cryptographic signing.
- `DATABASE_URL`: Connection string for PostgreSQL (e.g., `postgres://user:password@localhost:5432/dbname`).
- `ALLOWED_HOSTS`: Comma-separated list of allowed hostnames (e.g., `sso.example.com`).

## Deployment Steps

1.  **Build the Image:**
    ```bash
    docker build -t sso-platform:latest .
    ```

2.  **Run Migrations:**
    ```bash
    docker run --rm \
      -e DATABASE_URL=$DATABASE_URL \
      -e DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY \
      sso-platform:latest \
      python manage.py migrate
    ```

3.  **Run Production Container:**
    Run with appropriate environment variables. It is recommended to use a reverse proxy (like Nginx) in front of the container.
    ```bash
    docker run -d \
      --name sso-platform \
      -e DATABASE_URL=$DATABASE_URL \
      -e DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY \
      -e ALLOWED_HOSTS=$ALLOWED_HOSTS \
      -p 8000:8000 \
      --restart unless-stopped \
      sso-platform:latest
    ```
