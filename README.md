# SSO Platform

Multi-tenant SSO authentication platform built with Django.

## Features

- Multi-tenant SSO authentication.
- Support for OIDC and OAuth2 providers (Keycloak, Okta, Auth0, Azure AD).
- REST API for seamless integration.
- Production-ready Docker configuration.

## Project Structure

```text
.
├── accounts/           # User management
├── core/               # SSO core logic
├── sso_platform/       # Project configuration (settings, WSGI, URLs)
├── tests/              # Test suite
├── Dockerfile          # Production Dockerfile
├── docker-compose.yml  # Local development orchestration
├── requirements.txt    # Production dependencies
└── requirements-dev.txt# Development & CI dependencies
```

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Environment variables (see `.env.example`)

### Local Development

1. Clone the repository.
2. Create a `.env` file from `.env.example`.
3. Run the stack:
   ```bash
   docker-compose up
   ```

## Production Deployment

See [DEPLOY.md](DEPLOY.md) for detailed production deployment instructions.
