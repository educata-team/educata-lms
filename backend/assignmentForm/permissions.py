from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission, SAFE_METHODS

from .models import *
from course.models import Assignment, AttendedCourse


class FormQuestionPermission(BasePermission):
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
                course__pk=assignment.unit.course.pk)
            if request.method in SAFE_METHODS:
                if request.user in [att_course.user for att_course in attended_courses] or request.user == assignment.unit.course.owner or request.user in assignment.unit.course.managers.all() \
                        or request.user in assignment.unit.course.editors.all() or request.user.role == 'moderator':
                    return True

            if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
                if request.user == assignment.unit.course.owner or request.user in assignment.unit.course.managers.all() \
                        or request.user in assignment.unit.course.editors.all() or request.user.role == 'moderator':
                    return True
                else:
                    raise PermissionDenied({'detail': 'You do not have permission'})
        except (Assignment.DoesNotExist, KeyError, AttributeError):
            return True
        raise PermissionDenied({'detail': 'You do not have permission'})

    def has_object_permission(self, request, view, obj):
        if request.user == obj.assignment.unit.course.owner or request.user in obj.assignment.unit.course.managers.all() \
                or request.user in obj.assignment.unit.course.editors.all() or request.user.role == 'moderator':
            return True
        else:
            raise PermissionDenied({'detail': 'You do not have permission'})


class OptionPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            raise PermissionDenied({'detail': 'You do not have permission'})

        if request.method in SAFE_METHODS:
            try:
                question = FormChoiceQuestion.objects \
                    .select_related('assignment', 'assignment__unit__course') \
                    .prefetch_related('assignment__unit__course__managers', 'assignment__unit__course__editors') \
                    .get(pk=request.data.get('question'))
                if request.user in question.assignment.unit.course.managers.all() or \
                        request.user in question.assignment.unit.course.editors.all() \
                        or request.user is question.assignment.unit.course.owner or request.user.role == 'manager':
                    return True
                raise PermissionDenied({'detail': 'You do not have permission'})
            except FormChoiceQuestion.DoesNotExist:
                return True

        if request.method == 'POST':
            if not len(set([instance.get('question') for instance in request.data])) > 1 and request.data:
                try:
                    question = FormChoiceQuestion.objects\
                        .select_related('assignment', 'assignment__unit__course')\
                        .prefetch_related('assignment__unit__course__managers', 'assignment__unit__course__editors') \
                        .get(pk=request.data[0].get('question'))
                except FormChoiceQuestion.DoesNotExist:
                    return True

                if not question.is_multiple_answer and [instance if instance.get('correct') else None for instance
                                                        in request.data]:
                    return PermissionDenied({'detail': 'In this question there could be only one correct answer'})

                if request.user in question.assignment.unit.course.editors.all() or request.user in question.assignment.unit.course.managers.all() \
                        or request.user is question.assignment.unit.course.owner or request.user.role == 'moderator':
                    return True
                raise PermissionDenied({'detail': 'You do not have permission'})
        return True
