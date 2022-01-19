from django.contrib.auth import get_user_model
from rest_framework import permissions

from .utils import check_role

User = get_user_model()


class ReadOrAdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or check_role(request, User.ADMIN))


class AdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (check_role(request, User.ADMIN))


class AuthorOrAdminOrModeratorOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (request.user.is_authenticated
                and (request.user.is_admin
                     or request.user.is_moderator
                     or obj.author == request.user))
