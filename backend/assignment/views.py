from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView

from .permissions import AnswerPermission
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


class AssignmentAnswerViewSet(ModelViewSet):
    serializer_class = AssignmentInputAnswerSerializer
    permission_classes = [AnswerPermission]

    def check_choice_answers(self, choice_answers: list):
        questions = list(FormChoiceQuestion.objects.filter(pk__in=[choice.get('question') for choice in choice_answers]))
        if not questions:
            return True
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
                return False, 'You indicate few answers when one is necessary'
        return True

    def create(self, request, *args, **kwargs):
        self.check_permissions(request)
        input_answers = [answer if answer.get('type') == 'input' else None for answer in request.data]
        file_answers = [answer if answer.get('type') == 'file' else None for answer in request.data]
        choice_answers = [answer if answer.get('type') == 'choice' else None for answer in request.data]

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


class AssignmentChoiceAnswerViewSet(ModelViewSet):
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
        print(request.data)
        if not self.check_ability_to_answer(request.user.id, request.data.get('question'), request.data.get('answer')):
            return Response({'detail': 'You cannot answer on this question'}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(request.data, many=True)
        if serializer.is_valid():
            # serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AssignmentInputAnswerViewSet(ModelViewSet):
    permission_classes = [AnswerPermission]
    serializer_class = AssignmentInputAnswerSerializer

    def check_ability_to_answer(self, user_id: str, question_id: str, answer_id: str):
        try:
            question_id = set()
            question = FormInputQuestion.objects.select_related('answer').get(pk=question_id)
            assignment_input_answers = AssignmentInputAnswer.objects.get(user__pk=user_id, question=question)
            if assignment_input_answers:
                return False
        except (FormInputQuestion.DoesNotExist, AssignmentInputAnswer.DoesNotExist) as e:
            if e is FormInputQuestion.DoesNotExist:
                return False
            elif e is AssignmentInputAnswer.DoesNotExist:
                return True

    def create(self, request, *args, **kwargs):
        self.check_permissions(request)
        print(request.data)
        # if not self.check_ability_to_answer(request.user.id, request.data.get('question'), request.data.get('answer')):
        #     return Response({'detail': 'You cannot answer on this question'}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(data=request.data, many=True)
        if serializer.is_valid():
            print('is valid')
            # serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AssignmentFileAnswerViewSet(ModelViewSet):
    permission_classes = [AnswerPermission]
    serializer_class = AssigmentFileAnswerSerializer

    def check_ability_to_answer(self, user_id: str, question_id: str, answer_id: str):
        try:
            question = FormFileQuestion.objects.select_related('answer').get(pk=question_id)
            assignment_file_answers = AssignmentFileAnswer.objects.get(user__pk=user_id, question=question)
            if assignment_file_answers:
                return False
        except (FormFileQuestion.DoesNotExist, AssignmentFileAnswer.DoesNotExist) as e:
            if e is FormFileQuestion.DoesNotExist:
                return False
            elif e is AssignmentFileAnswer.DoesNotExist:
                return True

    def create(self, request, *args, **kwargs):
        self.check_permissions(request)
        print(request.data)
        if not self.check_ability_to_answer(request.user.id, request.data.get('question'), request.data.get('answer')):
            return Response({'detail': 'You cannot answer on this question'}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(request.data, many=True)
        if serializer.is_valid():
            # serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
