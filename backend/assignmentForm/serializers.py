from rest_framework.serializers import ModelSerializer, IntegerField, CharField

from assignmentForm.models import *
from .fields import Base64ImageField


class FormInputQuestionSerializer(ModelSerializer):
    class Meta:
        model = FormInputQuestion
        fields = '__all__'


class FormChoiceQuestionSerializer(ModelSerializer):

    class Meta:
        model = FormChoiceQuestion
        fields = '__all__'
