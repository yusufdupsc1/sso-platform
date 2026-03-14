"""
SSO Service - handles OAuth2/OIDC flow.
"""

import hashlib
import secrets
from urllib.parse import urlencode
from django.conf import settings


class SSOService:
    """Base SSO service handler."""

    def __init__(self, provider):
        self.provider = provider
        self.client_id = provider.client_id
        self.client_secret = provider.client_secret
        self.issuer_url = provider.issuer_url
        self.redirect_urls = provider.redirect_urls

    def get_authorization_url(self, redirect_uri, state=None):
        """Generate authorization URL."""
        if state is None:
            state = secrets.token_urlsafe(32)

        params = {
            'client_id': self.client_id,
            'redirect_uri': redirect_uri,
            'response_type': 'code',
            'scope': 'openid email profile',
            'state': state,
        }

        auth_endpoint = f"{self.issuer_url}/protocol/openid-connect/auth"
        return f"{auth_endpoint}?{urlencode(params)}", state

    def exchange_code(self, code, redirect_uri):
        """Exchange authorization code for tokens."""
        import requests

        token_url = f"{self.issuer_url}/protocol/openid-connect/token"

        data = {
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
            'redirect_uri': redirect_uri,
        }

        response = requests.post(token_url, data=data)
        response.raise_for_status()
        return response.json()

    def get_userinfo(self, access_token):
        """Fetch user info from provider."""
        import requests

        userinfo_url = f"{self.issuer_url}/protocol/openid-connect/userinfo"
        headers = {'Authorization': f'Bearer {access_token}'}

        response = requests.get(userinfo_url, headers=headers)
        response.raise_for_status()
        return response.json()

    def validate_token(self, id_token):
        """Validate ID token."""
        # In production, verify signature with JWKS
        # For now, decode and return claims
        import base64
        import json

        parts = id_token.split('.')
        if len(parts) != 3:
            raise ValueError("Invalid token format")

        payload = parts[1]
        # Add padding if needed
        padding = 4 - (len(payload) % 4)
        if padding != 4:
            payload += '=' * padding

        claims = json.loads(base64.urlsafe_b64decode(payload))
        return claims


class KeycloakService(SSOService):
    """Keycloak-specific implementation."""
    pass


class OktaService(SSOService):
    """Okta-specific implementation."""
    pass


class Auth0Service(SSOService):
    """Auth0-specific implementation."""
    pass


class AzureADService(SSOService):
    """Azure AD-specific implementation."""
    pass


def get_provider_service(provider):
    """Factory to get appropriate service."""
    services = {
        'keycloak': KeycloakService,
        'okta': OktaService,
        'auth0': Auth0Service,
        'azure': AzureADService,
    }
    service_class = services.get(provider.provider_type)
    if not service_class:
        raise ValueError(f"Unknown provider: {provider.provider_type}")
    return service_class(provider)
