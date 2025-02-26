import pytest
from django.contrib.auth.models import User
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_create_user_unauthenticated(api_client):
    """Test user creation unauthenticated."""
    url = reverse("user-list")
    data = {
        "username": "test",
        "email": "test@example.com",
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == 401


def test_create_user(admin_auth_client):
    """Test user creation."""
    url = reverse("user-list")
    data = {
        "username": "test",
        "email": "test@example.com",
    }
    response = admin_auth_client.post(url, data, format="json")

    assert response.status_code == 201
    assert User.objects.filter(username="test").exists()


def test_get_users(admin_auth_client):
    """Test retrieving the list of users."""
    url = reverse("user-list")
    response = admin_auth_client.get(url)

    assert response.status_code == 200


def test_get_user_detail(admin_auth_client, regular_user):
    """Test retrieving a single user by ID."""
    url = reverse("user-detail", kwargs={"pk": regular_user.id})
    response = admin_auth_client.get(url)

    assert response.status_code == 200
    assert response.data["username"] == regular_user.username


def test_update_user(admin_auth_client, regular_user):
    """Test updating a user."""
    url = reverse("user-detail", kwargs={"pk": regular_user.id})
    data = {"username": "updated_regular"}
    response = admin_auth_client.patch(url, data, format="json")

    assert response.status_code == 200
    regular_user.refresh_from_db()
    assert regular_user.username == "updated_regular"


def test_delete_user(admin_auth_client, regular_user):
    """Test deleting a user."""
    url = reverse("user-detail", kwargs={"pk": regular_user.id})
    response = admin_auth_client.delete(url)

    assert response.status_code == 204
    assert not User.objects.filter(id=regular_user.id).exists()


@pytest.mark.parametrize(
    "url, expected_status",
    [
        (reverse("user-list"), 403),
        (reverse("user-detail", kwargs={"pk": 1}), 403),
    ],
)
def test_regular_user_access(regular_auth_client, url, expected_status):
    """Test access control for regular users."""
    response = regular_auth_client.get(url)
    assert response.status_code == expected_status
