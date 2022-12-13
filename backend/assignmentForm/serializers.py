from rest_framework.serializers import ModelSerializer

from assignmentForm.models import *


class FormInputQuestionSerializer(ModelSerializer):

    class Meta:
        model = FormInputQuestion
        fields = '__all__'


class FormChoiceQuestionSerializer(ModelSerializer):

    class Meta:
        model = FormChoiceQuestion
        fields = '__all__'


class FormFileQuestionSerializer(ModelSerializer):

    class Meta:
        model = FormFileQuestion
        fields = '__all__'
