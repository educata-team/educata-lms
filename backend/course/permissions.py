from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS

from .models import *


class CreateUpdateDeletePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):

        if request.method not in SAFE_METHODS:

            if request.user.is_anonymous:
                return False

            if request.user == obj.owner or request.user.is_admin:
                return True

            if request.method == 'PUT' or request.method == 'PATCH':
                editors = obj.editors.set.all()
                managers = obj.managers.set.all()
                if request.user in editors or request.user in managers:
                    return True
            if not request.user.role == 'lecturer':
                return False
        return False


class AttendedCoursePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ('PUT', 'PATCH'):
            return False
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE':
            if request.user == obj.user or request.user == obj.course.owner or request.user in obj.course.managers.all():
                return True
        return False


class ReviewPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.user == obj.user or request.user.is_admin:
            return True
