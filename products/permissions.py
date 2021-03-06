from rest_framework.permissions import BasePermission


class IsAdminOrReadOnly(BasePermission):
    SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')

    def has_permission(self, request, view):
        return bool(
            request.method in self.SAFE_METHODS or
            request.user and
            request.user.is_staff
        )
