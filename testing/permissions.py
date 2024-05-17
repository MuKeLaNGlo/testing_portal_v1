from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView

from testing import models


class IsInterwierOrReadOnly(permissions.BasePermission):

    def has_permission(self, request: Request, view: APIView):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated and request.user.is_interviewer)
        )

    def has_object_permission(self, request: Request, view: APIView, obj: models.Test):
        return (
            (request.user.is_interviewer and obj.author == request.user)
            or (request.method in permissions.SAFE_METHODS)
            or request.user.is_staff
        )


class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    def has_permission(self, request: Request, view: APIView):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )
