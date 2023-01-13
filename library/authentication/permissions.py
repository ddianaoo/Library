from rest_framework import permissions


class CustomUserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.method in permissions.SAFE_METHODS:
                return True


class IsSuperUserOrNotAuthenticate(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated or request.user.is_superuser:
            return True

        return False


class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser


class IsOwnerOrStaff(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # print(request.user.is_staff or request.user == obj)
        return request.user.is_staff or request.user == obj or request.user.role != 0


class IsOwnerOrSuperUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # print(request.user.is_superuser or request.user == obj)
        return request.user.is_superuser or request.user == obj


class IsNotAllowed(permissions.BasePermission):
    def has_permission(self, request, view):
        return False


class NotAuthenticate(permissions.BasePermission):
    def has_permission(self, request, view):
        print(not request.user.is_authenticated)
        return not request.user.is_authenticated
