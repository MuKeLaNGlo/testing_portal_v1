from rest_framework import permissions


class IsInterwierOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated and request.user.is_interviewer)
        )

    def has_object_permission(self, request, view, obj):
        return (
            (request.user.is_interviewer and obj.author == request.user)
            or request.method in permissions.SAFE_METHODS
        )

class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )
