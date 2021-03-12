from rest_framework import permissions


class IsCartOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of cart.
    """

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
