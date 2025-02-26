from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import RedirectRule
from .permissions import IsRuleOwner
from .serializers import RedirectRuleSerializer


class RedirectRuleViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing RedirectRule instances.

    - Users can only see, update, or delete their own redirect rules.
    - Authentication is required for all operations.

    Permissions:
    - `IsAuthenticated`: Only authenticated users can access this view.
    - `IsRuleOwner`: Users can only modify or delete their own redirect rules.

    Endpoints:
    - `GET /redirects/` → List all redirect rules of the authenticated user(if owned/exists).
    - `GET /redirects/{id}/` → Retrieve details of a specific redirect rule (if owned).
    - `POST /redirects/` → Create a new redirect rule (assigned to the current user).
    - `PATCH /redirects/{id}/` → Partially update a redirect rule (if owned).
    - `DELETE /redirects/{id}/` → Delete a redirect rule (if owned).
    """

    serializer_class = RedirectRuleSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsRuleOwner]

    def get_queryset(self):
        """
        Returns the RedirectRules that belong to the currently authenticated user.
        """
        return RedirectRule.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        """
        Attach the current user as the owner when a RedirectRule is created.
        """
        serializer.save(owner=self.request.user)
