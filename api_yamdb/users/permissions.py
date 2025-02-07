from rest_framework import permissions
from .models import User


user = User.objects.all()


class AdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return (
                User.objects.get(pk=request.user.id).is_admin
                or User.objects.get(pk=request.user.id).is_superuser
            )
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            User.objects.get(pk=request.user.id).is_admin
            or User.objects.get(pk=request.user.id).is_superuser
        )


class AdminOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return (
                User.objects.get(pk=request.user.id).is_admin
                or User.objects.get(pk=request.user.id).is_superuser
            )
        return False


class OnlyOwnAccount(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsAuthorOrModerOrAdmin(permissions.BasePermission):
    """Permission for Review and Comment"""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return (
                User.objects.get(pk=request.user.id).is_admin
                or User.objects.get(pk=request.user.id).is_moderator
                or (User.objects.get(pk=request.user.id).is_user
                    and request.user == User.objects.get(pk=request.user.id).id)
            )
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return (
                User.objects.get(pk=request.user.id).is_admin
                or User.objects.get(pk=request.user.id).is_moderator
                or (User.objects.get(pk=request.user.id).is_user
                    and request.user == obj.author)
            )
        return False
