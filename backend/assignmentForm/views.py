from rest_framework import status
from rest_framework.response import Response

from rest_framework.viewsets import ModelViewSet

from assignmentForm.serializers import *
from assignmentForm.permissions import *


class FormInputQuestionViewSet(ModelViewSet):
    serializer_class = FormInputQuestionSerializer
    permission_classes = [FormQuestionPermission]

    def get_queryset(self):
        self.check_permissions(self.request)
        return FormInputQuestion.objects.filter(assignment__pk=self.request.data.get('assignment'))

    def get_object(self):
        try:
            form_input_question = FormInputQuestion.objects.select_related('assignment').get(pk=self.kwargs.get('form_input_question_pk'))
            self.check_object_permissions(self.request, form_input_question)
            return form_input_question
        except FormInputQuestion.DoesNotExist:
            return None

    def get_assignment(self):
        try:
            return Assignment.objects.get(pk=self.request.data.get('assignment'))
        except Assignment.DoesNotExist:
            return None

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        self.check_permissions(request)
        assignment = self.get_assignment()

        if not assignment:
            return Response({'Indicated assignment does not exist'}, status=status.HTTP_404_NOT_FOUND)
        if not assignment.form_required:
            return Response({'detail': 'This assignment cannot contains input questions'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        obj = self.get_object()
        if not obj:
            return Response({'detail': 'Indicated input question does not exist'}, status=status.HTTP_404_NOT_FOUND)
        if not obj.assignment.form_required:
            return Response({'detail': 'This assignment cannot contains input questions'})
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
        return Response({'detail': 'Indicated input question does not exist'}, status=status.HTTP_404_NOT_FOUND)


class FormChoiceQuestionViewSet(ModelViewSet):
    serializer_class = FormChoiceQuestionSerializer
    permission_classes = [FormQuestionPermission]

    def get_queryset(self):
        self.check_permissions(self.request)
        return FormChoiceQuestion.objects.select_related('assignment').filter(assignment__pk=self.request.data.get('assignment'))

    def get_object(self):
        try:
            choice_question = FormChoiceQuestion.objects.get(pk=self.kwargs.get('choice_question_pk'))
            self.check_object_permissions(self.request, choice_question)
            return choice_question
        except FormChoiceQuestion.DoesNotExist:
            return None

    def get_assignment(self):
        try:
            assignment_id = self.request.data.get('assignment_id') or self.request.data.get('assignment') or None
            return Assignment.objects.get(pk=assignment_id)
        except Assignment.DoesNotExist:
            return None

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not request.data.get('assignment'):
            return Response({'detail': 'There is no indicated assignment'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(instance=queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        self.check_permissions(request)
        assignment = self.get_assignment()
        if not assignment:
            return Response({'detail': 'Indicated assignment does not exist'}, status=status.HTTP_404_NOT_FOUND)
        if not assignment.form_required:
            return Response({'detail': 'This assignment cannot contains choice questions'})
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        obj = self.get_object()
        assignment = self.get_assignment()
        if not assignment:
            return Response({'detail': 'Indicated assignment does not exist'}, status=status.HTTP_404_NOT_FOUND)
        if not assignment.form_required:
            return Response({'detail': 'This assignment cannot contains choice questions'})

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
        return Response({'detail': 'Indicated choice question does not exist'}, status=status.HTTP_404_NOT_FOUND)


class FormFileQuestionViewSet(ModelViewSet):
    serializer_class = FormFileQuestionSerializer
    permission_classes = [FormQuestionPermission]

    def get_queryset(self):
        self.check_permissions(self.request)
        return FormFileQuestion.objects.select_related('assignment').filter(assignment__pk=self.request.data.get('assignment'))

    def get_object(self):
        try:
            file_question = FormFileQuestion.objects.get(pk=self.request.data.get('file_question_pk'))
            self.check_object_permissions(self.request, file_question)
            return file_question
        except FormFileQuestion.DoesNotExist:
            return None

    def get_assignment(self):
        try:
            assignment_id = self.request.data.get('assignment_id') or self.request.data.get('assignment') or None
            return Assignment.objects.get(pk=assignment_id)
        except Assignment.DoesNotExist:
            return None

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not request.data.get('assignment'):
            return Response({'detail': 'There is no indicated assignment'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(instance=queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        self.check_permissions(request)
        assignment = self.get_assignment()
        if not assignment:
            return Response({'detail': 'Indicated assignment does not exist'}, status=status.HTTP_404_NOT_FOUND)
        if not assignment.file_required:
            return Response({'detail': 'This assignment cannot contains file questions'})
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        obj = self.get_object()
        assignment = self.get_assignment()
        if not assignment:
            return Response({'detail': 'Indicated assignment does not exist'}, status=status.HTTP_404_NOT_FOUND)
        if not assignment.form_required:
            return Response({'detail': 'This assignment cannot contains file questions'})

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
        return Response({'detail': 'Indicated file question does not exist'}, status=status.HTTP_404_NOT_FOUND)


class FormChoiceOptionViewSet(ModelViewSet):
    serializer_class = FormChoiceOptionSerializer
    permission_classes = [OptionPermission]

    def get_queryset(self):
        self.check_permissions(self.request)
        try:
            question = FormChoiceQuestion.objects.get(pk=self.request.data.get('question'))
        except FormChoiceQuestion.DoesNotExist:
            return [], False
        return FormChoiceOption.objects.select_related('question')\
            .filter(question__pk=self.request.data.get('question')), True

    def list(self, request, *args, **kwargs):
        queryset, is_valid = self.get_queryset()
        if not is_valid:
            return Response({'detail': 'Indicated question does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        if len(set([instance.get('question') for instance in request.data])) > 1:
            return Response({'detail': 'All choices must be bounded to one question'},
                            status=status.HTTP_400_BAD_REQUEST)

        if not request.data:
            return Response({'detail': 'There is no choices'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        self.check_permissions(request)
        response = []
        for record in request.data:
            try:
                choice = FormChoiceOption.objects.get(pk=record.get('id'))
                record_serializer = self.get_serializer(data=record, instance=choice)
                if record_serializer.is_valid():
                    record_serializer.save()
                    response.append(record_serializer.data)
                    continue
                response.append(record_serializer.errors)
            except FormChoiceOption.DoesNotExist:
                response.append({'id': record.get('id'), 'detail': 'Indicated choice doest not exist'})
        return Response(data=response, status=status.HTTP_200_OK)
