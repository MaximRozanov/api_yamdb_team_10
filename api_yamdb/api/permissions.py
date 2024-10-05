from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_admin
        )


class AdminOnly(permissions.BasePermission):
    pass


class ModeratorAdmin(permissions.BasePermission):
    pass


# SAFE_METHODS - все, добавлять - авторизированные, менять author Модератор или Админ
class IsOwnerOrModeratorAdmin(permissions.BasePermission):
    pass
