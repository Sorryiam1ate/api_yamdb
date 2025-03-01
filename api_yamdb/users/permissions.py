from rest_framework import permissions

from .models import User

user = User.objects.all()


class AdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            (request.method in permissions.SAFE_METHODS)
            or (request.user.is_authenticated and request.user.is_admin)
        )


class AdminOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.is_admin)


class IsAuthorOrModerOrAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or (
                request.user.is_admin
                or request.user.is_moderator
                or obj.author == request.user
            )
        )
