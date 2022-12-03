from rest_framework import status
from rest_framework.response import Response

from rest_framework.viewsets import ModelViewSet

from assignmentForm.serializers import *
from assignmentForm.permissions import *


class FormInputQuestionViewSet(ModelViewSet):
    serializer_class = FormInputQuestionSerializer
    permission_classes = [FormInputPermission]

    def get_queryset(self):
        self.check_permissions(self.request)
        return FormInputQuestion.objects.filter(assignment__pk=self.request.data.get('assignment_id'))

    def get_object(self):
        try:
            form_input_question = FormInputQuestion.objects.select_related('assignment').get(pk=self.kwargs.get('form_input_question_pk'))
            self.check_object_permissions(self.request, form_input_question)
            return form_input_question
        except FormInputQuestion.DoesNotExist:
            return None

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        self.check_permissions(request)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        obj = self.get_object()
        if not obj:
            return Response({'detail': 'Indicated form does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(data=request.data, instance=obj)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj:
            obj.delete()
            return Response({'detail': 'Successfully deleted'}, status=status.HTTP_200_OK)
        return Response({'detail': 'Indicated form input question does not exist'}, status=status.HTTP_404_NOT_FOUND)


class FormChoiceQuestionViewSet(ModelViewSet):
    serializer_class = FormChoiceQuestionSerializer
    permission_classes = []

    def get_queryset(self):
        self.check_permissions(self.request)
        return FormChoiceQuestion.objects.select_related('assignment').filter(assignment__pk=self.request.data.get('assignment_pk'))

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(instance=queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        self.check_permissions(request)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
