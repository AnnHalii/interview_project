from django.shortcuts import get_object_or_404, redirect
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from interview_project.apps.url_management.models import RedirectRule


class PublicRedirectView(APIView):
    """
    Handles public redirects. No authentication required.
    """
    authentication_classes = []
    permission_classes = []

    def get(self, request, redirect_identifier):
        """
        Find a public RedirectRule by its identifier and redirect to its URL.
        """
        rule = get_object_or_404(
            RedirectRule, redirect_identifier=redirect_identifier, is_private=False
        )
        return redirect(rule.redirect_url)


class PrivateRedirectView(APIView):
    """
    Handles private redirects. Authentication is required.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, redirect_identifier):
        """
        Find a private RedirectRule by its identifier and redirect to its URL.
        Only accessible by authenticated users.
        """
        rule = get_object_or_404(
            RedirectRule, redirect_identifier=redirect_identifier, is_private=True
        )
        return redirect(rule.redirect_url)
