from rest_framework import permissions


class NotAllowedUpdateAndDeletePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.method in permissions.SAFE_METHODS:
                return True

            if request.method in ('DELETE', 'PATCH'):
                return False

            if request.method == 'PUT' and request.user.role == 1:
                return True

            if request.method == 'POST' and request.user.role == 0:
                return True
        return False