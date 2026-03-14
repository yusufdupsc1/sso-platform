"""
Core app URLs.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('sso/initiate/', views.SSOInitiateView.as_view({'post': 'create'}), 
    path('sso/callback/', views.SSOCallbackView.as_view({'post': 'create'})),
]
