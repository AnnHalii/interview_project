import pytest
from django.urls import reverse

from ..models import RedirectRule

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    "url_data, expected_status",
    [
        ({"redirect_url": "https://example.com", "is_private": False}, 201),
        ({"redirect_url": "https://google.com", "is_private": True}, 201),
        ({"redirect_url": "https://youtube.com"}, 201),
        ({"is_private": True}, 400),
        ({}, 400),
        ({"redirect_url": "not-a-url", "is_private": False}, 400),
    ],
)
def test_create_redirect_rule(admin_auth_client, url_data, expected_status):
    """
    Test creating a RedirectRule with various data.
    """
    url = reverse("url-list")
    response = admin_auth_client.post(url, url_data)
    assert response.status_code == expected_status


def test_create_redirect_rule_without_auth(api_client):
    """
    Test creating a RedirectRule without authentication.
    """
    url = reverse("url-list")
    url_data = {"redirect_url": "https://example.com", "is_private": False}
    response = api_client.post(url, url_data)
    assert response.status_code == 401


def test_list_redirect_rules(regular_user, regular_auth_client, admin_user_rule):
    """
    Test listing all RedirectRules. All users should only see their own rules.
    """
    regular_rule_1 = RedirectRule.objects.create(
        redirect_url="https://example.com", is_private=False, owner=regular_user
    )
    regular_rule_2 = RedirectRule.objects.create(
        redirect_url="https://exampletest.com", is_private=True, owner=regular_user
    )

    url = reverse("url-list")
    response = regular_auth_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 2
    assert response.data[0]["id"] == str(regular_rule_1.id)
    assert response.data[1]["id"] == str(regular_rule_2.id)
    assert RedirectRule.objects.filter(id=admin_user_rule.id).exists()


@pytest.mark.parametrize(
    "url_data, expected_status",
    [
        ({"is_private": True}, 200),
        ({"redirect_url": "invalid-url"}, 400),
        ({"is_private": False}, 200),
    ],
)
def test_update_redirect_rule_as_owner(
    admin_user_rule, admin_auth_client, url_data, expected_status
):
    """
    Test updating a RedirectRule. Users can update only their rules.
    """
    url = reverse("url-detail", args=[admin_user_rule.id])
    response = admin_auth_client.patch(url, url_data)
    assert response.status_code == expected_status


def test_update_redirect_rule_as_non_owner(regular_user_rule, admin_auth_client):
    """
    Test that a non-owner cannot update a RedirectRule.
    """
    assert RedirectRule.objects.filter(id=regular_user_rule.id).exists()
    url = reverse("url-detail", args=[regular_user_rule.id])
    data = {"redirect_url": "https://updated-url.com", "is_private": True}

    response = admin_auth_client.patch(url, data, format="json")

    assert response.status_code == 404


def test_delete_redirect_rule_as_owner(regular_auth_client, regular_user_rule):
    """
    Test that the owner of a RedirectRule can delete their own rule.
    """
    url = reverse("url-detail", args=[regular_user_rule.id])
    response = regular_auth_client.delete(url)

    assert response.status_code == 204
    assert not RedirectRule.objects.filter(id=regular_user_rule.id).exists()


def test_delete_redirect_rule_as_non_owner(regular_user_rule, admin_auth_client):
    """
    Test that a non-owner cannot delete a RedirectRule.
    """
    url = reverse("url-detail", args=[regular_user_rule.id])
    response = admin_auth_client.delete(url)

    assert response.status_code == 404
    assert RedirectRule.objects.filter(id=regular_user_rule.id).exists()
