from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission, SAFE_METHODS

from .models import *
from course.models import Assignment, AttendedCourse


class FormInputPermission(BasePermission):
    # TODO: add permission to 'moderator' role
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            raise PermissionDenied({'detail': 'You do not have permission'})

        try:
            assignment = Assignment.objects.select_related('unit',
                                                           'unit__course',
                                                           'unit__course__owner',
                                                           'unit__course__managers',
                                                           'unit__course__editors').get(pk=request.data.get('assignment'))
        except:
            return True

        attended_courses = AttendedCourse.objects.select_related('course', 'user').filter(course__pk=assignment.unit.course.pk)
        if request.user in [attended_course.user for attended_course in attended_courses] or request.user:
            return True
        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            if request.user == assignment.unit.course.owner or request.user in assignment.unit.course.managers.all() \
                    or request.user in assignment.unit.course.editors.all():
                return True
            else:
                raise PermissionDenied({'detail': 'You do not have permission'})

        return True
