from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing User instances.

    - Only admin users can perform any actions (list, retrieve, create, update, delete).
    - Authentication is enforced using JWT.
    - Regular users do not have access to this endpoint.

    Permissions:
    - `IsAdminUser`: Only users with admin privileges can access this view.

    Endpoints:
    - `GET /users/` → List all users (Admin only)
    - `GET /users/{id}/` → Retrieve a single user (Admin only)
    - `POST /users/` → Create a new user (Admin only)
    - `PATCH /users/{id}/` → Partially update a user (Admin only)
    - `DELETE /users/{id}/` → Delete a user (Admin only)
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
