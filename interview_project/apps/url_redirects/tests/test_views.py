import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_public_redirect(api_client, regular_user_rule):
    """
    Test that a public redirect rule correctly redirects without authentication.
    """

    url = reverse("public-redirect", args=[regular_user_rule.redirect_identifier])
    response = api_client.get(url, follow=False)

    assert response.status_code == 302
    assert response["Location"] == regular_user_rule.redirect_url


def test_public_redirect_authenticated(regular_auth_client, regular_user_rule):
    """
    Test that an authenticated user can access a public redirect rule.
    """
    url = reverse("public-redirect", args=[regular_user_rule.redirect_identifier])
    response = regular_auth_client.get(url, follow=False)

    assert response.status_code == 302
    assert response["Location"] == regular_user_rule.redirect_url


def test_public_redirect_not_found(api_client):
    """
    Test that accessing a non-existent public redirect returns 404.
    """
    url = reverse("public-redirect", args=["nonexistent123"])
    response = api_client.get(url)

    assert response.status_code == 404


def test_private_redirect_authenticated(regular_auth_client, admin_user_rule):
    """
    Test that an authenticated user can access a private redirect rule.
    """
    admin_user_rule.is_private = True
    admin_user_rule.save()

    url = reverse("private-redirect", args=[admin_user_rule.redirect_identifier])
    response = regular_auth_client.get(url, follow=False)

    assert response.status_code == 302
    assert response["Location"] == admin_user_rule.redirect_url


def test_private_redirect_unauthenticated(api_client, admin_user_rule):
    """
    Test that an unauthenticated user cannot access a private redirect rule.
    """
    admin_user_rule.is_private = True
    admin_user_rule.save()

    url = reverse("private-redirect", args=[admin_user_rule.redirect_identifier])
    response = api_client.get(url)

    assert response.status_code == 401


def test_private_redirect_not_found(regular_auth_client):
    """
    Test that accessing a non-existent private redirect returns 404.
    """
    url = reverse("private-redirect", args=["nonexistent123"])
    response = regular_auth_client.get(url)

    assert response.status_code == 404
