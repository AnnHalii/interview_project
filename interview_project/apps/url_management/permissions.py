from rest_framework import permissions


class IsRuleOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of a RedirectRule to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
