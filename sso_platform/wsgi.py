"""
WSGI config for SSO Platform.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sso_platform.settings')

application = get_wsgi_application()
