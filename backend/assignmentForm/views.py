from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response

from rest_framework.viewsets import ModelViewSet

from assignmentForm.serializers import *
from assignmentForm.permissions import *


class FormInputQuestionModelViewSet(ModelViewSet):
    serializer_class = FormInputQuestionSerializer
    permission_classes = [FormInputPermission]

    def get_queryset(self):
        self.check_permissions(self.request)
        return FormInputQuestion.objects.filter(assignment__pk=self.request.data.get('assignment_id'))

    def get_object(self):
        try:
            form_input_question = FormInputQuestion.objects.select_related('assignment').get(self.kwargs.get('form_input_question'))
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

    # TODO: decide in which way FormInputQuestion should be updated and set the url
    def update(self, request, *args, **kwargs):
        obj = self.get_object()
        if not obj:
            return Response({'detail': 'Indicated form does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(data=request.data, instance=obj)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
