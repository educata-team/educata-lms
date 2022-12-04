from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS
from rest_framework.exceptions import PermissionDenied

from .models import *


class CreateUpdateDeletePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            if request.user.is_authenticated and (request.user.role == 'moderator' or request.user.role == 'lecturer'):
                return True
            else:
                raise PermissionDenied({'detail': 'You do not have permission'})
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        if request.user.is_anonymous:
            raise PermissionDenied({'detail': 'You do not have permission'})

        if request.user.role == 'moderator' or request.user == obj.owner:
            return True

        if request.method not in SAFE_METHODS:

            if request.user.is_anonymous:
                raise PermissionDenied({'detail': 'You do not have permission'})

            if request.user == obj.owner or request.user.role == 'moderator':
                return True

            if request.method == 'PUT' or request.method == 'PATCH':
                editors = obj.editors.all()
                managers = obj.managers.all()
                if request.user in editors or request.user in managers:
                    return True
            if not request.user.role == 'lecturer':
                raise PermissionDenied({'detail': 'You do not have permission'})
        raise PermissionDenied({'detail': 'You do not have permission'})


class AttendedCoursePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE':
            if request.user == obj.user or request.user == obj.course.owner or request.user in obj.course.managers.all()\
                    or request.user.role == 'moderator':
                return True
        return False


class UnitPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            if request.user.is_anonymous:
                raise PermissionDenied({'detail': 'You do not have permission'})

            try:
                course = Course.objects.get(pk=view.kwargs.get('course_pk'))
                if request.user in course.editors.all() or request.user in course.managers.all() \
                        or request.user == course.owner or request.user.role == 'moderator':
                    return True
                raise PermissionDenied({'detail': 'You do not have permission'})
            except Course.DoesNotExist:
                pass
        return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            raise PermissionDenied({'detail': 'You do not have permission'})
        elif request.user in obj.course.editors.all() or request.user in obj.course.managers.all() \
                or request.user == obj.course.owner or request.user.role == 'moderator':
            return True
        else:
            raise PermissionDenied({'detail': 'You do not have permission'})


class ReviewPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.user == obj.user or request.user.is_admin or request.user.role == 'moderator':
            return True


class AssignmentPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            raise PermissionDenied({'detail': 'You do not have permission'})

        if request.method == 'POST':
            try:
                unit = Unit.objects\
                    .select_related('course', 'course__owner')\
                    .prefetch_related('course__managers', 'course__editors')\
                    .get(pk=view.kwargs.get('unit_pk'))
            except (Unit.DoesNotExist, KeyError, AttributeError):
                return True
            if request.user in unit.course.editors.all() or request.user in unit.course.managers.all() \
                    or request.user == unit.course.owner or request.user.role == 'moderator':
                return True
            else:
                raise PermissionDenied({'detail': 'You do not have permission'})
        try:
            unit = Unit.objects.select_related('course').prefetch_related('course__attendedcourse_set').get(pk=view.kwargs.get('unit_pk'))

            # check if user from request has subscription on the unit`s course
            if request.user in [attended_course.user for attended_course in unit.course.attendedcourse_set.all()] \
                    or request.user.role == 'moderator' or request.user in unit.course.editors.all() or request.user in unit.course.managers.all() \
                    or request.user == unit.course.owner:
                return True
            else:
                raise PermissionDenied({'detail': 'You do not have permission'})
        except (AttributeError, KeyError, Unit.DoesNotExist):
            return True
        raise PermissionDenied({'detail': 'You do not have permission'})

    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            raise PermissionDenied({'detail': 'You do not have permission'})
        elif request.user in obj.unit.course.editors.all() or request.user in obj.unit.course.managers.all() \
                or request.user == obj.unit.course.owner or request.user.role == 'moderator':
            return True
        else:
            raise PermissionDenied({'detail': 'You do not have permission'})
