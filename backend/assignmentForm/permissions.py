from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission, SAFE_METHODS

from .models import *
from course.models import Assignment, AttendedCourse


class FormInputPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            raise PermissionDenied({'detail': 'You do not have permission'})

        try:
            assignment_id = request.data.get('assignment_id') or request.data.get('assignment') or None
            assignment = Assignment.objects.select_related('unit',
                                                           'unit__course',
                                                           'unit__course__owner') \
                .prefetch_related('unit__course__managers',
                                  'unit__course__editors') \
                .get(pk=assignment_id)
            attended_courses = AttendedCourse.objects.select_related('course', 'user').filter(
                course__pk=assignment.unit.course.pk, user=request.user)

            if attended_courses or request.user == assignment.unit.course.owner or request.user in assignment.unit.course.managers.all() \
                    or request.user in assignment.unit.course.editors.all() or request.user.role == 'moderator':
                return True

            if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
                if request.user == assignment.unit.course.owner or request.user in assignment.unit.course.managers.all() \
                        or request.user in assignment.unit.course.editors.all() or request.user.role == 'moderator':
                    return True
                else:
                    raise PermissionDenied({'detail': 'You do not have permission'})
        except:
            pass
        raise PermissionDenied({'detail': 'You do not have permission'})

    def has_object_permission(self, request, view, obj):
        if request.user == obj.unit.course.owner or request.user in obj.unit.course.managers.all() \
                or request.user in obj.unit.course.editors.all() or request.user.role == 'moderator':
            return True
        else:
            raise PermissionDenied({'detail': 'You do not have permission'})
