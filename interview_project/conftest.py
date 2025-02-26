import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken

from interview_project.apps.url_management.models import RedirectRule


@pytest.fixture
def admin_user():
    """Fixture to create an admin user."""
    return User.objects.create_user(
        username="adminuser", password="adminpassword", is_staff=True
    )


@pytest.fixture
def regular_user():
    """Fixture to create a regular user."""
    return User.objects.create_user(
        username="regularuser", password="userpassword", is_staff=False
    )


@pytest.fixture
def api_client():
    """Fixture for API client."""
    return APIClient()


@pytest.fixture
def admin_auth_client(api_client, admin_user):
    """Fixture to get a client with JWT auth for the admin user."""
    access_token = AccessToken.for_user(admin_user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    return api_client


@pytest.fixture
def regular_auth_client(api_client, regular_user):
    """Fixture to get a client with JWT auth for the regular user."""
    access_token = AccessToken.for_user(regular_user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    return api_client


@pytest.fixture
def admin_user_rule(admin_user):
    return RedirectRule.objects.create(
        redirect_url="https://adminexample.com", is_private=False, owner=admin_user
    )


@pytest.fixture
def regular_user_rule(regular_user):
    return RedirectRule.objects.create(
        redirect_url="https://example.com", is_private=False, owner=regular_user
    )
