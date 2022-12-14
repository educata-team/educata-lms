from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.exceptions import PermissionDenied

from assignment.models import AssignmentAnswer
from assignmentForm.models import FormInputQuestion, FormFileQuestion, FormChoiceQuestion
from course.models import Assignment, AttendedCourse


class AnswerAssignmentPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            raise PermissionDenied({'detail': 'You do not have permission'})
        try:
            assignment = Assignment.objects.prefetch_related('unit__course__managers',
                                                             'unit__course__evaluators',
                                                             'unit__course__editors',
                                                             'unit__course__attendedcourse_set').get(pk=request.data.get('assignment'))
        except Assignment.DoesNotExist:
            return True

        if request.method in SAFE_METHODS:
            if request.user in assignment.unit.course.editors.all() or request.user in assignment.unit.course.managers.all() \
                    or request.user in assignment.unit.course.evaluators.all() or request.user == assignment.unit.course.owner \
                    or request.user.role == 'moderator' or AttendedCourse.objects.filter(user=request.user, course=assignment.unit.course):
                return True
            else:
                raise PermissionDenied({'detail': 'You do not have permission'})

        if request.method == 'POST':
            try:
                some = AssignmentAnswer.objects.get(user=request.user, assignment=assignment)
                print(some)
                raise PermissionDenied({'detail': 'You do not have permission'})
            except AssignmentAnswer.DoesNotExist:
                return True

        return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            raise PermissionDenied({'detail': 'You do not have permission'})

        if request.method in SAFE_METHODS:
            print(AttendedCourse.objects.filter(user=request.user, course=obj.assignment.unit.course))
            if request.user in obj.assignment.unit.course.editors.all() or request.user in obj.assignment.unit.course.managers.all() \
                    or request.user in obj.assignment.unit.course.evaluators.all() or request.user == obj.assignment.unit.course.owner \
                    or request.user.role == 'moderator' \
                    or AttendedCourse.objects.filter(user=request.user, course=obj.assignment.unit.course):
                return True
            raise PermissionDenied({'detail': 'You do not have permission'})

        if request.user in obj.assignment.unit.course.editors.all() or request.user in obj.assignment.unit.course.managers.all() \
                or request.user in obj.assignment.unit.course.evaluators.all() or request.user == obj.assignment.unit.course.owner \
                or request.user.role == 'moderator':
            return True
        raise PermissionDenied({'detail': 'You do not have permission'})


class AnswerPermission(BasePermission):
    def has_permission(self, request, view):
        print(request.user)
        if request.user.is_anonymous:
            raise PermissionDenied({'detail': 'You do not have permission'})

        if request.method == 'POST':

            # get from request all questions id
            input_questions_id = [instance.get('question') if instance.get('type') == 'input' else None for instance
                                  in request.data]
            file_question_id = [instance.get('question') if instance.get('type') == 'file' else None for instance in
                                request.data]
            choice_question_id = [instance.get('question') if instance.get('type') == 'choice' else None for
                                  instance in request.data]

            # get questions from database
            input_questions = FormInputQuestion.objects \
                .select_related('assignment') \
                .prefetch_related('assignment__unit__course__attendedcourse_set') \
                .filter(pk__in=input_questions_id)
            file_questions = FormFileQuestion.objects \
                .select_related('assignment') \
                .prefetch_related('assignment__unit__course__attendedcourse_set') \
                .filter(pk__in=file_question_id)
            choice_questions = FormChoiceQuestion.objects \
                .select_related('assignment') \
                .prefetch_related('assignment__unit__course__attendedcourse_set') \
                .filter(pk__in=choice_question_id)

            # get assignments and check if it's one in all questions and check user permission
            assignment_id = [question.assignment for question in input_questions]
            assignment_id.extend([question.assignment for question in file_questions])
            assignment_id.extend([question.assignment for question in choice_questions])

            if len(set(assignment_id)) > 1:
                raise PermissionDenied({'detail': 'All answers must be bounded to one assignment'})
            assignment = set(assignment_id).pop()
            # if request.user not in [user.user for user in assignment.unit.course.attendedcourse_set.all()] or \
            #         request.user.role != 'moderator':
            print(AttendedCourse.objects.filter(user=request.user, course=assignment.unit.course))
            if not AttendedCourse.objects.filter(user=request.user, course=assignment.unit.course) and \
                    request.user.role != 'moderator':
                raise PermissionDenied({'detail': 'You do not have permission'})
        return True
