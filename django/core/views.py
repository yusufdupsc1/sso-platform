"""
API views for SSO Platform.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Tenant, SSOProvider, SSOUser
from .sso_service import get_provider_service


class TenantViewSet(viewsets.ModelViewSet):
    """Tenant CRUD operations."""
    queryset = Tenant.objects.all()
    serializer_class = None  # Add serializer
    permission_classes = [IsAuthenticated]


class SSOProviderViewSet(viewsets.ModelViewSet):
    """SSO Provider CRUD operations."""
    queryset = SSOProvider.objects.all()
    serializer_class = None
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SSOProvider.objects.filter(tenant__id=self.request.user.tenant_id)


class SSOInitiateView(viewsets.ViewSet):
    """Initiate SSO login."""

    def create(self, request):
        provider_id = request.data.get('provider_id')
        redirect_uri = request.data.get('redirect_uri')

        if not provider_id or not redirect_uri:
            return Response(
                {'error': 'provider_id and redirect_uri required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            provider = SSOProvider.objects.get(id=provider_id, is_active=True)
        except SSOProvider.DoesNotExist:
            return Response(
                {'error': 'Provider not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        service = get_provider_service(provider)
        auth_url, state = service.get_authorization_url(redirect_uri)

        return Response({
            'authorization_url': auth_url,
            'state': state,
        })


class SSOCallbackView(viewsets.ViewSet):
    """Handle SSO callback."""

    def create(self, request):
        code = request.data.get('code')
        state = request.data.get('state')
        provider_id = request.data.get('provider_id')
        redirect_uri = request.data.get('redirect_uri')

        if not code or not provider_id:
            return Response(
                {'error': 'code and provider_id required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            provider = SSOProvider.objects.get(id=provider_id, is_active=True)
        except SSOProvider.DoesNotExist:
            return Response(
                {'error': 'Provider not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        service = get_provider_service(provider)

        # Exchange code for tokens
        tokens = service.exchange_code(code, redirect_uri)

        # Get user info
        userinfo = service.get_userinfo(tokens['access_token'])

        # Validate ID token
        id_token = tokens.get('id_token')
        if id_token:
            claims = service.validate_token(id_token)

        # Create or update SSO user
        sso_user, created = SSOUser.objects.update_or_create(
            provider=provider,
            provider_user_id=userinfo.get('sub'),
            defaults={
                'email': userinfo.get('email'),
                'first_name': userinfo.get('given_name', ''),
                'last_name': userinfo.get('family_name', ''),
                'roles': claims.get('roles', []) if id_token else [],
                'last_login': timezone.now(),
            }
        )

        return Response({
            'success': True,
            'user': {
                'email': sso_user.email,
                'name': f"{sso_user.first_name} {sso_user.last_name}".strip(),
                'roles': sso_user.roles,
            },
        })


from django.utils import timezone
