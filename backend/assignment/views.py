from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView

from .serializers import *


class AssignmentAnswerCreateUpdateView(CreateAPIView, RetrieveUpdateAPIView):
    serializer_class = AssignmentAnswerSerializer

    def create(self, request, *args, **kwargs):
        try:
            AssignmentAnswer.objects.get(assignment__pk=request.data.get('assignment'), user__pk=request.user.id)
            return Response({'detail': 'You have already passed this assignment'}, status=status.HTTP_403_FORBIDDEN)
        except AssignmentAnswer.DoesNotExist:
            serializer = self.get_serializer(request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AssignmentChoiceAnswerModelViewSet(ModelViewSet):
    serializer_class = AssignmentChoiceAnswerSerializer

    def check_ability_to_answer(self, user_id: str, question_id: str, answer_id: str):
        try:
            question = FormChoiceQuestion.objects.select_related('answer').get(pk=question_id)
            if not question.is_multiple_answer:
                assignment_choice_answers = AssignmentChoiceAnswer.objects.get(user__pk=user_id, question=question)
                if assignment_choice_answers:
                    return False
        except (FormChoiceQuestion.DoesNotExist, AssignmentChoiceAnswer.DoesNotExist) as e:
            if e is FormChoiceQuestion.DoesNotExist:
                return False
            elif e is AssignmentChoiceAnswer.DoesNotExist:
                return True

    def create(self, request, *args, **kwargs):
        self.check_permissions(request)
        if not self.check_ability_to_answer(request.user.id, request.data.get('question'), request.data.get('answer')):
            return Response({'detail': 'You cannot answer on this question'}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
