from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

from assignmentForm.models import FormInputQuestion, FormFileQuestion, FormChoiceQuestion


class AnswerPermission(BasePermission):
    def has_permission(self, request, view):
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
            if request.user not in [user for user in assignment.unit.course.attendedcourse_set.all()] or \
                    request.user.role != 'moderator':
                raise PermissionDenied({'detail': 'You do not have permission'})
        return True
