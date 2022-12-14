from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView

from .permissions import AnswerPermission, AnswerAssignmentPermission
from .serializers import *


class AssignmentAnswerCreateUpdateView(ModelViewSet):
    serializer_class = AssignmentAnswerSerializer
    permission_classes = [AnswerAssignmentPermission]

    def get_object(self):
        try:
            obj = AssignmentAnswer.objects\
                .select_related('assignment__unit__course__owner') \
                .prefetch_related('assignment__unit__course__managers',
                                  'assignment__unit__course__managers',
                                  'assignment__unit__course__evaluators') \
                .get(user=self.request.user, assignment=self.request.data.get('assignment'))
            self.check_object_permissions(self.request, obj)
            return obj
        except AssignmentAnswer.DoesNotExist:
            return None

    def retrieve(self, request, *args, **kwargs):
        try:
            assignment = Assignment.objects.get(pk=request.data.get('assignment'))
        except Assignment.DoesNotExist:
            return Response({'detail': 'Indicated assignment answer does not exist'}, status=status.HTTP_404_NOT_FOUND)

        if request.user in assignment.unit.course.editors.all() or request.user in assignment.unit.course.managers.all() \
                or request.user in assignment.unit.course.evaluators.all() or request.user == assignment.unit.course.owner \
                or request.user.role == 'moderator':
            serializer = self.get_serializer(AssignmentAnswer.objects.filter(assignment=assignment), many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        obj = self.get_object()
        if not obj:
            return Response({'detail': 'Indicated assignment answer does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        self.check_permissions(request)
        try:
            AssignmentAnswer.objects.get(assignment__pk=request.data.get('assignment'), user__pk=request.user.id)
            return Response({'detail': 'You have already passed this assignment'}, status=status.HTTP_403_FORBIDDEN)
        except AssignmentAnswer.DoesNotExist:
            serializer = self.get_serializer(data=request.data, context={'user': request.user})
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        obj = AssignmentAnswer.objects.get(pk=request.data.get('id'))
        self.check_object_permissions(request, obj)
        serializer = self.get_serializer(data=request.data, instance=obj)
        if serializer.is_valid():
            serializer.update(obj, dict(serializer.validated_data))
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AssignmentAnswerViewSet(ModelViewSet):
    serializer_class = AssignmentInputAnswerSerializer
    permission_classes = [AnswerPermission]

    def check_choice_answers(self, choice_answers: list):
        questions = list(FormChoiceQuestion.objects.filter(pk__in=[choice.get('question') for choice in choice_answers]))
        if not questions:
            return (True, None)
        for choice in choice_answers:
            founded = False
            for question in questions:
                if choice.get('question') == question.pk:
                    founded = True
                    # if question does not have multiple answers, delete question from the list so that next
                    # iteration return error
                    if not question.is_multiple_answer:
                        questions.remove(question)
                    break
            if not founded:
                return (False, 'You indicate few answers when one is necessary')
        return (True, None)

    def create(self, request, *args, **kwargs):
        self.check_permissions(request)
        input_answers = [answer for answer in request.data if answer.get('type') == 'input']
        file_answers = [answer for answer in request.data if answer.get('type') == 'file']
        choice_answers = [answer for answer in request.data if answer.get('type') == 'choice']
        for answer in input_answers:
            answer['user'] = request.user.id

        for answer in file_answers:
            answer['user'] = request.user.id

        for answer in choice_answers:
            answer['user'] = request.user.id

        go_ahead, detail = self.check_choice_answers(choice_answers)
        if not go_ahead:
            return Response({'detail': detail}, status=status.HTTP_400_BAD_REQUEST)

        # initializing bool for further saving
        input_serializer_valid = True
        file_serializer_valid = True
        choice_serializer_valid = True

        # initializing serializers only if such type of answers is present in request.data
        if input_answers:
            input_serializer = self.get_serializer(data=input_answers, many=True)
            input_serializer_valid = input_serializer.is_valid()
        if file_answers:
            file_serializer = AssigmentFileAnswerSerializer(data=file_answers, many=True)
            file_serializer_valid = file_serializer.is_valid()
        if choice_answers:
            choice_serializer = AssignmentChoiceAnswerSerializer(data=choice_answers, many=True)
            choice_serializer_valid = choice_serializer.is_valid()

        if input_serializer_valid and file_serializer_valid and choice_serializer_valid:
            response = []
            if input_answers:
                input_serializer.save()
                response.extend(input_serializer.data)
            if file_answers:
                file_serializer.save()
                response.extend(file_serializer.data)
            if choice_answers:
                choice_serializer.save()
                response.extend(choice_serializer.data)
            return Response(data=response, status=status.HTTP_201_CREATED)

        return Response({'detail': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)
