import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_health_check(client):
    # Just a simple dummy test to verify setup
    assert True
