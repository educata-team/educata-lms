from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .serializers import *


class AssignmentChoiceAnswerModelViewSet(ModelViewSet):
    serializer_class = AssignmentChoiceAnswerSerializer

    def check_ability_to_answer(self, user_id: str, question_id: str, answer_id: str):
        try:
            question = FormChoiceQuestion.objects.select_related('answer').get(pk=question_id)
            if not question.is_multiple_answer:
                assignment_choice_answers = AssignmentChoiceAnswer.objects.get(user__pk=user_id, question=question)
                if assignment_choice_answers:
                    return False
        except (FormChoiceQuestion.DoesNotExist):
            return True

    def create(self, request, *args, **kwargs):
        self.check_permissions(request)
        if not self.check_ability_to_answer(request.user.id, request.data.get('question'), request.data.get('answer')):
            return Response({'detail': 'You cannot answer on this question anymore'}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
