# SSO Platform

Multi-tenant SSO authentication platform.

## Project Structure

```
sso-platform/
├── docker-compose.yml      # Full stack
├── django/                # Django API
│   ├── sso_platform/     # Django project
│   ├── core/              # SSO logic
│   └── requirements.txt
└── frontend/             # Next.js (placeholder)
```

## Features

- Multi-tenant SSO
- Multiple providers (Keycloak, Okta, Auth0, Azure AD)
- OAuth2/OIDC
- REST API

## Quick Start

```bash
docker compose up -d
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/sso/initiate/ | Start SSO login |
| POST | /api/sso/callback/ | Handle SSO callback |

## Tech Stack

- Django 4.2
- Django REST Framework
- PostgreSQL
- Docker
