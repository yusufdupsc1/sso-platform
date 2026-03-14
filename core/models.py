"""
Core models for SSO Platform.
"""

from django.db import models
from django.contrib.auth.models import AbstractUser


class Tenant(models.Model):
    """Tenant organization."""
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    domain = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tenants'

    def __str__(self):
        return self.name


class SSOProvider(models.Model):
    """SSO provider configuration."""
    PROVIDER_TYPES = [
        ('keycloak', 'Keycloak'),
        ('okta', 'Okta'),
        ('auth0', 'Auth0'),
        ('azure', 'Azure AD'),
    ]

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='providers')
    provider_type = models.CharField(max_length=50, choices=PROVIDER_TYPES)
    name = models.CharField(max_length=255)
    client_id = models.CharField(max_length=255)
    client_secret = models.CharField(max_length=255, blank=True)
    issuer_url = models.URLField()
    redirect_urls = models.JSONField(default=list)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'sso_providers'
        unique_together = ['tenant', 'provider_type']

    def __str__(self):
        return f"{self.tenant.name} - {self.provider_type}"


class SSOUser(models.Model):
    """User mapped from SSO provider."""
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    provider = models.ForeignKey(SSOProvider, on_delete=models.CASCADE)
    provider_user_id = models.CharField(max_length=255)
    email = models.EmailField()
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    roles = models.JSONField(default=list)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'sso_users'
        unique_together = ['provider', 'provider_user_id']

    def __str__(self):
        return self.email
