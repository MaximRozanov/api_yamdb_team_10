from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or bool(request.user and request.user.is_staff))


class AdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
                request.user.is_admin
                or request.user.is_staff
        )

    def has_object_permission(self, request, view, obj):
        return (
                request.user.is_admin
                or request.user.is_staff
        )


class ModeratorAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
                request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
                request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.is_moderator
                or request.user.is_admin
        )


# SAFE_METHODS - все, добавлять - авторизированные, менять author Модератор или Админ
class IsOwnerOrModeratorAdmin(permissions.BasePermission):
    pass
